#!/bin/bash

# Setup convenient alias for The Colonel
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🔗 Setting up command alias for The Colonel..."

# Add alias to bashrc if it doesn't exist
if ! grep -q "alias colonel=" ~/.bashrc 2>/dev/null; then
    echo "" >> ~/.bashrc
    echo "# The Colonel AI Assistant" >> ~/.bashrc
    echo "alias colonel='$SCRIPT_DIR/launch_colonel.sh'" >> ~/.bashrc
    echo "✅ Added 'colonel' alias to ~/.bashrc"
else
    echo "ℹ️  Alias already exists in ~/.bashrc"
fi

# Add alias to zshrc if it exists and doesn't have the alias
if [[ -f ~/.zshrc ]] && ! grep -q "alias colonel=" ~/.zshrc 2>/dev/null; then
    echo "" >> ~/.zshrc
    echo "# The Colonel AI Assistant" >> ~/.zshrc
    echo "alias colonel='$SCRIPT_DIR/launch_colonel.sh'" >> ~/.zshrc
    echo "✅ Added 'colonel' alias to ~/.zshrc"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "You can now launch The Colonel by:"
echo "  • Typing 'colonel' in any terminal (after restarting terminal)"
echo "  • Clicking the application icon in KDE"
echo "  • Searching for 'The Colonel' in KRunner (Alt+Space)"
echo ""