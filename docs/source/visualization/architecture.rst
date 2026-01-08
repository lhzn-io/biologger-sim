=========================
Technical Architecture
=========================

This document outlines the architecture for the **Omniverse Kit Extension** (`whoimpg.biologger.subscriber`) that serves as the bridge between high-frequency biologger data and 3D rigged animal assets.

The core objective is to move data from a **ZeroMQ (ZMQ)** stream into the **USD Fabric** (runtime memory) at low latency, ensuring that the 3D model, sensor telemetry, and behavioral predictions remain in lockstep.

Architectural Overview
----------------------

The extension operates as an asynchronous background service within **Omniverse USD Composer**. It decouples the simulation/processing logic (running on a separate machine or process) from the rendering viewport.

**Data Flow:**

1.  **ZMQ Socket**: Listens for `PUB` packets containing Quaternions and Physics telemetry.
2.  **Logic Engine**: A non-blocking Python thread parses JSON packets.
3.  **Fabric Writer**: Injects pose data directly into the **USD Fabric** layer for sub-millisecond updates to the Prim (e.g., `/World/Animal`).

Implementation Details
----------------------

Asynchronous Subscription
~~~~~~~~~~~~~~~~~~~~~~~~~

To prevent UI "hitching," the subscriber runs in a separate `asyncio` loop.

*   **Mechanism**: `ZMQ SUB` socket.
*   **Port**: Configurable (Default: `5555`).
*   **Topic**: Subscribes to all topics (empty filter) or specific animal IDs.

Dynamic Asset Loading
~~~~~~~~~~~~~~~~~~~~~

The extension supports dynamic loading of different animal assets based on command-line arguments. This allows the same extension code to drive a Shark, Swordfish, or other marine animals without code changes.

*   **Base Scene**: `omniverse/assets/ocean_scene.usda` (Empty environment).
*   **Asset Injection**: The extension reads the `--/biologger/animal` argument and references the corresponding USD/GLB file into the stage at runtime.

**Supported Assets:**

*   `shark` -> `great_white_shark.glb`
*   `swordfish` -> `swordfish.usd`
*   `whaleshark` -> `whale_shark.usd`

Payload Structure
-----------------

The extension expects a ZMQ packet adhering to the following structure. This matches the output of `scripts/zmq_rotate_test.py`.

.. code-block:: json

    {
      "transform": {
        "quat": [0.707, 0.0, 0.707, 0.0] // Orientation (w, x, y, z)
      },
      "physics": {
        "accel_dynamic": [0.01, 0.5, 0.02], // Body-frame acceleration [x, y, z]
        "vedba": 0.51                       // Vectorial Dynamic Body Acceleration
      }
    }

**Note on Quaternions:**
Omniverse uses `(w, x, y, z)` ordering. Ensure your publisher reorders standard `(x, y, z, w)` quaternions (e.g., from Scipy) before sending.

Deployment Considerations
-------------------------

Streaming (Virtual Ocean)
~~~~~~~~~~~~~~~~~~~~~~~~~

To support the "Virtual Ocean" use case, the extension is designed to be compatible with **Omniverse Kit Streaming**.

*   **Headless Operation**: The extension does not rely on local GUI windows for critical functionality.
*   **WebRTC Support**: UI overlays are rendered as part of the viewport stream.

Verification
------------

To validate the pipeline without the full simulation:

1.  Launch the Omniverse App with the extension enabled.
2.  Run the test script:

    .. code-block:: bash

        python scripts/zmq_rotate_test.py

3.  **Success Metric**: The animal model in the viewport should rotate and tumble smoothly with <10ms latency.

.. _slip-angle-validation:

Slip Angle Diagnostics
----------------------

The extension computes a **slip angle** metric to validate alignment between the animal's heading direction and its actual velocity vector. This is critical for confirming that coordinate system conversions are correct.

**Definition:**

.. math::

    \theta_{slip} = \arccos(\hat{v} \cdot \hat{h})

Where:

*   :math:`\hat{v}` = Normalized velocity vector (computed from consecutive position deltas)
*   :math:`\hat{h}` = Normalized heading vector (forward direction of the mesh in world space)

**Expected Values:**

*   **Swimming straight**: Slip angle < 15° (typically 5-10°)
*   **Turning maneuver**: Slip angle may spike to 30-45°
*   **Coordinate bug**: Slip angle consistently > 80° indicates a sign error or axis mismatch

**Implementation Details:**

The heading vector is computed by transforming the mesh's local forward direction ``(0, 0, -1)`` by the telemetry quaternion:

.. code-block:: python

    fwd = rot_quat.Transform(Gf.Vec3f(0, 0, -1))

This works because the USD xform op order ensures telemetry is applied in world space:

.. code-block:: text

    v_world = telemetry × spawn × v_local

Since ``spawn × (0, 1, 0) = (0, 0, -1)``, we have:

.. code-block:: text

    telemetry × spawn × (0, 1, 0) = telemetry × (0, 0, -1)

**Diagnostic Logging:**

The extension logs slip angle data to ``omniverse-logs/<session>/slip_log.csv`` with columns:

*   ``Timestamp``: Simulation time
*   ``SlipAngle``: Angle in degrees
*   ``Speed``: Movement distance between frames
*   ``Vx, Vy, Vz``: Normalized velocity vector components
*   ``Hx, Hy, Hz``: Normalized heading vector components
*   ``NED_Heading``: Raw NED compass heading (before negation)

Coordinate System Reference
---------------------------

The following table summarizes the coordinate conventions used throughout the system:

.. list-table:: Coordinate System Conventions
   :header-rows: 1
   :widths: 20 25 25 30

   * - System
     - Forward
     - Up
     - Heading Convention
   * - NED (Marine)
     - +X (North)
     - -Z (Up from Down)
     - Clockwise (0°=N, 90°=E)
   * - USD Y-Up
     - -Z
     - +Y
     - Counter-Clockwise (Right-Hand Rule)
   * - Shark GLB (Native)
     - +Y
     - +Z
     - N/A (requires spawn rotation)

**Conversion Summary:**

.. code-block:: text

    NED Heading → USD Heading:  h_usd = -h_ned
    NED Depth   → USD Y:        y_usd = -depth_ned
    NED X (North) → USD Z:      z_usd = -x_ned
    NED Y (East)  → USD X:      x_usd = y_ned
