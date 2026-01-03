=======================
Omniverse Visualization
=======================

The visualization component of ``biologger-sim`` uses NVIDIA Omniverse USD Composer to render a high-fidelity digital twin of the tracked animal.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   setup_windows
   setup_ubuntu
   hybrid_workflow
   architecture

Architecture
------------

The system uses a "Hybrid" architecture:

1.  **Simulation (WSL/Linux)**: Runs the Python pipeline and publishes telemetry via ZeroMQ.
2.  **Visualization (Windows/Omniverse)**: Subscribes to the ZeroMQ stream and updates the 3D scene.

.. image:: ../../figures/architecture_diagram.png
   :alt: Architecture Diagram
   :align: center
