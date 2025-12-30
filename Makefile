# Makefile for biologger-sim
# Uses micromamba for environment management

ENV_NAME := biologger-sim
PYTHON := python
MAMBA := micromamba

.PHONY: help setup clean run test

help:
	@echo "Biologger Sim - Development Commands"
	@echo "===================================="
	@echo "make setup   : Create/Update the micromamba environment"
	@echo "make run     : Run the simulation (requires activated env)"
	@echo "make clean   : Remove the environment"
	@echo "make test    : Run tests"
	@echo "make lint    : Run linters (ruff, mypy)"
	@echo "make format  : Format code (ruff)"

setup:
	@if ! command -v $(MAMBA) > /dev/null; then \
		echo "Error: $(MAMBA) not found."; \
		echo "Please install micromamba: https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html"; \
		exit 1; \
	fi
	@echo "Creating/Updating environment $(ENV_NAME)..."
	$(MAMBA) env create -f environment.yml -y || $(MAMBA) env update -f environment.yml
	$(MAMBA) run -n $(ENV_NAME) pre-commit install

clean:
	@echo "Removing environment $(ENV_NAME)..."
	$(MAMBA) env remove -n $(ENV_NAME) -y

# Example run command (adjust path to data as needed)
run:
	$(PYTHON) -m biologger_sim --config config/Swordfish-RED001_20220812_19A0564-postfacto.yaml

test:
	pytest tests/

lint:
	ruff check .
	mypy src/

format:
	ruff check --fix .
	ruff format .
