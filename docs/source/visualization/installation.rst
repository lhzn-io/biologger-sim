=========================
Installation & Setup
=========================

This guide covers the installation of NVIDIA Omniverse applications on Windows and Ubuntu (for headless setups), as well as configuring the "Hybrid" workflow connecting WSL to Windows.

Windows Setup (Visualization)
-----------------------------

This guide covers the installation of NVIDIA Omniverse applications on Windows using the **Kit App Template**. This is the modern, developer-centric approach replacing the deprecated Omniverse Launcher.

Prerequisites
~~~~~~~~~~~~~

*   **OS**: Windows 10 or 11 (64-bit)
*   **GPU**: NVIDIA RTX GPU (RTX 3070 or higher recommended)
*   **Driver**: NVIDIA Studio Driver **>=591.44** (Verified 2026-01-02)

    .. warning::
       **Laptop Users (RTX 5080 etc.)**: Avoid Game Ready Driver 591.59. It is known to cause conflicts with Intel integrated graphics. Use the **NVIDIA App** to install the **Studio Driver** (591.44+) instead.

*   **Tools**:
    *   Git
    *   Visual Studio 2019 or 2022 (with "Desktop development with C++" workload)

Installation Steps
~~~~~~~~~~~~~~~~~~

1. Configure Environment
^^^^^^^^^^^^^^^^^^^^^^^^

Before cloning, set up the Packman dependency cache to avoid long download times and path issues.

1.  Open PowerShell as Administrator.
2.  Set the ``PM_PACKAGES_ROOT`` environment variable to a local path (e.g., ``C:\packman-repo``):

    .. code-block:: powershell

       setx PM_PACKAGES_ROOT "C:\packman-repo"

3.  Close and reopen PowerShell to apply the change.

2. Clone the Kit App Template
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Clone the official template repository to a **local drive** (e.g., ``C:\Projects``). Do not clone into a network share or WSL mount.

.. code-block:: powershell

   cd C:\Projects
   git clone https://github.com/NVIDIA-Omniverse/kit-app-template.git
   cd kit-app-template

Ubuntu Setup (Headless Simulation)
----------------------------------

This guide covers setting up NVIDIA Omniverse in a Docker container on Ubuntu. This is useful for headless simulation, CI/CD, or running on a Linux server (e.g., NVIDIA Thor).

Prerequisites
~~~~~~~~~~~~~

*   **OS**: Ubuntu 20.04 or 22.04
*   **GPU**: NVIDIA RTX GPU
*   **Driver**: Latest NVIDIA Linux Driver

Step 1: NVIDIA Developer Account & NGC
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To access Omniverse container images, you need an NVIDIA NGC account.

1.  **Register**: Go to `ngc.nvidia.com <https://ngc.nvidia.com/>`_ and create an account.
2.  **API Key**:
    *   Log in to NGC.
    *   Click your user profile (top right) > **Setup**.
    *   Click **Get API Key**.
    *   Click **Generate API Key**.
    *   **SAVE THIS KEY**. You cannot see it again.

Step 2: Install Docker & NVIDIA Container Toolkit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you haven't already, install Docker and the NVIDIA runtime.

.. code-block:: bash

    # 1. Install Docker
    curl https://get.docker.com | sh \
      && sudo systemctl --now enable docker

    # 2. Setup NVIDIA Container Toolkit repository
    curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
      && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
        sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
        sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

    # 3. Install Toolkit
    sudo apt-get update
    sudo apt-get install -y nvidia-container-toolkit

    # 4. Configure Docker
    sudo nvidia-ctk runtime configure --runtime=docker
    sudo systemctl restart docker

Hybrid Workflow (WSL + Windows)
-------------------------------

This section explains how to set up the "Hybrid" development environment where the **Simulation** runs in WSL (Linux) and the **Visualization** runs in NVIDIA Omniverse USD Composer on Windows.

Architecture
~~~~~~~~~~~~

*   **Simulation (WSL)**: Runs the Python pipeline (``biologger-sim``). Publishes telemetry via ZeroMQ (ZMQ) on port ``5555``.
*   **Visualization (Windows)**: Runs Omniverse USD Composer. The ``whoimpg.biologger.subscriber`` extension connects to ``localhost:5555`` to receive data.

.. note::
   Windows can access WSL ports via ``localhost`` automatically in standard WSL2 configurations.

Configuration Instructions
~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Prepare the Simulation (WSL)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ensure your environment is ready and you can run the simulation:

.. code-block:: bash

    # In WSL Terminal
    micromamba activate biologger-sim
    pip install -e .

    # Verify you can run the help command
    python -m biologger_sim --help

2. Configure Omniverse (Windows)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We need to tell Omniverse where to find our custom extension. Since the code lives in WSL, we will point Omniverse to the network path.

1.  **Find your WSL Path**:
    *   Open Windows Explorer.
    *   Type ``\\wsl.localhost\Ubuntu`` (or your distro name) in the address bar.
    *   Navigate to your project folder: ``.../biologger-sim/omniverse/extensions``.
    *   Copy this path. It should look like: ``\\wsl.localhost\Ubuntu\home\username\Projects\whoi-mpg\biologger-sim\omniverse\extensions``.
