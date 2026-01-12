# Biologger Simulation Environment (biologger-sim)

Real-time simulation environment for marine animal tracking and behavioral prediction.

## Overview

This project provides a simulation framework for developing and validating biologger algorithms. It supports a "Dual-Mode" architecture:

1. **Lab Mode**: High-precision, acausal processing for post-hoc analysis.
2. **Simulation Mode**: Real-time, causal processing for on-tag algorithm development.

It integrates with **NVIDIA Omniverse** via ZeroMQ for high-fidelity visualization.

## Installation

```bash
# Create environment (if not exists)
micromamba env create -f environment.yml
micromamba activate biologger-sim

# Install package
pip install -e .
```

## Usage

### Streaming Data

To stream a CSV file to the visualization client:

```bash
python -m biologger_sim --config config/Swordfish-RED001_20220812_19A0564-postfacto.yaml
```

## Architecture

- **Core**: Type definitions and configuration.
- **IO**: Data streaming (CSV) and ZeroMQ publishing.
- **Processing**: (Coming soon) Filters and sensor fusion algorithms.

## Documentation

See `docs/` for detailed architectural plans and research notes.

## License

Apache License 2.0

## Attribution

This simulation environment is built on biologger processing algorithms originally developed in R by Camrin Braun at the Woods Hole Oceanographic Institution Marine Predators Group, and ported to Python by Daniel Fry.

## Troubleshooting

### UJITSO / DomeLight Build Errors

If you encounter errors similar to:

```text
[Error] [gpu.foundation.plugin] Failed to request UJITSO build result for: ./textures/color_0C0C0C.exr:5
[Error] [rtx.scenedb.plugin] Failed to upload DomeLight texture ./textures/color_0C0C0C.exr
```

This indicates a stale build state. Please rebuild the project:

**Windows:**

```bash
.\repo.bat build -c
.\repo.bat build
```

**Linux:**

```bash
./repo.sh build -c
./repo.sh build
```
