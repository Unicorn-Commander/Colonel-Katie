from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QTextEdit, QLabel, QComboBox, QPushButton, QListWidget
from PySide6.QtCore import Qt, QPoint, QSize, QScreen
from PySide6.QtGui import QKeyEvent

from .quick_settings import QuickSettings

class QuickChatWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.quick_settings = QuickSettings()
        self._load_geometry()

        self.layout = QVBoxLayout(self)
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Ask The Colonel...")
        self.layout.addWidget(self.input_field)

        self.display_area = QTextEdit(self)
        self.display_area.setReadOnly(True)
        self.layout.addWidget(self.display_area)

        self.model_switcher = QComboBox(self)
        self.model_switcher.setPlaceholderText("Select Model")
        self.layout.addWidget(self.model_switcher)

        self.open_main_app_button = QPushButton("Open in Main App")
        self.layout.addWidget(self.open_main_app_button)

        self.recent_conversations_label = QLabel("Recent Conversations:")
        self.layout.addWidget(self.recent_conversations_label)

        self.recent_conversations_list = QListWidget(self)
        self.recent_conversations_list.setPlaceholderText("No recent conversations.")
        self.layout.addWidget(self.recent_conversations_list)

        self.input_field.installEventFilter(self) # To capture focus out event

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Escape:
            self.hide()
            event.accept()
        else:
            super().keyPressEvent(event)

    def focusOutEvent(self, event):
        self.hide()
        super().focusOutEvent(event)

    def _load_geometry(self):
        pos_setting = self.quick_settings.get_setting("window_position", {"x": 100, "y": 100})
        size_setting = self.quick_settings.get_setting("window_size", {"width": 400, "height": 300})
        position_type = self.quick_settings.get_setting("position_type", "last")

        self.resize(QSize(size_setting["width"], size_setting["height"]))

        if position_type == "center":
            screen = QApplication.primaryScreen().geometry()
            x = (screen.width() - self.width()) // 2
            y = (screen.height() - self.height()) // 2
            self.move(QPoint(x, y))
        elif position_type == "top-left":
            self.move(QPoint(0, 0))
        elif position_type == "top-right":
            screen = QApplication.primaryScreen().geometry()
            x = screen.width() - self.width()
            self.move(QPoint(x, 0))
        elif position_type == "bottom-left":
            screen = QApplication.primaryScreen().geometry()
            y = screen.height() - self.height()
            self.move(QPoint(0, y))
        elif position_type == "bottom-right":
            screen = QApplication.primaryScreen().geometry()
            x = screen.width() - self.width()
            y = screen.height() - self.height()
            self.move(QPoint(x, y))
        else: # "last" or any other value
            self.move(QPoint(pos_setting["x"], pos_setting["y"]))

    def _save_geometry(self):
        self.quick_settings.set_setting("window_position", {"x": self.pos().x(), "y": self.pos().y()})
        self.quick_settings.set_setting("window_size", {"width": self.size().width(), "height": self.size().height()})
        # self.quick_settings.set_setting("position_type", "last") # Save current position as last

    def hideEvent(self, event):
        self._save_geometry()
        super().hideEvent(event)

    def set_position_type(self, position_type):
        self.quick_settings.set_setting("position_type", position_type)
        self._load_geometry() # Apply new position immediately

    def populate_recent_conversations(self, conversations):
        self.recent_conversations_list.clear()
        for conv_id, conv_data in conversations.items():
            # Assuming conv_data has a 'title' or first message to display
            display_text = f"Conversation {conv_id[:8]}..."
            if conv_data["messages"]:
                first_msg = conv_data["messages"][0]["content"]
                display_text = f"{first_msg[:30]}... (ID: {conv_id[:8]}...)"
            self.recent_conversations_list.addItem(display_text)
