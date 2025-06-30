#!/bin/bash

# Find the process ID of uvicorn running openwebui_server.py
PID=$(pgrep -f "uvicorn interpreter.core.openwebui_server:app")

if [ -z "$PID" ]
then
    echo "The_Colonel server is not running."
else
    echo "Stopping The_Colonel server (PID: $PID)..."
    kill $PID
    echo "The_Colonel server stopped."
fi
