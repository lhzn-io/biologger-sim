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
import colorsys
import contextlib
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

HUD_WINDOW_X_POS = 2240
HUD_WINDOW_Y_POS = 500
HUD_WINDOW_WIDTH = 240
HUD_WINDOW_HEIGHT = 500

"""
Key Function Locations for Camera & Spawn Logic:

1. Initial Spawn & Camera Position (Startup/Load):
   - Function: `_load_animal_asset`
   - Role: Spawns the USD asset and sets the initial "Global" camera view
     (e.g. looking from behind/above).

2. Follow Mode Configuration (Toggle On):
   - Function: `_setup_biologger_subscriber` (Initializes variables)
   - Variables: `self._cam_azimuth`, `self._cam_elevation`, `self._cam_distance`
   - Logic: `_update_follow_camera` (Applies the orbit logic every frame)
"""


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

        # DEBUG: Print Gamepad Input options
        with contextlib.suppress(Exception):
            carb.log_info(f"[whoimpg.biologger] GamepadInput dir: {dir(carb.input.GamepadInput)}")
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
        # --- Kit 109.x Refined Configuration (Gemini 3 Guidance) ---

        # 1. Viewport & Visualization
        self._settings.set("/app/viewport/boundingBoxes/enabled", True)
        self._settings.set("/rtx/sceneDb/grid/enabled", False)
        self._settings.set("/persistent/app/viewport/grid/enabled", False)
        # Modern Viewport 2.0 grid disablement fallback
        self._settings.set("/app/viewport/displayOptions", 0)

        # 2. Lighting Mode (Stage Lighting vs. Simple/Headlight)
        # In newer Kit versions, lightingMode 0 is "Stage", 1 is "Entry/Simple"
        self._settings.set("/rtx/scene/lightingMode", 0)
        self._settings.set("/rtx/lightingMode", 0)
        self._settings.set("/persistent/rtx/scene/lightingMode", 0)
        self._settings.set("/persistent/rtx/lightingMode", 0)

        # IMPORTANT: This ensures the "Headlight" doesn't follow the camera
        self._settings.set("/rtx/sceneDb/enableStageLight", True)
        self._settings.set("/rtx/useViewLightingMode", False)
        self._settings.set("/persistent/rtx/useViewLightingMode", False)

        # 3. Post-Processing & Exposure Control
        # To stop the "glare" or shifting brightness when moving the camera:
        self._settings.set("/rtx/post/tonemap/autoExposure/enabled", False)
        self._settings.set("/persistent/rtx/post/tonemap/autoExposure/enabled", False)

        # Set a fixed exposure value to ensure it's not pitch black after disabling auto
        # Lower values are brighter; 0.0 is a common neutral starting point
        self._settings.set("/rtx/post/tonemap/exposure", 0.0)

        # Delayed force to ensure it sticks after the viewport is fully initialized
        async def _force_active_settings() -> None:
            # Import registry within task to avoid startup import issues
            try:
                import omni.kit.actions.core as action_core

                registry = action_core.get_action_registry()
                set_lighting_action = registry.get_action(
                    "omni.kit.viewport.window", "set_lighting_mode"
                )
            except Exception:
                set_lighting_action = None

            # Re-apply for 10 ticks to beat any competing extension or viewport init
            for _ in range(10):
                await omni.kit.app.get_app().next_update_async()
                # Re-force keys
                self._settings.set("/rtx/scene/lightingMode", 0)
                self._settings.set("/rtx/sceneDb/grid/enabled", False)
                self._settings.set("/app/viewport/displayOptions", 0)
                self._settings.set("/rtx/post/tonemap/autoExposure/enabled", False)
                self._settings.set("/rtx/post/tonemap/exposure", 0.0)

                if set_lighting_action:
                    set_lighting_action.execute(0)  # 0 = Stage Lighting

        self._force_lighting_task = asyncio.ensure_future(_force_active_settings())

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
        carb.log_info(f"[whoimpg.biologger] Attempting to load animal: {species} (sim_id={sim_id})")
        # Wait for stage to be ready
        stage = None
        # Wait up to ~5 seconds (300 frames at 60fps)
        for _ in range(300):
            await omni.kit.app.get_app().next_update_async()
            stage = omni.usd.get_context().get_stage()
            if stage:
                break

        if not stage:
            carb.log_error("[whoimpg.biologger] Error: No stage loaded, cannot spawn animal.")
            return None

        # Map scientific names or generic types to asset filenames
        # Extension is responsible for the choice of asset.
        species_map = {
            "xiphias gladius": "great_white_shark.glb",
            "rhincodon typus": "great_white_shark.glb",
            "carcharodon carcharias": "great_white_shark.glb",
            # Fallback/Generic types
            "shark": "great_white_shark.glb",
            "swordfish": "great_white_shark.glb",
            "whaleshark": "great_white_shark.glb",
        }

        asset_filename = species_map.get(species.lower(), "great_white_shark.glb")
        carb.log_info(f"[whoimpg.biologger] Mapping species '{species}' to asset: {asset_filename}")

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
            carb.log_error(
                f"[whoimpg.biologger] Error: Could not find asset file {asset_filename} "
                f"in {possible_paths}"
            )
            return None

        carb.log_info(f"[whoimpg.biologger] Found asset at: {full_asset_path}")

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
        # Apply initial visual offset to prevent overlapping if all start at (0,0)
        # Offset by 500 units (5m) along X-axis per eid
        visual_offset_x = float(eid) * 500.0
        op_translate.Set((visual_offset_x, 0, 0))
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

        carb.log_info(f"[whoimpg.biologger] Spawned {species} (sim_id={sim_id}) at {prim_path}")

        # Set initial camera view
        camera_path = omni.kit.viewport.utility.get_active_viewport_camera_path()
        if camera_path:
            camera_prim = stage.GetPrimAtPath(camera_path)
            if camera_prim.IsValid():
                # Position: Above (+Y) and behind (+Z) the animal
                # Animal is at (0,0,0), facing -Z.

                cam_pos = Gf.Vec3d(0, 300, 1000)
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

        return prim_path

    def _setup_biologger_subscriber(self) -> None:
        carb.log_info("[whoimpg.biologger] Initializing Subscriber...")

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
        self._cam_azimuth: float = 180.0  # Start behind origin (looking from -Z toward +Z)
        self._cam_elevation: float = 10.0  # Degrees up - start slightly above for visibility
        self._cam_distance: float = 1500.0  # Start 1500 units back
        self._input = carb.input.acquire_input_interface()
        self._input_sub_id = None
        self._last_input_heartbeat = 0.0
        self._last_gp_heartbeat = 0.0
        self._is_rmb_down = False
        self._last_mouse_pos = (0.0, 0.0)
        self._last_mouse_pos_valid: bool = False

        # Unified Camera Controller State
        self._follow_mode_enabled: bool = False
        self._cam_smooth_pos: Gf.Vec3d | None = None  # For Lerp smoothing
        self._cam_smooth_speed: float = 5.0  # Interpolation speed

        # Trail State
        # Refactored for Multi-Entity Segmented Trails
        self._entities_trail_buffers: dict[int, dict] = {}

        self._trail_prim_path = "/World/Trails"
        self._last_trail_update_ms = 0.0
        self._trail_segment_size = 5000

        # Temporal Replay State
        self._replay_live_time: float = 0.0
        self._replay_playhead: float = 0.0
        self._session_start_time: float = 0.0

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
            carb.log_warn("[whoimpg.biologger] Safe Mode enabled via startup config.")

        # Backend Config
        # --/biologger/backend=warp (or cpu)
        self._backend = self._settings.get("/biologger/backend") or "cpu"
        carb.log_info(f"[whoimpg.biologger] Backend Selected: {self._backend}")

        if self._backend == "warp":
            carb.log_info("[whoimpg.biologger] Initializing Warp...")
            try:
                global wp, warp_logic
                import warp as wp
                import whoimpg.biologger.subscriber.warp_logic as warp_logic

                wp.init()
                carb.log_info("[whoimpg.biologger] Warp Initialized successfully.")
            except ImportError as e:
                carb.log_error(f"[whoimpg.biologger] Failed to import Warp/Kernel: {e}")
                carb.log_warn("[whoimpg.biologger] Fallback to CPU backend.")
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
            carb.log_info(f"[whoimpg.biologger] Resolved Repo Root for Logs: {repo_root}")

        except Exception as e:
            carb.log_warn(f"[whoimpg.biologger] Error resolving root, falling back to CWD: {e}")
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
            carb.log_info(f"[whoimpg.biologger] Created session log dir: {self._session_dir}")
        except Exception as e:
            carb.log_error(f"[whoimpg.biologger] Failed to create log dir {self._session_dir}: {e}")
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
                carb.log_error(f"[whoimpg.biologger] Failed to open CSV log: {e}")
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
                carb.log_error(f"[whoimpg.biologger] Failed to write config log: {e}")
        carb.log_info(f"[whoimpg.biologger] Logging slip diagnostics to: {self._csv_log_path}")

        # Setup Menu Item for Manual HUD Toggle
        # Allows user to recover HUD if lost
        self._menu_list = [
            MenuItemDescription(
                name="Biologger HUD",
                onclick_fn=lambda: self._toggle_hud_visibility(),
            )
        ]
        omni.kit.menu.utils.add_menu_items(self._menu_list, "Window")

        # Throughput calculation
        self._packets_since_last_update = 0
        self._last_throughput_time = time.time()
        self._throughput_str = "0.0 pkts/s"

        # Subscribe to input events immediately (Persistent)
        # High priority (low order) to intercept Gamepad/Keys before Viewport
        if not self._input_sub_id:
            try:
                self._input_sub_id = self._input.subscribe_to_input_events(
                    self._on_input_event,
                    order=-10000,  # even earlier
                )
                carb.log_info(
                    f"[whoimpg.biologger] Subscribed to input events (ID: {self._input_sub_id})"
                )

            except Exception as e:
                carb.log_error(f"[whoimpg.biologger] Failed to subscribe to input events: {e}")

        # 1. Setup the UI Dashboard (Overlay style)
        # Using a small window in the top-left corner as a HUD
        # Removed dockPreference to ensure it appears floating/visible
        self._window = ui.Window(
            "Biologger Data", width=300, height=300, dockPreference=ui.DockPreference.DISABLED
        )
        self._window.position_x = 50
        self._window.position_y = 70
        self._window.visible = True
        carb.log_info("[whoimpg.biologger] Created HUD Window")
        with (
            self._window.frame,
            ui.ScrollingFrame(
                horizontal_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_OFF,
                vertical_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_AS_NEEDED,
            ),
            ui.VStack(height=0, spacing=1),
        ):
            self._status_label = ui.Label("Status: Disconnected", style={"color": 0xFF888888})

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
                    self._follow_mode_checkbox.model.set_value(self._follow_mode_enabled)
                    self._follow_mode_checkbox.model.add_value_changed_fn(
                        self._on_follow_mode_changed
                    )
                    ui.Label("Follow Mode (3rd Person)")

                with ui.HStack(height=20):
                    self._trail_checkbox = ui.CheckBox(width=20)
                    self._trail_checkbox.model.set_value(True)
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
                if self._safe_mode:
                    self._safe_mode_checkbox.enabled = False
                ui.Label("Safe Mode (Live Only)")

            ui.Spacer(height=5)
            ui.Button("Show Timeline & Playback Controls", clicked_fn=self._show_timeline_window)

            ui.Spacer(height=5)
            with (
                ui.CollapsableFrame("Camera Settings", collapsed=True),
                ui.VStack(spacing=5),
                ui.HStack(height=20),
            ):
                ui.Label("Damping:", width=60)
                self._camera_damping_field = ui.FloatSlider(min=0.001, max=1.0)
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

        # 1b. Create the HUD Window (Transparent Overlay)
        hud_flags = (
            ui.WINDOW_FLAGS_NO_TITLE_BAR
            | ui.WINDOW_FLAGS_NO_RESIZE
            | ui.WINDOW_FLAGS_NO_SCROLLBAR
            | ui.WINDOW_FLAGS_NO_COLLAPSE
        )
        self._hud_window = ui.Window(
            "Biologger HUD",
            width=HUD_WINDOW_WIDTH,
            height=HUD_WINDOW_HEIGHT,
            flags=hud_flags,
            dockPreference=ui.DockPreference.DISABLED,
        )
        # Initial position (refined in _on_update_ui)
        try:
            ws_width = ui.Workspace.get_main_window_width()
            self._hud_window.position_x = (
                ws_width - (HUD_WINDOW_WIDTH + 20) if ws_width > 100 else HUD_WINDOW_X_POS
            )
        except AttributeError:
            self._hud_window.position_x = HUD_WINDOW_X_POS
        self._hud_window.position_y = HUD_WINDOW_Y_POS
        self._hud_window.visible = True
        # Bring to front immediately
        self._hud_window.focus()
        carb.log_info(
            f"[whoimpg.biologger] HUD Window Created. Visible: {self._hud_window.visible}"
        )

        hud_style = {
            "Window": {
                "background_color": 0x0,
                "border_width": 0,
            },
            "Label": {
                "font_size": 16,
                "color": 0xFFFFFFFF,
                "margin_height": 0,
                "text_shadow": True,
            },
        }
        self._hud_window.frame.style = hud_style

        with self._hud_window.frame, ui.ZStack():
            ui.Rectangle(style={"background_color": 0x44000000})
            with ui.VStack(spacing=0, margin=10):
                # Align everything to the left
                def make_label(text: str, style: dict | None = None) -> ui.Label:
                    # Default soft gray/yellow (FPS-like): 0xFFCCCCDD
                    base_style = {"alignment": ui.Alignment.LEFT, "color": 0xFFCCCCDD}
                    if style:
                        base_style.update(style)
                    return ui.Label(text, style=base_style, alignment=ui.Alignment.LEFT, width=300)

                self._hud_status_label = make_label(
                    "Status: Disconnected", style={"color": 0xFFDDDDDD}
                )
                self._hud_packet_label = make_label("Packets: 0", style={"color": 0xFF88AAAA})
                self._hud_throughput_label = make_label("TPS: 0.0 pkts/s")
                self._hud_time_label = make_label("Time: --:--:--", style={"color": 0xFFEEEEEE})

                self._hud_active_animal_label = make_label(
                    "ENTITY: --", style={"color": 0xFFFFFF00}
                )
                self._hud_physics_title = make_label("TELEMETRY", style={"color": 0xFF00AAAA})
                self._hud_sim_clock_drift = make_label("Clock Drift: +0.0000s")
                self._hud_orientation_label = make_label("Orientation: R:-- P:-- H:--")
                self._hud_depth_label = make_label("Depth: --.- m")
                self._hud_sim_3d_vel = make_label("3D Vel: --.- m/s")
                self._hud_sim_h_vel = make_label("H. Vel: --.- m/s")
                self._hud_sim_v_vel = make_label("V. Vel: --.- m/s")
                self._hud_odba_label = make_label("ODBA: 0.00")
                self._hud_vedba_label = make_label("VeDBA: 0.00")
                self._hud_accel_label = make_label("Dyn. Accel: [0.0, 0.0, 0.0]")
                self._hud_static_accel_label = make_label("Static Accel: [0.0, 0.0, 0.0]")
                self._hud_pos_label = make_label("Pos: [0.0, 0.0, 0.0]")

                self._hud_derived_title = make_label("DERIVED METRICS", style={"color": 0xFF00AAAA})
                self._hud_est_clock_drift = make_label("Clock Drift: +0.0000s")
                self._hud_est_3d_vel = make_label("3D Vel: 0.00 m/s")
                self._hud_est_h_vel = make_label("H. Vel: 0.00 m/s")
                self._hud_est_v_vel = make_label("V. Vel: 0.00 m/s")
                self._hud_path_label = make_label("Trajectory: P:-- H:--")
                self._hud_attack_angle_label = make_label("Attack Angle: --.-°")
                self._hud_sideslip_label = make_label("Sideslip: --.-°")

        # 2. Fabric setup for the animal prim (e.g., /World/Shark)
        self._stage = None

        # 3. Auto-connect on startup
        self._start_listener()
        self._is_running = True

        # 4. Setup UI update loop (safe way to update UI from main thread)
        self._update_sub = (
            omni.kit.app.get_app()
            .get_update_event_stream()
            .create_subscription_to_pop(self._on_update_ui, name="whoimpg.biologger.update")
        )

        # 5. Initialize HUD with defaults (Consistent State)
        self._update_hud_labels(
            status="Status: Disconnected",
            animal_name="--",
            packets=0,
            tps="0.0 pkts/s",
            time_str="Time: --:--:--",
            roll=0.0,
            pitch=0.0,
            heading=0.0,
            alpha=0.0,
            beta=0.0,
            path_info="P:-- H:--",
            depth=0.0,
            sim_3d_vel=0.0,
            sim_h_vel=0.0,
            sim_v_vel=0.0,
            est_h_vel=0.0,
            est_v_vel=0.0,
            est_3d_vel=0.0,
            odba=0.0,
            vedba=0.0,
            dyn_accel=[0.0, 0.0, 0.0],
            static_accel=[0.0, 0.0, 0.0],
            pos=[0.0, 0.0, 0.0],
            sim_clock_drift=0.0,
            est_clock_drift=0.0,
        )

    def _cycle_active_animal(self, direction: int, index: int | None = None) -> None:
        """Cycles or sets the active animal selection."""
        if not self._entities_state:
            return

        sorted_eids = sorted(self._entities_state.keys())
        if not sorted_eids:
            return

        if index is not None:
            if 0 <= index < len(sorted_eids):
                self._active_eid = sorted_eids[index]
                carb.log_info(f"[whoimpg.biologger] Selected EID: {self._active_eid}")
            return

        try:
            current_idx = sorted_eids.index(self._active_eid)
        except ValueError:
            current_idx = 0

        new_idx = (current_idx + direction) % len(sorted_eids)
        self._active_eid = sorted_eids[new_idx]
        carb.log_info(f"[whoimpg.biologger] Switched to EID: {self._active_eid}")

        # Provide visual feedback via Toast or Console logic if needed
        # (Status label updates in _on_update_ui)

    def _update_telemetry_window(self) -> None:
        """Centralized HUD logic: Calcs -> Update Call."""
        if not self._window:
            return

        # 1. Window Positioning
        if hasattr(self, "_hud_window") and self._hud_window:
            try:
                ws_width = ui.Workspace.get_main_window_width()
                if ws_width > 100:
                    self._hud_window.position_x = ws_width - (HUD_WINDOW_WIDTH + 20)
                    self._hud_window.position_y = HUD_WINDOW_Y_POS
            except AttributeError:
                self._hud_window.position_x = HUD_WINDOW_X_POS
                self._hud_window.position_y = HUD_WINDOW_Y_POS

        # 2. Calculate Values
        # Status
        sim_id = "None"
        state = {}
        if self._active_eid != -1:
            state = self._entities_state.get(self._active_eid, {})
            sim_id = state.get("id", "Unknown")

        status_str = f"Status: {self._connection_status}"
        if self._active_eid != -1:
            status_str += f"\nActive: {sim_id}"
            status_str += " [LOCKED]" if self._follow_mode_enabled else " [Global View]"

        # Time
        if self._latest_timestamp > 0:
            dt = datetime.datetime.fromtimestamp(self._latest_timestamp, tz=datetime.timezone.utc)
            time_str = f"Time: {dt.strftime('%Y-%m-%d %H:%M:%S')}"
        else:
            time_str = "Time: --:--:--"

        # Physics / Telemetry
        phys = self._latest_physics_data or {}

        # Attack Angle & Sideslip Calculation
        alpha_val = 0.0
        beta_val = 0.0
        est_h_vel = 0.0
        est_v_vel = 0.0
        est_v_vel = 0.0
        est_3d_vel = 0.0

        if self._active_eid != -1:
            active_trail = self._entities_trail_buffers.get(self._active_eid)
            # Allow display if we have AT LEAST 1 point (for Position)
            if active_trail and active_trail["buffer"] and len(active_trail["buffer"]) > 1:
                # Look back logic for distinct timestamps
                # (omitted for brevity, assume valid p_prev found)
                # Find distinct timestamp
                p_now = active_trail["buffer"][-1]
                p_prev = None
                for i in range(len(active_trail["buffer"]) - 2, -1, -1):
                    if active_trail["buffer"][i][0] != p_now[0]:
                        p_prev = active_trail["buffer"][i]
                        break

                # Calculate speed if we found a valid previous point
                if p_prev:
                    pos_cur = p_now[1]
                    pos_old = p_prev[1]
                    # Mypy thinks this might be datetime so we explicitly cast and rename
                    ts_now = float(p_now[0])
                    ts_prev = float(p_prev[0])
                    delta_time = ts_now - ts_prev
                    if delta_time > 0.0001:
                        dx = (pos_cur[0] - pos_old[0]) / 100.0  # cm -> m
                        dy = (pos_cur[1] - pos_old[1]) / 100.0
                        dz = (pos_cur[2] - pos_old[2]) / 100.0

                        h_dist = math.sqrt(dx * dx + dz * dz)
                        v_dist = dy  # Sign matters for V. Vel? Yes.

                        est_h_vel = h_dist / delta_time
                        est_v_vel = v_dist / delta_time
                        est_3d_vel = math.sqrt(dx * dx + dy * dy + dz * dz) / delta_time

                        # DEBUG: Detailed contributions (optional, can be disabled)
                        # print(
                        #     f"[DEBUG] Vel: TS={p_now[0]:.4f}<-{p_prev[0]:.4f} dt={dt:.4f} "
                        #     f"HVel={est_h_vel:.2f} VVel={est_v_vel:.2f} m/s | "
                        #     f"dXYZ=[{dx:.2f}, {dy:.2f}, {dz:.2f}] (m)"
                        # )

        # Attack Angle & Sideslip Calculation
        path_str = "P:-- H:--"
        if self._active_eid != -1:
            active_trail = self._entities_trail_buffers.get(self._active_eid)
            if active_trail and active_trail["buffer"] and len(active_trail["buffer"]) > 1:
                p_now = active_trail["buffer"][-1]
                p_prev = None
                for i in range(len(active_trail["buffer"]) - 2, -1, -1):
                    if active_trail["buffer"][i][0] != p_now[0]:
                        p_prev = active_trail["buffer"][i]
                        break
                if p_prev:
                    pos_cur = p_now[1]
                    pos_old = p_prev[1]
                    # Explicit cast to appease Mypy
                    ts_now = float(p_now[0])
                    ts_prev = float(p_prev[0])
                    delta_time = ts_now - ts_prev
                    if delta_time > 0.0001:
                        dx = (pos_cur[0] - pos_old[0]) / 100.0  # cm -> m
                        dy = (pos_cur[1] - pos_old[1]) / 100.0
                        dz = (pos_cur[2] - pos_old[2]) / 100.0

                        if est_3d_vel > 0.01:  # Avoid division by zero or tiny vectors
                            rot = p_now[2]
                            # fwd = rot.Transform(Gf.Vec3f(0, 0, -1))  # Forward vector in USD space

                            # Velocity vector is directional, normalize by distance (not speed!)
                            # dx, dy, dz are displacements in meters
                            dist_3d = math.sqrt(dx * dx + dy * dy + dz * dz)
                            if dist_3d > 0.00001:
                                vel_vec = Gf.Vec3f(dx, dy, dz) / dist_3d

                                # Calculate Path Pitch/Heading from velocity vector
                                # Pitch = asin(dy) since it's normalized Y-up
                                path_pitch = math.degrees(
                                    math.asin(max(min(vel_vec[1], 1.0), -1.0))
                                )
                                # Heading = atan2(dx, -dz) (USD convention: -Z is fwd)
                                path_heading = math.degrees(math.atan2(vel_vec[0], -vel_vec[2]))
                                path_str = f"P:{path_pitch:.1f} H:{path_heading:.1f}"

                            else:
                                vel_vec = Gf.Vec3f(0, 0, 0)

                            # Calculate Alpha (AoA) and Beta (Sideslip) in Body Frame
                            # Transforms World Velocity -> Body Velocity
                            vel_body = rot.GetInverse().Transform(vel_vec)

                            # Alpha (Pitch): Angle between Vertical (Y) and Forward (-Z)
                            # Beta (Sideslip): Angle between Lateral (X) and Forward (-Z)

                            # Note: vel_body is normalized IF vel_vec was normalized.
                            # Standard atan2 handles magnitude.

                            alpha_val = math.degrees(math.atan2(vel_body[1], -vel_body[2]))
                            beta_val = math.degrees(math.atan2(vel_body[0], -vel_body[2]))

        # Data extraction
        depth_val = phys.get("d", 0.0)

        # Telemetry Velocities
        sim_3d_vel = float(phys.get("v", 0.0))
        sim_v_vel = float(phys.get("vv", 0.0))

        # Telemetry H. Vel = sqrt(3D^2 - V^2)
        diff_sq = sim_3d_vel**2 - sim_v_vel**2
        sim_h_vel = math.sqrt(diff_sq) if diff_sq > 0 else 0.0

        dyn_accel_val = phys.get("dacc", [0.0, 0.0, 0.0])
        if not isinstance(dyn_accel_val, list) or len(dyn_accel_val) < 3:
            dyn_accel_val = [0.0, 0.0, 0.0]

        static_accel_val = phys.get("sacc", [0.0, 0.0, 0.0])
        if not isinstance(static_accel_val, list) or len(static_accel_val) < 3:
            static_accel_val = [0.0, 0.0, 0.0]

        # Attitude
        # rot_str = self._get_rph(state.get("rot_data"))
        # Extract RPH values for direct display
        rph_tuple = self._get_rph_values(state.get("rot_data"))
        roll_val, pitch_val, heading_val = rph_tuple if rph_tuple else (0.0, 0.0, 0.0)

        # ODBA / VeDBA
        odba_val = phys.get("odba", 0.0)
        vedba_val = phys.get("vedba", 0.0)

        # Current Position (from Active Trail if available, else Physics)
        # We calculated pos_cur above if trail exists
        pos_val = [0.0, 0.0, 0.0]
        if self._active_eid != -1:
            active_trail = self._entities_trail_buffers.get(self._active_eid)
            if active_trail and active_trail["buffer"]:
                p_now = active_trail["buffer"][-1]
                pos_cur = p_now[1]
                pos_val = [
                    pos_cur[0] / 100.0,
                    pos_cur[1] / 100.0,
                    pos_cur[2] / 100.0,
                ]  # Convert cm to m

        # Drift values
        sim_clock_drift_val = float(phys.get("cd", 0.0))
        est_clock_drift_val = float(state.get("est_clock_drift", 0.0))

        # 3. Invoke Update Helper
        self._update_hud_labels(
            self._connection_status,
            sim_id,
            self._packet_count,
            self._throughput_str,
            time_str,
            roll_val,
            pitch_val,
            heading_val,
            alpha_val,
            beta_val,
            path_str,
            depth_val,
            sim_3d_vel,
            sim_h_vel,
            sim_v_vel,
            est_h_vel,
            est_v_vel,
            est_3d_vel,
            odba_val,
            vedba_val,
            dyn_accel_val,
            static_accel_val,
            pos_val,
            sim_clock_drift_val,
            est_clock_drift_val,
        )

    def _update_hud_labels(
        self,
        status: str,
        animal_name: str,
        packets: int,
        tps: str,
        time_str: str,
        roll: float,
        pitch: float,
        heading: float,
        alpha: float,
        beta: float,
        path_info: str,
        depth: float,
        sim_3d_vel: float,
        sim_h_vel: float,
        sim_v_vel: float,
        est_h_vel: float,
        est_v_vel: float,
        est_3d_vel: float,
        odba: float,
        vedba: float,
        dyn_accel: list[float],
        static_accel: list[float],
        pos: list[float],
        sim_clock_drift: float,
        est_clock_drift: float,
    ) -> None:
        """Pure UI update function."""
        # Determine colors based on Debug Vectors checkbox
        # Default Soft Gray: 0xFFCCCCDD
        # Red (Orientation): 0xFF6666FF (Soft Red)
        # Green (Trajectory): 0xFF66FF66 (Soft Green)

        # Assuming standard Kit Checkbox logic
        debug_active = False
        if hasattr(self, "_debug_vec_checkbox") and self._debug_vec_checkbox:
            debug_active = self._debug_vec_checkbox.model.get_value_as_bool()

        def_color = 0xFFCCCCDD
        orient_color = 0xFF6666FF if debug_active else def_color
        path_color = 0xFF66FF66 if debug_active else def_color

        # Connection Stats
        self._hud_status_label.text = f"Status: {self._connection_status}"
        self._hud_packet_label.text = f"Packets: {packets}"
        self._hud_throughput_label.text = f"TPS: {tps}"
        self._hud_time_label.text = time_str

        # Active Animal
        self._hud_active_animal_label.text = f"ENTITY: {animal_name}"

        # Telemetry
        self._hud_sim_clock_drift.text = f"Clock Drift: {sim_clock_drift:+.4f}s"
        self._hud_orientation_label.text = (
            f"Orientation: R:{roll:.1f} P:{pitch:.1f} H:{heading:.1f}"
        )
        self._hud_orientation_label.style = {"color": orient_color}
        self._hud_path_label.text = f"Trajectory: {path_info}"
        self._hud_path_label.style = {"color": path_color}
        self._hud_attack_angle_label.text = f"Attack Angle: {alpha:.1f}°"
        self._hud_sideslip_label.text = f"Sideslip: {beta:.1f}°"
        self._hud_depth_label.text = f"Depth: {depth:.1f} m"
        self._hud_sim_3d_vel.text = f"3D Vel: {sim_3d_vel:.2f} m/s"
        self._hud_sim_h_vel.text = f"H. Vel: {sim_h_vel:.2f} m/s"
        self._hud_sim_v_vel.text = f"V. Vel: {sim_v_vel:.2f} m/s"
        self._hud_odba_label.text = f"ODBA: {odba:.2f}"
        self._hud_vedba_label.text = f"VeDBA: {vedba:.2f}"
        self._hud_accel_label.text = (
            f"Dyn. Accel: [{dyn_accel[0]:.1f}, {dyn_accel[1]:.1f}, {dyn_accel[2]:.1f}]"
        )
        self._hud_static_accel_label.text = (
            f"Static Accel: [{static_accel[0]:.1f}, {static_accel[1]:.1f}, {static_accel[2]:.1f}]"
        )
        self._hud_pos_label.text = f"Pos: [{pos[0]:.1f}, {pos[1]:.1f}, {pos[2]:.1f}]"

        # Derived Metrics (Drift & Speed)
        self._hud_est_clock_drift.text = f"Clock Drift: {est_clock_drift:+.4f}s"
        self._hud_est_3d_vel.text = f"3D Vel: {est_3d_vel:.2f} m/s"
        self._hud_est_h_vel.text = f"H. Vel: {est_h_vel:.2f} m/s"
        self._hud_est_v_vel.text = f"V. Vel: {est_v_vel:.2f} m/s"
        # Attack Angle/Sideslip updated above using alpha/beta

    def _get_rph_values(self, rot_data: list[float] | None) -> tuple[float, float, float] | None:
        """Helper to extract Roll, Pitch, Heading values from rotation data."""
        if not rot_data:
            return None

        # Check if it's Euler [r, p, h] or Quat [r, i, j, k]
        # Assuming ZMQ payload sends Euler [r, p, h] as standard from lab.py
        # But if it sends Quat, we need conversion.
        # lab.py sends "rot": [roll, pitch, heading] unless using quat.

        if len(rot_data) == 3:
            # Assume Euler [Roll, Pitch, Heading]
            return (rot_data[0], rot_data[1], rot_data[2])
        elif len(rot_data) == 4:
            # Assume Quaternion
            # We already have _compute_orientation, but that returns Gf.Quatf.
            # We want Euler degrees for display.
            # For now, if 4, just return 0s or try to decompose?
            # lab.py default is Euler.
            return (0.0, 0.0, 0.0)
        return None

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
            h = -h_raw
            r = float(q_data[0]) + off_r

            # Store raw heading for CSV logging
            self._last_ned_heading = h_raw

            # Create Rotations
            rot_yaw = Gf.Rotation(Gf.Vec3d(0, 1, 0), h)
            rot_pitch = Gf.Rotation(Gf.Vec3d(1, 0, 0), p)
            rot_roll = Gf.Rotation(Gf.Vec3d(0, 0, -1), r)

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
                return

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
                raw_d = phys.get("d")
                raw_px = phys.get("px")
                raw_py = phys.get("py")

                # Guard against None or NaN
                # If any coordinate is NaN, we skip the update to prevent breaking the USD prim
                import math

                if (
                    raw_d is not None
                    and not math.isnan(float(raw_d))
                    and raw_px is not None
                    and not math.isnan(float(raw_px))
                    and raw_py is not None
                    and not math.isnan(float(raw_py))
                ):
                    depth = float(raw_d)
                    px = float(raw_px)
                    py = float(raw_py)
                    # Legacy/CPU Mapping: Y=-depth, X=pseudo_y, Z=-pseudo_x
                    target_pos = Gf.Vec3d(py * 100.0, -depth * 100.0, -px * 100.0)
                else:
                    carb.log_warn(
                        f"Invalid position data for entity {eid} ({prim_path}): "
                        f"d={raw_d}, px={raw_px}, py={raw_py}. Skipping position update."
                    )
                    pass

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

            # Populate Segmented Trail Buffer (Only for active entity for now or per-entity)
            # Performance: Use dict to store per-entity history
            trail_state = self._entities_trail_buffers.setdefault(
                eid, {"buffer": [], "hue": (eid * 137) % 360.0, "segment_count": 0}
            )

            if target_pos and target_rot_quat:
                ts = float(state.get("ts", 0.0))
                odba = float(phys.get("odba", 0.0)) if phys else 0.0

                # Record path history
                # Filter duplicates: Only append if timestamp > last timestamp (or empty)
                # This prevents "Sample and Hold" artifacts at slow playback speeds
                should_append = True
                if trail_state["buffer"]:
                    last_ts = trail_state["buffer"][-1][0]
                    if ts <= last_ts:
                        should_append = False

                if should_append:
                    trail_state["buffer"].append((ts, Gf.Vec3f(target_pos), target_rot_quat, odba))

                # Segment Baking (Infinite Trail Logic)
                if len(trail_state["buffer"]) >= self._trail_segment_size:
                    self._bake_trail_segment(stage, eid, trail_state)

        except Exception as e:
            if not hasattr(self, "_pose_error_shown"):
                carb.log_error(f"[whoimpg.biologger] Error updating pose: {e}")
                self._pose_error_shown = True

    def _update_prim(self, stage_event: Any) -> None:
        """Main update loop triggered every frame."""
        # Enforce navigation block if follow mode is active
        if self._follow_mode_enabled:
            s = carb.settings.get_settings()
            # Try multiple common paths for Kit 109+
            paths = [
                "/app/viewport/camManipulation/enabled",
                "/app/viewport/gamepadCameraControl",
                "/app/viewport/navigation/enabled",
                "/persistent/app/viewport/camManipulation/enabled",
            ]
            for p in paths:
                if s.get(p):
                    s.set(p, False)
                    carb.log_warn(f"[whoimpg.biologger] Suppressing viewport setting: {p}")

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
                            carb.log_error(f"Error spawning eid {eid}: {e}")

                    task.add_done_callback(_on_spawn_done)
                    continue

                if state.get("path") != "PENDING":
                    self._update_animal_pose(stage, eid, state)

            # Global Trail Update (All entities, persistent)
            self._update_trail(stage, None)

            # Debug Vectors
            # Always call if we have an entity, so it can handle Hide if disabled
            active_state = self._entities_state.get(self._active_eid)
            if active_state and active_state.get("path") and active_state["path"] != "PENDING":
                prim = stage.GetPrimAtPath(active_state["path"])
                if prim.IsValid():
                    self._update_debug_vectors(stage, prim)

            # Camera follow logic - always update when follow mode is enabled
            if self._follow_mode_enabled:
                # Get active entity prim if available
                target_prim = None
                active_state = self._entities_state.get(self._active_eid)
                if (
                    active_state
                    and active_state.get("path")
                    and active_state.get("path") != "PENDING"
                ):
                    prim = stage.GetPrimAtPath(active_state["path"])
                    if prim and prim.IsValid():
                        target_prim = prim

                # Always update camera (will use origin if no target yet)
                self._update_follow_camera(stage, target_prim)
        except Exception as e:
            if not hasattr(self, "_update_error_shown"):
                carb.log_error(f"[whoimpg.biologger] Error updating prim: {e}")
                import traceback

                traceback.print_exc()
                self._update_error_shown = True

    def _on_follow_mode_changed(self, model: ui.AbstractValueModel) -> None:
        val = model.get_value_as_bool()
        carb.log_info(
            f"[whoimpg.biologger] _on_follow_mode_changed entry: {val} "
            f"(Current state: {self._follow_mode_enabled})"
        )
        self._follow_mode_enabled = val
        carb.log_info(f"[whoimpg.biologger] Follow mode state updated to: {val}")

        if val:
            # Store current camera to restore later
            self._previous_camera_path = omni.kit.viewport.utility.get_active_viewport_camera_path()

            # Create follow camera if needed (now targets /OmniverseKit_Persp)
            self._ensure_follow_camera()

            # Switch to follow camera (now just ensures /OmniverseKit_Persp is active)
            # self._set_active_camera("/OmniverseKit_Persp") # Optional, usually already active

            # CRITICAL: Disable viewport navigation so it doesn't override our camera transforms
            try:
                viewport_window = omni.kit.viewport.utility.get_active_viewport_window()
                if viewport_window and hasattr(viewport_window, "viewport_api"):
                    # Steal focus back to viewport to ensure hotkeys work
                    if hasattr(viewport_window, "focus"):
                        viewport_window.focus()

                    # Store current navigation state to restore later
                    settings = carb.settings.get_settings()
                    # Store current navigation state to restore later
                    # Check both persistent and live app paths
                    self._viewport_nav_enabled = settings.get(
                        "/app/viewport/camManipulation/enabled"
                    )
                    if self._viewport_nav_enabled is None:
                        self._viewport_nav_enabled = settings.get(
                            "/persistent/app/viewport/camManipulation/enabled"
                        )

                    # Force disable navigation (Live and Persistent paths)
                    settings.set("/app/viewport/camManipulation/enabled", False)
                    settings.set("/persistent/app/viewport/camManipulation/enabled", False)

                    # Also disable gamepad just in case
                    settings.set("/app/viewport/gamepadCameraControl", False)
                    settings.set("/persistent/app/viewport/gamepadCameraControl", False)

                    carb.log_info("[whoimpg.biologger] Viewport navigation DISABLED (Aggressive).")
            except Exception as e:
                carb.log_error(f"[whoimpg.biologger] Could not disable viewport navigation: {e}")

        else:
            # Re-enable viewport navigation
            try:
                if hasattr(self, "_viewport_nav_enabled"):
                    settings = carb.settings.get_settings()
                    restore_val = (
                        self._viewport_nav_enabled
                        if self._viewport_nav_enabled is not None
                        else True
                    )
                    settings.set("/app/viewport/camManipulation/enabled", restore_val)
                    settings.set("/persistent/app/viewport/camManipulation/enabled", restore_val)
                    settings.set("/app/viewport/gamepadCameraControl", True)
                    settings.set("/persistent/app/viewport/gamepadCameraControl", True)
                    delattr(self, "_viewport_nav_enabled")
            except Exception as e:
                carb.log_error(f"[whoimpg.biologger] Could not restore viewport navigation: {e}")
            # Note: We hijack the active camera, so no need to switch back.

    def _on_input_event(self, event: carb.input.InputEvent) -> bool:
        """Central hub for all user inputs (Keyboard & Gamepad)"""
        if event.deviceType == carb.input.DeviceType.KEYBOARD:
            e = event.event
            carb.log_info(
                f"[whoimpg.biologger] INPUT DEBUG: Keyboard Event Type={e.type} "
                f"Input={e.input} (Val={int(e.input)})"
            )

        now = time.time()

        # Heartbeat: Print input activity every 5s
        if now - self._last_input_heartbeat > 5.0:
            self._last_input_heartbeat = now
            safe_type = getattr(event.event, "type", "N/A")
            carb.log_info(f"[whoimpg.biologger] HB: Dev={event.deviceType} Ev={safe_type}")

        # 1. Gamepad Handling
        if event.deviceType == carb.input.DeviceType.GAMEPAD:
            pad_input = event.event.input
            val = event.event.value

            # Buttons (Threshold > 0.5)
            if val > 0.5:
                if pad_input == carb.input.GamepadInput.LEFT_SHOULDER:
                    self._cycle_active_animal(-1)
                    return True
                if pad_input == carb.input.GamepadInput.RIGHT_SHOULDER:
                    self._cycle_active_animal(1)
                    return True
                if pad_input == carb.input.GamepadInput.X:
                    carb.log_info("[whoimpg.biologger] GP Button X: Snap triggered.")
                    self._follow_mode_enabled = not self._follow_mode_enabled

                    # Update UI (prevents double-toggle)
                    if hasattr(self, "_follow_mode_checkbox"):
                        self._follow_mode_checkbox.model.set_value(self._follow_mode_enabled)

                    # Force Snap directly
                    if self._follow_mode_enabled:
                        self._cam_smooth_pos = None
                        stage = omni.usd.get_context().get_stage()
                        if stage:
                            astate = self._entities_state.get(self._active_eid)
                            if astate and astate.get("path"):
                                prim = stage.GetPrimAtPath(astate["path"])
                                if prim:
                                    self._update_follow_camera(stage, prim, force_snap=True)
                    return True

            # Axes (Continuous)
            if self._follow_mode_enabled:
                # Debug logging for ANY stick input to identify ID mismatch
                if abs(val) > 0.1 and (now - self._last_gp_heartbeat > 0.5):
                    self._last_gp_heartbeat = now
                    carb.log_info(f"[whoimpg.biologger] GP Axis Active: {pad_input} Val={val:.2f}")

                def get_val(v: float) -> float:
                    return v if abs(v) > 0.1 else 0.0

                # Input consumption flag
                is_stick_input = False

                # Left Stick Up (Signed Zoom)
                if pad_input == carb.input.GamepadInput.LEFT_STICK_UP:
                    self._cam_distance -= get_val(val) * 20.0
                    self._cam_distance = max(50.0, min(10000.0, self._cam_distance))
                    is_stick_input = True

                # Right Stick Right (Signed Azimuth)
                if pad_input == carb.input.GamepadInput.RIGHT_STICK_RIGHT:
                    self._cam_azimuth -= get_val(val) * 2.0
                    is_stick_input = True

                # Right Stick Up (Signed Elevation)
                if pad_input == carb.input.GamepadInput.RIGHT_STICK_UP:
                    self._cam_elevation -= get_val(val) * 2.0
                    self._cam_elevation = max(-89.0, min(89.0, self._cam_elevation))
                    is_stick_input = True

                # Aggressive Consumption: If ANY stick axis is moving > 0.1, block viewport nav
                if is_stick_input or abs(val) > 0.1:
                    return True

            return False

        # 2. Mouse handling
        if event.deviceType == carb.input.DeviceType.MOUSE:
            e = event.event

            # Safe attribute access
            mi = getattr(e, "mouseInput", None)
            val = getattr(e, "value", 0.0)

            # If we are NOT in follow mode, let events pass normally
            if not self._follow_mode_enabled:
                return False

            # --- Logic: RMB Drag to Orbit ---
            if mi == carb.input.MouseInput.RIGHT_BUTTON:
                is_down = val > 0.5
                self._is_rmb_down = is_down

                # On press, mark position as valid/reset delta logic if needed
                # (We track position continuously below)
                return True  # Consume RMB to prevent context menu

            # Detect Mouse Move
            # Robust check: If no specific button input (mi is None), and we have position,
            # assume move.
            is_move = mi is None and hasattr(e, "position")

            # Also check if it is explicitly a move type if we can safely detect it
            if (
                not is_move
                and hasattr(carb.input, "MouseEventType")
                and hasattr(e, "type")
                and e.type == getattr(carb.input.MouseEventType, "MOVE", -999)
            ):
                is_move = True

            if is_move:
                # Mouse Move Event
                # CAUTION: 'position' may be normalized or absolute pixels depending on OS/Setting
                # typically 'pixelPosition' or 'position' (normalized)

                # Try to get position (Tuple[float, float])
                # Note: carb.input provides normalized coordinates (0..1) typically
                pos = getattr(e, "position", None)
                if pos:
                    x, y = pos.x, pos.y  # Attributes of Float2

                    if self._is_rmb_down and self._last_mouse_pos_valid:
                        # Calculate Delta (Normalized coords)
                        dx = x - self._last_mouse_pos[0]
                        dy = y - self._last_mouse_pos[1]

                        # Sensitivity Tuning
                        # dx=1.0 is full screen width.
                        # orbit 360 deg = 1.0 screen width? Maybe
                        sens_x = 300.0
                        sens_y = 150.0

                        self._cam_azimuth -= dx * sens_x
                        self._cam_elevation += dy * sens_y

                        # Clamp Elevation
                        self._cam_elevation = max(-89.0, min(89.0, self._cam_elevation))

                    # Update last pos
                    self._last_mouse_pos = (x, y)
                    self._last_mouse_pos_valid = True

                    # If dragging, consume event
                    if self._is_rmb_down:
                        return True

            # --- Logic: Scroll to Zoom ---
            # carb.input.MouseInput has SCROLL_UP / SCROLL_DOWN, not generic SCROLL
            # (Use getattr to be safe against version diffs, but error log confirmed SCROLL_UP
            # exists)
            scroll_up = getattr(carb.input.MouseInput, "SCROLL_UP", None)
            scroll_down = getattr(carb.input.MouseInput, "SCROLL_DOWN", None)

            if mi is not None and mi in (scroll_up, scroll_down):
                # Determine direction
                direction = 1.0 if mi == scroll_up else -1.0

                # Scroll delta in 'value' (often 1.0 per tick)
                # Zoom In (UP) -> Decrease Distance
                # Zoom Out (DOWN) -> Increase Distance
                # Note: direction * value gives signed delta

                zoom_speed = 100.0 if abs(val) < 10.0 else 10.0
                delta = direction * val * zoom_speed

                self._cam_distance -= delta
                self._cam_distance = max(50.0, min(10000.0, self._cam_distance))
                return True

            # Consume Middle Button to prevent panning if desired
            return bool(mi == carb.input.MouseInput.MIDDLE_BUTTON)

        # 3. Keyboard handling
        if event.deviceType == carb.input.DeviceType.KEYBOARD:
            # Allow PRESS, REPEAT, and RELEASE to pass through for consumption
            if event.event.type not in [
                carb.input.KeyboardEventType.KEY_PRESS,
                carb.input.KeyboardEventType.KEY_REPEAT,
                carb.input.KeyboardEventType.KEY_RELEASE,
            ]:
                return False

            k = event.event.input
            evt_type = event.event.type

            # Debug: Log every key press to help identify codes
            if evt_type == carb.input.KeyboardEventType.KEY_PRESS:
                carb.log_info(f"[whoimpg.biologger] Key Press: {k} (Val: {int(k)})")

            def is_key(key_in: Any, names: list[str]) -> bool:
                for name in names:
                    v = getattr(carb.input.KeyboardInput, name, None)
                    if key_in == v:
                        return True
                    if not name.startswith("KEY_"):
                        v = getattr(carb.input.KeyboardInput, f"KEY_{name}", None)
                        if key_in == v:
                            return True
                return False

            # Selection
            # Ensure "consuming" return True actually stops UI propogation
            is_press = evt_type == carb.input.KeyboardEventType.KEY_PRESS

            if is_key(k, ["NUM_1", "KEY_1"]) and is_press:
                self._cycle_active_animal(0, 0)
                return True
            if is_key(k, ["NUM_2", "KEY_2"]) and is_press:
                self._cycle_active_animal(0, 1)
                return True
            if is_key(k, ["NUM_3", "KEY_3"]) and is_press:
                self._cycle_active_animal(0, 2)
                return True
            if is_key(k, ["NUM_4", "KEY_4"]) and is_press:
                self._cycle_active_animal(0, 3)
                return True
            if is_key(k, ["NUM_5", "KEY_5"]) and is_press:
                self._cycle_active_animal(0, 4)
                return True

            # Cycling Shortcuts ([ and ])
            if is_key(k, ["LEFT_BRACKET", "BRACKET_LEFT"]) and is_press:
                carb.log_info("[whoimpg.biologger] Shortcut: Cycle Previous Animal")
                self._cycle_active_animal(-1)
                return True
            if is_key(k, ["RIGHT_BRACKET", "BRACKET_RIGHT"]) and is_press:
                carb.log_info("[whoimpg.biologger] Shortcut: Cycle Next Animal")
                self._cycle_active_animal(1)
                return True

            if is_key(k, ["P"]):
                # Toggle Follow Mode (ON PRESS ONLY)
                if evt_type == carb.input.KeyboardEventType.KEY_PRESS:
                    self._follow_mode_enabled = not self._follow_mode_enabled
                    if hasattr(self, "_follow_mode_checkbox"):
                        self._follow_mode_checkbox.model.set_value(self._follow_mode_enabled)

                    carb.log_info(
                        f"[whoimpg.biologger] Follow Mode Toggled via Key 'P': "
                        f"{self._follow_mode_enabled}"
                    )

                    if self._follow_mode_enabled:
                        stage = omni.usd.get_context().get_stage()
                        if stage:
                            active_state = self._entities_state.get(self._active_eid)
                            if active_state and active_state.get("path"):
                                target_prim = stage.GetPrimAtPath(active_state["path"])
                                if target_prim:
                                    self._cam_smooth_pos = None
                                    self._update_follow_camera(stage, target_prim, force_snap=True)

                # Consume BOTH Press and Release to prevent "Parent" command
                return True

            # Navigation
            sens = 5.0
            if is_key(k, ["A", "LEFT"]):
                self._cam_azimuth += sens
                return True
            if is_key(k, ["D", "RIGHT"]):
                self._cam_azimuth -= sens
                return True

            # Elevation (W/S)
            if is_key(k, ["W"]):
                # W = Elevation Up
                self._cam_elevation = min(89.0, self._cam_elevation + sens)
                return True
            if is_key(k, ["S"]):
                # S = Elevation Down
                self._cam_elevation = max(-89.0, self._cam_elevation - sens)
                return True

            # Zoom (Up/Down)
            if is_key(k, ["UP", "EQUAL", "PLUS"]):
                # Up/Plus = Zoom In (Decrease Distance)
                self._cam_distance = max(50.0, self._cam_distance - 100.0)
                return True
            if is_key(k, ["DOWN", "MINUS"]):
                # Down/Minus = Zoom Out (Increase Distance)
                self._cam_distance = min(10000.0, self._cam_distance + 100.0)
                return True

            # UI
            if is_key(k, ["F5"]):
                w = ui.Workspace.get_window("Stage")
                if w:
                    w.visible = not w.visible
                return True
            if is_key(k, ["F6"]):
                w = ui.Workspace.get_window("Timeline")
                if w:
                    w.visible = not w.visible
                return True

        return False

    def _toggle_hud_visibility(self) -> None:
        """Toggles the HUD window visibility safely"""
        # Manual toggle implies user wants to see/hide it
        if hasattr(self, "_hud_window") and self._hud_window:
            self._hud_window.visible = not self._hud_window.visible
            if self._hud_window.visible:
                self._hud_window.focus()
            carb.log_info(f"[whoimpg.biologger] HUD Visibility toggled: {self._hud_window.visible}")
        else:
            # Try to recover if lost (e.g. if User closed it via X and it was destroyed)
            w = ui.Workspace.get_window("Biologger HUD")
            if w:
                carb.log_info("[whoimpg.biologger] Recovered HUD window handle from Workspace.")
                self._hud_window = w
                try:
                    ws_width = ui.Workspace.get_main_window_width()
                    self._hud_window.position_x = (
                        ws_width - (HUD_WINDOW_WIDTH + 20) if ws_width > 100 else HUD_WINDOW_X_POS
                    )
                except AttributeError:
                    self._hud_window.position_x = HUD_WINDOW_X_POS
                self._hud_window.position_y = HUD_WINDOW_Y_POS
                self._hud_window.visible = True
                self._hud_window.focus()
            else:
                carb.log_warn("[whoimpg.biologger] HUD Window not found to toggle.")

    def _set_active_camera(self, camera_path: str) -> None:
        """
        Set the active camera using modern Kit 105+ APIs.

        Prioritizes the Viewport Window API (viewport_api.camera_path).
        Falls back to 'LookThroughCamera' command if the direct API is unavailable.
        Legacy methods (Kit <105) have been deprecated and removed.
        """
        carb.log_info(f"[whoimpg.biologger] Switching camera to: {camera_path}")

        # Method 1: Try Viewport Window API (Direct & Preferred for Kit 105+)
        # This allows setting the camera without populating the undo stack (which is often preferred
        # during simulation playback) and works reliably when the Viewport extension is active.
        try:
            viewport_window = omni.kit.viewport.utility.get_active_viewport_window()
            if viewport_window and hasattr(viewport_window, "viewport_api"):
                viewport_window.viewport_api.camera_path = camera_path
                carb.log_info(f"[whoimpg.biologger] ✓ Viewport camera set to: {camera_path}")
                return
        except Exception as e:
            carb.log_error(f"[whoimpg.biologger] Viewport Window API failed: {e}")

        # Method 2: Try LookThroughCamera command (Standard Fallback)
        try:
            omni.kit.commands.execute("LookThroughCamera", camera_path=camera_path)
            return
        except Exception as e:
            carb.log_error(f"[whoimpg.biologger] Command 'LookThroughCamera' failed: {e}")

        carb.log_error("[whoimpg.biologger] Error: Could not switch camera (all methods failed).")

    def _ensure_follow_camera(self) -> None:
        # Deprecated: We now hijack the main viewport camera (/OmniverseKit_Persp)
        # logic handled in _update_follow_camera
        pass

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
        carb.log_info(f"[whoimpg.biologger] Safe Mode set to: {val}")
        if val:
            # Clear history immediately to free memory
            self._entities_trail_buffers.clear()

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

        # Check overall visibility
        is_visible = True
        if hasattr(self, "_trail_checkbox") and not self._trail_checkbox.model.get_value_as_bool():
            is_visible = False

        # Return early if no active entities to track or not visible
        if not self._entities_trail_buffers or not is_visible:
            self._last_trail_update_ms = 0.0
            parent_prim = stage.GetPrimAtPath(self._trail_prim_path)
            if parent_prim.IsValid():
                UsdGeom.Imageable(parent_prim).MakeInvisible()
            return

        # Iterate over all entity trail buffers and update/render them
        for eid, trail_state in self._entities_trail_buffers.items():
            buffer = trail_state["buffer"]
            if not buffer or len(buffer) < 2:
                continue

            # Path for the ACTIVE segment (the one currently being populated)
            active_trail_path = f"{self._trail_prim_path}/Trail_{eid}_active"

            # Decimate for visualization performance
            max_visual_points = 5000
            step = max(1, len(buffer) // max_visual_points)
            visual_buffer = buffer[::step]

            # Base Hue for this entity
            base_hue = trail_state.get("hue", 0.0)

            # Render the active curve
            self._render_curve(stage, active_trail_path, visual_buffer, base_hue)

        t1 = time.perf_counter()
        self._last_trail_update_ms = (t1 - t0) * 1000.0

    def _render_curve(
        self, stage: Usd.Stage, path: str, visual_buffer: list, base_hue: float
    ) -> None:
        points = [p[1] for p in visual_buffer]
        colors = []

        for p in visual_buffer:
            odba = p[3] if len(p) > 3 else 0.0
            # Gradient Expansion: Broad "Cold Plateau" for normal swimming.
            # 0.1 (Rest) -> Cyan (180°)
            # 0.85 (Steady) -> Green/Yellow (90°)
            # 1.6+ (Burst) -> Red (0°)
            norm = min(max((odba - 0.1) / 1.5, 0.0), 1.0)

            # Hue: Cyan (180°) -> Yellow (60°) -> Red (0°)
            h = (180.0 - 180.0 * norm) / 360.0
            s = 0.8 + 0.2 * norm  # High base saturation for vibrancy
            v = 0.7 + 0.3 * norm  # Vibrant brightness

            rgb = colorsys.hsv_to_rgb(h, s, v)
            colors.append(Gf.Vec3f(rgb[0], rgb[1], rgb[2]))

        prim = stage.GetPrimAtPath(path)
        curves = None
        if not prim.IsValid():
            curves = UsdGeom.BasisCurves.Define(stage, path)
            curves.CreateTypeAttr(UsdGeom.Tokens.linear)
            curves.CreateWidthsAttr(Vt.FloatArray([5.0]))
            curves.SetWidthsInterpolation(UsdGeom.Tokens.constant)
        else:
            curves = UsdGeom.BasisCurves(prim)

        # Bind Neon Material
        mat_path = self._ensure_trail_material(stage)
        UsdShade.MaterialBindingAPI(curves).Bind(UsdShade.Material(stage.GetPrimAtPath(mat_path)))

        curves.GetCurveVertexCountsAttr().Set(Vt.IntArray([len(points)]))
        points_tuples = [(p[0], p[1], p[2]) for p in points]
        curves.GetPointsAttr().Set(Vt.Vec3fArray(points_tuples))

        primvar_api = UsdGeom.PrimvarsAPI(curves.GetPrim())
        if curves.GetPrim().HasAttribute("primvars:displayColor:indices"):
            curves.GetPrim().RemoveProperty("primvars:displayColor:indices")

        color_primvar = primvar_api.CreatePrimvar("displayColor", Sdf.ValueTypeNames.Color3fArray)
        color_primvar.SetInterpolation(UsdGeom.Tokens.vertex)
        colors_tuples = [(c[0], c[1], c[2]) for c in colors]
        color_primvar.Set(Vt.Vec3fArray(colors_tuples))

    def _bake_trail_segment(self, stage: Usd.Stage, eid: int, trail_state: dict) -> None:
        """Bakes the current trail buffer into a static USD prim and clears the buffer."""
        seg_idx = trail_state["segment_count"]
        path = f"{self._trail_prim_path}/Trail_{eid}_seg_{seg_idx}"

        carb.log_info(f"[whoimpg.biologger] Baking trail segment for EID {eid} to {path}")

        # Render the final static segment
        self._render_curve(stage, path, trail_state["buffer"], trail_state["hue"])

        # Increment counter and clear buffer for next segment
        trail_state["segment_count"] += 1
        # Keep the last point as the start of the next segment to maintain connectivity
        last_pt = trail_state["buffer"][-1]
        trail_state["buffer"] = [last_pt]

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

        # Use active entity for debug vectors
        trail_state = self._entities_trail_buffers.get(self._active_eid)
        if not trail_state or not trail_state["buffer"] or len(trail_state["buffer"]) < 2:
            return

        # Get latest state
        p_now = trail_state["buffer"][-1]
        p_prev = trail_state["buffer"][-2]
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

                # Refresh prim pointer
                prim = curves.GetPrim()
            else:
                curves = UsdGeom.BasisCurves(prim)

            # Line from Shark Center to Vector Tip
            points = [pos_cur_d, pos_cur_d + end_pos]
            curves.GetCurveVertexCountsAttr().Set(Vt.IntArray([2]))
            # Convert Vec3d to Vec3f for the point array
            points_f = [Gf.Vec3f(p[0], p[1], p[2]) for p in points]
            curves.GetPointsAttr().Set(Vt.Vec3fArray(points_f))

            # Ensure vector is visible
            if prim.IsValid():
                UsdGeom.Imageable(prim).MakeVisible()

        # Green = Velocity (Truth)
        draw_line("Velocity", Gf.Vec3f(0, 1, 0), vel_vec)
        # Red = Heading (Sensor)
        draw_line("Heading", Gf.Vec3f(1, 0, 0), head_vec)

    def _update_follow_camera(
        self, stage: Usd.Stage, target_prim: Usd.Prim | None, force_snap: bool = False
    ) -> None:
        # Throttle update logging
        t_now = time.time()
        if not hasattr(self, "_last_cam_debug_time"):
            self._last_cam_debug_time = 0.0

        if t_now - self._last_cam_debug_time > 2.0:
            self._last_cam_debug_time = t_now
            target_path = target_prim.GetPath() if target_prim else "None"
            carb.log_info(
                f"[whoimpg.biologger] _update_follow_camera: "
                f"enabled={self._follow_mode_enabled} force={force_snap} target={target_path}"
            )

        # 1. State Check: Only run if follow mode is enabled OR we are forcing a snap (F key)
        if not self._follow_mode_enabled and not force_snap:
            self._cam_smooth_pos = None  # Reset smoothing on exit
            return

        # 2. Get the Active Viewport Camera (The hijack!)
        import omni.kit.viewport.utility

        viewport_window = omni.kit.viewport.utility.get_active_viewport_window()
        if not viewport_window:
            return

        viewport_api = getattr(viewport_window, "viewport_api", None)
        if not viewport_api:
            # Fallback for older Kit versions or specific contexts
            viewport_api = omni.kit.viewport.utility.get_active_viewport()

        if not viewport_api:
            return

        camera_path = viewport_api.camera_path
        camera_prim = stage.GetPrimAtPath(camera_path)
        if not camera_prim.IsValid():
            return

        # 3. Get Target Position
        target_trans = Gf.Vec3d(0, 0, 0)
        if target_prim and target_prim.IsValid():
            target_xform = UsdGeom.Xformable(target_prim)
            target_mat = target_xform.ComputeLocalToWorldTransform(Usd.TimeCode.Default())
            target_trans = target_mat.ExtractTranslation()

        if not hasattr(self, "_cam_distance"):
            self._cam_distance = 1500.0

        # Debug Printing (Throttled)
        if not hasattr(self, "_last_orbit_debug_time"):
            self._last_orbit_debug_time = 0.0

        if time.time() - self._last_orbit_debug_time > 5.0:
            carb.log_info(
                f"[whoimpg.biologger] Following EID {self._active_eid} with '{camera_path}'"
            )
            self._last_orbit_debug_time = time.time()

        # 4. Calculate Desired Camera Position (Orbit Logic)
        az_rad = self._cam_azimuth * (math.pi / 180.0)
        el_rad = self._cam_elevation * (math.pi / 180.0)

        # X-Z plane rotation (azimuth) + Y offset (elevation)
        follow_dist = self._cam_distance
        horizontal_dist = follow_dist * math.cos(el_rad)

        # Note: Depending on coordinate system, sin and cos mapping varies.
        # Assuming Y-up, -Z forward for standard orbit.
        offset_x = horizontal_dist * math.sin(-az_rad)
        offset_y = follow_dist * math.sin(el_rad)
        offset_z = horizontal_dist * math.cos(-az_rad)

        desired_pos = target_trans + Gf.Vec3d(offset_x, offset_y, offset_z)

        # 5. Smoothing (Lerp)
        final_pos = desired_pos

        if force_snap:
            final_pos = desired_pos
            self._cam_smooth_pos = desired_pos
        elif self._cam_smooth_pos is not None:
            # Simple Lerp
            alpha = 0.1  # Smoothing factor (frame-rate dependent, but acceptable for simple sim)
            cur = self._cam_smooth_pos

            # Lerp each component
            lx = cur[0] + (desired_pos[0] - cur[0]) * alpha
            ly = cur[1] + (desired_pos[1] - cur[1]) * alpha
            lz = cur[2] + (desired_pos[2] - cur[2]) * alpha

            final_pos = Gf.Vec3d(lx, ly, lz)
            self._cam_smooth_pos = final_pos
        else:
            # First frame initialization
            self._cam_smooth_pos = desired_pos
            final_pos = desired_pos

        # 6. Apply Transform to Camera
        cam_xform = UsdGeom.Xformable(camera_prim)

        # Calculate LookAt Matrix
        # Z axis points FROM target TO eye (Standard USD Camera looks down -Z)
        z_axis = (final_pos - target_trans).GetNormalized()
        world_up = Gf.Vec3d(0, 1, 0)

        # Handle gimbal lock case (looking straight up/down)
        if abs(Gf.Dot(z_axis, world_up)) > 0.99:
            world_up = Gf.Vec3d(0, 0, 1)  # Shift up vector

        x_axis = Gf.Cross(world_up, z_axis).GetNormalized()
        y_axis = Gf.Cross(z_axis, x_axis).GetNormalized()

        mat = Gf.Matrix4d(
            x_axis[0],
            x_axis[1],
            x_axis[2],
            0.0,
            y_axis[0],
            y_axis[1],
            y_axis[2],
            0.0,
            z_axis[0],
            z_axis[1],
            z_axis[2],
            0.0,
            final_pos[0],
            final_pos[1],
            final_pos[2],
            1.0,
        )

        # We hijack the FIRST xform op or reset order to ensure WE have control
        # But for /OmniverseKit_Persp, it usually has xformOps from navigation.
        # We should overwrite the Translate and Rotate, or just set the Matrix.

        # Strategy: Clear ops and set one Matrix op.
        # This effectively overrides standard navigation while active.
        # When we release control (return early in step 1), standard nav takes over
        # (though it might snap back if it has internal state, but usually it respects USD state).

        # However, to be nice to the nav system, we might want to update the Viewport API directly
        # if possible, but writing to USD is the standard way to move the camera.

        transform_op = cam_xform.GetTransformOp()
        if not transform_op:
            cam_xform.ClearXformOpOrder()
            transform_op = cam_xform.AddTransformOp()

        # Ensure we are using the Op
        ops = cam_xform.GetOrderedXformOps()
        if len(ops) > 1 or (len(ops) == 1 and ops[0].GetName() != "xformOp:transform"):
            cam_xform.ClearXformOpOrder()
            transform_op = cam_xform.AddTransformOp()

        transform_op.Set(mat)

    def _restart_listener(self) -> None:
        """Restarts the ZMQ listener with new settings"""
        carb.log_info("[whoimpg.biologger] Restarting listener...")
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
            carb.log_warn("[whoimpg.biologger] Listener already running.")
            return

        # Get config from UI if available, otherwise defaults
        host = "127.0.0.1"
        port = 5555
        if hasattr(self, "_host_field"):
            host = self._host_field.model.get_value_as_string()
        if hasattr(self, "_port_field"):
            port = self._port_field.model.get_value_as_int()

        carb.log_info(f"[whoimpg.biologger] Starting ZMQ listener on {host}:{port}...")
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
            carb.log_error(
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
            carb.log_info(f"[whoimpg.biologger] ZMQ listener connected to {address}")
            self._connection_status = "Connected (Listening)"
        except Exception as e:
            carb.log_error(f"[whoimpg.biologger] ZMQ Connection Error: {e}")
            self._connection_status = f"Error ({str(e)[:20]}...)"
            return

        seen_eids = set()
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

                # Peek at EID for logging
                if isinstance(message, dict) and "eid" in message:
                    peid = message["eid"]
                    if peid not in seen_eids:
                        carb.log_info(f"[whoimpg.biologger] First packet for EID {peid}: {message}")
                        seen_eids.add(peid)

                # Format: { eid, sim_id, ts, rot: [r,p,h], phys: { ... } }
                if isinstance(message, dict) and "eid" in message:
                    eid = int(message["eid"])
                    sim_id = message.get("sim_id", "unknown")
                    tag_id = message.get("tag_id")
                    ts = float(message.get("ts", 0.0))

                    # Update global timestamp for UI
                    self._latest_timestamp = ts
                    self._replay_live_time = ts

                    # Resolve species for asset selection
                    species = None
                    if tag_id:
                        species = self._id_to_species.get(tag_id)
                        # Fuzzy match if exact fails
                        if not species:
                            for key, sp in self._id_to_species.items():
                                if tag_id in key or key in tag_id:
                                    species = sp
                                    break

                    if not species:
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

                    # print(
                    #    f"DEBUG: ZMQ Recv [eid={eid} vs active={self._active_eid}] ts={ts}: {phys}"
                    # )

                    # Prepare state update
                    state = self._entities_state.setdefault(eid, {"id": sim_id, "sp": species})

                    # Update placeholder ID if we have a real one now
                    # (Handles the case where default scene spawned "default" shark)
                    current_id = state.get("id")
                    if current_id == "default" and sim_id not in ("unknown", "default"):
                        state["id"] = sim_id
                        # Also update species if it was generic
                        if species != "unknown":
                            state["sp"] = species

                    state.update({"ts": ts, "rot_data": rot_data, "phys": phys})

                    # Clock Drift Calculation (Local Derived)
                    # Track simple packet count to derive "Ideal Clock"
                    # Drift = Actual - (Start + Count * 0.0625)
                    pkt_count = state.get("packet_count", 0)
                    start_ts = state.get("start_ts")

                    if start_ts is None:
                        start_ts = ts
                        state["start_ts"] = start_ts
                        # Reset count on first packet or re-init
                        pkt_count = 0

                    # Ideal time assumes 16Hz (0.0625s)
                    # TODO: Retrieve freq from config/message if possible
                    ideal_ts = start_ts + (pkt_count * 0.0625)
                    local_drift = ts - ideal_ts

                    state["packet_count"] = pkt_count + 1
                    state["est_clock_drift"] = local_drift

                    # Update global physics data for HUD (only if it's the active entity)
                    if self._active_eid == -1 or eid == self._active_eid:
                        self._latest_physics_data = phys

            except zmq.Again:
                import time

                time.sleep(0.001)
                continue
            except Exception as e:
                carb.log_error(f"Error in ZMQ loop: {e}")
                import time

                time.sleep(1.0)

    def _get_rph(self, rot_data: list[float] | None) -> str:
        if not rot_data or len(rot_data) < 3:
            return "R:-- P:-- H:--"
        return f"R:{rot_data[0]:.1f} P:{rot_data[1]:.1f} H:{rot_data[2]:.1f}"

    def _get_accel_str(self, phys: dict) -> str:
        acc = phys.get("lin_acc", [0, 0, 0])
        if isinstance(acc, list) and len(acc) >= 3:
            mag = math.sqrt(acc[0] ** 2 + acc[1] ** 2 + acc[2] ** 2)
            return f"{mag:.2f} m/s²"
        return "N/A"

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
            self._update_telemetry_window()

    def _reset_orientation(self) -> None:
        """Resets the telemetry orientation op to identity."""
        carb.log_info("[whoimpg.biologger] Resetting orientation...")
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
                carb.log_info("[whoimpg.biologger] Telemetry orientation reset to identity.")

                # Also clear the last vector string in UI
                self._last_vector_str = "Reset (Identity)"
                self._latest_quat_data = None
            else:
                carb.log_warn("[whoimpg.biologger] No telemetry orientation op found to reset.")

        except Exception as e:
            carb.log_error(f"[whoimpg.biologger] Error resetting orientation: {e}")

    def _show_timeline_window(self) -> None:
        """Helper to bring the Timeline controls to the foreground."""
        try:
            # Ensure extension is enabled using the Extension Manager
            manager = omni.kit.app.get_app().get_extension_manager()
            if not manager.is_extension_enabled("omni.anim.timeline"):
                manager.set_extension_enabled("omni.anim.timeline", True)
                carb.log_info("[whoimpg.biologger] Enabled omni.anim.timeline extension.")
            else:
                carb.log_info("[whoimpg.biologger] omni.anim.timeline is already enabled.")

            # Optional: Try to focus it via layout or command (if known working)
            # Avoiding ToggleExtension command as it requires specific arguments
            # and changes per version.
        except Exception as e:
            carb.log_error(f"[whoimpg.biologger] Error showing timeline window: {e}")

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
            carb.log_info(f"[whoimpg.biologger] Opening custom stage from setting: {custom_stage}")
            ctx.open_stage(str(custom_stage))
            if animal_type:
                await self._load_animal_asset(animal_type)
            # Create follow camera
            self._ensure_follow_camera()
            return

        if ctx.get_stage_url():
            carb.log_info(f"[whoimpg.biologger] Stage already loaded: {ctx.get_stage_url()}")
            if animal_type:
                await self._load_animal_asset(animal_type)
            # Create follow camera
            self._ensure_follow_camera()
            return

        # Check if user wants to skip default scene (for testing)
        if self._settings.get("/biologger/skipDefaultScene"):
            carb.log_info("[whoimpg.biologger] Skipping default scene (skipDefaultScene=true)")
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
                carb.log_info(f"[whoimpg.biologger] Opening default scene: {scene_path}")
                omni.usd.get_context().open_stage(str(scene_path))
                # Load the animal asset based on command line arguments
                if animal_type:
                    prim_path = await self._load_animal_asset(animal_type, eid=0, sim_id="default")
                    if prim_path:
                        # Register in state so ZMQ/UpdatePrim knows it exists
                        self._entities_state[0] = {
                            "path": prim_path,
                            "id": "default",
                            "sp": animal_type,
                            "ts": 0.0,
                            "rot_data": None,
                            "phys": {},
                        }
                # Create follow camera for the scene
                self._ensure_follow_camera()
            else:
                carb.log_warn(
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
            carb.log_error(f"cannot find executable{kit_exe}")
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
            carb.log_warn(
                "[whoimpg.biologger] Warning: Could not find "
                "biologger_meta.csv in standard locations."
            )
            return

        carb.log_info(f"[whoimpg.biologger] Loading metadata from: {meta_file}")
        try:
            with open(meta_file, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    tag_id = row.get("tag_id") or row.get("id")
                    species = row.get("species")
                    if tag_id and species:
                        self._id_to_species[tag_id] = species
        except Exception as e:
            carb.log_error(f"[whoimpg.biologger] Error loading metadata: {e}")

    def on_shutdown(self) -> None:
        """Clean up the extension"""
        # --- WHOI Biologger Subscriber Cleanup ---
        if hasattr(self, "_csv_file") and self._csv_file:
            self._csv_file.close()
            carb.log_info(f"[whoimpg.biologger] Closed log file: {self._csv_log_path}")

        # Cleanup HUD Menu
        if hasattr(self, "_menu_list"):
            omni.kit.menu.utils.remove_menu_items(self._menu_list, "Window")

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
