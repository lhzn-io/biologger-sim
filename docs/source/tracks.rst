Tracks and ocean currents
=========================

A track bundle (``python -m biologger_sim export-track``) places the animal in space from three
things: the tag's own motion sensors, the deployment's position fixes, and, optionally, the
ocean current from a parent ocean model. This page explains how the three combine, so that you
can compare two reconstructions of the same deployment and know exactly what differs between
them. Code links on this page and in the :doc:`api` point to GitHub at the commit used to build
these docs.

Dead reckoning
--------------

Lab mode integrates the animal's velocity through the water from its heading and a speed:

.. math::

   n_i = n_{i-1} + s\cos\psi_i\,\Delta t_i, \qquad
   e_i = e_{i-1} + s\sin\psi_i\,\Delta t_i

where :math:`n, e` are meters north and east of the start fix, :math:`\psi` is the heading and
:math:`s` the through-water speed. :math:`\Delta t_i` is the time step. With
``clock_source: fixed_frequency`` (the default, as in the R scripts) it is the nominal
``1 / sampling_rate_hz``. With ``clock_source: sensor_timestamps`` it is the recorded timestamp
difference.

Post-facto exports use a constant speed (``dead_reckoning.constant_speed_m_s``, default
1.0 m/s), whatever ``speed_model`` says. Only the streaming processor implements the
``odba_scaled`` speed model. When a config sets it, the bundle's ``dead_reckoning`` step records
the configured model as ``configured_speed_model``. The bundle records the speed used for each
sample as ``speed_m_s``. ``PostFactoProcessor.calibrate_from_batch_data`` in
:src:`processors/lab.py` performs the integration.

**Heading is magnetic.** The heading comes from the tilt-compensated magnetometer
(``atan2(-m_y, m_x)`` after the attachment rotation and the per-sample pitch and roll
rotation). biologger-sim applies no declination. Near pitch :math:`\pm 90^\circ` the roll is
numerically undefined, so the heading is undefined too and can jump. The heading is NaN only
where pitch or roll is missing.

**No magnetometer, no dead reckoning.** A tag without a magnetometer gives no heading. Its
deployments can only be placed by fix interpolation (below), and their dead-reckoned and
fix-pinned variants cannot be made.

Track models
------------

``dead_reckoning.track_model`` (default ``dead_reckoning``) sets how biologger-sim places the
integrated track relative to the fixes (:func:`~biologger_sim.core.track_models.apply_track_model`):

``dead_reckoning``
   The integrated track, anchored at the start fix. The bundle's ``end_fix_miss`` metric is the
   distance between this track and the end fix at the time of the end fix. The metric measures
   the accumulated error directly.

``fix_pinned``
   The integrated track, rotated and scaled so it starts on the start fix and ends on the end
   fix. In the complex plane (north + i east) one factor
   (:func:`~biologger_sim.core.track_models.fix_pinning_factor`)

   .. math:: k = \frac{z_\text{end fix}}{z_\text{DR}(t_1) - z_\text{DR}(t_0)}

   maps the dead-reckoned fix-to-fix displacement onto the fixes. Every sample becomes
   :math:`k\,(z_\text{DR} - z_\text{DR}(t_0))`. With the current correction,
   :math:`z_\text{DR}` is the through-water track, and the current's drift :math:`z_c` is added
   afterward without rotation. Over the fix window
   :math:`k = (z_\text{end fix} - \Delta z_c) / \Delta z_\text{DR}`, and every sample becomes
   :math:`k\,(z_\text{DR} - z_\text{DR}(t_0)) + (z_c - z_c(t_0))`.

   The angle of :math:`k` is a compass rotation, positive clockwise. It absorbs the tag's
   heading bias and the declination together. The modulus of :math:`k` is a speed scale. The
   heading column is rotated by the same angle, and the unrotated heading is kept internally.
   The bundle's ``placement`` step records ``scale``, ``rotation_deg`` and
   ``heading_correction_deg``. When the dead-reckoned fix-to-fix displacement is under 1 m, the
   rotation is undefined and the track falls back to fix interpolation.

``fix_interpolation``
   Linear in time between the fixes (the mean of a Brownian bridge). It ignores heading, so it
   is the only option for a tag without a magnetometer. Depth and orientation still come from
   the tag.

A model that needs an end fix falls back to ``dead_reckoning`` when the deployment has none,
and the bundle reports the model actually used (``track_model_used``).

Ocean current correction
------------------------

The water moves too. When ``dead_reckoning.current_correction.forcingkit_url`` is set, the
velocity over ground includes the current :math:`(u, v)` at the animal's position, time and
depth:

.. math::

   n_i = n_{i-1} + (s\cos\psi_i + v_i)\,\Delta t_i, \qquad
   e_i = e_{i-1} + (s\sin\psi_i + u_i)\,\Delta t_i

How biologger-sim obtains the current
(:func:`~biologger_sim.core.currents.compute_current_drift`, in :src:`core/currents.py`):

1. biologger-sim thins the track to one point per ``sample_interval_s`` (60 s by default),
   always keeping the first and last record. The first pass uses the through-water
   dead-reckoned track. Each later pass uses the track placed by the previous pass (see "Where
   the current is sampled" below).
2. biologger-sim converts each point to latitude and longitude relative to the start fix. It
   converts the point's depth to forcingkit's z (meters, positive up, with surface excursions
   clamped to 0).
3. forcingkit's trajectory interpolation samples ``u`` and ``v`` from the parent ocean model at
   those points. forcingkit, not the simulator, chooses the donor model by coverage (NECOFS on
   the Northeast shelf, HYCOM where NECOFS has none). forcingkit reports the donor it used, and
   the bundle's ``current_correction`` step records it as ``donor_used``. forcingkit serves
   NECOFS regridded onto 200 m cells and 10 m levels (``vertical_spacing_m``). The 200 m grid
   suggests more detail than the model has, because its values are interpolated from NECOFS's
   own triangles.
4. biologger-sim interpolates the samples linearly in time back to every record. It integrates
   them over the same time steps as dead reckoning, so the drift and the animal's swimming
   share one clock.

biologger-sim computes the correction before placement and places it together with the track
(``PostFactoProcessor._add_current_drift``, then ``_place_track``, in :src:`processors/lab.py`):

- For ``dead_reckoning``, the drift is added to the through-water track.
- For ``fix_pinned``, only the through-water track is rotated and scaled, and the drift is added
  as the model gives it. The pinning rotation and scale represent the tag's heading bias and
  speed error, and the water does not share those errors. With or without the current, the
  pinned track ends on the fixes. The current changes the track's shape and the pinning factor.
- For ``fix_interpolation``, the placed track depends only on the fixes, so the correction
  changes only the recorded currents.

**Missing forcing counts as still water.** A sample with no value (on land, below the model's
sea floor, or outside every donor's grid) counts as zero current. The number of missing samples
is logged and recorded in the ``current_correction`` step. The bundle's ``current_missing`` flag
marks each stretch that uses a missing sample. If every sample is missing, the track is left
uncorrected and the step is recorded as failed.

If the service is unreachable or the client is missing, the track is left uncorrected and the
step is recorded as failed with the error. The export still completes.

Configuration (post-facto mode):

.. code-block:: yaml

   dead_reckoning:
     track_model: fix_pinned          # dead_reckoning (default) | fix_pinned | fix_interpolation
     constant_speed_m_s: 1.0
     current_correction:
       forcingkit_url: "http://localhost:9598"   # null (default) turns it off
       ocean_store: null                         # a local z-v3 store instead (pipelines page)
       sample_interval_s: 60.0
       vertical_spacing_m: 10.0
       cache_dir: null                           # client chunk cache (null: client default)
       timeout_s: 1800.0
       max_passes: 30                            # sampling passes at most (1: water track only)
       convergence_m: 50.0                       # stop when the placed track moves less than this

The parent ocean models
-----------------------

Two regional models cover the Northeast shelf break, each on its own grid:

.. list-table::
   :header-rows: 1
   :widths: 22 39 39

   * -
     - NECOFS (GOM7 hindcast)
     - DOPPIO
   * - Model
     - FVCOM, UMass Dartmouth (SMAST)
     - ROMS, Rutgers University Ocean Modeling Group
   * - Horizontal grid
     - Unstructured triangles; finer along the slope and canyons, coarser offshore
     - Curvilinear cells of about 7 km
   * - Vertical
     - 45 terrain-following (sigma) layers
     - 40 terrain-following (s) layers
   * - Data assimilation
     - No (hindcast)
     - Yes (reanalysis), ending in 2024
   * - Used by the correction
     - Yes, forcingkit's first choice on the Northeast shelf
     - No, because forcingkit does not offer it for trajectories

The forcing stores cut for the RED001 swordfish deployment cover an area about 50 km on a side at
the shelf break, read on the models' native grids for 11 to 14 August 2022. Over that area NECOFS
has about 1200 triangles with a median edge of about 1.5 km. DOPPIO covers the same area with
about 10 by 10 cells. Neither model resolves a canyon a few kilometers wide well. NECOFS has a
few triangles across such a canyon, and DOPPIO has none. Canyon-scale features in NECOFS, such
as a closed eddy at a canyon mouth, may come from steep sigma layers over steep topography. Do
not treat them as established without observations. Neither model is a measurement. Credit
NECOFS/UMASSD (SMAST, UMass Dartmouth) and the Rutgers University Ocean Modeling Group (DOPPIO)
wherever their currents are shown.

.. The label keeps links to this section's former title working (the portal's compare page used it).

.. _known-limit-where-the-current-is-sampled:

Where the current is sampled
----------------------------

At the shelf break the NECOFS current changes over distances of about 1.5 km (its median
triangle edge), so the correction must sample the current where the animal actually was. The
animal's positions are known only after the track is placed, and placing the track needs the
current. The correction therefore samples in passes:

1. Pass 1 samples along the through-water dead-reckoned track and places the track with that
   drift.
2. Each later pass samples along the track placed by the previous pass, then places the track
   again.
3. The passes stop when the placed track moves less than ``convergence_m`` (50 m by default) at
   every record from one pass to the next, or after ``max_passes`` (30) passes. If the track has
   not settled by then, biologger-sim keeps it and logs a warning.

Multi-day tracks need many passes: the move shrinks by a roughly constant factor per pass, so
the 19A0564 whale shark pinned track (about 2.5 days) settled in 22 passes and the WHOI.001
pinned track in 13. A pass whose track has moved samples new forcing stores, and the client
keeps every one it fetches, so the 22 passes cached about 40 GB. Point ``cache_dir`` at a disk
with room for that, and clear it after the export.

The ``current_correction`` step records ``passes``, ``pass_shift_max_m``, ``convergence_m`` and
``converged``. ``pass_shift_max_m`` is the largest move of the placed track in each pass, and the
first move is measured from the through-water track. Setting ``max_passes: 1`` reproduces the
correction used before 2026-11-18, which made a single pass along the through-water track.

For the RED001 swordfish deployment, the single pass sampled NECOFS up to 17.0 km (median
11.6 km) away from the final pinned track. That pass applied 6.7 km of drift toward 262 degrees,
and pinning then turned the track by 57.0 degrees and scaled it by 1.14.

With multiple passes, the pinned track settles after five passes (the placed track moved
17.0 km, 3.7 km, 408 m, 110 m and 15 m). The drift over the deployment is then 0.57 km toward
191 degrees. Pinning turns the track by 93.6 degrees and scales it by 1.31, close to the
91.3 degrees and 1.33 obtained without the current. The current correction therefore changes
RED001's pinned track only a little. Most of the heading correction is the tag's own bias. The
dead-reckoned variant (``dr_cur``) settles after four passes with 6.6 km of drift, because its
positions stay on the through-water path plus the drift.

``scripts/current_sampling_offset.py`` measures the distance between a placed track and the
through-water track. With ``--forcingkit-url``, the script also re-samples the current along the
placed track to check the applied drift:

.. code-block:: bash

   python scripts/current_sampling_offset.py <tracks>/<run>_dr <tracks>/<run>_pin_cur \
       --forcingkit-url http://localhost:9598   # optional: re-sample along the placed track

For a bundle exported with multiple passes, the re-sampled drift should match the applied drift
to within the shift of the last pass.

What a bundle records
---------------------

``track.f32`` holds one row per output sample (``--rate``, 1 Hz by default).
:func:`~biologger_sim.io.track_bundle.write_bundle` writes it. Every bundle has ``t``,
``north_m``, ``east_m``, ``depth_m``, ``heading_deg``, ``pitch_deg``, ``roll_deg``, ``vedba``,
``odba`` and the roll continuity columns. The following columns are added when the run produced
them:

.. list-table::
   :header-rows: 1
   :widths: 25 12 63

   * - Column
     - Unit
     - Meaning
   * - ``current_east_m_s``
     - m/s
     - Eastward current applied at the animal's depth, at sample time (current correction only)
   * - ``current_north_m_s``
     - m/s
     - Northward current applied at the animal's depth, at sample time (current correction only)
   * - ``current_missing``
     - flag
     - 1 if a missing forcing sample (still water) was used since the previous output sample
   * - ``speed_m_s``
     - m/s
     - Through-water speed used by dead reckoning, before placement. A fix-pinned track scales
       it by the placement step's ``scale``. Present whenever the run has a heading
   * - ``accel_static_x``, ``_y``, ``_z``
     - run's ``vedba`` unit
     - Static (low-passed) acceleration, which points along gravity
   * - ``accel_dynamic_x``, ``_y``, ``_z``
     - run's ``vedba`` unit
     - Dynamic acceleration (total minus static), at sample time

The acceleration columns, like ``vedba`` and ``odba``, are in the run's unit: m/s\ :sup:`2` for
lab mode, g for streaming mode (``track.json`` lists each column's unit). The columns use the
body (tag) axes after the attachment rotation, in a forward-right-down frame: x toward the head,
y to the right, z down. Pitch and roll come from the static part as
``pitch_deg = -atan2(x, hypot(y, z))`` (nose up positive) and ``roll_deg = atan2(y, z)``
(right side down positive).

``track.json`` describes how the track was made, so that two bundles can be compared step by
step:

``pipeline``
   The ordered steps, each ``{step, method, version, status, params}``: ``dead_reckoning``
   (method ``constant``, with ``constant_speed_m_s`` and ``true_integration``),
   ``current_correction`` (``forcingkit``, with ``donor_used``, ``samples``, ``missing``,
   ``drift_end_m`` as north and east meters, ``passes``, ``pass_shift_max_m``,
   ``convergence_m`` and ``converged``, and the forcing store's attributes, or status
   ``failed`` with an ``error`` when the correction could not be applied) and ``placement``
   (the model used, with ``scale``, ``rotation_deg`` and ``heading_correction_deg`` for
   ``fix_pinned``).

``metrics``
   ``end_fix_miss_before_placement`` and ``end_fix_miss``, in meters. "Before placement" refers
   to the dead-reckoned track, including the current when the correction was applied. For a
   fix-pinned track, ``end_fix_miss`` is zero by construction.

``reproducibility``
   A SHA-256 fingerprint over the recipe: the sim commit, any uncommitted diff, the
   environment, the resolved config, the tag data file, the deployment's metadata row and the
   forcing store. ``config.yaml`` and ``environment.txt`` sit beside ``track.json``. When the
   simulator's working tree had uncommitted changes, ``code.patch`` sits there too.

Comparing reconstructions
-------------------------

Each deployment is exported in four variants, and each run ID ends in the variant name. The
variants differ only in ``track_model`` and in whether ``current_correction`` is set:

.. list-table::
   :header-rows: 1

   * - Variant
     - ``track_model``
     - Current
     - What it shows
   * - ``dr``
     - ``dead_reckoning``
     - off
     - The tag alone. The miss at the end fix is the accumulated error
   * - ``dr_cur``
     - ``dead_reckoning``
     - on
     - Whether the current explains part of that miss
   * - ``pin``
     - ``fix_pinned``
     - off
     - The tag's path shape, forced onto both fixes
   * - ``pin_cur``
     - ``fix_pinned``
     - on
     - The same, with the current's drift added (not rotated or scaled by the pinning)

The biologger portal's compare page (``/deployments/<id>/compare``) draws a deployment's
variants together. The page also shows each variant's depth against the seafloor and the
separation between the variants over time.
