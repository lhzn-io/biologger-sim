# Copyright (c) 2018-2020, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#
# Portions Copyright (c) 2025 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.
#

import asyncio
import inspect
import json
import logging
import os
import platform
import subprocess
import sys
import threading
import time
import webbrowser
from pathlib import Path
from typing import Any

import carb
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
from pxr import Gf, UsdGeom

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

        # Add the reference
        references = prim.GetReferences()
        references.AddReference(full_asset_path)

        # Set default transform
        xform = UsdGeom.XformCommonAPI(prim)
        xform.SetRotate((-90, 0, 0))  # GLB usually needs -90 X rotation
        xform.SetScale((5000, 5000, 5000))  # Scale up the animal significantly (was 500)

        # Select the animal
        # We select the prim so the user can see it in the Stage tree
        omni.usd.get_context().get_selection().set_selected_prim_paths([prim_path], False)
        print(f"[whoimpg.biologger] Spawned {animal_type} from {full_asset_path}")

    def _setup_biologger_subscriber(self) -> None:
        print("[whoimpg.biologger] Initializing Subscriber...")

        # Initialize state
        self._packet_count = 0
        self._last_vector_str = "N/A"
        self._connection_status = "Disconnected"
        self._latest_quat_data: list[Any] | None = None  # Store latest data for main thread update
        self._latest_data_type: str = "quat"  # "quat" or "euler"
        self._latest_physics_data: dict[str, Any] | None = None

        # Throughput calculation
        self._packets_since_last_update = 0
        self._last_throughput_time = time.time()
        self._throughput_str = "0.0 pkts/s"

        # 1. Setup the UI Dashboard (Overlay style)
        # Using a small window in the top-left corner as a HUD
        self._window = ui.Window(
            "Biologger Data", width=300, height=250, dockPreference=ui.DockPreference.LEFT
        )
        with self._window.frame, ui.VStack(spacing=5):
            self._status_label = ui.Label("Status: Disconnected", style={"color": 0xFF888888})
            self._packet_label = ui.Label("Packets: 0")
            self._throughput_label = ui.Label("Throughput: 0.0 pkts/s")
            self._vector_label = ui.Label("Last Quat: N/A")
            self._physics_label = ui.Label("Physics: N/A")

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
            self._vector_label.text = f"Last Quat: {self._last_vector_str}"

            if self._latest_physics_data:
                p = self._latest_physics_data
                self._physics_label.text = (
                    f"D: {p.get('depth', 0):.1f}m | V: {p.get('velocity', 0):.1f}m/s\n"
                    f"ODBA: {p.get('odba', 0):.2f} | VeDBA: {p.get('vedba', 0):.2f}"
                )

        # Apply rotation in main thread using standard USD API
        if self._latest_quat_data:
            try:
                # Get the standard USD stage context
                usd_context = omni.usd.get_context()
                stage = usd_context.get_stage()

                if stage:
                    prim = stage.GetPrimAtPath("/World/Animal")
                    if prim.IsValid():
                        q_data = self._latest_quat_data

                        # Use UsdGeom.Xformable to handle transforms robustly
                        xformable = UsdGeom.Xformable(prim)

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
                                    # Order: ZYX (Yaw, Pitch, Roll)
                                    r_deg = float(q_data[0])
                                    p_deg = float(q_data[1])
                                    h_deg = float(q_data[2])

                                    # Use explicit vectors to avoid potential static method issues
                                    # Gf.Rotation(axis, angle_degrees)
                                    rot_x = Gf.Rotation(Gf.Vec3d(1, 0, 0), r_deg)
                                    rot_y = Gf.Rotation(Gf.Vec3d(0, 1, 0), p_deg)
                                    rot_z = Gf.Rotation(Gf.Vec3d(0, 0, 1), h_deg)

                                    # Composition order: Z * Y * X (intrinsic)
                                    rot = rot_z * rot_y * rot_x
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
                                rotate_op.Set(Gf.Quatf(q_data[0], q_data[1], q_data[2], q_data[3]))

                        elif rotate_op.GetOpType() == UsdGeom.XformOp.TypeRotateXYZ:
                            if self._latest_data_type == "euler":
                                # USD RotateXYZ applies X, then Y, then Z.
                                # Assume direct mapping: X=Roll, Y=Pitch, Z=Heading.
                                rotate_op.Set(Gf.Vec3f(q_data[0], q_data[1], q_data[2]))
                            else:
                                # Convert Quat to Euler
                                q = Gf.Quatd(q_data[0], q_data[1], q_data[2], q_data[3])
                                rotation = Gf.Rotation(q)
                                euler = rotation.Decompose(
                                    Gf.Vec3d.XAxis(), Gf.Vec3d.YAxis(), Gf.Vec3d.ZAxis()
                                )
                                rotate_op.Set(
                                    Gf.Vec3f(float(euler[0]), float(euler[1]), float(euler[2]))
                                )

            except Exception as e:
                # Prevent spamming errors
                if not hasattr(self, "_update_error_shown"):
                    print(f"[whoimpg.biologger] Error updating prim: {e}")
                    self._update_error_shown = True

    def _restart_listener(self) -> None:
        """Restarts the ZMQ listener with new settings"""
        print("[whoimpg.biologger] Restarting listener...")
        if hasattr(self, "_stop_event"):
            self._stop_event.set()

        if hasattr(self, "_thread") and self._thread.is_alive():
            self._thread.join(timeout=1.0)

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
                    topic, json_str = parts
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
                if isinstance(message, dict) and "physics" in message:
                    self._latest_physics_data = message["physics"]

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
