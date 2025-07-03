from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QHBoxLayout, QCheckBox, QSpinBox, QTextEdit, QScrollArea, QWidget, QFileDialog
from PySide6.QtCore import Qt
import os

class AgentBuilderDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agent Builder")
        self.setGeometry(100, 100, 800, 600)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.create_general_settings_group()
        self.create_model_settings_group()
        self.create_interpreter_settings_group()
        self.create_custom_instructions_group()
        self.create_tool_selection_group()
        self.create_action_buttons()

    def create_general_settings_group(self):
        general_group_layout = QVBoxLayout()
        general_group_layout.addWidget(QLabel("<h3>General Settings</h3>"))

        # Agent Name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Agent Name:"))
        self.agent_name_edit = QLineEdit("MyCustomAgent")
        name_layout.addWidget(self.agent_name_edit)
        general_group_layout.addLayout(name_layout)

        # Profile Picture
        profile_pic_layout = QHBoxLayout()
        profile_pic_layout.addWidget(QLabel("Profile Picture:"))
        self.profile_pic_path_edit = QLineEdit()
        self.profile_pic_path_edit.setReadOnly(True)
        profile_pic_layout.addWidget(self.profile_pic_path_edit)
        self.profile_pic_button = QPushButton("Browse...")
        self.profile_pic_button.clicked.connect(self.select_profile_picture)
        profile_pic_layout.addWidget(self.profile_pic_button)
        general_group_layout.addLayout(profile_pic_layout)

        self.main_layout.addLayout(general_group_layout)

    def select_profile_picture(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.svg)")
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.profile_pic_path_edit.setText(selected_files[0])

    def create_model_settings_group(self):
        model_group_layout = QVBoxLayout()
        model_group_layout.addWidget(QLabel("<h3>LLM Settings</h3>"))

        # Model selection
        model_layout = QHBoxLayout()
        model_layout.addWidget(QLabel("Model:"))
        self.model_combo = QComboBox()
        self.model_combo.addItems(["groq/llama-3.1-70b-versatile", "openai/gpt-4o", "ollama/llama3"]) # Placeholder models
        model_layout.addWidget(self.model_combo)
        model_group_layout.addLayout(model_layout)

        # API Base
        api_base_layout = QHBoxLayout()
        api_base_layout.addWidget(QLabel("API Base:"))
        self.api_base_edit = QLineEdit("https://api.example.com")
        api_base_layout.addWidget(self.api_base_edit)
        model_group_layout.addLayout(api_base_layout)

        # API Key
        api_key_layout = QHBoxLayout()
        api_key_layout.addWidget(QLabel("API Key:"))
        self.api_key_edit = QLineEdit("your_api_key_here")
        api_key_layout.addWidget(self.api_key_edit)
        model_group_layout.addLayout(api_key_layout)

        # Context Window
        context_window_layout = QHBoxLayout()
        context_window_layout.addWidget(QLabel("Context Window:"))
        self.context_window_spin = QSpinBox()
        self.context_window_spin.setRange(1024, 200000)
        self.context_window_spin.setValue(110000)
        context_window_layout.addWidget(self.context_window_spin)
        model_group_layout.addLayout(context_window_layout)

        # Max Tokens
        max_tokens_layout = QHBoxLayout()
        max_tokens_layout.addWidget(QLabel("Max Tokens:"))
        self.max_tokens_spin = QSpinBox()
        self.max_tokens_spin.setRange(128, 8192)
        self.max_tokens_spin.setValue(4096)
        max_tokens_layout.addWidget(self.max_tokens_spin)
        model_group_layout.addLayout(max_tokens_layout)

        # Supports Functions/Vision
        self.supports_functions_checkbox = QCheckBox("Supports Functions")
        self.supports_functions_checkbox.setChecked(False)
        model_group_layout.addWidget(self.supports_functions_checkbox)

        self.supports_vision_checkbox = QCheckBox("Supports Vision")
        self.supports_vision_checkbox.setChecked(False)
        model_group_layout.addWidget(self.supports_vision_checkbox)

        self.main_layout.addLayout(model_group_layout)

    def create_interpreter_settings_group(self):
        interpreter_group_layout = QVBoxLayout()
        interpreter_group_layout.addWidget(QLabel("<h3>Interpreter Settings</h3>"))

        self.offline_checkbox = QCheckBox("Offline Mode")
        self.offline_checkbox.setChecked(False)
        interpreter_group_layout.addWidget(self.offline_checkbox)

        self.loop_checkbox = QCheckBox("Loop Mode")
        self.loop_checkbox.setChecked(True)
        interpreter_group_layout.addWidget(self.loop_checkbox)

        self.auto_run_checkbox = QCheckBox("Auto Run")
        self.auto_run_checkbox.setChecked(False)
        interpreter_group_layout.addWidget(self.auto_run_checkbox)

        self.os_mode_checkbox = QCheckBox("OS Mode")
        self.os_mode_checkbox.setChecked(False)
        interpreter_group_layout.addWidget(self.os_mode_checkbox)

        self.import_computer_api_checkbox = QCheckBox("Import Computer API")
        self.import_computer_api_checkbox.setChecked(True)
        interpreter_group_layout.addWidget(self.import_computer_api_checkbox)

        self.main_layout.addLayout(interpreter_group_layout)

    def create_custom_instructions_group(self):
        instructions_group_layout = QVBoxLayout()
        instructions_group_layout.addWidget(QLabel("<h3>System Prompt / Custom Instructions</h3>"))

        self.system_prompt_edit = QTextEdit()
        self.system_prompt_edit.setPlaceholderText("Enter the system prompt for the agent...")
        self.system_prompt_edit.setPlainText("You are a helpful AI assistant.") # Default system prompt
        instructions_group_layout.addWidget(self.system_prompt_edit)

        self.custom_instructions_edit = QTextEdit()
        self.custom_instructions_edit.setPlaceholderText("Enter additional custom instructions for the agent...")
        instructions_group_layout.addWidget(self.custom_instructions_edit)

        self.main_layout.addLayout(instructions_group_layout)

    def create_tool_selection_group(self):
        tool_group_layout = QVBoxLayout()
        tool_group_layout.addWidget(QLabel("<h3>Tools & Capabilities</h3>"))

        self.shell_tool_checkbox = QCheckBox("Shell Tool")
        self.shell_tool_checkbox.setChecked(True) # Default to enabled
        tool_group_layout.addWidget(self.shell_tool_checkbox)

        self.browser_tool_checkbox = QCheckBox("Browser Tool")
        self.browser_tool_checkbox.setChecked(False)
        tool_group_layout.addWidget(self.browser_tool_checkbox)

        self.files_tool_checkbox = QCheckBox("Files Tool")
        self.files_tool_checkbox.setChecked(True) # Default to enabled
        tool_group_layout.addWidget(self.files_tool_checkbox)

        self.main_layout.addLayout(tool_group_layout)

    def create_action_buttons(self):
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save Agent Profile")
        self.cancel_button = QPushButton("Cancel")

        self.save_button.clicked.connect(self.save_agent_profile)
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addStretch()

        self.main_layout.addLayout(button_layout)

    def save_agent_profile(self):
        # Collect data from UI elements
        agent_name = self.agent_name_edit.text()
        profile_pic_path = self.profile_pic_path_edit.text()
        system_prompt = self.system_prompt_edit.toPlainText()

        model = self.model_combo.currentText()
        api_base = self.api_base_edit.text()
        api_key = self.api_key_edit.text()
        context_window = self.context_window_spin.value()
        max_tokens = self.max_tokens_spin.value()
        supports_functions = self.supports_functions_checkbox.isChecked()
        supports_vision = self.supports_vision_checkbox.isChecked()

        offline = self.offline_checkbox.isChecked()
        loop = self.loop_checkbox.isChecked()
        auto_run = self.auto_run_checkbox.isChecked()
        os_mode = self.os_mode_checkbox.isChecked()
        import_computer_api = self.import_computer_api_checkbox.isChecked()

        custom_instructions = self.custom_instructions_edit.toPlainText()

        # Collect selected tools
        selected_tools = []
        if self.shell_tool_checkbox.isChecked():
            selected_tools.append("shell")
        if self.browser_tool_checkbox.isChecked():
            selected_tools.append("browser")
        if self.files_tool_checkbox.isChecked():
            selected_tools.append("files")

        # Generate Python file content
        profile_content = f'''"""This is a custom generated Open Interpreter profile.
"""

# Import the interpreter
from interpreter import interpreter

# You can import other libraries too
from datetime import date

# You can set variables
today = date.today()

# Agent Metadata
interpreter.agent_name = "{agent_name}"
interpreter.profile_picture = "{profile_pic_path}"

# System Prompt
interpreter.system_prompt = f"""\
    {system_prompt.replace('"' , '\'')}
    """

# LLM Settings
interpreter.llm.model = "{model}"
interpreter.llm.context_window = {context_window}
interpreter.llm.max_tokens = {max_tokens}
interpreter.llm.api_base = "{api_base}"
interpreter.llm.api_key = "{api_key}"
interpreter.llm.supports_functions = {supports_functions}
interpreter.llm.supports_vision = {supports_vision}


# Interpreter Settings
interpreter.offline = {offline}
interpreter.loop = {loop}
interpreter.auto_run = {auto_run}

# Toggle OS Mode - https://docs.openinterpreter.com/guides/os-mode
interpreter.os = {os_mode}

# Import Computer API - https://docs.openinterpreter.com/code-execution/computer-api
interpreter.computer.import_computer_api = {import_computer_api}

# Tools
interpreter.tools = {selected_tools}

# Set Custom Instructions to improve your Interpreter\'s performance at a given task
interpreter.custom_instructions = f"""\
    {custom_instructions.replace('"' , '\'')}
    """
'''

        # Determine file path
        profiles_dir = "/home/ucadmin/Development/Colonel-Katie/interpreter/terminal_interface/profiles/custom"
        os.makedirs(profiles_dir, exist_ok=True)
        file_path = os.path.join(profiles_dir, f"{agent_name.replace(' ', '_').lower()}.py")

        # Save the file
        try:
            with open(file_path, "w") as f:
                f.write(profile_content)
            print(f"Agent profile saved to {file_path}")
            self.accept() # Close dialog on success
        except Exception as e:
            print(f"Error saving agent profile: {e}")

if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    dialog = AgentBuilderDialog()
    dialog.exec()
    sys.exit(app.exec())