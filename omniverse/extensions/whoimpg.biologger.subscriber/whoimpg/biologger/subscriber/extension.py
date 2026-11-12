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
from bisect import bisect_left, bisect_right
from pathlib import Path

# Static Typing for Dynamic Imports
from typing import TYPE_CHECKING, Any

import carb
import carb.input
import msgpack
import numpy as np
import omni.ext
import omni.kit.app
import omni.kit.commands
import omni.kit.menu.utils
import omni.kit.ui
import omni.kit.viewport.utility
import omni.kit.window.property as property_window_ext
import omni.timeline
import omni.ui as ui
import omni.usd
from omni.kit.menu.utils import MenuItemDescription, MenuLayout
from omni.kit.property.usd import PrimPathWidget
from omni.kit.quicklayout import QuickLayout
from omni.kit.window.title import get_main_window_title

# Use standard USD for main thread updates to ensure compatibility with Hydra
from pxr import Gf, Sdf, Usd, UsdGeom, UsdShade, Vt

from . import agent_control, dem_tiles, geo_overlay, hud, scene_look, view_scale
from .bathymetry import BathymetryBridge

if TYPE_CHECKING:
    import warp as wp
    import whoimpg.biologger.subscriber.warp_logic as warp_logic
else:
    # Dummy placeholders for runtime (will be overwritten by dynamic import)
    wp = None
    warp_logic = None

DATA_PATH = Path(carb.tokens.get_tokens_interface().resolve("${whoimpg.biologger.subscriber}"))


def _find_repo_root() -> Path:
    """Locate the repo hosting this extension (biologger-sim via the source/extensions link),
    independent of the process CWD."""
    current_path = Path(__file__).resolve().parent
    # 1. Explicit Check: Are we in a _build folder? (Common in Kit apps)
    if "_build" in current_path.parts:
        idx = current_path.parts.index("_build")
        return Path(*current_path.parts[:idx])
    # 2. Marker Check: Walk up looking for repo configuration files
    for parent in [current_path, *list(current_path.parents)]:
        if (parent / "repo.toml").exists() or (parent / "environment.yml").exists():
            return parent
    return current_path


REPO_ROOT = _find_repo_root()
LOOK_SETTINGS = "/exts/whoimpg.biologger.subscriber/look"
# Trail position and ODBA averaged over this many record seconds (0: every sample)
TRAIL_SMOOTHING_SETTING = f"{LOOK_SETTINGS}/trailSmoothingS"
DEFAULT_TRAIL_SMOOTHING_S = 2.0

# Live playback. Samples arrive in batches (about 8 a second for a 16 Hz stream), so drawing
# the newest one makes the animal hold still for several frames and then jump. Live mode
# instead draws every animal from its sample history at a playhead this far behind the
# stream, so there is always a sample on each side to interpolate between.
LIVE_DELAY_S = 0.25
LIVE_RATE_WINDOW_S = 3.0  # arrivals used to fit stream time against wall time
LIVE_TAU_S = 1.0  # time constant of the correction toward the target lag
LIVE_SLEW = 0.1  # the correction never exceeds this fraction of the playback rate
LIVE_RESYNC_S = 2.0  # jump straight to the target when further off than this (stream time)

# Camera and input: the shared lhzn.vantagekit extension drives /World/PlayerCam
# (ViewerControls, built in _setup_biologger_subscriber). Free mode is Kit's native
# navigation; attaching (K, pad X) orbits the active animal. Orbit is the only attached
# view: a swordfish yaws and rolls through each tail stroke, so a chase camera that turns
# with its heading swings with every stroke, while orbit holds a fixed angle on the animal.
PLAYER_CAM = "/World/PlayerCam"
# Animal models face -Z in the frame of their orient:telemetry op (see _compute_orientation).
ANIMAL_BODY_FORWARD = (0.0, 0.0, -1.0)
# vantagekit's orbit hint offers chase on T / D-pad down; biologger has no chase view.
VIEW_HINT_DROP = "T / D-pad down: chase from here    "


def _biologger_bindings() -> list:
    """vantagekit's default bindings without view cycling (T is the seafloor detail
    texture here, and orbit is the only attached view)."""
    from vantagekit.core import DEFAULT_BINDINGS

    return [b for b in DEFAULT_BINDINGS if b.action != "view_next"]


def _biologger_rig() -> Any:
    """Rig tuning in metres (vantagekit converts to the stage's centimetres). The chase
    settings only place the Home / pad A vantage, behind and above the animal."""
    from vantagekit.kit import RigSettings

    return RigSettings(
        views=("orbit",),
        body_forward=ANIMAL_BODY_FORWARD,
        chase_back_m=15.0,
        chase_up_m=3.0,
        chase_look_up_m=0.0,
        orbit_range_m=30.0,
        orbit_min_m=1.0,
        orbit_max_m=5000.0,
        orbit_min_elevation_deg=-60.0,
    )


async def _load_layout(layout_file: str, keep_windows_open: bool = False) -> None:
    """Loads a provided layout file and ensures the viewport is set to FILL."""
    try:
        # few frames delay to avoid the conflict with the
        # layout of omni.kit.mainwindow
        for _ in range(3):
            await omni.kit.app.get_app().next_update_async()
        QuickLayout.load_file(layout_file, keep_windows_open)

        # HACK: Explicitly hide clutter windows on startup to clean up the UI
        # User requested hiding: Stage, Layer, Render Settings, Properties,
        # Content, Console
        await omni.kit.app.get_app().next_update_async()
        windows_to_hide = [
            "Main Toolbar",
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
        self._input = carb.input.acquire_input_interface()
        self._controls: Any = None  # vantagekit ViewerControls (camera and camera input)
        self._hud: hud.BiologgerHUD | None = None  # telemetry and controls (hud.py)
        self._syncing_follow_checkbox = False

        # Agent camera/capture routes on the omni.services HTTP server (see agent_control.py)
        self._agent_router = agent_control.register(self)

        self._last_timeline_ui_update = 0.0
        self._is_scrubbing = False  # Track valid scrubbing state
        self._is_catching_up = False  # Track "Catch-Up" fast-forward state

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
        self._settings.set("/app/viewport/grid/enabled", False)
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
        # ensure predictable lighting
        self._settings.set("/rtx/post/tonemap/autoExposure/enabled", True)
        self._settings.set("/persistent/rtx/post/tonemap/autoExposure/enabled", True)

        # Set a fixed exposure value to ensure it's not pitch black after
        # disabling auto. Lower values are brighter; 0.0 is a common neutral
        # starting point
        self._settings.set("/rtx/post/tonemap/exposure", 10.0)

        # Delayed force to ensure it sticks after the viewport is fully
        # initialized
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

            # Re-apply for 10 ticks to beat any competing extension or
            # viewport init
            for _ in range(10):
                await omni.kit.app.get_app().next_update_async()
                # Re-force keys
                self._settings.set("/rtx/scene/lightingMode", 0)
                self._settings.set("/rtx/sceneDb/grid/enabled", False)
                self._settings.set("/app/viewport/displayOptions", 0)
                self._settings.set("/rtx/post/tonemap/autoExposure/enabled", True)
                self._settings.set("/rtx/post/tonemap/exposure", 10.0)

                if set_lighting_action:
                    set_lighting_action.execute(0)  # 0 = Stage Lighting

            # --- Disable Selection Highlight (Keep Box + Gimbal) ---
            # We assume it starts ON, so we toggle it OFF once after the loop.
            try:
                import omni.kit.actions.core as action_core

                registry = action_core.get_action_registry()
                toggle_highlight_action = registry.get_action(
                    "omni.kit.viewport.actions", "toggle_selection_hilight_visibility"
                )
                if toggle_highlight_action:
                    toggle_highlight_action.execute()
                    carb.log_info(
                        "[whoimpg.biologger] Disabled Selection Highlight (Action Executed)"
                    )
            except Exception as e:
                carb.log_warn(f"[whoimpg.biologger] Failed to toggle selection highlight: {e}")

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
            "xiphias gladius": "Swordfish_Clear_Patched.glb",
            "rhincodon typus": "Whale_Shark_Clear_Patched.glb",
            "carcharodon carcharias": "great_white_shark.glb",
            # Fallback/Generic types
            "shark": "great_white_shark.glb",
            "swordfish": "Swordfish_Clear_Patched.glb",
            "whaleshark": "Whale_Shark_Clear_Patched.glb",
        }

        # Per-Asset Initial Rotation Configuration
        # (Pitch, Yaw, Roll)
        asset_rotations = {
            "Swordfish_Clear_Patched.glb": (0, 180, 0),
            "Whale_Shark_Clear_Patched.glb": (0, 180, 0),
            "great_white_shark.glb": (-90, 180, 0),
        }

        # Normalize species string to handle trailing spaces and casing from CSV
        normalized_species = species.lower().strip()
        print(f"[DEBUG] Raw species received: '{species}' type:{type(species)}")
        print(f"[DEBUG] Normalized species: '{normalized_species}'")

        asset_filename = species_map.get(normalized_species, "great_white_shark.glb")
        print(f"[DEBUG] Initial mapping: '{normalized_species}' -> {asset_filename}")

        # Double check: if exact scientific name failed, try a fuzzy match against keys
        if asset_filename == "great_white_shark.glb" and normalized_species not in species_map:
            print(
                f"[DEBUG] Exact match failed for '{normalized_species}', checking fuzzy mapping..."
            )
            for key in species_map:
                if key in normalized_species or normalized_species in key:
                    asset_filename = species_map[key]
                    print(
                        f"[DEBUG] Fuzzy match found! '{key}' in '{normalized_species}' "
                        f"-> {asset_filename}"
                    )
                    break

        print(
            f"[DEBUG] Final decision: Mapping species '{species}' -> '{normalized_species}' "
            f"to asset: {asset_filename}"
        )
        carb.log_info(
            f"[whoimpg.biologger] Mapping species '{species}' -> '{normalized_species}' "
            f"to asset: {asset_filename}"
        )

        # Resolve absolute path for USD
        # Check common locations
        import os

        # Repo root first so the lookup does not depend on where Kit was launched from
        possible_paths = [
            os.path.join(root, sub, asset_filename)
            for root in (str(REPO_ROOT), os.getcwd())
            for sub in (
                os.path.join("source", "assets"),
                "assets",
                os.path.join("omniverse", "assets"),
            )
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
        # transform schema, which helps avoid Fabric "evaluatedTranslations"
        # warnings.
        xformable = UsdGeom.Xformable(prim)
        xformable.ClearXformOpOrder()  # Clear any existing/referenced transforms

        # Add ops with telemetry BEFORE spawn for correct world-space heading
        # rotation.
        # Order: [Translate, Orient:telemetry, RotateXYZ:spawn, Scale]
        #
        # CRITICAL: USD applies ops as M = M_op0 * M_op1 * ... for vertex
        # transform. If spawn is op0 and telemetry is op1:
        # v_world = spawn * telemetry * v_local
        # This applies telemetry in LOCAL space (wrong: Y-rotation doesn't
        # affect Y-axis nose).
        #
        # Correct order: telemetry op0, spawn op1:
        # v_world = telemetry * spawn * v_local
        # This applies spawn first (moving nose from +Y to -Z), THEN telemetry
        # rotates around world Y axis, correctly affecting the -Z nose
        # direction.

        op_translate = xformable.AddTranslateOp()
        # Reserve slot for telemetry orient (will be set dynamically in
        # _update_animal_pose)
        op_orient_telemetry = xformable.AddOrientOp(UsdGeom.XformOp.PrecisionFloat, "telemetry")
        op_rotate = xformable.AddRotateXYZOp()
        op_scale = xformable.AddScaleOp()

        # Set values
        # Apply initial visual offset to prevent overlapping if all start at (0,0)
        visual_offset_x = float(eid) * 1.0
        op_translate.Set((visual_offset_x, 0, 0))
        op_orient_telemetry.Set(Gf.Quatf(1, 0, 0, 0))  # Identity until telemetry arrives
        # Lookup rotation or default to standard GLB conversion
        initial_rot = asset_rotations.get(asset_filename, (-90, 180, 0))
        op_rotate.Set(initial_rot)
        op_scale.Set((100, 100, 100))  # Scale: 100 (1m -> 100cm)

        # Add the reference
        references = prim.GetReferences()
        references.ClearReferences()
        references.AddReference(full_asset_path)

        # Select first animal by default
        if eid == 0 or self._active_eid == -1:
            omni.usd.get_context().get_selection().set_selected_prim_paths([prim_path], False)
            self._active_eid = eid

        carb.log_info(f"[whoimpg.biologger] Spawned {species} (sim_id={sim_id}) at {prim_path}")

        # Make the animal unpickable in the viewport (Look but don't touch)
        # Allows selection via Stage, but prevents accidental drags
        omni.usd.get_context().set_pickable(prim_path, False)
        carb.log_info(f"[whoimpg.biologger] Set {prim_path} to unpickable.")

        # Player Camera Setup
        # Create dedicated /World/PlayerCam if missing, but do NOT switch to it
        # automatically unless it is the very first selection or explicit
        # request logic requires it.
        # User refinement: "let animals spawn in without snapping to each new
        # animal"
        player_cam_path = self._setup_player_camera(stage)

        # Only switch camera/selection if this is the FIRST animal (eid 0) or
        # we have no active selection
        if eid == 0 or self._active_eid == -1:
            self._set_active_camera(player_cam_path)
            carb.log_info(
                f"[whoimpg.biologger] First Animal: Switched active camera to {player_cam_path}"
            )
        else:
            carb.log_info(
                f"[whoimpg.biologger] Spawned {species} (eid={eid}) - Mantaining current view."
            )

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

        # Multi-Entity State
        # Map: eid (int) -> state dict
        # { 'id': view_id, 'pos': Vec3f, 'rot': Quatf, 'path': prim_path, 'data': latest_message }
        self._entities_state: dict[int, dict] = {}
        self._active_eid = -1  # Currently selected/followed entity

        # Metadata Registry
        self._id_to_species: dict[str, str] = {}
        self._species_cache: dict[tuple[Any, Any], str] = {}  # (tag_id, sim_id) -> species
        self._load_metadata()

        # App keys (entity select, exaggeration, detail texture, windows); the camera's keys,
        # mouse and gamepad belong to vantagekit's InputRouter
        self._input_sub_id = None

        # Trail State
        # Refactored for Multi-Entity Segmented Trails
        self._entities_trail_buffers: dict[int, dict] = {}

        self._trail_prim_path = "/World/Trails"
        self._last_trail_update_ms = 0.0
        self._trail_segment_size = 5000
        self._curve_written: dict[str, int] = {}  # curve path -> digest of the last write
        # Live mode builds trails from the received history (every sample), not from the
        # poses shown on rendered frames; see _backfill_trail_gaps
        self._trail_from_history = False
        self._trail_width_cm = 5.0  # see set_trail_width
        # Out of follow mode the width tracks the camera's distance (view_scale), until a
        # width is set by hand; follow mode keeps the close-up width
        self._trail_width_auto = True
        self._trail_width_last_check = 0.0
        # Vertical exaggeration of the whole scene about sea level (see
        # set_vertical_exaggeration); trail buffers keep true positions
        self._vexag = 1.0
        # Seafloor detail texture (decoration, off by default; T toggles it): wanted state, and
        # the state last applied to the seabed material (None until the DEM material exists)
        self._seafloor_detail = bool(self._settings.get(f"{LOOK_SETTINGS}/seafloorDetail"))
        self._seafloor_detail_applied: bool | None = None

        # Temporal Replay State
        # Temporal Replay State
        self._replay_live_time: float = 0.0
        self._replay_playhead: float = 0.0
        self._replay_time: float | None = None  # scripted replay time; see set_replay_time
        self._frame_ms_max: dict[str, float] = {}  # slowest frame sections since last read
        # Per-frame trace for smoothness checks (/agent/trace): frames still to record, rows
        self._trace_left = 0
        self._trace_rows: list[tuple[float, ...]] = []
        # Live playhead (stream seconds) and its clock; see _advance_live_playhead
        self._live_playhead: float | None = None
        self._live_wall: float | None = None
        self._live_arrivals: collections.deque[tuple[float, float]] = collections.deque(maxlen=256)
        self._session_start_time: float = 0.0

        # History Buffer:
        # { eid: { 'times': [], 'pos': [], 'rot': [] } }
        self._entity_history: dict[int, dict] = {}
        self._live_sync_active = True

        # Georeference and uncertainty from the simulator's <topic>/meta messages.
        # Written by the listener thread, consumed on the main thread in _update_geo_layers.
        self._entity_meta: dict[int, dict] = {}
        self._geo_origin: tuple[float, float] | None = None
        self._dem_streamer: dem_tiles.DemTileStreamer | dem_tiles.DemGridSource | None = None
        self._geo_last_update = 0.0
        self._dem_last_focus_update = 0.0
        self._look_applied = False  # with the deployment's sun (after the georeference)
        self._look_neutral_applied = False  # with the neutral sun, from startup

        def on_surface_crossing(under: bool) -> None:
            stage = omni.usd.get_context().get_stage()
            if stage is not None:
                scene_look.set_water_reflection(stage, on=not under)

        def on_deep_water(deep: bool) -> None:
            stage = omni.usd.get_context().get_stage()
            water = stage.GetPrimAtPath(scene_look.WATER_PRIM) if stage is not None else None
            if water and water.IsValid():
                if deep:
                    UsdGeom.Imageable(water).MakeInvisible()
                else:
                    UsdGeom.Imageable(water).MakeVisible()

        self._underwater_fog = scene_look.UnderwaterFog(
            self._settings,
            self._settings.get_as_float(f"{LOOK_SETTINGS}/underwaterVisibilityM")
            or scene_look.DEFAULT_VISIBILITY_M,
            on_change=on_surface_crossing,
            on_deep=on_deep_water,
        )

        # Omni Timeline Integration
        self._timeline = omni.timeline.get_timeline_interface()
        self._timeline_sub = self._timeline.get_timeline_event_stream().create_subscription_to_pop(
            self._on_timeline_event
        )
        # Ensure scrubbing initializes correctly
        self._is_scrubbing = False

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
        # --/biologger/backend=warp (default)
        self._backend = self._settings.get("/biologger/backend") or "warp"
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
            repo_root = REPO_ROOT
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

        # Camera and camera input (vantagekit): free mode is Kit's native navigation;
        # the attached view orbits the active animal
        self._setup_viewer_controls()

        # Render each frame from the poses this update wrote. With async rendering (the app's
        # default) the update loop runs ahead of the renderer and each picture takes whatever
        # poses were written last, at uneven moments, so a followed animal steps however
        # smooth the poses are; off, the update rate is the rendered rate.
        self._settings.set_bool("/app/asyncRendering", False)
        carb.log_info("[whoimpg.biologger] /app/asyncRendering set to false")

        # App keys only (see _on_input_event); order 0 like vantagekit's router
        if not self._input_sub_id:
            try:
                self._input_sub_id = self._input.subscribe_to_input_events(self._on_input_event)
            except Exception as e:
                carb.log_error(f"[whoimpg] Failed to subscribe to input: {e}")

        # 1. The HUD (hud.py): telemetry and controls in one column over the viewport. The
        # controls' state lives here (hud.Control), so the column can rebuild at any time.
        def check(value: bool) -> hud.Control:
            return hud.Control(ui.SimpleBoolModel(bool(value)))

        self._follow_mode_checkbox = check(self._follow_mode_enabled)
        self._follow_mode_checkbox.model.add_value_changed_fn(self._on_follow_mode_changed)
        self._trail_checkbox = check(True)
        self._trail_checkbox.model.add_value_changed_fn(self._on_trail_mode_changed)
        self._trail_auto_checkbox = check(self._trail_width_auto)
        self._trail_auto_checkbox.model.add_value_changed_fn(
            lambda m: self.set_trail_width_auto(m.get_value_as_bool())
        )
        self._detail_checkbox = check(self._seafloor_detail)
        self._detail_checkbox.model.add_value_changed_fn(
            lambda m: self.set_seafloor_detail(m.get_value_as_bool())
        )
        # Bathymetry is a startup setting (no box): it only acts when the stage is set up
        self._bathymetry_checkbox = check(
            self._settings.get("/exts/whoimpg.biologger.subscriber/enableBathymetry")
        )
        self._dem_stream_checkbox = check(
            self._settings.get("/exts/whoimpg.biologger.subscriber/demStreaming") is not False
        )
        self._uncertainty_checkbox = check(True)
        self._debug_vec_checkbox = check(False)
        self._safe_mode_checkbox = hud.Control(
            ui.SimpleBoolModel(self._safe_mode), enabled=not self._safe_mode
        )
        self._safe_mode_checkbox.model.add_value_changed_fn(self._on_safe_mode_changed)
        self._offset_roll_slider = hud.Control(ui.SimpleFloatModel(0.0))
        self._offset_pitch_slider = hud.Control(ui.SimpleFloatModel(0.0))
        self._offset_heading_slider = hud.Control(ui.SimpleFloatModel(0.0))
        for slider in (
            self._offset_roll_slider,
            self._offset_pitch_slider,
            self._offset_heading_slider,
        ):
            slider.model.add_value_changed_fn(self._on_align_changed)
        self._host_field = hud.Control(ui.SimpleStringModel("127.0.0.1"))
        self._port_field = hud.Control(ui.SimpleIntModel(5555))

        self._hud = hud.BiologgerHUD(self)
        self._mode_toggle_btn = self._hud.mode_button
        self._hud.set("exag", f"Exaggeration {self._vexag:g}x  (V)")
        self._chrome_task = asyncio.ensure_future(self._hide_viewport_chrome())

        # 2. Fabric setup for the animal prim (e.g., /World/Shark)
        self._stage = None

        # 3. Auto-connect on startup
        self._start_listener()
        self._is_running = True

        # 4. Per-frame update on the main thread (Events 2.0 through vantagekit, with a
        # fallback to the legacy update stream); _on_update_ui receives dt in seconds
        from vantagekit.kit import on_update

        self._update_sub = on_update(self._on_update_ui, "whoimpg.biologger.update")

    def _cycle_active_animal(self, direction: int, index: int | None = None) -> None:
        """
        Cycle through active entities.
        If index is provided, select that index directly.
        Else use direction +1 or -1.
        """
        eids = sorted(self._entities_state.keys())
        if not eids:
            return

        # Current Index
        curr_idx = 0
        with contextlib.suppress(ValueError):
            curr_idx = eids.index(self._active_eid)

        # Calculate New Index
        if index is not None:
            new_idx = max(0, min(len(eids) - 1, index))
        else:
            new_idx = (curr_idx + direction) % len(eids)

        new_eid = eids[new_idx]
        if self._controls is not None:
            # The camera follows the selection; _on_camera_target sets the active animal
            self._controls.select(new_eid)
        else:
            self._on_camera_target(new_eid)

    def _on_camera_target(self, eid: Any) -> None:
        """vantagekit's target changed (cycling keys or _cycle_active_animal): make it the
        active animal and select its prim."""
        if eid is None or eid not in self._entities_state:
            return
        self._active_eid = eid
        state = self._entities_state[eid]
        carb.log_info(f"[whoimpg] Active animal EID {eid}: {state.get('sp', 'Unknown')}")
        path = state.get("path")
        if path and path != "PENDING":
            omni.usd.get_context().get_selection().set_selected_prim_paths([path], False)

    # Camera (vantagekit) -----------------------------------------------------------------

    @property
    def _follow_mode_enabled(self) -> bool:
        """True while the camera is attached to an animal (orbit)."""
        return self._controls is not None and self._controls.rig.attached

    def _animal_ids(self) -> list:
        """Camera targets: animals whose prim has been created, in eid order."""
        return [
            eid
            for eid, s in sorted(self._entities_state.items())
            if s.get("path") and s.get("path") != "PENDING"
        ]

    def _animal_pose(self, eid: Any) -> Any:
        """World position (exaggerated, as drawn) and the telemetry orientation of an animal.

        The orientation comes from the orient:telemetry op (composed with the parent's world
        rotation), not the prim's full matrix, which also holds the per-asset spawn rotation
        and the x100 scale; in that frame the model faces -Z (ANIMAL_BODY_FORWARD)."""
        from vantagekit.core import Pose

        state = self._entities_state.get(eid)
        path = state.get("path") if state else None
        if not path or path == "PENDING":
            return None
        stage = omni.usd.get_context().get_stage()
        prim = stage.GetPrimAtPath(path) if stage else None
        if not prim or not prim.IsValid():
            return None
        xf = UsdGeom.Xformable(prim)
        t = xf.ComputeLocalToWorldTransform(Usd.TimeCode.Default()).ExtractTranslation()
        q = Gf.Quatd(1.0)
        for op in xf.GetOrderedXformOps():
            if op.GetOpType() == UsdGeom.XformOp.TypeOrient and "telemetry" in op.GetOpName():
                v = op.Get()
                if v is not None:
                    q = Gf.Quatd(v)
                break
        parent = prim.GetParent()
        if parent and parent.IsValid() and not parent.IsPseudoRoot():
            pw = UsdGeom.Xformable(parent).ComputeLocalToWorldTransform(Usd.TimeCode.Default())
            q = Gf.Matrix4d(pw).RemoveScaleShear().ExtractRotationQuat() * q
        q.Normalize()
        i = q.GetImaginary()
        return Pose((t[0], t[1], t[2]), (q.GetReal(), i[0], i[1], i[2]))

    def _setup_viewer_controls(self) -> None:
        """Build the vantagekit camera controls on /World/PlayerCam (see module notes)."""
        try:
            from vantagekit.core import CallbackTargets
            from vantagekit.kit import ViewerControls
        except ImportError as e:
            carb.log_error(f"[whoimpg.biologger] lhzn.vantagekit not loaded; no camera: {e}")
            return
        self._controls = ViewerControls(
            PLAYER_CAM,
            CallbackTargets(ids=self._animal_ids, pose=self._animal_pose),
            bindings=_biologger_bindings(),
            settings=_biologger_rig(),
            free_gamepad=True,
            name="whoimpg.biologger",
            overlay=False,
        )
        self._controls.on_target_change(self._on_camera_target)
        self._controls.on_mode_change(self._on_camera_mode)
        # Any stage opening (default scene, custom stage, scene reset): back to free mode and
        # re-read the stage's up axis and units (Y up; metersPerUnit falls back to 0.01)
        from vantagekit.kit import on_stage_opened

        self._camera_stage_sub = on_stage_opened(
            lambda: self._controls.on_stage_opened() if self._controls is not None else None,
            "whoimpg.biologger.camera.stage",
        )

    def _on_camera_mode(self, mode: str) -> None:
        """Keep the HUD's follow checkbox in step with the camera mode."""
        cb = getattr(self, "_follow_mode_checkbox", None)
        if cb is None:
            return
        self._syncing_follow_checkbox = True
        try:
            cb.model.set_value(mode != "free")
        finally:
            self._syncing_follow_checkbox = False

    def set_follow(self, enabled: bool) -> bool:
        """Attach the camera to the active animal (its last attached view) or free it."""
        if self._controls is None:
            return False
        c = self._controls
        if enabled and not c.rig.attached:
            if self._active_eid in self._animal_ids():
                c.targets.selected = self._active_eid
            c.set_mode(c.rig.view)
        elif not enabled and c.rig.attached:
            c.set_mode("free")
        return bool(c.rig.attached)

    def _update_camera(self, dt: float) -> None:
        """One camera step per frame; also draws the view badge in the HUD."""
        c = self._controls
        if c is None:
            return
        # Follow selections made elsewhere (spawn, listener auto-select, 1-5 keys)
        if c.targets.selected != self._active_eid and self._active_eid in self._animal_ids():
            c.targets.selected = self._active_eid
        try:
            c.update(dt)
        except Exception as e:
            carb.log_warn(f"[whoimpg.biologger] Camera update failed: {e}")
        if self._hud is not None:
            mode, title, hint = c.view_badge()
            self._hud.update_view(mode, title, hint.replace(VIEW_HINT_DROP, ""))

    def _update_telemetry_window(self) -> None:
        """Computes the HUD readouts for the active animal and hands them to the HUD."""
        if self._hud is None:
            return

        sim_id = "None"
        state = {}
        if self._active_eid != -1:
            state = self._entities_state.get(self._active_eid, {})
            sim_id = state.get("id", "Unknown")

        # Time of the pose drawn: the live playhead, or the replay head
        if self._live_sync_active and not self._is_catching_up:
            shown_ts = self._live_playhead or self._latest_timestamp
        elif self._session_start_time > 0:
            shown_ts = self._session_start_time + self._replay_head()
        else:
            shown_ts = self._latest_timestamp
        if shown_ts > 0:
            dt = datetime.datetime.fromtimestamp(shown_ts, tz=datetime.timezone.utc)
            time_str = dt.strftime("%Y-%m-%d %H:%M:%S UTC")
        else:
            time_str = "--"
        # Record time since the release (the start fix); without a georeference, since the
        # first sample this viewer received, which is later when it joined a running stream.
        fixes = (self._entity_meta.get(self._active_eid) or {}).get("fixes") or []
        since_fix = bool(fixes and fixes[0].get("t"))
        t_ref = float(fixes[0]["t"]) if since_fix else self._session_start_time
        elapsed_s = shown_ts - t_ref if shown_ts > 0 and t_ref > 0 else None

        # Physics / Telemetry
        phys = self._latest_physics_data or {}

        # Attack Angle & Sideslip Calculation
        alpha_val = 0.0
        beta_val = 0.0
        est_3d_vel = 0.0  # speed along the trail, gates the attack angle below

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

                        est_3d_vel = math.sqrt(dx * dx + dy * dy + dz * dz) / delta_time

        # Attack Angle & Sideslip Calculation
        path_str = "Path pitch --   heading --"
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
                                path_str = (
                                    f"Path pitch {path_pitch:+.1f}°   "
                                    f"heading {path_heading % 360:.0f}°"
                                )

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

        # Seafloor under the animal from the fused DEM grid (scene x is east, z is south)
        seafloor_val: float | None = None
        if self._dem_streamer is not None and pos_val != [0.0, 0.0, 0.0]:
            seafloor_val = self._dem_streamer.depth_at(-pos_val[2], pos_val[0])

        # Latitude and longitude of the drawn position, from the georeference origin
        latlon: tuple[float, float] | None = None
        if self._geo_origin is not None and pos_val != [0.0, 0.0, 0.0]:
            latlon = dem_tiles.ne_to_latlon(-pos_val[2], pos_val[0], self._geo_origin)

        self._update_hud_labels(
            animal_name=str(sim_id) if self._active_eid != -1 else "--",
            time_str=time_str,
            elapsed_s=elapsed_s,
            elapsed_from="release" if since_fix else "first sample",
            latlon=latlon,
            roll=roll_val,
            pitch=pitch_val,
            heading=heading_val,
            alpha=alpha_val,
            beta=beta_val,
            path_info=path_str,
            depth=float(depth_val),
            speed=sim_3d_vel,
            h_speed=sim_h_vel,
            v_speed=sim_v_vel,
            odba=float(odba_val),
            vedba=float(vedba_val),
            seafloor=seafloor_val,
        )

    def _update_hud_labels(
        self,
        animal_name: str,
        time_str: str,
        elapsed_s: float | None,
        elapsed_from: str,
        latlon: tuple[float, float] | None,
        roll: float,
        pitch: float,
        heading: float,
        alpha: float,
        beta: float,
        path_info: str,
        depth: float,
        speed: float,
        h_speed: float,
        v_speed: float,
        odba: float,
        vedba: float,
        seafloor: float | None,
    ) -> None:
        """Writes the HUD readouts (hud.py); the HUD caches them across rebuilds."""
        h = self._hud
        if h is None:
            return
        debug = self._debug_vec_checkbox.model.get_value_as_bool()
        # With the debug vectors on, the lines match their colours (orientation red, path green)
        orient_style = {**hud.TEXT, "color": 0xFF6666FF} if debug else hud.TEXT
        path_style = {**hud.DIM, "color": 0xFF66FF66} if debug else hud.DIM

        h.set("animal", f"Animal: {animal_name}")
        # Large: time since the release; below it, the record date and time (UTC)
        if elapsed_s is not None and elapsed_s >= 0:
            hours, rem = divmod(int(elapsed_s), 3600)
            h.set("clock", f"T+ {hours}:{rem // 60:02d}:{rem % 60:02d}")
            h.set("date", f"since {elapsed_from}   {time_str}")
        else:
            h.set("clock", "T+ --:--:--")
            h.set("date", time_str)
        if latlon is None:
            h.set("position", "Position --   (no georeference)")
        else:
            lat, lon = latlon
            h.set(
                "position",
                f"{abs(lat):.4f}° {'N' if lat >= 0 else 'S'}   "
                f"{abs(lon):.4f}° {'E' if lon >= 0 else 'W'}",
            )
        # Deeper than the seafloor under it means the placed position is wrong
        if seafloor is None:
            h.set("depth", f"Depth {depth:.1f} m   Seafloor --", hud.TEXT)
            clear = ""
        elif depth > seafloor:
            h.set(
                "depth",
                f"Depth {depth:.1f} m   Seafloor {seafloor:.0f} m   {depth - seafloor:.0f} m BELOW",
                hud.WARN,
            )
            clear = f"   {depth - seafloor:.0f} m below the floor"
        else:
            h.set(
                "depth",
                f"Depth {depth:.1f} m   Seafloor {seafloor:.0f} m   {seafloor - depth:.0f} m clear",
                hud.TEXT,
            )
            clear = f"   {seafloor - depth:.0f} m clear"
        h.set("speed", f"Speed {speed:.2f} m/s   (horiz. {h_speed:.2f}, vert. {v_speed:+.2f})")
        h.set(
            "attitude",
            f"Roll {roll:+.1f}°   Pitch {pitch:+.1f}°   Heading {heading % 360:.0f}°",
            orient_style,
        )
        h.set("effort", f"ODBA {odba:.2f}   VeDBA {vedba:.2f}")
        h.set("path", path_info, path_style)
        h.set("aoa", f"Attack angle {alpha:+.1f}°   Sideslip {beta:+.1f}°")
        mode = "REPLAY" if not self._live_sync_active or self._is_catching_up else "LIVE"
        h.set("stream", f"{self._connection_status}   {self._throughput_str}   {mode}")
        h.set("summary", f"{time_str[11:19] or '--'}   Depth {depth:.0f} m{clear}")

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

            # Gf composes left to right (row vectors: a * b applies a, then b), so roll and
            # pitch act in the body frame and yaw is applied last, about world up. Yaw first
            # would pitch about world X, which turns pitch into roll on east or west headings
            # (RED001 diving at heading 70 degrees, pitch -32, was drawn nose-up).
            rot = rot_roll * rot_pitch * rot_yaw
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
            quat_data = state.get("quat")  # Direct Quaternion support (History/Warp)
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

            if quat_data:
                # Direct Quaternion application (from History or Warp)
                # Expects list/tuple [w, x, y, z] or Gf.Quatf
                if isinstance(quat_data, list | tuple):
                    target_rot_quat = Gf.Quatf(
                        float(quat_data[0]),
                        float(quat_data[1]),
                        float(quat_data[2]),
                        float(quat_data[3]),
                    )
                else:
                    target_rot_quat = quat_data
            elif rot_data:
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
                translate_op.Set(self._exaggerated(target_pos))

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
                    # Safely access last element
                    try:
                        last_ts = trail_state["buffer"][-1][0]
                        if ts <= last_ts:
                            should_append = False
                    except IndexError:
                        pass  # Buffer might be empty or malformed logic

                if should_append and not self._trail_from_history:
                    trail_state["buffer"].append((ts, Gf.Vec3f(target_pos), target_rot_quat, odba))

                # Segment Baking (Infinite Trail Logic)
                if len(trail_state["buffer"]) >= self._trail_segment_size:
                    self._bake_trail_segment(stage, eid, trail_state)

        except Exception as e:
            if not hasattr(self, "_pose_error_shown"):
                carb.log_error(f"[whoimpg.biologger] Error updating pose: {e}")
                self._pose_error_shown = True

    def _update_prim_batched_warp(self, stage: Usd.Stage) -> None:
        """
        Batched update using NVIDIA Warp for coordinate transformation (NED -> USD).
        Gather -> Compute (GPU) -> Scatter (USD)
        """
        try:
            # 1. Gather valid entities
            valid_eids = []
            inputs_pos = []
            inputs_quat = []

            # Helper to map state to input arrays
            # We need to preserve the order to map back to entities

            # Temporary storage for pre-computation data (scales, etc) if needed
            # For now, we assume standard NED inputs and let Warp handle the transform.

            for eid, state in self._entities_state.items():
                if not state.get("path") or state.get("path") == "PENDING":
                    # Handle spawning logic (same as CPU loop)
                    if not state.get("path"):
                        species = state.get("sp", "shark")
                        sim_id_str = state.get("id", "unknown")
                        task = asyncio.ensure_future(
                            self._load_animal_asset(species, eid, sim_id_str)
                        )
                        state["path"] = "PENDING"

                        def _on_spawn_done(t: asyncio.Task, eid: int = eid) -> None:
                            try:
                                res = t.result()
                                self._entities_state[eid]["path"] = res
                            except Exception as e:
                                carb.log_error(f"Error spawning eid {eid}: {e}")

                        task.add_done_callback(_on_spawn_done)
                    continue

                phys = state.get("phys", {})
                rot_data = state.get("rot_data")

                if phys:
                    raw_d = phys.get("d")
                    raw_px = phys.get("px")
                    raw_py = phys.get("py")

                    import math

                    if (
                        raw_d is not None
                        and not math.isnan(float(raw_d))
                        and raw_px is not None
                        and not math.isnan(float(raw_px))
                        and raw_py is not None
                        and not math.isnan(float(raw_py))
                    ):
                        # NED Input: x=North(px), y=East(py), z=Down(depth)
                        # Note: we pass raw values.
                        # Warp Kernel expects: vec3(x, y, z)
                        # But wait, our 'px' is usually 'pseudo_x' (m) and 'py' is 'pseudo_y'.
                        # The "NED" convention in streaming.py varies, but typically:
                        # Px, Py are 2D local. Depth is Z.
                        inputs_pos.append((float(raw_px), float(raw_py), float(raw_d)))
                    else:
                        inputs_pos.append((0.0, 0.0, 0.0))  # Placeholder/Invalid
                else:
                    inputs_pos.append((0.0, 0.0, 0.0))

                valid_eids.append(eid)

                # Setup Rotation inputs (Placeholder for now, keeping CPU orientation
                # logic or simplified)
                # Warp kernel expects vec4 quat.
                # If we have rot_data, we can pass it.
                if rot_data and len(rot_data) == 4:
                    inputs_quat.append(tuple(rot_data))
                elif rot_data and len(rot_data) == 3:
                    # Euler (r,p,h) -> we might need to convert or pass as vec3 and handle in kernel
                    # For now, append 0,0,0,1 Identity
                    inputs_quat.append((0.0, 0.0, 0.0, 1.0))
                else:
                    inputs_quat.append((0.0, 0.0, 0.0, 1.0))

            if not valid_eids:
                return

            n = len(valid_eids)

            # 2. Warp Compute
            # Create Arrays
            wp_inputs_pos: Any = wp.array(inputs_pos, dtype=wp.vec3, device="cuda")
            wp_inputs_quat: Any = wp.array(inputs_quat, dtype=wp.vec4, device="cuda")

            wp_outputs_pos = wp.zeros(n, dtype=wp.vec3, device="cuda")
            wp_outputs_quat = wp.zeros(n, dtype=wp.vec4, device="cuda")
            wp_slip = wp.zeros(n, dtype=float, device="cuda")

            # Launch Kernel
            wp.launch(
                kernel=warp_logic.transform_ned_to_usd_kernel,
                dim=n,
                inputs=[wp_inputs_pos, wp_inputs_quat, wp_outputs_pos, wp_outputs_quat, wp_slip],
                device="cuda",
            )

            # Sync/Copy Back
            out_pos = wp_outputs_pos.numpy()
            # out_quat = wp_outputs_quat.numpy()

            # 3. Apply changes to USD (Scatter)
            for i, eid in enumerate(valid_eids):
                state = self._entities_state[eid]
                prim_path = state.get("path")
                if not prim_path:
                    continue

                prim = stage.GetPrimAtPath(prim_path)
                if not prim.IsValid():
                    continue

                # Position from Warp (Already transformed to USD Y-Up, need scaling?)
                # Warp kernel: Y_usd = -Z_ned (-depth), X_usd = Y_ned (py), Z_usd = -X_ned (px)
                # We need to multiply by 100.0 (cm/m conversion).
                # I will scale here: p * 100.0

                p = out_pos[i]
                target_pos = Gf.Vec3d(float(p[0]) * 100.0, float(p[1]) * 100.0, float(p[2]) * 100.0)

                # Orientation: For now, re-use CPU logic for complex offsets
                # until we port the offset logic to Warp.
                # This hybrid approach ensures correctness while offloading the bulk
                # position transform.
                rot_data = state.get("rot_data")
                target_rot_quat = None
                if rot_data:
                    target_rot_quat = self._compute_orientation(rot_data, is_euler=True)

                # Apply Position
                xformable = UsdGeom.Xformable(prim)
                translate_op = None
                for op in xformable.GetOrderedXformOps():
                    if op.GetOpType() == UsdGeom.XformOp.TypeTranslate:
                        translate_op = op
                        break
                if not translate_op:
                    translate_op = xformable.AddTranslateOp()
                translate_op.Set(self._exaggerated(target_pos))

                # Apply Rotation
                if target_rot_quat:
                    rotate_op_name = "xformOp:orient:telemetry"
                    rotate_op = None
                    for op in xformable.GetOrderedXformOps():
                        if op.GetOpName() == rotate_op_name:
                            rotate_op = op
                            break
                    if rotate_op:
                        rotate_op.Set(target_rot_quat)

                # Trail Logic (Keep CPU side logic for buffer management for now)
                trail_state = self._entities_trail_buffers.setdefault(
                    eid, {"buffer": [], "hue": (eid * 137) % 360.0, "segment_count": 0}
                )
                if target_pos and target_rot_quat:
                    ts = float(state.get("ts", 0.0))
                    phys = state.get("phys", {})
                    odba = float(phys.get("odba", 0.0)) if phys else 0.0

                    should_append = True
                    if trail_state["buffer"]:
                        last_ts = trail_state["buffer"][-1][0]
                        if ts <= last_ts:
                            should_append = False
                    if should_append and not self._trail_from_history:
                        trail_state["buffer"].append(
                            (ts, Gf.Vec3f(target_pos), target_rot_quat, odba)
                        )
                    if len(trail_state["buffer"]) >= self._trail_segment_size:
                        self._bake_trail_segment(stage, eid, trail_state)

        except Exception as e:
            if not hasattr(self, "_warp_update_error_shown"):
                carb.log_error(f"[whoimpg.biologger] Error in Batched Warp Update: {e}")
                import traceback

                traceback.print_exc()
                self._warp_update_error_shown = True

    def _on_timeline_event(self, event: carb.events.IEvent) -> None:
        """Handle Timeline events (Play/Pause/Scrub)."""
        if event.type in (
            int(omni.timeline.TimelineEventType.CURRENT_TIME_CHANGED),
            int(omni.timeline.TimelineEventType.PLAY),
        ):
            self._replay_time = None  # the timeline is being used again
        if event.type == int(omni.timeline.TimelineEventType.CURRENT_TIME_CHANGED):
            # Detect manual scrubbing:
            if not self._timeline.is_playing() and self._live_sync_active:
                # Valid scrub. Disable Live Sync strictly.
                self._switch_to_timeline_mode()
                carb.log_info("[whoimpg] Scrub detected - Switched to TIMELINE MODE.")

        elif event.type == int(omni.timeline.TimelineEventType.PLAY):
            # User hits play -> History Playback
            # If we were catching up, this is valid.
            # If we were live sync, this breaks it? No, live sync stops timeline.
            # If user manually hits play while live sync is active,
            # we should fallback to timeline mode
            if self._live_sync_active and not self._is_catching_up:
                self._switch_to_timeline_mode()
                carb.log_info("[whoimpg] Play pressed - Switched to TIMELINE MODE.")

        elif event.type == int(omni.timeline.TimelineEventType.PAUSE):
            # User hits Pause -> Timeline Mode
            # If catching up, this aborts catch-up
            if self._is_catching_up:
                self._is_catching_up = False
                self._live_sync_active = False  # Manual abort
                self._mode_toggle_btn.text = "MODE: TIMELINE"
                self._mode_toggle_btn.style = {"background_color": 0xFF805000}
                carb.log_info("[whoimpg] Pause pressed - Aborted Catch-Up.")

            elif self._live_sync_active:
                self._switch_to_timeline_mode()
                carb.log_info("[whoimpg] Pause pressed - Switched to TIMELINE MODE.")

    def _history_pose(self, eid: int, query_time: float) -> dict | None:
        """An animal's pose at query_time (stream seconds) from its sample history: position
        interpolated linearly, orientation by quaternion slerp (blending Euler angles goes
        wrong across the 0/360 heading wrap). Before the first or after the last sample it
        holds that sample. Returns a payload for _update_animal_pose (phys, quat), or None
        without history."""
        hist = self._entity_history.get(eid)
        if not hist or not hist["times"]:
            return None
        times = hist["times"]
        n = min(len(times), len(hist["pos"]), len(hist["rot"]))  # the listener may be mid-append
        if n == 0:
            return None
        idx = bisect_left(times, query_time, 0, n)
        if idx == 0 or idx >= n:
            k = 0 if idx == 0 else n - 1
            p = hist["pos"][k]
            q = self._compute_orientation(list(hist["rot"][k]), is_euler=True)
            return {"phys": {"d": p[2], "px": p[0], "py": p[1]}, "quat": q}
        t1, t2 = times[idx - 1], times[idx]
        a = 0.0 if t2 <= t1 else (query_time - t1) / (t2 - t1)
        p1, p2 = hist["pos"][idx - 1], hist["pos"][idx]
        p = tuple(p1[i] + a * (p2[i] - p1[i]) for i in range(3))
        q1 = self._compute_orientation(list(hist["rot"][idx - 1]), is_euler=True)
        q2 = self._compute_orientation(list(hist["rot"][idx]), is_euler=True)
        q = Gf.Slerp(a, q1, q2)
        return {"phys": {"d": p[2], "px": p[0], "py": p[1]}, "quat": q}

    def _spawn_animal(self, eid: int, state: dict) -> None:
        """Starts loading an entity's animal asset; its path is PENDING until it lands."""
        task = asyncio.ensure_future(
            self._load_animal_asset(state.get("sp", "shark"), eid, state.get("id", "unknown"))
        )
        state["path"] = "PENDING"

        def _on_spawn_done(t: asyncio.Task) -> None:
            try:
                self._entities_state[eid]["path"] = t.result()
            except Exception as e:
                carb.log_error(f"Error spawning eid {eid}: {e}")

        task.add_done_callback(_on_spawn_done)

    def _advance_live_playhead(self) -> float:
        """Stream time to draw this frame in live mode: LIVE_DELAY_S behind the stream.

        The stream's rate against the wall clock is fitted over the last LIVE_RATE_WINDOW_S
        of arrivals (the simulator need not run at 1x), the playhead advances at that rate,
        and a low-passed, slew-capped correction holds it at the target lag; it jumps only
        when more than LIVE_RESYNC_S off (start, seek, stall)."""
        now = time.perf_counter()
        latest = float(self._latest_timestamp)
        arr = self._live_arrivals
        if arr and latest < arr[-1][1]:
            # Stream time went back (a new run): the old run's arrivals would fit a
            # negative rate, clamped to 0, and hold the playhead until they aged out.
            arr.clear()
        if not arr or latest != arr[-1][1]:
            arr.append((now, latest))
        while arr and now - arr[0][0] > LIVE_RATE_WINDOW_S:
            arr.popleft()
        rate, base = 1.0, latest
        if len(arr) >= 4 and arr[-1][0] - arr[0][0] > 0.5:
            w = np.array([a[0] for a in arr]) - now
            s = np.array([a[1] for a in arr])
            rate, base = (float(v) for v in np.polyfit(w, s, 1))  # stream time at w = 0
            rate = max(rate, 0.0)
        target = base - LIVE_DELAY_S
        last, ph = self._live_wall, self._live_playhead
        self._live_wall = now
        if ph is None or last is None or abs(target - ph) > LIVE_RESYNC_S * max(rate, 1.0):
            # The fit extrapolates to now, past the last arrival when the stream stalls.
            self._live_playhead = min(target, latest)
            return self._live_playhead
        step = rate * (now - last)
        err = target - (ph + step)
        cap = LIVE_SLEW * step
        corr = max(-cap, min(cap, err * (now - last) / LIVE_TAU_S))
        # Never past the newest sample: when the stream pauses or stops, the fitted rate
        # decays to the 1x fallback and the playhead would run on until the resync threw
        # it back LIVE_RESYNC_S (the animal jerking back every couple of seconds).
        self._live_playhead = min(ph + step + corr, latest)
        return self._live_playhead

    def _backfill_trail_gaps(
        self, stage: Usd.Stage, start_time: float | None, end_time: float
    ) -> None:
        """
        Appends received history samples to the trail buffers, so the trail holds every sample
        rather than only the poses shown on rendered frames. Used during Catch-Up and, with
        ``start_time`` None (from each trail's last sample), every live frame: a slow or
        stalled frame at a fast replay would otherwise draw a straight chord across the
        skipped stretch of track.
        """
        import bisect

        for eid, hist in self._entity_history.items():
            times = hist["times"]
            if not times:
                continue

            # Get Trail Buffer
            trail_state = self._entities_trail_buffers.setdefault(
                eid, {"buffer": [], "hue": (eid * 137) % 360.0, "segment_count": 0}
            )
            buffer = trail_state["buffer"]

            # The listener thread appends each sample's fields one list at a time; read only
            # samples whose fields have all arrived
            complete = min(len(times), len(hist["pos"]), len(hist["rot"]), len(hist["odba"]))
            start = start_time
            if start is None:
                start = buffer[-1][0] if buffer else float("-inf")
            # Find first index > start, and last index <= end_time
            idx_start = bisect.bisect_right(times, start, 0, complete)
            idx_end = bisect.bisect_right(times, end_time, 0, complete)

            if idx_start >= idx_end:
                continue

            # Iterate and Transform
            for i in range(idx_start, idx_end):
                ts = times[i]
                # Avoid dupes
                if buffer and ts <= buffer[-1][0]:
                    continue

                # Retrieve Raw Data
                try:
                    p = hist["pos"][i]
                    r = hist["rot"][i]
                    # Phys
                    depth = float(p[2])
                    px = float(p[0])
                    py = float(p[1])

                    # Transform Function (NED -> USD Y-Up)
                    # Legacy: Y=-depth, X=py, Z=-px. Scaled by 100.
                    target_pos = Gf.Vec3f(py * 100.0, -depth * 100.0, -px * 100.0)

                    # Rotation
                    target_rot_quat = self._compute_orientation(r, is_euler=True)

                    buffer.append((ts, target_pos, target_rot_quat, float(hist["odba"][i])))

                except (IndexError, TypeError):
                    continue

                # Bake each full segment as it fills: a fast replay can deliver most of a
                # record between two frames, and one oversized segment then re-renders in
                # seconds whenever it changes (a replay's trail clipping changes it every frame)
                if len(buffer) >= self._trail_segment_size:
                    self._bake_trail_segment(stage, eid, trail_state)
                    buffer = trail_state["buffer"]

    def _update_prim(self, stage_event: Any) -> None:
        """Main update loop triggered every frame."""
        try:
            stage = omni.usd.get_context().get_stage()
            if not stage:
                return

            # Determine Mode: Live or Replay based on internal flag

            # --- CATCH UP LOGIC ---
            if self._is_catching_up:
                # Check Convergence
                current_time = self._session_start_time + self._timeline.get_current_time()
                lag = self._latest_timestamp - current_time

                # Update UI
                self._mode_toggle_btn.text = f"CATCHING UP ({lag:.1f}s)"

                if lag < 1.0:  # 1.0s convergence threshold
                    # Convergence!
                    self._is_catching_up = False
                    self._timeline.stop()  # Stop playback
                    # No need to reset speed
                    # Live Sync is already True, just UI update and ensure lock
                    self._mode_toggle_btn.text = "MODE: LIVE"
                    self._mode_toggle_btn.style = {"background_color": 0xFF00AA00}
                    carb.log_info("[whoimpg] Catch-Up Complete. Live Sync Engaged.")
                else:
                    # Still catching up.

                    # Manual Advancement ("Uncorked")
                    # Advance aggressively to close the gap.
                    # Use adaptive step size (min 5.0s, or 10% of lag) to guarantee convergence.
                    step = max(5.0, lag * 0.1)
                    current_rel_time = self._timeline.get_current_time()
                    new_time = current_rel_time + step

                    # Backfill Trail Logic for high-speed replay
                    backfill_start_abs = self._session_start_time + current_rel_time
                    backfill_end_abs = self._session_start_time + new_time
                    self._backfill_trail_gaps(stage, backfill_start_abs, backfill_end_abs)

                    self._timeline.set_current_time(new_time)
                    pass

            # Logic Fork: Live Sync vs Replay
            # Catching Up is effectively Replay until finished.

            if self._live_sync_active and not self._is_catching_up:
                # --- LIVE MODE ---
                # 1. Stop Timeline if it's playing (Force Real-Time)
                if self._timeline.is_playing():
                    self._timeline.stop()

                # 2. Update Timeline Visuals to match stream (Low Frequency Update)
                if (
                    self._session_start_time > 0
                    and time.time() - self._last_timeline_ui_update > 1.0
                ):
                    now = time.time()
                    rel_time = self._latest_timestamp - self._session_start_time
                    self._timeline.set_current_time(rel_time)
                    self._timeline.set_end_time(rel_time)
                    self._last_timeline_ui_update = now

                # 3. Give the trail every sample received since the last frame, not just the
                # latest pose, up to the playhead the animals are drawn at (so the trail
                # meets the animal). The pose updates below then leave the trail alone: one
                # newer than this backfill would make the next frame's backfill skip the
                # samples in between.
                self._trail_from_history = not self._safe_mode
                playhead = self._advance_live_playhead()
                self._backfill_trail_gaps(
                    stage, None, playhead if not self._safe_mode else self._latest_timestamp
                )

                # 4. Draw every animal from its history at the playhead (see LIVE_DELAY_S).
                # Safe mode keeps no history, so it draws the newest sample (Warp or CPU).
                if not self._safe_mode:
                    for eid, state in list(self._entities_state.items()):
                        if not state.get("path"):
                            self._spawn_animal(eid, state)
                            continue
                        if state.get("path") == "PENDING":
                            continue
                        pose = self._history_pose(eid, playhead)
                        if pose is not None:
                            pose["path"] = state["path"]
                            self._update_animal_pose(stage, eid, pose)
                elif self._backend == "warp" and wp is not None:
                    self._update_prim_batched_warp(stage)
                else:
                    for eid, state in self._entities_state.items():
                        # Auto-spawn if path is missing
                        if not state.get("path"):
                            species = state.get("sp", "shark")
                            sim_id_str = state.get("id", "unknown")
                            task = asyncio.ensure_future(
                                self._load_animal_asset(species, eid, sim_id_str)
                            )
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
                            # In Live Mode, we rely on the ZMQ listener to update `state['pos']`.
                            # We just ensure the Prim matches the state.
                            self._update_animal_pose(stage, eid, state)

            else:
                # --- TIMELINE / REPLAY MODE (Or Catch-Up) ---
                self._trail_from_history = False
                # 1. Read Timeline Time (Relative), or the scripted replay time
                time_code = self._replay_head()

                # 2. Convert to Absolute Time for History Query
                absolute_query_time = self._session_start_time + time_code

                # 3. Update all entities from History
                for eid, state in self._entities_state.items():
                    # Auto-spawn if path is missing (same as live mode)
                    if not state.get("path"):
                        species = state.get("sp", "shark")
                        sim_id_str = state.get("id", "unknown")
                        task = asyncio.ensure_future(
                            self._load_animal_asset(species, eid, sim_id_str)
                        )
                        state["path"] = "PENDING"

                        def _on_spawn_done(t: asyncio.Task, eid: int = eid) -> None:
                            try:
                                res = t.result()
                                self._entities_state[eid]["path"] = res
                            except Exception as e:
                                carb.log_error(f"Error spawning eid {eid}: {e}")

                        task.add_done_callback(_on_spawn_done)
                        continue

                    # From history only, never merged with 'state' (which holds live data)
                    replay_pose = self._history_pose(eid, absolute_query_time)
                    if replay_pose and state.get("path") and state.get("path") != "PENDING":
                        replay_pose["path"] = state["path"]
                        self._update_animal_pose(stage, eid, replay_pose)

            # Global Trail Update (All entities, persistent)
            t_trail = time.perf_counter()
            self._update_trail(stage, None)
            self._note_frame_ms("trail", t_trail)

            # Debug Vectors
            # Always call if we have an entity, so it can handle Hide if disabled
            active_state = self._entities_state.get(self._active_eid)
            if active_state and active_state.get("path") and active_state["path"] != "PENDING":
                prim = stage.GetPrimAtPath(active_state["path"])
                if prim.IsValid():
                    self._update_debug_vectors(stage, prim)

        except Exception as e:
            if not hasattr(self, "_update_error_shown"):
                carb.log_error(f"[whoimpg.biologger] Error updating prim: {e}")
                import traceback

                traceback.print_exc()
                self._update_error_shown = True

    def _on_follow_mode_changed(self, model: ui.AbstractValueModel) -> None:
        """HUD follow checkbox: attach the camera to the active animal or free it."""
        if self._syncing_follow_checkbox:
            return
        self.set_follow(model.get_value_as_bool())

    def _on_input_event(self, event: carb.input.InputEvent) -> bool:
        """carb input callback. The return value says whether later subscribers get the
        event (True passes it on, False consumes it); every event is passed on, so
        vantagekit's router (subscribed at the same order) still sees the camera's keys and
        mouse."""
        if (
            event.deviceType == carb.input.DeviceType.KEYBOARD
            and event.event.type == carb.input.KeyboardEventType.KEY_PRESS
        ):
            self._on_app_key(event.event)
        return True

    def _on_app_key(self, e: Any) -> None:
        """App keys: 1-5 select an animal, V / Shift+V step the vertical exaggeration, T the
        seafloor detail texture, F5 / F6 the Stage and Timeline windows. The camera's keys,
        mouse and gamepad belong to vantagekit (see _setup_viewer_controls)."""
        mods = e.modifiers
        ctrl_alt = carb.input.KEYBOARD_MODIFIER_FLAG_CONTROL | carb.input.KEYBOARD_MODIFIER_FLAG_ALT
        if mods & ctrl_alt:
            return  # Ctrl+1, Ctrl+7, Ctrl+8 are the layout hotkeys
        k = e.input

        def is_key(*names: str) -> bool:
            return any(k == getattr(carb.input.KeyboardInput, name, None) for name in names)

        for i in range(5):
            if is_key(f"KEY_{i + 1}", f"NUMPAD_{i + 1}"):
                self._cycle_active_animal(0, i)
                return
        if is_key("V"):
            down = bool(mods & carb.input.KEYBOARD_MODIFIER_FLAG_SHIFT)
            self.step_exaggeration(-1 if down else 1)
        elif is_key("T"):
            self.set_seafloor_detail(not self._seafloor_detail)
        else:
            for key, window in (("F5", "Stage"), ("F6", "Timeline")):
                if is_key(key):
                    w = ui.Workspace.get_window(window)
                    if w:
                        w.visible = not w.visible

    def _toggle_hud_visibility(self) -> None:
        """Shows or hides the HUD column (Window > Biologger HUD)."""
        if self._hud is not None:
            self._hud.toggle()

    def step_exaggeration(self, direction: int) -> None:
        """One step up (1) or down (-1) through the vertical exaggeration factors."""
        self.set_vertical_exaggeration(view_scale.step_exaggeration(self._vexag, direction))

    async def _hide_viewport_chrome(self) -> None:
        """Hides the viewport's own toolbar (the Menubar layer: settings, renderer, visibility
        and camera pickers, resolution and lighting) and its stats overlay (the HUD header shows
        the frame rate), the way Kit's F7 toggle does. The viewport may appear late, so this
        checks for about 15 s and hides each layer once; F7 brings them back."""
        layers = [("Menubar", "menubar"), ("All Stats", "stats")]
        done: set[str] = set()
        app = omni.kit.app.get_app()
        for frame in range(900):
            await app.next_update_async()
            if frame % 30:
                continue
            try:
                vpw = omni.kit.viewport.utility.get_active_viewport_window()
            except Exception:
                vpw = None
            if vpw is None:
                continue
            for layer_id, category in layers:
                if layer_id in done:
                    continue
                layer = vpw._find_viewport_layer(layer_id, category)  # as Kit's F7 does
                if layer is not None:
                    layer.visible = False
                    done.add(layer_id)
                    carb.log_info(f"[whoimpg.biologger] Hid viewport layer: {layer_id}")
            if len(done) == len(layers):
                return

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
                carb.log_info(f"[whoimpg.biologger] Viewport camera set to: {camera_path}")
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

    def _on_mode_toggle_clicked(self) -> None:
        """Toggle between LIVE and TIMELINE modes."""
        if self._live_sync_active:
            self._switch_to_timeline_mode()
        else:
            self._switch_to_live_mode()

    def _switch_to_timeline_mode(self) -> None:
        self._live_sync_active = False
        self._mode_toggle_btn.text = "MODE: TIMELINE"
        self._mode_toggle_btn.style = {
            "background_color": 0xFF805000
        }  # Dark Teal/Slate for better text contrast

        # Show Timeline Window
        import contextlib

        with contextlib.suppress(Exception):
            ui.Workspace.show_window("Timeline", True)
            # Fallback/Redundancy
            w = ui.Workspace.get_window("Timeline")
            if w:
                w.visible = True
        # Pause immediately
        if self._timeline.is_playing():
            self._timeline.pause()

    def set_replay_time(self, seconds: float) -> None:
        """Replays at ``seconds`` from the session start without moving Kit's timeline.

        Changing the timeline's time makes the renderer re-sync the whole stage (about 2.4 s
        per change with the 30 m DEM), so scripted replays, such as rendering a reel frame by
        frame, set this instead. Scrubbing or playing the timeline takes over again.
        """
        self._is_catching_up = False
        self._switch_to_timeline_mode()
        self._replay_time = float(seconds)

    def _replay_head(self) -> float:
        """Replay time in seconds from the session start: the scripted one, else the timeline's."""
        return (
            self._replay_time
            if self._replay_time is not None
            else self._timeline.get_current_time()
        )

    def _switch_to_live_mode(self) -> None:
        self._replay_time = None
        # Check Lag
        current_time = self._session_start_time + self._timeline.get_current_time()
        lag = self._latest_timestamp - current_time

        # Threshold: 2.0 seconds
        if lag > 2.0:
            # Enter Catch-Up Mode
            self._live_sync_active = True
            self._is_catching_up = True
            self._mode_toggle_btn.text = "MODE: CATCH UP"
            self._mode_toggle_btn.style = {"background_color": 0xFFCC00}  # Yellow

            # Manual Catch-Up via Update Loop (Uncorked)
            # We do NOT play the timeline, we just set the flag.
            # The _update_prim loop will manually advance time fast.
            self._timeline.stop()

            carb.log_info(f"[whoimpg] Catch-Up started. Lag: {lag:.2f}s. mode=MANUAL_STEP")
        else:
            # Immediate Engagement
            self._live_sync_active = True
            self._is_catching_up = False
            self._mode_toggle_btn.text = "MODE: LIVE"
            self._mode_toggle_btn.style = {"background_color": 0xFF00AA00}  # Green

            # Stop playback to prevent conflict
            if self._timeline.is_playing():
                self._timeline.stop()

        # Optional: Hide timeline? For now keep it visible.

    def _on_align_changed(self, model: ui.AbstractValueModel) -> None:
        self._offset_roll = self._offset_roll_slider.model.get_value_as_float()
        self._offset_pitch = self._offset_pitch_slider.model.get_value_as_float()
        self._offset_heading = self._offset_heading_slider.model.get_value_as_float()

    def _reset_full_scene(self) -> None:
        """Wipes EVERYTHING: animals, tracks, and bathymetry."""
        carb.log_info("[whoimpg.biologger] Full Scene Reset triggered...")
        stage = omni.usd.get_context().get_stage()
        if not stage:
            return

        # 1. Clean animals and tracks
        self._clear_all_entities()

        # 2. Clean bathymetry
        bathymetry_path = "/World/Bathymetry"
        if stage.GetPrimAtPath(bathymetry_path).IsValid():
            carb.log_info(f"[whoimpg.biologger] Removing bathymetry at {bathymetry_path}")
            stage.RemovePrim(bathymetry_path)

        # 3. Optional: Trigger a fresh stage setup if bathymetry is enabled
        if self._bathymetry_checkbox.model.get_value_as_bool():
            import asyncio

            # Keep a reference so the task is not garbage collected mid-run
            self._new_stage_task = asyncio.ensure_future(self.__new_stage())

    def _clear_all_entities(self) -> None:
        """Clears all spawned animals and their trajectory tracks from the stage."""
        carb.log_info("[whoimpg.biologger] Clearing all entities and tracks...")

        stage = omni.usd.get_context().get_stage()
        if not stage:
            return

        # 1. Remove spawned animal prims
        for state in self._entities_state.values():
            path = state.get("path")
            if path and stage.GetPrimAtPath(path).IsValid():
                stage.RemovePrim(path)

        # 2. Clear trail prims
        if hasattr(self, "_trail_prim_path"):
            trail_prim = stage.GetPrimAtPath(self._trail_prim_path)
            if trail_prim.IsValid():
                # Remove all children of the trail root
                for child in trail_prim.GetChildren():
                    stage.RemovePrim(child.GetPath())

        # 3. Reset internal state
        self._entities_state.clear()
        self._entities_trail_buffers.clear()
        self._entity_history.clear()
        self._active_eid = -1
        self._packet_count = 0

        # 4. Remove Bathymetry if present
        # This is now handled by the separate "Reset Scene" button if needed.
        # Keeping animals and bathymetry cleanup separate as requested.
        pass

        # The HUD readouts follow on the next frame (no active animal)
        carb.log_info("[whoimpg.biologger] Scene cleared successfully.")

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

        # Matte, sunlit trail: the ODBA colour drives diffuse so the tube shades like the
        # seafloor, with no specular (the default sheen read as glossy plastic).
        shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).ConnectToSource(
            reader.ConnectableAPI(), "result"
        )
        shader.CreateInput("emissiveColor", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(0, 0, 0))
        shader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(1.0)
        shader.CreateInput("useSpecularWorkflow", Sdf.ValueTypeNames.Int).Set(1)
        shader.CreateInput("specularColor", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(0, 0, 0))

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

        # In replay (timeline) mode the trail ends at the replay time, as it did when the
        # animal was there; live, it ends at the newest sample
        cutoff = None
        if not self._live_sync_active or self._is_catching_up:
            cutoff = self._session_start_time + self._replay_head()

        # Iterate over all entity trail buffers and update/render them
        for eid, trail_state in self._entities_trail_buffers.items():
            self._clip_baked_segments(stage, trail_state, cutoff)
            buffer = trail_state["buffer"]
            if cutoff is not None and buffer:
                buffer = buffer[: bisect_right(buffer, cutoff, key=lambda p: p[0])]
            active = stage.GetPrimAtPath(f"{self._trail_prim_path}/Trail_{eid}_active")
            if active.IsValid():
                if len(buffer) < 2:
                    UsdGeom.Imageable(active).MakeInvisible()
                else:
                    UsdGeom.Imageable(active).MakeVisible()
            if not buffer or len(buffer) < 2:
                # if eid == 0:
                # if eid == 0:
                #     carb.log_warn(
                #         f"[whoimpg.biologger] Trail buffer for eid {eid} is "
                #         f"empty or too small: {len(buffer) if buffer else 0}"
                #     )
                continue

            # Debug log for eid=0
            # if eid == 0 and self._packet_count % 60 == 0:
            # if eid == 0 and self._packet_count % 60 == 0:
            #    carb.log_info(
            #        f"[whoimpg.biologger] Rendering trail for eid {eid}, "
            #        f"buffer size: {len(buffer)}"
            #    )

            # Path for the ACTIVE segment (the one currently being populated)
            active_trail_path = f"{self._trail_prim_path}/Trail_{eid}_active"

            # Decimate for visualization performance, averaging ODBA over each block so the
            # colour shows the block's mean effort rather than one aliased sample
            max_visual_points = 5000
            step = max(1, len(buffer) // max_visual_points)
            visual_buffer = [
                (
                    *buffer[i][:3],
                    sum(p[3] for p in buffer[i : i + step]) / len(buffer[i : i + step]),
                )
                for i in range(0, len(buffer), step)
            ]

            # Live, the samples stop at the playhead's last whole sample; end the trail at the
            # animal as drawn (interpolated at the playhead), so the tip glides with it
            # instead of stepping once per sample
            ph = self._live_playhead
            if cutoff is None and not self._safe_mode and ph is not None and ph > buffer[-1][0]:
                tip = self._history_pose(eid, ph)
                if tip is not None:
                    d, x, y = tip["phys"]["d"], tip["phys"]["px"], tip["phys"]["py"]
                    visual_buffer.append(
                        (ph, Gf.Vec3f(y * 100.0, -d * 100.0, -x * 100.0), None, buffer[-1][3])
                    )

            # Base Hue for this entity
            base_hue = trail_state.get("hue", 0.0)

            # Render the active curve
            self._render_curve(stage, active_trail_path, visual_buffer, base_hue)

        t1 = time.perf_counter()
        self._last_trail_update_ms = (t1 - t0) * 1000.0

    def _clip_baked_segments(
        self, stage: Usd.Stage, trail_state: dict, cutoff: float | None
    ) -> None:
        """Shows baked trail segments up to ``cutoff`` (record time; None: all of them).

        Segments that end before it stay as baked, those that start after it are hidden, and
        the one it falls in is re-rendered up to it. Only changes are written, so a replay
        that moves forward re-renders one segment per frame.
        """
        shown = trail_state.setdefault("clip", {})  # path -> (visible, rendered cutoff or None)
        for path, samples in trail_state.get("baked", {}).items():
            if cutoff is None or samples[-1][0] <= cutoff:
                visible, cut = True, None
            elif samples[0][0] > cutoff:
                visible, cut = False, None
            else:
                visible, cut = True, cutoff
            was_visible, was_cut = shown.get(path, (True, None))
            prim = stage.GetPrimAtPath(path)
            if not prim.IsValid():
                continue
            if visible != was_visible:
                if visible:
                    UsdGeom.Imageable(prim).MakeVisible()
                else:
                    UsdGeom.Imageable(prim).MakeInvisible()
            if visible and cut != was_cut:
                part = (
                    samples
                    if cut is None
                    else samples[: bisect_right(samples, cut, key=lambda p: p[0])]
                )
                if len(part) >= 2:
                    self._render_curve(stage, path, part, trail_state["hue"])
            shown[path] = (visible, cut if visible else was_cut)

    def _render_curve(
        self, stage: Usd.Stage, path: str, visual_buffer: list, base_hue: float
    ) -> None:
        # Array maths (view_scale): segments hold up to 5000 samples and a replay re-renders
        # one per frame, so per-sample Python loops here held Kit's main thread for seconds
        ts = np.fromiter((p[0] for p in visual_buffer), dtype=np.float64, count=len(visual_buffer))
        pos = np.array([(p[1][0], p[1][1], p[1][2]) for p in visual_buffer], dtype=np.float64)
        odba = np.fromiter(
            (p[3] if len(p) > 3 else 0.0 for p in visual_buffer),
            dtype=np.float64,
            count=len(visual_buffer),
        )
        smoothing = self._settings.get(TRAIL_SMOOTHING_SETTING)
        ts, pos, odba = view_scale.smooth_trail(
            ts,
            pos,
            odba,
            DEFAULT_TRAIL_SMOOTHING_S if smoothing is None else float(smoothing),
            self._trail_width_cm,
        )
        pos[:, 1] *= self._vexag
        rgb = view_scale.odba_colors(odba)

        prim = stage.GetPrimAtPath(path)
        curves = None
        if not prim.IsValid():
            self._curve_written.pop(path, None)  # a new curve at an old path is empty
            curves = UsdGeom.BasisCurves.Define(stage, path)
            curves.CreateWidthsAttr(Vt.FloatArray([self._trail_width_cm]))
            curves.SetWidthsInterpolation(UsdGeom.Tokens.constant)
            # A linear curve renders as one capsule per sample, which beads into lumps
            # wherever samples are closer than the tube is wide; a Catmull-Rom spline through
            # the same samples renders as one continuous tube. It spans only its inner points,
            # so the ends are repeated below to reach the first and last sample (and meet the
            # neighbouring segment).
            curves.CreateTypeAttr().Set(UsdGeom.Tokens.cubic)
            curves.CreateBasisAttr().Set(UsdGeom.Tokens.catmullRom)
            # Unpickable, so the trail does not interfere with selection. Done once per curve:
            # set_pickable is slow on a large stage, and replays re-render a curve every frame
            omni.usd.get_context().set_pickable(path, False)
            mat_path = self._ensure_trail_material(stage)
            UsdShade.MaterialBindingAPI(curves).Bind(
                UsdShade.Material(stage.GetPrimAtPath(mat_path))
            )
        else:
            curves = UsdGeom.BasisCurves(prim)
        pos = np.vstack([pos[:1], pos, pos[-1:]]).astype(np.float32)
        rgb = np.vstack([rgb[:1], rgb, rgb[-1:]]).astype(np.float32)

        # Write only what changed. Setting the points re-submits the curve to the renderer
        # even with the same values, and a re-submitted curve has no valid motion for the
        # frame, so DLSS blends in the trail from earlier frames at its old screen place
        # (offset copies while the camera moves). Most frames the trail has not changed.
        digest = hash((pos.tobytes(), rgb.tobytes()))
        if self._curve_written.get(path) == digest:
            return
        self._curve_written[path] = digest

        curves.GetCurveVertexCountsAttr().Set(Vt.IntArray([len(pos)]))
        curves.GetPointsAttr().Set(Vt.Vec3fArray.FromNumpy(pos))

        primvar_api = UsdGeom.PrimvarsAPI(curves.GetPrim())
        if curves.GetPrim().HasAttribute("primvars:displayColor:indices"):
            curves.GetPrim().RemoveProperty("primvars:displayColor:indices")

        color_primvar = primvar_api.CreatePrimvar("displayColor", Sdf.ValueTypeNames.Color3fArray)
        color_primvar.SetInterpolation(UsdGeom.Tokens.vertex)
        color_primvar.Set(Vt.Vec3fArray.FromNumpy(rgb))

    def set_trail_width(self, width_cm: float, auto: bool = False) -> int:
        """Sets the width of every trail curve, existing and new; returns how many changed.

        The default (5 cm) suits close views of the animal; kilometre-scale overviews of a
        whole deployment need metres to be visible. A width set by hand (``auto`` False)
        turns the distance-adaptive width off until ``set_trail_width_auto(True)``.
        """
        if not auto and self._trail_width_auto:
            self.set_trail_width_auto(False)
        self._trail_width_cm = float(width_cm)
        stage = omni.usd.get_context().get_stage()
        root = stage.GetPrimAtPath(self._trail_prim_path) if stage else None
        if not root or not root.IsValid():
            return 0
        changed = 0
        for prim in Usd.PrimRange(root):
            if prim.IsA(UsdGeom.BasisCurves):
                UsdGeom.BasisCurves(prim).GetWidthsAttr().Set(Vt.FloatArray([self._trail_width_cm]))
                changed += 1
        # Baked segments are re-rendered so their averaging matches the new width
        self._rerender_baked_trails(stage)
        return changed

    def set_trail_width_auto(self, enabled: bool) -> None:
        """Turns the distance-adaptive trail width (out of follow mode) on or off."""
        self._trail_width_auto = enabled
        self._trail_width_last_check = 0.0
        if hasattr(self, "_trail_auto_checkbox"):
            self._trail_auto_checkbox.model.set_value(enabled)

    def _update_auto_trail_width(self, stage: Usd.Stage) -> None:
        """Out of follow mode, steps the trail width with the camera's distance to the trail.

        Checked twice a second; the trail is re-rendered only when the width takes a step.
        Follow mode returns to the close-up width.
        """
        now = time.time()
        if not self._trail_width_auto or now - self._trail_width_last_check < 0.5:
            return
        self._trail_width_last_check = now
        if self._follow_mode_enabled:
            width = view_scale.TRAIL_WIDTH_MIN_CM
        else:
            root = stage.GetPrimAtPath(self._trail_prim_path)
            cam_path = omni.kit.viewport.utility.get_active_viewport_camera_path()
            cam = stage.GetPrimAtPath(str(cam_path)) if cam_path else None
            if not root.IsValid() or not cam or not cam.IsValid():
                return
            eye = np.array(
                UsdGeom.Xformable(cam)
                .ComputeLocalToWorldTransform(Usd.TimeCode.Default())
                .ExtractTranslation()
            )
            nearest = math.inf
            for prim in Usd.PrimRange(root):
                if not prim.IsA(UsdGeom.BasisCurves):
                    continue
                if UsdGeom.Imageable(prim).ComputeVisibility() == UsdGeom.Tokens.invisible:
                    continue
                pts = UsdGeom.BasisCurves(prim).GetPointsAttr().Get()
                if pts:
                    d = np.linalg.norm(np.asarray(pts, dtype=np.float64) - eye, axis=1)
                    nearest = min(nearest, float(d.min()))
            if not math.isfinite(nearest):
                return
            width = view_scale.adaptive_trail_width_cm(nearest, self._trail_width_cm)
        if width != self._trail_width_cm:
            self.set_trail_width(width, auto=True)

    def set_vertical_exaggeration(self, factor: float) -> float:
        """Stretches the scene vertically about sea level by ``factor``; returns the factor.

        The DEM and uncertainty band take a scale on their root prims, the trails are
        re-rendered from their true samples and the animals are placed at exaggerated depth,
        keeping their true shape and orientation. Lighting follows the stretched geometry;
        the DEM's baked hillshade keeps the true slopes.
        """
        previous = self._vexag
        self._vexag = min(max(float(factor), 1.0), view_scale.EXAGGERATION_MAX)
        stage = omni.usd.get_context().get_stage()
        if stage is not None:
            self._apply_exaggeration_scale(stage)
            self._rerender_baked_trails(stage)
            # Animals move on their next sample; re-place them now in case playback has
            # stopped
            for state in self._entities_state.values():
                prim = stage.GetPrimAtPath(state.get("path") or "/")
                if not prim.IsValid() or prim.IsPseudoRoot():
                    continue
                for op in UsdGeom.Xformable(prim).GetOrderedXformOps():
                    if op.GetOpType() == UsdGeom.XformOp.TypeTranslate:
                        pos = op.Get()
                        if pos is not None:
                            op.Set(type(pos)(pos[0], pos[1] * self._vexag / previous, pos[2]))
                        break
        if self._hud is not None:
            self._hud.set("exag", f"Exaggeration {self._vexag:g}x  (V)")
        carb.log_info(f"[whoimpg.biologger] Vertical exaggeration {self._vexag:g}x")
        return self._vexag

    def set_seafloor_detail(self, on: bool) -> None:
        """Turns the decorative seafloor detail texture on or off (applied once the DEM loads)."""
        self._seafloor_detail = bool(on)
        self._settings.set(f"{LOOK_SETTINGS}/seafloorDetail", self._seafloor_detail)
        if hasattr(self, "_detail_checkbox"):
            self._detail_checkbox.model.set_value(self._seafloor_detail)
        stage = omni.usd.get_context().get_stage()
        if stage is not None:
            self._apply_seafloor_detail(stage)

    def _apply_seafloor_detail(self, stage: Usd.Stage) -> None:
        if self._seafloor_detail_applied == self._seafloor_detail:
            return
        cache = str(REPO_ROOT / "omniverse-logs" / "detail-cache")
        if dem_tiles.set_seafloor_detail(stage, self._seafloor_detail, cache):
            self._seafloor_detail_applied = self._seafloor_detail
            carb.log_info(f"[whoimpg.biologger] Seafloor detail texture {self._seafloor_detail}")

    def _exaggerated(self, pos: Any) -> Any:
        """A scene position (Y up, sea level at 0) with depth stretched by the exaggeration."""
        if self._vexag == 1.0:
            return pos
        return type(pos)(pos[0], pos[1] * self._vexag, pos[2])

    def _apply_exaggeration_scale(self, stage: Usd.Stage) -> None:
        """Sets the vertical scale on the DEM and uncertainty roots (created later too)."""
        for path in (dem_tiles.DEM_ROOT, geo_overlay.ROOT):
            prim = stage.GetPrimAtPath(path)
            if not prim.IsValid() or not prim.IsA(UsdGeom.Xformable):
                continue
            xf = UsdGeom.Xformable(prim)
            op = next(
                (o for o in xf.GetOrderedXformOps() if o.GetOpName() == "xformOp:scale:vexag"),
                None,
            ) or xf.AddScaleOp(UsdGeom.XformOp.PrecisionDouble, "vexag")
            scale = Gf.Vec3d(1.0, self._vexag, 1.0)
            if op.Get() != scale:
                op.Set(scale)

    def _rerender_baked_trails(self, stage: Usd.Stage) -> None:
        """Re-renders baked trail segments from their true samples (active ones re-render
        every frame anyway)."""
        for trail_state in self._entities_trail_buffers.values():
            for path, buffer in trail_state.get("baked", {}).items():
                self._render_curve(stage, path, buffer, trail_state["hue"])
            # Rendered in full now; a replay re-clips them on the next frame
            shown = trail_state.get("clip", {})
            for path in shown:
                shown[path] = (shown[path][0], None)

    def _bake_trail_segment(self, stage: Usd.Stage, eid: int, trail_state: dict) -> None:
        """Bakes the current trail buffer into a static USD prim and clears the buffer."""
        seg_idx = trail_state["segment_count"]
        path = f"{self._trail_prim_path}/Trail_{eid}_seg_{seg_idx}"

        carb.log_info(f"[whoimpg.biologger] Baking trail segment for EID {eid} to {path}")

        # Render the final static segment
        self._render_curve(stage, path, trail_state["buffer"], trail_state["hue"])

        # Keep the raw samples so a trail width change can re-render the segment
        trail_state.setdefault("baked", {})[path] = trail_state["buffer"]

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

    def _setup_player_camera(self, stage: Usd.Stage) -> str:
        """
        Spawns or resets the dedicated Player Camera at /World/PlayerCam.
        Returns the path to the camera.
        """
        cam_path = "/World/PlayerCam"

        prim = stage.GetPrimAtPath(cam_path)

        if not prim.IsValid():
            # Create the camera
            cam = UsdGeom.Camera.Define(stage, cam_path)

            # Set default attributes similar to standard kit camera
            # Optics: Matching standard "Persp" defaults to avoid exposure shifts
            # INSPECTED DATA: FL=18.147562 FD=400.0 FStop=0.0 HA=20.955 VA=15.29 Clip=(1, 10000000)
            cam.CreateFocalLengthAttr(18.1476)
            cam.CreateFocusDistanceAttr(400.0)
            cam.CreateFStopAttr(0.0)  # 0.0 = Pinhole / Infinite DoF (Matches Persp)
            cam.CreateHorizontalApertureAttr(20.955)  # Standard sensor
            cam.CreateVerticalApertureAttr(15.2908)

            # Clipping: Match Persp exactly
            cam.CreateClippingRangeAttr(Gf.Vec2f(1.0, 10000000.0))

            # Ensure it has Xformable for movement
            xform = UsdGeom.Xformable(cam)
            xform.ClearXformOpOrder()  # Reset

            # Set initial position (High and back)
            # Default to tracking a generic center if no animal yet
            cam_pos = Gf.Vec3d(0, 300, 1600)
            target_pos = Gf.Vec3d(0, 0, 0)

            look_at = Gf.Matrix4d().SetLookAt(cam_pos, target_pos, Gf.Vec3d(0, 1, 0))
            mat = look_at.GetInverse()  # World Transform

            op = xform.AddTransformOp()
            op.Set(mat)

            # --- FORCE PER-CAMERA OPTICS (Persistent) ---
            # Matched from "Persp" inspection: exposure:value = 1.0
            # We do NOT force AutoExposure (it was absent in inspection)

            # Exposure Bias: 1.0
            exp_attr = cam.GetPrim().CreateAttribute(
                "rtx:post:tonemap:exposure", Sdf.ValueTypeNames.Float
            )
            exp_attr.Set(1.0)

            carb.log_info(
                f"[whoimpg.biologger] Created Player Camera at {cam_path} (Optics Matched)"
            )
        else:
            carb.log_info(f"[whoimpg.biologger] Player Camera already exists at {cam_path}")

        return cam_path

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

                topic = frames[0]
                payload = frames[1]

                # Unpack MessagePack
                message = msgpack.unpackb(payload, raw=False)

                # Georeference/uncertainty messages also carry "eid"; keep them out of the
                # state path below.
                if topic.endswith(b"/meta"):
                    if isinstance(message, dict) and "eid" in message:
                        self._entity_meta[int(message["eid"])] = message
                    continue

                # State arrives in batches (see ZMQPublisher.flush); a single state
                # message is still accepted
                batch = topic.endswith(b"/batch") and isinstance(message, dict)
                states = message.get("batch", []) if batch else [message]
                for message in states:
                    self._packet_count += 1
                    self._packets_since_last_update += 1

                    # Peek at EID for logging
                    if isinstance(message, dict) and "eid" in message:
                        peid = message["eid"]
                        if peid not in seen_eids:
                            carb.log_info(
                                f"[whoimpg.biologger] First packet for EID {peid}: {message}"
                            )
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

                        # Init session start time if 0
                        if self._session_start_time == 0.0:
                            self._session_start_time = ts

                        # --- History Recording (CPU Optimized) ---
                        if not self._safe_mode:
                            # Ensure buffers exist
                            if eid not in self._entity_history:
                                self._entity_history[eid] = {
                                    "times": [],
                                    "pos": [],  # List of (px, py, depth)
                                    "rot": [],  # List of (r, p, h) or quat
                                    "odba": [],  # for the trail colour
                                }

                            hist = self._entity_history[eid]

                            # Only append if time moved forward (deduplicate)
                            if not hist["times"] or ts > hist["times"][-1]:
                                hist["times"].append(ts)

                                # Extract minimal state for replay
                                phys_data = message.get("phys", {})
                                px = float(phys_data.get("px", 0.0))
                                py = float(phys_data.get("py", 0.0))
                                d = float(phys_data.get("d", 0.0))
                                hist["pos"].append((px, py, d))

                                rot = message.get("rot", [0, 0, 0])
                                # Ensure we store consistent type (list/tuple)
                                hist["rot"].append(tuple(rot) if rot else (0.0, 0.0, 0.0))
                                hist["odba"].append(float(phys_data.get("odba", 0.0) or 0.0))

                                # Update Timeline Range (Throttle to avoid API spam)
                                if self._live_sync_active and self._packet_count % 10 == 0:
                                    # We need to schedule this on main thread really, but
                                    # for now let's update a flag or try direct call if thread-safe
                                    # Creating a task is safer
                                    pass  # Timeline update moved to main thread update loop

                        # Resolve species for asset selection
                        # Species per (tag, sim) once, not a metadata scan per sample
                        species = self._species_cache.get((tag_id, sim_id))
                        if species is None:
                            species = None
                            if tag_id:
                                # Case-insensitive lookup for tag_id
                                lookup_tag = str(tag_id).lower().strip()
                                for k, v in self._id_to_species.items():
                                    if str(k).lower().strip() == lookup_tag:
                                        species = v
                                        break

                                # Fuzzy match if exact fails
                                if not species:
                                    for key, sp in self._id_to_species.items():
                                        if (
                                            lookup_tag in str(key).lower()
                                            or str(key).lower() in lookup_tag
                                        ):
                                            species = sp
                                            break

                            if not species:
                                lookup_sim = str(sim_id).lower().strip()
                                # Extra pattern match for sword/swordfish
                                if "sword" in lookup_sim:
                                    for v in self._id_to_species.values():
                                        if "xiphias" in str(v).lower():
                                            species = v
                                            break

                                if not species:
                                    for k, v in self._id_to_species.items():
                                        if str(k).lower().strip() == lookup_sim:
                                            species = v
                                            break

                            if not species:
                                # Fallback: check if the sim_id contains a known tag_id as a prefix
                                # This supports A/B testing like "RED001_A"
                                lookup_sim = str(sim_id).lower().strip()
                                for tid_key, sp in self._id_to_species.items():
                                    if lookup_sim.startswith(str(tid_key).lower().strip()):
                                        species = sp
                                        break

                            if not species:
                                species = "unknown"
                            self._species_cache[(tag_id, sim_id)] = species

                        # Extraction orientation (Euler)
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

                        # Update placeholder ID if we have a real one now
                        # (Handles the case where default scene spawned "default" shark)
                        current_id = state.get("id")
                        if current_id == "default" and sim_id not in ("unknown", "default"):
                            state["id"] = sim_id
                            # Also update species if it was generic
                            if species != "unknown":
                                state["sp"] = species

                        state.update({"ts": ts, "rot_data": rot_data, "phys": phys})

                        # AUTO-SELECTION: If this is the first animal we see, follow it immediately
                        if self._active_eid == -1:
                            self._active_eid = eid
                            carb.log_info(
                                f"[whoimpg.biologger] Auto-selected first active EID: {eid}"
                            )

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

    def _update_geo_layers(self) -> None:
        """Applies simulator georeference: scene origin, uncertainty overlay, DEM tiles.

        Throttled to once a second for the overlay and every two seconds for DEM focus.
        """
        now = time.time()
        if not getattr(self, "_entity_meta", None) or not hasattr(self, "_uncertainty_checkbox"):
            return  # subscriber or HUD not set up yet, or no georeference received
        if now - self._geo_last_update < 1.0:
            return
        self._geo_last_update = now
        stage = omni.usd.get_context().get_stage()
        if stage is None:
            return
        # DEM and overlay roots appear after the georeference; give them the exaggeration
        self._apply_exaggeration_scale(stage)
        self._apply_seafloor_detail(stage)  # the seabed material appears with the first mesh

        metas = list(self._entity_meta.values())

        # Origin: the first entity that has one (the simulator's start fix).
        if self._geo_origin is None:
            for meta in metas:
                origin = meta.get("origin")
                if origin:
                    self._geo_origin = (float(origin["lat"]), float(origin["lon"]))
                    carb.log_info(
                        f"[whoimpg.biologger] Scene origin from simulator: {self._geo_origin} "
                        f"({meta.get('sim_id')}, track model {meta.get('track_model')})"
                    )
                    break

        if self._geo_origin is not None and not self._look_applied:
            self._look_applied = True
            self.apply_scene_look()

        show_prism = self._uncertainty_checkbox.model.get_value_as_bool()
        for meta in metas:
            geo_overlay.write_prism_mesh(
                stage, str(meta.get("sim_id", meta.get("eid"))), meta.get("prism") or [], show_prism
            )

        if self._geo_origin is None or not self._dem_stream_checkbox.model.get_value_as_bool():
            return

        if self._dem_streamer is None:
            self._dem_streamer = self._make_dem_source(self._geo_origin)
            for meta in metas:
                bounds = meta.get("prefetch_bounds_ne")
                if bounds:
                    self._dem_streamer.set_prefetch(bounds)
                    break

        if now - self._dem_last_focus_update >= 2.0:
            self._dem_last_focus_update = now
            self._dem_streamer.update(self._dem_focus_points(stage))

    def apply_scene_look(self) -> None:
        """Sun, sky, water surface and tone mapping for the scene.

        Before the simulator's georeference arrives the sun is a neutral default; with it,
        the sun stands where it did over the deployment. Settings under ``look/``:
        ``solarHour`` (local solar time on the deployment date, default 9), ``turbidity`` (2),
        ``sunIntensity`` (7000), ``skyIntensity`` (300), ``fNumber`` (11, fixed exposure) and
        ``underwaterVisibilityM`` (40). The DEM's baked hillshade follows the same sun.
        """

        def look_float(name: str, default: float) -> float:
            value = self._settings.get(f"{LOOK_SETTINGS}/{name}")
            return default if value is None else float(value)

        stage = omni.usd.get_context().get_stage()
        if stage is None:
            return
        start = None
        for meta in self._entity_meta.values():
            fixes = meta.get("fixes") or []
            if fixes and fixes[0].get("t") is not None:
                start = float(fixes[0]["t"])
                break
        sun_el, sun_az = scene_look.apply_scene_look(
            stage,
            self._settings,
            self._geo_origin,
            start,
            cache_dir=str(REPO_ROOT / "omniverse-logs" / "sky-cache"),
            log=lambda msg: carb.log_info(f"[whoimpg.biologger] {msg}"),
            solar_hour=look_float("solarHour", scene_look.DEFAULT_SOLAR_HOUR),
            turbidity=look_float("turbidity", scene_look.DEFAULT_TURBIDITY),
            sun_intensity=look_float("sunIntensity", scene_look.DEFAULT_SUN_INTENSITY),
            sky_intensity=look_float("skyIntensity", scene_look.DEFAULT_SKY_INTENSITY),
            f_number=look_float("fNumber", scene_look.DEFAULT_F_NUMBER),
        )
        dem_tiles.set_sun(sun_el, sun_az)
        if dem_tiles.set_in_situ(bool(self._settings.get(f"{LOOK_SETTINGS}/seafloorInSitu"))):
            n = dem_tiles.recolour_dem_meshes(stage)
            view = "in situ" if dem_tiles.IN_SITU else "from the surface"
            carb.log_info(f"[whoimpg.biologger] Seafloor colour {view} ({n} meshes)")
        self.set_seafloor_detail(bool(self._settings.get(f"{LOOK_SETTINGS}/seafloorDetail")))
        self._underwater_fog.visibility_m = look_float(
            "underwaterVisibilityM", scene_look.DEFAULT_VISIBILITY_M
        )
        self._underwater_fog.reset()  # re-apply fog and surface reflection for the camera

    def _make_dem_source(
        self, origin: tuple[float, float]
    ) -> dem_tiles.DemTileStreamer | dem_tiles.DemGridSource:
        """A fused-grid source when a topobathykit policy file is configured, else XYZ tiles.

        ``demPolicy`` is a policy YAML path, absolute or relative to the repo hosting this
        extension (default ``config/topobathykit/ne_canyons.yaml``); set it to "" for tiles.
        """
        url = (
            self._settings.get_as_string("/exts/whoimpg.biologger.subscriber/topobathykitUrl")
            or "http://garnet.internal:9595"
        )
        log = lambda msg: carb.log_info(f"[whoimpg.biologger] {msg}")  # noqa: E731
        get_stage = lambda: omni.usd.get_context().get_stage()  # noqa: E731
        policy_setting = self._settings.get("/exts/whoimpg.biologger.subscriber/demPolicy")
        if policy_setting is None:
            policy_setting = "config/topobathykit/ne_canyons.yaml"
        policy: Path | None = None
        if policy_setting:
            policy = Path(policy_setting)
            if not policy.is_absolute():
                policy = REPO_ROOT / policy
        if policy is not None and policy.is_file():
            log(f"DEM source: fused grid with policy {policy}")
            return dem_tiles.DemGridSource(
                get_stage=get_stage,
                origin=origin,
                service_url=url,
                policy_yaml=policy.read_text(encoding="utf-8"),
                cache_dir=str(REPO_ROOT / "omniverse-logs" / "dem-cache"),
                log=log,
            )
        log("DEM source: server-policy XYZ tiles (no demPolicy file)")
        return dem_tiles.DemTileStreamer(
            get_stage=get_stage, origin=origin, service_url=url, log=log
        )

    def _dem_focus_points(self, stage: Usd.Stage) -> list[tuple[float, float]]:
        """(north, east) metres of the active camera and the active animal."""
        points: list[tuple[float, float]] = []
        try:
            cam_path = omni.kit.viewport.utility.get_active_viewport_camera_path()
            cam = stage.GetPrimAtPath(str(cam_path)) if cam_path else None
            if cam and cam.IsValid():
                pos = (
                    UsdGeom.Xformable(cam)
                    .ComputeLocalToWorldTransform(Usd.TimeCode.Default())
                    .ExtractTranslation()
                )
                points.append((-pos[2] / dem_tiles.SCENE_SCALE, pos[0] / dem_tiles.SCENE_SCALE))
        except Exception:
            pass
        state = self._entities_state.get(self._active_eid)
        path = state.get("path") if state else None
        if path:
            prim = stage.GetPrimAtPath(path)
            if prim and prim.IsValid():
                pos = (
                    UsdGeom.Xformable(prim)
                    .ComputeLocalToWorldTransform(Usd.TimeCode.Default())
                    .ExtractTranslation()
                )
                points.append((-pos[2] / dem_tiles.SCENE_SCALE, pos[0] / dem_tiles.SCENE_SCALE))
        return points

    def _note_frame_ms(self, section: str, since: float) -> None:
        """Keeps the slowest time (ms) per section of the frame update, for /agent/status."""
        ms = (time.perf_counter() - since) * 1000.0
        self._frame_ms_max[section] = max(self._frame_ms_max.get(section, 0.0), ms)

    def _on_update_ui(self, dt_event: Any) -> None:
        """Called every frame to update UI elements safely; times its sections."""
        t0 = time.perf_counter()
        self._on_update_ui_body(dt_event)
        self._note_frame_ms("total", t0)
        if self._trace_left > 0:
            self._record_trace_row(t0, dt_event)

    def start_trace(self, frames: int) -> None:
        """Record one row per frame for the next `frames` frames (see _record_trace_row)."""
        self._trace_rows = []
        self._trace_left = max(0, int(frames))

    def _record_trace_row(self, t0: float, dt_event: Any) -> None:
        """One trace row: frame start (perf_counter s), Kit's dt, the active animal's drawn
        position and the camera eye (stage cm), the newest sample's time, the samples
        received so far and the live playhead. Read back through GET /agent/trace."""
        try:
            dt = float(dt_event if isinstance(dt_event, float) else dt_event.payload["dt"])
        except Exception:
            dt = float("nan")
        nan = float("nan")
        pose = self._animal_pose(self._active_eid) if self._active_eid is not None else None
        p = tuple(pose.position) if pose is not None else (nan, nan, nan)
        c = self._controls
        e = tuple(c.rig.eye()) if c is not None else (nan, nan, nan)
        ph = self._live_playhead if self._live_playhead is not None else nan
        self._trace_rows.append(
            (t0, dt, *p, *e, float(self._latest_timestamp), float(self._packet_count), ph)
        )
        self._trace_left -= 1

    def _on_update_ui_body(self, dt_event: Any) -> None:
        """Called every frame to update UI elements safely"""
        # Call the main 3D update loop
        # dt_event is likely delta time in seconds, or an event with .payload['dt']
        dt = 0.016  # fallback
        try:
            # If carb.events.IEvent, payload is a dictionary-like object
            if hasattr(dt_event, "payload") and "dt" in dt_event.payload:
                dt = dt_event.payload["dt"]
            elif isinstance(dt_event, float):
                dt = dt_event
        except Exception:
            pass

        t = time.perf_counter()
        self._update_prim(dt_event)
        self._note_frame_ms("prim", t)

        t = time.perf_counter()
        try:
            self._update_geo_layers()
        except Exception as e:
            carb.log_warn(f"[whoimpg.biologger] Geo layer update failed: {e}")
        self._note_frame_ms("geo", t)

        t = time.perf_counter()
        try:
            stage = omni.usd.get_context().get_stage()
            if stage is not None:
                self._update_auto_trail_width(stage)
        except Exception as e:
            carb.log_warn(f"[whoimpg.biologger] Adaptive trail width failed: {e}")
        self._note_frame_ms("trail_width", t)

        # The look from startup, with a neutral sun until the georeference arrives. Waits for
        # the scene's sun light, so it is not spent on the empty stage Kit starts with.
        if not self._look_applied and not self._look_neutral_applied:
            stage = omni.usd.get_context().get_stage()
            if stage is not None and stage.GetPrimAtPath(scene_look.SUN_PATH).IsValid():
                self._look_neutral_applied = True
                try:
                    self.apply_scene_look()
                except Exception as e:
                    carb.log_warn(f"[whoimpg.biologger] Scene look failed: {e}")

        if self._look_applied or self._look_neutral_applied:
            try:
                cam_path = omni.kit.viewport.utility.get_active_viewport_camera_path()
                stage = omni.usd.get_context().get_stage()
                cam = stage.GetPrimAtPath(str(cam_path)) if stage and cam_path else None
                if cam and cam.IsValid():
                    eye = (
                        UsdGeom.Xformable(cam)
                        .ComputeLocalToWorldTransform(Usd.TimeCode.Default())
                        .ExtractTranslation()
                    )
                    self._underwater_fog.update(eye[1])
                scene_look.hold_fixed_exposure(self._settings)
            except Exception as e:
                carb.log_warn(f"[whoimpg.biologger] Underwater fog update failed: {e}")

        # Camera: one vantagekit step (input, attached view) after the poses moved
        t = time.perf_counter()
        self._update_camera(dt)
        self._note_frame_ms("camera", t)

        # Calculate throughput
        current_time = time.time()
        if current_time - self._last_throughput_time >= 1.0:
            rate = self._packets_since_last_update / (current_time - self._last_throughput_time)
            self._throughput_str = f"{rate:.1f} pkts/s"
            self._packets_since_last_update = 0
            self._last_throughput_time = current_time

        if self._hud is not None:
            self._hud.tick()
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

        # Biologger Specific Defaults
        self._settings.set_default("/exts/whoimpg.biologger.subscriber/enableBathymetry", False)

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
        import carb

        custom_stage = self._settings.get("/biologger/stage")
        if custom_stage:
            carb.log_info(f"[whoimpg.biologger] Opening custom stage from setting: {custom_stage}")
            ctx.open_stage(str(custom_stage))
            if animal_type:
                await self._load_animal_asset(animal_type)
            # Create follow camera
            return

        if ctx.get_stage_url():
            carb.log_info(f"[whoimpg.biologger] Stage already loaded: {ctx.get_stage_url()}")
            if animal_type:
                await self._load_animal_asset(animal_type)
            # Create follow camera
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

                # Initialize Player Cam immediately (refinement)
                pc = self._setup_player_camera(omni.usd.get_context().get_stage())
                self._set_active_camera(pc)

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
            else:
                carb.log_warn(
                    "[whoimpg.biologger] Default scene not found "
                    f"(searched up from {DATA_PATH}), creating new stage."
                )

        # Fallback: If no scene loaded, still setup PlayerCam on the empty stage
        if not self._settings.get("/biologger/skipDefaultScene") and not scene_path:
            pc = self._setup_player_camera(ctx.get_stage())
            self._set_active_camera(pc)

        # --- LOAD BATHYMETRY ---
        # Only if enabled in UI and not opening a custom stage
        if (
            hasattr(self, "_bathymetry_checkbox")
            and not self._bathymetry_checkbox.model.get_value_as_bool()
        ):
            carb.log_info("[whoimpg.biologger] Bathymetry disabled via UI. Skipping fetch.")
            return

        # 1. Parse Origin
        origin_str = self._settings.get("/biologger/origin")
        origin_lat = 41.52
        origin_lon = -70.67

        if origin_str:
            try:
                parts = origin_str.split(",")
                if len(parts) == 2:
                    origin_lat = float(parts[0].strip())
                    origin_lon = float(parts[1].strip())
                    carb.log_info(
                        f"[whoimpg.biologger] Using Origin from CLI: {origin_lat}, {origin_lon}"
                    )
                else:
                    carb.log_warn(
                        f"[whoimpg.biologger] Invalid origin format '{origin_str}'. "
                        "Expected 'lat,lon'. Using default."
                    )
            except ValueError:
                carb.log_warn(
                    f"[whoimpg.biologger] Error parsing origin '{origin_str}'. Using default."
                )
        else:
            carb.log_info(
                "[whoimpg.biologger] No origin specified. "
                f"Using default Woods Hole: {origin_lat}, {origin_lon}"
            )

        # 2. Define Bounds (e.g. 2km x 2km? or 0.05 degrees?)
        # 0.02 deg is approx 2.2km lat.
        # Let's fetch a decent patch.
        lat_size = 0.05
        lon_size = 0.05

        north = origin_lat + lat_size / 2
        south = origin_lat - lat_size / 2
        east = origin_lon + lon_size / 2
        west = origin_lon - lon_size / 2

        # 3. Fetch and Create
        import carb.settings

        settings = carb.settings.get_settings()
        service_url = settings.get_as_string("/exts/whoimpg.biologger.subscriber/topobathykitUrl")
        if not service_url:
            # Deprecated key, accepted for one release.
            service_url = settings.get_as_string(
                "/exts/whoimpg.biologger.subscriber/topobathysimUrl"
            )
            if service_url:
                carb.log_warn(
                    "[whoimpg.biologger] Setting "
                    "/exts/whoimpg.biologger.subscriber/topobathysimUrl is deprecated and "
                    "will be removed in the next release; use topobathykitUrl."
                )
        service_url = service_url or "http://garnet.internal:9595"

        bridge = BathymetryBridge(service_url=service_url)
        # Run async fetch
        carb.log_info(
            "[whoimpg.biologger] Fetching Bathymetry for "
            f"N={north:.4f} S={south:.4f} W={west:.4f} E={east:.4f}..."
        )

        elevation = await bridge.fetch_elevation(north, south, west, east)

        if elevation is not None:
            # Ensure stage is valid (it should be open by now)
            stage = omni.usd.get_context().get_stage()
            if stage:
                bridge.create_mesh(
                    stage, "/World/Bathymetry", elevation, (north, south, west, east)
                )
        else:
            carb.log_warn(
                "[whoimpg.biologger] Bathymetry fetch failed. "
                "Using default scene floor if available."
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
            DATA_PATH / "data" / "biologger_meta.csv",
            REPO_ROOT / "datasets" / "biologger_meta.csv",
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
            self._species_cache.clear()  # resolved before the metadata arrived
        except Exception as e:
            carb.log_error(f"[whoimpg.biologger] Error loading metadata: {e}")

    def on_shutdown(self) -> None:
        """Clean up the extension"""
        agent_control.deregister(getattr(self, "_agent_router", None))
        self._agent_router = None
        # Camera and input: unlock the camera, restore the gamepad setting, unsubscribe
        self._camera_stage_sub = None
        if getattr(self, "_controls", None) is not None:
            self._controls.dispose()
            self._controls = None
        if getattr(self, "_input_sub_id", None):
            with contextlib.suppress(Exception):
                self._input.unsubscribe_to_input_events(self._input_sub_id)
            self._input_sub_id = None
        self._timeline_sub = None
        dem_streamer = getattr(self, "_dem_streamer", None)
        if dem_streamer is not None:
            dem_streamer.shutdown()
            self._dem_streamer = None

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
        if self._hud is not None:
            self._hud.destroy()  # dropping the reference alone leaves the column drawn
        self._hud = None
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
