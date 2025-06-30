#!/usr/bin/env python3
"""
Simple test file to verify KDE tools functionality
"""
import os
import sys

def test_imports():
    """Test that all KDE tools can be imported successfully"""
    try:
        from kde_tools import notifications, plasma_shell, virtual_desktops, windows, file_operations, clipboard
        print("✅ All KDE tools imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_pyside6_availability():
    """Test that PySide6 is available for D-Bus operations"""
    try:
        from PySide6.QtDBus import QDBusConnection, QDBusMessage
        from PySide6.QtCore import QCoreApplication
        print("✅ PySide6 D-Bus modules available")
        return True
    except ImportError as e:
        print(f"❌ PySide6 import error: {e}")
        return False

def test_core_dependencies():
    """Test core server dependencies"""
    try:
        import fastapi
        import janus
        import uvicorn
        print("✅ Core server dependencies available")
        return True
    except ImportError as e:
        print(f"❌ Core dependency error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing The Colonel KDE Tools Migration")
    print("=" * 50)
    
    all_passed = True
    all_passed &= test_pyside6_availability()
    all_passed &= test_imports()
    all_passed &= test_core_dependencies()
    
    print("=" * 50)
    if all_passed:
        print("✅ All tests passed! PySide6 migration successful.")
        sys.exit(0)
    else:
        print("❌ Some tests failed.")
        sys.exit(1)