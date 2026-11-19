=========================
User Guide
=========================

This guide describes how to use the Biologger Simulation in NVIDIA Omniverse. The extension
is a digital twin environment for visualizing animal movement, sensor fusion accuracy and
behavioral patterns.

.. _coordinate-conventions:

Coordinate Systems & Conventions
--------------------------------

Typical oceanographic data and the 3D visualization environment use different coordinate
conventions. Readers from marine science, robotics or hydrography should keep the difference
in mind.

Marine Science Standard (NED)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Oceanographic data (for example, from biologging tags) usually follow the **NED
(North-East-Down)** convention:

*   **X**: North
*   **Y**: East
*   **Z**: Down (Depth)
*   **Heading**: Clockwise from North (0° = North, 90° = East)

Visualization Standard (USD Y-Up)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
NVIDIA Omniverse and the underlying USD (Universal Scene Description) format use a **Y-Up,
Right-Handed** convention:

*   **Y**: Up (Altitude)
*   **-Z**: Forward (North)
*   **X**: Right (East)
*   **Rotation**: Counterclockwise (Right-Hand Rule)

Automatic Conversion
~~~~~~~~~~~~~~~~~~~~
The ``biologger-sim`` extension re-projects the data automatically, so the visuals match the
physical motion:

1.  **Heading Negation**: The extension negates the clockwise compass heading (N→E→S→W) to
    match the counterclockwise rotation of USD's right-hand rule. A NED heading of +90°
    (East) becomes -90° in USD, which points the forward vector toward +X.

2.  **Euler-to-Quaternion Mapping**:

    *   Sensor **Pitch** (Nose Up/Down) → Rotation around **X-Axis**
    *   Sensor **Heading** (Compass) → Rotation around **Y-Axis** (negated)
    *   Sensor **Roll** (Bank Left/Right) → Rotation around **-Z-Axis**

3.  **Rotation Application Order**: Yaw (Heading) → Pitch → Roll, which matches standard
    aerospace and marine conventions.

.. _mesh-orientation:

Mesh Orientation & Transform Stack
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Animal mesh assets (GLB/USD) are typically authored with an arbitrary "up" direction. The
extension applies a **spawn rotation** that aligns the mesh with USD conventions before it
applies the telemetry rotations.

**Example: Shark GLB Asset**

The shark mesh is authored with its nose pointing along +Y (upward in its native coordinate
frame). To align the mesh with USD's -Z = Forward convention:

*   **Spawn Rotation**: ``(-90°, 180°, 0°)`` XYZ Euler
*   This maps the mesh's +Y nose to world -Z (North)

**Required: USD XformOp Order**

USD applies transform operations in their order in the ``xformOpOrder`` attribute. For
correct world-space heading rotation, the **telemetry orientation must be applied BEFORE the
spawn rotation** in the op list:

.. code-block:: text

    xformOpOrder = ["xformOp:translate", "xformOp:orient:telemetry", "xformOp:rotateXYZ", "xformOp:scale"]

This produces the transform: ``v_world = telemetry × spawn × v_local``

1. **Spawn** maps the mesh-local nose (+Y) to world -Z
2. **Telemetry** then rotates around the world Y-axis, which turns the -Z forward direction

.. warning::
    **Common Pitfall**: If the spawn rotation comes BEFORE telemetry in the op order,
    telemetry rotations are applied in **mesh-local space**. The mesh nose lies along the
    local Y-axis, so a Y-rotation (heading) would spin the mesh about its own nose and leave
    the heading direction unchanged.

.. warning::
    **For Asset Creators**: Orient your animal models to face **-Z** (Forward) in their bind
    pose, or document the required spawn rotation. An asset that faces +Z or +X will appear
    to "drift" sideways or backwards relative to the trajectory.

Features Overview
-----------------

The visualization toolkit includes:

*   **Real-time Telemetry HUD**: A heads-up display (HUD) of sensor metrics.
*   **Follow Camera**: The camera follows the animal, and you can orbit around it.
*   **Instant Replay (Time Travel)**: Pause and rewind live simulations without losing data.
*   **Infinite Track**: The full trajectory stays visible during scrubbing.
*   **Georeferenced Scene**: The track is anchored to its deployment fixes over a fused DEM,
    with the sun, sky and water of the deployment's place and date (see :doc:`scene`).
*   **Overview Tools**: Vertical exaggeration and a trail whose width follows the camera
    distance, for kilometer-scale views of a whole deployment (see :doc:`controls`).

Telemetry Display (HUD)
-----------------------

The heads-up display (HUD) overlays sensor data on the viewport, so you can check the
pipeline's output immediately.

*   **Header**: The camera view (FREE or ORBIT) and the frame rate.
*   **Clock**: Time since release, the record date and time (UTC), and the position.
*   **ANIMAL**: Depth, seafloor and clearance, speed, roll, pitch, heading, ODBA and VeDBA.
*   **MOTION**: Path pitch and heading, attack angle and sideslip.
*   **STREAM**: Connection, sample rate, and LIVE or REPLAY.

The Biologger HUD item in the Window menu turns the HUD on and off, for clean screenshots
or video recordings. The :doc:`controls` describes each part of the HUD.

Understanding Angle of Attack (AoA)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You may see a nonzero **Angle of Attack (AoA)** even when the animal appears to swim
straight. This value correctly represents the physics of the input data:

*   **AoA Definition**: The angle between the animal's **Orientation Vector** (where it is
    looking) and its **Movement Vector** (where it is going).
*   **The Decoupling Effect**:

    *   **Orientation (Red Vector)**: Derived from the **Accelerometer/Magnetometer**. If the
        animal pitches down by -30°, the model looks down.
    *   **Trajectory (Green Vector)**: Derived from **Speed** and **Depth Sensor**. Only the
        change in pressure (depth) drives the vertical component.

*   **Physical Interpretation**: An animal pitched down (-30°) at constant depth (zero
    vertical velocity) is "sliding" forward through the water. This sliding gives a 30° AoA.
    The AoA therefore shows real differences between body attitude and the direction the
    animal actually moves.

Camera & Navigation
-------------------

The viewer drives one camera, ``/World/PlayerCam``, through the shared ``lhzn.vantagekit``
extension. The camera starts free and can be attached to the active animal, which it then
orbits.

Input Map
~~~~~~~~~

The :doc:`controls` lists every key, mouse and gamepad control, including vertical
exaggeration and the adaptive trail width, and the matching HTTP routes.

Follow Mode
~~~~~~~~~~~

``K`` (gamepad ``X``) or the HUD's Follow animal box attaches the camera. When Follow Mode is
**Active**:

*   The camera tracks the selected animal automatically.
*   **Orbit**: You can rotate around the animal to view it from any angle.
*   **Zoom**: The scroll wheel or the gamepad triggers set the orbit distance, from 1 m to
    5 km.
*   **Cycling animals**: The camera moves to the new animal.

Free Fly Mode (Default)
~~~~~~~~~~~~~~~~~~~~~~~

When Follow Mode is **Inactive**:

*   Standard Omniverse navigation applies.
*   You can fly through the scene to inspect the environment. Hold the right mouse button to
    fly with ``W`` ``A`` ``S`` ``D``. The keys alone do not move the camera.
*   **Cycling animals**: In this mode, cycling animals selects the new animal without moving
    the camera. ``F`` then frames the animal, and ``K`` attaches the camera to it.

Time Control & Analysis (Instant Replay)
----------------------------------------

The **Instant Replay** system lets you pause, rewind and scrub through the visualization in
real time. It separates the **View Time** from the **Simulation Time**.

Simulation Mode (Real-Time)
~~~~~~~~~~~~~~~~~~~~~~~~~~~
*   **Live Behavior**: The viewport tracks the latest data ("Live Head").
*   **Pause/Rewind**: You can pause the view or scrub backward to inspect an anomaly while the
    simulator keeps recording data in the background.

Lab Mode (Post-Facto)
~~~~~~~~~~~~~~~~~~~~~
*   **Full Access**: In post-hoc analysis, the entire dataset is buffered, so you can jump
    instantly to any point in the dive.

Configuration
-------------

The system is configured at two levels: the **Simulation Publisher** (YAML) and the
**Omniverse Subscriber** (Kit settings). The Kit application is built and launched from the
separate ``biologger-viz`` repository. Its README gives the launch commands.

Omniverse Subscriber (Kit Settings)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The HUD and Kit command-line arguments set the most commonly adjusted options. The YAML
configuration of the publisher is described under Multi-Entity Configuration below.

*   **Animal Asset**: Switch between supported assets (Shark, Swordfish, etc.) with
    ``--/biologger/animal=<type>``.
*   **Backend Selection**: Choose the processing engine for coordinate transforms and physics
    updates.

    *   ``--/biologger/backend=warp`` (Default): GPU processing with NVIDIA Warp kernels. The
        extension falls back to the CPU backend if Warp fails to load.
    *   ``--/biologger/backend=cpu``: Standard Python code.

Multi-Entity Configuration
--------------------------

The simulation can stream multiple entities to Omniverse at the same time. Configure them in
the ``entities`` list in the ``simulation`` section of your YAML configuration.

.. code-block:: yaml

   simulation:
     playback_speed: 1.0  # Real-time multiplier
     entities:
       - sim_id: shark_postfacto_v1
         tag_id: RED001
         sampling_rate_hz: 16.0
         input_file: "datasets/shark_data.csv"
       - sim_id: shark_causal_v1
         tag_id: RED001
         sampling_rate_hz: 16.0
         input_file: "datasets/shark_data.csv"
     loop: true

**Configuration Fields:**

*   **sim_id**: A unique descriptive handle for the simulation view (for example,
    ``sword_r_exact``). Used for labels and ZMQ topics.
*   **tag_id**: The biological/deployment ID (for example, ``RED001``). Used to look up
    metadata and species in ``biologger_meta.csv``.
*   **sampling_rate_hz**: The recording frequency of the source sensor data for this entity.
*   **input_file**: Path to the CSV or Feather data stream for this entity.

**Backward Compatibility**

The system still accepts legacy single-file configurations. Existing configurations have
been updated to use the descriptive ``sim_id`` and ``tag_id`` fields. ``publication_rate_hz``
has been retired, so playback runs at full fidelity by default.

ZMQ Protocol (MessagePack)
--------------------------

The simulator now sends data to the Omniverse extension in **MessagePack**, a compact binary
serialization format.

*   **Transparency**: The switch from JSON to MessagePack is handled automatically.
*   **Performance**: Packets are much smaller, so dozens of entities can be shown smoothly at
    the same time.
*   **Entity Mapping**: The system identifies entities over the wire by a compact integer
    ``eid``, mapped by the ``EcosystemRegistry``.

High-Performance Scaling
------------------------

For simulations at very large scale (10,000+ entities), the extension offers these
performance options:

*   **NVIDIA Warp Acceleration**: Moves NED-to-USD transforms and "Slip Angle" calculations
    to the GPU. Enable it with the ``--/biologger/backend=warp`` CLI argument.
*   **Ecosystem Registry**: A structured taxonomy (``registry.json``) maps telemetry IDs to
    specific biological and mechanical USD assets.
*   **Fabric PointInstancer**: (Beta) Uses USDRT Fabric and ``UsdGeom.PointInstancer`` for
    low-latency updates to large schools of animals.


Terrain & Bathymetry Visualization
----------------------------------

The georeferenced seafloor (a fused DEM placed under the real track) is described in
:doc:`scene`. The extension also keeps an older, ungeoreferenced terrain path:

*   **FastAPI Elevation Service**: The extension queries the central ``topobathykit`` service
    on ``http://garnet.internal:9595`` (override it with the
    ``/exts/whoimpg.biologger.subscriber/topobathykitUrl`` setting). The extension fetches,
    stitches and crops tiles asynchronously at a fixed **50-meter resolution** (Web Mercator
    Zoom 11) to keep the viewport frame rate up.
*   **Dynamic USD Mesh Creation**: The ``BathymetryBridge`` module turns fused elevation
    rasters into exact, scaled 3D terrain meshes (``UsdGeom.Mesh``) in the USD Stage.
*   **Scene Controls**:

    *   **enableBathymetry**: A settings-backed checkbox in the extension control panel that
        turns terrain generation on or off during stage initialization.
    *   **Clear Tracks**: Removes the active animal USD prims and resets the trajectory
        trails. The bathymetry terrain meshes stay in place.
    *   **Reset Scene**: Removes both the animal prims and the bathymetry mesh, and starts a
        fresh stage setup.
