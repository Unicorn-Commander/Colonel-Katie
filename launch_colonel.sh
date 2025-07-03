#!/bin/bash

# Colonel Katie GUI Launcher Script
# This script launches Colonel Katie with proper environment setup

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the project directory
cd "$SCRIPT_DIR"

echo "🦄⚡ Launching Colonel Katie..."

# Check if we're in a virtual environment, if not, try to activate one
if [[ -z "$VIRTUAL_ENV" ]]; then
    # Try to find and activate a virtual environment
    if [[ -f ".venv/bin/activate" ]]; then
        echo "Activating .venv virtual environment..."
        source .venv/bin/activate
    elif [[ -f "venv/bin/activate" ]]; then
        echo "Activating venv virtual environment..."
        source venv/bin/activate
    elif command -v poetry &> /dev/null; then
        # Use poetry if available
        echo "Using poetry to run..."
        exec poetry run python main.py "$@"
    fi
fi

# Launch Colonel Katie GUI
echo "Starting application..."
exec python main.py "$@"