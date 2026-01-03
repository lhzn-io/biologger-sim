=========================
Ubuntu Setup (Headless)
=========================

This guide covers setting up NVIDIA Omniverse in a Docker container on Ubuntu. This is useful for headless simulation, CI/CD, or running on a Linux server (e.g., NVIDIA Thor).

Prerequisites
-------------

*   **OS**: Ubuntu 20.04 or 22.04
*   **GPU**: NVIDIA RTX GPU
*   **Driver**: Latest NVIDIA Linux Driver

Step 1: NVIDIA Developer Account & NGC
--------------------------------------

To access Omniverse container images, you need an NVIDIA NGC account.

1.  **Register**: Go to `ngc.nvidia.com <https://ngc.nvidia.com/>`_ and create an account.
2.  **API Key**:
    *   Log in to NGC.
    *   Click your user profile (top right) > **Setup**.
    *   Click **Get API Key**.
    *   Click **Generate API Key**.
    *   **SAVE THIS KEY**. You cannot see it again.

Step 2: Install Docker & NVIDIA Container Toolkit
-------------------------------------------------

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

Step 3: Log in to NGC Registry
------------------------------

Authenticate Docker with your NGC API key.

.. code-block:: bash

    # Username is ALWAYS '$oauthtoken'
    # Password is your generated API Key
    docker login nvcr.io

Step 4: Pull & Run Omniverse Kit
--------------------------------

You can now pull Omniverse Kit or Isaac Sim images.

.. code-block:: bash

    # Example: Pull Isaac Sim (includes Kit)
    docker pull nvcr.io/nvidia/isaac-sim:2023.1.1

    # Run with GPU support
    docker run --name isaac-sim --entrypoint bash -it --gpus all -e "ACCEPT_EULA=Y" --rm --network=host \
        nvcr.io/nvidia/isaac-sim:2023.1.1
