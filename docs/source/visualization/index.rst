=======================
Omniverse Visualization
=======================

The ``biologger-sim`` visualizer is an NVIDIA Omniverse Kit app that renders a 3D model of the
tracked animal and moves it with the tag data. The app is built from the Kit App Template in the
separate ``biologger-viz`` repository. It runs the ``whoimpg.biologger.subscriber`` extension,
whose source is in this repository.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   user_guide
   scene
   controls
   architecture

Features
--------

*   **Real-time telemetry streaming** via ZeroMQ. The simulator sends every sample, grouped in
    MessagePack batches (one batch per 50 ms of wall time or per 1000 samples).
*   **Automatic NED → USD coordinate conversion** (NED: north-east-down), with slip angle
    diagnostics that check the conversion.
*   **Mesh orientation** that handles any axis convention used to author the asset.
*   **Replay** of the full trajectory, with scrubbing forward and backward in time.
*   **Georeferenced scene**. The track is anchored to its deployment fixes and drawn over a fused
    DEM (digital elevation model). The scene shows the position uncertainty region and sets the
    sun, sky and water for the deployment's place and date (:doc:`scene`).
*   **Overview tools**: vertical exaggeration, and a trail whose width follows the camera
    distance (:doc:`controls`).

Architecture
------------

The system runs as two parts (the "Hybrid" architecture):

1.  **Simulation (WSL/Linux)**: Runs the Python pipeline and publishes telemetry via ZeroMQ.
2.  **Visualization (Windows/Omniverse)**: Subscribes to the ZeroMQ stream and updates the 3D scene.

Quick Reference
---------------

.. seealso::

   :ref:`coordinate-conventions`
      The NED and USD coordinate systems and the automatic conversion between them.

   :ref:`mesh-orientation`
      How spawn rotations align animal mesh assets with USD conventions.

   :ref:`slip-angle-validation`
      Metrics that check whether heading and velocity are aligned.
