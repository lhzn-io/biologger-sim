=========================
Windows Setup (Kit App)
=========================

This guide covers the installation of NVIDIA Omniverse applications on Windows using the **Kit App Template**. This is the modern, developer-centric approach replacing the deprecated Omniverse Launcher.

Prerequisites
-------------

*   **OS**: Windows 10 or 11 (64-bit)
*   **GPU**: NVIDIA RTX GPU (RTX 3070 or higher recommended)
*   **Driver**: NVIDIA Studio Driver **>=591.44** (Verified 2026-01-02)

    .. warning::
       **Laptop Users (RTX 5080 etc.)**: Avoid Game Ready Driver 591.59. It is known to cause conflicts with Intel integrated graphics. Use the **NVIDIA App** to install the **Studio Driver** (591.44+) instead.

*   **Tools**:
    *   Git
    *   Visual Studio 2019 or 2022 (with "Desktop development with C++" workload)

Installation Steps
------------------

1. Configure Environment
~~~~~~~~~~~~~~~~~~~~~~~~

Before cloning, set up the Packman dependency cache to avoid long download times and path issues.

1.  Open PowerShell as Administrator.
2.  Set the ``PM_PACKAGES_ROOT`` environment variable to a local path (e.g., ``C:\packman-repo``):

    .. code-block:: powershell

       setx PM_PACKAGES_ROOT "C:\packman-repo"

3.  Close and reopen PowerShell to apply the change.

2. Clone the Kit App Template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Clone the official template repository to a **local drive** (e.g., ``C:\Projects``). Do not clone into a network share or WSL mount.

.. code-block:: powershell

   cd C:\Projects
   git clone https://github.com/NVIDIA-Omniverse/kit-app-template.git
   cd kit-app-template

3. Configure the Application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run the configuration script to scaffold your application. You will be prompted to accept the EULA on first run.

.. code-block:: powershell

   .\repo.bat template new

Follow the prompts with these values:

1.  **Select what you want to create**: ``Application``
2.  **Select desired template**: ``USD Composer``
3.  **Enter name of application .kit file**: ``whoimpg.biologger.sim``
4.  **Enter application_display_name**: ``WHOI-MPG Biologger Simulator``
5.  **Enter version**: ``0.1.0``
6.  **Enter name of extension** (Setup Extension): ``whoimpg.biologger.subscriber``
7.  **Enter extension_display_name**: ``WHOI-MPG Biologger Subscriber Extension``
8.  **Enter version**: ``0.1.0``
9.  **Do you want to add application layers?**: ``No``

4. Link to Monorepo Source (Critical)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To enable the "Monorepo" workflow where code lives in WSL but runs on Windows, we replace the generated extension code with a symlink to our repository.

1.  **Delete** the generated extension folder:

    .. code-block:: powershell

       Remove-Item -Recurse -Force "source\extensions\whoimpg.biologger.subscriber"

2.  **Create a Symlink** to your WSL repository:

    .. code-block:: cmd

       :: Run in Command Prompt (cmd.exe) as Administrator, NOT PowerShell
       mklink /D "source\extensions\whoimpg.biologger.subscriber" "\\wsl$\Ubuntu-24.04\home\[WSL_USER]\Projects\whoi-mpg\biologger-sim\omniverse\extensions\whoimpg.biologger.subscriber"

    *(Replace `[WSL_USER]` with your actual WSL username)*

5. Build the Application
~~~~~~~~~~~~~~~~~~~~~~~~

Compile the application binaries for your local machine. This ensures you have the latest Kit SDK (v106.0+).

.. code-block:: powershell

   .\repo.bat build

6. Launch the Application
~~~~~~~~~~~~~~~~~~~~~~~~~

Start the application.

.. code-block:: powershell

   .\repo.bat launch

.. note::
   The initial startup may take **5–8 minutes** as shaders compile. Subsequent launches will be much faster.

7. Accessing Files from Windows
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To access your WSL project files (logs, data, etc.) from this Windows application:

1.  In the Omniverse Content Browser, navigate to the **My Computer** tab.
2.  Enter the WSL network path in the address bar:

    .. code-block:: text

       \wsl$\Ubuntu\home\username\projects\biologger-sim

    *(Replace 'Ubuntu' with your specific distribution name if different)*

8. Opening the Sample Scene
~~~~~~~~~~~~~~~~~~~~~~~~~~~

A sample USD scene with a rigged shark is provided in the repository.

**Prerequisite: Download Assets**

The high-fidelity 3D models are not stored in the git repository. You must download them separately.

1.  Download the asset pack from the project's shared drive (see ``omniverse/assets/README.md`` for the link).
2.  Place ``great_white_shark.glb`` into the ``omniverse/assets/`` folder.

**Opening the Scene:**

1.  In the Omniverse application, go to **File > Open**.
2.  Navigate to your WSL repository path (via the **My Computer** tab as described above).
3.  Open ``omniverse/assets/ocean_scene.usda``.

9. Launching with Dynamic Assets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can launch the application with a specific scene and configuration from the command line. This is useful for switching between different animal models (e.g., Shark vs. Swordfish) while using a shared environment.

**Command Line Syntax:**

.. code-block:: powershell

   .\repo.bat launch -- "path\to\scene.usda" --/biologger/animal=[type]

**Examples:**

1.  **Launch with Shark:**

    .. code-block:: powershell

       .\repo.bat launch -- "omniverse/assets/ocean_scene.usda" --/biologger/animal=shark

2.  **Launch with Swordfish:**

    .. code-block:: powershell

       .\repo.bat launch -- "omniverse/assets/ocean_scene.usda" --/biologger/animal=swordfish

**Note:** Ensure you have downloaded the corresponding `.glb` assets (e.g., `swordfish.glb`) into the `omniverse/assets/` folder.
