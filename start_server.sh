#!/bin/bash
echo "🔥 Starting The_Colonel Open WebUI Server..."
source venv/bin/activate
python -c "
from interpreter.core.openwebui_server import server
from interpreter import interpreter
print('🚀 Starting The_Colonel Open WebUI Server...')
print('📡 Chat endpoint: http://localhost:8264/v1/chat/completions')
print('🔧 Tools endpoint: http://localhost:8264/v1/tools/*')
print('📋 OpenAPI spec: http://localhost:8264/openapi.json')
print('Press Ctrl+C to stop')
server(interpreter, host='localhost', port=8264)
"