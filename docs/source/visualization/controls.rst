Controls Cheat Sheet
====================

Every keyboard, mouse and gamepad control in the Biologger Simulator viewer, and the HTTP
routes an agent or script can use for the same actions. Keys act while the viewport has
focus. The camera is either **free** (standard Omniverse navigation) or **attached** to the
active animal, orbiting it: the camera keeps a fixed angle and distance on the animal and
moves with it, but does not turn with its heading. ``K`` attaches and frees it.

There is no chase view (a camera that turns with the animal's heading). A swordfish yaws
and rolls through each tail stroke, so a heading-locked camera would swing with every
stroke; the orbit view holds steady and shows the swimming motion instead.

The camera and its controls come from the shared ``lhzn.vantagekit`` Kit extension
(``lhzn-io/vantagekit``), which other lhzn viewers use too. The HUD's first lines name
the current view and its buttons.

Any Mode
--------

.. list-table::
   :header-rows: 1
   :widths: 30 22 18 30

   * - Action
     - Keyboard
     - Gamepad
     - Notes
   * - Attach the camera to the animal, or free it
     - ``K``
     - ``X``
     - The HUD's Follow Animal box does the same.
   * - Previous / next animal
     - ``[`` / ``]``
     - ``LB`` / ``RB``
     - Cycles through every streamed animal; an attached camera moves to the new one.
   * - Select animal 1 to 5
     - ``1`` to ``5``
     -
     - Number keys or numpad, in stream order.
   * - Vertical exaggeration up / down
     - ``V`` / ``Shift+V``
     -
     - Steps through 1x, 2x, 3x, 5x and 10x. The current factor is shown in the HUD.
   * - Seafloor detail texture on / off
     - ``T``
     -
     - Decorative; off by default.
   * - Show / hide the Stage window
     - ``F5``
     -
     -
   * - Show / hide the Timeline window
     - ``F6``
     -
     -
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

Attached Camera
---------------

.. list-table::
   :header-rows: 1
   :widths: 30 22 18 30

   * - Action
     - Keyboard / mouse
     - Gamepad
     - Notes
   * - Orbit around the animal
     - Left mouse drag
     - Right stick
     -
   * - Closer / farther
     - Scroll wheel
     - Left / right trigger
     - From 1 m to 5 km.
   * - Back to the default view behind the animal
     - ``Home``
     - ``A``
     - 15 m behind and 3 m above the animal, along its heading at that moment.

While attached, Kit's own navigation is locked on the camera, so right-drag and ``W``
``A`` ``S`` ``D`` do nothing until the camera is freed.

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
   * - Fly with a gamepad
     - Kit's native gamepad navigation (sticks)

``W`` ``A`` ``S`` ``D`` do nothing on their own in Free Fly: Kit moves the camera only while
the right mouse button is held. Fly speed is Kit's own camera speed setting, which suits
building-sized scenes; across a deployment tens of kilometres wide, fly mode is slow, and
orbiting (``Alt`` + left drag) and the scroll wheel cover distance faster.

Cycling animals in Free Fly selects the new animal without moving the camera; ``F`` frames
it, and ``K`` attaches to it.

Trail Width
-----------

The trail is drawn as a tube. While the camera is attached it is 5 cm wide, which suits
close views of the animal. With a free camera, with **Auto Trail Width** checked in the HUD (the
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
     - Orbit the active animal, or free the camera.
   * - ``POST /agent/camera {"mode": "orbit"}``
     - Set the view (``free`` or ``orbit``); ``{"home": true}`` returns behind
       the animal; ``{"orbit_deg": [30, 0, 1]}`` steps the orbit. ``GET /agent/camera``
       returns the rig's state.
   * - ``POST /agent/animal {"eid": 0}``
     - Make an animal the active one.
   * - ``POST /agent/exaggeration {"factor": 3}``
     - Vertical exaggeration, 1 to 20.
   * - ``POST /agent/trail {"width_cm": 3000}``
     - Fixed trail width (turns the automatic width off).
   * - ``POST /agent/trail {"auto": true}``
     - Return to the automatic trail width.
   * - ``GET /agent/animals``
     - Streamed animals, with samples received, gaps and an estimate of samples missing
       (a check that a fast replay arrived complete).
   * - ``POST /agent/layers {"uncertainty": false}``
     - Show or hide the position uncertainty band (the HUD's Show Position Uncertainty).
   * - ``POST /agent/time {"seconds": 3600}`` or ``{"deepest": true}``
     - Move the replay head (seconds from the session start), or to the active animal's
       deepest sample; returns its depth and scene position.
   * - ``POST /agent/view {"eye": [...], "target": [...]}``
     - Place the camera (scene centimetres, Y up); frees an attached camera first.
   * - ``POST /agent/capture {"name": "shot.png"}``
     - Save the viewport to the capture folder, without the selection outline
       (``"clean": false`` keeps it).

The full route list is in the ``agent_control`` module docstring.
