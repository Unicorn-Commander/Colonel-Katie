#!/bin/bash

# Colonel Katie - Update Script
# Safely updates your installation while preserving user data

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🦄⚡ Colonel Katie - Update System ⚡🦄${NC}"
echo -e "${BLUE}======================================${NC}"

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo -e "${RED}❌ Not a git repository. Cannot update.${NC}"
    echo -e "${YELLOW}   Please use git clone for initial installation${NC}"
    exit 1
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo -e "${YELLOW}⚠️  You have uncommitted changes:${NC}"
    git status --short
    echo
    read -p "Stash changes and continue? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git stash push -m "Auto-stash before update $(date +%Y%m%d_%H%M%S)"
        echo -e "${GREEN}✅ Changes stashed${NC}"
    else
        echo -e "${RED}❌ Update cancelled${NC}"
        exit 1
    fi
fi

# Backup user data
echo -e "\n${YELLOW}💾 Backing up user data...${NC}"
BACKUP_DIR="$SCRIPT_DIR/.backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Backup configuration if it exists
if [ -f ~/.interpreter/config.yaml ]; then
    cp ~/.interpreter/config.yaml "$BACKUP_DIR/config.yaml"
    echo -e "   ✅ Backed up config.yaml"
fi

# Backup any custom profiles
if [ -d "$SCRIPT_DIR/interpreter/terminal_interface/profiles/custom" ]; then
    cp -r "$SCRIPT_DIR/interpreter/terminal_interface/profiles/custom" "$BACKUP_DIR/custom_profiles"
    echo -e "   ✅ Backed up custom profiles"
fi

# Backup conversation history if it exists
if [ -d ~/.interpreter/conversations ]; then
    cp -r ~/.interpreter/conversations "$BACKUP_DIR/conversations"
    echo -e "   ✅ Backed up conversation history"
fi

# Record current version
CURRENT_COMMIT=$(git rev-parse HEAD)
echo "$CURRENT_COMMIT" > "$BACKUP_DIR/previous_version.txt"

# Fetch latest changes
echo -e "\n${YELLOW}📥 Fetching latest updates...${NC}"
git fetch origin main

# Show what will be updated
echo -e "\n${YELLOW}📋 Changes to be applied:${NC}"
git log --oneline HEAD..origin/main

echo
read -p "Continue with update? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${RED}❌ Update cancelled${NC}"
    exit 1
fi

# Pull latest changes
echo -e "\n${YELLOW}🔄 Updating to latest version...${NC}"
git pull origin main

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "\n${YELLOW}📦 No virtual environment found. Running fresh install...${NC}"
    ./install-headless.sh
    exit 0
fi

# Update dependencies
echo -e "\n${YELLOW}📚 Updating dependencies...${NC}"
source venv/bin/activate

# Upgrade pip first
pip install --upgrade pip wheel setuptools

# Update the package if installed in editable mode
if pip show -q open-interpreter 2>/dev/null; then
    echo -e "   Updating open-interpreter package..."
    pip install -e . --no-deps
fi

# Create updated requirements file
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

# Update dependencies
pip install --upgrade -r requirements-headless.txt

# Try to update tiktoken if Rust is available
if command -v rustc >/dev/null 2>&1; then
    pip install --upgrade tiktoken 2>/dev/null || true
fi

# Run any migration scripts if they exist
if [ -f "$SCRIPT_DIR/scripts/migrate.py" ]; then
    echo -e "\n${YELLOW}🔧 Running migration scripts...${NC}"
    python "$SCRIPT_DIR/scripts/migrate.py"
fi

# Update convenience scripts
echo -e "\n${YELLOW}🔧 Updating convenience scripts...${NC}"
chmod +x "$SCRIPT_DIR/interpreter.sh" 2>/dev/null || true
chmod +x "$SCRIPT_DIR/interpreter-server.sh" 2>/dev/null || true
chmod +x "$SCRIPT_DIR/katie" 2>/dev/null || true

# Test the update
echo -e "\n${YELLOW}🧪 Testing updated installation...${NC}"
if interpreter --version 2>/dev/null; then
    VERSION=$(interpreter --version 2>&1 | head -n1)
    echo -e "${GREEN}✅ Update successful!${NC}"
    echo -e "   Version: $VERSION"
else
    echo -e "${YELLOW}⚠️  Could not verify interpreter command${NC}"
fi

# Show update summary
NEW_COMMIT=$(git rev-parse HEAD)
echo -e "\n${GREEN}═══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Colonel Katie Updated Successfully! 🎉${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
echo -e "\n${BLUE}📊 Update Summary:${NC}"
echo -e "  • Previous version: $(echo $CURRENT_COMMIT | cut -c1-8)"
echo -e "  • New version:      $(echo $NEW_COMMIT | cut -c1-8)"
echo -e "  • Backup location:  $BACKUP_DIR"

# Check for stashed changes
if git stash list | grep -q "Auto-stash before update"; then
    echo -e "\n${YELLOW}📌 Remember: You have stashed changes${NC}"
    echo -e "   To restore: ${GREEN}git stash pop${NC}"
fi

echo -e "\n${BLUE}💡 What's next:${NC}"
echo -e "  • Check the changelog: ${GREEN}git log --oneline $CURRENT_COMMIT..$NEW_COMMIT${NC}"
echo -e "  • Test your setup:     ${GREEN}./katie --help${NC}"
echo -e "  • Read update notes:   ${GREEN}cat docs/CHANGELOG.md${NC}"

echo -e "\n${BLUE}Happy coding! 🦄⚡${NC}\n"