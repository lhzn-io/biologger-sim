# Copyright (c) 2026 Long Horizon Observatory
# Licensed under the Apache License, Version 2.0. See LICENSE file for details.

"""The biologger HUD: telemetry and controls in one column over the viewport.

A translucent column pinned to the viewport's top left, in the viewport window's own overlay
frame (ViewportWindow.get_frame), after the slop-fest HUD:

    telemetry panel  the camera view and frame rate in a header that collapses the panel to
                     a one-line summary, then the ANIMAL, MOTION and STREAM readouts
    controls panel   pinned below, collapsed to its header at first: VIEW, SCENE, PLAYBACK
                     and a collapsed ADVANCED section

The frame has a build function, every label's text and style are cached, and the controls
bind to models the extension keeps (Control), so Kit can rebuild the column at any time (an
extension reload, a viewport rebuild, a collapse) without losing what it shows or the state
of a control. Mouse events pass through the readouts, so camera drags work over them; the
headers and the controls take clicks.
"""

from __future__ import annotations

import collections
import time
from collections.abc import Callable
from typing import Any

import carb
import omni.ui as ui

PANEL_WIDTH = 340
PANEL_LEFT = 16
PANEL_TOP = 16
PANEL_GAP = 6
PAD = 10
PANEL_BACKGROUND = 0x5A000000  # ABGR, about 35 percent black
TITLE = {"font_size": 13, "color": 0xFF999999}
TEXT = {"font_size": 14, "color": 0xFFDDDDDD}
DIM = {"font_size": 13, "color": 0xFFAAAAAA}
WARN = {"font_size": 14, "color": 0xFF3468EB}  # below the seafloor
RULE = {"background_color": 0x50FFFFFF}
CHEVRON = 0xFFCCCCCC
CHECKBOX = {"background_color": 0xFF404040, "color": 0xFFDDDDDD, "border_radius": 2}
BUTTON = {"background_color": 0xFF3A3A3A, "border_radius": 3, "font_size": 13}
# View line colours per camera mode (ABGR), matching vantagekit's badge
VIEW_COLORS = {"free": 0xFFBBBBBB, "orbit": 0xFFFFB050, "chase": 0xFF40D0FF, "pov": 0xFF60FF90}
NM = {"opaque_for_mouse_events": False}


class Control:
    """A control's state, kept by the extension across HUD rebuilds: `model` is the omni.ui
    model the drawn widget binds to (same interface as a widget's .model)."""

    def __init__(self, model: Any, enabled: bool = True) -> None:
        self.model = model
        self.enabled = enabled


class ButtonProxy:
    """Stands in for a button whose text and style the extension sets (the mode button):
    setting .text or .style updates the cached state and the drawn button."""

    def __init__(self, hud: BiologgerHUD, name: str) -> None:
        self._hud = hud
        self._name = name

    @property
    def text(self) -> str:
        return str(self._hud._texts[self._name][0])

    @text.setter
    def text(self, value: str) -> None:
        self._hud.set(self._name, value)

    @property
    def style(self) -> dict:
        return dict(self._hud._texts[self._name][1])

    @style.setter
    def style(self, value: dict) -> None:
        self._hud.set(self._name, self.text, {**BUTTON, **value})


def _section(title: str) -> None:
    ui.Spacer(height=3, **NM)
    ui.Rectangle(height=1, style=RULE, **NM)
    ui.Spacer(height=2, **NM)
    ui.Label(title, height=0, style=TITLE, **NM)


def _header(title_fn: Callable[[], None], collapsed: bool, on_toggle: Callable[[], None]) -> None:
    """A clickable header row: a chevron (right when collapsed, down when open), then
    whatever title_fn draws. Clicking anywhere on the row calls on_toggle."""

    def pressed(x: float, y: float, button: int, mods: int) -> None:
        if button == 0:
            on_toggle()

    with ui.ZStack(height=0, mouse_pressed_fn=pressed, opaque_for_mouse_events=True):
        ui.Rectangle(style={"background_color": 0x01000000})  # takes the click
        with ui.HStack(height=0, spacing=6):
            with ui.VStack(width=12):
                ui.Spacer()
                ui.Triangle(
                    width=9 if collapsed else 11,
                    height=11 if collapsed else 9,
                    alignment=(
                        ui.Alignment.RIGHT_CENTER if collapsed else ui.Alignment.CENTER_BOTTOM
                    ),
                    style={"background_color": CHEVRON},
                )
                ui.Spacer()
            title_fn()


class BiologgerHUD:
    """The HUD column. `ext` is the extension: the controls read its Control objects and
    call its methods (set_follow, step_exaggeration, ...)."""

    def __init__(self, ext: Any, frame_name: str = "whoimpg.biologger.hud") -> None:
        self._ext = ext
        self._frame_name = frame_name
        self._frame: Any = None
        self._attach_retry_t = 0.0
        self._widgets: dict[str, Any] = {}
        # name -> [text, style]; the build function draws from this
        self._texts: dict[str, list] = {
            "view": ["FREE", {"font_size": 20, "color": VIEW_COLORS["free"]}],
            "view_hint": ["K / X: attach", {"font_size": 13, "color": 0xFFCCCCCC}],
            "fps": ["-- fps", {"font_size": 15, "color": 0xFFAAAAAA}],
            "summary": ["Waiting for the stream", TEXT],
            "animal": ["Animal: --", TEXT],
            "time": ["Time: --", DIM],
            "depth": ["Depth --   Seafloor --", TEXT],
            "speed": ["Speed --", TEXT],
            "attitude": ["Roll --   Pitch --   Heading --", TEXT],
            "effort": ["ODBA --   VeDBA --", TEXT],
            "path": ["Path pitch --   heading --", DIM],
            "aoa": ["Attack angle --   Sideslip --", DIM],
            "stream": ["Disconnected", DIM],
            "mode": ["MODE: LIVE", {**BUTTON, "background_color": 0xFF00AA00}],
            "exag": ["Exaggeration 1x", TEXT],
        }
        self.visible = True
        self.collapsed = False
        self.controls_collapsed = True
        self.advanced_collapsed = True
        self._frame_times: collections.deque[float] = collections.deque(maxlen=240)
        self._fps_t = 0.0
        self.mode_button = ButtonProxy(self, "mode")
        self._attach()

    # frame --------------------------------------------------------------------------
    def _attach(self) -> None:
        """Attach to the viewport's overlay frame. The viewport window may not exist yet at
        startup, so tick() retries this about once a second until it does."""
        if self._frame is not None:
            return
        now = time.monotonic()
        if now < self._attach_retry_t:
            return
        self._attach_retry_t = now + 1.0
        try:
            from omni.kit.viewport.utility import get_active_viewport_window

            win = get_active_viewport_window()
            self._frame = win.get_frame(self._frame_name) if win is not None else None
        except Exception as e:
            carb.log_warn(f"[whoimpg.biologger] HUD overlay unavailable: {e}")
        if self._frame is not None:
            self._frame.set_build_fn(self._build)
            self._frame.rebuild()

    def rebuild(self) -> None:
        self._attach()
        if self._frame is not None:
            self._frame.rebuild()

    def destroy(self) -> None:
        if self._frame is not None:
            self._frame.set_build_fn(lambda: None)  # a later rebuild must not call into us
            self._frame.clear()
        self._frame = None
        self._widgets = {}

    def toggle(self) -> None:
        self.visible = not self.visible
        self.rebuild()

    def _toggle(self, attr: str) -> None:
        setattr(self, attr, not getattr(self, attr))
        self.rebuild()

    # layout -------------------------------------------------------------------------
    def _label(self, name: str, **kw: Any) -> None:
        text, style = self._texts[name]
        self._widgets[name] = ui.Label(text, height=0, style=style, **NM, **kw)

    def _build(self) -> None:
        self._widgets = {}
        if not self.visible:
            return
        with ui.VStack(**NM):
            ui.Spacer(height=PANEL_TOP, **NM)
            with ui.HStack(height=0, **NM):
                ui.Spacer(width=PANEL_LEFT, **NM)
                with ui.VStack(width=PANEL_WIDTH, height=0, spacing=PANEL_GAP, **NM):
                    self._panel(self._build_telemetry)
                    self._panel(self._build_controls)
                ui.Spacer(**NM)
            ui.Spacer(**NM)

    def _panel(self, body: Callable[[], None]) -> None:
        with ui.ZStack(height=0, **NM):
            ui.Rectangle(style={"background_color": PANEL_BACKGROUND, "border_radius": 5})
            with ui.HStack(height=0, **NM):
                ui.Spacer(width=PAD, **NM)
                with ui.VStack(height=0, spacing=1, **NM):
                    ui.Spacer(height=5, **NM)
                    try:
                        body()
                    except Exception as e:
                        carb.log_warn(f"[whoimpg.biologger] HUD panel failed to build: {e}")
                    ui.Spacer(height=6, **NM)
                ui.Spacer(width=PAD, **NM)

    def _build_telemetry(self) -> None:
        def title() -> None:
            with ui.VStack(height=0, **NM):
                with ui.HStack(height=0, **NM):
                    self._label("view")
                    ui.Spacer(**NM)
                    self._label("fps", width=0)
                self._label("view_hint", word_wrap=True)

        _header(title, self.collapsed, lambda: self._toggle("collapsed"))
        if self.collapsed:
            ui.Spacer(height=2, **NM)
            self._label("summary")
            return
        _section("ANIMAL")
        for name in ("animal", "time", "depth", "speed", "attitude", "effort"):
            self._label(name)
        _section("MOTION")
        for name in ("path", "aoa"):
            self._label(name)
        _section("STREAM")
        self._label("stream")

    def _check(self, control: Control, text: str, tooltip: str = "") -> None:
        with ui.HStack(height=20, spacing=6):
            with ui.VStack(width=14):
                ui.Spacer()
                cb = ui.CheckBox(
                    model=control.model, width=14, height=14, style=CHECKBOX, tooltip=tooltip
                )
                cb.enabled = control.enabled
                ui.Spacer()
            ui.Label(text, style=TEXT, tooltip=tooltip)

    def _build_controls(self) -> None:
        ext = self._ext

        def title() -> None:
            ui.Label("CONTROLS", height=0, style={"font_size": 14, "color": 0xFFCCCCCC})

        _header(title, self.controls_collapsed, lambda: self._toggle("controls_collapsed"))
        if self.controls_collapsed:
            return
        _section("VIEW")
        self._check(ext._follow_mode_checkbox, "Follow animal (K)")
        self._check(ext._trail_checkbox, "Show trail")
        self._check(ext._trail_auto_checkbox, "Auto trail width (free camera)")
        self._check(ext._uncertainty_checkbox, "Position uncertainty band")
        with ui.HStack(height=22, spacing=6):
            self._label("exag")
            ui.Spacer()
            ui.Button("-", width=26, style=BUTTON, clicked_fn=lambda: ext.step_exaggeration(-1))
            ui.Button("+", width=26, style=BUTTON, clicked_fn=lambda: ext.step_exaggeration(1))
        _section("SCENE")
        self._check(ext._detail_checkbox, "Seafloor detail texture (T)")
        self._check(ext._dem_stream_checkbox, "Stream DEM tiles")
        _section("PLAYBACK")
        text, style = self._texts["mode"]
        with ui.HStack(height=26, spacing=6):
            self._widgets["mode"] = ui.Button(
                text, style=style, clicked_fn=ext._on_mode_toggle_clicked
            )
            ui.Button("Timeline (F6)", style=BUTTON, clicked_fn=ext._show_timeline_window)
        with ui.HStack(height=26, spacing=6):
            ui.Button(
                "Clear tracks",
                style={**BUTTON, "background_color": 0xFF4444AA},
                clicked_fn=ext._clear_all_entities,
                tooltip="Removes animals and lines, leaves bathymetry.",
            )
            ui.Button(
                "Reset scene",
                style={**BUTTON, "background_color": 0xFF222266},
                clicked_fn=ext._reset_full_scene,
                tooltip="Removes everything and re-draws bathymetry if enabled.",
            )
        ui.Spacer(height=3)
        _header(
            lambda: ui.Label("ADVANCED", height=0, style=TITLE),
            self.advanced_collapsed,
            lambda: self._toggle("advanced_collapsed"),
        )
        if self.advanced_collapsed:
            return
        with ui.HStack(height=22, spacing=6):
            ui.Label("ZMQ", width=40, style=DIM)
            ui.StringField(model=ext._host_field.model)
            ui.IntField(model=ext._port_field.model, width=60)
            ui.Button("Reconnect", width=80, style=BUTTON, clicked_fn=ext._restart_listener)
        for name, control in (
            ("Roll offset", ext._offset_roll_slider),
            ("Pitch offset", ext._offset_pitch_slider),
            ("Heading offset", ext._offset_heading_slider),
        ):
            with ui.HStack(height=22, spacing=6):
                ui.Label(name, width=96, style=DIM)
                # A drag field, not a slider: the slider draws its value across the handle
                ui.FloatDrag(model=control.model, min=-180, max=180, step=0.5)
        ui.Button("Reset orientation", height=24, style=BUTTON, clicked_fn=ext._reset_orientation)
        self._check(ext._safe_mode_checkbox, "Safe mode (live only, no history)")
        self._check(ext._debug_vec_checkbox, "Debug vectors")

    # updates ------------------------------------------------------------------------
    def set(self, name: str, text: str, style: dict | None = None) -> None:
        """Set a readout's text (and style); cached, so a rebuild draws it again."""
        entry = self._texts[name]
        if entry[0] == text and (style is None or entry[1] == style):
            return
        entry[0] = text
        if style is not None:
            entry[1] = style
        w = self._widgets.get(name)
        if w is not None:
            w.text = text
            if style is not None:
                w.style = style

    def tick(self) -> None:
        """Once per frame: attach if needed, and the frame rate in the header (over at least
        the last 10 frames and 1 s, refreshed twice a second)."""
        self._attach()
        now = time.perf_counter()
        ft = self._frame_times
        ft.append(now)
        if now - self._fps_t < 0.5 or len(ft) < 10:
            return
        self._fps_t = now
        times = list(ft)
        i = len(times) - 10
        while i > 0 and now - times[i] < 1.0:
            i -= 1
        fps = (len(times) - 1 - i) / (now - times[i])
        color = 0xFF60E060 if fps >= 55 else (0xFF30B0FF if fps >= 25 else 0xFF4040FF)
        self.set("fps", f"{fps:.0f} fps", {"font_size": 15, "color": color})

    def update_view(self, mode: str, title: str, hint: str) -> None:
        """The camera view line: vantagekit ViewerControls.view_badge()."""
        self.set("view", title, {"font_size": 20, "color": VIEW_COLORS.get(mode, 0xFFFFFFFF)})
        self.set("view_hint", hint)
