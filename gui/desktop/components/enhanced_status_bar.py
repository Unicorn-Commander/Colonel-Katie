"""
Enhanced status bar with real-time information and animations.
"""

from PySide6.QtWidgets import QStatusBar, QLabel, QProgressBar, QHBoxLayout, QWidget
from PySide6.QtCore import QTimer, Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QColor
import psutil
import platform
from datetime import datetime

class EnhancedStatusBar(QStatusBar):
    """Status bar with system info, model status, and memory usage."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_status_bar()
        self.setup_timer()
        
    def setup_status_bar(self):
        """Initialize status bar components."""
        # Status message (left side)
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #00CED1; font-weight: bold;")
        self.addWidget(self.status_label)
        
        # Spacer
        self.addPermanentWidget(QLabel(""), 1)
        
        # Memory usage
        self.memory_widget = QWidget()
        self.memory_layout = QHBoxLayout(self.memory_widget)
        self.memory_layout.setContentsMargins(0, 0, 0, 0)
        
        self.memory_label = QLabel("RAM: ")
        self.memory_label.setStyleSheet("color: #E0E0E0;")
        self.memory_layout.addWidget(self.memory_label)
        
        self.memory_bar = QProgressBar()
        self.memory_bar.setMaximum(100)
        self.memory_bar.setFixedWidth(100)
        self.memory_bar.setFixedHeight(16)
        self.memory_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #3A3A5A;
                border-radius: 3px;
                background-color: #1A1A2E;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00CED1, stop:0.8 #8A2BE2, stop:1 #FF6347);
                border-radius: 2px;
            }
        """)
        self.memory_layout.addWidget(self.memory_bar)
        
        self.addPermanentWidget(self.memory_widget)
        
        # Separator
        separator = QLabel(" | ")
        separator.setStyleSheet("color: #3A3A5A;")
        self.addPermanentWidget(separator)
        
        # Model status
        self.model_status = QLabel("Model: N/A")
        self.model_status.setStyleSheet("color: #E0E0E0;")
        self.addPermanentWidget(self.model_status)
        
        # Separator
        separator2 = QLabel(" | ")
        separator2.setStyleSheet("color: #3A3A5A;")
        self.addPermanentWidget(separator2)
        
        # Connection status
        self.connection_status = QLabel("⚫ Offline")
        self.connection_status.setStyleSheet("color: #FF6347;")
        self.addPermanentWidget(self.connection_status)
        
        # Time
        self.time_label = QLabel()
        self.time_label.setStyleSheet("color: #E0E0E0; font-family: monospace;")
        self.addPermanentWidget(self.time_label)
        
    def setup_timer(self):
        """Setup update timer for real-time information."""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_info)
        self.timer.start(2000)  # Update every 2 seconds
        self.update_info()  # Initial update
        
    def update_info(self):
        """Update status bar information."""
        # Memory usage
        memory = psutil.virtual_memory()
        self.memory_bar.setValue(int(memory.percent))
        self.memory_bar.setToolTip(f"RAM Usage: {memory.percent:.1f}%\\n"
                                  f"Used: {memory.used / (1024**3):.1f} GB\\n"
                                  f"Total: {memory.total / (1024**3):.1f} GB")
        
        # Update time
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.setText(current_time)
        
    def set_status_message(self, message, color="#00CED1"):
        """Set the main status message with optional color."""
        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"color: {color}; font-weight: bold;")
        
    def set_model_status(self, model_name, provider=""):
        """Update the model status display."""
        if provider:
            text = f"Model: {provider}:{model_name}"
        else:
            text = f"Model: {model_name}"
        self.model_status.setText(text)
        self.model_status.setToolTip(f"Active Model: {model_name}\\nProvider: {provider}")
        
    def set_connection_status(self, status):
        """Update connection status with color coding."""
        if status.lower() == "connected":
            self.connection_status.setText("🟢 Connected")
            self.connection_status.setStyleSheet("color: #00CED1;")
        elif status.lower() == "processing":
            self.connection_status.setText("🟡 Processing")
            self.connection_status.setStyleSheet("color: #FFD700;")
        elif status.lower() == "error":
            self.connection_status.setText("🔴 Error")
            self.connection_status.setStyleSheet("color: #FF6347;")
        else:
            self.connection_status.setText("⚫ Offline")
            self.connection_status.setStyleSheet("color: #808080;")
            
    def show_progress(self, message, progress=None):
        """Show a progress message with optional progress bar."""
        if progress is not None:
            self.set_status_message(f"{message} ({progress}%)", "#FFD700")
        else:
            self.set_status_message(message, "#FFD700")
            
    def show_success(self, message):
        """Show a success message briefly."""
        self.set_status_message(message, "#00CED1")
        # Reset to "Ready" after 3 seconds
        QTimer.singleShot(3000, lambda: self.set_status_message("Ready"))
        
    def show_error(self, message):
        """Show an error message briefly."""
        self.set_status_message(message, "#FF6347")
        # Reset to "Ready" after 5 seconds
        QTimer.singleShot(5000, lambda: self.set_status_message("Ready"))