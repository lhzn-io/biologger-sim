Backend Acceleration Analysis
=============================

This document evaluates the potential processing performance benefits of migrating the core simulation engine to accelerated backends: **Compiled CPU** (Rust/Go) and **GPU** (CUDA/Warp).

1. Compiled CPU (Rust/Go)

-------------------------

A rewrite in Rust or Go would primarily target the removal of Python's interpreter overhead and Global Interpreter Lock (GIL).

* **Benefit**: 10-50x speedup in raw processing throughput.
* **Bottleneck Solved**: Serialization cost (MsgPack) and Manual Iterator overhead.
* **Status**: With the current `heapq.merge` optimization in Python, we are already achieving ~33k SPS. This is sufficient for real-time visualization (typically 60-120 Hz). Rust is a "nice to have" optimization unless per-entity compute becomes extremely heavy.

2. GPU Acceleration (NVIDIA Warp / CUDA)

-------------------------

GPU acceleration offers a fundamental paradigm shift from *sequential* processing to *massive parallelism*. The benefit depends heavily on the simulation topology.

Scenario A: Identical Data, Many Parameters (Monte Carlo)
-------------------------

**Topology**: Simulating 1,000+ instances of the *same* animal deployment, but sweeping parameters (e.g., varying AHRS filter gains, slight sensor noise variations).

* **Architecture**:
  * Load the sensor dataset (N MB) into GPU VRAM **once**.
  * Launch a CUDA kernel with K threads (one per simulation instance).
  * Each thread reads from the *same* read-only memory buffer but maintains its own state (quaternion, velocity).
* **Performance Estimate**: **1000x - 10,000x Speedup**.
* **Why**: This is the "Holy Grail" of GPU computing (Single Instruction, Multiple Data). Memory bandwidth is perfectly cached (all threads access the same addresses), and compute density is maximized.
* **Suitability**: **Extremely High**. If the goal is parameter optimization or uncertainty quantification, GPU is non-negotiable.

Scenario B: Diverse Data, Many Animals (School of Fish)
-------------------------

**Topology**: Simulating 1,000+ *different* animals, each with a unique dataset loaded from disk.

* **Architecture**:
  * Must load K distinct datasets into GPU VRAM (Total Size: K * N MB).
  * Launch K threads. Each thread reads from a *different* region of global memory.
* **Performance Estimate**: **10x - 50x Speedup** (Bounded by Memory Bandwidth).
* **Challenge**: The bottleneck shifts from Compute to **Memory Bandwidth**. GPUs hate uncorrelated memory access ("gather/scatter"). If thread 0 reads address 0 and thread 1 reads address 1,000,000, the cache line efficiency drops.
* **Size Limits**: You are limited by VRAM. (e.g., 24GB VRAM / 50MB per file = ~480 animals max). Python/Rust can stream from disk/RAM more easily.
* **Suitability**: **Moderate**. High performance, but requires complex "Texture Streaming" or "Unified Memory" management.

Implementation Strategy
-----------------------

For a Python-native project, **NVIDIA Warp** is the recommended bridge.

* **Hybrid Approach**:
    1. Keep the outer control loop in Python.
    2. Write the `Processor.process()` logic as a Warp Kernel (`@wp.kernel`).
    3. Pass data as Warp Arrays (`wp.array`).
* **Avoid**: Writing raw C++/CUDA unless absolutely necessary. Warp provides near-native CUDA performance with Python syntax.

Recommendation
--------------

1. **Current Status**: Stick with Python `heapq.merge`. It is fast enough for ~50-100 concurrent real-time entities.
2. **Next Step (If Batching)**: If the user needs to run "Monte Carlo" runs (Same Data, Random Params), implement a **Warp Backend**. The speedup will be Order-of-Magnitude.
3. **Optimization**: Do not move to Rust just for serialization speed; the engineering cost is high for a solved problem.
