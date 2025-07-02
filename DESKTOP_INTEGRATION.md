# 🖥️ The Colonel - Desktop Integration Guide

## Quick Installation

To install The Colonel as a native KDE application with icon and launcher:

```bash
./install_desktop.sh
```

## What Gets Installed

✅ **Application Launcher Entry** - Find "The Colonel" in your KDE Application Menu  
✅ **KRunner Integration** - Search for "Colonel" or "AI Assistant" with Alt+Space  
✅ **Desktop Icon** - Professional application icon in system icon cache  
✅ **Command Line Alias** - Type `colonel` in any terminal  

## Installation Options

### 1. Full Desktop Integration
```bash
./install_desktop.sh    # Install as KDE application
./setup_alias.sh        # Add terminal alias
```

### 2. Terminal Only
```bash
./setup_alias.sh        # Just add 'colonel' command
```

### 3. Manual Launch
```bash
./launch_colonel.sh     # Direct script execution
```

## How to Launch

### From KDE Application Launcher
1. Open the Application Launcher (usually bottom-left corner)
2. Search for "The Colonel" or "AI Assistant"
3. Click the icon to launch

### From KRunner
1. Press `Alt + Space` to open KRunner
2. Type "colonel" or "ai assistant"
3. Press Enter to launch

### From Terminal
```bash
colonel                 # If alias is installed
./launch_colonel.sh     # Direct script execution
```

### From File Manager
- Navigate to the project folder
- Double-click `launch_colonel.sh`

## Advanced Usage

### Pin to Taskbar
1. Launch The Colonel from Application Launcher
2. Right-click the taskbar icon
3. Select "Pin to Task Manager"

### Create Desktop Shortcut
1. Right-click on desktop
2. Select "Create New" → "Link to Application"
3. Browse to `/home/ucadmin/.local/share/applications/the-colonel.desktop`

### Add to Favorites
1. Open Application Launcher
2. Right-click "The Colonel"
3. Select "Add to Favorites"

## Uninstallation

To remove The Colonel from your desktop environment:

```bash
./uninstall_desktop.sh
```

This removes:
- Desktop entry from Application Launcher
- Icon from system cache
- Updates desktop database

The project files remain untouched in the project directory.

## Troubleshooting

### Icon Not Showing
```bash
# Manually update icon cache
gtk-update-icon-cache ~/.local/share/icons
```

### Application Not Found in Launcher
```bash
# Manually update desktop database
update-desktop-database ~/.local/share/applications
```

### Permission Issues
```bash
# Ensure scripts are executable
chmod +x *.sh
```

### Environment Issues
The launcher script automatically:
- Detects and activates Python virtual environments
- Uses Poetry if available
- Falls back to system Python

## File Structure

```
Colonel-Katie/
├── the-colonel.desktop      # KDE desktop entry
├── launch_colonel.sh        # Main launcher script
├── install_desktop.sh       # Installation script
├── uninstall_desktop.sh     # Uninstall script
├── setup_alias.sh           # Terminal alias setup
├── The_Colonel.png          # Application icon
└── DESKTOP_INTEGRATION.md   # This guide
```

## Technical Details

- **Desktop Entry**: Follows freedesktop.org standards
- **Categories**: Development, Utility, Office
- **Icon Format**: PNG (with SVG fallback)
- **Launch Method**: Bash script with environment detection
- **Installation Location**: `~/.local/share/applications/`
- **Icon Location**: `~/.local/share/icons/`

---

🎉 **Enjoy your fully integrated Colonel AI Assistant!**