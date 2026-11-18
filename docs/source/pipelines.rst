=========================================
Pipeline Architecture: Lab vs Simulation
=========================================

The package provides **two distinct processing pipelines** designed for different stages of the research workflow. The top-level ``mode`` key of the YAML config selects one (:class:`~biologger_sim.core.types.PipelineConfig`); the per-entity settings sit under ``simulation.entities`` in both.

Lab Mode (Post-Facto)
=====================

**High-Precision Analysis & Validation**

The Lab Mode pipeline is designed for batch analysis where the complete dataset is available. It aims for parity with the legacy R implementation. Every entity runs through :class:`~biologger_sim.processors.lab.PostFactoProcessor`.

Characteristics
---------------

- **Memory**: Full dataset loaded into memory.
- **Processing**: Acausal algorithms (e.g., ``filtfilt``, centered moving averages).
- **Calibration**: Batch computation from the full dataset (``batch_compute``, the default), or locked values (``fixed``).
- **Depth**: Acausal interpolation of missing values.

Configuration
-------------

A Lab Mode config (abridged from ``config/Swordfish-RED001_20220812_19A0564-postfacto.yaml``):

.. code-block:: yaml

   mode: LAB
   simulation:
     meta_file: ../datasets/biologger_meta.csv   # start and end fixes, species
     entities:
       - sim_id: sword_postfacto
         tag_id: RED001_20220812
         sampling_rate_hz: 16
         clock_source: fixed_frequency   # sensor_timestamps integrates the recorded time steps
         input_file: path/to/tag.csv
         calibration:
           attachment_angle_mode: batch_compute   # default
           magnetometer_mode: batch_compute       # default
           sensor_signs: negated                  # r_script (default) | negated
         depth_estimation:
           algorithm: acausal_interpolate
         dead_reckoning:
           track_model: fix_pinned

Clock Drift & Jitter
--------------------
Real hardware sensors often have clock jitter (variable sampling rates).
Legacy R implementations use **Fixed Step Integration** (assuming ``dt = 1/freq``), which ignores this jitter. This produces smooth tracks but mathematically implies that the animal speeds up/slows down inversely to the clock jitter if analyzed against real time.

- **Default Behavior (R-Compatibility)**: ``clock_source: fixed_frequency`` uses a fixed ``dt``. Matches legacy R output exactly. Velocity calculated from position/time ratio will show jitter.
- **True Integration (``clock_source: sensor_timestamps``)**: Uses the recorded time deltas. Matches the physical path to the clock. Velocity is stable, but positions differ slightly from R legacy tracks. ``strict_r_parity: true`` forces ``fixed_frequency``.

**Diagnostic Output**:
Lab Mode includes a ``clock_drift_sec`` column in the output, measuring the deviation between the sensor clock and an ideal clock:
``clock_drift_sec = Timestamp_Actual - (Start_Time + Index * 1/Freq)``

Simulation Mode (Real-Time)
===========================

**On-Tag Algorithm Development**

The Simulation Mode pipeline is designed for real-time processing where data arrives sample-by-sample. It uses fully causal algorithms with no lookahead. Entities run through :class:`~biologger_sim.processors.streaming.StreamingProcessor`, except an entity with ``strict_r_parity: true``, which runs through ``PostFactoProcessor``.

Characteristics
---------------

- **Memory**: Fixed memory footprint (O(1)).
- **Processing**: Causal algorithms (e.g., ``lfilter``, EMA).
- **Calibration**: Fixed parameters (``locked_*`` values); the streaming processor has no online calibration.
- **Depth**: Kalman filter nowcast from the last pressure sample and the vertical acceleration.

Configuration
-------------

A Simulation Mode config (abridged from ``config/Swordfish-RED001_20220812_19A0564-causal.yaml``):

.. code-block:: yaml

   mode: SIMULATION
   simulation:
     entities:
       - sim_id: sword_causal
         calibration:
           attachment_angle_mode: fixed
           magnetometer_mode: fixed
         depth_estimation:
           algorithm: causal_sample_hold

Streaming Algorithm (11 Steps plus Terrain)
===========================================

The ``StreamingProcessor`` (:src:`processors/streaming.py`) implements a strictly causal motion model reconciled with validated post-facto pipelines. Each step processes data as it arrives with O(1) memory footprint.

1. Input Acquisition
--------------------
Raw sensor data is extracted from the input record. Accelerometer values arrive in **0.1 g units** (1 count = 0.1 g). Magnetometer values are in raw ADC counts.

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
A trailing moving average window of ``filt_len=48`` samples (3 seconds at 16 Hz) estimates the static (gravity) component. Dynamic acceleration is the residual.

.. code-block:: python

   static_x = sum(buffer_x) / filt_len
   dyn_x = ax_att - static_x
   odba_g = (|dyn_x| + |dyn_y| + |dyn_z|) / 10.0  # Convert to g

**Warmup Behavior**: Until the window holds 48 samples, static = raw accel, dynamic = 0, ODBA = 0.

4. Dead Reckoning Timing
------------------------
The time step is the difference between consecutive record timestamps, or the nominal ``1 / freq`` for the first record and whenever the difference is not positive. The streaming processor does not read ``clock_source``.

5. Orientation (R-style pitchRoll2)
-----------------------------------
Pitch and roll are calculated from the static acceleration vector using R-compatible trigonometric formulas:

.. math::

   \text{pitch} = -\arctan2(a_x^{static}, \sqrt{a_y^2 + a_z^2})

   \text{roll} = \arctan2(a_y^{static}, a_z^{static})

6. World Frame Transformation
-----------------------------
The vertical component of the acceleration is rotated from the body frame to the world frame (NED convention) and gravity is removed:

.. math::

   a_z^{world} = -\sin(\text{pitch}) \cdot a_x + \cos(\text{pitch})\sin(\text{roll}) \cdot a_y + \cos(\text{pitch})\cos(\text{roll}) \cdot a_z

   a_z^{no\_gravity} = a_z^{world} \times 9.81 - 9.81

7. High-Pass Filter (Bias Removal)
----------------------------------
A 2nd-order Butterworth high-pass filter (cutoff 0.1 Hz by default, ``highpass_cutoff``) removes sensor bias and integration drift:

.. code-block:: python

   accel_z_filtered, zi = lfilter(highpass_b, highpass_a, [accel_z_no_gravity], zi=zi)

8. INS Depth Estimation (Kalman Filter)
---------------------------------------
A 2-state Kalman Filter (depth, vertical velocity) fuses:

- **Prediction**: Vertical acceleration integration (at the sampling rate, 16 Hz for the example tags)
- **Update**: Sparse pressure sensor depth measurements (about 1 Hz on the example tags)

Parameters: ``process_noise_depth=1e-4``, ``process_noise_velocity=1e-3``, ``measurement_noise=0.02``

9. Multi-Scale Depth Smoothing
------------------------------
Three EMAs of the Kalman depth (time constants 3 s, 12 s and 45 s) are blended by activity, measured as ODBA in 0.1 g units (``DepthSmoother``):

- **Low activity** (ODBA at or below 0.15): 0.3 medium + 0.7 slow
- **High activity** (ODBA at or above 0.20): 0.4 fast + 0.6 medium
- **Between**: Linear blend of the two weightings

10. Magnetometer & Heading
--------------------------
Tilt-compensated magnetic heading using locked hard-iron calibration:

.. code-block:: python

   mx_n = (mx_raw - offset_x) / sphere_radius
   heading = atan2(-my_world, mx_world)

11. Dead Reckoning Integration
------------------------------
Track position is updated in the horizontal plane using heading and speed:

.. code-block:: python

   pseudo_x += speed * dt * cos(heading)
   pseudo_y += speed * dt * sin(heading)

Speed model: ``odba_scaled`` (the default: ``speed = odba_g * odba_speed_factor``, factor 2.0) or ``constant`` (``constant_speed_m_s``, 1.0 m/s).

11b. Terrain and Altitude Processing
------------------------------------
To model real-world swimming kinematics in complex benthic zones, the simulator estimates geographic coordinates and queries an external elevation service:

*   **GPS Estimation**: If the record has no latitude and longitude, coordinates are estimated in real time using a flat-earth approximation from the deployment's start location (from the metadata file) and the dead-reckoning displacement (``pseudo_x`` and ``pseudo_y``).
*   **Centralized Elevation Query**: The processor queries the ``topobathykit`` service at ``simulation.topobathykit_url`` (CLI ``--topobathykit-url``) through a caching client that fetches zoom 11 Web Mercator tiles (the service sets each tile's pixel spacing) and interpolates bilinearly.
*   **Benthic Telemetry**: Calculates the animal's height above the seafloor:

.. math::

   \text{Altitude\_Above\_Seafloor} = -\text{Depth} - \text{Seafloor\_Elevation}

Where ``Depth`` is positive down and ``Seafloor_Elevation`` is the Mean Sea Level (MSL) altitude of the sea bottom (typically negative). The resulting ``Seafloor_Elevation`` and ``Altitude_Above_Seafloor`` are injected into the ZMQ stream.


Hardware-Specific Parallel Backends
===================================

To scale up to large numbers of parallel entities (e.g., Monte Carlo simulations or swarms), Simulation Mode can run the inertial steps in a GPU-resident backend. Without a ``backend`` (the default) or when the requested one is unavailable, each entity uses ``StreamingProcessor`` on the CPU.

NVIDIA Warp (CUDA)
------------------
Offloads Gsep ring buffers, running sums, and orientation calculations to NVIDIA GPUs using JIT-compiled CUDA kernels.

* **Requirements:** NVIDIA GPU, CUDA driver, and ``warp-lang`` package.
* **Usage:** Set ``simulation.backend: warp``.

Apple MLX (Metal)
-----------------
Specifically optimized for Apple Silicon (macOS) architectures. It leverages Apple's MLX machine learning framework and the Apple Silicon GPU (Metal) using JIT-compiled execution graphs via ``mlx.core.compile``.

* **Unified Memory Advantage:** Because the CPU and GPU share the same physical RAM space on Apple Silicon, data ingestion is zero-copy, avoiding the PCIe transfer bottlenecks typical of discrete GPU architectures.
* **Performance:** In a prototype benchmark on an Apple M4 Max (128 GB unified memory), the MLX backend reached 30.7M samples per second for 500,000 entities in blocks of 100,000, about 3x vectorized NumPy (``docs/analysis/20260606-apple-silicon-mlx-metal-optimization-planning.md``).
* **Requirements:** Apple Silicon Mac and ``mlx`` package.
* **Usage:** Set ``simulation.backend: mlx``.


Configuration Reference
=======================

Streaming Mode Configuration
----------------------------

The following YAML shows the configuration attributes (global simulation parameters and entity-specific options) with their default values, from :mod:`biologger_sim.core.types`. ``sim_id`` and ``input_file`` are required; ``locked_*`` values have no default.

.. code-block:: yaml

   mode: SIMULATION                      # SIMULATION (default) | LAB
   publish_zmq: true                     # CLI --no-publish-zmq turns it off
   simulation:
     playback_speed: 1.0                 # Real-time speed multiplier (CLI --speed)
     loop: false                         # Loop simulation playback
     backend: null                       # null (CPU) | warp | mlx
     meta_file: null                     # biologger_meta.csv: species and position fixes
     topobathykit_url: "http://garnet.internal:9595"   # tiled elevation service
     zmq:
       host: 127.0.0.1
       port: 5555
       topic: biologger/telemetry

     entities:
       - sim_id: sword_causal            # Unique identifier for this entity
         tag_id: null                    # Key in biologger_meta.csv (defaults to sim_id)
         input_file: path/to/data.csv    # Path to input CSV file
         sampling_rate_hz: 16            # Sensor sampling rate in Hz
         start_time_offset: 0.0
         clock_source: fixed_frequency   # fixed_frequency | sensor_timestamps
         strict_r_parity: false          # true: PostFactoProcessor with R-compatible settings

         calibration:
           attachment_angle_mode: batch_compute   # batch_compute | fixed
           magnetometer_mode: batch_compute       # batch_compute | fixed
           # Locked values, used by fixed mode and by the streaming processor
           locked_attachment_roll_deg: null
           locked_attachment_pitch_deg: null
           locked_mag_offset_x: null
           locked_mag_offset_y: null
           locked_mag_offset_z: null
           locked_mag_sphere_radius: null
           sensor_signs: r_script        # r_script | negated
           accel_depth_bias: false

         depth_estimation:
           algorithm: causal_sample_hold # causal_sample_hold | acausal_interpolate | off

         dead_reckoning:
           speed_model: odba_scaled      # odba_scaled | constant
           constant_speed_m_s: 1.0       # Speed when model=constant (and in Lab Mode)
           odba_speed_factor: 2.0        # Speed per g of ODBA when model=odba_scaled
           track_model: dead_reckoning   # Lab Mode placement; see Tracks and ocean currents

         ahrs:
           enabled: false

         save_telemetry: false           # Write output CSV

The deployment's start location is not a config key: it comes from the metadata file's start fix.

Key Configuration Decisions
---------------------------

**clock_source** (Lab Mode):

- ``fixed_frequency``: Use nominal dt = 1/sampling_rate. Matches R legacy behavior.
- ``sensor_timestamps``: Use actual timestamp deltas. Physically accurate but differs from R.

**calibration.attachment_angle_mode**:

- ``batch_compute``: Compute the angles from the full dataset (Lab Mode).
- ``fixed``: Use pre-computed angles from ``locked_attachment_*_deg``.

**dead_reckoning.speed_model** (Simulation Mode; Lab Mode always uses ``constant_speed_m_s``):

- ``constant``: Fixed speed (default 1.0 m/s). Simple, reproducible.
- ``odba_scaled``: Speed = ODBA (g) x ``odba_speed_factor``. More responsive to activity but noisier.

**dead_reckoning.current_correction** (post-facto mode):

Dead reckoning integrates the animal's motion through the water; the water moves too. With a
forcingkit service configured, the simulator samples ocean ``u`` and ``v`` along the
dead-reckoned track (one point per ``sample_interval_s``, at the animal's depth) and adds their
displacement to each step, before the track model places the track. The through-water track is
kept as ``pseudo_x_water`` / ``pseudo_y_water`` and the per-record current is published as
``current_u`` / ``current_v`` (``current_east_m_s`` / ``current_north_m_s`` in a track bundle).
It needs the deployment's start fix in the metadata and the optional client
(``pip install 'biologger-sim[currents]'``, Python 3.11 or newer). If the service is
unreachable or has no coverage, the track is left uncorrected and the error is logged.

.. code-block:: yaml

   dead_reckoning:
     current_correction:
       forcingkit_url: "http://localhost:9598"   # null (default) turns the correction off
       sample_interval_s: 60.0                   # one forcing sample a minute
       vertical_spacing_m: 10.0                  # parent-ocean store spacing
       cache_dir: null                           # client chunk cache (null: client default)
       timeout_s: 1800.0                         # wait for a store that is not cached yet

With ``track_model: fix_interpolation`` the placed track depends only on the fixes, so the
correction changes the recorded currents and the intermediate track but not ``pseudo_x`` /
``pseudo_y``; it matters for ``dead_reckoning`` and ``fix_pinned``.

The method, its limits and what a bundle records are described in :doc:`tracks`.
