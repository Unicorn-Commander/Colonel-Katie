#!/bin/bash

# Colonel Katie - Simple Update Wrapper
# Quick way to update your installation

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}🦄⚡ Updating Colonel Katie...${NC}"

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Pull latest changes
echo -e "${YELLOW}📥 Fetching latest changes...${NC}"
git pull origin main

# Run install script which now handles updates
echo -e "\n${YELLOW}📦 Updating installation...${NC}"
./install-headless.sh

echo -e "\n${GREEN}✅ Update complete!${NC}"