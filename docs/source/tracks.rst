Tracks and ocean currents
=========================

A track bundle (``python -m biologger_sim export-track``) places the animal in space from three
things: the tag's own motion sensors, the deployment's position fixes, and, optionally, the
ocean current from a parent ocean model. This page explains how they combine, so that two
reconstructions of the same deployment can be compared knowing exactly what differs. Code
links on this page and in the :doc:`api` point to GitHub at the commit these docs were built
from.

.. contents:: On this page
   :local:
   :depth: 1

Dead reckoning
--------------

Lab mode integrates the animal's velocity through the water from its heading and a speed:

.. math::

   n_i = n_{i-1} + s\cos\psi_i\,\Delta t_i, \qquad
   e_i = e_{i-1} + s\sin\psi_i\,\Delta t_i

where :math:`n, e` are meters north and east of the start fix, :math:`\psi` is the heading and
:math:`s` the through-water speed. :math:`\Delta t_i` is the nominal ``1 / sampling_rate_hz``
with ``clock_source: fixed_frequency`` (the default, as in the R scripts) and the recorded
timestamp difference with ``clock_source: sensor_timestamps``. Post-facto exports use a
constant speed (``dead_reckoning.constant_speed_m_s``, default 1.0 m/s) whatever
``speed_model`` says; the ``odba_scaled`` speed model is wired only in the streaming processor,
and the bundle's ``dead_reckoning`` step then records the configured model as
``configured_speed_model``. The bundle records the speed used per sample as ``speed_m_s``.
The integration is in ``PostFactoProcessor.calibrate_from_batch_data`` in
:src:`processors/lab.py`.

**Heading is magnetic.** It comes from the tilt-compensated magnetometer
(``atan2(-m_y, m_x)`` after the attachment rotation and the per-sample pitch and roll
rotation), with no declination applied. Near pitch :math:`\pm 90^\circ` the roll, and so the
heading, is numerically undefined and can jump; it is NaN only where pitch or roll is missing.

**No magnetometer, no dead reckoning.** Deployments whose tag has no magnetometer have no
heading, so they can only be placed by fix interpolation (below). Their dead-reckoned and
fix-pinned variants cannot be made.

Track models
------------

``dead_reckoning.track_model`` (default ``dead_reckoning``) decides how the integrated track
is placed relative to the fixes (:func:`~biologger_sim.core.track_models.apply_track_model`):

``dead_reckoning``
   The integrated track, anchored at the start fix. Its distance from the end fix at the end
   fix's time is the bundle's ``end_fix_miss`` metric: a direct measure of accumulated error.

``fix_pinned``
   The integrated track, rotated and scaled so it starts on the start fix and ends on the end
   fix. In the complex plane (north + i east) one factor
   (:func:`~biologger_sim.core.track_models.fix_pinning_factor`)

   .. math:: k = \frac{z_\text{end fix}}{z_\text{DR}(t_1) - z_\text{DR}(t_0)}

   maps the dead-reckoned fix-to-fix displacement onto the fixes; every sample becomes
   :math:`k\,(z_\text{DR} - z_\text{DR}(t_0))`. The angle of :math:`k` is a compass rotation
   (positive clockwise; it absorbs the tag's heading bias and the declination together) and its
   modulus a speed scale. The heading column is rotated by the same angle; the unrotated
   heading is kept internally. The bundle's ``placement`` step records ``scale``,
   ``rotation_deg`` and ``heading_correction_deg``. When the dead-reckoned fix-to-fix
   displacement is under 1 m the rotation is undefined, and the track falls back to fix
   interpolation.

``fix_interpolation``
   Linear in time between the fixes (the mean of a Brownian bridge). It ignores heading, so it
   is the only option without a magnetometer; depth and orientation still come from the tag.

A model that needs an end fix falls back to ``dead_reckoning`` when the deployment has none,
and the bundle reports the model actually used (``track_model_used``).

Ocean current correction
------------------------

The water moves too. With ``dead_reckoning.current_correction.forcingkit_url`` set, the
velocity over ground adds the current :math:`(u, v)` at the animal's position, time and depth:

.. math::

   n_i = n_{i-1} + (s\cos\psi_i + v_i)\,\Delta t_i, \qquad
   e_i = e_{i-1} + (s\sin\psi_i + u_i)\,\Delta t_i

How the current is obtained
(:func:`~biologger_sim.core.currents.compute_current_drift`, in :src:`core/currents.py`):

1. The dead-reckoned track is thinned to one point per ``sample_interval_s`` (60 s by
   default), always keeping the first and last record.
2. Each point is converted to latitude and longitude from the start fix, and its depth to
   forcingkit's z (meters, positive up; surface excursions clamp to 0).
3. forcingkit's trajectory interpolation samples ``u`` and ``v`` from the parent ocean model at
   those points. forcingkit, not the simulator, chooses the donor model by coverage (NECOFS on
   the Northeast shelf, HYCOM where NECOFS has none) and reports the donor it used; the
   bundle's ``current_correction`` step records it as ``donor_used``. forcingkit serves NECOFS
   regridded onto 200 m cells and 10 m levels (``vertical_spacing_m``). That grid looks finer
   than the model is: it interpolates NECOFS's own triangles.
4. The samples are interpolated linearly in time back to every record and integrated over the
   same time steps as dead reckoning, so the drift and the swim share one clock.

The correction is added **before** placement (``PostFactoProcessor._add_current_drift``, called
just before ``_place_track`` in :src:`processors/lab.py`). For ``fix_pinned`` this matters:
pinning then rotates and scales the current-corrected track, so the endpoints are the same with
or without the current, and the current changes the track's shape and the pinning factor
instead. For ``fix_interpolation`` the placed track depends only on the fixes, so the
correction changes only the recorded currents.

**Missing forcing is still water.** A sample with no value (on land, below the model's sea
floor, or outside every donor's grid) counts as zero current. The count is logged and recorded
in the ``current_correction`` step, and the bundle's ``current_missing`` flag marks each
stretch that leans on one. A track where every sample is missing is left uncorrected and the
step is recorded as failed.

If the service is unreachable or the client is missing, the track is left uncorrected, the
step is recorded as failed with the error, and the export still completes.

Configuration (post-facto mode):

.. code-block:: yaml

   dead_reckoning:
     track_model: fix_pinned          # dead_reckoning (default) | fix_pinned | fix_interpolation
     constant_speed_m_s: 1.0
     current_correction:
       forcingkit_url: "http://localhost:9598"   # null (default) turns it off
       sample_interval_s: 60.0
       vertical_spacing_m: 10.0
       cache_dir: null                           # client chunk cache (null: client default)
       timeout_s: 1800.0

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
     - Yes (reanalysis); ends in 2024
   * - Used by the correction
     - Yes, forcingkit's first choice on the Northeast shelf
     - No; forcingkit does not offer it for trajectories

Over the forcing stores cut for the RED001 swordfish deployment (an area about 50 km on a side
at the shelf break, read on the models' native grids for 11 to 14 August 2022), NECOFS has
about 1200 triangles with a median edge of about 1.5 km; DOPPIO covers the same area with about
10 by 10 cells. Neither resolves a canyon a few kilometers wide well; NECOFS has a few
triangles across one, DOPPIO none. Canyon-scale features in NECOFS, such as a closed eddy at a
canyon mouth, may come from steep sigma layers over steep topography and should not be read
as established without observations. Neither model is a measurement. Credit NECOFS/UMASSD
(SMAST, UMass Dartmouth) and the Rutgers University Ocean Modeling Group (DOPPIO) wherever
their currents are shown.

Known limit: where the current is sampled
-----------------------------------------

The current is sampled once, at the dead-reckoned through-water positions, before placement.
Those positions are only as good as the dead reckoning. Two things move the final track away
from them:

- the drift itself, when it reaches several kilometers or more; and
- pinning, which turns and stretches the whole track.

For the RED001 swordfish deployment (bundles ``dr`` and ``pin_cur`` exported from
biologger-sim ``87b294f``), pinning the current-corrected track turns it by 57.0 degrees and
scales it by 1.14, so the pinned track runs a median of 11.6 km (at most 17.0 km, over its
1 Hz samples) from the positions where its current was sampled. The applied NECOFS drift is
6.7 km toward 262 degrees (``drift_end_m``). Re-sampled through forcingkit along the pinned
track instead, the same NECOFS current gives 1.8 km toward 249 degrees. A separate reading of
each model on its native grid along the pinned track (nearest triangle or cell, at the
animal's depth, hourly records interpolated) gave 2.1 km toward 254 degrees for NECOFS and
4.1 km toward 269 degrees for DOPPIO; that reading needs the model stores themselves and is
kept with the project's review notes, not in this repository. The direction is consistent; the
size depends on where the current is sampled and which model is asked, by a factor of two to
three. RED001's smaller miss at the end fix with the current (12.1 km against 17.0 km without)
therefore cannot yet be credited to the current.

All the figures above except the native-grid reading come from two bundles and are
recomputed by ``scripts/current_sampling_offset.py``:

.. code-block:: bash

   python scripts/current_sampling_offset.py <tracks>/<run>_dr <tracks>/<run>_pin_cur \
       --forcingkit-url http://localhost:9598   # optional: re-sample along the placed track

With a parent model resolving about 1.5 km (NECOFS at the shelf break), a current sampled
kilometers away is a different current. Until the correction is iterated (place, re-sample at
the placed positions, place again), read a corrected track as "the track with the model current
along the dead-reckoned path", and check ``drift_end_m`` and the pinning turn before trusting
it.

What a bundle records
---------------------

``track.f32`` holds one row per output sample (``--rate``, 1 Hz by default; written by
:func:`~biologger_sim.io.track_bundle.write_bundle`). Every bundle has ``t``, ``north_m``,
``east_m``, ``depth_m``, ``heading_deg``, ``pitch_deg``, ``roll_deg``, ``vedba``, ``odba`` and
the roll continuity columns. These are added when the run produced them:

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
     - Through-water speed used by dead reckoning, before placement (a fix-pinned track scales
       it by the placement step's ``scale``); present whenever the run has a heading
   * - ``accel_static_x``, ``_y``, ``_z``
     - run's ``vedba`` unit
     - Static (low-passed) acceleration, which points along gravity
   * - ``accel_dynamic_x``, ``_y``, ``_z``
     - run's ``vedba`` unit
     - Dynamic acceleration (total minus static), at sample time

The acceleration columns, like ``vedba`` and ``odba``, are in the run's unit: m/s\ :sup:`2` for
lab mode, g for streaming mode (``track.json`` lists each column's unit). Their frame is the
body (tag) axes after the attachment rotation, forward-right-down: x toward the head, y to the
right, z down. Pitch and roll come from the static part as
``pitch_deg = -atan2(x, hypot(y, z))`` (nose up positive) and ``roll_deg = atan2(y, z)``
(right side down positive).

``track.json`` describes how the track was made, so that two bundles can be compared step by
step:

``pipeline``
   The ordered steps, each ``{step, method, version, status, params}``: ``dead_reckoning``
   (method ``constant``, with ``constant_speed_m_s`` and ``true_integration``),
   ``current_correction`` (``forcingkit``, with ``donor_used``, ``samples``, ``missing``,
   ``drift_end_m`` as north and east meters, and the forcing store's attributes; status
   ``failed`` with an ``error`` when it could not be applied) and ``placement`` (the model
   used, with ``scale``, ``rotation_deg`` and ``heading_correction_deg`` for ``fix_pinned``).

``metrics``
   ``end_fix_miss_before_placement`` and ``end_fix_miss``, in meters. "Before placement" is the
   dead-reckoned track, with the current when it was applied; for a fix-pinned track
   ``end_fix_miss`` is zero by construction.

``reproducibility``
   A SHA-256 fingerprint over the recipe: the sim commit, any uncommitted diff, the
   environment, the resolved config, the tag data file, the deployment's metadata row and the
   forcing store. ``config.yaml`` and ``environment.txt`` sit beside ``track.json``, and
   ``code.patch`` when the simulator's tree was dirty.

Comparing reconstructions
-------------------------

The four variants exported for each deployment (their run IDs end in the variant name) differ
only in ``track_model`` and whether ``current_correction`` is set:

.. list-table::
   :header-rows: 1

   * - Variant
     - ``track_model``
     - Current
     - What it shows
   * - ``dr``
     - ``dead_reckoning``
     - off
     - The tag alone; the miss at the end fix is the accumulated error
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
     - The same, with the current's shape added before pinning

The biologger portal's compare page (``/deployments/<id>/compare``) draws a deployment's
variants together, with the depth against the seafloor under each and their separation over
time.
