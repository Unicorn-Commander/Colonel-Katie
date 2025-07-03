#!/usr/bin/env python3
"""
Colonel Katie Installation Script
Professional installation wizard for the Colonel Katie AI Agent Platform
"""

import os
import sys
import subprocess
import shutil
import json
import platform
from pathlib import Path

class ColonelKatieInstaller:
    def __init__(self):
        self.system = platform.system()
        self.python_exe = sys.executable
        self.install_dir = None
        self.venv_dir = None
        self.requirements_installed = False
        
    def print_banner(self):
        """Display installation banner."""
        print("=" * 70)
        print("🦄⚡ COLONEL KATIE - AI AGENT PLATFORM INSTALLER ⚡🦄")
        print("=" * 70)
        print("Version 2.0 - Production Ready")
        print("AI Agent Development Platform with Visual Builder")
        print("=" * 70)
        print()
        
    def check_python_version(self):
        """Check if Python version is compatible."""
        print("🔍 Checking Python version...")
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            print("❌ Error: Python 3.8 or higher is required!")
            print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
            return False
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible!")
        return True
        
    def get_install_location(self):
        """Get installation directory from user."""
        print("\n📂 Choose installation location:")
        
        if self.system == "Windows":
            default_dir = Path.home() / "AppData" / "Local" / "ColonelKatie"
        elif self.system == "Darwin":  # macOS
            default_dir = Path.home() / "Applications" / "ColonelKatie"
        else:  # Linux
            default_dir = Path.home() / ".local" / "share" / "colonel-katie"
            
        print(f"   Default: {default_dir}")
        choice = input("   Press Enter for default, or type custom path: ").strip()
        
        if choice:
            self.install_dir = Path(choice)
        else:
            self.install_dir = default_dir
            
        print(f"✅ Installation directory: {self.install_dir}")
        return True
        
    def create_directories(self):
        """Create installation directories."""
        print(f"\n📁 Creating directories...")
        try:
            self.install_dir.mkdir(parents=True, exist_ok=True)
            self.venv_dir = self.install_dir / "venv"
            print(f"✅ Created: {self.install_dir}")
            return True
        except Exception as e:
            print(f"❌ Error creating directories: {e}")
            return False
            
    def create_virtual_environment(self):
        """Create Python virtual environment."""
        print(f"\n🐍 Creating virtual environment...")
        try:
            subprocess.run([
                self.python_exe, "-m", "venv", str(self.venv_dir)
            ], check=True, capture_output=True, text=True)
            print(f"✅ Virtual environment created: {self.venv_dir}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error creating virtual environment: {e}")
            return False
            
    def get_venv_python(self):
        """Get path to virtual environment Python."""
        if self.system == "Windows":
            return self.venv_dir / "Scripts" / "python.exe"
        else:
            return self.venv_dir / "bin" / "python"
            
    def install_requirements(self):
        """Install Python requirements."""
        print(f"\n📦 Installing Python dependencies...")
        
        requirements = [
            "PySide6>=6.5.0",
            "open-interpreter>=0.2.0",
            "python-dotenv>=1.0.0",
            "markdown-it-py>=3.0.0",
            "pygments>=2.15.0",
            "psutil>=5.9.0",
            "requests>=2.31.0",
            "beautifulsoup4>=4.12.0",
            "PyPDF2>=3.0.0",
            "python-docx>=0.8.11",
            "chromadb>=0.4.0",
            "sentence-transformers>=2.2.0",
            "pyaudio>=0.2.11",
            "pyttsx3>=2.90",
            "SpeechRecognition>=3.10.0",
            "mem0ai>=0.1.0"
        ]
        
        venv_python = self.get_venv_python()
        
        for req in requirements:
            print(f"   Installing {req}...")
            try:
                subprocess.run([
                    str(venv_python), "-m", "pip", "install", req
                ], check=True, capture_output=True, text=True)
                print(f"   ✅ {req}")
            except subprocess.CalledProcessError as e:
                print(f"   ⚠️  Warning: Failed to install {req}")
                print(f"      Error: {e}")
                
        self.requirements_installed = True
        print("✅ Python dependencies installation completed!")
        return True
        
    def copy_application_files(self):
        """Copy application files to installation directory."""
        print(f"\n📋 Copying application files...")
        
        source_dir = Path(__file__).parent
        app_dir = self.install_dir / "app"
        
        try:
            # Copy main application files
            if app_dir.exists():
                shutil.rmtree(app_dir)
            app_dir.mkdir()
            
            # Files and directories to copy
            items_to_copy = [
                "gui",
                "main.py",
                "colonel-katie-icon.png",
                "README.md",
                "DEVELOPMENT_ROADMAP.md"
            ]
            
            for item in items_to_copy:
                source_path = source_dir / item
                dest_path = app_dir / item
                
                if source_path.exists():
                    if source_path.is_dir():
                        shutil.copytree(source_path, dest_path)
                        print(f"   ✅ Copied directory: {item}")
                    else:
                        shutil.copy2(source_path, dest_path)
                        print(f"   ✅ Copied file: {item}")
                else:
                    print(f"   ⚠️  Warning: {item} not found in source")
                    
            print("✅ Application files copied successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error copying files: {e}")
            return False
            
    def create_launcher_scripts(self):
        """Create launcher scripts for the application."""
        print(f"\n🚀 Creating launcher scripts...")
        
        app_dir = self.install_dir / "app"
        venv_python = self.get_venv_python()
        
        try:
            if self.system == "Windows":
                # Windows batch file
                launcher_path = self.install_dir / "ColonelKatie.bat"
                launcher_content = f'''@echo off
cd /d "{app_dir}"
"{venv_python}" main.py
pause
'''
                with open(launcher_path, 'w') as f:
                    f.write(launcher_content)
                print(f"   ✅ Created Windows launcher: {launcher_path}")
                
            else:
                # Unix shell script
                launcher_path = self.install_dir / "colonel-katie"
                launcher_content = f'''#!/bin/bash
cd "{app_dir}"
"{venv_python}" main.py
'''
                with open(launcher_path, 'w') as f:
                    f.write(launcher_content)
                os.chmod(launcher_path, 0o755)
                print(f"   ✅ Created launcher script: {launcher_path}")
                
            return True
            
        except Exception as e:
            print(f"❌ Error creating launcher: {e}")
            return False
            
    def create_desktop_entry(self):
        """Create desktop entry (Linux) or shortcut (Windows)."""
        if self.system == "Linux":
            print(f"\n🖥️  Creating desktop entry...")
            try:
                desktop_dir = Path.home() / ".local" / "share" / "applications"
                desktop_dir.mkdir(parents=True, exist_ok=True)
                
                desktop_file = desktop_dir / "colonel-katie.desktop"
                launcher_script = self.install_dir / "colonel-katie"
                icon_path = self.install_dir / "app" / "colonel-katie-icon.png"
                
                desktop_content = f'''[Desktop Entry]
Name=Colonel Katie
Comment=AI Agent Development Platform
Exec={launcher_script}
Icon={icon_path}
Terminal=false
Type=Application
Categories=Development;Office;
StartupWMClass=colonel-katie
'''
                with open(desktop_file, 'w') as f:
                    f.write(desktop_content)
                os.chmod(desktop_file, 0o755)
                print(f"   ✅ Desktop entry created: {desktop_file}")
                return True
                
            except Exception as e:
                print(f"❌ Error creating desktop entry: {e}")
                return False
        return True
        
    def create_config_file(self):
        """Create initial configuration file."""
        print(f"\n⚙️  Creating configuration...")
        
        config_dir = self.install_dir / "config"
        config_dir.mkdir(exist_ok=True)
        
        config_file = config_dir / "colonel-katie.json"
        config_data = {
            "version": "2.0",
            "installation_date": str(Path().ctime()),
            "installation_path": str(self.install_dir),
            "first_run": True,
            "settings": {
                "theme": "modern_dark",
                "auto_updates": True,
                "telemetry": False
            }
        }
        
        try:
            with open(config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
            print(f"   ✅ Configuration created: {config_file}")
            return True
        except Exception as e:
            print(f"❌ Error creating config: {e}")
            return False
            
    def run_installation(self):
        """Run the complete installation process."""
        self.print_banner()
        
        steps = [
            ("Checking Python version", self.check_python_version),
            ("Getting installation location", self.get_install_location),
            ("Creating directories", self.create_directories),
            ("Creating virtual environment", self.create_virtual_environment),
            ("Installing requirements", self.install_requirements),
            ("Copying application files", self.copy_application_files),
            ("Creating launcher scripts", self.create_launcher_scripts),
            ("Creating desktop entry", self.create_desktop_entry),
            ("Creating configuration", self.create_config_file)
        ]
        
        for step_name, step_function in steps:
            print(f"\n{'='*20} {step_name} {'='*20}")
            if not step_function():
                print(f"\n❌ Installation failed at: {step_name}")
                return False
                
        self.print_success()
        return True
        
    def print_success(self):
        """Print installation success message."""
        print("\n" + "="*70)
        print("🎉 COLONEL KATIE INSTALLATION COMPLETED SUCCESSFULLY! 🎉")
        print("="*70)
        print()
        print("📍 Installation Details:")
        print(f"   Location: {self.install_dir}")
        print(f"   Virtual Environment: {self.venv_dir}")
        print()
        print("🚀 How to run Colonel Katie:")
        
        if self.system == "Windows":
            launcher = self.install_dir / "ColonelKatie.bat"
            print(f"   Double-click: {launcher}")
            print(f"   Or run from cmd: {launcher}")
        else:
            launcher = self.install_dir / "colonel-katie"
            print(f"   Run: {launcher}")
            if self.system == "Linux":
                print("   Or search for 'Colonel Katie' in your application menu")
                
        print()
        print("📚 Documentation:")
        print(f"   README: {self.install_dir}/app/README.md")
        print(f"   Roadmap: {self.install_dir}/app/DEVELOPMENT_ROADMAP.md")
        print()
        print("🦄⚡ Welcome to Colonel Katie - AI Agent Platform! ⚡🦄")
        print("="*70)

def main():
    """Main installation function."""
    installer = ColonelKatieInstaller()
    
    try:
        success = installer.run_installation()
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n❌ Installation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during installation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()