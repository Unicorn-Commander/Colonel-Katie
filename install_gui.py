#!/usr/bin/env python3
"""
Colonel Katie GUI Installation Script
Graphical installer for the Colonel Katie AI Agent Platform
"""

import os
import sys
import subprocess
import shutil
import json
import platform
from pathlib import Path
from datetime import datetime
import threading

try:
    from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                                   QHBoxLayout, QWidget, QLabel, QPushButton, 
                                   QTextEdit, QLineEdit, QFileDialog, 
                                   QProgressBar, QMessageBox, QCheckBox)
    from PySide6.QtCore import Qt, QThread, QTimer, Signal
    from PySide6.QtGui import QFont, QPixmap, QIcon
except ImportError:
    print("❌ PySide6 not found. Installing...")
    subprocess.run([sys.executable, "-m", "pip", "install", "PySide6"], check=True)
    from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                                   QHBoxLayout, QWidget, QLabel, QPushButton, 
                                   QTextEdit, QLineEdit, QFileDialog, 
                                   QProgressBar, QMessageBox, QCheckBox)
    from PySide6.QtCore import Qt, QThread, QTimer, Signal
    from PySide6.QtGui import QFont, QPixmap, QIcon

class InstallationWorker(QThread):
    progress_updated = Signal(int)
    log_updated = Signal(str)
    installation_complete = Signal(bool)
    
    def __init__(self, install_dir, create_desktop_entry=True):
        super().__init__()
        self.install_dir = Path(install_dir)
        self.create_desktop_entry = create_desktop_entry
        self.system = platform.system()
        self.python_exe = sys.executable
        self.venv_dir = None
        
    def run(self):
        try:
            self.progress_updated.emit(10)
            self.log_updated.emit("🔍 Checking Python version...")
            
            if not self.check_python_version():
                self.installation_complete.emit(False)
                return
                
            self.progress_updated.emit(20)
            self.log_updated.emit("📁 Creating directories...")
            
            if not self.create_directories():
                self.installation_complete.emit(False)
                return
                
            self.progress_updated.emit(30)
            self.log_updated.emit("🐍 Creating virtual environment...")
            
            if not self.create_virtual_environment():
                self.installation_complete.emit(False)
                return
                
            self.progress_updated.emit(40)
            self.log_updated.emit("📦 Installing Python dependencies...")
            
            if not self.install_requirements():
                self.installation_complete.emit(False)
                return
                
            self.progress_updated.emit(70)
            self.log_updated.emit("📋 Copying application files...")
            
            if not self.copy_application_files():
                self.installation_complete.emit(False)
                return
                
            self.progress_updated.emit(85)
            self.log_updated.emit("🚀 Creating launcher scripts...")
            
            if not self.create_launcher_scripts():
                self.installation_complete.emit(False)
                return
                
            self.progress_updated.emit(95)
            if self.create_desktop_entry and self.system == "Linux":
                self.log_updated.emit("🖥️ Creating desktop entry...")
                self.create_desktop_entry_file()
                
            self.log_updated.emit("⚙️ Creating configuration...")
            self.create_config_file()
            
            self.progress_updated.emit(100)
            self.log_updated.emit("✅ Installation completed successfully!")
            self.installation_complete.emit(True)
            
        except Exception as e:
            self.log_updated.emit(f"❌ Installation failed: {e}")
            self.installation_complete.emit(False)
    
    def check_python_version(self):
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            self.log_updated.emit(f"❌ Python 3.8+ required. Found: {version.major}.{version.minor}")
            return False
        self.log_updated.emit(f"✅ Python {version.major}.{version.minor}.{version.micro} compatible")
        return True
    
    def create_directories(self):
        try:
            self.install_dir.mkdir(parents=True, exist_ok=True)
            self.venv_dir = self.install_dir / "venv"
            self.log_updated.emit(f"✅ Created: {self.install_dir}")
            return True
        except Exception as e:
            self.log_updated.emit(f"❌ Error creating directories: {e}")
            return False
    
    def create_virtual_environment(self):
        try:
            subprocess.run([
                self.python_exe, "-m", "venv", str(self.venv_dir)
            ], check=True, capture_output=True, text=True)
            self.log_updated.emit(f"✅ Virtual environment created")
            return True
        except subprocess.CalledProcessError as e:
            self.log_updated.emit(f"❌ Error creating virtual environment: {e}")
            return False
    
    def get_venv_python(self):
        if self.system == "Windows":
            return self.venv_dir / "Scripts" / "python.exe"
        else:
            return self.venv_dir / "bin" / "python"
    
    def install_requirements(self):
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
            self.log_updated.emit(f"   Installing {req}...")
            try:
                subprocess.run([
                    str(venv_python), "-m", "pip", "install", req
                ], check=True, capture_output=True, text=True)
                self.log_updated.emit(f"   ✅ {req}")
            except subprocess.CalledProcessError as e:
                self.log_updated.emit(f"   ⚠️ Warning: Failed to install {req}")
        
        return True
    
    def copy_application_files(self):
        source_dir = Path(__file__).parent
        app_dir = self.install_dir / "app"
        
        try:
            if app_dir.exists():
                shutil.rmtree(app_dir)
            app_dir.mkdir()
            
            items_to_copy = [
                "gui", "main.py", "colonel-katie-icon.png", 
                "README.md", "DEVELOPMENT_ROADMAP.md"
            ]
            
            for item in items_to_copy:
                source_path = source_dir / item
                dest_path = app_dir / item
                
                if source_path.exists():
                    if source_path.is_dir():
                        shutil.copytree(source_path, dest_path)
                    else:
                        shutil.copy2(source_path, dest_path)
                    self.log_updated.emit(f"   ✅ Copied: {item}")
                else:
                    self.log_updated.emit(f"   ⚠️ Warning: {item} not found")
            
            return True
        except Exception as e:
            self.log_updated.emit(f"❌ Error copying files: {e}")
            return False
    
    def create_launcher_scripts(self):
        app_dir = self.install_dir / "app"
        venv_python = self.get_venv_python()
        
        try:
            if self.system == "Windows":
                launcher_path = self.install_dir / "ColonelKatie.bat"
                launcher_content = f'''@echo off
cd /d "{app_dir}"
"{venv_python}" main.py
pause
'''
                with open(launcher_path, 'w') as f:
                    f.write(launcher_content)
                self.log_updated.emit(f"   ✅ Created Windows launcher")
            else:
                launcher_path = self.install_dir / "colonel-katie"
                launcher_content = f'''#!/bin/bash
cd "{app_dir}"
"{venv_python}" main.py
'''
                with open(launcher_path, 'w') as f:
                    f.write(launcher_content)
                os.chmod(launcher_path, 0o755)
                self.log_updated.emit(f"   ✅ Created launcher script")
            
            return True
        except Exception as e:
            self.log_updated.emit(f"❌ Error creating launcher: {e}")
            return False
    
    def create_desktop_entry_file(self):
        if self.system == "Linux":
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
                self.log_updated.emit(f"   ✅ Desktop entry created")
            except Exception as e:
                self.log_updated.emit(f"❌ Error creating desktop entry: {e}")
    
    def create_config_file(self):
        config_dir = self.install_dir / "config"
        config_dir.mkdir(exist_ok=True)
        
        config_file = config_dir / "colonel-katie.json"
        config_data = {
            "version": "2.0",
            "installation_date": datetime.now().isoformat(),
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
            self.log_updated.emit(f"   ✅ Configuration created")
        except Exception as e:
            self.log_updated.emit(f"❌ Error creating config: {e}")

class ColonelKatieGUIInstaller(QMainWindow):
    def __init__(self):
        super().__init__()
        self.system = platform.system()
        self.default_install_dir = self.get_default_install_dir()
        self.init_ui()
        
    def get_default_install_dir(self):
        if self.system == "Windows":
            return Path.home() / "AppData" / "Local" / "ColonelKatie"
        elif self.system == "Darwin":
            return Path.home() / "Applications" / "ColonelKatie"
        else:
            return Path.home() / ".local" / "share" / "colonel-katie"
    
    def init_ui(self):
        self.setWindowTitle("Colonel Katie Installer")
        self.setFixedSize(600, 500)
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Header
        header = QLabel("🦄⚡ Colonel Katie AI Agent Platform ⚡🦄")
        header.setAlignment(Qt.AlignCenter)
        header.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(header)
        
        version_label = QLabel("Version 2.0 - Production Ready")
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setFont(QFont("Arial", 10))
        layout.addWidget(version_label)
        
        # Install directory selection
        dir_layout = QHBoxLayout()
        dir_label = QLabel("Install Directory:")
        self.dir_input = QLineEdit(str(self.default_install_dir))
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_directory)
        
        dir_layout.addWidget(dir_label)
        dir_layout.addWidget(self.dir_input)
        dir_layout.addWidget(browse_btn)
        layout.addLayout(dir_layout)
        
        # Options
        self.desktop_entry_cb = QCheckBox("Create desktop entry (Linux only)")
        self.desktop_entry_cb.setChecked(True)
        if self.system != "Linux":
            self.desktop_entry_cb.setEnabled(False)
        layout.addWidget(self.desktop_entry_cb)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Log area
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setMaximumHeight(200)
        layout.addWidget(self.log_area)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.install_btn = QPushButton("Install")
        self.install_btn.clicked.connect(self.start_installation)
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.close)
        
        button_layout.addWidget(self.install_btn)
        button_layout.addWidget(self.close_btn)
        layout.addLayout(button_layout)
        
        # Style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
            QPushButton {
                background-color: #4a4a4a;
                border: 1px solid #666666;
                border-radius: 4px;
                padding: 8px;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #5a5a5a;
            }
            QPushButton:pressed {
                background-color: #3a3a3a;
            }
            QLineEdit {
                background-color: #3a3a3a;
                border: 1px solid #666666;
                border-radius: 4px;
                padding: 4px;
                color: #ffffff;
            }
            QTextEdit {
                background-color: #1a1a1a;
                border: 1px solid #666666;
                border-radius: 4px;
                color: #ffffff;
                font-family: monospace;
            }
            QCheckBox {
                color: #ffffff;
            }
            QProgressBar {
                border: 1px solid #666666;
                border-radius: 4px;
                text-align: center;
                color: #ffffff;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 4px;
            }
        """)
    
    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Installation Directory")
        if directory:
            self.dir_input.setText(directory)
    
    def start_installation(self):
        install_dir = self.dir_input.text().strip()
        if not install_dir:
            QMessageBox.warning(self, "Error", "Please select an installation directory.")
            return
        
        self.install_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.log_area.clear()
        
        # Start installation in worker thread
        self.worker = InstallationWorker(
            install_dir, 
            self.desktop_entry_cb.isChecked()
        )
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.log_updated.connect(self.update_log)
        self.worker.installation_complete.connect(self.installation_finished)
        self.worker.start()
    
    def update_progress(self, value):
        self.progress_bar.setValue(value)
    
    def update_log(self, message):
        self.log_area.append(message)
        self.log_area.ensureCursorVisible()
    
    def installation_finished(self, success):
        self.install_btn.setEnabled(True)
        
        if success:
            QMessageBox.information(
                self, 
                "Installation Complete", 
                "Colonel Katie has been installed successfully!\n\n"
                f"Installation location: {self.dir_input.text()}"
            )
        else:
            QMessageBox.critical(
                self, 
                "Installation Failed", 
                "Installation failed. Please check the log for details."
            )

def main():
    app = QApplication(sys.argv)
    installer = ColonelKatieGUIInstaller()
    installer.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()