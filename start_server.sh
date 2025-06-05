#!/bin/bash

# Load environment variables from .env file if it exists
if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
    echo "📝 Loaded environment variables from .env file"
fi

# Use environment variables or set defaults
DEFAULT_PROFILE=${DEFAULT_PROFILE:-"The_Colonel.py"}
SERVER_HOST=${SERVER_HOST:-"localhost"}
SERVER_PORT=${SERVER_PORT:-8264}

echo "🔥 Starting The_Colonel Open WebUI Server..."
echo "🎯 Profile: $DEFAULT_PROFILE"
echo "📡 Chat endpoint: http://$SERVER_HOST:$SERVER_PORT/v1/chat/completions"
echo "🔧 Tools endpoint: http://$SERVER_HOST:$SERVER_PORT/v1/tools/*"
echo "📋 OpenAPI spec: http://$SERVER_HOST:$SERVER_PORT/openapi.json"
echo "Press Ctrl+C to stop"
echo ""

source venv/bin/activate
python -c "
from interpreter.core.openwebui_server import server
from interpreter import interpreter
server(interpreter, host='$SERVER_HOST', port=$SERVER_PORT, profile_name='$DEFAULT_PROFILE')
"