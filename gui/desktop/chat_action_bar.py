from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSizePolicy
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

class ChatActionBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        # Files Button
        self.files_button = QPushButton(QIcon.fromTheme("document-open"), "")
        self.files_button.setObjectName("chatActionButton")
        self.files_button.setToolTip("Attach Files (documents, images)")
        self.layout.addWidget(self.files_button)

        # Web Search Button
        self.web_search_button = QPushButton(QIcon.fromTheme("system-search"), "")
        self.web_search_button.setObjectName("chatActionButton")
        self.web_search_button.setToolTip("Toggle Web Search")
        self.layout.addWidget(self.web_search_button)

        # RAG Knowledge Button
        self.rag_button = QPushButton(QIcon.fromTheme("folder-saved-search"), "")
        self.rag_button.setObjectName("chatActionButton")
        self.rag_button.setToolTip("Toggle RAG Knowledge")
        self.layout.addWidget(self.rag_button)

        # Voice Input Button
        self.voice_input_button = QPushButton(QIcon.fromTheme("audio-input-microphone"), "")
        self.voice_input_button.setObjectName("chatActionButton")
        self.voice_input_button.setToolTip("Voice Input (STT)")
        self.layout.addWidget(self.voice_input_button)

        # Voice Output Button
        self.voice_output_button = QPushButton(QIcon.fromTheme("audio-volume-high"), "")
        self.voice_output_button.setObjectName("chatActionButton")
        self.voice_output_button.setToolTip("Voice Output (TTS)")
        self.layout.addWidget(self.voice_output_button)

        # Quick Settings Button
        self.quick_settings_button = QPushButton(QIcon.fromTheme("preferences-system"), "")
        self.quick_settings_button.setObjectName("chatActionButton")
        self.quick_settings_button.setToolTip("Quick Settings (temperature, model)")
        self.layout.addWidget(self.quick_settings_button)

        # Export Chat Button
        self.export_chat_button = QPushButton(QIcon.fromTheme("document-save"), "")
        self.export_chat_button.setObjectName("chatActionButton")
        self.export_chat_button.setToolTip("Export Chat (JSON, MD, PDF)")
        self.layout.addWidget(self.export_chat_button)

        # Regenerate Response Button
        self.regenerate_button = QPushButton(QIcon.fromTheme("view-refresh"), "")
        self.regenerate_button.setObjectName("chatActionButton")
        self.regenerate_button.setToolTip("Regenerate Response")
        self.layout.addWidget(self.regenerate_button)

        self.layout.addStretch() # Push buttons to the left
