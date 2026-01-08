=========================
User Guide
=========================

This guide describes how to interact with the Biologger Simulation in NVIDIA Omniverse. The extension provides a high-fidelity digital twin environment for visualizing animal movement, sensor fusion accuracy, and behavioral patterns.

.. _coordinate-conventions:

Coordinate Systems & Conventions
--------------------------------

For users coming from marine science, robotics, or hydrography fields, it is important to note the difference in coordinate conventions between typical oceanographic data and the 3D visualization environment.

Marine Science Standard (NED)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Oceanographic data (e.g., from biologging tags) typically uses the **NED (North-East-Down)** convention:
*   **X**: North
*   **Y**: East
*   **Z**: Down (Depth)
*   **Heading**: Clockwise from North (0° = North, 90° = East)

Visualization Standard (USD Y-Up)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
NVIDIA Omniverse and the underlying USD (Universal Scene Description) format use a **Y-Up, Right-Handed** convention:
*   **Y**: Up (Altitude)
*   **-Z**: Forward (North)
*   **X**: Right (East)
*   **Rotation**: Counter-Clockwise (Right-Hand Rule)

Automatic Conversion
~~~~~~~~~~~~~~~~~~~~
The ``biologger-sim`` extension automatically handles the re-projection of data to ensure visuals match physical reality:

1.  **Heading Negation**: The clockwise compass heading (N→E→S→W) is negated to match the counter-clockwise rotation convention of USD's right-hand rule. A NED heading of +90° (East) becomes -90° in USD, correctly pointing the forward vector toward +X.

2.  **Euler-to-Quaternion Mapping**:

    *   Sensor **Pitch** (Nose Up/Down) → Rotation around **X-Axis**
    *   Sensor **Heading** (Compass) → Rotation around **Y-Axis** (negated)
    *   Sensor **Roll** (Bank Left/Right) → Rotation around **-Z-Axis**

3.  **Rotation Application Order**: Yaw (Heading) → Pitch → Roll, matching standard aerospace/marine conventions.

.. _mesh-orientation:

Mesh Orientation & Transform Stack
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Animal mesh assets (GLB/USD) are typically authored with an arbitrary "up" direction. The extension applies a **spawn rotation** to align the mesh with USD conventions before telemetry rotations are applied.

**Example: Shark GLB Asset**

The shark mesh is authored with its nose pointing along +Y (upward in its native coordinate frame). To align it with USD's -Z = Forward convention:

*   **Spawn Rotation**: ``(-90°, 180°, 0°)`` XYZ Euler
*   This maps the mesh's +Y nose to world -Z (North)

**Critical: USD XformOp Order**

USD applies transform operations in the order they appear in the ``xformOpOrder`` attribute. For correct world-space heading rotation, the **telemetry orientation must be applied BEFORE the spawn rotation** in the op list:

.. code-block:: text

    xformOpOrder = ["xformOp:translate", "xformOp:orient:telemetry", "xformOp:rotateXYZ", "xformOp:scale"]

This produces the transform: ``v_world = telemetry × spawn × v_local``

1. **Spawn** maps mesh-local nose (+Y) to world -Z
2. **Telemetry** then rotates around world Y-axis, correctly affecting the -Z forward direction

.. warning::
    **Common Pitfall**: If the spawn rotation appears BEFORE telemetry in the op order, telemetry rotations are applied in **mesh-local space**. Since the mesh nose is along the local Y-axis, a Y-rotation (heading) would rotate around the nose itself—having no visible effect on heading direction.

.. warning::
    **For Asset Creators**: Ensure your animal models are oriented to face **-Z** (Forward) in their bind pose, OR document the required spawn rotation. If an asset faces +Z or +X, it will appear to "drift" sideways or backwards relative to the trajectory.

Features Overview
-----------------

The visualization toolkit includes:

*   **Real-time Telemetry HUD**: Heads-up display for sensor metrics.
*   **Flexible Tracking Modes**: Toggle between full position tracking or orientation-only analysis.
*   **Cinematic Camera**: Smooth follow camera with user-controllable orbit.
*   **Instant Replay (Time Travel)**: Pause and rewind live simulations without losing data.
*   **Infinite Track**: Full trajectory remains visible during scrubbing, with future path "ghosted".

Telemetry Display (HUD)
-----------------------

The Heads-Up Display overlays critical sensor data directly in the viewport, allowing for immediate validation of the pipeline's output.

*   **Status Indicators**: Shows connection health and data rate.
*   **Sensor Metrics**: Real-time display of Pitch, Roll, Heading, and Depth.
*   **System Diagnostics**: Latency counters and processing frame times.

.. note::
   The HUD can be toggled on/off to capture clean screenshots or video recordings.

Tracking & Visualization Modes
------------------------------

The extension supports different visualization strategies depending on your analysis needs:

1. Full Position Tracking (Default)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In this mode, the animal moves through the virtual ocean based on the **Dead Reckoned** path calculated by the pipeline.

*   **Best for**: Analyzing large-scale movements, foraging patterns, and depth profiles.
*   **Visuals**: A 3D trajectory line ("Infinite Track") is drawn behind the animal, visualizing the path taken.

2. Orientation-Only Mode
~~~~~~~~~~~~~~~~~~~~~~~~
This mode locks the animal's position to the center of the world (0,0,0) while applying real-time rotation updates.

*   **Best for**: Debugging IMU sensor fusion (AHRS), validating attachment angles, and inspecting fine-scale body motion without the distraction of translation.
*   **Usage**: Uncheck "Enable Position Tracking" in the extension UI.

Camera Controls
---------------

The system features a custom camera controller designed for tracking fast-moving marine animals.

*   **Follow Camera**: Automatically keeps the animal in frame, smoothing out jittery motions to provide a cinematic view.
*   **Orbital Control**: While the camera follows the animal, you can orbit around it to view movement from any angle.
    *   **Left Click + Drag**: Orbit/Rotate camera.
    *   **Scroll Wheel**: Zoom in/out.
    *   **Middle Click**: Pan.

Time Control & Analysis (Instant Replay)
----------------------------------------

The **Instant Replay** system allows you to pause, rewind, and scrub through the visualization in real-time, decoupling the **View Time** from the **Simulation Time**.

Simulation Mode (Real-Time)
~~~~~~~~~~~~~~~~~~~~~~~~~~~
*   **Live Behavior**: The viewport tracks the latest data ("Live Head").
*   **Pause/Rewind**: You can pause the view or scrub backward to inspect an anomaly while the simulator continues to record data in the background.
*   **Ghost Path**: When you scrub backward, the full trajectory remains visible. The "future" path (relative to your playback head) is rendered as a semi-transparent "ghost" line, maintaining context of where the animal eventually goes.

Lab Mode (Post-Facto)
~~~~~~~~~~~~~~~~~~~~~
*   **Full Access**: In post-hoc analysis, the entire dataset is buffered, allowing instant random access to any point in the dive duration.

Configuration
-------------

The extension panel provides immediate access to commonly adjusted settings:

*   **Animal Asset**: Switch between supported assets (Shark, Swordfish, etc.) via command line arguments.
*   **Buffer Size**: Configure how much history is kept in memory (Default: 100k points).
*   **Visualization Options**: Toggle the HUD, Trajectory Line, or Coordinate Axes.
