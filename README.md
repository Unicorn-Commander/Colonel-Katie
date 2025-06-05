# 🔥 The_Colonel

**An enhanced Open Interpreter fork with robust Open WebUI integration and advanced computer control capabilities**

<p align="center">
    <a href="LICENSE"><img src="https://img.shields.io/static/v1?label=license&message=AGPL&color=white&style=flat" alt="License"/></a>
    <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python Version"/>
    <img src="https://img.shields.io/badge/Open%20WebUI-Compatible-green.svg" alt="Open WebUI Compatible"/>
    <img src="https://img.shields.io/badge/Streaming-Responses-orange.svg" alt="Streaming Support"/>
    <img src="https://img.shields.io/badge/Computer-Control-red.svg" alt="Computer Control"/>
</p>

The_Colonel is a powerful, battle-tested fork of Open Interpreter designed for serious automation and AI-powered computer control. With comprehensive Open WebUI integration, advanced streaming capabilities, and robust error handling, it bridges the gap between conversational AI and practical system automation.

## ✨ Key Features

- **🌐 Seamless Open WebUI Integration**: Production-ready API server with OpenAI-compatible streaming endpoints
- **🛠️ Comprehensive Tool Arsenal**: 12+ specialized endpoints for code execution, file operations, and computer control
- **🖥️ Advanced Computer Control**: Direct mouse/keyboard interaction, screenshots, and window management
- **📁 Intelligent File Management**: Advanced file operations with upload/download capabilities
- **👤 Dynamic Profile System**: Hot-swappable configurations for different AI models and use cases
- **🔐 Enterprise-Ready Security**: Bearer token authentication with localhost development mode
- **⚡ Optimized Streaming**: Robust chunk processing with real-time response streaming
- **🔧 Error-Resilient Architecture**: Advanced error handling and recovery mechanisms
- **📋 OpenAPI 3.1 Specification**: Full API documentation with tagged tool categorization

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/YourUsername/The_Colonel.git
cd The_Colonel

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
```

### Basic Usage

**Traditional Terminal Interface:**
```bash
interpreter
```

**Open WebUI Server Mode:**
```bash
interpreter --openwebui_server --host localhost --port 8264
```

**With Custom Profile:**
```bash
interpreter --openwebui_server --profile The_Colonel.py
```

**Remote Access with Authentication:**
```bash
interpreter --openwebui_server --host 0.0.0.0 --port 8264 --auth_token your_secure_token
```

**Quick Start Scripts:**
```bash
# Local development (no authentication)
./start_server.sh

# Remote access with authentication
./start_server_auth.sh
```

## 🔧 Open WebUI Integration

### Server Endpoints

**Chat Endpoint:**
- `POST /v1/chat/completions` - OpenAI-compatible chat with profile selection

**Code Execution Tools:**
- `POST /v1/tools/execute/python` - Execute Python code
- `POST /v1/tools/execute/shell` - Execute shell commands

**File Management Tools:**
- `POST /v1/tools/files/read` - Read file contents
- `POST /v1/tools/files/write` - Write file contents  
- `POST /v1/tools/files/upload` - Upload files

**Computer Control Tools:**
- `POST /v1/tools/computer/screenshot` - Take screenshots
- `POST /v1/tools/computer/click` - Click at coordinates
- `POST /v1/tools/computer/type` - Type text
- `POST /v1/tools/computer/key` - Press keys

**API Documentation:**
- `GET /openapi.json` - Complete OpenAPI specification

### Open WebUI Configuration

**LLM Connection:**
- Base URL: `http://localhost:8264/v1`
- Model: `the-colonel` (or any name)

**Tool Server:**
- Base URL: `http://localhost:8264`
- OpenAPI JSON: Use the served specification at `/openapi.json`

### Profile Selection

Use the `profile` query parameter to select different configurations:
```bash
curl -X POST "http://localhost:8264/v1/chat/completions?profile=The_Colonel" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Hello"}]}'
```

## 🎯 Use Cases

**For Developers:**
- Code execution and debugging through web interface
- File management and project manipulation
- Automated testing and deployment scripts

**For Power Users:**
- Computer automation via API calls
- Screen capture and GUI automation
- Advanced file processing workflows

**For Integration:**
- Embed in existing web applications
- Build custom frontends with the API
- Create automated workflows and pipelines

## 🛡️ Security & Safety

**Local Development:**
- No authentication required for `localhost` access
- Safe for development and testing

**Remote Access:**
- Bearer token authentication required
- Use strong tokens for production deployments

**Code Execution:**
- All code execution happens in your local environment
- Review and approve code before execution in interactive mode
- Use `auto_run` carefully in production environments

## 📚 Advanced Usage

### Python API

```python
from interpreter import interpreter

# Basic chat
interpreter.chat("Analyze this dataset and create visualizations")

# Streaming responses
for chunk in interpreter.chat("Process these files", stream=True):
    print(chunk)

# Custom configuration
interpreter.llm.model = "gpt-4"
interpreter.auto_run = True
interpreter.os = True  # Enable OS control features
```

### Profile System

Create custom profiles in `interpreter/terminal_interface/profiles/defaults/`:

```python
# my_profile.py
from interpreter import interpreter

interpreter.llm.model = "gpt-4"
interpreter.llm.temperature = 0.1
interpreter.auto_run = True
interpreter.os = True
interpreter.computer.import_computer_api = True
```

Use with:
```bash
interpreter --profile my_profile.py
```

## ⚡ Streaming & Performance

### Robust Chunk Processing

The_Colonel features advanced streaming response handling that properly processes various chunk formats from the interpreter:

- **Error-Resilient**: Individual chunk processing errors don't crash the entire conversation
- **Format-Agnostic**: Handles dictionary chunks, string chunks, and malformed data gracefully  
- **Type-Safe**: Uses `.get()` methods instead of direct key access to prevent KeyErrors
- **Debug-Friendly**: Comprehensive logging for troubleshooting chunk processing issues

### Technical Architecture

**Streaming Response Flow:**
1. OpenAI-compatible request received
2. Profile configuration loaded dynamically
3. Messages converted to interpreter format
4. Interpreter streams chunks in real-time
5. Chunks processed through robust error handling
6. Server-Sent Events formatted for Open WebUI
7. Real-time display in web interface

## 🛠️ Troubleshooting

### Common Issues

**1. API Key Authentication Errors**
```bash
# Check your API key is set correctly
echo $OPENAI_API_KEY

# Update .env file if needed
nano .env
```

**2. Streaming Response Issues** 
- "Error: 'type'" on second messages → Fixed with improved message state management
- Messages appear in terminal but not GUI → Resolved with proper SSE formatting
- KeyError 'type' exceptions → Handled with robust chunk processing

**3. Profile Loading Problems**
```bash
# Clear Python cache if profiles aren't reloading
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +
```

**4. Port Already in Use**
```bash
# Find and kill process using port 8264
lsof -ti:8264 | xargs kill -9
```

### Debug Mode

Enable detailed logging:
```bash
interpreter --openwebui_server --verbose
```

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure your settings:

```bash
cp .env.example .env
# Edit with your actual API keys and settings
```

```env
# API Keys
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
XAI_API_KEY=your_xai_key_here
DEEPSEEK_API_KEY=your_deepseek_key_here

# Server Configuration  
DEFAULT_PROFILE=The_Colonel.py
SERVER_HOST=0.0.0.0
SERVER_PORT=8264
AUTH_TOKEN=your_secure_random_token

# General Settings
DISABLE_TELEMETRY=true
AUTO_RUN=false
SAFE_MODE=off
```

### Profile Customization

Advanced profile example with environment-based API key:

```python
# custom_profile.py
import os
from interpreter import interpreter

# Model Configuration
interpreter.llm.model = "gpt-4o-mini"
interpreter.llm.api_key = os.getenv("OPENAI_API_KEY")
interpreter.llm.temperature = 0.1
interpreter.llm.context_window = 128000
interpreter.llm.max_tokens = 16384

# Capabilities
interpreter.auto_run = True
interpreter.os = True
interpreter.computer.import_computer_api = True

# Custom instructions for better computer control
interpreter.custom_instructions = """
When taking screenshots, if you encounter errors with pywinctl, 
try using computer.display.screenshot(active_app_only=False) instead.
"""
```

## 🔨 Development

### Project Structure

```
The_Colonel/
├── interpreter/
│   ├── core/
│   │   ├── openwebui_server.py    # Open WebUI integration
│   │   └── ...
│   ├── computer_use/
│   │   └── tools/                 # Computer control tools
│   └── terminal_interface/
│       └── profiles/              # Configuration profiles
├── openapi.json                   # API specification
├── documentation/                 # Project documentation
└── examples/                      # Usage examples
```

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Submit a pull request with detailed description

### Testing

```bash
# Test server functionality
source venv/bin/activate
python -c "from interpreter.core.openwebui_server import create_openwebui_server; print('✅ Server tests passed')"

# Start test server
interpreter --openwebui_server --host localhost --port 8264

# Test endpoints
curl http://localhost:8264/openapi.json
```

## 📖 Documentation

- **[Setup Guide](documentation/Task_Checklist-The_Colonel.md)** - Complete installation and configuration
- **[Project Plan](documentation/Project_Plan-The_Colonel.md)** - Technical implementation details
- **[OpenAPI Spec](openapi.json)** - Complete API documentation

## 🏗️ Based on Open Interpreter

The_Colonel builds upon the excellent foundation of [Open Interpreter](https://github.com/OpenInterpreter/open-interpreter), adding:

- Open WebUI compatibility
- Enhanced tool endpoints
- Computer control capabilities
- Improved profile system
- Production-ready API server

## 📜 License

This project is licensed under the AGPL License - see the [LICENSE](LICENSE) file for details.

## 🤝 Acknowledgments

- **Open Interpreter Team** - For the incredible foundation
- **Open WebUI Community** - For the inspiration and integration target
- **Contributors** - For making this project better

---

**⚠️ Note**: The_Colonel executes code in your local environment. Always review and understand code before execution, especially when using `auto_run` mode or in production environments.