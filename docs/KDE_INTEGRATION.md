# ⚡ KDE Plasma Integration - Colonel Katie

Deep integration with KDE Plasma desktop environment for advanced automation and control.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [API Reference](#api-reference)
  - [Window Management](#window-management)
  - [Virtual Desktops](#virtual-desktops)
  - [Clipboard Operations](#clipboard-operations)
  - [File Operations](#file-operations)
  - [Notifications](#notifications)
  - [Plasma Shell](#plasma-shell)
- [Usage Examples](#usage-examples)
- [Advanced Automation](#advanced-automation)
- [Troubleshooting](#troubleshooting)

---

## Overview

Colonel Katie provides native KDE Plasma integration through the `computer.kde` module, enabling:
- Complete window and desktop control
- System-wide automation
- Native notifications
- Clipboard management
- File manager integration
- Plasma widget control

### Requirements
- KDE Plasma 5.x or 6.x
- Python D-Bus bindings
- PyQt5 or PySide6

---

## Features

### 🪟 Window Management
- List all windows
- Focus, minimize, maximize windows
- Move and resize windows
- Close applications
- Get window properties

### 🖥️ Virtual Desktop Control
- Switch between desktops
- Move windows between desktops
- Create/remove virtual desktops
- Get desktop information

### 📋 Clipboard Integration
- Read/write clipboard
- Clipboard history
- Multiple clipboard formats
- Clipboard monitoring

### 📁 File Manager (Dolphin)
- Open directories
- Select files
- File operations
- Integrated actions

### 🔔 System Notifications
- Send native KDE notifications
- Custom icons and actions
- Notification history
- Priority levels

### ⚡ Plasma Shell
- Control panels and widgets
- Desktop configuration
- Activity management
- Global shortcuts

---

## Installation

### Prerequisites

```bash
# Ubuntu/Debian
sudo apt install python3-pyqt5 python3-dbus python3-pyqt5.qtdbus

# Fedora
sudo dnf install python3-qt5 python3-dbus

# Arch
sudo pacman -S python-pyqt5 python-dbus
```

### Verify KDE Integration

```python
# In interpreter
>>> computer.kde.test_connection()
KDE integration status:
✅ D-Bus connection: Active
✅ KDE version: 5.27.0
✅ Plasma version: 5.27.0
✅ Window manager: KWin
✅ All systems operational
```

---

## API Reference

### Window Management

#### List Windows
```python
# Get all windows
windows = computer.kde.windows.list_windows()
for window in windows:
    print(f"Title: {window['title']}")
    print(f"Application: {window['application']}")
    print(f"Window ID: {window['id']}")
```

#### Window Operations
```python
# Find window by title
window_id = computer.kde.windows.find_window("Firefox")

# Focus window
computer.kde.windows.focus(window_id)

# Minimize/Maximize
computer.kde.windows.minimize(window_id)
computer.kde.windows.maximize(window_id)

# Move window
computer.kde.windows.move(window_id, x=100, y=100)

# Resize window
computer.kde.windows.resize(window_id, width=1200, height=800)

# Close window
computer.kde.windows.close(window_id)
```

#### Advanced Window Control
```python
# Get window properties
props = computer.kde.windows.get_properties(window_id)
print(f"Position: {props['x']}, {props['y']}")
print(f"Size: {props['width']}x{props['height']}")
print(f"Desktop: {props['desktop']}")
print(f"Minimized: {props['minimized']}")

# Set window properties
computer.kde.windows.set_properties(window_id, {
    'always_on_top': True,
    'skip_taskbar': False,
    'fullscreen': True
})
```

### Virtual Desktops

#### Desktop Navigation
```python
# Get current desktop
current = computer.kde.virtual_desktops.get_current()
print(f"Current desktop: {current}")

# Get total desktops
total = computer.kde.virtual_desktops.get_count()
print(f"Total desktops: {total}")

# Switch desktop
computer.kde.virtual_desktops.switch_to(2)

# Next/Previous desktop
computer.kde.virtual_desktops.next()
computer.kde.virtual_desktops.previous()
```

#### Desktop Management
```python
# Add new desktop
computer.kde.virtual_desktops.add_desktop("Development")

# Remove desktop
computer.kde.virtual_desktops.remove_desktop(4)

# Rename desktop
computer.kde.virtual_desktops.rename_desktop(1, "Main")

# Move window to desktop
computer.kde.virtual_desktops.move_window_to_desktop(window_id, 3)
```

### Clipboard Operations

#### Basic Clipboard
```python
# Get clipboard text
text = computer.kde.clipboard.get_text()
print(f"Clipboard: {text}")

# Set clipboard text
computer.kde.clipboard.set_text("Hello from Colonel Katie!")

# Clear clipboard
computer.kde.clipboard.clear()
```

#### Advanced Clipboard
```python
# Get clipboard history
history = computer.kde.clipboard.get_history()
for item in history:
    print(f"- {item[:50]}...")

# Get clipboard formats
formats = computer.kde.clipboard.get_formats()
print(f"Available formats: {formats}")

# Monitor clipboard changes
def on_clipboard_change(content):
    print(f"Clipboard changed: {content}")

computer.kde.clipboard.monitor(on_clipboard_change)
```

### File Operations

#### Dolphin Integration
```python
# Open directory in Dolphin
computer.kde.files.open_directory("/home/user/Documents")

# Open and select file
computer.kde.files.open_and_select("/home/user/file.txt")

# Get selected files in Dolphin
selected = computer.kde.files.get_selected_files()
for file in selected:
    print(f"Selected: {file}")
```

#### File Actions
```python
# Move to trash
computer.kde.files.trash("/path/to/file")

# Create directory
computer.kde.files.create_directory("/home/user/NewFolder")

# File properties dialog
computer.kde.files.show_properties("/path/to/file")
```

### Notifications

#### Basic Notifications
```python
# Simple notification
computer.kde.notifications.notify(
    title="Task Complete",
    message="Your script has finished running"
)

# With icon
computer.kde.notifications.notify(
    title="Download Complete", 
    message="file.zip downloaded successfully",
    icon="download"
)
```

#### Advanced Notifications
```python
# With actions
computer.kde.notifications.notify(
    title="Update Available",
    message="Colonel Katie v2.2 is available",
    actions=[
        ("update", "Update Now"),
        ("later", "Remind Later")
    ],
    on_action=lambda action: print(f"User clicked: {action}")
)

# With priority and timeout
computer.kde.notifications.notify(
    title="Critical Alert",
    message="System running low on disk space",
    priority="critical",
    timeout=10000  # 10 seconds
)
```

### Plasma Shell

#### Panel and Widget Control
```python
# Get panels
panels = computer.kde.plasma.get_panels()
for panel in panels:
    print(f"Panel {panel['id']}: {panel['location']}")

# Add widget to panel
computer.kde.plasma.add_widget(
    panel_id=1,
    widget="org.kde.plasma.digitalclock"
)

# Configure widget
computer.kde.plasma.configure_widget(
    widget_id="digitalclock-1",
    settings={
        "showDate": True,
        "dateFormat": "longDate"
    }
)
```

#### Activities
```python
# List activities
activities = computer.kde.plasma.get_activities()
for activity in activities:
    print(f"{activity['name']} ({activity['id']})")

# Switch activity
computer.kde.plasma.switch_activity("work")

# Create activity
computer.kde.plasma.create_activity(
    name="Gaming",
    icon="applications-games"
)
```

---

## Usage Examples

### Example 1: Window Tiling Script
```python
# Tile all windows on current desktop
def tile_windows():
    windows = computer.kde.windows.list_windows()
    desktop = computer.kde.virtual_desktops.get_current()
    
    # Filter windows on current desktop
    desktop_windows = [w for w in windows if w['desktop'] == desktop]
    
    if not desktop_windows:
        print("No windows to tile")
        return
    
    # Get screen dimensions
    screen = computer.kde.get_screen_geometry()
    width = screen['width'] // 2
    height = screen['height'] // len(desktop_windows) * 2
    
    # Tile windows
    for i, window in enumerate(desktop_windows[:4]):
        x = (i % 2) * width
        y = (i // 2) * height
        computer.kde.windows.move(window['id'], x, y)
        computer.kde.windows.resize(window['id'], width, height)
    
    print(f"Tiled {len(desktop_windows)} windows")

tile_windows()
```

### Example 2: Workspace Automation
```python
# Set up development workspace
def setup_dev_workspace():
    # Create or switch to Dev desktop
    computer.kde.virtual_desktops.switch_to_or_create("Development")
    
    # Open applications
    computer.kde.launch_application("code")  # VS Code
    computer.kde.launch_application("konsole")  # Terminal
    computer.kde.launch_application("firefox")  # Browser
    
    # Wait for windows to open
    import time
    time.sleep(3)
    
    # Arrange windows
    vscode = computer.kde.windows.find_window("Visual Studio Code")
    terminal = computer.kde.windows.find_window("Konsole")
    browser = computer.kde.windows.find_window("Firefox")
    
    # Left half for VS Code
    computer.kde.windows.move(vscode, 0, 0)
    computer.kde.windows.resize(vscode, 960, 1080)
    
    # Top right for browser
    computer.kde.windows.move(browser, 960, 0)
    computer.kde.windows.resize(browser, 960, 540)
    
    # Bottom right for terminal
    computer.kde.windows.move(terminal, 960, 540)
    computer.kde.windows.resize(terminal, 960, 540)
    
    computer.kde.notifications.notify(
        "Workspace Ready",
        "Development environment is set up"
    )

setup_dev_workspace()
```

### Example 3: System Monitor
```python
# Monitor system and send KDE notifications
import psutil

def monitor_system():
    # CPU usage
    cpu_percent = psutil.cpu_percent(interval=1)
    if cpu_percent > 80:
        computer.kde.notifications.notify(
            "High CPU Usage",
            f"CPU usage is at {cpu_percent}%",
            priority="high"
        )
    
    # Memory usage
    memory = psutil.virtual_memory()
    if memory.percent > 85:
        computer.kde.notifications.notify(
            "Low Memory",
            f"Only {memory.available // (1024**3)}GB available",
            priority="critical"
        )
    
    # Disk usage
    disk = psutil.disk_usage('/')
    if disk.percent > 90:
        computer.kde.notifications.notify(
            "Low Disk Space",
            f"Only {disk.free // (1024**3)}GB free",
            priority="critical",
            actions=[("clean", "Clean Now")],
            on_action=lambda a: computer.kde.launch_application("sweeper")
        )

# Run monitor
monitor_system()
```

### Example 4: Clipboard Manager
```python
# Enhanced clipboard manager with categories
class ClipboardManager:
    def __init__(self):
        self.categories = {
            'code': [],
            'urls': [],
            'text': []
        }
    
    def categorize_content(self, content):
        if content.startswith(('http://', 'https://')):
            return 'urls'
        elif any(keyword in content for keyword in ['def ', 'class ', 'import ', 'function']):
            return 'code'
        else:
            return 'text'
    
    def save_clipboard(self):
        content = computer.kde.clipboard.get_text()
        if content:
            category = self.categorize_content(content)
            self.categories[category].append(content)
            
            computer.kde.notifications.notify(
                "Clipboard Saved",
                f"Saved to {category} category",
                icon="edit-copy"
            )
    
    def show_menu(self):
        # Create menu using KDE runner or rofi
        items = []
        for category, contents in self.categories.items():
            for content in contents:
                preview = content[:50] + "..." if len(content) > 50 else content
                items.append(f"[{category}] {preview}")
        
        # This would integrate with KDE runner
        return items

manager = ClipboardManager()
manager.save_clipboard()
```

---

## Advanced Automation

### KWin Scripts
```python
# Generate and load KWin script
def create_kwin_script(name, code):
    script_path = f"~/.local/share/kwin/scripts/{name}/"
    
    # Create metadata
    metadata = """
[Desktop Entry]
Name={name}
Comment=Generated by Colonel Katie
Type=Service
X-KDE-ServiceTypes=KWin/Script
X-KDE-PluginInfo-Name={name}
X-KDE-PluginInfo-Version=1.0
X-Plasma-API=javascript
X-Plasma-MainScript=code/main.js
    """.format(name=name)
    
    # Install script
    computer.kde.plasma.install_kwin_script(name, metadata, code)
    computer.kde.plasma.enable_kwin_script(name)
```

### Global Shortcuts
```python
# Register global shortcut
computer.kde.register_shortcut(
    name="colonel_katie_assistant",
    key="Meta+Shift+K",
    action=lambda: computer.kde.launch_application("colonel-katie-gui")
)

# Custom action shortcuts
shortcuts = {
    "Meta+Shift+T": lambda: tile_windows(),
    "Meta+Shift+D": lambda: setup_dev_workspace(),
    "Meta+Shift+C": lambda: manager.save_clipboard()
}

for key, action in shortcuts.items():
    computer.kde.register_shortcut(f"katie_{key}", key, action)
```

### D-Bus Integration
```python
# Direct D-Bus calls for advanced control
def get_kwin_debug_info():
    import dbus
    bus = dbus.SessionBus()
    kwin = bus.get_object('org.kde.KWin', '/KWin')
    
    # Get compositor info
    compositing = kwin.compositingActive()
    effects = kwin.activeEffects()
    
    return {
        'compositing': compositing,
        'effects': effects,
        'platform': kwin.supportInformation()
    }

# Custom D-Bus service
class ColonelKatieService:
    def __init__(self):
        self.bus = dbus.SessionBus()
        self.name = dbus.service.BusName('org.colonelkatie.Assistant', self.bus)
        self.object = dbus.service.Object(self.bus, '/Assistant')
    
    @dbus.service.method('org.colonelkatie.Interface', in_signature='s', out_signature='s')
    def ExecuteCommand(self, command):
        # Execute interpreter command via D-Bus
        result = computer.execute(command)
        return str(result)
```

---

## Troubleshooting

### Common Issues

#### KDE Integration Not Working
```bash
# Check D-Bus
qdbus org.kde.KWin /KWin

# Check Python bindings
python3 -c "import PyQt5.QtDBus; print('Qt DBus OK')"

# Test connection
python3 -c "import dbus; bus = dbus.SessionBus(); print(bus.list_names())"
```

#### Permission Issues
```bash
# Add user to necessary groups
sudo usermod -a -G audio,video,input $USER

# Restart KDE session
qdbus org.kde.ksmserver /KSMServer logout 0 0 0
```

#### Missing Dependencies
```bash
# Full KDE development environment
sudo apt install kde-dev-scripts kdelibs5-dev

# Python KDE bindings
pip install PyQt5 python-dbus PyKDE5
```

### Debug Mode

Enable KDE debug output:
```python
# In interpreter
computer.kde.set_debug(True)

# Now all KDE operations will show debug info
computer.kde.windows.list_windows()
# [DEBUG] D-Bus call: org.kde.KWin.queryWindowInfo
# [DEBUG] Response time: 0.023s
# [DEBUG] Windows found: 5
```

### Performance Tips

1. **Batch Operations**
   ```python
   # Good - single D-Bus call
   computer.kde.windows.batch_operation([
       ('move', window1, 0, 0),
       ('resize', window1, 800, 600),
       ('move', window2, 800, 0)
   ])
   
   # Bad - multiple D-Bus calls
   computer.kde.windows.move(window1, 0, 0)
   computer.kde.windows.resize(window1, 800, 600)
   computer.kde.windows.move(window2, 800, 0)
   ```

2. **Cache Window IDs**
   ```python
   # Cache frequently accessed windows
   window_cache = {}
   window_cache['editor'] = computer.kde.windows.find_window("VS Code")
   window_cache['browser'] = computer.kde.windows.find_window("Firefox")
   ```

3. **Use Signals Instead of Polling**
   ```python
   # Good - event-driven
   computer.kde.windows.on_window_added(handle_new_window)
   
   # Bad - polling
   while True:
       check_for_new_windows()
       time.sleep(1)
   ```

---

## Resources

- [KDE Developer Documentation](https://develop.kde.org/)
- [D-Bus Specification](https://dbus.freedesktop.org/doc/dbus-specification.html)
- [KWin Scripting Tutorial](https://develop.kde.org/docs/plasma/kwin/)
- [Plasma Widget Development](https://develop.kde.org/docs/plasma/widget/)

---

**Note**: KDE integration features require a running KDE Plasma session and will not work in headless mode or other desktop environments.