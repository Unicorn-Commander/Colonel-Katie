from PySide6.QtWidgets import QSplashScreen, QProgressBar, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap, QFont, QColor
from PySide6.QtCore import Qt, QTimer

class SplashScreen(QSplashScreen):
    def __init__(self, pixmap, parent=None):
        super().__init__(pixmap)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #8A2BE2;
                border-radius: 5px;
                background-color: #1A1A2E;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #00CED1;
                width: 20px;
            }
        """)
        self.layout.addWidget(self.progress_bar)

        self.message_label = QLabel("Loading modules...")
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setStyleSheet("color: white; font-weight: bold;")
        self.layout.addWidget(self.message_label)

        self.setFont(QFont("Inter", 10))

    def set_progress(self, value, message):
        self.progress_bar.setValue(value)
        self.message_label.setText(message)
        self.repaint() # Force repaint to update message
