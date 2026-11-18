Tracks and ocean currents
=========================

A track bundle (``python -m biologger_sim export-track``) places the animal in space from three
things: the tag's own motion sensors, the deployment's position fixes, and, optionally, the
ocean current from a parent ocean model. This page explains how they combine, so that two
reconstructions of the same deployment can be compared knowing exactly what differs.

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
:math:`s` the through-water speed. Post-facto exports use a constant speed
(``dead_reckoning.constant_speed_m_s``, default 1.0 m/s); the ``odba_scaled`` speed model exists
only in the streaming processor. The bundle records the speed used per sample as ``speed_m_s``.

**Heading is magnetic.** It comes from the tilt-compensated magnetometer
(``atan2(-m_y, m_x)`` after the pitch and roll rotation), with no declination applied. Near
pitch :math:`\pm 90^\circ` the roll, and so the heading, is numerically undefined and can jump;
it is NaN only where pitch or roll is missing.

**No magnetometer, no dead reckoning.** Deployments whose tag has no magnetometer have no
heading, so they can only be placed by fix interpolation (below). Their dead-reckoned and
fix-pinned variants cannot be made.

Track models
------------

``dead_reckoning.track_model`` decides how the integrated track is placed relative to the fixes:

``dead_reckoning``
   The integrated track, anchored at the start fix. Its distance from the end fix at the end
   time is the bundle's ``end_fix_miss`` metric: a direct measure of accumulated error.

``fix_pinned``
   The integrated track, rotated and scaled so it starts on the start fix and ends on the end
   fix. In the complex plane (north + i east) one factor

   .. math:: k = \frac{z_\text{end fix}}{z_\text{DR}(t_1) - z_\text{DR}(t_0)}

   maps the dead-reckoned fix-to-fix displacement onto the fixes; every sample becomes
   :math:`k\,(z_\text{DR} - z_\text{DR}(t_0))`. The angle of :math:`k` is a compass rotation
   (it absorbs the tag's heading bias and the declination together) and its modulus a speed
   scale. The heading column is rotated by the same angle; the unrotated heading is kept
   internally. The bundle's ``placement`` step records ``scale`` and ``rotation_deg``.

``fix_interpolation``
   Linear in time between the fixes (the mean of a Brownian bridge). It ignores heading, so it
   is the only option without a magnetometer; depth and orientation still come from the tag.

A model that needs an end fix falls back to ``dead_reckoning`` when the deployment has none,
and the bundle reports the model actually used.

Ocean current correction
------------------------

The water moves too. With ``dead_reckoning.current_correction.forcingkit_url`` set, the
velocity over ground adds the current :math:`(u, v)` at the animal's position, time and depth:

.. math::

   n_i = n_{i-1} + (s\cos\psi_i + v_i)\,\Delta t_i, \qquad
   e_i = e_{i-1} + (s\sin\psi_i + u_i)\,\Delta t_i

How the current is obtained (``biologger_sim.core.currents.compute_current_drift``):

1. The dead-reckoned track is thinned to one point per ``sample_interval_s`` (60 s by
   default), always keeping the first and last record.
2. Each point is converted to latitude and longitude from the start fix, and its depth to
   forcingkit's z (meters, positive up; surface excursions clamp to 0).
3. forcingkit's trajectory interpolation samples ``u`` and ``v`` from the parent ocean model at
   those points. forcingkit chooses the donor model by coverage (NECOFS on the Northeast shelf,
   HYCOM otherwise) and reports the donor it used; the bundle records it as ``donor_used``.
4. The samples are interpolated back to every record and integrated over the same time steps
   as dead reckoning, so the drift and the swim share one clock.

The correction is added **before** placement. For ``fix_pinned`` this matters: pinning then
rotates and scales the current-corrected track, so the endpoints are the same with or without
the current, and the current changes the track's shape and the pinning factor instead.

**Missing forcing is still water.** A sample with no value (on land, below the model's sea
floor, or outside every donor's grid) counts as zero current. The count is logged and recorded
in the ``current_correction`` step, and the bundle's ``current_missing`` flag marks each
stretch that leans on one. A track where every sample is missing is left uncorrected.

**Known limit: where the current is sampled.** The current is sampled once, at the
dead-reckoned through-water positions, before placement. Those positions are only as good as
the dead reckoning. Two things move the final track away from them:

- the drift itself, when it reaches several kilometers or more; and
- pinning, which turns and stretches the whole track. RED001's pinning turns it by 57 degrees,
  so the pinned track runs a median of 11.6 km (at most 17 km) from the positions where its
  current was sampled. Sampled along the pinned track instead, the NECOFS current over the same
  hours adds 2.1 km of drift rather than 6.7 km.

With a parent model resolving 1 to 2 km (NECOFS near the shelf break), a current
sampled kilometers away is a different current. Until the correction is iterated (place,
re-sample at the placed positions, place again), read a corrected track as "the track with the
model current along the dead-reckoned path", and check ``drift_end_m`` and the pinning turn
before trusting it.

If the service is unreachable or the client is missing, the track is left uncorrected, the
step is recorded as failed, and the export still completes.

Configuration (post-facto mode):

.. code-block:: yaml

   dead_reckoning:
     track_model: fix_pinned          # dead_reckoning | fix_pinned | fix_interpolation
     constant_speed_m_s: 1.0
     current_correction:
       forcingkit_url: "http://garnet.internal:9598"   # null (default) turns it off
       sample_interval_s: 60.0
       vertical_spacing_m: 10.0
       timeout_s: 1800.0

What a bundle records
---------------------

``track.f32`` holds one row per output sample (1 Hz by default). Besides position, depth and
attitude, a run with the current correction adds:

.. list-table::
   :header-rows: 1
   :widths: 25 10 65

   * - Column
     - Unit
     - Meaning
   * - ``current_east_m_s``
     - m/s
     - Eastward current applied at the animal's depth, at sample time
   * - ``current_north_m_s``
     - m/s
     - Northward current applied at the animal's depth, at sample time
   * - ``current_missing``
     - flag
     - 1 if a missing forcing sample (still water) was used since the previous output sample
   * - ``speed_m_s``
     - m/s
     - Through-water speed used by dead reckoning, before placement (a fix-pinned track scales
       it by the placement step's ``scale``)

``track.json`` describes how the track was made, so that two bundles can be compared step by
step:

``pipeline``
   The ordered steps, each ``{step, method, version, status, params}``: ``dead_reckoning``
   (method ``constant``, with its speed), ``current_correction`` (``forcingkit``, with
   ``donor_used``, ``samples``, ``missing``, ``drift_end_m`` and the forcing store's attributes)
   and ``placement`` (``fix_pinned`` with ``scale`` and ``rotation_deg``, for example).

``metrics``
   ``end_fix_miss_before_placement`` and ``end_fix_miss``, in meters.

``reproducibility``
   A SHA-256 fingerprint over the recipe: the sim commit, any uncommitted diff, the
   environment, the resolved config, the tag data file, the deployment's metadata row and the
   forcing store. ``config.yaml`` and ``environment.txt`` sit beside ``track.json``.

Comparing reconstructions
-------------------------

The four standard variants of a deployment differ only in ``track_model`` and whether
``current_correction`` is set:

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
