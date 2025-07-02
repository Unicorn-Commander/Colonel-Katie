
import os
from PySide6.QtWidgets import QDialog, QFormLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QComboBox, QTabWidget, QWidget, QVBoxLayout, QFileDialog
from PySide6.QtCore import Qt, Signal
from services.settings_manager import SettingsManager

class SettingsDialog(QDialog):
    settings_saved = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings_manager = SettingsManager()
        self.setWindowTitle("Settings")
        self.setGeometry(200, 200, 500, 400)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint) # Remove help button

        self.layout = QVBoxLayout(self)
        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        self.models_tab = QWidget()
        self.rag_tab = QWidget()
        self.search_tab = QWidget()
        self.appearance_tab = QWidget()
        self.advanced_tab = QWidget()

        self.tab_widget.addTab(self.models_tab, "Models")
        self.tab_widget.addTab(self.rag_tab, "RAG")
        self.tab_widget.addTab(self.search_tab, "Search")
        self.tab_widget.addTab(self.appearance_tab, "Appearance")
        self.tab_widget.addTab(self.advanced_tab, "Advanced")

        # New Tabs
        self.auth_tab = QWidget()
        self.agent_management_tab = QWidget()
        self.global_shortcuts_tab = QWidget()
        self.directories_tab = QWidget()

        self.tab_widget.addTab(self.auth_tab, "Authentication")
        self.tab_widget.addTab(self.agent_management_tab, "Agent Management")
        self.tab_widget.addTab(self.global_shortcuts_tab, "Global Shortcuts")
        self.tab_widget.addTab(self.directories_tab, "Directories")

        self.models_layout = QFormLayout(self.models_tab)
        self.rag_layout = QFormLayout(self.rag_tab)
        self.search_layout = QFormLayout(self.search_tab)
        self.appearance_layout = QFormLayout(self.appearance_tab)
        self.advanced_layout = QFormLayout(self.advanced_tab)

        # New Layouts
        self.auth_layout = QFormLayout(self.auth_tab)
        self.agent_management_layout = QFormLayout(self.agent_management_tab)
        self.global_shortcuts_layout = QFormLayout(self.global_shortcuts_tab)
        self.directories_layout = QFormLayout(self.directories_tab)

        self.settings_fields = {}

        # Define settings and their types
        self.settings_config = {
            "OPENAI_API_KEY": {"type": "text", "label": "OpenAI API Key", "tab": "auth"},
            "ANTHROPIC_API_KEY": {"type": "text", "label": "Anthropic API Key", "tab": "auth"},
            "AUTH_TOKEN": {"type": "text", "label": "Auth Token", "tab": "auth"},
            "DEFAULT_PROFILE": {"type": "text", "label": "Default Profile", "tab": "agent_management"},
            "SERVER_HOST": {"type": "text", "label": "Server Host", "tab": "advanced"},
            "SERVER_PORT": {"type": "text", "label": "Server Port", "tab": "advanced"},
            "DISABLE_TELEMETRY": {"type": "bool", "label": "Disable Telemetry", "tab": "advanced"},
            "AUTO_RUN": {"type": "bool", "label": "Auto Run", "tab": "advanced"},
            "SAFE_MODE": {"type": "text", "label": "Safe Mode", "tab": "advanced"},
            "MEMORY_BACKEND": {"type": "combo", "label": "Memory Backend", "options": ["sqlite_chroma", "postgres_qdrant"], "tab": "rag"},
            "EMBEDDING_MODEL": {"type": "text", "label": "Embedding Model", "tab": "rag"},
            "CHUNK_SIZE": {"type": "text", "label": "Chunk Size", "tab": "rag"},
            "CHUNK_OVERLAP": {"type": "text", "label": "Chunk Overlap", "tab": "rag"},
            "SEARXNG_ENDPOINT": {"type": "text", "label": "SearXNG Endpoint", "tab": "search"},
            "DEFAULT_ENGINES": {"type": "text", "label": "Default Search Engines", "tab": "search"},
            "THEME": {"type": "combo", "label": "Theme", "options": ["dark", "light"], "tab": "appearance"},
            "FONT_SIZE": {"type": "text", "label": "Font Size", "tab": "appearance"},
            # Agent Management Placeholders
            "AGENT_TEMPLATES_PATH": {"type": "text", "label": "Agent Templates Path", "tab": "agent_management"},
            # Global Shortcuts Placeholders
            "GLOBAL_HOTKEY": {"type": "text", "label": "Global Hotkey", "tab": "global_shortcuts"},
            # Directories Placeholders
            "CACHE_DIRECTORY": {"type": "text", "label": "Cache Directory", "tab": "directories"},
            "LOG_DIRECTORY": {"type": "text", "label": "Log Directory", "tab": "directories"},
        }

        self.load_settings()
        self.create_ui()

    def create_ui(self):
        # Clear existing widgets from layouts if re-creating UI
        for i in reversed(range(self.models_layout.count())): self.models_layout.itemAt(i).widget().setParent(None)
        for i in reversed(range(self.rag_layout.count())): self.rag_layout.itemAt(i).widget().setParent(None)
        for i in reversed(range(self.search_layout.count())): self.search_layout.itemAt(i).widget().setParent(None)
        for i in reversed(range(self.appearance_layout.count())): self.appearance_layout.itemAt(i).widget().setParent(None)
        for i in reversed(range(self.advanced_layout.count())): self.advanced_layout.itemAt(i).widget().setParent(None)
        for i in reversed(range(self.auth_layout.count())): self.auth_layout.itemAt(i).widget().setParent(None)
        for i in reversed(range(self.agent_management_layout.count())): self.agent_management_layout.itemAt(i).widget().setParent(None)
        for i in reversed(range(self.global_shortcuts_layout.count())): self.global_shortcuts_layout.itemAt(i).widget().setParent(None)
        for i in reversed(range(self.directories_layout.count())): self.directories_layout.itemAt(i).widget().setParent(None)

        for key, config in self.settings_config.items():
            label = QLabel(config["label"] + ":")
            field = None
            if config["type"] == "text":
                field = QLineEdit(self)
                field.setText(self.settings_fields.get(key, ""))
            elif config["type"] == "bool":
                field = QCheckBox(self)
                field.setChecked(self.settings_fields.get(key, "false").lower() == "true")
            elif config["type"] == "combo":
                field = QComboBox(self)
                field.addItems(config["options"])
                current_value = self.settings_fields.get(key, config["options"][0])
                field.setCurrentText(current_value)
            
            if field:
                if config["tab"] == "models":
                    self.models_layout.addRow(label, field)
                elif config["tab"] == "rag":
                    self.rag_layout.addRow(label, field)
                elif config["tab"] == "search":
                    self.search_layout.addRow(label, field)
                elif config["tab"] == "appearance":
                    self.appearance_layout.addRow(label, field)
                elif config["tab"] == "advanced":
                    self.advanced_layout.addRow(label, field)
                elif config["tab"] == "auth":
                    self.auth_layout.addRow(label, field)
                elif config["tab"] == "agent_management":
                    self.agent_management_layout.addRow(label, field)
                elif config["tab"] == "global_shortcuts":
                    self.global_shortcuts_layout.addRow(label, field)
                elif config["tab"] == "directories":
                    self.directories_layout.addRow(label, field)
                self.settings_fields[key] = field # Store the actual widget

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)
        self.save_button.setToolTip("Save your settings.")
        self.layout.addWidget(self.save_button) # Add save button to the main layout, not individual tabs

        self.import_button = QPushButton("Import Settings")
        self.import_button.clicked.connect(self.import_settings_from_file)
        self.import_button.setToolTip("Import settings from a JSON file.")
        self.advanced_layout.addWidget(self.import_button)

        self.export_button = QPushButton("Export Settings")
        self.export_button.clicked.connect(self.export_settings_to_file)
        self.export_button.setToolTip("Export current settings to a JSON file.")
        self.advanced_layout.addWidget(self.export_button)

        # Pipeline Framework Placeholders
        self.pipeline_builder_label = QLabel("Pipeline Builder (Coming Soon)")
        self.advanced_layout.addWidget(self.pipeline_builder_label)

        self.pipeline_templates_label = QLabel("Pipeline Templates (Coming Soon)")
        self.advanced_layout.addWidget(self.pipeline_templates_label)

        self.pipeline_testing_label = QLabel("Pipeline Testing & Debugging (Coming Soon)")
        self.advanced_layout.addWidget(self.pipeline_testing_label)

        self.pipeline_marketplace_label = QLabel("Pipeline Marketplace (Coming Soon)")
        self.advanced_layout.addWidget(self.pipeline_marketplace_label)

        # Collaboration Features Placeholders
        self.collaboration_indicators_label = QLabel("Real-time Collaboration Indicators (Coming Soon)")
        self.advanced_layout.addWidget(self.collaboration_indicators_label)

        self.shared_spaces_label = QLabel("Shared Conversation Spaces (Coming Soon)")
        self.advanced_layout.addWidget(self.shared_spaces_label)

        self.user_tracking_label = QLabel("User Presence & Activity Tracking (Coming Soon)")
        self.advanced_layout.addWidget(self.user_tracking_label)

        self.access_control_label = QLabel("Conversation Permissions & Access Control (Coming Soon)")
        self.advanced_layout.addWidget(self.access_control_label)

        # UI/UX Polish Placeholders
        self.responsive_design_label = QLabel("Responsive Design (Coming Soon)")
        self.advanced_layout.addWidget(self.responsive_design_label)

        self.accessibility_label = QLabel("Accessibility & Usability (Coming Soon)")
        self.advanced_layout.addWidget(self.accessibility_label)

        self.performance_optimization_label = QLabel("Performance Optimization (Coming Soon)")
        self.advanced_layout.addWidget(self.performance_optimization_label)

    def load_settings(self):
        for key in self.settings_config.keys():
            self.settings_fields[key] = self.settings_manager.get_setting(key, "")

    def import_settings_from_file(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Import Settings", "", "JSON Files (*.json)")
        if file_path:
            if self.settings_manager.import_settings(file_path):
                self.load_settings() # Reload UI with imported settings
                self.create_ui() # Recreate UI to reflect changes
                self.parent().output_display.append("Settings imported successfully!")
            else:
                self.parent().output_display.append("Failed to import settings.")

    def export_settings_to_file(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getSaveFileName(self, "Export Settings", "settings.json", "JSON Files (*.json)")
        if file_path:
            if self.settings_manager.export_settings(file_path):
                self.parent().output_display.append("Settings exported successfully!")
            else:
                self.parent().output_display.append("Failed to export settings.")

    def save_settings(self):
        try:
            for key, config in self.settings_config.items():
                value = None
                if config["type"] == "text":
                    value = self.settings_fields[key].text()
                elif config["type"] == "bool":
                    value = str(self.settings_fields[key].isChecked()).lower()
                elif config["type"] == "combo":
                    value = self.settings_fields[key].currentText()
                
                if value is not None:
                    self.settings_manager.set_setting(key, value)
            
            self.parent().output_display.append("Settings saved successfully!")
            self.settings_saved.emit() # Emit signal that settings have been saved
            self.accept() # Close dialog
        except Exception as e:
            self.parent().output_display.append(f"Error saving settings: {e}")

