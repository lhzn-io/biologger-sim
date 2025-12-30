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
