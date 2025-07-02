#!/bin/bash

# The Colonel Desktop Integration Installer
# This script installs The Colonel as a KDE application

set -e  # Exit on any error

echo "🚀 Installing The Colonel Desktop Integration..."

# Get current directory
CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Create user applications directory if it doesn't exist
APPS_DIR="$HOME/.local/share/applications"
mkdir -p "$APPS_DIR"

# Create user icons directory if it doesn't exist  
ICONS_DIR="$HOME/.local/share/icons"
mkdir -p "$ICONS_DIR"

# Copy icon to user icons directory
if [[ -f "$CURRENT_DIR/The_Colonel.png" ]]; then
    cp "$CURRENT_DIR/The_Colonel.png" "$ICONS_DIR/"
    echo "✅ Icon copied to $ICONS_DIR"
elif [[ -f "$CURRENT_DIR/unicorn.svg" ]]; then
    cp "$CURRENT_DIR/unicorn.svg" "$ICONS_DIR/"
    echo "✅ Icon copied to $ICONS_DIR"
else
    echo "⚠️  No icon found, using default"
fi

# Update the desktop file with correct paths
sed "s|/home/ucadmin/Development/Colonel-Katie|$CURRENT_DIR|g" "$CURRENT_DIR/the-colonel.desktop" > "$APPS_DIR/the-colonel.desktop"

# Make the launcher script executable
chmod +x "$CURRENT_DIR/launch_colonel.sh"

# Make the desktop file executable
chmod +x "$APPS_DIR/the-colonel.desktop"

echo "✅ Desktop entry installed to $APPS_DIR"

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$APPS_DIR"
    echo "✅ Desktop database updated"
fi

# Update icon cache
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache "$ICONS_DIR" 2>/dev/null || true
    echo "✅ Icon cache updated"
fi

echo ""
echo "🎉 The Colonel has been installed!"
echo ""
echo "You can now:"
echo "  • Find 'The Colonel' in your KDE Application Launcher"
echo "  • Search for 'Colonel' or 'AI Assistant' in KRunner (Alt+Space)"
echo "  • Pin it to your taskbar or desktop"
echo ""
echo "To uninstall, simply delete:"
echo "  • $APPS_DIR/the-colonel.desktop"
echo "  • $ICONS_DIR/The_Colonel.png (or unicorn.svg)"
echo ""