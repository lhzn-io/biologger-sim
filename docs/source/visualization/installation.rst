=========================
Installation & Setup
=========================

This guide sets up the Omniverse Kit app that runs the visualizer on Windows. It also configures
the "Hybrid" workflow, which connects the simulation in WSL to the visualizer on Windows.

Windows Setup (Visualization)
-----------------------------

On Windows, install the Omniverse applications from the **Kit App Template**. The Kit App
Template replaces the Omniverse Launcher, which is deprecated.

Prerequisites
~~~~~~~~~~~~~

*   **OS**: Windows 10 or 11 (64-bit)
*   **GPU**: NVIDIA RTX GPU (RTX 3070 or higher recommended)
*   **Driver**: NVIDIA Studio Driver **>=591.44** (Verified 2026-01-02)

    .. warning::
       **Laptop Users (RTX 5080 etc.)**: Avoid Game Ready Driver 591.59, which conflicts with
       Intel integrated graphics. Use the **NVIDIA App** to install the **Studio Driver**
       (591.44+) instead.

*   **Tools**:
    *   Git
    *   Visual Studio 2019 or 2022 (with "Desktop development with C++" workload)

Installation Steps
~~~~~~~~~~~~~~~~~~

1. Configure Environment
^^^^^^^^^^^^^^^^^^^^^^^^

Before you clone the template, set up the Packman dependency cache. A local cache shortens
downloads and avoids path problems.

1.  Open PowerShell as Administrator.
2.  Set the ``PM_PACKAGES_ROOT`` environment variable to a local path (e.g., ``C:\packman-repo``):

    .. code-block:: powershell

       setx PM_PACKAGES_ROOT "C:\packman-repo"

3.  Close and reopen PowerShell to apply the change.

2. Clone the Kit App Template
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The visualizer app lives in the separate ``biologger-viz`` repository, which is a Kit App
Template project (Kit 109.0.2). To start a new app from the template, clone the official template
repository to a **local drive** (e.g., ``C:\Projects``). Do not clone into a network share or WSL
mount.

.. code-block:: powershell

   cd C:\Projects
   git clone https://github.com/NVIDIA-Omniverse/kit-app-template.git
   cd kit-app-template

3. Build and Launch
^^^^^^^^^^^^^^^^^^^

Build with ``.\repo.bat build`` and launch with ``.\repo.bat launch``, as the template README
describes. The release build also writes one launcher script per app. In ``biologger-viz`` the
visualizer launcher is ``_build\windows-x86_64\release\whoimpg.biologger.sim.kit.bat``. The app
definitions it runs are ``source\apps\whoimpg.biologger.sim.kit`` and
``whoimpg.biologger.sim_streaming.kit``.

Linux and Jetson Hosts
----------------------

This repository has no Linux, container, or Jetson setup for the Kit app. The Jetson hosts
(``skipper.internal``, an AGX Thor, and ``mariner.internal``, an AGX Orin) are aarch64 machines;
this guide does not cover running the visualizer on them.

Hybrid Workflow (WSL + Windows)
-------------------------------

This section sets up the "Hybrid" development environment. The **Simulation** runs in WSL
(Linux), and the **Visualization** runs in the ``biologger-viz`` Kit app on Windows.

.. note::
   In a standard WSL2 configuration, Windows reaches WSL ports through ``localhost``
   automatically. The simulation publishes on port 5555 by default.

Configuration Instructions
~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Prepare the Simulation (WSL)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Activate the environment, install the package, and check that the simulation runs:

.. code-block:: bash

    # In WSL Terminal
    micromamba activate biologger-sim
    pip install -e .

    # Verify you can run the help command
    python -m biologger_sim --help

2. Link the Extension (Windows)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The extension source is ``omniverse/extensions/whoimpg.biologger.subscriber`` in this repository,
inside WSL. ``biologger-viz`` does not copy it. Its
``source\extensions\whoimpg.biologger.subscriber`` is a symbolic link to the WSL folder, for
example
``\\wsl$\Ubuntu-24.04\home\lhzn\Projects\whoi-mpg\biologger-sim\omniverse\extensions\whoimpg.biologger.subscriber``.
The build's ``_build\windows-x86_64\release\exts\whoimpg.biologger.subscriber`` folder holds
junctions back into ``source\extensions``. Kit therefore runs the WSL source directly, and edits in
WSL take effect at the next launch.

``omniverse/apps`` in this repository holds copies of the two ``.kit`` files. They differ slightly
from the copies in ``biologger-viz`` (for example, the extension search path is ``../extensions``
here and ``../exts`` there). The ``biologger-viz`` copies are the ones that run.

3. Run
^^^^^^

1.  Launch the visualizer from Windows (see "Build and Launch" above).
2.  In WSL, start the simulation:

    .. code-block:: bash

        python -m biologger_sim run --config config/Swordfish-RED001_20220812_19A0564-causal.yaml
