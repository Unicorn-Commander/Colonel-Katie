
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QToolButton, QSizePolicy
from PySide6.QtCore import Qt, QPropertyAnimation, QRect, QSize
from PySide6.QtGui import QIcon
import os
from interpreter import interpreter

class CollapsibleSection(QWidget):
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.toggle_button = QToolButton(self)
        self.toggle_button.setStyleSheet("QToolButton { border: none; }")
        self.toggle_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(Qt.RightArrow)
        self.toggle_button.setText(title)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(False)

        self.content_area = QFrame(self)
        self.content_area.setMaximumHeight(0)
        self.content_area.setMinimumHeight(0)
        self.content_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.content_area.setStyleSheet("QFrame { background-color: #1A1A2E; border: none; }")

        self.toggle_button.clicked.connect(self.toggle_content)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.addWidget(self.toggle_button)
        self.main_layout.addWidget(self.content_area)

        self.animation = QPropertyAnimation(self.content_area, b"maximumHeight")
        self.animation.setDuration(300) # milliseconds

    def toggle_content(self):
        if self.toggle_button.isChecked():
            self.toggle_button.setArrowType(Qt.DownArrow)
            self.animation.setStartValue(self.content_area.height())
            self.animation.setEndValue(self.content_area.sizeHint().height())
        else:
            self.toggle_button.setArrowType(Qt.RightArrow)
            self.animation.setStartValue(self.content_area.height())
            self.animation.setEndValue(0)
        self.animation.start()

    def set_content_layout(self, layout):
        self.content_area.setLayout(layout)

class RightSidebar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop) # Align content to the top
        self.layout.setContentsMargins(5, 5, 5, 5)

        # Session Details Section
        self.session_details_section = CollapsibleSection("Session Details")
        self.session_details_layout = QVBoxLayout()
        self.session_details_layout.setContentsMargins(10, 5, 10, 5)
        self.session_details_layout.setSpacing(5)

        self.profile_label = QLabel("Profile: N/A")
        self.model_label = QLabel("Model: N/A")
        self.api_key_status_label = QLabel("API Key: Not Set")

        self.session_details_layout.addWidget(self.profile_label)
        self.session_details_layout.addWidget(self.model_label)
        self.session_details_layout.addWidget(self.api_key_status_label)

        self.session_details_section.set_content_layout(self.session_details_layout)
        self.layout.addWidget(self.session_details_section)

        # Memory Summary Section (Placeholder for now)
        self.memory_summary_section = CollapsibleSection("Memory Summary")
        self.memory_summary_layout = QVBoxLayout()
        self.memory_summary_layout.setContentsMargins(10, 5, 10, 5)
        self.memory_summary_layout.setSpacing(5)
        self.memory_summary_layout.addWidget(QLabel("Extracted memories will appear here."))
        self.memory_summary_section.set_content_layout(self.memory_summary_layout)
        self.layout.addWidget(self.memory_summary_section)

        # File Indexing Section
        self.file_indexing_section = CollapsibleSection("File Indexing")
        self.file_indexing_layout = QVBoxLayout()
        self.file_indexing_layout.setContentsMargins(10, 5, 10, 5)
        self.file_indexing_layout.setSpacing(5)

        self.index_button = QPushButton("Index Project Directory")
        self.index_button.setObjectName("indexButton") # For styling
        self.file_indexing_layout.addWidget(self.index_button)

        self.file_indexing_section.set_content_layout(self.file_indexing_layout)
        self.layout.addWidget(self.file_indexing_section)

        self.update_session_details()

    def update_session_details(self):
        # Update profile
        profile_name = os.getenv("DEFAULT_PROFILE", "default.yaml")
        self.profile_label.setText(f"Profile: {profile_name}")

        # Update LLM model
        self.model_label.setText(f"Model: {interpreter.llm.model}")

        # Update API Key Status
        api_key_set = bool(interpreter.llm.api_key)
        self.api_key_status_label.setText(f"API Key: {"Set" if api_key_set else "Not Set"}")

    def update_memory_summary(self, memories):
        # Clear existing memory summary
        for i in reversed(range(self.memory_summary_layout.count())):
            widget = self.memory_summary_layout.itemAt(i).widget()
            if widget is not None:
                self.memory_summary_layout.removeWidget(widget)
                widget.deleteLater()
        
        if memories:
            for memory in memories:
                self.memory_summary_layout.addWidget(QLabel(f"- {memory}"))
        else:
            self.memory_summary_layout.addWidget(QLabel("No extracted memories yet."))

        # Ensure the layout updates correctly after adding/removing widgets
        self.memory_summary_layout.update()
