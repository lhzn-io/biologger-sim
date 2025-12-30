# Plan: Bootstrap `biologger-sim`

We will bootstrap `biologger-sim` as a clean-slate implementation of the "Dual-Mode" architecture, porting proven logic from `biologger-pseudotrack` while establishing the new real-time simulation capabilities.

## MVP Definition

A **Dual-Mode Simulation Engine** that ingests raw sensor data and runs two parallel pipelines:

1. **Lab Pipeline**: High-accuracy, acausal processing (matching R).
2. **Sim Pipeline**: Low-latency, causal processing (simulating on-tag hardware).
3. **Viz Stream**: A real-time data pump that broadcasts the "Sim" state via UDP/ZMQ for visualization.

## Milestones

### 1. Infrastructure & Core Types

Establish the Python package structure and shared data models.

* Initialize `src/biologger_sim` and `pyproject.toml`.
* Define `Frame` and `Telemetry` dataclasses (the contract between Sim and Viz).
* Port `StreamingProcessor` interface from `biologger-pseudotrack` as the base for `SimProcessor`.

### 2. Data Integration & Streaming Architecture

Develop a robust data ingestion layer that mimics real-time sensor streams.

* **Data Source**: Integrate with the `datasets/` directory (Swordfish, WhaleShark, Porbeagle).
* **Sensor Stream**: Refactor `biologger_pseudotrack.io.sensor_input` into a `SensorStream` class.
  * Support CSV/Feather loading (with auto-conversion).
  * Implement a `stream(rate_hz=...)` generator that yields data chunks.
  * Add playback controls: Real-time (1x), Fast-Forward (10x, 100x), and Step-by-Step.

### 3. The Simulation Engine (Logic)

Implement the core processing logic by porting and refining existing code.

* **Lab Mode**: Port `adaptive_sensor_fusion` logic using `scipy.signal.filtfilt` (acausal).
* **Sim Mode**: Port `streaming_gsep` logic using `lfilter` or EMA (causal).
* **Comparison**: Calculate real-time divergence between Lab and Sim states.

### 4. Visualization Interface (The "Discovery Platform" Start)

Build the bridge to the visualization layer.

* **Architecture**: Use **UDP/ZeroMQ** to decouple the Sim Engine from the Visualizer (as per research report).
* **Streamer**: Implement a `ZmqStreamer` (preferred over UDP for reliability/ease) to broadcast telemetry packets.
* **Monitor**: Create a simple "Monitor" script (CLI or basic Plot) to verify the stream.
* *Future*: Build an Omniverse Kit Extension that subscribes to this ZMQ stream and drives USD Fabric prims.

## Implementation Plan

### Step 1: Project Skeleton

1. Create `pyproject.toml` and `src/biologger_sim/__init__.py`.
2. Create `src/biologger_sim/core/types.py` for shared data structures.
3. Create `src/biologger_sim/io/` for data loading.

### Step 2: Data Layer

1. Implement `src/biologger_sim/io/stream.py` to handle data loading and streaming.
2. Ensure it can read from the `datasets/` workspace folder.

### Step 3: Porting Core Logic

1. Port `biologger_pseudotrack/adaptive_sensor_fusion/streaming.py` to `biologger_sim/processors/sim.py`.
2. Port `biologger_pseudotrack/functions/dead_reckoning.py` (specifically the filter logic) to `biologger_sim/processors/lab.py`.
3. Ensure both implement a common `process_window()` interface.
4. *Note*: Consider using **NVIDIA Warp** for the Sim Pipeline in future iterations for GPU acceleration.

### Step 4: The Runner

1. Create `src/biologger_sim/sim.py` as the main entry point.
2. Implement the loop: Read Stream → Process (Lab & Sim) → Broadcast Sim → Log Lab.

### Further Considerations

1. **Visualization Tech**: Confirmed **UDP/ZeroMQ** is the correct architecture. It decouples the simulation from the visualization, allowing for future distribution (e.g., Sim on Jetson, Viz on Workstation).
2. **Data Source**: We will use the `WhaleShark` dataset from the other repo as the primary test case.
