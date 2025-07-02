#!/bin/bash

# The Colonel Desktop Integration Uninstaller
# This script removes The Colonel from KDE applications

echo "🗑️  Uninstalling The Colonel Desktop Integration..."

# Remove desktop entry
DESKTOP_FILE="$HOME/.local/share/applications/the-colonel.desktop"
if [[ -f "$DESKTOP_FILE" ]]; then
    rm "$DESKTOP_FILE"
    echo "✅ Removed desktop entry"
else
    echo "ℹ️  Desktop entry not found"
fi

# Remove icons
ICONS_DIR="$HOME/.local/share/icons"
if [[ -f "$ICONS_DIR/The_Colonel.png" ]]; then
    rm "$ICONS_DIR/The_Colonel.png"
    echo "✅ Removed The_Colonel.png icon"
fi

if [[ -f "$ICONS_DIR/unicorn.svg" ]]; then
    rm "$ICONS_DIR/unicorn.svg"
    echo "✅ Removed unicorn.svg icon"
fi

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$HOME/.local/share/applications"
    echo "✅ Desktop database updated"
fi

# Update icon cache
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache "$ICONS_DIR" 2>/dev/null || true
    echo "✅ Icon cache updated"
fi

echo ""
echo "🎉 The Colonel has been uninstalled from your desktop!"
echo "The application files remain in the project directory."
echo ""