===============
Getting Started
===============

Installation
============

From Source (Recommended)
-------------------------

.. code-block:: bash

   git clone https://github.com/lhzn-io/biologger-sim.git
   cd biologger-sim
   micromamba env create -f environment.yml
   micromamba activate biologger-sim
   pip install -e .

Basic Usage
===========

Command-Line Interface
----------------------

.. code-block:: bash

   # Run simulation (streaming mode)
   python -m biologger_sim --config config/Swordfish-RED001_20220812_19A0564-causal.yaml

   # Run lab analysis (post-facto mode)
   python -m biologger_sim --config config/Swordfish-RED001_20220812_19A0564-postfacto.yaml

   # Write a track bundle from a LAB-mode config (see Tracks and ocean currents)
   python -m biologger_sim export-track --config config/Swordfish-RED001_20220812_19A0564-postfacto.yaml --rate 1

``--config`` without a subcommand runs ``run``. ``run`` also takes ``--speed``, ``--uncork``
(no rate limit), ``--stop-at SECONDS``, ``--no-publish-zmq``, ``--topobathykit-url`` and
``--set key=value`` overrides. ``export-track`` takes ``--config`` or ``--from-run RUN_DIR``,
``--rate`` (Hz, default 1), ``--out`` and ``--set``.

Python API
----------

.. code-block:: python

   from biologger_sim.processors.lab import PostFactoProcessor

   # Create post-facto processor
   processor = PostFactoProcessor(
       filt_len=48,
       freq=16,
       r_exact_mode=True
   )

   # Process data (example)
   # result = processor.process(record)

Configuration
=============

The pipeline reads YAML configuration files. The ``config/`` directory holds example configs for
several tags. The two used above are:

- ``Swordfish-RED001_20220812_19A0564-causal.yaml``: real-time simulation
- ``Swordfish-RED001_20220812_19A0564-postfacto.yaml``: lab analysis

Files ending in ``-causal`` run Simulation Mode, and files ending in ``-postfacto`` run Lab Mode.
``Swordfish-RED001_20220812_19A0564-causal-mlx.yaml`` runs Simulation Mode on the MLX backend.

Calibration Modes
-----------------

Both pipelines share one ``calibration:`` config block
(``attachment_angle_mode`` and ``magnetometer_mode``) with two modes:

**Fixed** (pre-computed values)
   Uses locked calibration parameters (``locked_*``) from prior runs.
   This mode is the fastest because it makes a single pass with no calibration step.
   It requires a prior calibration from batch_compute or from the R analysis. The streaming
   processor always uses the locked values.

**Batch Compute** (default; post-facto only)
   Processes the data in two passes. The first pass collects the full dataset and computes the
   calibrations. The second pass reprocesses the data with them.
   Matches R gRumble's ``colMeans()`` and ``MagOffset()`` exactly.
   The validation target is an error below 0.1° against the R reference implementation.

Next Steps
==========

- :doc:`pipelines` describes the pipeline architecture in detail.
- :doc:`visualization/index` covers the Omniverse setup.
