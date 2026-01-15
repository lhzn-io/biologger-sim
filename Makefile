# Makefile for biologger-sim
# Uses micromamba for environment management

ENV_NAME := biologger-sim
VENV_DIR := .venv
PYTHON := python
MAMBA := micromamba

.PHONY: help setup clean run test lint format docs

help:
	@echo "Biologger Sim - Development Commands"
	@echo "===================================="
	@echo "make setup   : Interactive setup (auto-detects tools)"
	@echo "make run     : Run the simulation (requires activated env)"
	@echo "make clean   : Remove the environment"
	@echo "make test    : Run tests"
	@echo "make lint    : Run linters (ruff, mypy)"
	@echo "make format  : Format code (ruff)"

setup:
	@./scripts/setup_env.sh

_setup_venv:
	@echo "Creating/Updating virtual environment in $(VENV_DIR)..."
	python3 -m venv $(VENV_DIR)
	@echo "Installing dependencies..."
	./$(VENV_DIR)/bin/pip install -e ".[dev]"
	./$(VENV_DIR)/bin/pre-commit install
	@echo "Done! Activate with: source $(VENV_DIR)/bin/activate"

_setup_mamba:
	@echo "Creating/Updating environment $(ENV_NAME)..."
	$(MAMBA) env create -f environment.yml -y || $(MAMBA) env update -f environment.yml
	# We need to run pip install inside the mamba env
	$(MAMBA) run -n $(ENV_NAME) pip install -e ".[dev]"
	$(MAMBA) run -n $(ENV_NAME) pre-commit install

clean:
	@echo "Removing environment $(ENV_NAME)..."
	$(MAMBA) env remove -n $(ENV_NAME) -y || true
	rm -rf $(VENV_DIR)

# Example run command (adjust path to data as needed)
run:
	$(PYTHON) -m biologger_sim --config config/Swordfish-RED001_20220812_19A0564-postfacto.yaml

test:
	pytest tests/

lint:
	ruff check .
	mypy src/ tests/

format:
	ruff check --fix .
	ruff format .

docs:
	cd docs && sphinx-build -b html source build/html
