# 🦄⚡ Colonel Katie - AI Agent Development Platform ⚡🦄

**Professional AI Agent Development Platform with Visual Builder**

![Version](https://img.shields.io/badge/version-2.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-Production%20Ready-brightgreen.svg)

---

## 🌟 Overview

Colonel Katie is a comprehensive AI agent development platform that transforms the way you create, manage, and deploy AI agents. With a professional visual interface, extensive prompt library, and powerful integrations, Colonel Katie makes AI agent development accessible to everyone.

### ✨ Key Features

- 🎨 **Visual Agent Builder** - Create AI agents with an intuitive point-and-click interface
- 📚 **Professional Prompt Library** - 10+ expert-crafted templates across multiple categories
- 🤖 **Multi-Provider Support** - Ollama, OpenAI, HuggingFace, and custom model providers
- 🧠 **RAG Integration** - Upload documents and build intelligent knowledge bases
- 🎙️ **Voice Interaction** - Push-to-talk and text-to-speech capabilities
- 💾 **Memory Management** - Persistent memory with mem0ai integration
- 📊 **Real-time Monitoring** - System status, memory usage, and connection monitoring
- 🎯 **Export & Sharing** - Save conversations in JSON/Markdown formats
- ⌨️ **Power User Features** - Keyboard shortcuts and advanced settings

---

## 🚀 Quick Start

### Option 1: Automated Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-username/Colonel-Katie.git
cd Colonel-Katie

# Run the installer
python install.py
```

The installer will:
- Check Python compatibility
- Create a virtual environment
- Install all dependencies
- Set up desktop shortcuts
- Create launcher scripts

### Option 2: Manual Installation

```bash
# Clone the repository
git clone https://github.com/your-username/Colonel-Katie.git
cd Colonel-Katie

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run Colonel Katie
python main.py
```

---

## 📋 System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **RAM**: 4GB (8GB recommended)
- **Storage**: 2GB free space
- **OS**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)

### Recommended Requirements
- **Python**: 3.10+
- **RAM**: 8GB or more
- **Storage**: 5GB free space
- **GPU**: CUDA-compatible for local model inference

### Dependencies
- PySide6 (GUI framework)
- OpenInterpreter (AI integration)
- ChromaDB (vector database)
- SentenceTransformers (embeddings)
- PyAudio, pyttsx3, SpeechRecognition (voice features)
- mem0ai (memory management)

---

## 🎯 Core Features

### 🎨 Visual Agent Builder

Create sophisticated AI agents without writing code:

- **General Settings**: Agent name, profile picture, description
- **Model Configuration**: Choose from multiple providers and models
- **Prompt Templates**: Select from professional prompt library
- **Tool Selection**: Enable/disable capabilities (shell, browser, files)
- **Voice Settings**: Configure text-to-speech profiles
- **Memory Integration**: Persistent conversation memory

### 📚 Prompt Library

Choose from expertly crafted prompt templates:

- **General**: Helpful AI Assistant
- **Development**: Code Reviewer, Technical Writer
- **Writing**: Creative Writer, Content Creator
- **Analytics**: Data Analyst, Research Assistant
- **Business**: Business Analyst, Product Manager
- **Security**: Cybersecurity Expert
- **DevOps**: System Administrator

### 🧠 RAG (Retrieval Augmented Generation)

Build intelligent knowledge bases:

- **Document Upload**: PDF, DOCX, TXT, MD, HTML, code files
- **Drag & Drop**: Easy document management
- **Vector Search**: Semantic search through documents
- **Chunking Strategies**: Optimized text processing
- **Real-time Indexing**: Instant document processing

### 🎙️ Voice Interaction

Natural voice communication:

- **Push-to-Talk**: Space bar activation
- **Speech Recognition**: Convert speech to text
- **Text-to-Speech**: AI voice responses
- **Voice Profiles**: Multiple voice options
- **Wake Word Detection**: Hands-free activation (coming soon)

---

## 🎮 User Guide

### First Launch

1. **Welcome Screen**: Colonel Katie displays a splash screen during initialization
2. **Model Selection**: Choose your preferred AI model from the sidebar
3. **Agent Creation**: Use the Agent Builder (Ctrl+Shift+A) to create your first agent
4. **Document Upload**: Add knowledge documents via drag & drop

### Basic Usage

#### Creating an AI Agent

1. Press `Ctrl+Shift+A` or go to Options → Agent Builder
2. **General Settings**: Enter agent name and select profile picture
3. **Prompt Selection**: Choose from the prompt library or write custom instructions
4. **Model Configuration**: Select model provider and specific model
5. **Tool Selection**: Enable capabilities (shell, browser, files, etc.)
6. **Save**: Click "Save Agent Profile" to create your agent

#### Chat Interface

- **Send Messages**: Type in the input field and press Enter
- **Voice Input**: Hold Space bar to record voice messages
- **Speak Responses**: Click the 🔊 icon to hear responses
- **Context Menu**: Right-click messages for copy, edit, regenerate options
- **Quick Settings**: Click ⚙️ for model and temperature adjustments

#### Document Management

- **Upload Documents**: Drag & drop files into the knowledge management section
- **Supported Formats**: PDF, DOCX, TXT, MD, HTML, code files
- **Search Documents**: RAG automatically searches relevant content
- **Manage Collections**: Organize documents by topic or project

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+L` | Focus chat input field |
| `Ctrl+K` | Clear chat history |
| `F9` | Toggle sidebars |
| `Ctrl+Shift+A` | Open Agent Builder |
| `Ctrl+E` | Export conversation |
| `Space` (hold) | Push-to-talk voice input |
| `Ctrl+Q` | Quit application |

---

## ⚙️ Configuration

### Model Providers

#### Ollama (Local Models)
```python
# Install Ollama first: https://ollama.ai
# Pull models: ollama pull llama3
# Colonel Katie auto-discovers Ollama models
```

#### OpenAI
```python
# Set API key in environment or settings
OPENAI_API_KEY=your_api_key_here
```

#### HuggingFace
```python
# Set token for private models
HUGGINGFACE_TOKEN=your_token_here
```

### Environment Variables

Create a `.env` file in the application directory:

```bash
# API Keys
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
HUGGINGFACE_TOKEN=your_hf_token

# Model Settings
DEFAULT_MODEL=gpt-4
DEFAULT_PROVIDER=openai

# Voice Settings
TTS_ENABLED=true
STT_ENABLED=true

# Memory Settings
MEMORY_ENABLED=true
MEMORY_PROVIDER=mem0ai

# RAG Settings
RAG_ENABLED=true
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

---

## 🔧 Advanced Features

### Custom Model Providers

Add custom model providers through the Agent Builder:

1. Click "Add Custom Model" in model selection
2. Enter model name and API endpoint
3. Configure authentication and parameters
4. Test connection and save

### Memory Management

Colonel Katie uses mem0ai for persistent memory:

- **Automatic Extraction**: Key information saved from conversations
- **Context Retrieval**: Relevant memories injected into new conversations
- **Memory Visualization**: View extracted memories in the sidebar
- **Manual Management**: Add, edit, or delete memories

### Plugin System

Extend Colonel Katie with custom tools:

1. Create tool classes following the interface
2. Register tools in the function registry
3. Enable/disable tools per agent
4. Share tools with the community

---

## 🐛 Troubleshooting

### Common Issues

#### Installation Problems

**Python version incompatible**
```bash
# Check Python version
python --version
# Upgrade Python to 3.8+ if needed
```

**Missing system dependencies**
```bash
# Linux: Install audio libraries
sudo apt-get install portaudio19-dev python3-pyaudio

# macOS: Install with Homebrew
brew install portaudio
```

**Virtual environment issues**
```bash
# Delete and recreate venv
rm -rf venv
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

#### Runtime Issues

**Models not loading**
- Check API keys in environment variables
- Verify model names and provider availability
- Check internet connection for cloud providers

**Voice features not working**
- Install/update audio drivers
- Check microphone permissions
- Verify PyAudio installation

**Memory issues with large documents**
- Reduce chunk size in RAG settings
- Close other applications to free RAM
- Use document pagination for large files

### Getting Help

1. **Documentation**: Check this README and DEVELOPMENT_ROADMAP.md
2. **Status Bar**: Monitor system status in the bottom bar
3. **Logs**: Check console output for error messages
4. **Debug Mode**: Enable verbose logging in settings

---

## 🤝 Contributing

We welcome contributions to Colonel Katie! Here's how to get started:

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/your-username/Colonel-Katie.git
cd Colonel-Katie

# Create development environment
python -m venv dev-env
source dev-env/bin/activate  # or dev-env\Scripts\activate on Windows

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Start development server
python main.py
```

### Contribution Guidelines

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Focus Areas

- 🔧 **Performance Optimization**: Improve startup time and memory usage
- 🎨 **UI/UX Enhancements**: Better animations and user experience
- 🤖 **Model Integrations**: Support for new model providers
- 🧩 **Plugin System**: Extensible tool and capability framework
- 📱 **Mobile Support**: Web interface for mobile devices
- 🌐 **Cloud Deployment**: Docker containers and cloud deployment

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **OpenInterpreter Team** - Core AI integration framework
- **PySide6/Qt** - Professional GUI framework
- **ChromaDB** - Vector database for RAG
- **mem0ai** - Memory management system
- **The Open Source Community** - Various dependencies and tools

---

## 📞 Support

- **Documentation**: [GitHub Wiki](https://github.com/your-username/Colonel-Katie/wiki)
- **Issues**: [GitHub Issues](https://github.com/your-username/Colonel-Katie/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/Colonel-Katie/discussions)

---

<div align="center">

**🦄⚡ Colonel Katie - Empowering AI Development with Honor and Efficiency! ⚡🦄**

*Made with ❤️ by the Colonel Katie Team*

</div>