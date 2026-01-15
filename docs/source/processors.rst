Core Processors
===============

The ``biologger-sim`` package is built around a pluggable processor architecture that allows researchers to switch between real-time (causal) and post-facto (acausal) processing logic.

Processor Types: Lab vs. Simulation
===================================

The system supports two primary processor types designed for different stages of the research lifecycle:

.. list-table:: Processor Comparison
   :widths: 20 40 40
   :header-rows: 1

   * - Feature
     - PostFactoProcessor (Acausal)
     - StreamingProcessor (Causal)
   * - **Primary Goal**
     - Highest possible accuracy (Lab)
     - On-tag real-time execution
   * - **Processing**
     - Multi-pass, assumes lookahead
     - Single-pass, strictly causal
   * - **Filter Style**
     - ``filtfilt`` (Zero-phase)
     - ``lfilter`` (IIR/Butterworth)
   * - **Memory**
     - Full record set (O(N))
     - Fixed window (O(1))
   * - **Hardware**
     - High-performance workstations
     - Resource-constrained tags

---

PostFactoProcessor (Acausal)
============================

The ``PostFactoProcessor`` is the reference implementation used in **Lab Mode** (configured via ``strict_r_parity: true``). It is optimized for scientific validation and retrospective analysis.

Provenance & Portability
------------------------

This processor is a direct Python port of established R-based biologger analysis scripts (specifically from the ``gRumble`` and ``biologger-pseudotrack`` ecosystems). Its primary purpose is to maintain a "Gold Standard" baseline for verifying real-time algorithm performance.

Methodology: Batch Retrospective Analysis
-----------------------------------------

Unlike the streaming version, this processor has access to the entire dataset simultaneously, allowing for high-accuracy acausal techniques:

1.  **Full Dataset Buffering**: All sensor records are loaded into a collection buffer before any analysis begins.
2.  **Batch Calibration**:
    - **Attachment Angles**: Computes body-frame alignment by averaging the gravity vector across the entire deployment.
    - **Magnetometer**: Fits a sphere to the total magnetic sample cloud to find precise hard-iron offsets.
3.  **Zero-Phase Filtering**: Uses a centered moving average (R-style ``filter(sides=2)``) or ``filtfilt`` to eliminate phase shift and group delay.
4.  **Acausal Interpolation**: Uses linear interpolation to fill gaps in pressure sensor or velocity data before smoothing.
5.  **Velocity Decoupling**: A key mechanical distinction is how it handles motion:
    - **Horizontal Integration**: Constant speed (typically 1.0 m/s) is integrated purely in the horizontal plane (X-Y).
    - **Vertical Derivation**: Vertical velocity is derived post-hoc from the rate of change of smoothed depth data.
    - **Impact**: Because the 1.0 m/s speed is forced into the 2D plane, the animal's total trajectory length is effectively overestimated during steep maneuvers compared to a 3D-aware model.

---

StreamingProcessor (Causal)
===========================

The ``StreamingProcessor`` is the core of the **Digital Twin** mode. It simulates the constraints of a physical biologger tag where data arrives one sample at a time and future data is unknown.

Methodology: The 11-Step Causal Pipeline
----------------------------------------

The processor follows a strictly sequential, low-latency pipeline:

1.  **Input Acquisition**: Raw acceleration (0.1g counts), magnetometer, and pressure depth.
2.  **Attachment Correction**: Fixed roll/pitch rotation to align sensor axes with the animal's body.
3.  **Causal Gsep**: 3-second trailing window for gravity separation (Static vs. Dynamic).
4.  **Dead Reckoning Timing**: Dynamic ``dt`` calculation to handle sensor jitter.
5.  **R-Style Orientation**: Pitch/Roll from gravity using legacy-compatible formulas.
6.  **World Frame Transform**: Body-to-World (NED) rotation of acceleration.
7.  **High-Pass Filtering**: 4th-order causal bias removal for vertical acceleration.
8.  **INS Depth Estimation**: 2-state Kalman Filter nowcast (fusing Baro + Accel).
9.  **Multi-Scale Smoothing**: Activity-weighted blending of Fast/Slow EMAs for depth.
10. **Magnetometer & Heading**: Hard-iron compensated, tilt-corrected heading estimation.
11. **Dead Reckoning Integration**: Updates position using heading and speed (constant or ODBA-scaled). Unlike the Lab mode, this model is designed to support 3D-aware displacement.

Configuration Parameters
------------------------

Streaming processors are configured via the ``entities`` section in the simulation YAML:

*   **filt_len**: (Default: 48) Length of the causal Gsep window (in samples).
*   **freq**: (Default: 16) Sampling frequency for filters and integration.
*   **locked_attachment_roll_deg / locked_attachment_pitch_deg**: Fixed calibration angles.
*   **locked_mag_offset_x/y/z / locked_mag_sphere_radius**: Hard-iron calibration parameters.

Advantages & Inherent Disadvantages
-----------------------------------

**Advantages**:

* **Real-Time Visibility**: Allows for "nowcasting" depth and position with zero lag.
* **Portability**: Code is designed to be easily transcribed to C/C++/Warp for embedded tags.
* **Scalability**: Can simulate hundreds of entities in parallel due to fixed memory overhead.

**Disadvantages (The Cost of Causality)**:

* **Filter Phase Shift**: Causal filters (like Butterworth) introduce a small group delay in the signal.
* **Initialization (Warmup)**: Requires a short "warmup" period (e.g., 3s) for averaging windows to fill.
* **Noise Sensitivity**: Lacks the benefit of centered averaging (``filtfilt``), making signals inherently noisier than their lab counterparts.

---
