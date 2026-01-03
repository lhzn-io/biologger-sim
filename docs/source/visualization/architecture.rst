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
