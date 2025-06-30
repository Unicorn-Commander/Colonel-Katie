
import os
from PySide6.QtWidgets import QDialog, QFormLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QComboBox
from PySide6.QtCore import Qt, Signal
from dotenv import set_key, load_dotenv
from interpreter import interpreter
from interpreter.memory import MemoryManager # Import the MemoryManager

load_dotenv()

class SettingsDialog(QDialog):
    settings_saved = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setGeometry(200, 200, 500, 400)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint) # Remove help button

        self.layout = QFormLayout(self)
        self.settings_fields = {}

        # Define settings and their types
        self.settings_config = {
            "OPENAI_API_KEY": {"type": "text", "label": "OpenAI API Key"},
            "ANTHROPIC_API_KEY": {"type": "text", "label": "Anthropic API Key"},
            "DEFAULT_PROFILE": {"type": "text", "label": "Default Profile"},
            "SERVER_HOST": {"type": "text", "label": "Server Host"},
            "SERVER_PORT": {"type": "text", "label": "Server Port"},
            "AUTH_TOKEN": {"type": "text", "label": "Auth Token"},
            "DISABLE_TELEMETRY": {"type": "bool", "label": "Disable Telemetry"},
            "AUTO_RUN": {"type": "bool", "label": "Auto Run"},
            "SAFE_MODE": {"type": "text", "label": "Safe Mode"},
            "MEMORY_BACKEND": {"type": "combo", "label": "Memory Backend", "options": ["sqlite_chroma", "postgres_qdrant"]},
        }

        self.load_settings()
        self.create_ui()

    def create_ui(self):
        for key, config in self.settings_config.items():
            label = QLabel(config["label"] + ":")
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
            
            self.layout.addRow(label, field)
            self.settings_fields[key] = field # Store the actual widget

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)
        self.layout.addRow(self.save_button)

    def load_settings(self):
        for key in self.settings_config.keys():
            self.settings_fields[key] = os.getenv(key, "")

    def save_settings(self):
        try:
            for key, config in self.settings_config.items():
                if config["type"] == "text":
                    value = self.settings_fields[key].text()
                elif config["type"] == "bool":
                    value = str(self.settings_fields[key].isChecked()).lower()
                elif config["type"] == "combo":
                    value = self.settings_fields[key].currentText()
                
                # Update .env file
                set_key(os.getenv("DOTENV_PATH", ".env"), key, value)
            
            # Re-initialize interpreter with new settings, especially for memory backend
            # This is a simplified approach; a more robust solution might involve
            # restarting the interpreter or dynamically updating its components.
            # For now, we'll just re-create the interpreter instance.
            # Note: This might clear conversation history if not handled carefully.
            # We'll address conversation history persistence in a later step.
            
            # Update interpreter's memory backend
            interpreter.memory = MemoryManager(backend=os.getenv("MEMORY_BACKEND", "sqlite_chroma"))

            self.parent().output_display.append("Settings saved successfully!")
            self.settings_saved.emit() # Emit signal that settings have been saved
            self.accept() # Close dialog
        except Exception as e:
            self.parent().output_display.append(f"Error saving settings: {e}")

