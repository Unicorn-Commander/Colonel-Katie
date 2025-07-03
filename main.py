#!/usr/bin/env python3
"""
Colonel Katie - AI Agent Development Platform
Main application entry point

Launch the Colonel Katie GUI application with all features:
- Visual Agent Builder
- Multi-provider model support  
- RAG document processing
- Voice interaction
- Memory management
- Professional UI with status monitoring

Usage:
    python main.py
    
Requirements:
    - Python 3.8+
    - PySide6
    - All dependencies from requirements.txt
"""

import sys
import os
import traceback
from pathlib import Path

# Add current directory to Python path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def check_dependencies():
    """Check critical dependencies before launching."""
    missing_deps = []
    
    try:
        import PySide6
    except ImportError:
        missing_deps.append("PySide6")
        
    try:
        import interpreter
    except ImportError:
        missing_deps.append("open-interpreter")
        
    if missing_deps:
        print("❌ Missing critical dependencies:")
        for dep in missing_deps:
            print(f"   • {dep}")
        print("\n💡 Install with: pip install -r requirements.txt")
        return False
        
    return True

def main():
    """Main application entry point."""
    print("🦄⚡ Colonel Katie - AI Agent Development Platform ⚡🦄")
    print("Initializing application...")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    try:
        # Import Qt application
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import Qt
        from PySide6.QtGui import QIcon
        
        # Set high DPI attributes before creating QApplication
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        
        # Create QApplication instance
        app = QApplication(sys.argv)
        app.setApplicationName("Colonel Katie")
        app.setApplicationVersion("2.0")
        app.setOrganizationName("Colonel Katie Team")
        
        # Set application icon
        icon_path = current_dir / "colonel-katie-icon.png"
        if icon_path.exists():
            app.setWindowIcon(QIcon(str(icon_path)))
        
        # Import and create main window
        from gui.desktop.main_window import ColonelKDEApp
        
        # Create main window
        main_window = ColonelKDEApp()
        main_window.show()
        
        print("✅ Colonel Katie launched successfully!")
        print("   • Visual Agent Builder: Ctrl+Shift+A")
        print("   • Clear Chat: Ctrl+K")
        print("   • Toggle Sidebars: F9")
        print("   • Export Chat: Ctrl+E")
        print("   • Focus Input: Ctrl+L")
        print("\n🚀 Ready for AI agent development!")
        
        # Start the application event loop
        sys.exit(app.exec())
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Ensure all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Critical Error: {e}")
        print("\n🔍 Full traceback:")
        traceback.print_exc()
        print("\n💡 Please report this error to: https://github.com/your-username/Colonel-Katie/issues")
        sys.exit(1)

if __name__ == "__main__":
    main()