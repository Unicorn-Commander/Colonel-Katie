#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$SCRIPT_DIR/venv/bin/activate"
echo "Testing Colonel Katie installation..."
interpreter --version
python -c "import interpreter; print('✅ Import successful')"
