#!/bin/bash

# Load environment variables from .env file if it exists
if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
    echo "📝 Loaded environment variables from .env file"
fi

# Use environment variables or set defaults
DEFAULT_PROFILE=${DEFAULT_PROFILE:-"The_Colonel.py"}
SERVER_HOST=${SERVER_HOST:-"0.0.0.0"}
SERVER_PORT=${SERVER_PORT:-8264}

# Set your auth token here (replace with your actual token) or use environment variable
AUTH_TOKEN=${AUTH_TOKEN:-"kJ8mN2pQ4rT6uY9wE3zA5xC7vB1nM8qP2sD4fG6hJ0k"}

# Detect the local IP address
if command -v hostname &> /dev/null; then
    LOCAL_IP=$(hostname -I | awk '{print $1}' 2>/dev/null || echo "localhost")
else
    LOCAL_IP="localhost"
fi

echo "🔥 Starting The_Colonel Open WebUI Server with Authentication..."
echo "🎯 Profile: $DEFAULT_PROFILE"
echo "🔐 Auth Token: $AUTH_TOKEN"
echo "🌐 Server will be accessible from any IP address"
echo "📡 Configure Open WebUI with:"
echo "   LLM Base URL: http://$LOCAL_IP:$SERVER_PORT/v1"
echo "   Tool Server: http://$LOCAL_IP:$SERVER_PORT"
echo "   API Key: $AUTH_TOKEN"
echo ""

source venv/bin/activate
python -c "
from interpreter.core.openwebui_server import server
from interpreter import interpreter
server(interpreter, host='$SERVER_HOST', port=$SERVER_PORT, auth_token='$AUTH_TOKEN', profile_name='$DEFAULT_PROFILE')
"