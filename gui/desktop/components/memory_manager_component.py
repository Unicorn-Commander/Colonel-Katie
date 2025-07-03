from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QPushButton, QLineEdit, QTextEdit, QDialog, QMessageBox
from PySide6.QtCore import Qt, Signal
import json

class MemoryManagerComponent(QWidget):
    def __init__(self, memory_service, parent=None):
        super().__init__(parent)
        self.memory_service = memory_service

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)

        # Header
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("<b>Memory Management</b>"))
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.load_memories)
        header_layout.addWidget(self.refresh_button)
        self.layout.addLayout(header_layout)

        # Search Input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search memories...")
        self.search_input.textChanged.connect(self.filter_memories)
        self.layout.addWidget(self.search_input)

        # Memory List
        self.memory_list_widget = QListWidget()
        self.memory_list_widget.itemClicked.connect(self.on_memory_selected)
        self.layout.addWidget(self.memory_list_widget)

        # Memory Details/Edit
        self.memory_details_label = QLabel("Memory Details:")
        self.layout.addWidget(self.memory_details_label)
        self.memory_details_text = QTextEdit()
        self.memory_details_text.setReadOnly(False) # Allow editing
        self.layout.addWidget(self.memory_details_text)

        edit_buttons_layout = QHBoxLayout()
        self.save_edit_button = QPushButton("Save Edit")
        self.save_edit_button.clicked.connect(self.save_memory_edit)
        edit_buttons_layout.addWidget(self.save_edit_button)

        self.delete_memory_button = QPushButton("Delete Memory")
        self.delete_memory_button.clicked.connect(self.delete_selected_memory)
        edit_buttons_layout.addWidget(self.delete_memory_button)
        self.layout.addLayout(edit_buttons_layout)

        # Import/Export Buttons
        io_buttons_layout = QHBoxLayout()
        self.import_button = QPushButton("Import Memories")
        self.import_button.clicked.connect(self.import_memories)
        io_buttons_layout.addWidget(self.import_button)

        self.export_button = QPushButton("Export Memories")
        self.export_button.clicked.connect(self.export_memories)
        io_buttons_layout.addWidget(self.export_button)
        self.layout.addLayout(io_buttons_layout)

        self.load_memories()

    def load_memories(self):
        self.memory_list_widget.clear()
        # Fetch all memories (simple query for now)
        memories = self.memory_service.get_memories(query="") 
        self.all_memories = memories # Store for filtering
        self._display_memories(memories)

    def _display_memories(self, memories_to_display):
        self.memory_list_widget.clear()
        for mem in memories_to_display:
            item = QListWidgetItem(f"[{mem.get('timestamp', 'N/A')}] {mem.get('data', '')[:50]}...")
            item.setData(Qt.UserRole, mem['id']) # Store memory ID
            self.memory_list_widget.addItem(item)

    def filter_memories(self, search_text):
        filtered_memories = [mem for mem in self.all_memories if search_text.lower() in mem.get('data', '').lower()]
        self._display_memories(filtered_memories)

    def on_memory_selected(self, item):
        mem_id = item.data(Qt.UserRole)
        selected_memory = next((mem for mem in self.all_memories if mem['id'] == mem_id), None)
        if selected_memory:
            self.memory_details_text.setPlainText(selected_memory.get('data', ''))
            self.memory_details_text.setProperty("current_memory_id", mem_id) # Store ID for saving edits

    def save_memory_edit(self):
        mem_id = self.memory_details_text.property("current_memory_id")
        if mem_id:
            new_data = self.memory_details_text.toPlainText()
            # Find the original metadata
            original_memory = next((mem for mem in self.all_memories if mem['id'] == mem_id), None)
            if original_memory:
                new_metadata = original_memory.get('metadata')
                self.memory_service.update_memory(mem_id, new_data, new_metadata)
                QMessageBox.information(self, "Success", "Memory updated successfully.")
                self.load_memories()
            else:
                QMessageBox.warning(self, "Error", "Original memory not found.")
        else:
            QMessageBox.warning(self, "Error", "No memory selected for editing.")

    def delete_selected_memory(self):
        mem_id = self.memory_details_text.property("current_memory_id")
        if mem_id:
            reply = QMessageBox.question(self, "Confirm Delete",
                                         "Are you sure you want to delete this memory?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.memory_service.delete_memory(mem_id)
                QMessageBox.information(self, "Success", "Memory deleted successfully.")
                self.memory_details_text.clear()
                self.memory_details_text.setProperty("current_memory_id", None)
                self.load_memories()
        else:
            QMessageBox.warning(self, "Error", "No memory selected for deletion.")

    def import_memories(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Import Memories", "", "JSON Files (*.json)")
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    memories_to_import = json.load(f)
                for mem_data in memories_to_import:
                    self.memory_service.add_memory(mem_data.get('data'), mem_data.get('metadata'))
                QMessageBox.information(self, "Success", f"{len(memories_to_import)} memories imported.")
                self.load_memories()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to import memories: {e}")

    def export_memories(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getSaveFileName(self, "Export Memories", "memories.json", "JSON Files (*.json)")
        if file_path:
            try:
                memories_to_export = self.memory_service.get_memories(query="", limit=10000) # Export all
                with open(file_path, 'w') as f:
                    json.dump(memories_to_export, f, indent=4)
                QMessageBox.information(self, "Success", f"{len(memories_to_export)} memories exported.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export memories: {e}")
