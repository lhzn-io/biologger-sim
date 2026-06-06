# Apple Silicon / MLX Metal Optimization Planning & Analysis

This document consolidates the technical evaluation, benchmarks, and implementation plan for adding hardware-specific optimizations for Apple Silicon using Apple's MLX framework to the `biologger-sim` repository.

---

## 1. Technical Evaluation & Benchmarks

A prototype of the simulation pipeline was implemented in MLX and benchmarked on the laboratory compute node `garnet` (Mac Studio, M4 Max, 128 GB Unified Memory). 

* **High-Throughput Parallelism:** When processing large swarms (50,000+ entities) with large batch sizes, the MLX GPU backend achieves **30.7M - 30.9M Samples Per Second (SPS)**.
* **Comparison to NumPy:** For massive blocks, the MLX GPU backend is **3x faster** than vectorized NumPy and **100x faster** than sequential NumPy.
* **Unified Memory Advantage:** On Apple Silicon, unified memory allows the GPU to access CPU-allocated system memory directly. This eliminates the PCIe copy latency that commonly bottlenecks discrete GPU setups.
* **JIT Compilation Model:** Rather than manually writing Metal Shading Language (MSL) code, the prototype leverages Python JIT compilation via `mlx.core.compile`. The MLX graph compiler automatically detects state array modifications and optimizes them to run in-place on the GPU if no other reference to the array is held, ensuring high efficiency.

### Benchmark Results (SPS - Samples Per Second)

| Swarm Size | Update Block Size | NumPy Sequential | NumPy Vectorized | MLX CPU | MLX GPU (Metal) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **50,000** | **1,000** | 0.29M SPS | **5.95M SPS** | 1.23M SPS | 1.84M SPS |
| **200,000** | **50,000** | (Too slow) | 10.79M SPS | 5.42M SPS | **30.94M SPS** |
| **500,000** | **100,000** | (Too slow) | 9.89M SPS | 4.48M SPS | **30.73M SPS** |

---

## 2. Proposed Implementation Plan

To integrate the Apple Silicon optimization without disrupting existing CUDA support, we will implement a pluggable `mlx` backend.

### Component 1: Configuration Updates

#### [MODIFY] [types.py](file:///wsl.localhost/Ubuntu-24.04/home/lhzn/Projects/whoi-mpg/biologger-sim/src/biologger_sim/core/types.py)
* Add `"mlx"` to the documented options for the `backend` configuration field in `SimulationConfig`.

---

### Component 2: MLX Processor Class

#### [NEW] [mlx_tensor.py](file:///wsl.localhost/Ubuntu-24.04/home/lhzn/Projects/whoi-mpg/biologger-sim/src/biologger_sim/processors/mlx_tensor.py)
* Create `MLXInertialTensorProcessor` implementing `BiologgerProcessor`.
* Keep sliding window history in an MLX array of shape `(num_entities, filt_len, 3)`.
* Define an update step JIT-compiled with `@mlx.core.compile` to update the ring buffer history, calculate static gravity vectors, and compute orientation (Roll, Pitch, World-Z acceleration).
* Accept indices and raw accelerometer inputs, perform batched updates, run evaluation via `mx.eval()`, and return calculated kinematics.

---

### Component 3: Runner Integration

#### [MODIFY] [__main__.py](file:///wsl.localhost/Ubuntu-24.04/home/lhzn/Projects/whoi-mpg/biologger-sim/src/biologger_sim/__main__.py)
* Under `run_simulation_mode`, add logic to check if `backend == "mlx"`.
* If true, initialize `MLXInertialTensorProcessor` and set `use_parallel_mode = True`.
* Log initialization details and handle potential `ImportError` gracefully if `mlx` is not installed on the system.

---

### Component 4: Configurations and Dependencies

#### [NEW] [Swordfish-RED001_20220812_19A0564-causal-mlx.yaml](file:///wsl.localhost/Ubuntu-24.04/home/lhzn/Projects/whoi-mpg/biologger-sim/config/Swordfish-RED001_20220812_19A0564-causal-mlx.yaml)
* Set `backend: mlx`.
* Set entity `sim_id: sword_causal_mlx` to ensure output files are named `sword_causal_mlx_output.csv` (avoiding overlap with standard runs).

#### [MODIFY] [pyproject.toml](file:///wsl.localhost/Ubuntu-24.04/home/lhzn/Projects/whoi-mpg/biologger-sim/pyproject.toml)
* Add `mlx` to optional dependencies (under `gpu` or a new `mlx` list depending on target platform mapping).

---

## 3. Verification Plan

### Automated Verification
* Execute the benchmark runner `benchmark_mlx.py` on the `garnet` Mac Studio node to confirm the MLX JIT execution pathways compile and run correctly on Metal.

### Manual Verification
* Run the new configuration:
  ```bash
  python -m biologger_sim run --config config/Swordfish-RED001_20220812_19A0564-causal-mlx.yaml
  ```
* Verify that:
  1. The simulation starts and prints: `Initializing MLXInertialTensorProcessor (Back-end: MLX/Metal)...`
  2. Telemetry and processed data are published successfully to ZeroMQ.
  3. Output files are saved correctly to the run directory as `sword_causal_mlx_output.csv` without overwriting the default `sword_causal_output.csv` or `sword_postfacto_output.csv`.

---

## 4. Implementation Walkthrough & Verification Results

The implementation plan was successfully executed and verified on the compute node `garnet` (Mac Studio, Apple M4 Max, 128 GB Unified Memory).

### Changes Implemented
* **Configuration:** Documented the `"mlx"` backend option in [types.py](file:///wsl.localhost/Ubuntu-24.04/home/lhzn/Projects/whoi-mpg/biologger-sim/src/biologger_sim/core/types.py).
* **Core Logic:** Implemented `MLXInertialTensorProcessor` in [mlx_tensor.py](file:///wsl.localhost/Ubuntu-24.04/home/lhzn/Projects/whoi-mpg/biologger-sim/src/biologger_sim/processors/mlx_tensor.py) to manage the resident state (history buffer, running sums, pointers, and kinematics outputs) in Apple Silicon GPU Unified Memory and compile the update step via `@mlx.core.compile`.
* **Runner:** Modified [__main__.py](file:///wsl.localhost/Ubuntu-24.04/home/lhzn/Projects/whoi-mpg/biologger-sim/src/biologger_sim/__main__.py) to initialize the MLX processor and enable vectorized parallel mode if the backend is configured to `"mlx"`.
* **Configs & Dependencies:** Created [Swordfish-RED001_20220812_19A0564-causal-mlx.yaml](file:///wsl.localhost/Ubuntu-24.04/home/lhzn/Projects/whoi-mpg/biologger-sim/config/Swordfish-RED001_20220812_19A0564-causal-mlx.yaml) with unique simulation ids (`sword_causal_mlx` and `sword_postfacto_mlx`), and added the `mlx` dependency target to [pyproject.toml](file:///wsl.localhost/Ubuntu-24.04/home/lhzn/Projects/whoi-mpg/biologger-sim/pyproject.toml).

### Verification & Performance Parity
* **Code Standards:** Run `ruff check` and `mypy` on the host, passing all code quality and static typing checks successfully.
* **Functional Correctness:** Executed the causal MLX simulation on `garnet` via SSH:
  ```bash
  python -m biologger_sim run --config config/Swordfish-RED001_20220812_19A0564-causal-mlx.yaml --uncork
  ```
  The simulation successfully initialized on `gpu` (Metal) and processed all 1,058,000 records at max speed in less than 11 seconds.
* **Output Isolation:** Checked that output files were isolated to `sword_causal_mlx_output.csv` and `sword_postfacto_mlx_output.csv` in the pipeline-runs folder, ensuring zero overwrite of standard CUDA or CPU runs.
* **Data Verification:** Inspected headers and telemetry rows, confirming valid and expected output degrees/forces.
