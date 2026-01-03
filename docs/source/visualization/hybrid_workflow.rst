=========================
Hybrid Workflow (WSL)
=========================

This guide explains how to set up the "Hybrid" development environment where the **Simulation** runs in WSL (Linux) and the **Visualization** runs in NVIDIA Omniverse USD Composer on Windows.

Architecture
------------

*   **Simulation (WSL)**: Runs the Python pipeline (``biologger-sim``). Publishes telemetry via ZeroMQ (ZMQ) on port ``5555``.
*   **Visualization (Windows)**: Runs Omniverse USD Composer. The ``whoimpg.biologger.subscriber`` extension connects to ``localhost:5555`` to receive data.

.. note::
   Windows can access WSL ports via ``localhost`` automatically in standard WSL2 configurations.

Prerequisites
-------------

1.  **WSL2**: Ubuntu 22.04 or later recommended.
2.  **Python Environment**: The ``biologger-sim`` environment set up in WSL.
3.  **NVIDIA Omniverse**: Installed on Windows (see :doc:`setup_windows`).

Setup Instructions
------------------

1. Prepare the Simulation (WSL)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ensure your environment is ready and you can run the simulation:

.. code-block:: bash

    # In WSL Terminal
    micromamba activate biologger-sim
    pip install -e .

    # Verify you can run the help command
    python -m biologger_sim --help

2. Configure Omniverse (Windows)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We need to tell Omniverse where to find our custom extension. Since the code lives in WSL, we will point Omniverse to the network path.

1.  **Find your WSL Path**:
    *   Open Windows Explorer.
    *   Type ``\\wsl.localhost\Ubuntu`` (or your distro name) in the address bar.
    *   Navigate to your project folder: ``.../biologger-sim/omniverse/extensions``.
    *   Copy this path. It should look like: ``\\wsl.localhost\Ubuntu\home\username\Projects\whoi-mpg\biologger-sim\omniverse\extensions``.

2.  **Add to Extension Manager**:
    *   Launch **USD Composer** on Windows.
    *   Go to **Window > Extensions**.
    *   Click the **Gear Icon** (Settings) in the top-right of the Extensions window.
    *   Under **Extension Search Paths**, click the **+** button.
    *   Paste the WSL path you copied above.

3.  **Enable the Extension**:
    *   Search for "Biologger" in the Extensions window.
    *   You should see **Biologger ZMQ Subscriber**.
    *   Toggle the **Enabled** switch.
    *   A small window titled "Biologger Telemetry" should appear in the viewport.

Running the Loop
----------------

Step 1: Start the Simulation (WSL)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run the simulation in "lab mode" or "simulation mode" with a config that enables ZMQ.

.. code-block:: bash

    # In WSL
    python -m biologger_sim run --config config/Swordfish-RED001_20220812_19A0564-postfacto.yaml

*Note: Ensure your config has `zmq: enabled: true` and port `5555`.*

Step 2: Connect in Omniverse (Windows)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1.  With the simulation running, look at the **Biologger Telemetry** window in Omniverse.
2.  The status should change from "Disconnected" to "Connected".
3.  You should see telemetry metrics updating.
