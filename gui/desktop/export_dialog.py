from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QRadioButton, QGroupBox, QFileDialog, QLabel, QLineEdit, QCheckBox
from PySide6.QtCore import Qt
import os

class ExportDialog(QDialog):
    def __init__(self, chat_manager, parent=None):
        super().__init__(parent)
        self.chat_manager = chat_manager
        self.setWindowTitle("Export Conversation")
        self.setMinimumWidth(400)

        self.layout = QVBoxLayout(self)

        # Export Format Selection
        format_group = QGroupBox("Export Format")
        format_layout = QVBoxLayout()
        self.json_radio = QRadioButton("JSON")
        self.markdown_radio = QRadioButton("Markdown")
        self.pdf_radio = QRadioButton("PDF (Coming Soon)")
        self.pdf_radio.setEnabled(False) # PDF export is a stretch goal
        
        self.json_radio.setChecked(True) # Default selection

        format_layout.addWidget(self.json_radio)
        format_layout.addWidget(self.markdown_radio)
        format_layout.addWidget(self.pdf_radio)
        format_group.setLayout(format_layout)
        self.layout.addWidget(format_group)

        # Export Scope
        scope_group = QGroupBox("Export Scope")
        scope_layout = QVBoxLayout()
        self.current_conversation_radio = QRadioButton("Current Conversation")
        self.all_conversations_radio = QRadioButton("All Conversations (Bulk Export)")
        
        self.current_conversation_radio.setChecked(True) # Default selection

        scope_layout.addWidget(self.current_conversation_radio)
        scope_layout.addWidget(self.all_conversations_radio)
        scope_group.setLayout(scope_layout)
        self.layout.addWidget(scope_group)

        # Output File/Directory
        output_layout = QHBoxLayout()
        self.output_label = QLabel("Output Path:")
        self.output_path_edit = QLineEdit()
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_output_path)

        output_layout.addWidget(self.output_label)
        output_layout.addWidget(self.output_path_edit)
        output_layout.addWidget(self.browse_button)
        self.layout.addLayout(output_layout)

        # Options (Metadata, Timestamps)
        options_group = QGroupBox("Options")
        options_layout = QVBoxLayout()
        self.include_metadata_checkbox = QCheckBox("Include Metadata")
        self.include_timestamps_checkbox = QCheckBox("Include Timestamps")
        
        self.include_metadata_checkbox.setChecked(True)
        self.include_timestamps_checkbox.setChecked(True)

        options_layout.addWidget(self.include_metadata_checkbox)
        options_layout.addWidget(self.include_timestamps_checkbox)
        options_group.setLayout(options_layout)
        self.layout.addWidget(options_group)

        # Action Buttons
        button_layout = QHBoxLayout()
        self.export_button = QPushButton("Export")
        self.export_button.clicked.connect(self.accept) # Accept dialog on export
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject) # Reject dialog on cancel

        button_layout.addStretch()
        button_layout.addWidget(self.export_button)
        button_layout.addWidget(self.cancel_button)
        self.layout.addLayout(button_layout)

        self.update_output_path_placeholder()
        self.current_conversation_radio.toggled.connect(self.update_output_path_placeholder)
        self.all_conversations_radio.toggled.connect(self.update_output_path_placeholder)
        self.json_radio.toggled.connect(self.update_output_path_placeholder)
        self.markdown_radio.toggled.connect(self.update_output_path_placeholder)

    def update_output_path_placeholder(self):
        if self.all_conversations_radio.isChecked():
            self.output_path_edit.setPlaceholderText("Select output directory...")
        else:
            if self.json_radio.isChecked():
                self.output_path_edit.setPlaceholderText("conversation.json")
            elif self.markdown_radio.isChecked():
                self.output_path_edit.setPlaceholderText("conversation.md")
            elif self.pdf_radio.isChecked():
                self.output_path_edit.setPlaceholderText("conversation.pdf")

    def browse_output_path(self):
        if self.all_conversations_radio.isChecked():
            directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
            if directory:
                self.output_path_edit.setText(directory)
        else:
            if self.json_radio.isChecked():
                file_name, _ = QFileDialog.getSaveFileName(self, "Save Conversation", "conversation.json", "JSON Files (*.json)")
            elif self.markdown_radio.isChecked():
                file_name, _ = QFileDialog.getSaveFileName(self, "Save Conversation", "conversation.md", "Markdown Files (*.md)")
            elif self.pdf_radio.isChecked():
                file_name, _ = QFileDialog.getSaveFileName(self, "Save Conversation", "conversation.pdf", "PDF Files (*.pdf)")
            else:
                file_name = "" # Should not happen

            if file_name:
                self.output_path_edit.setText(file_name)

    def get_export_options(self):
        return {
            "format": "json" if self.json_radio.isChecked() else ("markdown" if self.markdown_radio.isChecked() else "pdf"),
            "scope": "current" if self.current_conversation_radio.isChecked() else "all",
            "output_path": self.output_path_edit.text(),
            "include_metadata": self.include_metadata_checkbox.isChecked(),
            "include_timestamps": self.include_timestamps_checkbox.isChecked()
        }
