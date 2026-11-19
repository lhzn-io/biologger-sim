=========================================
Pipeline Architecture: Lab vs Simulation
=========================================

The package provides **two processing pipelines** for different stages of the research
workflow. The top-level ``mode`` key of the YAML config selects one
(:class:`~biologger_sim.core.types.PipelineConfig`). In both pipelines, the per-entity settings
sit under ``simulation.entities``.

Lab Mode (Post-Facto)
=====================

**Batch Analysis & Validation**

The Lab Mode pipeline analyzes a complete dataset in one batch. It aims to reproduce the output of
the legacy R implementation. Every entity runs through
:class:`~biologger_sim.processors.lab.PostFactoProcessor`.

Characteristics
---------------

- **Memory**: Full dataset loaded into memory.
- **Processing**: Acausal algorithms (centered moving averages).
- **Calibration**: Batch computation from the full dataset (``batch_compute``, the default), or
  locked values (``fixed``).
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
Real tag clocks often jitter, so the actual sampling interval varies. Legacy R implementations
use **Fixed Step Integration** (``dt = 1/freq``), which ignores this jitter. Fixed steps produce
smooth tracks. Measured against real time, however, such a track implies that the animal speeds
up and slows down in inverse proportion to the clock jitter.

- **Default Behavior (R-Compatibility)**: ``clock_source: fixed_frequency`` uses a fixed ``dt``
  and matches the legacy R output exactly. Velocity computed as displacement over recorded time
  shows the jitter.
- **True Integration (``clock_source: sensor_timestamps``)**: Uses the recorded time deltas, so
  the integrated path follows the tag's clock. Velocity is stable, but positions differ slightly
  from the legacy R tracks. ``strict_r_parity: true`` forces ``fixed_frequency``.

**Diagnostic Output**:
Lab Mode adds a ``clock_drift_sec`` column to the output. The column measures how far the sensor
clock deviates from an ideal clock:
``clock_drift_sec = Timestamp_Actual - (Start_Time + Index * 1/Freq)``

Simulation Mode (Real-Time)
===========================

**On-Tag Algorithm Development**

The Simulation Mode pipeline processes data in real time, one sample at a time. It uses only
causal algorithms, with no lookahead. Entities run through
:class:`~biologger_sim.processors.streaming.StreamingProcessor`. The exception is an entity with
``strict_r_parity: true``, which runs through ``PostFactoProcessor``.

Characteristics
---------------

- **Memory**: Fixed memory footprint (O(1)).
- **Processing**: Causal algorithms (e.g., ``lfilter``, EMA).
- **Calibration**: Fixed parameters (``locked_*`` values). The streaming processor has no online
  calibration.
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

Streaming Algorithm (12 Steps)
==============================

The ``StreamingProcessor`` (:src:`processors/streaming.py`) implements a strictly causal motion
model, kept consistent with the validated post-facto pipelines. Each step processes data as it
arrives, with an O(1) memory footprint.

1. Input Acquisition
--------------------
The processor reads raw sensor values from the input record. Accelerometer values arrive in
**0.1 g units** (1 count = 0.1 g). Magnetometer values are raw ADC counts.

.. code-block:: python

   ax_m, ay_m, az_m = record["int aX"], record["int aY"], record["int aZ"]
   depth_raw = record["Depth"]

2. Attachment Correction
------------------------
The processor applies the locked attachment roll and pitch as rotation matrices (Rx, then Ry).
The rotation aligns the sensor frame with the animal's body frame.

.. math::

   \vec{a}_{att} = \vec{a}_{raw} \cdot R_x(\phi_{att}) \cdot R_y(\theta_{att})

Where :math:`\phi_{att}` is attachment roll and :math:`\theta_{att}` is attachment pitch.

3. Window Management (Causal Gsep)
----------------------------------
A trailing moving average over ``filt_len=48`` samples (3 seconds at 16 Hz) estimates the static
(gravity) component. Dynamic acceleration is the residual.

.. code-block:: python

   static_x = sum(buffer_x) / filt_len
   dyn_x = ax_att - static_x
   odba_g = (|dyn_x| + |dyn_y| + |dyn_z|) / 10.0  # Convert to g

**Warmup Behavior**: Until the window holds 48 samples, the static component equals the raw
acceleration, and dynamic acceleration and ODBA are 0.

4. Dead Reckoning Timing
------------------------
The time step is the difference between consecutive record timestamps. For the first record, and
whenever the difference is not positive, the time step is the nominal ``1 / freq``. The streaming
processor does not read ``clock_source``.

5. Orientation (R-style pitchRoll2)
-----------------------------------
The processor computes pitch and roll from the static acceleration vector with R-compatible
formulas:

.. math::

   \text{pitch} = -\arctan2(a_x^{static}, \sqrt{a_y^2 + a_z^2})

   \text{roll} = \arctan2(a_y^{static}, a_z^{static})

6. World Frame Transformation
-----------------------------
The processor rotates the acceleration from the body frame to the world frame (NED convention),
keeps the vertical component and removes gravity:

.. math::

   a_z^{world} = -\sin(\text{pitch}) \cdot a_x + \cos(\text{pitch})\sin(\text{roll}) \cdot a_y + \cos(\text{pitch})\cos(\text{roll}) \cdot a_z

   a_z^{no\_gravity} = a_z^{world} \times 9.81 - 9.81

7. High-Pass Filter (Bias Removal)
----------------------------------
A 2nd-order Butterworth high-pass filter (cutoff 0.1 Hz by default, ``highpass_cutoff``) removes
sensor bias and integration drift:

.. code-block:: python

   accel_z_filtered, zi = lfilter(highpass_b, highpass_a, [accel_z_no_gravity], zi=zi)

8. INS Depth Estimation (Kalman Filter)
---------------------------------------
A 2-state Kalman Filter (depth, vertical velocity) fuses:

- **Prediction**: Vertical acceleration integration (at the sampling rate, 16 Hz for the example
  tags)
- **Update**: Sparse pressure sensor depth measurements (about 1 Hz on the example tags)

Parameters: ``process_noise_depth=1e-4``, ``process_noise_velocity=1e-3``,
``measurement_noise=0.02``

9. Multi-Scale Depth Smoothing
------------------------------
``DepthSmoother`` blends three exponential moving averages (EMAs) of the Kalman depth, with time
constants of 3 s, 12 s and 45 s. The weights depend on activity, measured as ODBA in 0.1 g units:

- **Low activity** (ODBA at or below 0.15): 0.3 medium + 0.7 slow
- **High activity** (ODBA at or above 0.20): 0.4 fast + 0.6 medium
- **Between**: Linear blend of the two weightings

10. Magnetometer & Heading
--------------------------
The processor computes a tilt-compensated magnetic heading with the locked hard-iron calibration:

.. code-block:: python

   mx_n = (mx_raw - offset_x) / sphere_radius
   heading = atan2(-my_world, mx_world)

11. Dead Reckoning Integration
------------------------------
The processor updates the track position in the horizontal plane from heading and speed:

.. code-block:: python

   pseudo_x += speed * dt * cos(heading)
   pseudo_y += speed * dt * sin(heading)

The speed model applies to this streaming processor only. It is either ``odba_scaled`` (the
config default, ``speed = odba_g * odba_speed_factor`` with a factor of 2.0) or ``constant``
(``constant_speed_m_s``, 1.0 m/s). Post-facto (Lab Mode) dead reckoning ignores ``speed_model``
and always integrates at ``constant_speed_m_s``, as the R scripts do. See :doc:`tracks`.

12. Terrain and Altitude Processing
-----------------------------------
To relate the animal's motion to the seafloor, the simulator estimates geographic coordinates and
queries an external elevation service:

*   **GPS Estimation**: If the record has no latitude and longitude, the processor estimates them
    in real time with a flat-earth approximation. The estimate starts from the deployment's start
    location (from the metadata file) and adds the dead-reckoning displacement (``pseudo_x`` and
    ``pseudo_y``).
*   **Centralized Elevation Query**: The processor queries the ``topobathykit`` service at
    ``simulation.topobathykit_url`` (CLI ``--topobathykit-url``) through a caching client. The
    client fetches zoom 11 Web Mercator tiles and interpolates bilinearly. The service sets each
    tile's pixel spacing.
*   **Benthic Telemetry**: The processor computes the animal's height above the seafloor:

.. math::

   \text{Altitude\_Above\_Seafloor} = -\text{Depth} - \text{Seafloor\_Elevation}

Here ``Depth`` is positive down, and ``Seafloor_Elevation`` is the elevation of the sea bottom
relative to Mean Sea Level (MSL), typically negative. The processor adds ``Seafloor_Elevation``
and ``Altitude_Above_Seafloor`` to the ZMQ stream.


Hardware-Specific Parallel Backends
===================================

For large numbers of parallel entities (for example Monte Carlo simulations or swarms),
Simulation Mode can run the inertial steps in a GPU-resident backend. When ``backend`` is unset
(the default) or the requested backend is unavailable, each entity uses ``StreamingProcessor`` on
the CPU.

NVIDIA Warp (CUDA)
------------------
The Warp backend runs the Gsep ring buffers, running sums and orientation calculations on NVIDIA
GPUs, as JIT-compiled CUDA kernels.

* **Requirements:** NVIDIA GPU, CUDA driver, and ``warp-lang`` package.
* **Usage:** Set ``simulation.backend: warp``.

Apple MLX (Metal)
-----------------
The MLX backend targets Apple Silicon Macs. It runs on the Apple Silicon GPU (Metal) through
Apple's MLX machine learning framework, with execution graphs JIT-compiled by
``mlx.core.compile``.

* **Unified Memory:** On Apple Silicon the CPU and GPU share the same physical RAM, so loading data
  needs no copy. A discrete GPU instead receives data over PCIe, which is often a bottleneck.
* **Performance:** In a prototype benchmark on an Apple M4 Max (128 GB unified memory), the MLX
  backend reached 30.7M samples per second for 500,000 entities in blocks of 100,000. That is
  about 3x vectorized NumPy
  (``docs/analysis/20260606-apple-silicon-mlx-metal-optimization-planning.md``).
* **Requirements:** Apple Silicon Mac and ``mlx`` package.
* **Usage:** Set ``simulation.backend: mlx``.


Configuration Reference
=======================

Streaming Mode Configuration
----------------------------

The YAML below lists the configuration keys (global simulation parameters and per-entity options)
with their default values, from :mod:`biologger_sim.core.types`. ``sim_id`` and ``input_file``
are required. The ``locked_*`` values have no default.

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
           speed_model: odba_scaled      # odba_scaled | constant; Simulation Mode only
           constant_speed_m_s: 1.0       # Speed when model=constant, and always in Lab Mode
           odba_speed_factor: 2.0        # Speed per g of ODBA when model=odba_scaled
           track_model: dead_reckoning   # Lab Mode placement; see Tracks and ocean currents

         save_telemetry: false           # Write output CSV

The deployment's start location is not a config key. It comes from the start fix in the metadata
file. The Gsep window length (``filt_len``) is not a config key either. It is a processor
constructor argument, and the pipeline always uses its default of 48 samples (3 s at 16 Hz).
``sampling_rate_hz`` reaches the processors as their ``freq`` argument.

Key Configuration Decisions
---------------------------

**clock_source** (Lab Mode):

- ``fixed_frequency``: Uses the nominal dt = 1/sampling_rate. Matches the legacy R behavior.
- ``sensor_timestamps``: Uses the recorded timestamp deltas. Physically accurate, but differs
  from R.

**calibration.attachment_angle_mode**:

- ``batch_compute``: Computes the angles from the full dataset (Lab Mode).
- ``fixed``: Uses pre-computed angles from ``locked_attachment_*_deg``.

**dead_reckoning.speed_model** (Simulation Mode only, because Lab Mode always uses
``constant_speed_m_s``):

- ``constant``: Fixed speed (default 1.0 m/s). Simple and reproducible.
- ``odba_scaled``: Speed = ODBA (g) x ``odba_speed_factor``. The config default, used only by the
  streaming processor. Responds more to activity, but is noisier.

**dead_reckoning.current_correction** (post-facto mode):

Dead reckoning integrates the animal's motion through the water, but the water moves too. With a
forcingkit service configured, the simulator samples the ocean current ``u`` and ``v`` once per
``sample_interval_s``, at the animal's depth and time, and adds the resulting drift when the track
model places the track. It samples in passes: the first along the through-water track, each later
one along the track the previous pass placed, until the placed track moves less than
``convergence_m`` or ``max_passes`` is reached. The through-water track is kept as
``pseudo_x_water`` / ``pseudo_y_water``. The current for each record is published as
``current_u`` / ``current_v`` (``current_east_m_s`` / ``current_north_m_s`` in a track bundle).
The correction needs the deployment's start fix in the metadata and the optional client
(``pip install 'biologger-sim[currents]'``, Python 3.11 or newer). A sample with no model value
counts as still water. If the service is unreachable, or every sample is missing, the track is
left uncorrected and the error is logged.

.. code-block:: yaml

   dead_reckoning:
     current_correction:
       forcingkit_url: "http://localhost:9598"   # null (default) turns the correction off
       sample_interval_s: 60.0                   # one forcing sample a minute
       max_passes: 6                             # sampling passes at most
       convergence_m: 50.0                       # stop once the placed track moves less
       window_s: 21600.0                         # request the current in 6 h windows
       vertical_spacing_m: 10.0                  # parent-ocean store spacing
       cache_dir: null                           # client chunk cache (null: client default)
       timeout_s: 1800.0                         # wait for a store that is not cached yet

With ``track_model: fix_interpolation``, the placed track depends only on the fixes. The
correction then changes the recorded currents and the intermediate track, but not ``pseudo_x`` /
``pseudo_y``. The correction changes the placed track only for ``dead_reckoning`` and
``fix_pinned``.

:doc:`tracks` describes the method, its limits and what a bundle records.
