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
``--set key=value`` overrides; ``export-track`` takes ``--config`` or ``--from-run RUN_DIR``,
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

The pipeline uses YAML configuration files. Example configurations are provided in the ``config/`` directory:

- ``Swordfish-RED001_20220812_19A0564-causal.yaml`` - Real-time simulation
- ``Swordfish-RED001_20220812_19A0564-postfacto.yaml`` - Lab analysis

Calibration Modes
-----------------

Both pipelines share a unified ``calibration:`` config block
(``attachment_angle_mode`` and ``magnetometer_mode``) with two modes:

**Fixed** (pre-computed values)
   Uses locked calibration parameters (``locked_*``) from prior runs.
   Fastest processing (single-pass, no calibration overhead).
   Requires prior calibration from batch_compute or R analysis. The streaming processor
   always uses the locked values.

**Batch Compute** (default; post-facto only)
   Two-pass processing: collect full dataset, compute calibrations, reprocess.
   Matches R gRumble's ``colMeans()`` and ``MagOffset()`` exactly.
   Validation target: <0.1° error vs. R reference implementation.

Next Steps
==========

- See :doc:`pipelines` for detailed pipeline architecture
- Check :doc:`visualization/index` for Omniverse setup
