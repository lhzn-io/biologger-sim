# Dual-Mode Processing Architecture: Lab vs Digital Twin

**Document Status**: Living (Planning Phase)
**Created**: 2025-12-18
**Last Updated**: 2025-12-29

---

## Executive Summary

This document describes the multi-mode processing architecture for biologger data analysis, supporting:

1. **Lab Mode**: Post-hoc research analysis (maximum accuracy).
2. **Digital Twin Mode**: Real-time on-tag computation simulation (causal processing).
3. **Discovery Platform**: High-performance visualization and AI-driven analysis (RTX/AGX accelerated).

**Key Finding**: The ~2km trajectory divergence between R and Python implementations stems from **filter causality**, not algorithmic bugs:

- **R (batch)**: Uses centered filter (`stats::filter(sides=2)`) - looks ±24 samples (acausal)
- **Python (streaming)**: Uses causal filter - looks back 48 samples only
- **Impact**: Persistent 2-5° pitch/roll offset → 5.5° heading error → 2km position drift

**Solution**: Implement both modes with appropriate filters for each use case.

---

## Strategic Vision

The project targets three distinct application tiers:

### Tier 1: The "Scientific Tool" (Research Analysis)

- **Value**: Automated behavioral labeling. By scrubbing through synchronized video and IMU data, researchers can "ground truth" their ML models in real-time.

- **Feature**: Exportable "SimReady" behavioral snippets that can be used to train larger classifiers for the wider community.

### Tier 2: The "Public Experience" (Education & Outreach)

- **Value**: Immersive story-telling. A "God's Eye View" of a swordfish's 2,000m dive is more visceral than a 2D line graph.

- **Feature**: An interactive "Virtual Ocean" accessible via web browser. By running Omniverse in server mode on high-performance compute, users can stream the rendered visualization to any device, enabling broad public engagement without requiring specialized hardware.

### Tier 3: The "Edge Product" (Autonomous Tags)

- **Value**: Autonomous on-tag processing. This is the "Digital Twin v3" roadmap—simulating the logic that will eventually live on a Jetson-powered tag.

- **Feature**: Real-time "saliency filtering" where the tag decides to only record video when the IMU detects an interaction.

---

## Near-Term Project Plan (Sprint to Demo)

### Phase 1: The "Rig & Sync" (Months 1-2)

**Status**: **Completed**

- **Task**: Import a high-quality shark/swordfish USD model into Omniverse USD Composer.
- **Logic**: Implement the **UDP/ZeroMQ sidecar** to drive the `Root_Bone` rotation from the Madgwick-filtered IMU stream.
- **Deliverable**: A 3D shark that moves in real-time parity with a playback of recorded biologger data.

**Completed Items**:

- [x] **Infrastructure**: Project structure, environment, and linting setup.
- [x] **Data Loading**: Feather file support for high-performance I/O (`biologger_sim.io.converter`).
- [x] **Streaming**: Basic ZeroMQ publisher (`biologger_sim.io.zmq_publisher`).
- [x] **Telemetry**: Performance monitoring system (`biologger_sim.core.telemetry`).
- [x] **Documentation**: Initial Sphinx setup and visualization guides.
- [x] **Omniverse Extension**: Created `whoimpg.biologger.subscriber` extension.
- [x] **Rotation Logic**: Implemented basic rotation demo (Cube Rotation).
- [x] **Integration**: Connected Python simulator to Omniverse extension via ZeroMQ.

**Documentation Strategy**:

- **Incremental Migration**: Documentation from the reference repository (`biologger-pseudotrack`) will be ported incrementally as corresponding features are implemented in `biologger-sim`.
- **Coverage**: Ensure complete coverage of methodology and pipeline architecture by the end of Phase 2.

### Phase 2: The "Multi-Modal Viewport" (Months 3-4)

- **Task**: Create an Omniverse Kit Extension with a custom UI.

- **Logic**: Use the `kit.update` event to sync the 3D position with a video window displaying the animal's perspective.
- **Deliverable**: A synchronized "Ethogram HUD" that displays live depth, pitch, and predicted behavior (e.g., "Cruising") next to the 3D model.

### Phase 3: The "Scrub & Search" (Month 5+)

- **Task**: Implement a unified timeline slider that handles asynchronous data frequencies (e.g., 100Hz IMU vs 30fps Video).

- **Logic**: Use **NVIDIA VSS (Video Search & Summarization)** to index "interesting" segments (breaches/dives) for instant jumping via natural language.
- **Deliverable**: A polished, interactive demonstration where a user can type "Find the deepest dive" and the 3D scene and video jump to that exact timestamp.

### Phase 4: Remote Access & Cloud Deployment (Month 6+)

- **Task**: Enable Omniverse Kit Streaming (WebRTC) for browser-based access.
- **Logic**: Configure the Omniverse application to run in headless/server mode on high-performance compute (e.g., Thor) and stream the viewport to remote clients via web browser.
- **Deliverable**: A URL-accessible version of the visualization that allows users to view and interact with the simulation without needing a local workstation with an RTX GPU.
- **Reference**: [Omniverse Streaming Docs](https://docs.omniverse.nvidia.com/kit/docs/kit-app-template/latest/docs/streaming.html)

---

## OceanSim Integration Strategy

**OceanSim** is the chosen framework for bridging biological observation and engineering-grade simulation, shifting focus from map visualization to physical volume simulation.

### 1. Modeling Current Flows & Animal Interaction

OceanSim serves as a **perception and dynamics framework** built on Isaac Sim.

- **The "Current Vector" Method**: Ingest **NOAA/HYCOM current data** (V-X and V-Y velocity vectors) to apply as a "Global Force" in the Isaac Sim physics engine, interacting with the animal's orientation from 100Hz IMU data.
- **Animal Interaction**: Use **NVIDIA Warp** to calculate real-time "Drag" and "Lift" on the animal mesh based on the relative velocity between the current and the animal.
- **Visualizing the Flow**: Use a **Particle System** in Omniverse synced to NOAA current vectors to visualize water flow (marine snow/particulates).

### 2. The NOAA Bathymetry Pipeline

A "Digital Twin" workflow replaces the need for subsea surveys.

1. **Data Source**: **NOAA Bathymetric Data Viewer** (BAG or GeoTIFF files).
2. **Conversion**: Convert 2D elevation grids to 3D **Meshes** using QGIS or Blender.
3. **Import**: Import as `.usd` into the OceanSim Environment layer.
4. **Physics**: Apply **Colliders** to the seafloor mesh for physical interaction.

### 3. OceanSim Context

**Repository**: [https://github.com/umfieldrobotics/OceanSim](https://github.com/umfieldrobotics/OceanSim)

**OceanSim** is a GPU-accelerated underwater robot perception simulation framework built on **NVIDIA Isaac Sim** and the **Omniverse** ecosystem. It is designed to bridge the gap between biological observation and engineering-grade simulation.

**Key Capabilities**:

- **Physics-Based Sensor Rendering**: Accurately models both visual (camera) and acoustic (imaging sonar, DVL) sensors using advanced physics models.
- **GPU Acceleration**: Fully leverages GPU-based parallel computing for high-performance real-time rendering.
- **OpenUSD Workflow**: Enables efficient 3D workflows and local ownership of high-resolution environmental data.
- **Scientific Validation**: Featured by NVIDIA Robotics and presented at ICRA 2025 (Song et al., arXiv:2503.01074).

### 4. 2,000m Simulation Setup

Recommended setup for research presentations:

- **The Floor**: High-res **NOAA BAG** file of the specific trench/canyon (USD mesh).
- **The "Water"**: OceanSim's **Underwater Post-Processing** for depth-specific turbidity. Use **Imaging Sonar** model for visibility at depth.
- **The Current**: Python script feeding NOAA current data to push the animal's `SkelRoot`.

---

## Mode 1: Lab (Post-hoc Analysis)

### Purpose

Maximum accuracy reconstruction of animal behavior from recovered tag data.

**Status**: Implemented and Validated (Dec 2025)

### Key Features

- **Filter**: `scipy.signal.filtfilt` (zero-phase, centered)
- **Matches**: R's `stats::filter(sides=2, circular=TRUE)`
- **Mag calibration**: Locked offsets (pre-deployment calibration)
- **Attachment angles**: Locked (batch-computed from full dataset)
- **Output**: Full passthrough CSV with all variables

### Use Cases

1. Research analysis of recovered tags
2. R-compatibility validation
3. Algorithm baseline/ground truth
4. Training data for ML models
5. Publication-quality results

### Accuracy Target

- Pitch/roll error vs R: <0.1°
- Trajectory difference vs R: <100m over full deployment
- Correlation with R static accel: >0.999

---

## Mode 2: Simulation (Real-Time / On-Tag)

### Purpose

Simulate real-time computation that could run on the tag itself, enabling:

- Selective logging based on behavioral state
- Battery life optimization (3-10x extension)
- On-tag behavioral classification
- Algorithm development for future tag deployments

### Iteration Roadmap

#### **v1: EMA Crossover (Causal, Immediate)**

**Status**: Design complete, ready to implement

**Filter Strategy**:

```python
# Fast/slow EMA crossover (MACD-inspired)
fast_ema = alpha_fast * raw + (1 - alpha_fast) * fast_ema_prev  # α=0.2
slow_ema = alpha_slow * raw + (1 - alpha_slow) * slow_ema_prev  # α=0.02
crossover_signal = fast_ema - slow_ema

# Adaptive logging
if abs(crossover_signal) > threshold:
    log_full_resolution()  # Behavioral transition detected
else:
    log_summary_only()     # Steady state
```

**Features**:

- Fully causal (no future data)
- Detects behavioral transitions
- Computationally trivial (~10 ops/sample)
- Optional mag offset lock (realistic)
- Optional attachment angle lock (scientist request, less realistic)

**Trade-offs**:

- ~0.5-1° pitch/roll lag vs Lab mode
- ~500-1000m trajectory difference from Lab mode
- But enables 90% data reduction!

#### **v2: Madgwick-Inspired Adaptive Fusion**

**Status**: Planned, leverage existing `adaptive_sensor_fusion/` module

**Features**:

- Quaternion-based orientation tracking
- Gyroscope integration (if available)
- Adaptive filter gains based on motion state
- Better handling of dynamic maneuvers

**Requirements**:

- Dataset with gyroscope data
- True Madgwick filter for 9-DOF fusion
- Validation against IMU ground truth

**Expected Improvement**:

- <0.2° pitch/roll error in steady state
- Better tracking during rapid maneuvers
- Reduced trajectory drift

#### **v3/Epsilon+2: GPU-Equipped Tags**

**Status**: Future vision, feasibility study needed

**Hardware Target**:

- Jetson Nano or similar (5-10W)
- Solar panel (whale shark, basking shark)
- Or large battery pack (deep divers: swordfish, beaked whales)

**Capabilities**:

- Real-time particle filters (Monte Carlo position estimation)
- Neural network inference (behavioral classification)
- Online learning (adapt to individual behavior)
- Uncertainty-driven selective logging
- Multi-hypothesis trajectory tracking

**Selective Logging Strategy**:

```python
# GPU-accelerated on-tag
particles = run_particle_filter(sensor_data)
uncertainty = compute_position_uncertainty(particles)

if uncertainty > threshold:
    log_full_data()      # Model uncertain, need ground truth
    update_model()       # Online learning
else:
    log_summary_only()   # Model confident
```

---

## Mode 3: Discovery Platform (Visualization)

### Purpose

High-fidelity visualization and "Digital Twin" experience using NVIDIA Omniverse.

**Detailed Specification**: [Omniverse Extension Spec](./omniverse_extension_spec.md)

### Key Components

1. **`whoimpg.biologger.subscriber`**: Custom Kit Extension to bridge ZMQ data to USD Fabric.
2. **USD Fabric Integration**: Direct memory access for <10ms latency updates.
3. **Multi-Modal Sync**: Synchronized playback of 3D motion, video, and sensor data.

---

## Technical Deep Dive: Filter Causality

### The Root Cause

**R's Batch Filter (Acausal)**:

```r
Gsep <- function(xyz, filt=rep(1,48)/48) {
  X_Static <- stats::filter(xyz[,1], sides=2, circular=TRUE)
  # sides=2: centered window [i-24 to i+23]
  # circular=TRUE: wraps at boundaries
}
```

At sample 100:

- R averages samples [76-124] (24 before, current, 23 after)
- **Uses future data** from samples 101-124

**Python's Streaming Filter (Causal)**:

```python
def streaming_gsep(self, x, y, z):
    static_x = np.mean(self.accel_window)  # Last 48 samples
    # At sample 100: averages samples [53-100]
    # Only uses past data
```

At sample 100:

- Python averages samples [53-100] (past 48 samples)
- **No future data** - truly causal

### Why This Creates Persistent Offset

**The Swordfish Never Stops Moving!**

When the animal is constantly changing orientation:

1. Centered filter (R): Smooths transitions symmetrically → accurate instant orientation
2. Causal filter (Python): Always lags behind changes → systematic offset

**Analogy**: Driving a car while:

- **R**: You have dashcam footage of the whole trip, can average around each moment
- **Python**: You're in the car, can only use rearview mirror

The lag doesn't converge to zero because the animal keeps swimming, diving, turning!

### Why Centered is "More Accurate" for Post-hoc

For batch processing of recorded data:

- ✅ We have ALL the data already
- ✅ Animal has already moved
- ✅ We're reconstructing where it went
- ✅ Centered filter gives best estimate of true orientation
- ✅ Standard practice in post-hoc analysis

### Why Causal is Required for On-Tag

For real-time computation:

- ✅ Can only use past data
- ✅ Simulates what tag could compute
- ✅ Required for streaming pipelines
- ✅ Enables real-time behavioral classification
- ✅ Philosophically "pure" dead reckoning

---

## EMA Crossover Innovation

Inspired by finance (MACD), adapted for biologging.

### Multi-Timescale Feature Engineering

```python
# Ultra-fast: α=0.5 (noise/artifact detection)
# Fast: α=0.2 (behavior transitions)
# Medium: α=0.05 (activity state)
# Slow: α=0.01 (daily rhythm)

features = [
    fast_ema - slow_ema,         # Primary signal (inflection detector)
    abs(fast_ema - medium_ema),  # Activity intensity
    medium_ema - slow_ema,       # Trend
    zero_crossings_per_minute,   # State change frequency
    signal_variance_10s,         # Stability measure
]
```

### Behavioral State Detection

```python
signal = fast_ema - slow_ema

if signal > 2.0:
    state = "RAPID_CHANGE"   # Breach, attack, escape
elif signal > 0.5:
    state = "TRANSITION"     # Diving, turning
elif abs(signal) < 0.2:
    state = "STEADY"         # Cruising, gliding
elif signal < -0.5:
    state = "STABILIZING"    # Leveling off
```

### Battery Life Extension

**Steady State** (90% of deployment):

- Log summary only: mean orientation (1 Hz), activity metrics, GPS
- Data rate: ~100 bytes/sample → 10 bytes/sample (90% reduction)

**Events** (10% of deployment):

- Log full resolution: all sensors @ 16 Hz
- Triggered by: diving, turning, feeding, breaching
- Data rate: 100 bytes/sample

**Result**: 3-10x longer deployments!

---

## Expanded Vision: Pelagic Simulation & Discovery Platform

**Status**: Vision / Planning
**Hardware Target**: RTX 5080 (Batch) + AGX Thor (Real-time)

This project plan is designed to implement a high-performance, multimodal "Pelagic Simulation Environment" and discovery platform. It leverages **RTX 5080** for batch processing and **AGX Thor** for real-time visualization and edge-inference.

### 1. System Architecture Overview

The system is divided into three core pipelines that operate on a streaming basis to avoid memory bottlenecks.

- **Ingestion Pipeline:** Extracts frames and syncs telemetry.
- **Search & Summarization (VSS) Pipeline:** Indexes video for natural language queries.
- **Visualization (Sim Env) Pipeline:** Renders a 3D surrogate driven by high-frequency IMU data.

### 2. Technical Specification

#### A. Data Synchronization Engine (Clock-Master)

**Goal:** Align 30fps video with high-frequency (e.g., 50Hz-100Hz) IMU data.

- **Logic:** Parse the `.ubx` (GPS) pulses to establish a "Global Sync Time."
- **Implementation:** Create a lookup table mapping `Video_Frame_ID` ↔ `IMU_Timestamp`.
- **Agent Task:** Implement an interpolator (using `scipy.interpolate`) to estimate IMU values at exact shutter-open times of the camera.

#### B. IMU-Driven Saliency Filter

**Goal:** Drastically reduce video processing time by skipping "steady-state" swimming.

- **Feature Engineering:**
  - Calculate **Dynamic Body Acceleration (VeDBA)**.
  - Compute **Tailbeat Frequency (TBF)** via sliding-window FFT on `Accel_Y`.
- **Trigger Logic:** Identify segments where VeDBA or TBF deviates by `> 2σ` from the 5-minute rolling mean.
- **Output:** A list of `Interesting_Time_Windows` for priority YOLO/VLM processing.

#### C. NVIDIA VSS & VLM Integration

**Goal:** Enable natural language search (e.g., "Find me a breach or interaction with prey").
**Reference:** Based on [NVIDIA AI Blueprint for Video Search and Summarization](https://blogs.nvidia.com/blog/ai-blueprint-video-search-and-summarization/).

- **Hardware:** Deploy **NIM (NVIDIA Inference Microservices)** on the RTX 5080.
- **Model:** Use **YOLOv11x** for object detection and **VILA/Cosmos** as the Vision-Language Model for captioning.
- **Metadata:** Inject telemetry status (e.g., "Depth: 40m, Speed: High") into the VLM prompt to ground the AI's descriptions.

### 3. Digital Twin Visualization (The Demo)

#### 3D Rig Configuration

- **Model:** Use species-appropriate surrogates (e.g., Great White Shark, Swordfish, Tuna) from Sketchfab/Omniverse assets.
- **Transform Logic:**
  - **Root Orientation:** Apply a **Madgwick/Mahony filter** to fuse Accel/Gyro/Mag into Quaternions. Apply these to the model's `Root_Bone`.
  - **Locomotion Synthesis:** Use the `Accel_Y` (lateral) signal to drive the `Tail_Joint` rotations.
  - **Formula:** `Angle = k * Accel_Y`, where `k` is a scaling constant tuned to the species' maximum flexion.

#### Omniverse Live-Link Setup

- **Communication:** Implement a **UDP/ZeroMQ sidecar** that streams `[Quaternion, Tail_Angle, Depth]` from the Python processing script to **Omniverse USD Composer**.
- **Real-time Overlay:** Render a 3D vector arrow representing the **G-Force Vector** projecting from the animal's dorsal region.

#### High-Performance Scaling Strategy

- **Global Scaling (10k+ Entities)**: Migrate from individual Xform prims to `UsdGeom.PointInstancer` at `/World/Ecosystem`. This centralized management supports massive fleets of mixed entities (sharks, vessels, gliders).
- **GPU Acceleration (`omni.warp`)**: Move coordinate transformations (NED to USD) and "Slip Angle" calculations to a JIT-compiled GPU kernel, bypassing Python loop overhead for physics-grade throughput.
- **Data-Oriented Updates (`USDRT`)**: Utilize USDRT Fabric for direct GPU memory access/zero-copy updates, avoiding the latency of the standard USD stage write path.
- **Synthetic Scale Testing**: Generate 10,000+ simulation tracks by applying procedural noise (Perlin/Simplex) to historical swordfish datasets, creating a massive, biologically-plausible school to stress-test the `PointInstancer` backend without external data dependencies.

### 4. Implementation Roadmap for Agents

| Phase | Task | Deliverable |
| --- | --- | --- |
| **Phase 1** | **Sync & Stream** | Python module that yields `(frame, telemetry_vector)` pairs. |
| **Phase 2** | **VSS Indexing** | Milvus/VectorDB populated with VLM captions of "Interesting" segments. |
| **Phase 3** | **HUD Overlay** | Media player UI with real-time telemetry gauges (OpenCV/Streamlit). |
| **Phase 4** | **Digital Twin** | Omniverse extension that animates the shark rig from the UDP stream. |

### 5. Deployment Hardware Map

- **RTX 5080 (eGPU):**
  - YOLOv11 / VLM Batch Inference.
  - Vector Database (Milvus) Hosting.

- **AGX Thor (DevKit):**
  - **Omniverse USD Composer** (Rendering).
  - Real-time AHRS Filter implementation.
  - Interactive Dashboard Frontend.

### 6. Scalability: Multi-Animal Simulation

**Feasibility:** High. The proposed hardware stack (RTX 5080 + AGX Thor) is capable of simulating multiple animals in parallel.

- **Batch Processing (RTX 5080):** Can handle parallel ingestion streams. The bottleneck will be I/O, not compute.
- **Real-Time Visualization (AGX Thor):** Omniverse is designed for complex scenes. Rendering a "school" of digital twins (e.g., 5-10 individuals) is well within the rendering budget, provided assets are optimized (LODs).
- **Architecture:** The UDP/ZeroMQ sidecar should be designed to support a `Topic` or `ID` field (e.g., `topic="shark_01"`, `topic="swordfish_03"`) to route telemetry to the correct 3D asset in the scene.

### Final Implementation Note for AI Agents

> "Prioritize **Zero-Copy memory access**. When moving frames from the video decoder to YOLOv11, use `PyTorch.from_dlpack` to keep the data on the GPU. The IMU data should be handled in a non-blocking `multiprocessing` queue to ensure the visualization frame rate does not stutter during heavy computation."

---

## Implementation Priorities

### Phase 1: Lab/RCompat Mode (IMMEDIATE)

**Goal**: Perfect tie-out with R results

- [x] Root cause identified (centered vs causal filter)
- [ ] Implement `filtfilt` option in `streaming_gsep()`
- [ ] Add `mode` parameter to `StreamingProcessor`
- [ ] Lock mag offsets (from pre-deployment calibration)
- [ ] Lock attachment angles (from batch computation)
- [ ] Validate: <0.1° pitch/roll error vs R
- [ ] Regenerate swordfish passthrough CSV
- [ ] Confirm: <100m trajectory difference vs R

**Timeline**: 1-2 days
**Success Metric**: Correlation >0.999 with R on all orientation variables

### Phase 2: Digital Twin v1 (EMA Crossover)

**Goal**: First iteration causal mode with selective logging

- [ ] Implement fast/slow EMA crossover
- [ ] Tune alpha values for marine species
- [ ] Add crossover-based logging triggers
- [ ] Optional mag offset lock
- [ ] Optional attachment angle lock (scientist request)
- [ ] Test on historical data
- [ ] Estimate battery life savings

**Timeline**: 3-5 days
**Success Metric**: <1° pitch/roll lag, 90% data reduction achieved

### Phase 3: Digital Twin v2 (Madgwick)

**Goal**: Leverage existing adaptive sensor fusion

- [ ] Integrate with `biologger_pseudotrack/adaptive_sensor_fusion/`
- [ ] Madgwick filter for gyro-equipped tags
- [ ] Adaptive filter gains
- [ ] Validate on multi-sensor datasets

**Timeline**: 1-2 weeks
**Success Metric**: <0.2° error in steady state

### Phase 4: Digital Twin v3 (GPU)

**Goal**: Advanced capabilities for next-gen tags

- [ ] Particle filter implementation
- [ ] Neural network integration
- [ ] Power budget analysis
- [ ] Prototype on development board

**Timeline**: Research phase (months)
**Success Metric**: Proof-of-concept demonstration

---

## Execution: New Repository Setup (biologger-sim)

**Status**: Planning
**Target Hardware**: RTX 5080 (Windows/WSL) + AGX Thor (Edge)
**Goal**: Create a hybrid edge-cloud digital twin platform for pelagic species.

### 1. Repository Structure & Access Strategy

**Recommendation**: Use a **Monorepo** (`biologger-sim`) to keep shared configs and message schemas in sync.

**Access Method**: **VS Code Remote - WSL** (Primary)

- **Why**: 80% of the code (Backend Edge, AI Services, Docker configs) is Linux-native.
- **Workflow**:
    1. Clone the repo into your WSL 2 filesystem (e.g., `~/projects/biologger-sim`).
    2. Open VS Code in WSL (`code .`).
    3. **For Windows Viz**: You can edit the `frontend_viz` Python files in WSL. To run them, use the Windows Python interpreter (bundled with Omniverse) via a PowerShell terminal in VS Code, pointing to the WSL path (e.g., `\\wsl.localhost\Ubuntu\home\user\projects\...`).
    4. **Alternative**: Use the "Reopen Folder locally" option in VS Code only when strictly working on the Windows rendering loop, but the WSL-first approach is cleaner for a hybrid stack.

```text
biologger-sim/
├── src/                       # Backend Logic (Linux/WSL)
│   └── biologger_sim/         # Python Package
│       ├── core/              # Telemetry & State Management
│       ├── io/                # ZMQ Publishing & Data Loading
│       └── simulation/        # Digital Twin Algorithms (EMA, Madgwick)
│
├── omniverse/                 # Visualization (Windows/RTX)
│   ├── apps/                  # Kit App configurations (.kit files)
│   ├── assets/                # USD stages and models
│   └── extensions/            # Custom Kit Extensions
│       └── whoimpg.biologger.subscriber/
│           ├── extension.py   # Main entry point & UI logic
│           └── ...
│
├── services_ai/               # Runs on WSL 2 (RTX 5080)
│   ├── vss_pipeline/          # Video Search & Summarization
│   │   ├── ingestion.py       # FFMPEG chunking
│   │   ├── inference.py       # YOLOv11 / VILA (NIMs)
│   │   └── vector_db.py       # Milvus interaction
│   └── environment.yml        # Micromamba env for AI (PyTorch, Milvus, Ultralytics)
│
├── docs/                      # Documentation
└── scripts/                   # Deployment & Setup scripts

### Repository Strategy: Development vs. Production

**Recommendation**: **Monorepo for Development, Logical Separation for Release.**

*   **Development Phase**: Keep all components (`src`, `omniverse`, `services_ai`) in a single `biologger-sim` repository. This ensures the ZeroMQ message schemas stay in sync and simplifies full-stack testing.
*   **Productization Phase**:
    *   **The Product (AGX Thor)**: The `src` code is deployed to the hardware (containerized). The customer treats this as a "black box".
    *   **The Client (Viz App)**: The `omniverse` code is packaged as a standalone Omniverse Extension or Kit App installer. The customer installs this on their Windows machine.
    *   **Benefit**: You can ship the hardware without exposing the source code, and distribute the viewer separately, all while managing a single codebase.
```

### 2. Architecture & Data Flow

#### A. The "Brain" (Backend Edge) - AGX Thor

- **Mode**: Headless (No GUI).
- **Runtime**: Isaac Sim (Python API) or Omniverse Kit (Headless).
- **Responsibility**:
    1. **Ingest**: Reads raw sensor data (Accel, Gyro, Mag, Depth).
    2. **Process**: Runs the AHRS filter (Madgwick) and Saliency Filter.
    3. **Simulate**: Updates the "True State" of the digital twin in a headless USD stage.
    4. **Publish**: Broadcasts state updates via ZeroMQ (`pub-sub`).
- **Deployment**: Can be shipped as a standalone "Black Box".

#### B. The "Eye" (Frontend Viz) - Windows Native

- **Mode**: GUI (High-Fidelity Rendering).
- **Runtime**: Omniverse USD Composer (formerly Create).
- **Responsibility**:
    1. **Subscribe**: Listens to ZeroMQ stream from Thor.
    2. **Render**: Updates the visual rig (bones/joints) in real-time.
    3. **Display**: Provides the interactive dashboard for the user.

#### C. The "Librarian" (Services AI) - WSL 2

- **Mode**: Batch / Service.
- **Runtime**: Docker / Python.
- **Responsibility**:
    1. **Index**: Processes video logs for VSS.
    2. **Search**: Handles natural language queries.

### 3. Dependency Management

We will use separate `environment.yml` files because the dependencies are platform-specific.

#### Version Compatibility (Enterprise 25H1 Target)

- **Omniverse Kit**: 106.0+ (Foundation for 2025 apps)
- **Isaac Sim**: 4.5+ (Likely version for 25H1)
- **USD Composer**: 2024.1+ (or latest Enterprise release)
- **Python**: 3.12 (Updated for PB 25h1)
- **USD Core**: 25.02

#### A. `backend_edge/environment.yml` (Linux/aarch64 for Thor)

- **Base**: Python 3.12 (Standard for PB 25h1).
- **Key Packages**:
  - `isaac-sim` (or `isaac-lab`): Physics & Simulation.
  - `pxr-usd`: USD Core libraries (25.02).
  - `pyzmq`: Networking.
  - `numpy` (2.x), `scipy`: Math & Signal Processing.
  - `pyserial`: Sensor ingestion.

#### B. `frontend_viz/environment.yml` (Windows/x86_64)

- **Base**: Python 3.12 (Bundled with Kit SDK PB 25h1).
- **Key Packages**:
  - `nvidia-omniverse-kit-sdk`: For building extensions.
  - `pyzmq`: Networking (must match backend version).
  - `omni.ui`: UI Toolkit (internal to Kit).

#### C. `services_ai/environment.yml` (Linux/WSL)

- **Base**: Python 3.10/3.11.
- **Key Packages**:
  - `torch`, `torchvision`: Deep Learning.
  - `ultralytics`: YOLOv11.
  - `pymilvus`: Vector DB Client.
  - `ffmpeg-python`: Video processing.
  - `langchain`: VLM orchestration.

### 4. Networking Strategy (ZeroMQ)

To decouple the Thor (Backend) from the Windows PC (Frontend), we use a **Publisher-Subscriber** pattern.

- **Protocol**: TCP (Reliable, LAN) or UDP (Fast, Lossy).
- **Format**: JSON or Binary (Protobuf/Flatbuffers).
- **Topic-Based Routing**:
  - `telemetry/shark_01`: Live pose data.
  - `events/shark_01`: Saliency triggers (e.g., "Breach Detected").

**Example Payload:**

```json
{
  "topic": "telemetry/shark_01",
  "timestamp": 1703894400.123,
  "orientation": [0.707, 0.0, 0.707, 0.0],  // Quaternion (w, x, y, z)
  "tail_angle": 0.45,                       // Radians
  "depth": 15.2                             // Meters
}
```

### 5. NVIDIA Developer / DevKit Checklist (Non-Enterprise)

**Note**: Since we are using the **AGX Thor DevKit** and **RTX 5080** without an Enterprise subscription, we will use the **Developer / Community** versions of the stack.

**Licensing**:

- **Omniverse Standard License**: **Free** for individual developers. Includes full access to USD Composer, Isaac Sim, and Kit SDK.
- **Enterprise License**: ~$9,000/year (Team collaboration, support, advanced security). **Not required** for this project.

#### Phase 0: Environment & Core Components

- [ ] **Create NVIDIA Developer Account**: Required for NGC and SDK downloads (Free).
- [ ] **Install Docker Desktop (Windows)**: Ensure "Use WSL 2 instead of Hyper-V" is checked.
- [ ] **Verify GPU in Docker**: Run `docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi`.
- [ ] **Download Omniverse Launcher (or NGC Containers)**:
  - *Note*: If Launcher is deprecated for devs, use **NGC Containers** directly.
  - **Workstation**: Download **Isaac Sim** container or installer.
  - **Edge (Thor)**: Flash **JetPack 6+** and pull `nvcr.io/nvidia/isaac-sim:latest` (aarch64).
- [ ] **Install Workstation Nucleus**: Use the "Local Nucleus" service (Free for individuals) instead of Enterprise Nucleus.
- [ ] **Download Kit SDK (Community)**: Available via GitHub or Launcher/NGC.

#### Phase 1: Advanced Visualization & Simulation

- [ ] **Configure RTX Real-Time**: Use standard RTX rendering (Path Tracing available in Isaac Sim).
- [ ] **Enable Fabric**: Verify Fabric support in the Developer version of Isaac Sim.
- [ ] **Asset Management**: Use local USD files or the free **NVIDIA Assets** pack.

#### Phase 2: Data Fusion & Streaming

- [ ] **Implement AHRS via Python 3.10/3.12**: Match the Python version of your specific Isaac Sim container (likely 3.10 for Isaac Sim 4.x).
- [ ] **Setup Live-Link Bridge**: ZeroMQ works identically on Enterprise and Community versions.
- [ ] **Edge Deployment**: Run the "Headless Backend" on the AGX Thor using the Isaac Sim Docker container.

#### Phase 3: Final Deployment

- [ ] **Integrate USD**: Ensure asset compatibility with the USD version bundled in your Isaac Sim release.
- [ ] **Deep Link**: (Enterprise feature, may not be available). Use direct IP connection for demos.

### 6. Next Steps

1. **Initialize Repo**: Create the folder structure.
2. **Backend Prototype**: Write a simple Python script that publishes dummy data via ZMQ.
3. **Frontend Prototype**: Create a basic Omniverse Extension that subscribes to ZMQ and prints to console.
4. **Connect**: Link the two prototypes over the local network.

---

## Comparison Matrix

| Feature | Lab Mode | Digital Twin v1 | Digital Twin v2 | Digital Twin v3 |
|---------|----------|-----------------|-----------------|-----------------|
| **Filter** | filtfilt | EMA crossover | Madgwick | Particle filter |
| **Causality** | Acausal | Causal | Causal | Causal |
| **Sensors** | IMU + Mag | IMU + Mag | IMU + Mag + Gyro | All + extras |
| **Latency** | Zero phase | ~1.5s | ~0.5s | ~0.1s |
| **Accuracy** | Maximum | Good | Better | Best (w/uncertainty) |
| **On-tag viable** | No | Yes | Yes | Yes (GPU required) |
| **Data reduction** | 0% (full) | 90% | 90% | 95% |
| **Compute** | Offline | Microcontroller | Microcontroller | GPU |
| **Power** | N/A | ~1W | ~1-2W | ~5-10W |
| **Deployment** | Post-hoc | 3-10x longer | 5-15x longer | Limited by battery |

---

## References

### Key Files

- **R implementation**: `R/gRumble/gRumble/R/StomachTagFunctions.R:339-351`
- **Python streaming**: `biologger_pseudotrack/streaming/processor.py:1265-1310`
- **Adaptive fusion**: `biologger_pseudotrack/adaptive_sensor_fusion/`

### Related Documents

- `docs/analysis/attachment-angle-calibration.md` - Attachment angle methodology
- `docs/analysis/magnetometer-calibration-strategy.md` - Mag calibration approach
- `docs/source/dead-reckoning-methodology.md` - DR algorithm overview
- `docs/planning/digital-twin-roadmap.md` - Detailed v1/v2/v3 roadmap

### Investigation History

- 2025-12-18: Root cause analysis of 2km divergence
  - Identified centered (R) vs causal (Python) filter difference
  - Verified scipy.filtfilt matches R (correlation 0.9994)
  - Designed EMA crossover strategy for causal improvement
  - Architected dual-mode system

---

## Changelog

**2025-12-18**: Initial version

- Documented dual-mode architecture
- Identified filter causality as root cause
- Designed implementation roadmap
- Incorporated EMA crossover innovation
- Outlined new codebase considerations

## Digital Twin Evolution Roadmap

**Document Status**: Living (Planning Phase)
**Created**: 2025-12-18

---

## Vision

Create a progression of increasingly sophisticated "digital twin" processors that simulate what could run on the biologger tag itself, enabling:

- Real-time behavioral classification
- Selective logging (90-95% data reduction)
- Multi-year deployments on smaller species
- On-tag decision making for future smart tags

---

## Evolution Timeline

```text
v1: EMA Crossover          → Immediate (causal, simple)
     ↓ (validate, deploy)
v2: Madgwick Fusion        → 6-12 months (gyro integration)
     ↓ (field test, refine)
v3: GPU Neural/Particle    → 12-24 months (research phase)
```

---

## v1: EMA Crossover (Immediate Deployment)

### Design Philosophy

"The simplest thing that could possibly work on a microcontroller"

### Algorithm

```python
# State: just 6 floats per axis
fast_ema_x = 0.0
slow_ema_x = 0.0
# ... y, z

# Per sample (16 Hz = once every 62.5ms)
fast_ema_x = 0.2 * accel_x + 0.8 * fast_ema_x  # ~3 multiplies
slow_ema_x = 0.02 * accel_x + 0.98 * slow_ema_x
crossover_signal_x = fast_ema_x - slow_ema_x

# Decision (once per second = 16 samples)
if abs(crossover_signal_x) > 1.0 or abs(crossover_signal_y) > 1.0 or abs(crossover_signal_z) > 1.0:
    logging_mode = FULL_RESOLUTION
else:
    logging_mode = SUMMARY_ONLY
```

### Computational Cost

**Per sample**: ~20 FLOPs (6 EMAs × 3 ops each + comparisons)
**Memory**: 24 bytes state (6 floats × 4 bytes)
**Clock**: < 1 µs on ARM Cortex-M4 @ 80 MHz

### Expected Performance

- Pitch/roll lag: ~0.5-1° vs Lab mode
- Trajectory drift: ~500-1000m over deployment
- Event detection: >90% sensitivity for behavioral transitions
- Data reduction: 85-95% (depends on species activity)

### Tuning Parameters

| Parameter | Default | Range | Purpose |
|-----------|---------|-------|---------|
| `alpha_fast` | 0.2 | 0.1-0.3 | Transition sensitivity |
| `alpha_slow` | 0.02 | 0.01-0.05 | Baseline stability |
| `threshold` | 1.0 | 0.5-2.0 | Logging trigger |
| `decision_rate` | 1 Hz | 0.5-2 Hz | How often to evaluate |

**Species-Specific Tuning**:

- **Active (swordfish, tuna)**: alpha_fast=0.3, threshold=0.8
- **Moderate (whale shark)**: alpha_fast=0.2, threshold=1.0
- **Slow (basking shark)**: alpha_fast=0.15, threshold=1.5

### Implementation Plan

1. **Add to StreamingProcessor** - [x] (current codebase)
   - New parameter: `gsep_mode="ema_crossover"`
   - Maintain backward compatibility with "causal" mode

2. **Validation** (1-2 days)
   - [ ] Test on swordfish dataset
   - [ ] Measure data reduction achieved
   - [ ] Compare accuracy vs Lab mode
   - [ ] Tune alpha values

3. **Integration** (2-3 days)
   - [ ] Connect to behavioral classifiers
   - [ ] Implement logging triggers
   - [ ] Add diagnostic outputs

4. **Documentation** (1 day)
   - [ ] User guide for parameter tuning
   - [ ] Performance benchmarks
   - [ ] Example configs per species

### Deployment Readiness

**Ready for**:

- [x] Simulation/validation (Python)
- [ ] Embedded prototype (need C port)
- [ ] Field test (need tag integration)

**Next Steps**:

- [ ] Port to C for microcontroller
- [ ] Integrate with existing tag firmware
- [ ] Lab test on development boards
- [ ] Sea trial on captive animal

---

## v2: Madgwick-Inspired Fusion (6-12 months)

### Design Philosophy

"Leverage quaternions and gyroscopes for best causal accuracy"

### Prerequisites

- [x] Tag hardware with gyroscope (most modern tags have this)
- [x] Existing `adaptive_sensor_fusion/` module in codebase
- [ ] Dataset with gyro data for validation
- [ ] IMU ground truth for calibration

### Algorithm Enhancements

**Current v1**:

```python
# Static accel from EMA crossover
pitch, roll = pitchRoll2(ema_crossover_static_accel)
```

**Enhanced v2**:

```python
# Quaternion-based orientation tracking
q = madgwick_update(q, accel, gyro, mag, dt)
pitch, roll, yaw = quaternion_to_euler(q)

# Adaptive filter gain based on motion detection
beta = compute_adaptive_beta(accel_variance, gyro_magnitude)
```

### Key Improvements

1. **Gyroscope integration**: Tracks orientation between samples
2. **Quaternion math**: No gimbal lock, smooth rotations
3. **Adaptive gains**: Higher trust in gyro during fast maneuvers
4. **Better heading**: Magnetometer + gyro fusion for yaw

### Expected Performance

- Pitch/roll error: <0.2° in steady state
- Dynamic tracking: Better during rapid turns/dives
- Heading stability: Reduced magnetic interference sensitivity
- Trajectory drift: ~200-400m over deployment

### Computational Cost

**Per sample**: ~100 FLOPs (quaternion update)
**Memory**: 64 bytes state (quaternion + gains + buffers)
**Clock**: ~5 µs on ARM Cortex-M4 @ 80 MHz

Still fits on microcontroller!

### Implementation Leverages Existing Code

From `biologger_pseudotrack/adaptive_sensor_fusion/madgwick_filter.py`:

```python
class MadgwickAHRS:
    def updateIMU(self, gx, gy, gz, ax, ay, az):
        # Already implemented!
        # Just need to integrate into streaming processor
```

### Development Path

1. [ ] Extract Madgwick filter to standalone module
2. [ ] Add causal/streaming mode (no future data)
3. [ ] Integrate with Digital Twin processor
4. [ ] Validate on gyro-equipped datasets
5. [ ] Tune beta parameter for marine animals
6. [ ] Compare vs v1 (EMA crossover)

---

## v3: GPU-Accelerated Intelligence (12-24 months)

### Design Philosophy

"What if the tag had serious compute power?"

### Hardware Vision

**Target Platforms**:

- **Jetson Nano** (5W, $100): Whale shark, basking shark with solar
- **Coral Dev Board** (2W, $150): Medium pelagics with large battery
- **Custom FPGA** (1-3W): Future miniaturization

**Power Sources**:

- Solar panel (whale shark dorsalshark): 10-20W continuous
- Large Li-ion pack (swordfish, tuna): 100-200 Wh
- Hybrid (charge at surface): Extended missions

### Computational Capabilities

#### 1. Particle Filter Position Tracking

```python
# 1000 particles, each with (x, y, heading, speed)
particles = initialize_particles(n=1000)

for sensor_sample in stream:
    # Propagate (fast on GPU)
    particles = propagate(particles, motion_model, dt)

    # Weight by observation likelihood
    weights = compute_likelihood(particles, sensor_sample)

    # Resample
    particles = resample(particles, weights)

    # Estimate
    position_estimate = weighted_mean(particles, weights)
    uncertainty = weighted_variance(particles, weights)

    # Selective logging
    if uncertainty > threshold:
        log_full_data()
    else:
        log_summary_only()
```

**Advantage**: Quantified uncertainty → smarter logging decisions

#### 2. Neural Network Behavioral Classification

```python
# Real-time CNN inference
features = compute_features(accel, mag, gyro, depth)  # GPU
behavior_probs = neural_net.forward(features)  # GPU accelerated

if max(behavior_probs) > confidence_threshold:
    predicted_behavior = argmax(behavior_probs)
    log_summary(predicted_behavior)
else:
    log_full_data()  # Model uncertain
    update_online(features, true_label)  # Learn from mistakes
```

**Advantage**: Continuous learning, adapts to individual animal

#### 3. Monte Carlo Trajectory Simulation

```python
# Simulate multiple possible trajectories
trajectories = []
for i in range(100):
    traj = simulate_trajectory(
        start=gps_last_surface,
        sensors=sensor_history,
        uncertainty=current_uncertainty
    )
    trajectories.append(traj)

# Predictive planning
if any(traj.intersects_geofence() for traj in trajectories):
    trigger_surfacing()  # Get GPS fix before entering restricted area
```

**Advantage**: Predictive behavior, autonomous mission planning

### Expected Performance

- Position accuracy: ~100m (with GPS corrections)
- Behavioral classification: >95% accuracy
- Adaptive learning: Improves over deployment
- Mission planning: Autonomous surfacing decisions

### Computational Requirements

- **GPU**: ~100 GFLOPS for neural nets
- **Memory**: ~1-2 GB for models + buffers
- **Storage**: ~10-50 GB for logged data + models

### Development Path

1. **Proof-of-concept** (desktop Python/PyTorch)
   - [ ] Particle filter on historical data
   - [ ] Neural net training on labeled data
   - [ ] Validate uncertainty calibration

2. **Embedded prototyping** (Jetson Nano)
   - [ ] Port to TensorRT for inference
   - [ ] Optimize particle filter (CUDA kernels)
   - [ ] Power profiling

3. **Sea trials** (large animal, short deployment)
   - [ ] Whale shark with solar panel (days-weeks)
   - [ ] Validate in realistic conditions
   - [ ] Iterate on algorithms

4. **Production** (custom hardware)
   - [ ] Design application-specific board
   - Optimize power management
   - Long-term deployments

---

## Comparison Matrix

| Capability | v1 (EMA) | v2 (Madgwick) | v3 (GPU) |
|------------|----------|---------------|----------|
| **Compute** | 20 FLOP | 100 FLOP | 100 GFLOP |
| **Memory** | 24 B | 64 B | 1-2 GB |
| **Power** | <0.1 W | ~0.5 W | 5-10 W |
| **Accuracy** | Good | Better | Best |
| **Sensors** | IMU+Mag | IMU+Mag+Gyro | All sensors |
| **Learning** | No | No | Yes (online) |
| **Deployment** | 3-10x | 5-15x | Limited by battery |
| **Cost** | $500 | $600 | $1500+ |

---

## Migration Path

### From v1 → v2

**Trigger**: Gyro data available, validated on real deployments

**Strategy**: Feature flag in config

```yaml
digital_twin:
  version: "v2_madgwick"  # vs "v1_ema_crossover"
  madgwick:
    beta: 0.1  # Tuning parameter
```

**Timeline**: 6-12 months after v1 field trials

### From v2 → v3

**Trigger**: Funding secured, hardware prototype validated

**Strategy**: Separate deployment class (large animals only initially)

**Timeline**: Research phase, 12-24+ months

---

## Success Metrics

### v1 Milestones

- [ ] <1° pitch/roll lag vs Lab mode
- [ ] >90% data reduction achieved
- [ ] Validated on 3+ species
- [ ] C port running on development board
- [ ] Field trial on captive animal

### v2 Milestones

- [ ] <0.2° error in steady state
- [ ] Gyro integration validated
- [ ] Better than v1 in dynamic maneuvers
- [ ] Deployed on 2+ species with gyro tags

### v3 Milestones

- [ ] Particle filter proof-of-concept
- [ ] Neural net >95% accuracy
- [ ] Power budget validated (Jetson Nano)
- [ ] Short deployment success (days-weeks)
- [ ] Path to long deployment identified

---

## Risk Mitigation

### v1 Risks

- **Alpha tuning species-specific**: Solution: Auto-tuning from initial samples
- **False positives/negatives**: Solution: Adjustable threshold, validate on labeled data

### v2 Risks

- **Gyro drift**: Solution: Regular mag corrections, adaptive beta
- **Quaternion complexity**: Solution: Leverage existing tested code

### v3 Risks

- **Power budget**: Solution: Start with large animals + solar, iterate
- **Hardware cost**: Solution: Prototype on COTS, scale with custom board
- **Software complexity**: Solution: Extensive simulation before deployment

---

## Next Actions

- [x] Document architecture (this file)
- [ ] Implement v1 in current codebase
- [ ] Validate v1 on historical data
- [ ] Port v1 to C for embedded testing
- [ ] Design v2 integration strategy
- [ ] Research v3 hardware options

---

## See Also

- `dual-mode-architecture.md` - Overall system design
- `new-codebase-bootstrap-plan.md` - Future codebase structure
- `../analysis/attachment-angle-calibration.md` - Calibration methodology
- `../source/adaptive_sensor_fusion_migration_guide.md` - v2 starting point
