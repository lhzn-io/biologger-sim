.. Biologger Sim documentation master file

====================================
Biologger Sim Documentation
====================================

**Real-time simulation environment for marine animal tracking and behavioral prediction**

Biologger Sim provides a simulation framework for developing and validating biologger algorithms. It supports a "Dual-Mode" architecture:

1. **Lab Mode**: High-precision, acausal processing for post-hoc analysis.
2. **Simulation Mode**: Real-time, causal processing for on-tag algorithm development.

It integrates with **NVIDIA Omniverse** via ZeroMQ for high-fidelity visualization.

.. image:: https://img.shields.io/badge/python-3.10+-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python Version

.. image:: https://img.shields.io/badge/license-MIT-green.svg
   :target: https://github.com/lhzn-io/biologger-sim/blob/main/LICENSE
   :alt: License

Features
========

**Dual-Mode Processing**
   - **Lab Mode**: Replicates R-based post-hoc analysis with batch calibration and acausal filtering.
   - **Simulation Mode**: Simulates real-time tag constraints with causal filtering and online calibration.

**High-Fidelity Visualization**
   - ZeroMQ integration with NVIDIA Omniverse.
   - Real-time streaming of sensor data and derived metrics.

**Configurable Pipelines**
   - YAML-based configuration for species-specific parameters.
   - Support for custom sensor fusion and behavioral classification models.

Quick Start
===========

.. code-block:: bash

   # Install from source
   git clone https://github.com/lhzn-io/biologger-sim.git
   cd biologger-sim
   micromamba env create -f environment.yml
   micromamba activate biologger-sim
   pip install -e .

   # Run simulation
   python -m biologger_sim --config config/Swordfish-RED001_20220812_19A0564-postfacto.yaml

Documentation
=============

.. toctree::
   :maxdepth: 2
   :caption: Contents

   getting_started
   pipelines
   processors
   design/simulation_architecture
   visualization/index
   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
