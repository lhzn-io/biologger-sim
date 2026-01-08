=======================
Omniverse Visualization
=======================

The visualization component of ``biologger-sim`` uses NVIDIA Omniverse USD Composer to render a high-fidelity digital twin of the tracked animal.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   user_guide
   architecture

Key Features
------------

*   **Real-time telemetry streaming** via ZeroMQ at 60+ Hz
*   **Automatic NED → USD coordinate conversion** with validated slip angle diagnostics
*   **Flexible mesh orientation** supporting arbitrary asset authoring conventions
*   **Instant replay** with full trajectory visualization and time-travel scrubbing

Architecture
------------

The system uses a "Hybrid" architecture:

1.  **Simulation (WSL/Linux)**: Runs the Python pipeline and publishes telemetry via ZeroMQ.
2.  **Visualization (Windows/Omniverse)**: Subscribes to the ZeroMQ stream and updates the 3D scene.

.. image:: ../../figures/architecture_diagram.png
   :alt: Architecture Diagram
   :align: center

Quick Reference
---------------

.. seealso::

   :ref:`coordinate-conventions`
      Understanding NED vs USD coordinate systems and automatic conversion.

   :ref:`mesh-orientation`
      How animal mesh assets are aligned with USD conventions via spawn rotations.

   :ref:`slip-angle-validation`
      Diagnostic metrics for validating heading/velocity alignment.
