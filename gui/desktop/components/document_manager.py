from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QPushButton, QLineEdit, QTextEdit, QFileDialog, QMessageBox
from PySide6.QtCore import Qt, Signal
import os

class DocumentManager(QWidget):
    document_selected = Signal(str) # Emits document ID

    def __init__(self, document_storage_service, rag_manager, parent=None):
        super().__init__(parent)
        self.document_storage_service = document_storage_service
        self.rag_manager = rag_manager
        self.current_agent_id = "default_agent" # Placeholder for active agent

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)

        # Header
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("<b>Document Library</b>"))
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.load_documents)
        header_layout.addWidget(self.refresh_button)
        self.layout.addLayout(header_layout)

        # Document List
        self.document_list_widget = QListWidget()
        self.document_list_widget.itemClicked.connect(self.on_document_selected)
        self.layout.addWidget(self.document_list_widget)

        # Document Preview
        self.preview_label = QLabel("Document Preview:")
        self.layout.addWidget(self.preview_label)
        self.document_preview_text = QTextEdit()
        self.document_preview_text.setReadOnly(True)
        self.document_preview_text.setPlaceholderText("Select a document to preview.")
        self.layout.addWidget(self.document_preview_text)

        # Search Input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search documents...")
        self.search_input.textChanged.connect(self.filter_documents)
        self.layout.addWidget(self.search_input)

        # Bulk Operations (Placeholders)
        bulk_ops_layout = QHBoxLayout()
        self.delete_selected_button = QPushButton("Delete Selected")
        self.delete_selected_button.clicked.connect(self.delete_selected_documents)
        bulk_ops_layout.addWidget(self.delete_selected_button)

        self.move_selected_button = QPushButton("Move Selected")
        self.move_selected_button.clicked.connect(self.move_selected_documents)
        bulk_ops_layout.addWidget(self.move_selected_button)

        self.share_selected_button = QPushButton("Share Selected")
        self.share_selected_button.clicked.connect(self.share_selected_documents)
        bulk_ops_layout.addWidget(self.share_selected_button)
        self.layout.addLayout(bulk_ops_layout)

        self.load_documents()

    def load_documents(self):
        self.document_list_widget.clear()
        documents = self.document_storage_service.list_documents_for_agent(self.current_agent_id)
        for doc in documents:
            item = QListWidgetItem(f"{doc['filename']} ({doc['file_type']})")
            item.setData(Qt.UserRole, doc['id']) # Store document ID in UserRole
            self.document_list_widget.addItem(item)

    def on_document_selected(self, item):
        doc_id = item.data(Qt.UserRole)
        doc_metadata = self.document_storage_service.get_document_metadata(doc_id)
        if doc_metadata:
            file_path = doc_metadata['filepath']
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read(1000) # Read first 1000 characters for preview
                    self.document_preview_text.setText(content)
            except Exception as e:
                self.document_preview_text.setText(f"Could not preview file: {e}")
        self.document_selected.emit(doc_id)

    def filter_documents(self, search_text):
        for i in range(self.document_list_widget.count()):
            item = self.document_list_widget.item(i)
            if search_text.lower() in item.text().lower():
                item.setHidden(False)
            else:
                item.setHidden(True)

    def delete_selected_documents(self):
        selected_items = self.document_list_widget.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "No Selection", "Please select documents to delete.")
            return

        reply = QMessageBox.question(self, "Confirm Delete",
                                     "Are you sure you want to delete the selected documents? This cannot be undone.",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            for item in selected_items:
                doc_id = item.data(Qt.UserRole)
                doc_metadata = self.document_storage_service.get_document_metadata(doc_id)
                if doc_metadata:
                    # Delete from RAG (ChromaDB)
                    self.rag_manager.active_collection.delete(ids=[doc_id]) # Assuming doc_id is used as ChromaDB ID
                    # Delete from SQLite metadata
                    self.document_storage_service.delete_document_metadata(doc_id)
                    # Delete physical file (optional, based on user preference)
                    # os.remove(doc_metadata['filepath'])
            self.load_documents() # Refresh list
            QMessageBox.information(self, "Delete Complete", "Selected documents deleted.")

    def move_selected_documents(self):
        QMessageBox.information(self, "Coming Soon", "Move documents functionality is coming soon!")

    def share_selected_documents(self):
        QMessageBox.information(self, "Coming Soon", "Share documents functionality is coming soon!")
