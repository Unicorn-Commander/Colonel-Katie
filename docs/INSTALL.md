# 📦 Installation Guide - Colonel Katie

This guide covers all installation methods for Colonel Katie, from quick setups to advanced configurations.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation Methods](#installation-methods)
  - [Headless Installation](#headless-installation-recommended-for-servers)
  - [Full GUI Installation](#full-gui-installation)
  - [Development Installation](#development-installation)
  - [Docker Installation](#docker-installation)
- [Post-Installation](#post-installation)
- [Troubleshooting](#troubleshooting)
- [Upgrading](#upgrading)
- [Uninstallation](#uninstallation)

---

## Prerequisites

### System Requirements

| Component | Headless | GUI | Development |
|-----------|----------|-----|-------------|
| Python | 3.9-3.13 | 3.9-3.13 | 3.9-3.13 |
| RAM | 2GB min | 4GB min | 8GB recommended |
| Storage | 1GB | 3GB | 5GB |
| OS | Any Linux | Linux with X11/Wayland | Any Linux |
| Desktop | Not required | KDE Plasma (recommended) | Any |

### Required System Packages

**Ubuntu/Debian:**
```bash
# Basic dependencies
sudo apt update
sudo apt install -y python3-pip python3-venv git curl wget

# For GUI mode (optional)
sudo apt install -y python3-pyqt5 python3-dbus libportaudio2

# For voice features (optional)
sudo apt install -y espeak ffmpeg
```

**Fedora/RHEL:**
```bash
# Basic dependencies
sudo dnf install -y python3-pip python3-virtualenv git curl wget

# For GUI mode (optional)
sudo dnf install -y python3-qt5 python3-dbus portaudio

# For voice features (optional)
sudo dnf install -y espeak ffmpeg
```

**Arch/Manjaro:**
```bash
# Basic dependencies
sudo pacman -S python-pip python-virtualenv git curl wget

# For GUI mode (optional)
sudo pacman -S python-pyqt5 python-dbus portaudio

# For voice features (optional)
sudo pacman -S espeak ffmpeg
```

---

## Installation Methods

### Headless Installation (Recommended for Servers)

The headless installation is optimized for servers, containers, and systems without GUI support.

#### Method 1: Automated Script
```bash
# Clone the repository
git clone https://github.com/Unicorn-Commander/Colonel-Katie.git
cd Colonel-Katie

# Run the headless installer
chmod +x install-headless.sh
./install-headless.sh
```

The script will:
- ✅ Check Python version compatibility
- ✅ Create an isolated virtual environment
- ✅ Install only CLI dependencies (no GUI libraries)
- ✅ Create convenience scripts
- ✅ Verify the installation

#### Method 2: Manual Headless Installation
```bash
# Clone the repository
git clone https://github.com/Unicorn-Commander/Colonel-Katie.git
cd Colonel-Katie

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install core package without dependencies
pip install --no-deps open-interpreter

# Install headless dependencies only
pip install \
    anthropic astor git-python google-generativeai \
    html2image html2text inquirer ipykernel jupyter-client \
    litellm matplotlib platformdirs psutil pydantic \
    pyperclip pyyaml rich selenium send2trash setuptools \
    shortuuid six toml wget yaspin pyautogui typer \
    fastapi uvicorn webdriver-manager nltk tokentrim

# Test installation
interpreter --version
```

### Full GUI Installation

For desktop users who want the complete experience with visual interface and KDE integration.

#### Method 1: Automated Installer
```bash
# Clone the repository
git clone https://github.com/Unicorn-Commander/Colonel-Katie.git
cd Colonel-Katie

# Run the GUI installer
python install.py
```

Features installed:
- ✅ Full GUI with PySide6
- ✅ KDE Plasma integration
- ✅ Visual agent builder
- ✅ Voice interaction
- ✅ Document RAG system
- ✅ Memory management

#### Method 2: Manual GUI Installation
```bash
# Clone the repository
git clone https://github.com/Unicorn-Commander/Colonel-Katie.git
cd Colonel-Katie

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install everything including GUI
pip install -r requirements.txt

# Launch GUI
python main.py
```

### Development Installation

For contributors and developers who want to modify the code.

```bash
# Fork and clone your fork
git clone https://github.com/YOUR-USERNAME/Colonel-Katie.git
cd Colonel-Katie

# Add upstream remote
git remote add upstream https://github.com/Unicorn-Commander/Colonel-Katie.git

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install in editable mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests
pytest tests/
```

### Docker Installation

For containerized deployments:

```bash
# Clone the repository
git clone https://github.com/Unicorn-Commander/Colonel-Katie.git
cd Colonel-Katie

# Build Docker image
docker build -t colonel-katie .

# Run container (headless)
docker run -it colonel-katie interpreter

# Run with API server
docker run -p 8080:8080 colonel-katie interpreter --server
```

---

## Post-Installation

### 1. Verify Installation

```bash
# Check version
interpreter --version

# Run help
interpreter --help

# Test with simple command
interpreter "print('Hello from Colonel Katie!')"
```

### 2. Configure API Keys (Optional)

Create configuration file:
```bash
mkdir -p ~/.interpreter
cat > ~/.interpreter/config.yaml << EOF
# Model configuration
model: gpt-4
temperature: 0.7

# API keys (optional - can use environment variables)
# openai_api_key: your-key-here
# anthropic_api_key: your-key-here

# Features
auto_run: false
safe_mode: ask
EOF
```

Or use environment variables:
```bash
# Add to ~/.bashrc or ~/.zshrc
export OPENAI_API_KEY="your-key-here"
export ANTHROPIC_API_KEY="your-key-here"
```

### 3. Set Up Convenience Aliases

```bash
# Add to ~/.bashrc
alias katie="cd ~/Colonel-Katie && source venv/bin/activate && interpreter"
alias katie-gui="cd ~/Colonel-Katie && source venv/bin/activate && python main.py"

# Reload shell
source ~/.bashrc
```

### 4. Install Additional Models (Optional)

For local model support:
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull models
ollama pull llama2
ollama pull codellama
ollama pull mistral
```

---

## Troubleshooting

### Common Issues and Solutions

#### Python Version Issues
```bash
# Error: Python version not supported
# Solution: Install Python 3.11
wget https://www.python.org/ftp/python/3.11.7/Python-3.11.7.tgz
tar -xf Python-3.11.7.tgz
cd Python-3.11.7
./configure --enable-optimizations
make -j$(nproc)
sudo make altinstall
```

#### Missing Rust Compiler (for tiktoken)
```bash
# Error: Can't build tiktoken
# Solution: Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

#### Permission Errors
```bash
# Error: Permission denied
# Solution: Fix permissions
chmod +x install-headless.sh
chmod -R 755 venv/
```

#### Import Errors
```bash
# Error: Module not found
# Solution: Reinstall in virtual environment
deactivate
rm -rf venv/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### GUI Not Launching
```bash
# Error: No module named 'PySide6'
# Solution: Install GUI dependencies
pip install PySide6 PyQt5
```

### Debug Mode

Run with verbose output:
```bash
# CLI debug
interpreter --verbose --debug

# GUI debug
python main.py --debug
```

---

## Upgrading

### Automatic Update (Recommended)
```bash
cd Colonel-Katie
./update.sh
```

This automatically:
- Pulls latest changes
- Updates dependencies
- Preserves your configuration
- Creates backups

### Advanced Update
```bash
cd Colonel-Katie
./update-headless.sh
```

Features:
- Shows what will be updated
- Automatic backup creation
- Handles uncommitted changes
- Runs migration scripts

### Manual Update
```bash
cd Colonel-Katie
git pull origin main
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

### Major Version Upgrade
```bash
cd Colonel-Katie
git fetch --all
git checkout v2.1.0  # or latest version
./install-headless.sh  # or python install.py for GUI
```

For more details, see [UPDATING.md](./UPDATING.md)

---

## Uninstallation

### Complete Removal
```bash
# Remove virtual environment
rm -rf ~/Colonel-Katie/venv

# Remove configuration
rm -rf ~/.interpreter

# Remove the repository
rm -rf ~/Colonel-Katie

# Remove aliases (edit ~/.bashrc and remove katie aliases)
```

### Keep Configuration
```bash
# Just remove the installation
rm -rf ~/Colonel-Katie
# Configuration in ~/.interpreter remains
```

---

## Next Steps

- 📖 Read the [User Guide](./USER_GUIDE.md)
- 🖥️ Set up [Headless Mode](./HEADLESS.md)
- ⚡ Explore [KDE Integration](./KDE_INTEGRATION.md)
- 🔧 Configure [API Settings](./API.md)
- 🤝 [Contribute](./CONTRIBUTING.md) to the project

---

**Need Help?** Open an issue on [GitHub](https://github.com/Unicorn-Commander/Colonel-Katie/issues)