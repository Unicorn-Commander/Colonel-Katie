
from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import Signal, Qt
import os
import json

class ConversationHistory(QWidget):
    conversation_selected = Signal(str) # Emits the full path of the selected conversation file

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop) # Align content to the top

        self.label = QLabel("Conversation History")
        self.label.setObjectName("sidebarLabel") # For styling
        self.layout.addWidget(self.label)

        self.list_widget = QListWidget(self)
        self.list_widget.itemClicked.connect(self._on_item_clicked)
        self.layout.addWidget(self.list_widget)

        # Add a refresh button
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.load_conversations)
        self.layout.addWidget(self.refresh_button)

        self.conversations_path = os.path.join(os.path.expanduser("~/.open-interpreter"), "conversations")
        self.load_conversations()

    def load_conversations(self):
        self.list_widget.clear()
        
        if not os.path.exists(self.conversations_path):
            self.list_widget.addItem("No conversations found.")
            return

        for filename in os.listdir(self.conversations_path):
            if filename.endswith(".json"):
                # Display a more readable name
                display_name = filename.replace("__", " - ").replace(".json", "")
                self.list_widget.addItem(display_name)

    def _on_item_clicked(self, item):
        # Convert display name back to filename and emit full path
        filename = item.text().replace(" - ", "__") + ".json"
        full_path = os.path.join(self.conversations_path, filename)
        self.conversation_selected.emit(full_path)

    def get_selected_conversation(self):
        selected_items = self.list_widget.selectedItems()
        if selected_items:
            filename = selected_items[0].text().replace(" - ", "__") + ".json"
            return os.path.join(self.conversations_path, filename)
        return None
