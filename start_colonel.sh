#!/bin/bash

# Navigate to The_Colonel directory
cd "$(dirname "$0")"

# Check if uvicorn is already running for this project
if pgrep -f "uvicorn interpreter.core.openwebui_server:app" > /dev/null
then
    echo "The_Colonel server is already running."
else
    echo "Starting The_Colonel server..."
    # Activate poetry environment and run the server in the background
    # Redirect stdout/stderr to a log file
    poetry run uvicorn interpreter.core.openwebui_server:app --host 0.0.0.0 --port 8264 > colonel_server.log 2>&1 &
    echo "The_Colonel server started in the background. Check colonel_server.log for output."
fi
