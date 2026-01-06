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
import datetime
import inspect
import json
import logging
import os
import platform
import resource
import subprocess
import sys
import threading
import time
import webbrowser
from pathlib import Path
from typing import Any

import carb
import carb.input
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
from pxr import Gf, Usd, UsdGeom, Vt

DATA_PATH = Path(carb.tokens.get_tokens_interface().resolve("${whoimpg.biologger.subscriber}"))


async def _load_layout(layout_file: str, keep_windows_open: bool = False) -> None:
    """Loads a provided layout file and ensures the viewport is set to FILL."""
    try:
        # few frames delay to avoid the conflict with the
        # layout of omni.kit.mainwindow
        for _ in range(3):
            await omni.kit.app.get_app().next_update_async()
        QuickLayout.load_file(layout_file, keep_windows_open)
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

        # adjust couple of viewport settings
        self._settings.set("/app/viewport/boundingBoxes/enabled", True)

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

    async def _load_animal_asset(self, animal_type: str) -> None:
        print(f"[whoimpg.biologger] Attempting to load animal: {animal_type}")
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
            return

        # Define asset filenames
        assets = {
            "shark": "great_white_shark.glb",
            "swordfish": "swordfish.usd",
            "whaleshark": "whale_shark.usd",
        }

        asset_filename = assets.get(animal_type)
        if not asset_filename:
            print(f"[whoimpg.biologger] Error: Unknown animal type: {animal_type}")
            return

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
            return

        print(f"[whoimpg.biologger] Found asset at: {full_asset_path}")

        # Create a new Prim for the animal
        prim_path = "/World/Animal"
        prim = stage.DefinePrim(prim_path, "Xform")

        # Set default transform using robust Xformable API
        # We do this BEFORE adding the reference to ensure the prim has a stable
        # transform schema, which helps avoid Fabric "evaluatedTranslations" warnings.
        xformable = UsdGeom.Xformable(prim)
        xformable.ClearXformOpOrder()  # Clear any existing/referenced transforms

        # Add ops in standard TRS order (Translate, Rotate, Scale)
        # Note: USD applies these linearly. T * R * S * point means Scale happens first,
        # then Rotate, then Translate.
        op_translate = xformable.AddTranslateOp()
        op_rotate = xformable.AddRotateXYZOp()
        op_scale = xformable.AddScaleOp()

        # Set values
        op_translate.Set((0, 0, 0))
        op_rotate.Set((-90, 0, 0))  # GLB usually needs -90 X rotation
        op_scale.Set((100, 100, 100))  # Scale: 100 (1m -> 100cm)

        # Add the reference
        references = prim.GetReferences()
        references.AddReference(full_asset_path)

        # Select the animal
        # We select the prim so the user can see it in the Stage tree
        omni.usd.get_context().get_selection().set_selected_prim_paths([prim_path], False)

        print(f"[whoimpg.biologger] Spawned {animal_type} from {full_asset_path}")

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

        # Camera Orbit State
        self._cam_azimuth: float = 0.0  # Degrees around shark (0 = behind)
        self._cam_elevation: float = 20.0  # Degrees up (0 = level)
        self._cam_distance: float = 1500.0  # Default distance
        self._input = carb.input.acquire_input_interface()
        self._input_sub_id = None
        self._is_rmb_down = False
        self._last_mouse_pos = (0.0, 0.0)
        self._last_mouse_pos_valid: bool = False

        # Trail State
        self._trail_points: list[Gf.Vec3f] = []
        self._trail_prim_path = "/World/Trail"
        self._last_trail_update_ms = 0.0

        # Callibration State
        self._offset_roll = 0.0
        self._offset_pitch = 0.0
        self._offset_heading = 0.0

        # Throughput calculation
        self._packets_since_last_update = 0
        self._last_throughput_time = time.time()
        self._throughput_str = "0.0 pkts/s"

        # 1. Setup the UI Dashboard (Overlay style)
        # Using a small window in the top-left corner as a HUD
        self._window = ui.Window(
            "Biologger Data", width=300, height=350, dockPreference=ui.DockPreference.LEFT
        )
        with (
            self._window.frame,
            ui.ScrollingFrame(
                horizontal_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_OFF,
                vertical_scrollbar_policy=ui.ScrollBarPolicy.SCROLLBAR_AS_NEEDED,
            ),
            ui.VStack(spacing=5),
        ):
            self._status_label = ui.Label("Status: Disconnected", style={"color": 0xFF888888})
            self._packet_label = ui.Label("Packets: 0")
            self._throughput_label = ui.Label("Throughput: 0.0 pkts/s")
            self._time_label = ui.Label("Time: N/A")
            self._vector_label = ui.Label("Orientation: N/A")
            self._physics_label = ui.Label("Physics: N/A")
            self._perf_label = ui.Label("Mem: -- MB | Trail: -- ms", style={"color": 0xFFFFFF88})

            ui.Spacer(height=5)
            ui.Label("ZMQ Configuration", style={"color": 0xFFAAAAAA})
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

            ui.Spacer(height=5)
            ui.Label("Tracking Options", style={"color": 0xFFAAAAAA})
            with ui.HStack(height=20):
                self._position_tracking_checkbox = ui.CheckBox(width=20)
                self._position_tracking_checkbox.model.set_value(True)
                ui.Label("Enable Position Tracking")

            with ui.HStack(height=20):
                self._follow_mode_checkbox = ui.CheckBox(width=20)
                self._follow_mode_checkbox.model.set_value(False)
                self._follow_mode_checkbox.model.add_value_changed_fn(self._on_follow_mode_changed)
                ui.Label("Follow Mode (3rd Person)")

            with ui.HStack(height=20):
                self._trail_checkbox = ui.CheckBox(width=20)
                self._trail_checkbox.model.set_value(True)  # Default On
                self._trail_checkbox.model.add_value_changed_fn(self._on_trail_mode_changed)
                ui.Label("Show Trail")

            ui.Spacer(height=5)
            ui.Label("Camera Settings", style={"color": 0xFFAAAAAA})
            # Distance controlled via Scroll Wheel now

            with ui.HStack(height=20):
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

        # 2. Fabric setup for the animal prim (e.g., /World/Shark)
        # Note: This assumes the stage is already open or will be opened.
        # We might need to refresh this if the stage changes.
        self._stage = None
        # We will attach to stage in the update loop to be safe

        # 3. Auto-connect on startup
        self._start_listener()

        # 4. Setup UI update loop (safe way to update UI from main thread)
        self._update_sub = (
            omni.kit.app.get_app()
            .get_update_event_stream()
            .create_subscription_to_pop(self._on_update_ui, name="whoimpg.biologger.update")
        )

    def _on_update_ui(self, _: Any) -> None:
        """Called every frame to update UI elements safely"""
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

            # Memory Usage (RSS) in MB
            mem_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
            # Linux returns KB, macOS returns bytes. Assuming Linux based on environment context.
            if sys.platform != "linux":
                mem_usage /= 1024.0  # Normalize if on macOS to MB

            self._perf_label.text = (
                f"Mem: {mem_usage:.0f} MB | Trail: {self._last_trail_update_ms:.2f} ms"
            )

            if self._latest_timestamp > 0:
                dt = datetime.datetime.fromtimestamp(
                    self._latest_timestamp, tz=datetime.timezone.utc
                )
                self._time_label.text = f"Time: {dt.strftime('%Y-%m-%d %H:%M:%S')}"
            else:
                self._time_label.text = "Time: N/A"

            self._vector_label.text = f"Orientation: {self._last_vector_str}"

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

        # Apply rotation in main thread using standard USD API
        # We need to access the stage every frame for camera updates,
        # regardless of whether new telemetry data arrived.
        try:
            # Get the standard USD stage context
            usd_context = omni.usd.get_context()
            stage = usd_context.get_stage()

            if stage:
                prim = stage.GetPrimAtPath("/World/Animal")
                if prim.IsValid():
                    xformable = UsdGeom.Xformable(prim)

                    # --- Position Update (Depth + Dead Reckoning) ---
                    # Only update if we have NEW physics data
                    if (
                        self._latest_physics_data
                        and hasattr(self, "_position_tracking_checkbox")
                        and self._position_tracking_checkbox.model.get_value_as_bool()
                    ):
                        depth = float(self._latest_physics_data.get("depth", 0.0))
                        pseudo_x = float(self._latest_physics_data.get("pseudo_x", 0.0))
                        pseudo_y = float(self._latest_physics_data.get("pseudo_y", 0.0))

                        # Convert meters to cm (assuming stage is cm)
                        # Depth is positive down, so Y = -depth
                        y_pos = -depth * 100.0

                        # Dead Reckoning Mapping:
                        # Pseudo X (North-ish) -> -Z
                        # Pseudo Y (East-ish) -> +X
                        x_pos = pseudo_y * 100.0
                        z_pos = -pseudo_x * 100.0

                        # Find existing translate op
                        translate_op = None
                        for op in xformable.GetOrderedXformOps():
                            if op.GetOpType() == UsdGeom.XformOp.TypeTranslate:
                                translate_op = op
                                break

                        if not translate_op:
                            translate_op = xformable.AddTranslateOp()

                        # Update Position
                        new_trans = Gf.Vec3d(x_pos, y_pos, z_pos)
                        translate_op.Set(new_trans)

                    # --- Rotation Update ---
                    # Only update if we have NEW rotation data
                    if self._latest_quat_data:
                        q_data = self._latest_quat_data

                        # Clear existing ops if needed or just set the rotate op
                        # We look for an existing rotate op or create one
                        rotate_op = None

                        # Use a dedicated operation for telemetry to avoid overwriting
                        # the model's base orientation (which might be fixing a -90 pitch).
                        # We use a suffixed op 'xformOp:orient:telemetry'.

                        # Check if it already exists to avoid "already exists in xformOpOrder"
                        # errors when calling AddOrientOp repeatedly.
                        rotate_op = None
                        ops = xformable.GetOrderedXformOps()
                        for op in ops:
                            if op.GetOpName() == "xformOp:orient:telemetry":
                                rotate_op = op
                                break

                        if not rotate_op:
                            # Add it (this appends to xformOpOrder by default)
                            # Note: addToXformOpOrder is not supported in AddOrientOp in this
                            # version
                            rotate_op = xformable.AddOrientOp(
                                UsdGeom.XformOp.PrecisionFloat, "telemetry"
                            )

                            # Manually reorder to ensure it's BEFORE scale
                            # Standard order: [Translate, Rotate, Scale]
                            # We want: [Translate, Rotate, Telemetry, Scale]

                            current_order = xformable.GetXformOpOrderAttr().Get()
                            if current_order:
                                current_order = list(current_order)
                                tele_op_name = rotate_op.GetOpName()

                                # Remove if present (it should be at the end)
                                # ... (rest of reordering logic)
                                if tele_op_name in current_order:
                                    current_order.remove(tele_op_name)

                                # Find scale op
                                scale_idx = -1
                                for i, op_name in enumerate(current_order):
                                    if "scale" in op_name.lower():
                                        scale_idx = i
                                        break

                                if scale_idx != -1:
                                    # Insert before scale
                                    current_order.insert(scale_idx, tele_op_name)
                                else:
                                    # No scale, just append
                                    current_order.append(tele_op_name)

                                xformable.GetXformOpOrderAttr().Set(current_order)

                        # Set the value
                        if rotate_op.GetOpType() == UsdGeom.XformOp.TypeOrient:
                            if self._latest_data_type == "euler":
                                try:
                                    # Convert Euler (deg) to Quat
                                    # Input Data Assumed: [Roll, Pitch, Heading]
                                    r_deg = float(q_data[0]) + self._offset_roll
                                    p_deg = float(q_data[1]) + self._offset_pitch
                                    h_deg = float(q_data[2]) + self._offset_heading

                                    # Map to USD Axes (Y-Up, Right-Handed)
                                    # Yaw (Heading) -> Y Axis (0, 1, 0)
                                    # Pitch         -> X Axis (1, 0, 0)
                                    # Roll          -> Z Axis (0, 0, 1)

                                    # Fix "Backwards" swimming: Add 180 to Heading
                                    # (Shark model likely faces -Z, but data might be +Y)
                                    h_deg += 180.0

                                    rot_roll = Gf.Rotation(Gf.Vec3d(0, 0, 1), r_deg)
                                    rot_pitch = Gf.Rotation(Gf.Vec3d(1, 0, 0), p_deg)
                                    rot_yaw = Gf.Rotation(Gf.Vec3d(0, 1, 0), h_deg)

                                    # Composition order: Yaw * Pitch * Roll (Standard Euler)
                                    rot = rot_yaw * rot_pitch * rot_roll
                                    q = rot.GetQuat()

                                    # Extract components safely
                                    # Gf.Quatd -> Gf.Quatf
                                    real = float(q.GetReal())
                                    imag = q.GetImaginary()
                                    qi, qj, qk = float(imag[0]), float(imag[1]), float(imag[2])

                                    rotate_op.Set(Gf.Quatf(real, qi, qj, qk))
                                except Exception as math_err:
                                    print(f"[whoimpg.biologger] Math Error: {math_err}")

                            else:
                                # Already Quat
                                try:
                                    # Create offset rotation from UI sliders (Euler -> Quat)
                                    rot_roll = Gf.Rotation(Gf.Vec3d(0, 0, 1), self._offset_roll)
                                    rot_pitch = Gf.Rotation(Gf.Vec3d(1, 0, 0), self._offset_pitch)
                                    rot_yaw = Gf.Rotation(Gf.Vec3d(0, 1, 0), self._offset_heading)

                                    # Compose offsets
                                    offset_rot = rot_yaw * rot_pitch * rot_roll
                                    offset_q = offset_rot.GetQuat()

                                    # Incoming Quat
                                    input_q = Gf.Quatd(q_data[0], q_data[1], q_data[2], q_data[3])

                                    # Combine: Apply offset to input
                                    final_q = input_q * offset_q

                                    real = float(final_q.GetReal())
                                    imag = final_q.GetImaginary()
                                    qi, qj, qk = float(imag[0]), float(imag[1]), float(imag[2])

                                    rotate_op.Set(Gf.Quatf(real, qi, qj, qk))
                                except Exception:
                                    # Fallback
                                    rotate_op.Set(
                                        Gf.Quatf(q_data[0], q_data[1], q_data[2], q_data[3])
                                    )

                        elif rotate_op.GetOpType() == UsdGeom.XformOp.TypeRotateXYZ:
                            if self._latest_data_type == "euler":
                                # USD RotateXYZ applies X, then Y, then Z.
                                # Assume direct mapping: X=Roll, Y=Pitch, Z=Heading.
                                rotate_op.Set(
                                    Gf.Vec3f(
                                        q_data[0] + self._offset_roll,
                                        q_data[1] + self._offset_pitch,
                                        q_data[2] + self._offset_heading,
                                    )
                                )
                            else:
                                # Convert Quat to Euler
                                q = Gf.Quatd(q_data[0], q_data[1], q_data[2], q_data[3])

                                # Apply offsets
                                rot_roll = Gf.Rotation(Gf.Vec3d(0, 0, 1), self._offset_roll)
                                rot_pitch = Gf.Rotation(Gf.Vec3d(1, 0, 0), self._offset_pitch)
                                rot_yaw = Gf.Rotation(Gf.Vec3d(0, 1, 0), self._offset_heading)
                                offset_rot = rot_yaw * rot_pitch * rot_roll

                                final_rot = Gf.Rotation(q) * offset_rot

                                euler = final_rot.Decompose(
                                    Gf.Vec3d.XAxis(), Gf.Vec3d.YAxis(), Gf.Vec3d.ZAxis()
                                )
                                rotate_op.Set(
                                    Gf.Vec3f(float(euler[0]), float(euler[1]), float(euler[2]))
                                )

                    # --- Follow Camera Update ---
                    # ALWAYS update camera if enabled, regardless of new data
                    if (
                        hasattr(self, "_follow_mode_checkbox")
                        and self._follow_mode_checkbox.model.get_value_as_bool()
                    ):
                        self._update_follow_camera(stage, prim)

                    # --- Trail Update ---
                    # Update trail points always (so we don't have gaps when toggled off)
                    # Visibility is handled by the checkbox callback
                    if hasattr(self, "_trail_checkbox"):
                        self._update_trail(stage, prim)

        except Exception as e:
            # Prevent spamming errors
            if not hasattr(self, "_update_error_shown"):
                print(f"[whoimpg.biologger] Error updating prim: {e}")
                self._update_error_shown = True

    def _on_follow_mode_changed(self, model: ui.AbstractValueModel) -> None:
        enabled = model.get_value_as_bool()
        print(f"[whoimpg.biologger] Follow mode changed: {enabled}")

        if enabled:
            # Store current camera to restore later
            self._previous_camera_path = omni.kit.viewport.utility.get_active_viewport_camera_path()

            # Create follow camera if needed
            self._ensure_follow_camera()

            # Switch to follow camera
            self._set_active_camera("/World/FollowCamera")

            # Subscribe to input events for orbit control
            if not self._input_sub_id:
                # Note: DEFAULT_SUBSCRIPTION_ORDER might be missing in some Kit versions.
                # Using a very low number (high priority) to consume events before the Viewport.
                self._input_sub_id = self._input.subscribe_to_input_events(
                    self._on_input_event,
                    order=-1000,
                )
        else:
            # Unsubscribe from input events
            if self._input_sub_id:
                self._input.unsubscribe_to_input_events(self._input_sub_id)
                self._input_sub_id = None

            # Restore previous camera
            path = "/OmniverseKit_Persp"
            if hasattr(self, "_previous_camera_path") and self._previous_camera_path:
                path = self._previous_camera_path

            self._set_active_camera(path)

    def _on_input_event(self, event: carb.input.InputEvent) -> bool:
        """Handle input for camera orbit (Keyboard Only - WASD + Arrows)"""
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
                self._cam_azimuth -= sensitivity
                return True
            elif is_key(key, ["D", "KEY_D"]):
                self._cam_azimuth += sensitivity
                return True

            # Elevation (Orbit Up/Down) - WASD Only
            # User Requirement: "needs to allow us to position the camera directly
            # above or below" so we will clamp to -90/90.
            elif is_key(key, ["W", "KEY_W"]):
                self._cam_elevation += sensitivity
                return True
            elif is_key(key, ["S", "KEY_S"]):
                self._cam_elevation -= sensitivity
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
                return True
            elif is_key(key, ["DOWN", "DOWN_ARROW", "KEY_DOWN", "MINUS", "KEY_MINUS"]):
                if not hasattr(self, "_cam_distance"):
                    self._cam_distance = 1500.0
                self._cam_distance += 100.0  # Zoom Out (Further)
                self._cam_distance = max(100.0, min(5000.0, self._cam_distance))
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

            # Add xform ops
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

    def _update_trail(self, stage: Usd.Stage, animal_prim: Usd.Prim) -> None:
        t0 = time.perf_counter()

        # Get current position
        xformable = UsdGeom.Xformable(animal_prim)

        # We want the world position of the animal
        # Note: ComputeLocalToWorldTransform returns Matrix4d
        world_transform = xformable.ComputeLocalToWorldTransform(Usd.TimeCode.Default())
        translation = world_transform.ExtractTranslation()

        # Convert to Gf.Vec3f for array
        current_pos = Gf.Vec3f(float(translation[0]), float(translation[1]), float(translation[2]))

        # Optimization: Only add point if moved significantly (> 5cm)
        if self._trail_points:
            last_pos = self._trail_points[-1]
            dist_sq = (
                (current_pos[0] - last_pos[0]) ** 2
                + (current_pos[1] - last_pos[1]) ** 2
                + (current_pos[2] - last_pos[2]) ** 2
            )
            if dist_sq < 25.0:  # 5cm squared = 25
                return

        self._trail_points.append(current_pos)

        # Get or Create Trail Prim
        trail_prim = stage.GetPrimAtPath(self._trail_prim_path)
        curves = None

        if not trail_prim.IsValid():
            curves = UsdGeom.BasisCurves.Define(stage, self._trail_prim_path)
            curves.CreateTypeAttr(UsdGeom.Tokens.linear)  # Linear for connected lines

            # Set Color (Black)
            # CreateDisplayColorAttr takes a Vt.Vec3fArray (list of colors)
            curves.CreateDisplayColorAttr(Vt.Vec3fArray([Gf.Vec3f(0.0, 0.0, 0.0)]))

            # Set Width
            curves.CreateWidthsAttr(Vt.FloatArray([5.0]))  # 5cm thick
            curves.SetWidthsInterpolation(UsdGeom.Tokens.constant)
        else:
            curves = UsdGeom.BasisCurves(trail_prim)

        if curves:
            # Update Points
            curves.GetPointsAttr().Set(Vt.Vec3fArray(self._trail_points))

            # Update Vertex Counts (One single curve containing all points)
            curves.GetCurveVertexCountsAttr().Set(Vt.IntArray([len(self._trail_points)]))

        t1 = time.perf_counter()
        self._last_trail_update_ms = (t1 - t0) * 1000.0

    def _update_follow_camera(self, stage: Usd.Stage, target_prim: Usd.Prim) -> None:
        camera_prim = stage.GetPrimAtPath("/World/FollowCamera")
        if not camera_prim.IsValid():
            return

        # Get target transform
        target_xform = UsdGeom.Xformable(target_prim)
        target_mat = target_xform.ComputeLocalToWorldTransform(Usd.TimeCode.Default())

        # Extract translation and rotation
        target_trans = target_mat.ExtractTranslation()
        target_rot = target_mat.ExtractRotation()  # Gf.Rotation

        # --- Stable Follow Logic ---
        # Calculate offset in world space based on shark's heading (Yaw) only.
        # This prevents the camera from rolling/pitching with the shark ("geosynchronous orbit").

        # 1. Get Forward Vector (assuming -Z is forward for the asset)
        forward_dir = target_rot.TransformDir(Gf.Vec3d(0, 0, -1))

        # 2. Project to horizontal plane (XZ) to ignore pitch/roll
        flat_forward = Gf.Vec3d(forward_dir[0], 0, forward_dir[2])

        # Handle vertical case (gimbal lock prevention)
        if flat_forward.GetLength() < 0.1:
            # Shark is vertical, use previous forward or default -Z
            if hasattr(self, "_last_flat_forward") and self._last_flat_forward:
                flat_forward = self._last_flat_forward
            else:
                flat_forward = Gf.Vec3d(0, 0, -1)
        else:
            flat_forward.Normalize()
            self._last_flat_forward = flat_forward

        # 3. Calculate Target Position using Spherical Coordinates (Orbit)
        # Base Basis:
        # Forward = flat_forward
        # Up = (0,1,0)
        # Right = Forward x Up

        # Get distance from internal state
        if not hasattr(self, "_cam_distance"):
            self._cam_distance = 1500.0
        follow_dist = self._cam_distance

        # Calculate Orbit Rotation
        # Azimuth rotates around Up axis
        # Elevation rotates around Right axis
        # We start from "Behind" (-Forward)

        # Create rotation for Azimuth (around World Y)
        # Note: We add the shark's heading (implied by flat_forward) to the manual azimuth
        # But flat_forward is a vector, not an angle.
        # Let's construct a basis matrix from flat_forward.
        basis_z = -flat_forward  # Z points BACKWARDS in this basis (towards camera default)
        basis_y = Gf.Vec3d(0, 1, 0)
        basis_x = Gf.Cross(basis_y, basis_z).GetNormalized()

        # Apply Manual Orbit
        # Convert degrees to radians
        az_rad = self._cam_azimuth * (3.14159 / 180.0)
        el_rad = self._cam_elevation * (3.14159 / 180.0)

        # Spherical to Cartesian (relative to basis)
        # x = dist * cos(el) * sin(az)
        # y = dist * sin(el)
        # z = dist * cos(el) * cos(az)
        import math

        rel_x = follow_dist * math.cos(el_rad) * math.sin(az_rad)
        rel_y = follow_dist * math.sin(el_rad)
        rel_z = follow_dist * math.cos(el_rad) * math.cos(az_rad)

        # Transform relative offset to World Space using basis
        # Offset = (rel_x * basis_x) + (rel_y * basis_y) + (rel_z * basis_z)
        offset = (basis_x * rel_x) + (basis_y * rel_y) + (basis_z * rel_z)

        target_cam_pos = target_trans + offset

        # 4. Smoothing / Damping
        if not hasattr(self, "_cam_pos_smoothed"):
            self._cam_pos_smoothed = target_cam_pos
        else:
            # Lerp factor (0.05 = very smooth, 0.2 = responsive)
            alpha = 0.02  # Default very smooth
            if hasattr(self, "_camera_damping_field"):
                alpha = self._camera_damping_field.model.get_value_as_float()

            self._cam_pos_smoothed = (self._cam_pos_smoothed * (1.0 - alpha)) + (
                target_cam_pos * alpha
            )

        cam_pos = self._cam_pos_smoothed

        # Update Camera Transform
        cam_xform = UsdGeom.Xformable(camera_prim)

        # Find translate and rotate ops
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

        # Make camera look at shark
        # User Requirement: "Gimbal-like logic that keeps the camera horizontal
        # so we dont end up inverted"
        # Solution: Use strict World Up (0,1,0) for the LookAt matrix.
        # This prevents the camera from banking/rolling, effectively keeping
        # the horizon level.
        # This handles the "directly above/below" cases gracefully via Gf.Matrix4d
        # behavior (singularities may flick, but are generally stable).
        look_at_matrix = Gf.Matrix4d().SetLookAt(cam_pos, target_trans, Gf.Vec3d(0, 1, 0))

        # Extract rotation from look-at matrix
        # Note: SetLookAt creates a view matrix (inverse of camera transform).
        # We need the camera transform.
        cam_matrix = look_at_matrix.GetInverse()

        # Extract rotation (Euler XYZ)
        rot = cam_matrix.ExtractRotation()
        euler = rot.Decompose(Gf.Vec3d.XAxis(), Gf.Vec3d.YAxis(), Gf.Vec3d.ZAxis())

        rotate_op.Set(Gf.Vec3f(float(euler[0]), float(euler[1]), float(euler[2])))

    def _restart_listener(self) -> None:
        """Restarts the ZMQ listener with new settings"""
        print("[whoimpg.biologger] Restarting listener...")
        if hasattr(self, "_stop_event"):
            self._stop_event.set()

        if hasattr(self, "_thread") and self._thread.is_alive():
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
        if hasattr(self, "_thread") and self._thread.is_alive():
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
        self._thread: threading.Thread = threading.Thread(
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
                # Polling for data
                # We use recv_string to handle topic-prefixed messages
                # Format: "topic json_payload"
                msg_str = socket.recv_string(flags=zmq.NOBLOCK)
                # print(f"[whoimpg.biologger] DEBUG: Recv: {msg_str[:100]}")

                # Split topic and payload
                parts = msg_str.split(" ", 1)
                if len(parts) == 2:
                    _topic, json_str = parts
                    try:
                        message = json.loads(json_str)
                    except json.JSONDecodeError:
                        # Fallback: maybe it was just JSON without topic?
                        try:
                            message = json.loads(msg_str)
                        except json.JSONDecodeError:
                            continue
                else:
                    # Try parsing the whole string as JSON
                    try:
                        message = json.loads(msg_str)
                    except json.JSONDecodeError:
                        continue

                self._packet_count += 1
                self._packets_since_last_update += 1

                if first_msg:
                    print(f"[whoimpg.biologger] First ZMQ message received: {message}")
                    first_msg = False

                # Extract orientation (Euler or Quaternion)
                # Expected format: {"rotation": {"euler_deg": [r, p, h]}}
                # OR {"transform": {"quat": [w, x, y, z]}}
                if isinstance(message, dict):
                    if "rotation" in message:
                        rot = message["rotation"]
                        if isinstance(rot, dict) and "euler_deg" in rot:
                            e_data = rot["euler_deg"]
                            if isinstance(e_data, list) and len(e_data) >= 3:
                                self._last_vector_str = (
                                    f"R:{e_data[0]:.1f} P:{e_data[1]:.1f} H:{e_data[2]:.1f}"
                                )
                                # Store for main thread update
                                # Reusing variable for now, will handle type check in update
                                self._latest_quat_data = e_data
                                self._latest_data_type = "euler"

                    elif "transform" in message:
                        transform = message["transform"]
                        if isinstance(transform, dict) and "quat" in transform:
                            q_data = transform["quat"]
                            if isinstance(q_data, list) and len(q_data) >= 4:
                                self._last_vector_str = (
                                    f"[{q_data[0]:.2f}, {q_data[1]:.2f}, "
                                    f"{q_data[2]:.2f}, {q_data[3]:.2f}]"
                                )

                                # Store for main thread update
                                self._latest_quat_data = q_data
                                self._latest_data_type = "quat"

                # Extract physics data
                if isinstance(message, dict):
                    if "physics" in message:
                        self._latest_physics_data = message["physics"]
                    if "timestamp" in message:
                        self._latest_timestamp = float(message["timestamp"])

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
        # 5 frame delay to allow Layout
        for _ in range(5):
            await omni.kit.app.get_app().next_update_async()

        ctx = omni.usd.get_context()
        animal_type = self._settings.get("/biologger/animal")

        if ctx.get_stage_url():
            print(f"[whoimpg.biologger] Stage already loaded: {ctx.get_stage_url()}")
            if animal_type:
                await self._load_animal_asset(animal_type)
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
                    await self._load_animal_asset(animal_type)
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

    def on_shutdown(self) -> None:
        """Clean up the extension"""
        # --- WHOI Biologger Subscriber Cleanup ---
        if hasattr(self, "_stop_event"):
            self._stop_event.set()
        if hasattr(self, "_thread"):
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
