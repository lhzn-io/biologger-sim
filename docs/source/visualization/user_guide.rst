=========================
User Guide
=========================

This guide describes how to interact with the Biologger Simulation in NVIDIA Omniverse. The extension provides a high-fidelity digital twin environment for visualizing animal movement, sensor fusion accuracy, and behavioral patterns.

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
