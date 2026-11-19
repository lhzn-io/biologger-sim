Core Processors
===============

The ``biologger-sim`` package is built around interchangeable processors, so researchers can switch
between real-time (causal) and post-facto (acausal) processing.

Processor Types: Lab vs. Simulation
===================================

The package has two processor types, for different stages of the research workflow:

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
     - Centered moving average (zero-phase)
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

The ``PostFactoProcessor`` is the reference implementation. It runs every entity in **Lab Mode**
(``mode: LAB``), and any Simulation Mode entity with ``strict_r_parity: true``. It is built for
scientific validation and retrospective analysis.

Provenance & Portability
------------------------

This processor is a direct Python port of established R biologger analysis scripts, from
``gRumble`` and ``biologger-pseudotrack``. Its main purpose is to provide a reference baseline
for checking the performance of the real-time algorithms.

Methodology: Batch Retrospective Analysis
-----------------------------------------

Unlike the streaming processor, this processor sees the entire dataset at once, so it can use
more accurate acausal techniques:

1.  **Full Dataset Buffering**: All sensor records are loaded into a buffer before any analysis
    begins.
2.  **Batch Calibration**:

    - **Attachment Angles**: Computes the body-frame alignment by averaging the gravity vector
      across the entire deployment.
    - **Magnetometer**: Fits a sphere to all magnetometer samples to find the hard-iron offsets.

3.  **Zero-Phase Filtering**: Uses a centered moving average (R-style ``filter(sides=2)``), which
    has no phase shift or group delay.
4.  **Acausal Interpolation**: Fills gaps in pressure-sensor or velocity data by linear
    interpolation before smoothing.
5.  **Velocity Decoupling**: The processor handles horizontal and vertical motion separately:

    - **Horizontal Integration**: A constant speed (typically 1.0 m/s) is integrated only in the
      horizontal plane (X-Y).
    - **Vertical Derivation**: Vertical velocity is computed afterward from the rate of change of
      the smoothed depth.
    - **Impact**: The horizontal distance covered each second is fixed at the set speed,
      whatever the pitch. During steep dives or climbs the horizontal distance is therefore
      likely overestimated, compared with a model that applies 1.0 m/s along the body axis
      (where only the cos(pitch) share of that speed is horizontal).

---

StreamingProcessor (Causal)
===========================

The ``StreamingProcessor`` drives the **Digital Twin** mode. It simulates the constraints of a
physical biologger tag, where data arrives one sample at a time and future data is unknown.

Methodology: The Causal Pipeline (12 Steps)
-------------------------------------------

The processor runs these steps in strict order, with low latency:

1.  **Input Acquisition**: Raw acceleration (0.1 g counts), magnetometer, and pressure depth.
2.  **Attachment Correction**: Fixed roll and pitch rotation that aligns the sensor axes with the
    animal's body.
3.  **Causal Gsep**: 3-second trailing window (48 samples at 16 Hz) that separates gravity
    (static) from dynamic acceleration.
4.  **Dead Reckoning Timing**: ``dt`` from consecutive timestamps, to handle sensor jitter.
5.  **R-Style Orientation**: Pitch and roll from gravity, with legacy-compatible formulas.
6.  **World Frame Transform**: Body-to-world (NED) rotation of the vertical acceleration
    component.
7.  **High-Pass Filtering**: 2nd-order Butterworth (0.1 Hz) causal filter that removes bias from
    the vertical acceleration.
8.  **INS Depth Estimation**: 2-state Kalman Filter nowcast, fusing pressure depth and
    acceleration.
9.  **Multi-Scale Smoothing**: Blends fast, medium and slow exponential moving averages (EMAs;
    3, 12 and 45 s) of depth, weighted by activity.
10. **Magnetometer & Heading**: Tilt-compensated heading with hard-iron correction.
11. **Dead Reckoning Integration**: Updates the horizontal position from heading and speed
    (ODBA-scaled by default, or constant). Like Lab mode, it integrates in the horizontal plane
    only.
12. **Terrain & Altitude Processing**: Estimates GPS coordinates from the deployment's start
    location and the dead-reckoned displacement. Queries the central ``topobathykit`` elevation
    service for zoom 11 tiles. Computes the animal's height above the seafloor and streams it to
    the visualizer.

Configuration Parameters
------------------------

The ``entities`` section of the simulation YAML configures the streaming processors:

*   **sampling_rate_hz**: (Default: 16) Sampling frequency for filters and integration. The
    pipeline passes it to the processor as ``freq``.
*   **calibration.locked_attachment_roll_deg / locked_attachment_pitch_deg**: Fixed calibration
    angles.
*   **calibration.locked_mag_offset_x/y/z / locked_mag_sphere_radius**: Hard-iron calibration
    parameters.

The Gsep window length, ``filt_len``, is a constructor argument of ``StreamingProcessor``, not a
config key. The pipeline always uses its default of 48 samples, which spans 3 s only at 16 Hz.

Advantages & Inherent Disadvantages
-----------------------------------

**Advantages**:

* **Real-Time Visibility**: Updates depth and position at every sample, using no future samples.
* **Portability**: The code is written to be easy to port to C, C++ or Warp for embedded tags.
* **Scalability**: Fixed memory per entity lets hundreds of entities run in parallel.

**Disadvantages (The Cost of Causality)**:

* **Filter Delay**: The causal filters lag the signal. The 48-sample trailing mean delays the
  gravity estimate, and so pitch, roll and heading, by 23.5 samples (about 1.5 s at 16 Hz). The
  2nd-order Butterworth high-pass (0.1 Hz) delays vertical acceleration by about 2.3 s at the
  cutoff and by less than 0.1 s above 0.5 Hz. The depth EMAs add further lag to the smoothed
  depth.
* **Initialization (Warmup)**: The averaging windows need a short warmup period (for example
  3 s) to fill.
* **Noise Sensitivity**: Without centered averaging, the signals are noisier than
  their Lab Mode equivalents.

---
