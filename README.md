# 🦄⚡ Colonel Katie - Enhanced Open Interpreter ⚡🦄

**AI Agent Development Platform with KDE Integration & Python 3.13 Support**

![Version](https://img.shields.io/badge/version-2.1-blue.svg)
![Python](https://img.shields.io/badge/python-3.9--3.13-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-Production%20Ready-brightgreen.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20|%20Headless-orange.svg)

---

## 🌟 Overview

Colonel Katie is an enhanced fork of [Open Interpreter](https://github.com/OpenInterpreter/open-interpreter) that adds:
- **Python 3.13 Compatibility** - Works with the latest Python versions
- **KDE Plasma Integration** - Deep desktop automation for KDE users
- **Flexible Deployment** - Run headless on servers OR with full GUI
- **Enhanced Features** - Visual agent builder, RAG, voice interaction, and more

### 🎯 Key Differentiators

| Feature | Open Interpreter | Colonel Katie |
|---------|-----------------|---------------|
| Python Support | 3.9-3.12 | **3.9-3.13** ✨ |
| KDE Integration | ❌ | **✅ Full Control** |
| Headless Mode | Basic | **Optimized** |
| GUI Interface | Terminal Only | **Full PySide6 GUI** |
| Agent Builder | ❌ | **✅ Visual Builder** |
| Memory System | Basic | **Advanced (mem0ai)** |

---

## 🚀 Quick Start

### 🖥️ Headless Installation (Servers/CLI Only)

Perfect for servers, containers, and systems without GUI:

```bash
# Clone the repository
git clone https://github.com/Unicorn-Commander/Colonel-Katie.git
cd Colonel-Katie

# Run headless installer
./install-headless.sh
```

### 🎨 Full GUI Installation (Desktop)

For the complete experience with visual interface and KDE integration:

```bash
# Clone the repository
git clone https://github.com/Unicorn-Commander/Colonel-Katie.git
cd Colonel-Katie

# Run full installer
python install.py
```

### 📦 Quick Test

```bash
# For headless
./interpreter.sh --help

# For GUI
python main.py
```

---

## 📋 System Requirements

### Headless Mode
- **Python**: 3.9-3.13 (3.11+ recommended)
- **RAM**: 2GB minimum (4GB recommended)
- **OS**: Any Linux distribution
- **Dependencies**: Minimal (no GUI libraries)

### Full GUI Mode
- **Python**: 3.9-3.13 (3.11+ recommended)
- **RAM**: 4GB minimum (8GB recommended)
- **OS**: Linux with X11/Wayland
- **Desktop**: KDE Plasma (recommended) or any desktop
- **GPU**: Optional (for local models)

---

## 🎯 Features

### Core Capabilities (All Modes)
- ✅ **AI-Powered Code Execution** - Run code in multiple languages
- ✅ **Multi-Model Support** - OpenAI, Anthropic, Google, Ollama, and more
- ✅ **File Operations** - Read, write, and manipulate files
- ✅ **Web Browsing** - Automated web interactions
- ✅ **Python 3.13 Support** - Latest Python compatibility

### Headless Features
- 🖥️ **Server-Optimized** - Minimal resource usage
- 🔧 **CLI Interface** - Full terminal control
- 🐳 **Container-Ready** - Docker/Kubernetes compatible
- 📡 **API Server Mode** - RESTful API for integrations
- 🤖 **Automation Scripts** - Batch processing support

### GUI Exclusive Features
- 🎨 **Visual Agent Builder** - Create agents without code
- 📚 **Prompt Library** - Professional templates
- 🧠 **RAG Integration** - Document knowledge bases
- 🎙️ **Voice Interaction** - Speech recognition & TTS
- 💾 **Advanced Memory** - Persistent conversation history
- 📊 **Real-time Monitoring** - System and model metrics

### KDE Plasma Integration (GUI Mode)
- 🪟 **Window Management** - Control windows programmatically
- 🖥️ **Virtual Desktop Control** - Switch and manage desktops
- 📋 **Clipboard Operations** - Advanced clipboard automation
- 📁 **File Manager Integration** - Dolphin automation
- 🔔 **System Notifications** - Native KDE notifications
- ⚡ **Plasma Shell Control** - Widget and panel management

---

## 🛠️ Installation Guide

### Method 1: Headless Installation (Recommended for Servers)

```bash
# 1. Clone repository
git clone https://github.com/Unicorn-Commander/Colonel-Katie.git
cd Colonel-Katie

# 2. Run headless installer
chmod +x install-headless.sh
./install-headless.sh

# 3. Activate and use
source venv/bin/activate
interpreter
```

### Method 2: Full Installation (Desktop with GUI)

```bash
# 1. Clone repository
git clone https://github.com/Unicorn-Commander/Colonel-Katie.git
cd Colonel-Katie

# 2. Install with GUI support
python install.py

# 3. Launch GUI
python main.py

# Or use terminal mode
interpreter
```

### Method 3: Development Installation

```bash
# 1. Clone repository
git clone https://github.com/Unicorn-Commander/Colonel-Katie.git
cd Colonel-Katie

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install in editable mode
pip install -e .

# 4. Install development dependencies
pip install -r requirements-dev.txt
```

---

## 💻 Usage Examples

### Basic CLI Usage

```bash
# Start interactive session
interpreter

# Run with specific model
interpreter --model gpt-4

# Execute a task directly
interpreter "Create a Python script that downloads YouTube videos"

# Use local model
interpreter --local
```

### KDE Automation Examples

```python
# In interpreter session
>>> # List all windows
>>> computer.kde.windows.list_windows()

>>> # Switch virtual desktop
>>> computer.kde.virtual_desktops.switch_to(2)

>>> # Send notification
>>> computer.kde.notifications.notify("Task Complete", "Your script has finished running")

>>> # Clipboard operations
>>> computer.kde.clipboard.set_text("Hello from Colonel Katie!")
>>> print(computer.kde.clipboard.get_text())
```

### Headless Server Usage

```bash
# Start as API server
interpreter --server --port 8080

# Run batch script
interpreter < commands.txt

# Use in scripts
echo "analyze /var/log/syslog for errors" | interpreter
```

---

## 🔧 Configuration

### Environment Variables

```bash
# API Keys (optional)
export OPENAI_API_KEY="your-key-here"
export ANTHROPIC_API_KEY="your-key-here"

# Model Settings
export DEFAULT_MODEL="gpt-4"
export DEFAULT_TEMPERATURE="0.7"

# Server Settings (headless)
export INTERPRETER_PORT="8080"
export INTERPRETER_HOST="0.0.0.0"
```

### Configuration File

Create `~/.interpreter/config.yaml`:

```yaml
model: gpt-4
temperature: 0.7
context_window: 8192
auto_run: false
offline: false

# Headless specific
server:
  port: 8080
  host: 0.0.0.0
  
# KDE specific (GUI only)
kde:
  notifications: true
  clipboard_integration: true
```

---

## 📚 Documentation

- 📖 [Installation Guide](./docs/INSTALL.md) - Detailed installation instructions
- 🖥️ [Headless Setup](./docs/HEADLESS.md) - Server deployment guide
- 🎨 [GUI Features](./docs/GUI_GUIDE.md) - Visual interface documentation
- ⚡ [KDE Integration](./docs/KDE_INTEGRATION.md) - KDE automation guide
- 🐍 [Python Compatibility](./docs/PYTHON_COMPATIBILITY.md) - Python version details
- 🔧 [API Reference](./docs/API.md) - Server API documentation
- 🤝 [Contributing](./docs/CONTRIBUTING.md) - Development guidelines

---

## 🚨 Troubleshooting

### Common Issues

**Python Version Error**
```bash
# Check Python version
python3 --version

# If < 3.9, install newer version
# Ubuntu/Debian:
sudo apt update && sudo apt install python3.11

# Or use pyenv for any version
```

**Headless Installation Issues**
```bash
# Missing dependencies
pip install --upgrade pip
pip install wheel setuptools

# Permission errors
chmod +x install-headless.sh
```

**KDE Features Not Working**
```bash
# Check KDE version
plasmashell --version

# Install KDE dependencies
sudo apt install python3-pyqt5 python3-dbus
```

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](./docs/CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Fork and clone
git clone https://github.com/YOUR-USERNAME/Colonel-Katie.git
cd Colonel-Katie

# Create branch
git checkout -b feature/your-feature

# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built on [Open Interpreter](https://github.com/OpenInterpreter/open-interpreter)
- KDE integration inspired by [KDE Developer Documentation](https://develop.kde.org/)
- Enhanced by the Unicorn Commander community

---

## 🔗 Links

- **Repository**: [github.com/Unicorn-Commander/Colonel-Katie](https://github.com/Unicorn-Commander/Colonel-Katie)
- **Issues**: [Report bugs or request features](https://github.com/Unicorn-Commander/Colonel-Katie/issues)
- **Discussions**: [Community forum](https://github.com/Unicorn-Commander/Colonel-Katie/discussions)

---

**Colonel Katie** - *Where Open Interpreter meets KDE excellence* 🦄⚡