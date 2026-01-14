=========================================
Pipeline Architecture: Lab vs Simulation
=========================================

The package provides **two distinct processing pipelines** designed for different stages of the research workflow.

Lab Mode (Post-Facto)
=====================

**High-Precision Analysis & Validation**

The Lab Mode pipeline is designed for batch analysis where the complete dataset is available. It aims for parity with the legacy R implementation.

Characteristics
---------------

- **Memory**: Full dataset loaded into memory.
- **Processing**: Acausal algorithms (e.g., `filtfilt`, centered moving averages).
- **Calibration**: Batch computation from the full dataset.
- **Depth**: Acausal interpolation of missing values.

Configuration
-------------

To enable Lab Mode, set the following in your YAML config:

.. code-block:: yaml

   pipeline:
     mode: "LAB"
     calibration:
       attachment_angle: "batch_compute"
       magnetometer: "batch_compute"
     depth:
       mode: "interpolate"
     true_integration: false  # Set to true to use real timestamps for track generation (physically accurate but differs from R)

Clock Drift & Jitter
--------------------
Real hardware sensors often have clock jitter (variable sampling rates).
Legacy R implementations use **Fixed Step Integration** (assuming ``dt = 1/freq``), which ignores this jitter. This produces smooth tracks but mathematically implies that the animal speeds up/slows down inversely to the clock jitter if analyzed against real time.

- **Default Behavior (R-Compatibility)**: Uses fixed ``dt``. Matches legacy R output exactly. Velocity calculated from position/time ratio will show jitter.
- **True Integration (``true_integration: true``)**: Uses actual time deltas (``real_dt``). Matches the physical path to the clock. Velocity is stable, but positions differ slightly from R legacy tracks.

**Diagnostic Output**:
Lab Mode now includes a ``ClockDrift`` column in the output, measuring the deviation between the sensor clock and an ideal clock:
``Drift = Timestamp_Actual - (Start_Time + Index * 1/Freq)``

Simulation Mode (Real-Time)
===========================

**On-Tag Algorithm Development**

The Simulation Mode pipeline is designed for real-time processing where data arrives sample-by-sample. It uses fully causal algorithms with no lookahead.

Characteristics
---------------

- **Memory**: Fixed memory footprint (O(1)).
- **Processing**: Causal algorithms (e.g., `lfilter`, EMA).
- **Calibration**: Online adaptive calibration or fixed parameters.
- **Depth**: Real-time estimation (hold last value or predict).

Configuration
-------------

To enable Simulation Mode, set the following in your YAML config:

.. code-block:: yaml

   pipeline:
     mode: "SIMULATION"
     calibration:
       attachment_angle: "fixed"  # or "progressive" (future)
       magnetometer: "fixed"
     depth:
       mode: "realtime"

Streaming Algorithm (11-Step Architecture)
==========================================

The ``StreamingProcessor`` implements a strictly causal, high-fidelity motion model reconciled with validated post-facto pipelines. Each step processes data as it arrives with O(1) memory footprint.

1. Input Acquisition
--------------------
Raw sensor data is extracted from the input record. Accelerometer values arrive in **0.1g units** (1 count = 0.1g). Magnetometer values are in raw ADC counts.

.. code-block:: python

   ax_m, ay_m, az_m = record["int aX"], record["int aY"], record["int aZ"]
   depth_raw = record["Depth"]

2. Attachment Correction
------------------------
Locked calibration parameters for attachment roll and pitch are applied via rotation matrices (Rx then Ry). This aligns the sensor frame with the animal's body frame.

.. math::

   \vec{a}_{att} = \vec{a}_{raw} \cdot R_x(\phi_{att}) \cdot R_y(\theta_{att})

Where :math:`\phi_{att}` is attachment roll and :math:`\theta_{att}` is attachment pitch.

3. Window Management (Causal Gsep)
----------------------------------
A trailing moving average window of ``filt_len=48`` samples (3 seconds at 16Hz) estimates the static (gravity) component. Dynamic acceleration is the residual.

.. code-block:: python

   static_x = sum(buffer_x) / filt_len
   dyn_x = ax_att - static_x
   odba_g = (|dyn_x| + |dyn_y| + |dyn_z|) / 10.0  # Convert to g

**Warmup Behavior**: During the first 48 samples, static = raw accel, dynamic = 0, ODBA = 0.

4. Dead Reckoning Timing
------------------------
Time delta is computed from sensor timestamps (or fixed ``dt`` if ``clock_source: fixed_frequency``).

5. Orientation (R-style pitchRoll2)
-----------------------------------
Pitch and roll are calculated from the static acceleration vector using R-compatible trigonometric formulas:

.. math::

   \text{pitch} = -\arctan2(a_x^{static}, \sqrt{a_y^2 + a_z^2})

   \text{roll} = \arctan2(a_y^{static}, a_z^{static})

6. World Frame Transformation
-----------------------------
Acceleration is rotated from body frame to world frame (NED convention) and gravity is removed:

.. math::

   a_z^{world} = -\sin(\text{pitch}) \cdot a_x + \cos(\text{pitch})\sin(\text{roll}) \cdot a_y + \cos(\text{pitch})\cos(\text{roll}) \cdot a_z

   a_z^{no\_gravity} = a_z^{world} \times 9.81 - 9.81

7. High-Pass Filter (Bias Removal)
----------------------------------
A 4th-order Butterworth high-pass filter (cutoff 0.05 Hz at 16 Hz sample rate) removes sensor bias and integration drift:

.. code-block:: python

   accel_z_filtered, zi = lfilter(highpass_b, highpass_a, [accel_z_no_gravity], zi=zi)

8. INS Depth Estimation (Kalman Filter)
---------------------------------------
A 2-state Kalman Filter (depth, vertical velocity) fuses:

- **Prediction**: Vertical acceleration integration (16 Hz)
- **Update**: Sparse pressure sensor depth measurements (~1 Hz)

Parameters: ``process_noise_depth=1e-4``, ``process_noise_velocity=1e-3``, ``measurement_noise=0.02``

9. Multi-Scale Depth Smoothing
------------------------------
Adaptive EMA blending based on activity level:

- **Low activity** (ODBA < 0.15): Favor slow EMA (τ=45s)
- **High activity** (ODBA > 0.20): Favor fast EMA (τ=3s)
- **Transition**: Linear blend

10. Magnetometer & Heading
--------------------------
Tilt-compensated magnetic heading using locked hard-iron calibration:

.. code-block:: python

   mx_n = (mx_raw - offset_x) / sphere_radius
   heading = atan2(-my_world, mx_world)

11. Dead Reckoning Integration
------------------------------
Track position is updated using heading and speed:

.. code-block:: python

   pseudo_x += speed * dt * cos(heading)
   pseudo_y += speed * dt * sin(heading)

Speed model: ``constant`` (1.0 m/s) or ``odba_scaled``.


Configuration Reference
=======================

Streaming Mode Entity Configuration
-----------------------------------

The following YAML shows all configuration attributes with their default values:

.. code-block:: yaml

   entities:
     - sim_id: sword_causal              # Unique identifier for this entity
       tag_id: RED001                    # Biological tag ID (for metadata lookup)
       sampling_rate_hz: 16.0            # Sensor sampling rate in Hz
       clock_source: fixed_frequency     # fixed_frequency | sensor_time
       input_file: path/to/data.csv      # Path to input CSV file

       calibration:
         attachment_angle_mode: fixed    # fixed | progressive (future)
         magnetometer_mode: fixed        # fixed | progressive (future)
         # Pre-computed attachment angles (required if mode=fixed)
         locked_attachment_roll_deg: 117.43
         locked_attachment_pitch_deg: -5.99
         # Pre-computed hard-iron calibration (required if mode=fixed)
         locked_mag_offset_x: -21.15
         locked_mag_offset_y: -12.89
         locked_mag_offset_z: 30.27
         locked_mag_sphere_radius: 56.51

       depth_estimation:
         algorithm: causal_sample_hold   # causal_sample_hold | acausal_interp

       dead_reckoning:
         speed_model: constant           # constant | odba_scaled
         constant_speed_m_s: 1.0         # Speed when model=constant

       ahrs:
         enabled: false                  # true = Madgwick filter (future)

       save_telemetry: true              # Write output CSV

Key Configuration Decisions
---------------------------

**clock_source**:

- ``fixed_frequency``: Use nominal dt = 1/sampling_rate. Matches R legacy behavior.
- ``sensor_time``: Use actual timestamp deltas. Physically accurate but differs from R.

**calibration.attachment_angle_mode**:

- ``fixed``: Use pre-computed angles from ``locked_attachment_*_deg``.
- ``progressive`` (future): Online variance-based calibration.

**dead_reckoning.speed_model**:

- ``constant``: Fixed speed (default 1.0 m/s). Simple, reproducible.
- ``odba_scaled``: Speed = ODBA × scaling factor. More realistic but noisier.
