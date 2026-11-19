=========================
Technical Architecture
=========================

This page describes the architecture of the **Omniverse Kit Extension**
(`whoimpg.biologger.subscriber`). The extension connects high-frequency biologger data to 3D
rigged animal assets.

The extension moves data from a **ZeroMQ (ZMQ)** stream into the **USD Fabric** (runtime memory)
with low latency, so the 3D model, sensor telemetry, and behavioral predictions stay in lockstep.

Architectural Overview
----------------------

The extension runs as an asynchronous background service inside the **biologger-viz Kit app**. It
keeps the simulation and processing logic, which runs in a separate process or on a separate
machine, apart from the rendering viewport.

**Data Flow:**

1.  **ZMQ Socket**: Listens for ``PUB`` packets that carry Euler angles (``rot``) and physics
    telemetry.
2.  **Logic Engine**: A non-blocking Python thread unpacks MessagePack batches.
3.  **Backend Dispatcher**: Selects ``cpu`` (standard Python) or ``warp`` (NVIDIA Warp)
    processing.
4.  **Warp Kernel (Optional)**: If enabled, the GPU computes the NED-to-USD coordinate transforms
    (NED: north-east-down) and the slip angles.
5.  **Fabric Writer**: Writes pose data directly into the **USD Fabric** layer, which updates the
    Prim (e.g., ``/World/Animal``) in under a millisecond.

Implementation Details
----------------------

ZMQ Subscription
~~~~~~~~~~~~~~~~

The subscriber runs in its own background thread so that the UI does not stall ("hitch").

*   **Mechanism**: `ZMQ SUB` socket in dedicated thread.
*   **Port**: Configurable (Default: `5555`).
*   **Topic**: Subscribes to all topics (empty filter) for simplicity.
*   **Batches**: State samples arrive on ``<topic>/batch`` as ``{"batch": [state, ...]}``,
    one message per 50 ms or 1000 samples. A fast replay therefore sends tens of messages a
    second rather than thousands. A PUB socket drops messages once the subscriber falls behind.
    With one message per sample, an uncorked replay (no rate limit) lost half its samples. With
    batches it loses none. The extension still accepts single state messages on ``<topic>``.
    Georeference metadata goes on ``<topic>/meta``.

Dynamic Asset Loading
~~~~~~~~~~~~~~~~~~~~~

The extension loads the animal asset named in a command-line argument. The same extension code
therefore drives a shark, a swordfish, or another marine animal without code changes.

*   **Base Scene**: `omniverse/assets/ocean_scene.usda` (Empty environment).
*   **Asset Injection**: The extension reads the `--/biologger/animal` argument and, at runtime,
    adds a reference to the matching USD/GLB file to the stage.

**Supported Assets:**

*   `shark` -> `great_white_shark.glb`
*   `swordfish` -> `Swordfish_Clear_Patched.glb`
*   `whaleshark` -> `Whale_Shark_Clear_Patched.glb`

Payload Structure
-----------------

The simulator (``ZMQPublisher.publish_state`` in :src:`io/zmq_publisher.py`) sends each batch as
a MessagePack map ``{"batch": [state, ...]}``. Each state uses short keys (values here are
synthetic):

.. code-block:: python

    {
        "eid": 0,                    # entity index
        "sim_id": "sword_causal",
        "tag_id": "TAG001",
        "sp": "swordfish",           # species from the metadata file, or "unknown"
        "ts": 1700000000.0,          # Unix seconds
        "rot": [8.3, 35.2, -179.9],  # [roll, pitch, heading] in degrees
        "phys": {
            "dacc": [-0.38, -0.39, -0.21],  # dynamic acceleration, body frame [x, y, z]
            "sacc": [0.55, 0.02, 0.83],     # static acceleration, body frame [x, y, z]
            "vedba": 0.59,           # vectorial dynamic body acceleration
            "odba": 0.98,            # overall dynamic body acceleration
            "d": 4.6,                # depth (m, positive down)
            "v": 1.96,               # the state's velocity (streaming: dead-reckoning speed, m/s)
            "vv": 0.01,              # vertical velocity (m/s)
            "px": -0.06,             # dead-reckoned north (m)
            "py": 0.0,               # dead-reckoned east (m)
            "cd": 0.0,               # clock drift (s)
        },
    }

Accelerations are in the processor's unit (g in streaming mode, m/s\ :sup:`2` in lab mode).

**Note on Rotation:**
The extension expects Euler angles in degrees and converts them to a quaternion internally. It
applies heading, then pitch, then roll in the body frame: intrinsic Z-Y-X order (the standard
aerospace convention), which equals extrinsic X-Y-Z order (roll, pitch, heading about fixed axes).

Deployment Considerations
-------------------------

Streaming (Virtual Ocean)
~~~~~~~~~~~~~~~~~~~~~~~~~

For the "Virtual Ocean" use case, the extension is designed to work with **Omniverse Kit
Streaming**.

*   **Headless Operation**: The extension does not need local GUI windows for any required
    function.
*   **WebRTC Support**: UI overlays are rendered as part of the viewport stream.

Verification
------------

To check the pipeline:

1.  Launch the Omniverse App with the extension enabled.
2.  Run the simulation with a configuration file:

    .. code-block:: bash

        python -m biologger_sim run --config config/Swordfish-RED001_20220812_19A0564-causal.yaml

3.  **Success Metric**: The animal model in the viewport moves smoothly, with slip angles <15°
    during straight swimming.

.. _slip-angle-validation:

Slip Angle Diagnostics
----------------------

The extension computes a **slip angle**: the angle between the animal's heading and its actual
velocity vector. The slip angle shows whether the coordinate system conversions are correct.

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

The extension computes the heading vector by rotating the mesh's local forward direction
``(0, 0, -1)`` by the telemetry quaternion:

.. code-block:: python

    fwd = rot_quat.Transform(Gf.Vec3f(0, 0, -1))

This works because the USD xform op order applies the telemetry rotation in world space:

.. code-block:: text

    v_world = telemetry × spawn × v_local

Because ``spawn × (0, 1, 0) = (0, 0, -1)``, it follows that:

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

GPU Acceleration (NVIDIA Warp)
------------------------------

Warp kernels run the heavy computations on the GPU so that the extension scales to many
entities.

**NED to USD Coordinate Transform**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``transform_ned_to_usd_kernel`` re-projects positions and orientations in a vectorized pass:

.. code-block:: python

    @wp.kernel
    def transform_ned_to_usd_kernel(
        in_pos: wp.array(dtype=wp.vec3),
        in_quat: wp.array(dtype=wp.vec4),
        out_pos: wp.array(dtype=wp.vec3),
        out_quat: wp.array(dtype=wp.vec4),
        out_slip: wp.array(dtype=float)
    ):
        # Implementation of NED to USD Y-Up re-projection

With this kernel, coordinate conversion does not slow the main application thread, even with
thousands of entities.

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
