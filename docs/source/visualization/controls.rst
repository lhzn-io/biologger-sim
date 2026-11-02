Controls Cheat Sheet
====================

Every keyboard, mouse and gamepad control in the Biologger Simulator viewer, and the HTTP
routes an agent or script can use for the same actions. Keys act while the viewport has
focus. Two camera modes change what some inputs do: **Follow Mode** (the camera orbits
the active animal) and **Free Fly** (standard Omniverse navigation). ``K`` switches
between them.

Any Mode
--------

.. list-table::
   :header-rows: 1
   :widths: 30 22 18 30

   * - Action
     - Keyboard
     - Gamepad
     - Notes
   * - Toggle Follow Mode
     - ``K``
     - ``X``
     - Turning it on snaps the camera to the active animal.
   * - Previous / next animal
     - ``[`` / ``]``
     - ``LB`` / ``RB``
     - Cycles through every streamed animal.
   * - Select animal 1 to 5
     - ``1`` to ``5``
     -
     - Number keys or numpad, in stream order.
   * - Vertical exaggeration up / down
     - ``V`` / ``Shift+V``
     -
     - Steps through 1x, 2x, 3x, 5x and 10x. The current factor is shown in the HUD.
   * - Reset window layout
     - ``Ctrl+1``
     -
     - Restores the default panel layout.
   * - Quick save / quick load layout
     - ``Ctrl+7`` / ``Ctrl+8``
     -
     -
   * - Show the HUD
     -
     -
     - Window menu, Biologger HUD (no key).

Follow Mode
-----------

.. list-table::
   :header-rows: 1
   :widths: 30 22 18 30

   * - Action
     - Keyboard
     - Gamepad
     - Notes
   * - Orbit left / right
     - ``A`` / ``D`` or arrow keys
     - Left stick, horizontal
     - Right-click drag also orbits.
   * - Raise / lower the camera
     - ``W`` / ``S``
     - Right stick, vertical
     - Right-click drag also works. ``Invert Y`` in the HUD flips the stick.
   * - Zoom in / out
     - ``Up`` / ``Down``, ``=`` / ``-``
     - Left stick, vertical
     - The scroll wheel zooms too.
   * - Show / hide the Stage window
     - ``F5``
     -
     - Follow Mode only.
   * - Show / hide the Timeline window
     - ``F6``
     -
     - Follow Mode only.

Free Fly
--------

Standard Omniverse viewport navigation applies:

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Action
     - Input
   * - Fly
     - Hold right mouse button, then ``W`` ``A`` ``S`` ``D`` (``Q`` / ``E`` down / up)
   * - Look around
     - Right mouse button drag
   * - Orbit
     - ``Alt`` + left mouse button drag
   * - Pan
     - Middle mouse button drag
   * - Zoom
     - Scroll wheel
   * - Frame the selection
     - ``F``

Cycling animals in Free Fly frames the new animal without locking the camera to it.

Trail Width
-----------

The trail is drawn as a tube. In Follow Mode it is 5 cm wide, which suits close views of
the animal. Out of Follow Mode, with **Auto Trail Width** checked in the HUD (the
default), the width follows the camera's distance to the nearest point of the trail. It
stays about 4 pixels across, and changes only in steps (powers of two from 5 cm, up to
100 m) so the trail is not redrawn on every camera move. Setting a width by hand through
``/agent/trail`` turns the automatic width off until the box is checked again.

The trail averages position and ODBA over each tube width of track. A wide overview trail
therefore shows the mean path and mean effort; detail finer than the tube needs a closer
view.

Vertical Exaggeration
---------------------

Exaggeration stretches the scene vertically about sea level: the seafloor, the position
uncertainty band, the trails and the animals' depths. The animal models keep their true
shape and orientation. The seafloor's baked hillshade comes from the true slopes, while
the live lighting follows the stretched geometry. At any factor above 1x, dive angles and
slopes look steeper than they are; check the factor in the HUD before reading angles off
the view.

Agent and Script Routes
-----------------------

The same controls are available over HTTP on the viewer's services port (``8011``, bound
to ``127.0.0.1``):

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Route
     - Effect
   * - ``POST /agent/follow {"enabled": true}``
     - Follow Mode on or off.
   * - ``POST /agent/animal {"eid": 0}``
     - Make an animal the active one.
   * - ``POST /agent/exaggeration {"factor": 3}``
     - Vertical exaggeration, 1 to 20.
   * - ``POST /agent/trail {"width_cm": 3000}``
     - Fixed trail width (turns the automatic width off).
   * - ``POST /agent/trail {"auto": true}``
     - Return to the automatic trail width.
   * - ``POST /agent/view {"eye": [...], "target": [...]}``
     - Place the camera (scene centimetres, Y up).
   * - ``POST /agent/capture {"name": "shot.png"}``
     - Save the viewport to the capture folder.

The full route list is in the ``agent_control`` module docstring.
