# Copyright (c) 2018-2020, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#
# Portions Copyright (c) 2025-2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.
#

import asyncio
import collections
import csv
import datetime
import inspect
import json
import logging
import math
import os
import platform
import subprocess
import sys
import threading
import time
import webbrowser
from pathlib import Path

# Static Typing for Dynamic Imports
from typing import TYPE_CHECKING, Any

import carb
import carb.input
import msgpack
import omni.ext
import omni.kit.app
import omni.kit.commands
import omni.kit.menu.utils
import omni.kit.ui
import omni.kit.viewport.utility
import omni.kit.window.property as property_window_ext
import omni.ui as ui
import omni.usd
from omni.kit.menu.utils import MenuItemDescription, MenuLayout
from omni.kit.property.usd import PrimPathWidget
from omni.kit.quicklayout import QuickLayout
from omni.kit.window.title import get_main_window_title

# Use standard USD for main thread updates to ensure compatibility with Hydra
from pxr import Gf, Sdf, Usd, UsdGeom, UsdShade, Vt

if TYPE_CHECKING:
    import warp as wp
    import whoimpg.biologger.subscriber.warp_logic as warp_logic
else:
    # Dummy placeholders for runtime (will be overwritten by dynamic import)
    wp = None
    warp_logic = None

DATA_PATH = Path(carb.tokens.get_tokens_interface().resolve("${whoimpg.biologger.subscriber}"))


async def _load_layout(layout_file: str, keep_windows_open: bool = False) -> None:
    """Loads a provided layout file and ensures the viewport is set to FILL."""
    try:
        # few frames delay to avoid the conflict with the
        # layout of omni.kit.mainwindow
        for _ in range(3):
            await omni.kit.app.get_app().next_update_async()
        QuickLayout.load_file(layout_file, keep_windows_open)

        # HACK: Explicitly hide clutter windows on startup to clean up the UI
        # User requested hiding: Stage, Layer, Render Settings, Properties, Content, Console
        await omni.kit.app.get_app().next_update_async()
        windows_to_hide = [
            "Stage",
            "Layer",
            "Render Settings",
            "Property",
            "Content",
            "Console",
            "Materials",
            "Environments",
            "Variant Presenter",
            "Configurator Samples",
        ]
        for name in windows_to_hide:
            w = ui.Workspace.get_window(name)
            if w:
                w.visible = False

    except Exception:
        QuickLayout.load_file(layout_file)


class CreateSetupExtension(omni.ext.IExt):
    """Create Final Configuration"""

    def on_startup(self, _ext_id: str) -> None:
        """
        setup the window layout, menu, final configuration
        of the extensions etc
        """
        self._settings = carb.settings.get_settings()
        if self._settings and self._settings.get("/app/warmupMode"):
            # if warmup mode is enabled, we don't want to load the stage or
            # layout, just return
            return

        self._menu_layout: list[MenuItemDescription] = []
        self._tasks = set()

        telemetry_logger = logging.getLogger("idl.telemetry.opentelemetry")
        telemetry_logger.setLevel(logging.ERROR)

        # this is a work around as some Extensions don't properly setup their
        # default setting in time
        self._set_defaults()

        # Declare state for Mypy
        self._active_eid: int = -1
        self._stop_event: threading.Event = threading.Event()
        self._thread: threading.Thread | None = None

        # adjust couple of viewport settings
        self._settings.set("/app/viewport/boundingBoxes/enabled", True)
        # Disable Stage Light and enable Camera Light for better underwater visibility
        self._settings.set("/rtx/sceneDb/enableStageLight", False)
        self._settings.set("/rtx/sceneDb/ambientLightIntensity", 0.0)
        # Enable camera headlight
        self._settings.set_default("/rtx/useViewLightingMode", True)

        # These two settings do not co-operate well on ADA cards, so for
        # now simulate a toggle of the present thread on startup to work around
        if self._settings.get(
            "/exts/omni.kit.renderer.core/present/enabled"
        ) and self._settings.get("/exts/omni.kit.widget.viewport/autoAttach/mode"):

            async def _toggle_present(settings: carb.settings.ISettings, n_waits: int = 1) -> None:
                async def _toggle_setting(
                    app: omni.kit.app.IApp, enabled: bool, n_waits: int
                ) -> None:
                    for _ in range(n_waits):
                        await app.next_update_async()
                    settings.set("/exts/omni.kit.renderer.core/present/enabled", enabled)

                app = omni.kit.app.get_app()
                await _toggle_setting(app, False, n_waits)
                await _toggle_setting(app, True, n_waits)

            task = asyncio.ensure_future(_toggle_present(self._settings))
            self._tasks.add(task)
            task.add_done_callback(self._tasks.discard)

        # Setting and Saving FSD as a global change in preferences
        # Requires to listen for changes at the local path to update
        # Composer's persistent path.
        fabric_app_setting = self._settings.get("/app/useFabricSceneDelegate")
        fabric_persistent_setting = self._settings.get("/persistent/app/useFabricSceneDelegate")
        fabric_enabled: bool = (
            fabric_app_setting if fabric_persistent_setting is None else fabric_persistent_setting
        )

        self._settings.set("/app/useFabricSceneDelegate", fabric_enabled)

        self._sub_fabric_delegate_changed = omni.kit.app.SettingChangeSubscription(
            "/app/useFabricSceneDelegate", self._on_fabric_delegate_changed
        )

        # Adjust the Window Title to show the Create Version
        window_title = get_main_window_title()

        app_version = self._settings.get("/app/version")
        if not app_version:
            with open(
                carb.tokens.get_tokens_interface().resolve("${app}/../VERSION"), encoding="utf-8"
            ) as f:
                app_version = f.read()

        if app_version:
            if "+" in app_version:
                app_version, _ = app_version.split("+")

            # for RC version we remove some details
            if self._settings.get("/privacy/externalBuild"):
                if "-" in app_version:
                    app_version, _ = app_version.split("-")
                window_title.set_app_version(app_version)
            else:
                window_title.set_app_version(app_version)

        imgui_style_applied = False
        try:
            # using imgui directly to adjust some color and Variable
            import omni.kit.imgui as _imgui

            imgui = _imgui.acquire_imgui()
            if imgui.is_valid():
                imgui.push_style_color(
                    _imgui.StyleColor.ScrollbarGrab, carb.Float4(0.4, 0.4, 0.4, 1)
                )
                imgui.push_style_color(
                    _imgui.StyleColor.ScrollbarGrabHovered, carb.Float4(0.6, 0.6, 0.6, 1)
                )
                imgui.push_style_color(
                    _imgui.StyleColor.ScrollbarGrabActive, carb.Float4(0.8, 0.8, 0.8, 1)
                )
                imgui.push_style_var_float(_imgui.StyleVar.DockSplitterSize, 2)
                imgui_style_applied = True
        except ImportError:
            pass

        if not imgui_style_applied:
            carb.log_error("Style may not be as expected (carb.imgui was not valid)")

        layout_file = f"{DATA_PATH}/layouts/default.json"

        # Setting to hack few things in test run. Ideally we shouldn't need it.
        test_mode = self._settings.get("/app/testMode")

        if not test_mode:
            task = asyncio.ensure_future(_load_layout(layout_file, True))
            self._tasks.add(task)
            task.add_done_callback(self._tasks.discard)

        task = asyncio.ensure_future(self.__property_window())
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)

        self.__menu_update()

        if not test_mode and not self._settings.get("/app/content/emptyStageOnStart"):
            task = asyncio.ensure_future(self.__new_stage())
            self._tasks.add(task)
            task.add_done_callback(self._tasks.discard)

        startup_time = omni.kit.app.get_app_interface().get_time_since_start_s()
        self._settings.set("/crashreporter/data/startup_time", f"{startup_time}")

        def show_documentation(*args: Any) -> None:
            webbrowser.open("https://docs.omniverse.nvidia.com/composer/latest/index.html")

        self._help_menu_items = [
            MenuItemDescription(
                name="Documentation",
                onclick_fn=show_documentation,
                appear_after=[omni.kit.menu.utils.MenuItemOrder.FIRST],
            )
        ]
        omni.kit.menu.utils.add_menu_items(self._help_menu_items, name="Help")

        # --- WHOI Biologger Subscriber Setup ---
        self._setup_biologger_subscriber()

    async def _load_animal_asset(
        self, species: str, eid: int = 0, sim_id: str = "unknown"
    ) -> str | None:
        print(f"[whoimpg.biologger] Attempting to load animal: {species} (sim_id={sim_id})")
        # Wait for stage to be ready
        stage = None
        # Wait up to ~5 seconds (300 frames at 60fps)
        for _ in range(300):
            await omni.kit.app.get_app().next_update_async()
            stage = omni.usd.get_context().get_stage()
            if stage:
                break

        if not stage:
            print("[whoimpg.biologger] Error: No stage loaded, cannot spawn animal.")
            return None

        # Map scientific names or generic types to asset filenames
        # Extension is responsible for the choice of asset.
        species_map = {
            "xiphias gladius": "swordfish.usd",
            "rhincodon typus": "whale_shark.usd",
            "carcharodon carcharias": "great_white_shark.glb",
            # Fallback/Generic types
            "shark": "great_white_shark.glb",
            "swordfish": "swordfish.usd",
            "whaleshark": "whale_shark.usd",
        }

        asset_filename = species_map.get(species.lower(), "great_white_shark.glb")
        print(f"[whoimpg.biologger] Mapping species '{species}' to asset: {asset_filename}")

        # Resolve absolute path for USD
        # Check common locations
        import os

        cwd = os.getcwd()
        possible_paths = [
            os.path.join(cwd, "source", "assets", asset_filename),
            os.path.join(cwd, "assets", asset_filename),
            os.path.join(cwd, "omniverse", "assets", asset_filename),
        ]

        full_asset_path = None
        for path in possible_paths:
            if os.path.exists(path):
                full_asset_path = path.replace("\\", "/")
                break

        if not full_asset_path:
            print(
                f"[whoimpg.biologger] Error: Could not find asset file {asset_filename} "
                f"in {possible_paths}"
            )
            return None

        print(f"[whoimpg.biologger] Found asset at: {full_asset_path}")

        # Create a new Prim for the animal
        prim_name = f"Animal_{eid}" if eid > 0 else "Animal"
        prim_path = f"/World/{prim_name}"
        prim = stage.DefinePrim(prim_path, "Xform")

        # Set default transform using robust Xformable API
        # We do this BEFORE adding the reference to ensure the prim has a stable
        # transform schema, which helps avoid Fabric "evaluatedTranslations" warnings.
        xformable = UsdGeom.Xformable(prim)
        xformable.ClearXformOpOrder()  # Clear any existing/referenced transforms

        # Add ops with telemetry BEFORE spawn for correct world-space heading rotation.
        # Order: [Translate, Orient:telemetry, RotateXYZ:spawn, Scale]
        #
        # CRITICAL: USD applies ops as M = M_op0 * M_op1 * ... for vertex transform.
        # If spawn is op0 and telemetry is op1: v_world = spawn * telemetry * v_local
        # This applies telemetry in LOCAL space (wrong: Y-rotation doesn't affect Y-axis nose).
        #
        # Correct order: telemetry op0, spawn op1: v_world = telemetry * spawn * v_local
        # This applies spawn first (moving nose from +Y to -Z), THEN telemetry rotates
        # around world Y axis, correctly affecting the -Z nose direction.

        op_translate = xformable.AddTranslateOp()
        # Reserve slot for telemetry orient (will be set dynamically in _update_animal_pose)
        op_orient_telemetry = xformable.AddOrientOp(UsdGeom.XformOp.PrecisionFloat, "telemetry")
        op_rotate = xformable.AddRotateXYZOp()
        op_scale = xformable.AddScaleOp()

        # Set values
        op_translate.Set((0, 0, 0))
        op_orient_telemetry.Set(Gf.Quatf(1, 0, 0, 0))  # Identity until telemetry arrives
        # GLB mesh is authored with nose at +Y. After -90° X rotation, nose points +Z.
        # We add 180° Y to flip nose from +Z to -Z (USD North convention).
        op_rotate.Set((-90, 180, 0))
        op_scale.Set((100, 100, 100))  # Scale: 100 (1m -> 100cm)

        # Add the reference
        references = prim.GetReferences()
        references.AddReference(full_asset_path)

        # Select first animal by default
        if eid == 0 or self._active_eid == -1:
            omni.usd.get_context().get_selection().set_selected_prim_paths([prim_path], False)
            self._active_eid = eid

        print(f"[whoimpg.biologger] Spawned {species} (sim_id={sim_id}) at {prim_path}")
        return prim_path

        # Set initial camera view (from below)
        camera_path = omni.kit.viewport.utility.get_active_viewport_camera_path()
        if camera_path:
            camera_prim = stage.GetPrimAtPath(camera_path)
            if camera_prim.IsValid():
                # Position: Below (-Y) and in front (+Z or -Z depending on model)
                # Shark is at 0,0,0.
                # User requested "below and in front looking head on".
                # Updated: "further away" -> Increase Z distance.
                # Let's try (0, -100, 500) assuming +Z is front/nose-ish.

                cam_pos = Gf.Vec3d(0, -100, 500)
                target_pos = Gf.Vec3d(0, 0, 0)

                look_at_matrix = Gf.Matrix4d().SetLookAt(cam_pos, target_pos, Gf.Vec3d(0, 1, 0))
                cam_matrix = look_at_matrix.GetInverse()

                # Set transform
                xformable = UsdGeom.Xformable(camera_prim)
                # We don't want to clear all ops if it's a complex camera,
                # but for Persp it's usually fine. Better to find existing ops.
                op_translate = None
                op_rotate = None

                for op in xformable.GetOrderedXformOps():
                    if op.GetOpType() == UsdGeom.XformOp.TypeTranslate:
                        op_translate = op
                    elif op.GetOpType() == UsdGeom.XformOp.TypeRotateXYZ:
                        op_rotate = op

                if not op_translate:
                    op_translate = xformable.AddTranslateOp()
                if not op_rotate:
                    op_rotate = xformable.AddRotateXYZOp()

                trans = cam_matrix.ExtractTranslation()
                rot = cam_matrix.ExtractRotation().Decompose(
                    Gf.Vec3d.XAxis(), Gf.Vec3d.YAxis(), Gf.Vec3d.ZAxis()
                )

                op_translate.Set(trans)
                op_rotate.Set(Gf.Vec3f(float(rot[0]), float(rot[1]), float(rot[2])))

    def _setup_biologger_subscriber(self) -> None:
        print("[whoimpg.biologger] Initializing Subscriber...")

        # Initialize state
        self._packet_count = 0
        self._last_vector_str = "N/A"
        self._connection_status = "Disconnected"
        self._latest_quat_data: list[Any] | None = None  # Store latest data for main thread update
        self._latest_data_type: str = "quat"  # "quat" or "euler"
        self._latest_physics_data: dict[str, Any] | None = None
        self._latest_timestamp: float = 0.0
        self._last_flat_forward: Gf.Vec3d | None = None  # For camera follow logic

        # Multi-Entity State
        # Map: eid (int) -> state dict
        # { 'id': view_id, 'pos': Vec3f, 'rot': Quatf, 'path': prim_path, 'data': latest_message }
        self._entities_state: dict[int, dict] = {}
        self._active_eid = -1  # Currently selected/followed entity

        # Metadata Registry
        self._id_to_species: dict[str, str] = {}
        self._load_metadata()

        # Camera Orbit State
        # Azimuth 0° = behind shark (+Z looking toward -Z)
        # Elevation 0° = level with shark, positive = above
        self._cam_azimuth: float = 0.0  # Degrees around shark (0 = behind)
        self._cam_elevation: float = 10.0  # Degrees up - start slightly above for visibility
        self._cam_distance: float = 2500.0  # Start further back for better overview
        self._input = carb.input.acquire_input_interface()
        self._input_sub_id = None
        self._is_rmb_down = False
        self._last_mouse_pos = (0.0, 0.0)
        self._last_mouse_pos_valid: bool = False

        # Trail State
        # NOTE: Refactored for Instant Replay/Time-Travel support
        # _trail_buffer stores tuples of (timestamp, Gf.Vec3f, Gf.Quatf, ODBA)
        # This acts as the "Infinite Track" memory.
        self._trail_buffer: list[tuple[float, Gf.Vec3f, Gf.Quatf, float]] = []
        self._trail_times: list[float] = []  # Optimized lookup for bisect
        self._trail_prim_path = "/World/Trail"
        self._last_trail_update_ms = 0.0

        # Temporal Replay State
        self._replay_live_time: float = 0.0  # The latest timestamp received from ZMQ
        self._replay_playhead: float = 0.0  # The current view time (from Timeline)
        self._session_start_time: float = 0.0  # First received timestamp

        # Callibration State
        self._offset_roll = 0.0
        self._offset_pitch = 0.0
        self._offset_heading = 0.0

        # Safe Mode State
        # If True: Disables history buffer and replay to save memory/performance
        # Check startup flag via kit argument (e.g. --/biologger/safe_mode=1)
        safe_mode_cfg = self._settings.get("/biologger/safe_mode")
        self._safe_mode = bool(safe_mode_cfg) if safe_mode_cfg is not None else False
        if self._safe_mode:
            print("[whoimpg.biologger] Safe Mode enabled via startup config.")

        # Backend Config
        # --/biologger/backend=warp (or cpu)
        self._backend = self._settings.get("/biologger/backend") or "cpu"
        print(f"[whoimpg.biologger] Backend Selected: {self._backend}")

        if self._backend == "warp":
            print("[whoimpg.biologger] Initializing Warp...")
            try:
                global wp, warp_logic
                import warp as wp
                import whoimpg.biologger.subscriber.warp_logic as warp_logic

                wp.init()
                print("[whoimpg.biologger] Warp Initialized successfully.")
            except ImportError as e:
                print(f"[whoimpg.biologger] Failed to import Warp/Kernel: {e}")
                print("[whoimpg.biologger] Fallback to CPU backend.")
                self._backend = "cpu"

        # Diagnostics State
        # Accumulator for slip angles to track mean/max bias
        self._slip_history: collections.deque[float] = collections.deque(maxlen=1000)

        # Initialize Logger handles
        self._csv_writer: Any = None
        self._csv_file: Any = None
        self._csv_log_path = "N/A"

        # Logging Setup
        # Structure: omniverse-logs/YYYYMMDD-HHMMSS_omniverse_session/
        timestamp_str = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        session_name = "omniverse_session"

        # Base log dir: Find the repo root robustly
        try:
            current_path = Path(__file__).resolve().parent
            repo_root = current_path

            # 1. Explicit Check: Are we in a _build folder? (Common in Kit apps)
            # Look for "_build" in the path components
            # Note: We iterate to find the *first* occurrence if nested (unlikely but safe)
            if "_build" in current_path.parts:
                idx = current_path.parts.index("_build")
                # Slice parts up to _build and reconstruct path
                # parts[0] is usually drive/root, so Path(*parts) works on Win/Linux
                repo_root = Path(*current_path.parts[:idx])
            else:
                # 2. Marker Check: Walk up looking for repo configuration files
                for parent in [current_path, *list(current_path.parents)]:
                    if (parent / "repo.toml").exists() or (parent / "environment.yml").exists():
                        repo_root = parent
                        break

            base_log_dir = str(repo_root / "omniverse-logs")
            print(f"[whoimpg.biologger] Resolved Repo Root for Logs: {repo_root}")

        except Exception as e:
            print(f"[whoimpg.biologger] Error resolving root, falling back to CWD: {e}")
            base_log_dir = os.path.join(os.getcwd(), "omniverse-logs")

        # Create omniverse-logs if it doesn't exist at the discovered root
        if not os.path.exists(base_log_dir):
            try:
                os.makedirs(base_log_dir, exist_ok=True)
            except Exception:
                # Fallback to CWD if we can't write to the resolved root
                base_log_dir = os.path.join(os.getcwd(), "omniverse-logs")
                os.makedirs(base_log_dir, exist_ok=True)

        self._session_dir: str | None = os.path.join(
            base_log_dir, f"{timestamp_str}_{session_name}"
        )

        try:
            os.makedirs(self._session_dir, exist_ok=True)
            print(f"[whoimpg.biologger] Created session log dir: {self._session_dir}")
        except Exception as e:
            print(f"[whoimpg.biologger] Failed to create log dir {self._session_dir}: {e}")
            self._session_dir = None

        if self._session_dir:
            # 1. Open CSV Log
            # Note: File must remain open for the entire session, so we don't use 'with'
            # It will be closed in on_shutdown()
            self._csv_log_path = os.path.join(self._session_dir, "slip_log.csv")
            try:
                self._csv_file = open(self._csv_log_path, "w", newline="")  # noqa: SIM115
                self._csv_writer = csv.writer(self._csv_file)
                self._csv_writer.writerow(
                    [
                        "Timestamp",
                        "SlipAngle",
                        "Speed",
                        "Vx",
                        "Vy",
                        "Vz",
                        "Hx",
                        "Hy",
                        "Hz",
                        "NED_Heading",
                    ]
                )
            except Exception as e:
                print(f"[whoimpg.biologger] Failed to open CSV log: {e}")
                self._csv_file = None
                self._csv_writer = None

            # 2. Write Config Log
            config_log_path = os.path.join(self._session_dir, "config.json")
            try:
                # Capture current relevant settings
                cfg = {
                    "cmdline": sys.argv,
                    "offsets": {
                        "roll": self._offset_roll,
                        "pitch": self._offset_pitch,
                        "heading": self._offset_heading,
                    },
                    "safe_mode": self._safe_mode,
                    "csv_log_path": self._csv_log_path,
                }
                with open(config_log_path, "w") as f:
                    json.dump(cfg, f, indent=4)
            except Exception as e:
                print(f"[whoimpg.biologger] Failed to write config log: {e}")
        print(f"[whoimpg.biologger] Logging slip diagnostics to: {self._csv_log_path}")

        # Throughput calculation

        # Throughput calculation
        self._packets_since_last_update = 0
        self._last_throughput_time = time.time()
        self._throughput_str = "0.0 pkts/s"

        # 1. Setup the UI Dashboard (Overlay style)
        # Using a small window in the top-left corner as a HUD
        self._window = ui.Window(
            "Biologger Data", width=300, height=500, dockPreference=ui.DockPreference.LEFT
        )
        with (
            self._window.frame,
            ui.ScrollingFrame(
                horizontal_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_OFF,
                vertical_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_AS_NEEDED,
            ),
            ui.VStack(height=0, spacing=1),
        ):
            self._status_label = ui.Label("Status: Disconnected", style={"color": 0xFF888888})
            self._packet_label = ui.Label("Packets: 0")
            self._throughput_label = ui.Label("Throughput: 0.0 pkts/s")
            self._time_label = ui.Label("Time: N/A")
            self._vector_label = ui.Label("Orientation: N/A")
            self._slip_label = ui.Label("Slip Angle: N/A")
            self._cam_pos_label = ui.Label("Cam Pos: N/A", style={"color": 0xFFAAAAAA})
            self._physics_label = ui.Label("Physics: N/A")
            self._perf_label = ui.Label("Trail Update: -- ms", style={"color": 0xFFAAAAAA})

            ui.Spacer(height=5)
            self._tracking_options_frame = ui.CollapsableFrame("Tracking Options", collapsed=False)
            with self._tracking_options_frame, ui.VStack(spacing=5):
                # Live Sync
                with ui.HStack(height=20):
                    self._live_sync_checkbox = ui.CheckBox(model=ui.SimpleBoolModel(True), width=20)
                    ui.Label("Live Sync (Follow Stream)")

                # Position Tracking
                with ui.HStack(height=20):
                    self._position_tracking_checkbox = ui.CheckBox(width=20)
                    self._position_tracking_checkbox.model.set_value(True)
                    ui.Label("Enable Position Tracking")

                with ui.HStack(height=20):
                    self._follow_mode_checkbox = ui.CheckBox(width=20)
                    self._follow_mode_checkbox.model.set_value(False)
                    self._follow_mode_checkbox.model.add_value_changed_fn(
                        self._on_follow_mode_changed
                    )
                    ui.Label("Follow Mode (3rd Person)")

                with ui.HStack(height=20):
                    self._trail_checkbox = ui.CheckBox(width=20)
                    self._trail_checkbox.model.set_value(True)  # Default On
                    self._trail_checkbox.model.add_value_changed_fn(self._on_trail_mode_changed)
                    ui.Label("Show Trail")

                with ui.HStack(height=20):
                    self._debug_vec_checkbox = ui.CheckBox(width=20)
                    self._debug_vec_checkbox.model.set_value(False)
                    ui.Label("Show Debug Vectors")

            ui.Spacer(height=5)
            ui.Label("Performance & Safety", style={"color": 0xFFAAAAAA})

            with ui.HStack(height=20):
                self._safe_mode_checkbox = ui.CheckBox(model=ui.SimpleBoolModel(self._safe_mode))
                self._safe_mode_checkbox.model.add_value_changed_fn(self._on_safe_mode_changed)
                # If enabled via config, lock UI immediately
                if self._safe_mode:
                    self._safe_mode_checkbox.enabled = False
                ui.Label("Safe Mode (Live Only)")

            ui.Spacer(height=5)
            # Timeline Access (UX Helper)
            ui.Button("Show Timeline & Playback Controls", clicked_fn=self._show_timeline_window)

            ui.Spacer(height=5)
            with (
                ui.CollapsableFrame("Camera Settings", collapsed=True),
                ui.VStack(spacing=5),
                ui.HStack(height=20),
            ):
                ui.Label("Damping:", width=60)
                # Increased max damping to 1.0 (instant) to allow user tuning
                self._camera_damping_field = ui.FloatSlider(min=0.001, max=1.0)
                # Default increased to 0.1 for more responsive control (less spin/drift)
                self._camera_damping_field.model.set_value(0.1)

            ui.Spacer(height=5)
            with ui.CollapsableFrame("Model Alignment", collapsed=True), ui.VStack(spacing=5):
                with ui.HStack(height=20):
                    ui.Label("Offset Roll:", width=80)
                    self._offset_roll_slider = ui.FloatSlider(min=-180, max=180)
                    self._offset_roll_slider.model.set_value(0.0)
                    self._offset_roll_slider.model.add_value_changed_fn(self._on_align_changed)

                with ui.HStack(height=20):
                    ui.Label("Offset Pitch:", width=80)
                    self._offset_pitch_slider = ui.FloatSlider(min=-180, max=180)
                    self._offset_pitch_slider.model.set_value(0.0)
                    self._offset_pitch_slider.model.add_value_changed_fn(self._on_align_changed)

                with ui.HStack(height=20):
                    ui.Label("Offset Head:", width=80)
                    self._offset_heading_slider = ui.FloatSlider(min=-180, max=180)
                    self._offset_heading_slider.model.set_value(0.0)
                    self._offset_heading_slider.model.add_value_changed_fn(self._on_align_changed)

            ui.Spacer(height=5)
            with ui.CollapsableFrame("ZMQ Configuration", collapsed=True), ui.VStack(spacing=5):
                with ui.HStack(height=20):
                    ui.Label("Host:", width=40)
                    self._host_field = ui.StringField()
                    self._host_field.model.set_value("127.0.0.1")

                with ui.HStack(height=20):
                    ui.Label("Port:", width=40)
                    self._port_field = ui.IntField()
                    self._port_field.model.set_value(5555)

                with ui.HStack(height=20):
                    ui.Button("Reconnect", clicked_fn=self._restart_listener)
                    ui.Spacer(width=5)
                    ui.Button("Reset Orientation", clicked_fn=self._reset_orientation)

        # 2. Fabric setup for the animal prim (e.g., /World/Shark)
        # Note: This assumes the stage is already open or will be opened.
        # We might need to refresh this if the stage changes.
        self._stage = None
        # We will attach to stage in the update loop to be safe

        # 3. Auto-connect on startup
        self._start_listener()
        self._is_running = True

        # 4. Setup UI update loop (safe way to update UI from main thread)
        self._update_sub = (
            omni.kit.app.get_app()
            .get_update_event_stream()
            .create_subscription_to_pop(self._on_update_ui, name="whoimpg.biologger.update")
        )

    def _on_update_ui(self, _: Any) -> None:
        """Called every frame to update UI elements safely"""
        # Call the main 3D update loop
        self._update_prim(_)

        # Calculate throughput
        current_time = time.time()
        if current_time - self._last_throughput_time >= 1.0:
            rate = self._packets_since_last_update / (current_time - self._last_throughput_time)
            self._throughput_str = f"{rate:.1f} pkts/s"
            self._packets_since_last_update = 0
            self._last_throughput_time = current_time

        if self._window:
            self._status_label.text = f"Status: {self._connection_status}"
            self._packet_label.text = f"Packets: {self._packet_count}"
            self._throughput_label.text = f"Throughput: {self._throughput_str}"

            self._perf_label.text = f"Trail: {self._last_trail_update_ms:.2f} ms"

            if self._latest_timestamp > 0:
                dt = datetime.datetime.fromtimestamp(
                    self._latest_timestamp, tz=datetime.timezone.utc
                )
                self._time_label.text = f"Time: {dt.strftime('%Y-%m-%d %H:%M:%S')}"
            else:
                self._time_label.text = "Time: N/A"

            self._vector_label.text = f"Orientation: {self._last_vector_str}"

            # --- Calculate Slip Angle ---
            if self._trail_buffer and len(self._trail_buffer) >= 2:
                # Use last two points to estimate movement vector
                p_now = self._trail_buffer[-1]
                p_prev = self._trail_buffer[-2]

                # Position is index 1
                pos_cur = p_now[1]
                pos_old = p_prev[1]

                # Velocity Vector (World Space movement)
                dx = pos_cur[0] - pos_old[0]
                dy = pos_cur[1] - pos_old[1]
                dz = pos_cur[2] - pos_old[2]
                dist = math.sqrt(dx * dx + dy * dy + dz * dz)

                if dist > 0.1:  # Threshold to avoid noise/zeros
                    # Normalized Velocity Dir
                    vx, vy, vz = dx / dist, dy / dist, dz / dist

                    # Heading Vector (Realized Pose)
                    # Asset Forward is -Z in local space
                    rot = p_now[2]  # Quatf
                    # Transform (0,0,-1) for Standard USD Forward
                    fwd = rot.Transform(Gf.Vec3f(0, 0, -1))

                    # Dot Product
                    dot = vx * fwd[0] + vy * fwd[1] + vz * fwd[2]
                    dot = max(-1.0, min(1.0, dot))
                    angle = math.degrees(math.acos(dot))

                    # Update accumulator
                    self._slip_history.append(angle)

                    # Log to CSV
                    try:
                        if self._csv_writer and self._csv_file:
                            # Get NED heading if available
                            ned_h = getattr(self, "_last_ned_heading", 0.0)
                            self._csv_writer.writerow(
                                [
                                    f"{current_time:.3f}",
                                    f"{angle:.4f}",
                                    f"{dist:.4f}",
                                    f"{vx:.4f}",
                                    f"{vy:.4f}",
                                    f"{vz:.4f}",
                                    f"{fwd[0]:.4f}",
                                    f"{fwd[1]:.4f}",
                                    f"{fwd[2]:.4f}",
                                    f"{ned_h:.2f}",
                                ]
                            )
                            if self._packet_count % 60 == 0:
                                self._csv_file.flush()
                    except Exception as e:
                        print(f"Logging error: {e}")

                    # Compute Stats
                    avg_slip = sum(self._slip_history) / len(self._slip_history)
                    max_slip = max(self._slip_history)

                    self._slip_label.text = (
                        f"Slip: {angle:.1f}° (Avg: {avg_slip:.1f}° Max: {max_slip:.1f}°)"
                    )
                else:
                    self._slip_label.text = "Slip: < 0.1 m/s"

            # --- Update Camera Pos ---
            try:
                cam_path = omni.kit.viewport.utility.get_active_viewport_camera_path()
                stage = omni.usd.get_context().get_stage()
                if stage and cam_path:
                    cam_prim = stage.GetPrimAtPath(cam_path)
                    if cam_prim.IsValid():
                        # Use World Transform
                        xform = UsdGeom.Xformable(cam_prim).ComputeLocalToWorldTransform(
                            Usd.TimeCode.Default()
                        )
                        trans = xform.ExtractTranslation()
                        self._cam_pos_label.text = (
                            f"Cam: ({trans[0]:.0f}, {trans[1]:.0f}, {trans[2]:.0f})"
                        )
            except Exception:
                pass  # Ignore camera UI errors

            if self._latest_physics_data:
                p = self._latest_physics_data
                accel = p.get("accel_dynamic", [0, 0, 0])
                # Handle case where accel might be None or not a list
                if not isinstance(accel, list) or len(accel) < 3:
                    accel = [0.0, 0.0, 0.0]

                accel_str = f"[{accel[0]:.2f}, {accel[1]:.2f}, {accel[2]:.2f}]"

                # Extract position if available
                pos_x = p.get("pseudo_x", 0.0)
                pos_y = p.get("pseudo_y", 0.0)

                self._physics_label.text = (
                    f"D: {p.get('depth', 0):.1f}m | V: {p.get('velocity', 0):.1f}m/s\n"
                    f"Pos: ({pos_x:.1f}, {pos_y:.1f})\n"
                    f"ODBA: {p.get('odba', 0):.2f} | VeDBA: {p.get('vedba', 0):.2f}\n"
                    f"DynAccel: {accel_str}"
                )

    def _compute_orientation(self, q_data: list[float], is_euler: bool = True) -> Gf.Quatf:
        """
        Single source of truth for orientation calculation.
        Handles coordinate system mapping and offsets.
        """
        if is_euler:
            # Final Derived Mapping:
            # Matches Logic in _zmq_listener_loop and _update_animal_pose
            # p_val (Pitch, q[1]) -> X
            # r_val (Roll, q[0]) -> Y
            # h_val (Heading, q[2]) -> Z

            # Safely get offsets (default to 0.0 if not initialized)
            off_p = getattr(self, "_offset_pitch", 0.0)
            off_r = getattr(self, "_offset_roll", 0.0)
            off_h = getattr(self, "_offset_heading", 0.0)

            # Standard NED -> USD Y-Up Mapping
            # NED uses clockwise heading (N=0° → E=90° → S=180° → W=270°)
            # USD Y-Up uses right-hand rule: positive Y rotation is CCW from above
            #
            # Mapping:
            # 1. Heading (q[2]): Maps to Y-Axis rotation, but NEGATED to convert
            #    CW compass heading to CCW USD rotation.
            #    NED +90° (East) → USD -90° → forward vector points +X (East)
            # 2. Pitch (q[1]): Maps to X-Axis (Right). Nose-up is positive.
            # 3. Roll (q[0]): Maps to -Z-Axis (Forward) for Right-Hand-Rule "Right Bank".

            p = float(q_data[1]) + off_p
            h_raw = float(q_data[2]) + off_h
            h = -h_raw  # NEGATE: CW compass → CCW USD
            r = float(q_data[0]) + off_r

            # Store raw heading for CSV logging
            self._last_ned_heading = h_raw

            # Create Rotations
            rot_yaw = Gf.Rotation(Gf.Vec3d(0, 1, 0), h)  # Heading around Y (negated above)
            rot_pitch = Gf.Rotation(Gf.Vec3d(1, 0, 0), p)  # Pitch around X
            rot_roll = Gf.Rotation(
                Gf.Vec3d(0, 0, -1), r
            )  # Roll around -Z (Bank Right = CW from behind)

            # Apply rotations: Yaw (Global) -> Pitch -> Roll
            rot = rot_yaw * rot_pitch * rot_roll
            q = rot.GetQuat()
            return Gf.Quatf(
                float(q.GetReal()),
                float(q.GetImaginary()[0]),
                float(q.GetImaginary()[1]),
                float(q.GetImaginary()[2]),
            )
        else:
            return Gf.Quatf(q_data[0], q_data[1], q_data[2], q_data[3])

    def _update_animal_pose(self, stage: Usd.Stage, eid: int, state: dict) -> None:
        """
        Updates the Position and Rotation of a specific Animal Prim.
        """
        try:
            prim_path = state.get("path")
            if not prim_path:
                return  # Still spawning or not found

            prim = stage.GetPrimAtPath(prim_path)
            if not prim.IsValid():
                return

            # Extract data from state
            rot_data = state.get("rot_data")
            phys = state.get("phys", {})

            target_pos: Gf.Vec3d | None = None
            target_rot_quat: Gf.Quatf | None = None

            # Always Live for now in multi-entity mode (Simplified)
            if phys:
                depth = float(phys.get("d", 0.0))
                px = float(phys.get("px", 0.0))
                py = float(phys.get("py", 0.0))

                # Legacy/CPU Mapping: Y=-depth, X=pseudo_y, Z=-pseudo_x
                target_pos = Gf.Vec3d(py * 100.0, -depth * 100.0, -px * 100.0)

            if rot_data:
                target_rot_quat = self._compute_orientation(rot_data, is_euler=True)

            # Apply Position
            if target_pos:
                xformable = UsdGeom.Xformable(prim)
                translate_op = None
                for op in xformable.GetOrderedXformOps():
                    if op.GetOpType() == UsdGeom.XformOp.TypeTranslate:
                        translate_op = op
                        break
                if not translate_op:
                    translate_op = xformable.AddTranslateOp()
                translate_op.Set(target_pos)

            # Apply Rotation
            if target_rot_quat:
                xformable = UsdGeom.Xformable(prim)
                rotate_op_name = "xformOp:orient:telemetry"
                rotate_op = None
                for op in xformable.GetOrderedXformOps():
                    if op.GetOpName() == rotate_op_name:
                        rotate_op = op
                        break
                if rotate_op:
                    rotate_op.Set(target_rot_quat)

        except Exception as e:
            if not hasattr(self, "_pose_error_shown"):
                print(f"[whoimpg.biologger] Error updating pose: {e}")
                self._pose_error_shown = True

    def _update_prim(self, stage_event: Any) -> None:
        """Main update loop triggered every frame."""
        try:
            stage = omni.usd.get_context().get_stage()
            if not stage:
                return

            # Iterate over all registered entities and update their poses
            for eid, state in self._entities_state.items():
                # Auto-spawn if path is missing
                if not state.get("path"):
                    species = state.get("sp", "shark")
                    sim_id_str = state.get("id", "unknown")
                    # Use asyncio for asset loading as it may take time
                    task = asyncio.ensure_future(self._load_animal_asset(species, eid, sim_id_str))
                    state["path"] = "PENDING"

                    def _on_spawn_done(t: asyncio.Task, eid: int = eid) -> None:
                        try:
                            res = t.result()
                            self._entities_state[eid]["path"] = res
                        except Exception as e:
                            print(f"Error spawning eid {eid}: {e}")

                    task.add_done_callback(_on_spawn_done)
                    continue

                if state.get("path") != "PENDING":
                    self._update_animal_pose(stage, eid, state)

            # Camera follow logic (for active entity)
            active_state = self._entities_state.get(self._active_eid)
            if active_state and active_state.get("path") and active_state.get("path") != "PENDING":
                prim = stage.GetPrimAtPath(active_state["path"])
                if prim and prim.IsValid():
                    self._update_camera_follow(stage, prim)
        except Exception as e:
            if not hasattr(self, "_update_error_shown"):
                print(f"[whoimpg.biologger] Error updating prim: {e}")
                import traceback

                traceback.print_exc()
                self._update_error_shown = True

    def _on_follow_mode_changed(self, model: ui.AbstractValueModel) -> None:
        enabled = model.get_value_as_bool()
        self._follow_mode_enabled = enabled  # CRITICAL: Set the flag!
        print(f"[whoimpg.biologger] Follow mode changed: {enabled}")

        if enabled:
            # Store current camera to restore later
            self._previous_camera_path = omni.kit.viewport.utility.get_active_viewport_camera_path()

            # Create follow camera if needed
            self._ensure_follow_camera()

            # Switch to follow camera
            self._set_active_camera("/World/FollowCamera")

            # CRITICAL: Disable viewport navigation so it doesn't override our camera transforms
            try:
                viewport_window = omni.kit.viewport.utility.get_active_viewport_window()
                if viewport_window and hasattr(viewport_window, "viewport_api"):
                    # Store current navigation state to restore later
                    # Disable camera manipulation (mouse/keyboard navigation)
                    # This prevents the viewport from overriding our transforms
                    settings = carb.settings.get_settings()
                    self._viewport_nav_enabled = settings.get(
                        "/persistent/app/viewport/camManipulation/enabled"
                    )
                    settings.set("/persistent/app/viewport/camManipulation/enabled", False)
            except Exception as e:
                print(f"[whoimpg.biologger] Could not disable viewport navigation: {e}")

            # Subscribe to input events for orbit control
            if not self._input_sub_id:
                # Note: DEFAULT_SUBSCRIPTION_ORDER might be missing in some Kit versions.
                # Using a very low number (high priority) to consume events before the Viewport.
                self._input_sub_id = self._input.subscribe_to_input_events(
                    self._on_input_event,
                    order=-1000,
                )
                print(
                    f"[whoimpg.biologger] Subscribed to input events, sub_id={self._input_sub_id}"
                )
        else:
            # Unsubscribe from input events
            if self._input_sub_id:
                self._input.unsubscribe_to_input_events(self._input_sub_id)
                self._input_sub_id = None

            # Re-enable viewport navigation
            try:
                if hasattr(self, "_viewport_nav_enabled"):
                    settings = carb.settings.get_settings()
                    settings.set(
                        "/persistent/app/viewport/camManipulation/enabled",
                        self._viewport_nav_enabled,
                    )
                    delattr(self, "_viewport_nav_enabled")
            except Exception as e:
                print(f"[whoimpg.biologger] Could not restore viewport navigation: {e}")

            # Restore previous camera
            path = "/OmniverseKit_Persp"
            if hasattr(self, "_previous_camera_path") and self._previous_camera_path:
                path = self._previous_camera_path

            self._set_active_camera(path)

    def _on_input_event(self, event: carb.input.InputEvent) -> bool:
        """Handle input for camera orbit (Keyboard Only - WASD + Arrows)"""
        # Debug: Print any input event we receive
        print(
            f"[whoimpg.biologger] Input event: device={event.deviceType}, "
            f"follow_mode={self._follow_mode_enabled}"
        )

        # Mouse logic removed per user request to "leave the mouse alone while in follow mode"
        # Only keyboard controls will intercept input.
        if event.deviceType == carb.input.DeviceType.MOUSE:
            return False  # Pass through all mouse events (Selection, UI interaction)

        # Handle Keyboard Input
        elif event.deviceType == carb.input.DeviceType.KEYBOARD and (
            event.event.type == carb.input.KeyboardEventType.KEY_PRESS
            or event.event.type == carb.input.KeyboardEventType.KEY_REPEAT
        ):
            key = event.event.input
            sensitivity = 5.0

            # Helper to safely check key codes (handles A vs KEY_A,
            # LEFT vs LEFT_ARROW variations)
            def is_key(k: Any, names: list[str]) -> bool:
                return any(k == getattr(carb.input.KeyboardInput, name, -999) for name in names)

            # Azimuth (Orbit Left/Right) - WASD Only
            if is_key(key, ["A", "KEY_A"]):
                self._cam_azimuth += sensitivity  # Positive to orbit left
                print(f"[whoimpg.biologger] Key: A → Azimuth: {self._cam_azimuth:.1f}°")
                return True
            elif is_key(key, ["D", "KEY_D"]):
                self._cam_azimuth -= sensitivity  # Negative to orbit right
                print(f"[whoimpg.biologger] Key: D → Azimuth: {self._cam_azimuth:.1f}°")
                return True

            # Elevation (Orbit Up/Down) - WASD Only
            # Clamp to ±89 degrees to avoid gimbal lock at vertical (±90)
            elif is_key(key, ["W", "KEY_W"]):
                self._cam_elevation += sensitivity
                self._cam_elevation = min(89.0, self._cam_elevation)  # Clamp to 89 max
                print(f"[whoimpg.biologger] Key: W → Elevation: {self._cam_elevation:.1f}°")
                return True
            elif is_key(key, ["S", "KEY_S"]):
                self._cam_elevation -= sensitivity
                self._cam_elevation = max(-89.0, self._cam_elevation)  # Clamp to -89 min
                print(f"[whoimpg.biologger] Key: S → Elevation: {self._cam_elevation:.1f}°")
                return True

            # Zoom (Distance) - Up/Down Arrows (and +/- fallback)
            elif is_key(
                key, ["UP", "UP_ARROW", "KEY_UP", "EQUAL", "KEY_EQUAL", "PLUS", "KEY_PLUS"]
            ):
                # Update internal distance state
                if not hasattr(self, "_cam_distance"):
                    self._cam_distance = 1500.0
                self._cam_distance -= 100.0  # Zoom In (Closer)
                self._cam_distance = max(100.0, min(5000.0, self._cam_distance))
                print(f"[whoimpg.biologger] Key: UP → Distance: {self._cam_distance:.0f}")
                return True
            elif is_key(key, ["DOWN", "DOWN_ARROW", "KEY_DOWN", "MINUS", "KEY_MINUS"]):
                if not hasattr(self, "_cam_distance"):
                    self._cam_distance = 1500.0
                self._cam_distance += 100.0  # Zoom Out (Further)
                self._cam_distance = max(100.0, min(5000.0, self._cam_distance))
                print(f"[whoimpg.biologger] Key: DOWN → Distance: {self._cam_distance:.0f}")
                return True

            # Shortcuts for Window Toggles
            elif is_key(key, ["F5"]):
                w = ui.Workspace.get_window("Stage")
                if w:
                    w.visible = not w.visible
                    print(f"[whoimpg.biologger] Toggled Stage Window: {w.visible}")
                return True

            elif is_key(key, ["F6"]):
                # Timeline is sometimes part of a different layout or name
                w = ui.Workspace.get_window("Timeline")
                if w:
                    w.visible = not w.visible
                    print(f"[whoimpg.biologger] Toggled Timeline Window: {w.visible}")
                return True

            # Left/Right Arrows are unmapped per user request

            # Ensure elevation allows full verticality (-90 to +90)
            self._cam_elevation = max(-90.0, min(90.0, self._cam_elevation))

        return False  # Pass through other events

    def _set_active_camera(self, camera_path: str) -> None:
        """
        Set the active camera using modern Kit 105+ APIs.

        Prioritizes the Viewport Window API (viewport_api.camera_path).
        Falls back to 'LookThroughCamera' command if the direct API is unavailable.
        Legacy methods (Kit <105) have been deprecated and removed.
        """
        print(f"[whoimpg.biologger] Switching camera to: {camera_path}")

        # Method 1: Try Viewport Window API (Direct & Preferred for Kit 105+)
        # This allows setting the camera without populating the undo stack (which is often preferred
        # during simulation playback) and works reliably when the Viewport extension is active.
        try:
            viewport_window = omni.kit.viewport.utility.get_active_viewport_window()
            if viewport_window and hasattr(viewport_window, "viewport_api"):
                viewport_window.viewport_api.camera_path = camera_path
                return
        except Exception as e:
            print(f"[whoimpg.biologger] Viewport Window API failed: {e}")

        # Method 2: Try LookThroughCamera command (Standard Fallback)
        try:
            omni.kit.commands.execute("LookThroughCamera", camera_path=camera_path)
            return
        except Exception as e:
            print(f"[whoimpg.biologger] Command 'LookThroughCamera' failed: {e}")

        print("[whoimpg.biologger] Error: Could not switch camera (all methods failed).")

    def _ensure_follow_camera(self) -> None:
        stage = omni.usd.get_context().get_stage()
        if not stage:
            return

        camera_path = "/World/FollowCamera"
        if not stage.GetPrimAtPath(camera_path).IsValid():
            camera = UsdGeom.Camera.Define(stage, camera_path)
            # Set some default properties
            camera.GetFocalLengthAttr().Set(24)  # Wide angle
            camera.GetFocusDistanceAttr().Set(400)

            # Add xform ops (separate translate and rotate for USD/viewport compatibility)
            xformable = UsdGeom.Xformable(camera)
            xformable.AddTranslateOp()
            xformable.AddRotateXYZOp()

    def _on_align_changed(self, model: ui.AbstractValueModel) -> None:
        self._offset_roll = self._offset_roll_slider.model.get_value_as_float()
        self._offset_pitch = self._offset_pitch_slider.model.get_value_as_float()
        self._offset_heading = self._offset_heading_slider.model.get_value_as_float()

    def _on_trail_mode_changed(self, model: ui.AbstractValueModel) -> None:
        enabled = model.get_value_as_bool()
        stage = omni.usd.get_context().get_stage()
        if not stage:
            return

        prim = stage.GetPrimAtPath(self._trail_prim_path)
        if prim.IsValid():
            imageable = UsdGeom.Imageable(prim)
            if enabled:
                imageable.MakeVisible()
            else:
                imageable.MakeInvisible()

    def _on_safe_mode_changed(self, model: ui.AbstractValueModel) -> None:
        val = model.get_value_as_bool()
        self._safe_mode = val
        print(f"[whoimpg.biologger] Safe Mode set to: {val}")
        if val:
            # Clear history immediately to free memory
            # replacing list ref is thread-safe enough for this context
            self._trail_buffer = []
            self._trail_times = []

            # Lock the checkbox if it exists
            if hasattr(self, "_safe_mode_checkbox"):
                self._safe_mode_checkbox.enabled = False

    def _ensure_trail_material(self, stage: Usd.Stage) -> str:
        path = "/World/Looks/NeonTrail"

        # Always define basic Shader structure (Define is idempotent or updates)
        material = UsdShade.Material.Define(stage, path)
        shader = UsdShade.Shader.Define(stage, path + "/Shader")
        shader.CreateIdAttr("UsdPreviewSurface")

        # Connect displayColor primvar to Emissive Color
        reader = UsdShade.Shader.Define(stage, path + "/PrimvarReader")
        reader.CreateIdAttr("UsdPrimvarReader_float3")
        reader.CreateInput("varname", Sdf.ValueTypeNames.Token).Set("displayColor")
        # Default to Cyan if primvar missing
        reader.CreateInput("fallback", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(0, 1, 1))

        # Connect Reader Output -> Shader Emissive
        shader.CreateInput("emissiveColor", Sdf.ValueTypeNames.Color3f).ConnectToSource(
            reader.ConnectableAPI(), "result"
        )
        # Set diffuse to black so it doesn't wash out (Ensure this is set even if exists)
        shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(0, 0, 0))

        # Connect Surface
        material.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), "surface")

        return path

    def _update_trail(self, stage: Usd.Stage, animal_prim: Usd.Prim) -> None:
        t0 = time.perf_counter()

        # Get Grid Time (Playhead)
        timeline = omni.timeline.get_timeline_interface()
        current_time_seconds = timeline.get_current_time()

        points_to_draw: list[Gf.Vec3f] = []

        # Check if we have data
        if not self._trail_buffer or len(self._trail_buffer) < 2:
            return

        # Optimization: Decimate for visualization
        # With uncorked streaming (100k+ pts), we must limit rendered geometry
        max_visual_points = 20000
        total_points = len(self._trail_buffer)
        step = max(1, total_points // max_visual_points)

        # Slice the buffer for visualization
        visual_buffer = self._trail_buffer[::step]
        points_to_draw = [p[1] for p in visual_buffer]
        num_points = len(points_to_draw)

        # Split trail visual style based on playhead position
        # If Live Sync is ON, we treat the playhead as being at the END
        # so everything is "Past" (Black).
        force_live = False
        if (
            hasattr(self, "_live_sync_checkbox")
            and self._live_sync_checkbox.model.get_value_as_bool()
        ):
            force_live = True

        if force_live:
            split_idx = num_points
        else:
            # We must search within the DECIMATED time list to match the visual points
            times = [p[0] for p in visual_buffer]
            import bisect

            split_idx = bisect.bisect_right(times, current_time_seconds)

        # Colors: Past (Gradient based on ODBA), Future (Dim Grey)
        # ODBA scaling: 0.0 -> 1.75 (95th percentile)
        # Colormap: Blue (Low) -> Green -> Red (High)
        c_future = Gf.Vec3f(0.1, 0.1, 0.1)

        colors = []
        for i, p in enumerate(visual_buffer):
            if i >= split_idx:
                colors.append(c_future)
                continue

            # Extract ODBA (index 3 if available, else 0)
            odba = p[3] if len(p) > 3 else 0.0

            # Normalize 0.0 -> 1.75
            norm = min(max(odba / 1.75, 0.0), 1.0)

            # Heat Map: Blue (Low Activity) -> Green -> Red (High Activity)
            # Intensity multiplier for bloom: 5.0 (High visibility)
            intensity = 5.0

            if norm < 0.5:
                # Blue (0,0,1) -> Green (0,1,0)
                t = norm * 2.0
                c = Gf.Vec3f(0.0, t * intensity, (1.0 - t) * intensity)
            else:
                # Green (0,1,0) -> Red (1,0,0)
                t = (norm - 0.5) * 2.0
                c = Gf.Vec3f(t * intensity, (1.0 - t) * intensity, 0.0)

            colors.append(c)

        # Get or Create Trail Prim
        trail_prim = stage.GetPrimAtPath(self._trail_prim_path)
        curves = None

        if not trail_prim.IsValid():
            curves = UsdGeom.BasisCurves.Define(stage, self._trail_prim_path)
            curves.CreateTypeAttr(UsdGeom.Tokens.linear)  # Linear for connected lines

            # Set Width
            curves.CreateWidthsAttr(Vt.FloatArray([5.0]))  # 5cm thick
            curves.SetWidthsInterpolation(UsdGeom.Tokens.constant)
        else:
            curves = UsdGeom.BasisCurves(trail_prim)

        if curves and points_to_draw:
            # Bind Neon Material
            mat_path = self._ensure_trail_material(stage)
            UsdShade.MaterialBindingAPI(curves).Bind(
                UsdShade.Material(stage.GetPrimAtPath(mat_path))
            )

            # Update Vertex Counts FIRST to define topology
            # This ensures subsequent attribute updates match the expected count
            curves.GetCurveVertexCountsAttr().Set(Vt.IntArray([len(points_to_draw)]))

            # Update Points
            # Convert Gf.Vec3f objects to tuples to avoid "Unsupported type" warnings in Fabric/Vt
            points_tuples = [(p[0], p[1], p[2]) for p in points_to_draw]
            curves.GetPointsAttr().Set(Vt.Vec3fArray(points_tuples))

            # Update Colors using PrimvarsAPI
            primvar_api = UsdGeom.PrimvarsAPI(curves.GetPrim())

            # Explicitly remove indices property if it exists to avoid Fabric warning
            # "attribute primvars:displayColor:indices not found"
            if curves.GetPrim().HasAttribute("primvars:displayColor:indices"):
                curves.GetPrim().RemoveProperty("primvars:displayColor:indices")

            color_primvar = primvar_api.CreatePrimvar(
                "displayColor", Sdf.ValueTypeNames.Color3fArray
            )
            color_primvar.SetInterpolation(UsdGeom.Tokens.vertex)

            # Convert Gf.Vec3f objects to tuples for Vt compatibility
            colors_tuples = [(c[0], c[1], c[2]) for c in colors]
            color_primvar.Set(Vt.Vec3fArray(colors_tuples))

        t1 = time.perf_counter()
        self._last_trail_update_ms = (t1 - t0) * 1000.0

    def _update_debug_vectors(self, stage: Usd.Stage, animal_prim: Usd.Prim) -> None:
        """
        Draws debug vectors for Velocity (Green) and Heading (Red).
        """
        # Check if debug vectors are enabled
        if not self._debug_vec_checkbox.model.get_value_as_bool():
            # Hide vectors when disabled
            for name in ["Velocity", "Heading"]:
                prim = stage.GetPrimAtPath(f"/World/Debug/{name}")
                if prim.IsValid():
                    UsdGeom.Imageable(prim).MakeInvisible()
            return

        if not self._trail_buffer or len(self._trail_buffer) < 2:
            return

        # Get latest state
        p_now = self._trail_buffer[-1]
        p_prev = self._trail_buffer[-2]
        pos_cur = p_now[1]
        pos_cur_d = Gf.Vec3d(pos_cur[0], pos_cur[1], pos_cur[2])
        pos_old = p_prev[1]

        # Velocity Vector
        dx = pos_cur[0] - pos_old[0]
        dy = pos_cur[1] - pos_old[1]
        dz = pos_cur[2] - pos_old[2]

        # Scale for visibility (e.g. 500 units long)
        scale = 500.0

        # normalized velocity
        dist = math.sqrt(dx * dx + dy * dy + dz * dz)
        if dist < 0.001:
            vel_vec = Gf.Vec3d(0, 0, 0)
        else:
            vel_vec = Gf.Vec3d(dx / dist, dy / dist, dz / dist) * scale

        # Heading Vector
        rot = p_now[2]  # Quatf
        # Transform (0,0,-1) by rot
        fwd = rot.Transform(Gf.Vec3f(0, 0, -1))
        head_vec = Gf.Vec3d(fwd[0], fwd[1], fwd[2]) * scale

        def draw_line(name: str, color: Gf.Vec3f, end_pos: Gf.Vec3d) -> None:
            path = f"/World/Debug/{name}"
            prim = stage.GetPrimAtPath(path)
            if not prim.IsValid():
                curves = UsdGeom.BasisCurves.Define(stage, path)
                curves.CreateTypeAttr(UsdGeom.Tokens.linear)
                curves.CreateWidthsAttr(Vt.FloatArray([2.0]))
                curves.SetWidthsInterpolation(UsdGeom.Tokens.constant)

                primvar_api = UsdGeom.PrimvarsAPI(curves.GetPrim())
                c_primvar = primvar_api.CreatePrimvar(
                    "displayColor", Sdf.ValueTypeNames.Color3fArray
                )
                c_primvar.Set([color])  # Single color
            else:
                curves = UsdGeom.BasisCurves(prim)

            # Line from Shark Center to Vector Tip
            points = [pos_cur_d, pos_cur_d + end_pos]
            curves.GetCurveVertexCountsAttr().Set(Vt.IntArray([2]))
            # Convert Vec3d to Vec3f for the point array
            points_f = [Gf.Vec3f(p[0], p[1], p[2]) for p in points]
            curves.GetPointsAttr().Set(Vt.Vec3fArray(points_f))

            # Ensure vector is visible
            UsdGeom.Imageable(prim).MakeVisible()

        # Green = Velocity (Truth)
        draw_line("Velocity", Gf.Vec3f(0, 1, 0), vel_vec)
        # Red = Heading (Sensor)
        draw_line("Heading", Gf.Vec3f(1, 0, 0), head_vec)

    def _update_follow_camera(self, stage: Usd.Stage, target_prim: Usd.Prim) -> None:
        camera_prim = stage.GetPrimAtPath("/World/FollowCamera")
        if not camera_prim.IsValid():
            return

        # Get target transform (animal centroid)
        target_xform = UsdGeom.Xformable(target_prim)
        target_mat = target_xform.ComputeLocalToWorldTransform(Usd.TimeCode.Default())
        target_trans = target_mat.ExtractTranslation()  # Animal centroid position

        # 1. Calculate Camera Position (World Frame Y-axis orbit)
        # Orbit around animal on horizontal plane (XZ), maintaining fixed elevation
        if not hasattr(self, "_cam_distance"):
            self._cam_distance = 1500.0
        follow_dist = self._cam_distance

        import math

        # Debug: Print current orbit parameters
        if not hasattr(self, "_last_orbit_debug_time"):
            self._last_orbit_debug_time = 0.0
        import time

        if time.time() - self._last_orbit_debug_time > 2.0:
            print(
                f"[whoimpg.biologger] Orbit params: az={self._cam_azimuth:.1f}° "
                f"el={self._cam_elevation:.1f}° dist={follow_dist:.0f}"
            )
            print(f"[whoimpg.biologger] Animal pos: {target_trans}")
            self._last_orbit_debug_time = time.time()

        # Convert azimuth to radians (rotation around world Y-axis)
        az_rad = self._cam_azimuth * (math.pi / 180.0)
        # Convert elevation to radians (angle from horizontal plane)
        el_rad = self._cam_elevation * (math.pi / 180.0)

        # Calculate camera offset from target using cylindrical coordinates
        # X-Z plane rotation (azimuth) + Y offset (elevation)
        # Negate azimuth to fix orbit direction
        horizontal_dist = follow_dist * math.cos(el_rad)
        offset_x = horizontal_dist * math.sin(-az_rad)
        offset_y = follow_dist * math.sin(el_rad)
        offset_z = horizontal_dist * math.cos(-az_rad)

        # Camera position = target + offset (no smoothing - instant orbit response)
        cam_pos = target_trans + Gf.Vec3d(offset_x, offset_y, offset_z)

        # Debug position calculation
        if time.time() - self._last_orbit_debug_time < 0.1:
            # Calculate distance once
            dist = (target_trans - cam_pos).GetLength()
            print(
                f"[whoimpg.biologger] Cam pos: {cam_pos}, Target: {target_trans}, Dist: {dist:.1f}"
            )

        # 2. Update Camera Transform using SetLookAt (USD standard, viewport respects this)
        cam_xform = UsdGeom.Xformable(camera_prim)
        translate_op = None
        rotate_op = None

        for op in cam_xform.GetOrderedXformOps():
            if op.GetOpType() == UsdGeom.XformOp.TypeTranslate:
                translate_op = op
            elif op.GetOpType() == UsdGeom.XformOp.TypeRotateXYZ:
                rotate_op = op

        if not translate_op:
            translate_op = cam_xform.AddTranslateOp()
        if not rotate_op:
            rotate_op = cam_xform.AddRotateXYZOp()

        translate_op.Set(cam_pos)

        # CRITICAL: Calculate rotation to LOOK AT TARGET, not just use azimuth
        # The camera needs to point at the target regardless of where it moves
        # Pitch: Negative elevation (look down when elevation is positive)
        # Yaw: Calculate angle from camera to target in XZ plane
        # Roll: Always 0 for level horizon

        pitch_euler = -self._cam_elevation

        # Calculate yaw by finding the direction from camera to target
        # yaw = atan2(target.x - cam.x, -(target.z - cam.z)) in degrees
        # The negative Z is because USD camera forward is -Z
        import math

        delta_x = target_trans[0] - cam_pos[0]
        delta_z = target_trans[2] - cam_pos[2]
        yaw_rad = math.atan2(delta_x, -delta_z)  # atan2(x, -z) for proper heading
        yaw_euler = yaw_rad * 180.0 / math.pi

        # Roll: Always zero - maintain level horizon
        roll_euler = 0.0

        rotate_op.Set(Gf.Vec3f(pitch_euler, yaw_euler, roll_euler))

        # Debug rotation to verify we maintain zero roll
        if time.time() - self._last_orbit_debug_time < 0.1:
            print(
                f"[whoimpg.biologger] Camera Euler (XYZ): pitch={pitch_euler:.1f}° "
                f"yaw={yaw_euler:.1f}° roll={roll_euler:.1f}°"
            )

    def _restart_listener(self) -> None:
        """Restarts the ZMQ listener with new settings"""
        print("[whoimpg.biologger] Restarting listener...")
        if hasattr(self, "_stop_event"):
            self._stop_event.set()

        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.0)

        # Reset counters
        self._packet_count = 0
        self._packets_since_last_update = 0
        self._last_throughput_time = time.time()
        self._throughput_str = "0.0 pkts/s"
        self._last_vector_str = "N/A"
        self._latest_physics_data = None
        self._latest_timestamp = 0.0

        self._start_listener()

    def _start_listener(self) -> None:
        # We run the ZMQ listener in a separate thread to avoid blocking Kit
        if self._thread and self._thread.is_alive():
            print("[whoimpg.biologger] Listener already running.")
            return

        # Get config from UI if available, otherwise defaults
        host = "127.0.0.1"
        port = 5555
        if hasattr(self, "_host_field"):
            host = self._host_field.model.get_value_as_string()
        if hasattr(self, "_port_field"):
            port = self._port_field.model.get_value_as_int()

        print(f"[whoimpg.biologger] Starting ZMQ listener on {host}:{port}...")
        self._connection_status = "Connecting..."
        self._stop_event = threading.Event()
        self._thread = threading.Thread(
            target=self._zmq_listener_loop, args=(host, port), daemon=True
        )
        self._thread.start()

    def _zmq_listener_loop(self, host: str, port: int) -> None:
        try:
            import zmq
        except ImportError:
            print(
                "[whoimpg.biologger] Error: 'pyzmq' not found. "
                "Please ensure it is installed via extension.toml dependencies."
            )
            self._connection_status = "Error (Missing pyzmq)"
            return

        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        address = f"tcp://{host}:{port}"

        try:
            socket.connect(address)
            socket.subscribe("")  # Subscribe to all topics
            print(f"[whoimpg.biologger] ZMQ listener connected to {address}")
            self._connection_status = "Connected (Listening)"
        except Exception as e:
            print(f"[whoimpg.biologger] ZMQ Connection Error: {e}")
            self._connection_status = f"Error ({str(e)[:20]}...)"
            return

        first_msg = True
        while not self._stop_event.is_set():
            try:
                # Use binary multipart for efficiency
                frames = socket.recv_multipart(flags=zmq.NOBLOCK)
                if len(frames) < 2:
                    continue

                _topic = frames[0]
                payload = frames[1]

                # Unpack MessagePack
                message = msgpack.unpackb(payload, raw=False)

                self._packet_count += 1
                self._packets_since_last_update += 1

                if first_msg:
                    print(f"[whoimpg.biologger] First Multi-Entity message received: {message}")
                    first_msg = False

                # Format: { eid, sim_id, ts, rot: [r,p,h], phys: { ... } }
                if isinstance(message, dict) and "eid" in message:
                    eid = int(message["eid"])
                    sim_id = message.get("sim_id", "unknown")
                    ts = float(message.get("ts", 0.0))

                    # Update global timestamp for UI
                    self._latest_timestamp = ts
                    self._replay_live_time = ts

                    # Resolve species for asset selection
                    # Try sim_id first, then fuzzy match or default
                    species = self._id_to_species.get(sim_id)
                    if not species:
                        # Fallback: check if the sim_id contains a known tag_id as a prefix
                        # This supports A/B testing like "RED001_A"
                        for tag_id, sp in self._id_to_species.items():
                            if sim_id.startswith(tag_id):
                                species = sp
                                break

                    if not species:
                        species = "unknown"

                    # Extract orientation (Euler)
                    rot_data = message.get("rot")
                    if (
                        isinstance(rot_data, list)
                        and len(rot_data) >= 3
                        and (self._active_eid == -1 or eid == self._active_eid)
                    ):
                        self._last_vector_str = (
                            f"R:{rot_data[0]:.1f} P:{rot_data[1]:.1f} H:{rot_data[2]:.1f}"
                        )

                    # Extract physics
                    phys = message.get("phys", {})

                    # Prepare state update
                    state = self._entities_state.setdefault(eid, {"id": sim_id, "sp": species})
                    state.update({"ts": ts, "rot_data": rot_data, "phys": phys})

            except zmq.Again:
                import time

                time.sleep(0.001)
                continue
            except Exception as e:
                print(f"Error in ZMQ loop: {e}")
                import time

                time.sleep(1.0)

    def _reset_orientation(self) -> None:
        """Resets the telemetry orientation op to identity."""
        print("[whoimpg.biologger] Resetting orientation...")
        try:
            usd_context = omni.usd.get_context()
            stage = usd_context.get_stage()
            if not stage:
                return

            prim = stage.GetPrimAtPath("/World/Animal")
            if not prim.IsValid():
                return

            xformable = UsdGeom.Xformable(prim)

            # Look for our specific telemetry op
            telemetry_op = None
            for op in xformable.GetOrderedXformOps():
                if op.GetOpName() == "xformOp:orient:telemetry":
                    telemetry_op = op
                    break

            if telemetry_op:
                # Reset to identity quaternion (w=1, x=0, y=0, z=0)
                telemetry_op.Set(Gf.Quatf(1.0, 0.0, 0.0, 0.0))
                print("[whoimpg.biologger] Telemetry orientation reset to identity.")

                # Also clear the last vector string in UI
                self._last_vector_str = "Reset (Identity)"
                self._latest_quat_data = None
            else:
                print("[whoimpg.biologger] No telemetry orientation op found to reset.")

        except Exception as e:
            print(f"[whoimpg.biologger] Error resetting orientation: {e}")

    def _show_timeline_window(self) -> None:
        """Helper to bring the Timeline controls to the foreground."""
        try:
            # Ensure extension is enabled using the Extension Manager
            manager = omni.kit.app.get_app().get_extension_manager()
            if not manager.is_extension_enabled("omni.anim.timeline"):
                manager.set_extension_enabled("omni.anim.timeline", True)
                print("[whoimpg.biologger] Enabled omni.anim.timeline extension.")
            else:
                print("[whoimpg.biologger] omni.anim.timeline is already enabled.")

            # Optional: Try to focus it via layout or command (if known working)
            # Avoiding ToggleExtension command as it requires specific arguments
            # and changes per version.
        except Exception as e:
            print(f"[whoimpg.biologger] Error showing timeline window: {e}")

    def _set_defaults(self) -> None:
        """
        This is trying to setup some defaults for extensions to avoid warnings.
        """
        self._settings.set_default("/persistent/app/omniverse/bookmarks", {})
        self._settings.set_default("/persistent/app/stage/timeCodeRange", [0, 100])

        self._settings.set_default("/persistent/audio/context/closeAudioPlayerOnStop", False)

        self._settings.set_default(
            "/persistent/app/primCreation/PrimCreationWithDefaultXformOps", True
        )
        self._settings.set_default(
            "/persistent/app/primCreation/DefaultXformOpType", "Scale, Rotate, Translate"
        )
        self._settings.set_default("/persistent/app/primCreation/DefaultRotationOrder", "ZYX")
        self._settings.set_default("/persistent/app/primCreation/DefaultXformOpPrecision", "Double")

        # omni.kit.property.tagging
        self._settings.set_default(
            "/persistent/exts/omni.kit.property.tagging/showAdvancedTagView", False
        )
        self._settings.set_default(
            "/persistent/exts/omni.kit.property.tagging/showHiddenTags", False
        )
        self._settings.set_default(
            "/persistent/exts/omni.kit.property.tagging/modifyHiddenTags", False
        )

        self._settings.set_default(
            "/rtx/sceneDb/ambientLightIntensity", 0.0
        )  # set default ambientLight intensity to Zero

        # Enable USD Diagnostics
        self._settings.set_default("/persistent/app/usd/muteUsdDiagnostics", False)

    def _on_fabric_delegate_changed(
        self, _v: str, event_type: carb.settings.ChangeEventType
    ) -> None:
        if event_type == carb.settings.ChangeEventType.CHANGED:
            enabled: bool = self._settings.get_as_bool("/app/useFabricSceneDelegate")
            self._settings.set("/persistent/app/useFabricSceneDelegate", enabled)

    async def __new_stage(self) -> None:
        """Create a new stage"""
        # Disable Fog to prevent "cloudy milk" effect
        self._settings.set("/rtx/fog/enabled", False)
        self._settings.set("/rtx/post/fog/enabled", False)
        self._settings.set("/rtx/hydra/fog/enabled", False)

        # 5 frame delay to allow Layout
        for _ in range(5):
            await omni.kit.app.get_app().next_update_async()

        ctx = omni.usd.get_context()
        animal_type = self._settings.get("/biologger/animal")

        # Check if a stage file was passed via command line or settings
        custom_stage = self._settings.get("/biologger/stage")
        if custom_stage:
            print(f"[whoimpg.biologger] Opening custom stage from setting: {custom_stage}")
            ctx.open_stage(str(custom_stage))
            if animal_type:
                await self._load_animal_asset(animal_type)
            # Create follow camera
            self._ensure_follow_camera()
            return

        if ctx.get_stage_url():
            print(f"[whoimpg.biologger] Stage already loaded: {ctx.get_stage_url()}")
            if animal_type:
                await self._load_animal_asset(animal_type)
            # Create follow camera
            self._ensure_follow_camera()
            return

        # Check if user wants to skip default scene (for testing)
        if self._settings.get("/biologger/skipDefaultScene"):
            print("[whoimpg.biologger] Skipping default scene (skipDefaultScene=true)")
            return

        if ctx.can_open_stage():
            # Attempt to find ocean_scene.usda by walking up from the extension path
            # This handles differences between source and build directory structures
            current_dir = DATA_PATH
            scene_path = None
            # We need to go up quite a few levels from _build/windows-x86_64/release/extensions/...
            for _ in range(8):
                # Check direct path
                check_path = current_dir / "ocean_scene.usda"
                if check_path.exists():
                    scene_path = check_path
                    break

                # Check assets/
                check_path = current_dir / "assets" / "ocean_scene.usda"
                if check_path.exists():
                    scene_path = check_path
                    break

                # Check source/assets/
                check_path = current_dir / "source" / "assets" / "ocean_scene.usda"
                if check_path.exists():
                    scene_path = check_path
                    break

                current_dir = current_dir.parent

            if scene_path and scene_path.exists():
                print(f"[whoimpg.biologger] Opening default scene: {scene_path}")
                omni.usd.get_context().open_stage(str(scene_path))
                # Load the animal asset based on command line arguments
                if animal_type:
                    await self._load_animal_asset(animal_type, eid=0, sim_id="default")
                # Create follow camera for the scene
                self._ensure_follow_camera()
            else:
                print(
                    "[whoimpg.biologger] Default scene not found "
                    f"(searched up from {DATA_PATH}), creating new stage."
                )

    def _launch_app(
        self, app_id: str, console: bool = True, custom_args: dict[str, str] | None = None
    ) -> None:
        """launch another Kit app with the same settings"""
        app_path = carb.tokens.get_tokens_interface().resolve("${app}")
        kit_file_path = os.path.join(app_path, app_id)

        # https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
        # Validate input from command line (detected in static analysis)
        kit_exe = sys.argv[0]
        if not os.path.exists(kit_exe):
            print(f"cannot find executable{kit_exe}")
            return

        launch_args = [kit_exe]
        launch_args += [kit_file_path]
        if custom_args:
            launch_args.extend(custom_args)  # type: ignore

        # Pass all exts folders
        exts_folders = self._settings.get("/app/exts/folders")
        if exts_folders:
            for folder in exts_folders:
                launch_args.extend(["--ext-folder", folder])

        kwargs: dict[str, Any] = {"close_fds": False}
        if platform.system().lower() == "windows":
            create_new_console = getattr(subprocess, "CREATE_NEW_CONSOLE", 0)
            create_new_process_group = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)

            if console:
                kwargs["creationflags"] = create_new_console | create_new_process_group
            else:
                kwargs["creationflags"] = create_new_process_group

        subprocess.Popen(launch_args, **kwargs)

    def _show_ui_docs(self) -> None:
        """show the omniverse ui documentation as an external Application"""
        self._launch_app("omni.app.uidoc.kit")

    def _show_launcher(self) -> None:
        """show the omniverse ui documentation as an external Application"""
        self._launch_app(
            "omni.create.launcher.kit",
            console=False,
            custom_args={"--/app/auto_launch=false"},  # type: ignore
        )

    async def __property_window(self) -> None:
        """Creates a propety window and sets column sizes."""
        await omni.kit.app.get_app().next_update_async()

        property_window = property_window_ext.get_window()
        property_window.set_scheme_delegate_layout(
            "Create Layout",
            [
                "basis_curves_prim",
                "path_prim",
                "material_prim",
                "xformable_prim",
                "shade_prim",
                "camera_prim",
            ],
        )

        # expand width of path_items so "Instancable" doesn't get wrapped
        PrimPathWidget.set_path_item_padding(3.5)

    def __menu_update(self) -> None:
        """Update the menu"""
        self._menu_layout = [
            MenuLayout.Menu(
                "Window",
                [
                    MenuLayout.SubMenu(
                        "Animation",
                        [
                            MenuLayout.Item("Timeline"),
                            MenuLayout.Item("Sequencer"),
                            MenuLayout.Item("Curve Editor"),
                            MenuLayout.Item("Retargeting"),
                            MenuLayout.Item("Animation Graph"),
                            MenuLayout.Item("Animation Graph Samples"),
                        ],
                    ),
                    MenuLayout.SubMenu(
                        "Layout",
                        [
                            MenuLayout.Item("Quick Save", remove=True),
                            MenuLayout.Item("Quick Load", remove=True),
                        ],
                    ),
                    MenuLayout.SubMenu(
                        "Browsers",
                        [
                            MenuLayout.Item("Content", source="Window/Content"),
                            MenuLayout.Item("Materials"),
                            MenuLayout.Item("Skies"),
                        ],
                    ),
                    MenuLayout.SubMenu(
                        "Rendering",
                        [
                            MenuLayout.Item("Render Settings"),
                            MenuLayout.Item("Movie Capture"),
                            MenuLayout.Item("MDL Material Graph"),
                            MenuLayout.Item("Tablet XR"),
                        ],
                    ),
                    MenuLayout.SubMenu(
                        "Utilities",
                        [
                            MenuLayout.Item("Console"),
                            MenuLayout.Item("Profiler"),
                            MenuLayout.Item("USD Paths"),
                            MenuLayout.Item("Statistics"),
                            MenuLayout.Item("Activity Progress"),
                            MenuLayout.Item("Actions"),
                            MenuLayout.Item("Asset Validator"),
                        ],
                    ),
                    MenuLayout.Sort(exclude_items=["Extensions"], sort_submenus=True),
                    MenuLayout.Item("New Viewport Window", remove=True),
                ],
            ),
            MenuLayout.Menu(
                "Layout",
                [
                    MenuLayout.Item("Default", source="Reset Layout"),
                    MenuLayout.Seperator(),
                    MenuLayout.Item("UI Toggle Visibility", source="Window/UI Toggle Visibility"),
                    MenuLayout.Item("Fullscreen Mode", source="Window/Fullscreen Mode"),
                    MenuLayout.Seperator(),
                    MenuLayout.Item("Save Layout", source="Window/Layout/Save Layout..."),
                    MenuLayout.Item("Load Layout", source="Window/Layout/Load Layout..."),
                    MenuLayout.Seperator(),
                    MenuLayout.Item("Quick Save", source="Window/Layout/Quick Save"),
                    MenuLayout.Item("Quick Load", source="Window/Layout/Quick Load"),
                ],
            ),
        ]
        omni.kit.menu.utils.add_layout(self._menu_layout)

        self._layout_menu_items: list[Any] = []

        def add_layout_menu_entry(name: str, parameter: Any, key: int) -> None:
            """Add a layout menu entry."""
            if inspect.isfunction(parameter):
                menu_dict = omni.kit.menu.utils.build_submenu_dict(
                    [
                        MenuItemDescription(
                            name=f"Layout/{name}",
                            onclick_fn=lambda: asyncio.ensure_future(parameter()),
                            hotkey=(carb.input.KEYBOARD_MODIFIER_FLAG_CONTROL, key),
                        ),
                    ]
                )
            else:

                async def _active_layout(layout: str) -> None:
                    await _load_layout(layout)
                    # load layout file again to make sure layout correct
                    await _load_layout(layout)

                menu_dict = omni.kit.menu.utils.build_submenu_dict(
                    [
                        MenuItemDescription(
                            name=f"Layout/{name}",
                            onclick_fn=lambda: asyncio.ensure_future(
                                _active_layout(f"{DATA_PATH}/layouts/{parameter}.json")
                            ),
                            hotkey=(carb.input.KEYBOARD_MODIFIER_FLAG_CONTROL, key),
                        ),
                    ]
                )

            # add menu
            for group in menu_dict:
                omni.kit.menu.utils.add_menu_items(menu_dict[group], group)

            self._layout_menu_items.append(menu_dict)

        add_layout_menu_entry("Reset Layout", "default", carb.input.KeyboardInput.KEY_1)

        # create Quick Load & Quick Save
        async def quick_save() -> None:
            QuickLayout.quick_save(None, None)

        async def quick_load() -> None:
            QuickLayout.quick_load(None, None)

        add_layout_menu_entry("Quick Save", quick_save, carb.input.KeyboardInput.KEY_7)
        add_layout_menu_entry("Quick Load", quick_load, carb.input.KeyboardInput.KEY_8)

        # open "Asset Stores" window
        ui.Workspace.show_window("Asset Stores")

    def _load_metadata(self) -> None:
        """Loads species mapping from biologger_meta.csv."""
        # Try a few plausible locations
        cwd = Path(os.getcwd())
        possible_paths = [
            cwd / "datasets" / "biologger_meta.csv",
            cwd / "tests" / "data" / "biologger_meta.csv",
            DATA_PATH / "assets" / "biologger_meta.csv",
        ]

        meta_file = None
        for p in possible_paths:
            if p.exists():
                meta_file = p
                break

        if not meta_file:
            print(
                "[whoimpg.biologger] Warning: Could not find "
                "biologger_meta.csv in standard locations."
            )
            return

        print(f"[whoimpg.biologger] Loading metadata from: {meta_file}")
        try:
            with open(meta_file, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    tag_id = row.get("tag_id") or row.get("id")
                    species = row.get("species")
                    if tag_id and species:
                        self._id_to_species[tag_id] = species
        except Exception as e:
            print(f"[whoimpg.biologger] Error loading metadata: {e}")

    def on_shutdown(self) -> None:
        """Clean up the extension"""
        # --- WHOI Biologger Subscriber Cleanup ---
        if hasattr(self, "_csv_file") and self._csv_file:
            self._csv_file.close()
            print(f"[whoimpg.biologger] Closed log file: {self._csv_log_path}")

        if self._stop_event:
            self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=1.0)
        self._window = None
        self._update_sub = None  # Release subscription

        self._sub_fabric_delegate_changed = None

        omni.kit.menu.utils.remove_layout(self._menu_layout)
        self._menu_layout = []

        for menu_dict in self._layout_menu_items:
            for group in menu_dict:
                omni.kit.menu.utils.remove_menu_items(menu_dict[group], group)

        self._layout_menu_items = []
        self._launcher_menu = None
        self._reset_menu = None
