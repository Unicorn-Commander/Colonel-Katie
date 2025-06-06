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
echo ""
echo "📡 Configure Open WebUI LLM with:"
echo "   LLM Base URL: http://$SERVER_HOST:$SERVER_PORT/v1"
echo ""
echo "🔧 Add Individual Tools in Open WebUI (Admin Panel → Settings → Tools):"
echo "   🐍 Python Executor: http://$SERVER_HOST:$SERVER_PORT/python/openapi.json"
echo "   💻 Shell Executor: http://$SERVER_HOST:$SERVER_PORT/shell/openapi.json"
echo "   📁 File Operations: http://$SERVER_HOST:$SERVER_PORT/files/openapi.json"
echo "   🖥️  Computer Control: http://$SERVER_HOST:$SERVER_PORT/computer/openapi.json"
echo "   🌐 Browser Automation: http://$SERVER_HOST:$SERVER_PORT/browser/openapi.json"
echo "   📋 Clipboard Operations: http://$SERVER_HOST:$SERVER_PORT/clipboard/openapi.json"
echo "   🚀 JavaScript Execution: http://$SERVER_HOST:$SERVER_PORT/javascript/openapi.json"
echo "   📊 R Programming: http://$SERVER_HOST:$SERVER_PORT/r/openapi.json"
echo "   🍎 AppleScript (macOS): http://$SERVER_HOST:$SERVER_PORT/applescript/openapi.json"
echo "   📱 SMS/Messages (macOS): http://$SERVER_HOST:$SERVER_PORT/sms/openapi.json"
echo "   👁️  Computer Vision & OCR: http://$SERVER_HOST:$SERVER_PORT/vision/openapi.json"
echo ""
echo "Press Ctrl+C to stop"
echo ""

source venv/bin/activate
python -c "
from interpreter.core.openwebui_server import server
from interpreter import interpreter
server(interpreter, host='$SERVER_HOST', port=$SERVER_PORT, profile_name='$DEFAULT_PROFILE')
"