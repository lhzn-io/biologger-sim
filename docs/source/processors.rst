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
     - StreamingProcessor (Causal)
     - PostFactoProcessor (Acausal)
   * - **Primary Goal**
     - On-tag real-time execution
     - Highest possible accuracy (Lab)
   * - **Processing**
     - Single-pass, strictly causal
     - Multi-pass, assumes lookahead
   * - **Filter Style**
     - ``lfilter`` (IIR/Butterworth)
     - ``filtfilt`` (Zero-phase)
   * - **Memory**
     - Fixed window (O(1))
     - Full record set (O(N))
   * - **Hardware**
     - Resource-constrained tags
     - High-performance workstations

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
11. **Dead Reckoning Integration**: Position update via heading and speed (constant or ODBA-scaled).

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
- **Real-Time Visibility**: Allows for "nowcasting" depth and position with zero lag.
- **Portability**: Code is designed to be easily transcribed to C/C++/Warp for embedded tags.
- **Scalability**: Can simulate hundreds of entities in parallel due to fixed memory overhead.

**Disadvantages (The Cost of Causality)**:
- **Filter Phase Shift**: Causal filters (like Butterworth) introduce a small group delay in the signal.
- **Initialization (Warmup)**: Requires a short "warmup" period (e.g., 3s) for averaging windows to fill.
- **Noise Sensitivity**: Lacks the benefit of centered averaging (``filtfilt``), making signals inherently noisier than their lab counterparts.

---

PostFactoProcessor (Acausal)
============================

The ``PostFactoProcessor`` is used in **Lab Mode** (configured via ``strict_r_parity: true``). It is optimized for validation against established R implementations.

Methodology
-----------

Unlike the streaming version, this processor:
1.  Loads the **entire dataset** first.
2.  Performs **batch calibration** (finding the optimal attachment angles and mag offsets from the whole file).
3.  Uses **zero-phase filters** (``filtfilt``) which process the data both forward and backward to eliminate phase shift.
4.  Applies **linear interpolation** for depth gaps before any processing.

---

API Reference
=============

Streaming Processor
-------------------

.. automodule:: biologger_sim.processors.streaming
   :members:
   :undoc-members:
   :show-inheritance:

Lab Processor (Post-Facto)
--------------------------

.. automodule:: biologger_sim.processors.lab
   :members:
   :undoc-members:
   :show-inheritance:
