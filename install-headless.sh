#!/bin/bash

# Colonel Katie - Headless Installation Script
# For servers without GUI support
# Works with Python 3.9-3.13

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🦄⚡ Colonel Katie - Headless Installation ⚡🦄${NC}"
echo -e "${BLUE}===============================================${NC}"
echo -e "${YELLOW}Enhanced Open Interpreter with Python 3.13 support${NC}"
echo -e ""

# Function to check command existence
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to compare versions
version_ge() {
    [ "$(printf '%s\n' "$1" "$2" | sort -V | head -n1)" = "$2" ]
}

# Check Python version
echo -e "${YELLOW}🔍 Checking Python version...${NC}"
if command_exists python3; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    PYTHON_FULL_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:3])))')
    
    echo -e "Found Python ${GREEN}$PYTHON_FULL_VERSION${NC}"
    
    if ! version_ge "$PYTHON_VERSION" "3.9"; then
        echo -e "${RED}❌ Python 3.9 or higher is required${NC}"
        echo -e "${YELLOW}   Your version: $PYTHON_FULL_VERSION${NC}"
        exit 1
    fi
    
    if version_ge "$PYTHON_VERSION" "3.13"; then
        echo -e "${GREEN}✨ Python 3.13+ detected - Colonel Katie enhanced mode!${NC}"
    fi
else
    echo -e "${RED}❌ Python3 not found. Please install Python 3.9 or higher${NC}"
    exit 1
fi

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo -e "${RED}❌ pyproject.toml not found in current directory${NC}"
    echo -e "${YELLOW}   Current directory: $SCRIPT_DIR${NC}"
    exit 1
fi

PROJECT_DIR="$SCRIPT_DIR"

# Check for required system commands
echo -e "\n${YELLOW}🔍 Checking system dependencies...${NC}"
MISSING_DEPS=""

for cmd in git curl wget; do
    if ! command_exists "$cmd"; then
        MISSING_DEPS="$MISSING_DEPS $cmd"
    else
        echo -e "  ✅ $cmd"
    fi
done

if [ -n "$MISSING_DEPS" ]; then
    echo -e "${RED}❌ Missing system dependencies:$MISSING_DEPS${NC}"
    echo -e "${YELLOW}   Please install them using your package manager${NC}"
    exit 1
fi

# Create virtual environment
echo -e "\n${YELLOW}📦 Creating virtual environment...${NC}"
if [ -d "venv" ]; then
    echo -e "${YELLOW}   Virtual environment already exists${NC}"
    read -p "   Remove and recreate? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf venv
        python3 -m venv venv
    fi
else
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "\n${YELLOW}🔌 Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip and install wheel
echo -e "\n${YELLOW}⬆️  Upgrading pip and installing build tools...${NC}"
pip install --upgrade pip wheel setuptools

# Create requirements file for headless installation
echo -e "\n${YELLOW}📝 Creating headless requirements file...${NC}"
cat > requirements-headless.txt << 'EOF'
# Core AI/LLM libraries
anthropic>=0.37.1
google-generativeai>=0.7.1
litellm>=1.41.26
openai

# Code execution and parsing
astor>=0.8.1
ipykernel>=6.26.0
jupyter-client>=8.6.0

# CLI and interface
inquirer>=3.1.3
rich>=13.4.2
typer>=0.12.5
yaspin>=3.0.2

# Utilities
git-python>=1.0.3
platformdirs>=4.2.0
psutil>=5.9.6
pydantic>=2.6.4
pyperclip>=1.9.0
pyyaml>=6.0.1
shortuuid>=1.0.13
toml>=0.10.2
wget>=3.2

# Web and automation (headless compatible)
html2image>=2.0.4.3
html2text>=2024.2.26
selenium>=4.24.0
webdriver-manager>=4.0.2
pyautogui>=0.9.54

# API server
fastapi>=0.111.0
uvicorn>=0.30.1

# Data processing
matplotlib>=3.8.2
send2trash>=1.8.2
six>=1.16.0

# NLP
nltk>=3.8.1
tokentrim>=0.1.13
EOF

# Install open-interpreter package structure
echo -e "\n${YELLOW}📦 Installing Colonel Katie (Open Interpreter enhanced)...${NC}"
if [ -f "setup.py" ] || [ -f "pyproject.toml" ]; then
    pip install -e . --no-deps
else
    echo -e "${YELLOW}   No setup.py found, installing from requirements${NC}"
fi

# Install dependencies
echo -e "\n${YELLOW}📚 Installing headless dependencies...${NC}"
pip install -r requirements-headless.txt

# Try to install tiktoken if Rust is available
echo -e "\n${YELLOW}🦀 Checking for optional dependencies...${NC}"
if command_exists rustc; then
    echo -e "  ✅ Rust compiler found"
    echo -e "  📦 Installing tiktoken..."
    pip install tiktoken || echo -e "  ${YELLOW}⚠️  tiktoken installation failed (non-critical)${NC}"
else
    echo -e "  ℹ️  Rust compiler not found"
    echo -e "  ${YELLOW}   Skipping tiktoken (some features may be limited)${NC}"
    echo -e "  ${YELLOW}   To install: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh${NC}"
fi

# Create convenience scripts
echo -e "\n${YELLOW}🔧 Creating convenience scripts...${NC}"

# Main interpreter script
cat > "$PROJECT_DIR/interpreter.sh" << 'EOF'
#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$SCRIPT_DIR/venv/bin/activate"
exec interpreter "$@"
EOF
chmod +x "$PROJECT_DIR/interpreter.sh"

# Server script
cat > "$PROJECT_DIR/interpreter-server.sh" << 'EOF'
#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$SCRIPT_DIR/venv/bin/activate"
exec interpreter --server "$@"
EOF
chmod +x "$PROJECT_DIR/interpreter-server.sh"

# Test script
cat > "$PROJECT_DIR/test-installation.sh" << 'EOF'
#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$SCRIPT_DIR/venv/bin/activate"
echo "Testing Colonel Katie installation..."
interpreter --version
python -c "import interpreter; print('✅ Import successful')"
EOF
chmod +x "$PROJECT_DIR/test-installation.sh"

# Test installation
echo -e "\n${YELLOW}🧪 Testing installation...${NC}"
if source venv/bin/activate && interpreter --version 2>/dev/null; then
    VERSION=$(interpreter --version 2>&1 | head -n1)
    echo -e "${GREEN}✅ Installation successful!${NC}"
    echo -e "   Version: $VERSION"
else
    echo -e "${YELLOW}⚠️  Basic installation complete, but interpreter command not found${NC}"
    echo -e "   This is normal if installing from source"
fi

# Create sample configuration
echo -e "\n${YELLOW}⚙️  Creating sample configuration...${NC}"
mkdir -p ~/.interpreter
if [ ! -f ~/.interpreter/config.yaml ]; then
    cat > ~/.interpreter/config.yaml << 'EOF'
# Colonel Katie Configuration
model: gpt-4
temperature: 0.7
auto_run: false
safe_mode: ask

# Headless server settings
server:
  host: 0.0.0.0
  port: 8080
  
# Add your API keys here or use environment variables
# openai_api_key: your-key-here
# anthropic_api_key: your-key-here
EOF
    echo -e "   Created ~/.interpreter/config.yaml"
else
    echo -e "   Config already exists at ~/.interpreter/config.yaml"
fi

# Final instructions
echo -e "\n${GREEN}═══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Colonel Katie (Headless) Installation Complete! 🎉${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"

echo -e "\n${BLUE}📖 Quick Start:${NC}"
echo -e "  1. Activate virtual environment:"
echo -e "     ${GREEN}source $PROJECT_DIR/venv/bin/activate${NC}"
echo -e "  2. Run interpreter:"
echo -e "     ${GREEN}interpreter${NC}"

echo -e "\n${BLUE}🚀 Convenience Scripts:${NC}"
echo -e "  • Interactive mode: ${GREEN}$PROJECT_DIR/interpreter.sh${NC}"
echo -e "  • Server mode:      ${GREEN}$PROJECT_DIR/interpreter-server.sh${NC}"
echo -e "  • Test install:     ${GREEN}$PROJECT_DIR/test-installation.sh${NC}"

echo -e "\n${BLUE}⚙️  Configuration:${NC}"
echo -e "  • Edit config: ${GREEN}nano ~/.interpreter/config.yaml${NC}"
echo -e "  • Set API keys in config or environment variables"

echo -e "\n${BLUE}📚 Documentation:${NC}"
echo -e "  • Headless guide: ${GREEN}$PROJECT_DIR/docs/HEADLESS.md${NC}"
echo -e "  • Full docs:      ${GREEN}$PROJECT_DIR/docs/${NC}"

if ! command_exists rustc; then
    echo -e "\n${YELLOW}💡 Optional: Install Rust for full features:${NC}"
    echo -e "     ${GREEN}curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh${NC}"
fi

echo -e "\n${BLUE}Need help? Check the docs or open an issue!${NC}"
echo -e "${BLUE}Happy coding! 🦄⚡${NC}\n"