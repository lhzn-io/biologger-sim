# Research Report: Omniverse Integration & GPU Acceleration

## Executive Summary

For the "Dual-Mode" simulation engine, the recommended architecture is a **decoupled UDP/ZeroMQ stream** feeding into an **Omniverse Python Extension**. This approach offers the best balance of low latency, architectural simplicity, and flexibility.

For local GPU acceleration of the simulation pipeline, **NVIDIA Warp** is the preferred technology due to its native integration with the USD ecosystem and high-performance Python-to-CUDA JIT compilation.

## 1. Architecture Options for Live Streaming

### Option A: Socket Stream (UDP/ZeroMQ) → Python Extension (Recommended)

* **Mechanism**: `biologger-sim` acts as a publisher (ZMQ PUB or UDP broadcaster). An Omniverse Extension (running inside USD Composer) acts as a subscriber.
* **Data Flow**: `Sensor Data` → `Sim Pipeline` → `ZMQ Packet` → `Omniverse Extension` → `USD Fabric` → `Render`.
* **Pros**:
  * **Decoupled**: Sim engine can run in a separate process, micromamba env, or even a different machine (e.g., a Jetson).
  * **Low Latency**: ZeroMQ is designed for high-throughput, low-latency messaging.
  * **Lightweight**: No need to install full ROS stack or heavy middleware.
* **Cons**: Requires writing a small custom Python Extension for Omniverse.

### Option B: ROS2 Bridge

* **Mechanism**: `biologger-sim` publishes data as ROS2 topics. Omniverse uses its built-in "ROS2 Bridge" extension to subscribe and drive prims.
* **Pros**: "Out of the box" integration if data is in standard ROS formats (Odometry, IMU).
* **Cons**: Introduces a heavy dependency (ROS2) which can be complex to configure on all platforms. Overkill if the project is pure Python.

### Option C: Nucleus Live Sync (File-Based)

* **Mechanism**: `biologger-sim` writes updates to a `.live` layer on a USD stage hosted on Nucleus.
* **Pros**: Native multi-user collaboration.
* **Cons**: **Not suitable for high-frequency telemetry (>30Hz)**. The file-locking and replication overhead of Nucleus is designed for scene editing, not real-time sensor streaming.

## 2. Best Practices for High-Frequency Visualization

### Use USD Fabric (formerly USDRT)

Standard USD API calls (`UsdGeom.Xform.AddTranslateOp().Set(...)`) are designed for scene description and can be slow for per-frame updates at 60Hz+.

* **Solution**: Use **USD Fabric**. It provides a high-performance, low-latency subset of the USD API specifically for runtime data.
* **Implementation**: In the Omniverse Extension, write telemetry data directly to Fabric attributes for the target Prims (e.g., the shark's position/rotation).

### Asynchronous Data Handling

* The Omniverse Extension should run the ZMQ subscriber in a non-blocking manner (e.g., `asyncio` or a separate thread) to avoid freezing the UI/Rendering thread.
* Use the `kit.update` event to apply the latest received state to the scene.

## 3. Local GPU Acceleration (The "Sim Pipeline")

### NVIDIA Warp (`wp`)

Warp is a Python framework that compiles Python functions to efficient CUDA kernels.

* **Fit**: Ideal for the "Sim Pipeline" (sensor fusion, particle filters, dead reckoning).
* **Usage**:

    ```python
    import warp as wp

    @wp.kernel
    def madgwick_filter(q: wp.array(dtype=wp.vec4), acc: wp.array(dtype=wp.vec3), ...):
        # High-performance CUDA logic written in Python
        ...
    ```

* **Advantage**: Warp data structures are compatible with USD/Omniverse. If we eventually move the Sim Pipeline *inside* Omniverse, the code requires minimal changes.

### CuPy

* **Fit**: Good for general matrix operations (like NumPy on GPU).
* **Comparison**: Warp is more specialized for simulation/geometry and spatial math, whereas CuPy is a general array library. Warp is preferred for this project's physics/spatial context.

## 4. Specific Technologies & Workflow

* **Omniverse USD Composer** (formerly Create): This is the main application you will use. It loads the stage (environment + shark) and runs your custom "Telemetry Receiver" extension.
* **Omniverse Nucleus**: Use this **only** for storing static assets (the shark model, the ocean terrain, textures). Do not use it for the live data stream.
* **Omniverse Kit**: The underlying platform. Your "Receiver" will be a "Kit Extension".

## 5. Feasibility Assessment

The proposed plan to use **UDP/ZeroMQ** is **Highly Feasible** and aligns with industry best practices for custom simulator integration.

* **Complexity**: Low. Python `zmq` is simple.
* **Performance**: Excellent. Capable of supporting >1kHz streams easily.
* **Scalability**: Allows the Sim Engine to move to a dedicated GPU or edge device later without changing the visualization stack.

## Recommended Next Steps

1. **Stick to the Plan**: Proceed with `UdpStreamer` (or `ZmqStreamer`) in `biologger-sim`.
2. **Define the Packet**: Ensure the JSON/Binary packet structure matches the `Frame` dataclass.
3. **Future Task**: Create a "Hello World" Omniverse Extension that listens to a ZMQ port and moves a cube.

## References

* **NVIDIA Warp Documentation**: [https://nvidia.github.io/warp/](https://nvidia.github.io/warp/) - Validates Warp as the high-performance Python framework for simulation.
* **Omniverse Extensions Developer Guide**: [https://docs.omniverse.nvidia.com/dev-guide/latest/programmer_ref/extensions.html](https://docs.omniverse.nvidia.com/dev-guide/latest/programmer_ref/extensions.html) - Confirms Extensions as the core building block.
* **Omniverse Connect Overview**: [https://docs.omniverse.nvidia.com/connect/latest/index.html](https://docs.omniverse.nvidia.com/connect/latest/index.html) - Supports the decoupled architecture pattern.
* **Warp Extension for Omniverse**: [https://docs.omniverse.nvidia.com/extensions/latest/ext_warp.html](https://docs.omniverse.nvidia.com/extensions/latest/ext_warp.html) - Confirms native integration.
* **NVIDIA Omniverse Blueprints (Fluid Simulation)**: [https://github.com/NVIDIA-Omniverse-blueprints/digital-twins-for-fluid-simulation](https://github.com/NVIDIA-Omniverse-blueprints/digital-twins-for-fluid-simulation) - **Critical Validation**: This reference blueprint explicitly uses a **ZeroMQ service (`rtdt-zmq-service`)** to stream data into the Omniverse Kit application, confirming our architectural choice is aligned with NVIDIA's own reference implementations for real-time digital twins.
