# 🔥 The_Colonel

**An enhanced Open Interpreter fork with Open WebUI integration**

<p align="center">
    <a href="LICENSE"><img src="https://img.shields.io/static/v1?label=license&message=AGPL&color=white&style=flat" alt="License"/></a>
    <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python Version"/>
    <img src="https://img.shields.io/badge/Open%20WebUI-Compatible-green.svg" alt="Open WebUI Compatible"/>
</p>

The_Colonel is a powerful fork of Open Interpreter that brings enhanced capabilities and seamless Open WebUI integration. Built for power users who want both command-line flexibility and modern web interfaces.

## ✨ Key Features

- **🌐 Open WebUI Integration**: Full API server with OpenAI-compatible endpoints
- **🛠️ Comprehensive Tool Suite**: 9+ endpoints covering code execution, file ops, and computer control
- **👤 Profile System**: Easy configuration switching with profile support
- **🔐 Flexible Authentication**: Local development without auth, remote access with tokens
- **🖥️ Computer Control**: Direct mouse, keyboard, and screen interaction capabilities
- **📁 Advanced File Operations**: Read, write, upload, and manage files seamlessly

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
interpreter --openwebui_server --profile gpt-4.1-mini.py
```

**Remote Access with Authentication:**
```bash
interpreter --openwebui_server --host 0.0.0.0 --port 8264 --auth_token your_secure_token
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
curl -X POST "http://localhost:8264/v1/chat/completions?profile=fast" \
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