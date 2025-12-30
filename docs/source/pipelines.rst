=========================================
Pipeline Architecture: Lab vs Simulation
=========================================

The package provides **two distinct processing pipelines** designed for different stages of the research workflow.

Lab Mode (Post-Facto)
=====================

**High-Precision Analysis & Validation**

The Lab Mode pipeline is designed for batch analysis where the complete dataset is available. It aims for parity with the legacy R implementation.

Characteristics
---------------

- **Memory**: Full dataset loaded into memory.
- **Processing**: Acausal algorithms (e.g., `filtfilt`, centered moving averages).
- **Calibration**: Batch computation from the full dataset.
- **Depth**: Acausal interpolation of missing values.

Configuration
-------------

To enable Lab Mode, set the following in your YAML config:

.. code-block:: yaml

   pipeline:
     mode: "LAB"
     calibration:
       attachment_angle: "batch_compute"
       magnetometer: "batch_compute"
     depth:
       mode: "interpolate"

Simulation Mode (Real-Time)
===========================

**On-Tag Algorithm Development**

The Simulation Mode pipeline is designed for real-time processing where data arrives sample-by-sample. It uses fully causal algorithms with no lookahead.

Characteristics
---------------

- **Memory**: Fixed memory footprint (O(1)).
- **Processing**: Causal algorithms (e.g., `lfilter`, EMA).
- **Calibration**: Online adaptive calibration or fixed parameters.
- **Depth**: Real-time estimation (hold last value or predict).

Configuration
-------------

To enable Simulation Mode, set the following in your YAML config:

.. code-block:: yaml

   pipeline:
     mode: "SIMULATION"
     calibration:
       attachment_angle: "fixed"  # or "progressive" (future)
       magnetometer: "fixed"
     depth:
       mode: "realtime"
