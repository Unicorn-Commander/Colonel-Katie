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

- **🧠 Adaptive Memory System**: Persistent, LLM-driven memory for personalized and contextual interactions.
- **🎨 Cutting-Edge Modern GUI**: Next-generation interface with glass morphism effects, advanced typography, and micro-interactions
- **🖥️ Complete Desktop Integration**: Native KDE application launcher, KRunner search, system tray, and command-line access
- **🗃️ Custom File Indexing**: Intelligent indexing and embedding of local files for project-aware AI assistance.
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
git clone https://github.com/Unicorn-Commander/The_Colonel.git
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

**🎨 Modern Desktop GUI:**
```bash
# Launch cutting-edge modern GUI
python -m gui.desktop.main

# Or install as native KDE application
./install_desktop.sh

# Then launch from:
# - KDE Application Launcher (search "The Colonel")
# - KRunner (Alt+Space, type "colonel") 
# - Terminal (type "colonel")
```

**Open WebUI Server Mode:**
```bash
python -m interpreter.api.main
```

**With Custom Configuration:**
```bash
# Set environment variables in .env file
OPENAI_API_KEY=your_key_here
DEFAULT_PROFILE=The_Colonel.py
SERVER_PORT=8000

python -m interpreter.api.main
```

**Direct uvicorn Usage:**
```bash
uvicorn interpreter.api.main:app --host 0.0.0.0 --port 8000
```

**Quick Start Scripts:**
```bash
# Local development (no authentication)
./start_server.sh

# Remote access with authentication
./start_server_auth.sh
```

## 🎨 Modern Desktop GUI

The Colonel features a **cutting-edge, next-generation GUI** that surpasses the visual quality of Open WebUI and other AI interfaces.

### ✨ Design Features

- **🔮 Glass Morphism Effects**: Translucent sidebars with backdrop blur filters
- **📝 Modern Typography**: "Inter" and "SF Pro Display" fonts with optimized spacing  
- **🌈 Advanced Gradients**: Multi-stop gradients throughout the interface
- **💫 Micro-Interactions**: Smooth hover animations and shadow effects
- **🎯 Professional UX**: 16px border radius, enhanced spacing, premium aesthetics

### 🖥️ Desktop Integration

- **📱 KDE Application Launcher**: Search "The Colonel" in your application menu
- **🔍 KRunner Integration**: Press `Alt+Space` and type "colonel" 
- **🔔 System Tray**: Show/hide and quit functionality
- **⌨️ Terminal Access**: Use `colonel` command anywhere
- **⚙️ One-Click Install**: Automated desktop integration

### 🚀 Installation & Usage

```bash
# Install as native KDE application
./install_desktop.sh

# Launch Methods:
# 1. From Application Launcher: Search "The Colonel"
# 2. From KRunner: Alt+Space → type "colonel"
# 3. From Terminal: type "colonel"  
# 4. Direct: python -m gui.desktop.main
```

For complete installation guide, see [DESKTOP_INTEGRATION.md](DESKTOP_INTEGRATION.md).

## 🔧 Open WebUI Integration

### Individual Tool Servers

The_Colonel provides **4 specialized tool servers** that can be added individually to Open WebUI:

**🐍 Python Code Executor:**
- Server: `http://your-ip:8000/python`
- OpenAPI: `http://your-ip:8000/python/openapi.json`
- Execute Python code, data analysis, calculations

**🔧 Shell Command Executor:**
- Server: `http://your-ip:8000/shell` 
- OpenAPI: `http://your-ip:8000/shell/openapi.json`
- Run bash/shell commands, system operations

**📁 File Operations:**
- Server: `http://your-ip:8000/files`
- OpenAPI: `http://your-ip:8000/files/openapi.json`
- Read, write, and manage files

**🖥️ Computer Control:**
- Server: `http://your-ip:8000/computer`
- OpenAPI: `http://your-ip:8000/computer/openapi.json`
- Screenshots, mouse clicks, keyboard input

### Legacy Endpoints
- `GET /openapi.json` - Complete API specification
- `POST /v1/chat/completions` - OpenAI-compatible chat endpoint

### Open WebUI Configuration

**LLM Connection:**
- Base URL: `http://localhost:8000/v1`
- Model: `the-colonel`

**Individual Tool Setup:**
Add each tool separately to Open WebUI with:
- Tool Server URL: `http://your-ip:8000/{tool-name}`
- API Key: `your-auth-token` (not required for localhost)
- OpenAPI JSON: `http://your-ip:8000/{tool-name}/openapi.json`

**📖 Complete Tool Documentation:** See [Tool Reference Guide](documentation/Tool_Reference.md) for detailed setup instructions, examples, and usage patterns.

### Profile Selection

Use the `profile` query parameter for chat completions:
```bash
curl -X POST "http://localhost:8000/v1/chat/completions?profile=The_Colonel" \
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
# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9
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
SERVER_PORT=8000
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
python -c "from interpreter.api.server import create_colonel_katie_server; print('✅ Server tests passed')"

# Start test server
python -m interpreter.api.main

# Test endpoints
curl http://localhost:8000/openapi.json
```

## 📖 Documentation

- **[Tool Reference Guide](documentation/Tool_Reference.md)** - Complete tool documentation with examples
- **[Technical Implementation Guide](documentation/Technical_Implementation_Guide.md)** - Architecture and technical details
- **[Project Summary](documentation/Project_Summary.md)** - Project overview and current status
- **[Setup Guide](documentation/Task_Checklist-The_Colonel.md)** - Installation and configuration
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
