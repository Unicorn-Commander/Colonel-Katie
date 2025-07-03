#!/usr/bin/env python3
"""
Colonel Katie - Quick Launch Script
Simple launcher with environment checks and helpful messages
"""

import subprocess
import sys
import os

def main():
    """Quick launch with environment validation."""
    print("🦄⚡ Colonel Katie - Quick Launch ⚡🦄")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return
        
    # Check if we're in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    if not in_venv:
        print("⚠️  Recommendation: Use a virtual environment")
        print("   python -m venv venv")
        print("   source venv/bin/activate  # Linux/Mac")
        print("   venv\\Scripts\\activate     # Windows")
        print()
    
    print("🚀 Launching Colonel Katie...")
    
    # Launch main application
    try:
        subprocess.run([sys.executable, "main.py"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Launch failed. Try: pip install -r requirements.txt")
    except KeyboardInterrupt:
        print("\n👋 Colonel Katie closed by user")

if __name__ == "__main__":
    main()