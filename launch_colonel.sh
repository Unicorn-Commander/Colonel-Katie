#!/bin/bash

# The Colonel GUI Launcher Script
# This script launches The Colonel with proper environment setup

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the project directory
cd "$SCRIPT_DIR"

# Check if we're in a virtual environment, if not, try to activate one
if [[ -z "$VIRTUAL_ENV" ]]; then
    # Try to find and activate a virtual environment
    if [[ -f ".venv/bin/activate" ]]; then
        source .venv/bin/activate
    elif [[ -f "venv/bin/activate" ]]; then
        source venv/bin/activate
    elif command -v poetry &> /dev/null; then
        # Use poetry if available
        exec poetry run python -m gui.desktop.main "$@"
    fi
fi

# Launch The Colonel GUI
exec python -m gui.desktop.main "$@"