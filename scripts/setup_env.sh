#!/bin/bash
# scripts/setup_env.sh

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Biologger Sim Setup${NC}"
echo "==================="

# 1. Check for existing environments
if [ -d ".venv" ]; then
    echo -e "${GREEN}Found existing virtual environment (.venv).${NC}"
    if [ ! -t 0 ]; then
        echo "Non-interactive shell detected. Updating..."
        make _setup_venv
        exit $?
    fi

    read -p "Update it? [Y/n] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Nn]$ ]]; then
        echo "Skipping update."
        exit 0
    else
        make _setup_venv
        exit $?
    fi
fi

# TODO: Check for existing conda/mamba env (biologger-sim)
# This is harder to do reliably across conda/mamba without being slow,
# so we'll rely on the user choosing the tool if they want to update it.

# 2. Detect available tools
OPTIONS=()
has_command() {
    command -v "$1" >/dev/null 2>&1
}

if has_command python3; then
    OPTIONS+=("venv (Standard Python)")
fi

if has_command micromamba; then
    OPTIONS+=("micromamba")
fi

if has_command mamba; then
    OPTIONS+=("mamba")
fi

if has_command conda; then
    OPTIONS+=("conda")
fi

if [ ${#OPTIONS[@]} -eq 0 ]; then
    echo "Error: No suitable tools found (python3, micromamba, or conda)."
    exit 1
fi

# 3. Interactive Menu
echo "Found the following setup options:"
i=1
for opt in "${OPTIONS[@]}"; do
    echo "$i) $opt"
    ((i++))
done

# If non-interactive (e.g. CI), default to first option
if [ ! -t 0 ]; then
    echo "Non-interactive shell detected. Defaulting to ${OPTIONS[0]}."
    CHOICE=1
else
    read -p "Choose installation method [1-${#OPTIONS[@]}]: " CHOICE
fi


# 4. Execute Choice
SELECTED_OPT="${OPTIONS[$((CHOICE-1))]}"

case "$SELECTED_OPT" in
    "venv (Standard Python)")
        make _setup_venv
        ;;
    "micromamba")
        make _setup_mamba
        ;;
    "mamba")
        make _setup_mamba MAMBA=mamba
        ;;
    "conda")
        make _setup_mamba MAMBA=conda
        ;;
    *)
        echo "Invalid choice."
        exit 1
        ;;
esac
