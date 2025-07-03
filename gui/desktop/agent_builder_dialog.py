from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QHBoxLayout, QCheckBox, QSpinBox, QTextEdit, QScrollArea, QWidget, QFileDialog, QInputDialog, QMessageBox
from PySide6.QtCore import Qt
import os
from interpreter.core.config_manager import ConfigManager
from .services.prompt_library import PromptLibrary

class AgentBuilderDialog(QDialog):
    def __init__(self, tts_service, config_manager, parent=None):
        super().__init__(parent)
        self.tts_service = tts_service
        self.config_manager = config_manager
        self.prompt_library = PromptLibrary()
        self.setWindowTitle("Agent Builder")
        self.setGeometry(100, 100, 800, 600)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.create_general_settings_group()
        self.create_model_settings_group()
        self.create_voice_settings_group()
        self.create_interpreter_settings_group()
        self.create_custom_instructions_group()
        self.create_tool_selection_group()
        self.create_published_prompts_group() # New: Published Prompts
        self.create_workflow_settings_group() # New: Workflow settings
        self.create_action_buttons()

    def create_general_settings_group(self):
        general_group_layout = QVBoxLayout()
        general_group_layout.addWidget(QLabel("<h3>General Settings</h3>"))

        # Agent Name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Agent Name:"))
        self.agent_name_edit = QLineEdit("MyCustomAgent")
        self.agent_name_edit.setToolTip("Choose a unique name for your AI agent (used as filename for the .py profile)")
        name_layout.addWidget(self.agent_name_edit)
        general_group_layout.addLayout(name_layout)

        # Profile Picture
        profile_pic_layout = QHBoxLayout()
        profile_pic_layout.addWidget(QLabel("Profile Picture:"))
        self.profile_pic_path_edit = QLineEdit()
        self.profile_pic_path_edit.setReadOnly(True)
        profile_pic_layout.addWidget(self.profile_pic_path_edit)
        self.profile_pic_button = QPushButton("Browse...")
        self.profile_pic_button.setToolTip("Select an image file (PNG, JPG, JPEG, SVG) for your agent's avatar")
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

    def populate_model_combo(self):
        # This will eventually load from a config file or API
        self.available_models = {
            "Groq": ["llama-3.1-70b-versatile", "mixtral-8x7b-32768"],
            "OpenAI": ["gpt-4o", "gpt-3.5-turbo"],
            "Ollama": ["llama3", "mistral"],
        }
        custom_models = self.config_manager.get("llm.custom_models", {})
        for provider, models in custom_models.items():
            if provider not in self.available_models:
                self.available_models[provider] = []
            self.available_models[provider].extend(models)
        self.model_combo.clear()
        for provider, models in self.available_models.items():
            for model in models:
                self.model_combo.addItem(f"{provider}: {model}")

    def filter_models(self, text):
        self.model_combo.clear()
        search_text = text.lower()
        for provider, models in self.available_models.items():
            for model in models:
                if search_text in model.lower() or search_text in provider.lower():
                    self.model_combo.addItem(f"{provider}: {model}")

    def add_custom_model(self):
        # This will open a new dialog for adding custom model details
        # For now, just a placeholder
        model_name, ok = QInputDialog.getText(self, "Add Custom Model", "Enter model name (e.g., MyLocalModel):")
        if ok and model_name:
            api_base, ok_api = QInputDialog.getText(self, "Add Custom Model", "Enter API Base URL:")
            if ok_api and api_base:
                api_key, ok_key = QInputDialog.getText(self, "Add Custom Model", "Enter API Key (optional):")
                if ok_key:
                    custom_models = self.config_manager.get("llm.custom_models", {})
                    if provider not in custom_models:
                        custom_models[provider] = []
                    custom_models[provider].append(model_name)
                    self.config_manager.set("llm.custom_models", custom_models)
                    self.populate_model_combo()
                    # Select the newly added model
                    self.model_combo.setCurrentText(f"{provider}: {model_name}")
                    self.api_base_edit.setText(api_base)
                    self.api_key_edit.setText(api_key)

    def launch_custom_tool_wizard(self):
        # Placeholder for launching a custom tool integration wizard
        QMessageBox.information(self, "Custom Tool Wizard", "This will launch a wizard to integrate custom tools.")

    def create_model_settings_group(self):
        model_group_layout = QVBoxLayout()
        model_group_layout.addWidget(QLabel("<h3>LLM Settings</h3>"))

        # Model Search and Selection
        model_search_layout = QHBoxLayout()
        model_search_layout.addWidget(QLabel("Search Model:"))
        self.model_search_edit = QLineEdit()
        self.model_search_edit.setPlaceholderText("Search for models...")
        self.model_search_edit.textChanged.connect(self.filter_models)
        model_search_layout.addWidget(self.model_search_edit)
        model_group_layout.addLayout(model_search_layout)

        model_selection_layout = QHBoxLayout()
        model_selection_layout.addWidget(QLabel("Model:"))
        self.model_combo = QComboBox()
        self.populate_model_combo() # Call a new method to populate
        model_selection_layout.addWidget(self.model_combo)
        self.add_custom_model_button = QPushButton("Add Custom Model")
        self.add_custom_model_button.clicked.connect(self.add_custom_model)
        model_selection_layout.addWidget(self.add_custom_model_button)
        model_group_layout.addLayout(model_selection_layout)

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

    def create_voice_settings_group(self):
        voice_group_layout = QVBoxLayout()
        voice_group_layout.addWidget(QLabel("<h3>Voice Settings</h3>"))

        voice_profile_layout = QHBoxLayout()
        voice_profile_layout.addWidget(QLabel("Voice Profile:"))
        self.voice_profile_combo = QComboBox()
        for profile_name in self.tts_service.get_available_voice_profiles():
            self.voice_profile_combo.addItem(profile_name)
        voice_profile_layout.addWidget(self.voice_profile_combo)
        voice_group_layout.addLayout(voice_profile_layout)

        self.main_layout.addLayout(voice_group_layout)

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

        self.tools_data = {
            "shell": {"name": "Shell Tool", "description": "Allows the agent to execute shell commands.", "default": True},
            "browser": {"name": "Browser Tool", "description": "Enables the agent to browse the web.", "default": False},
            "files": {"name": "Files Tool", "description": "Provides access to file system operations (read, write, delete).", "default": True},
            # Add more tools as needed
        }

        for tool_id, tool_info in self.tools_data.items():
            tool_layout = QHBoxLayout()
            checkbox = QCheckBox(tool_info["name"])
            checkbox.setChecked(tool_info["default"])
            setattr(self, f"{tool_id}_tool_checkbox", checkbox) # Store reference to checkbox
            tool_layout.addWidget(checkbox)
            tool_layout.addWidget(QLabel(tool_info["description"]))
            tool_group_layout.addLayout(tool_layout)

        # Custom Tool Integration Placeholder
        custom_tool_layout = QHBoxLayout()
        custom_tool_layout.addWidget(QLabel("Custom Tool Integration:"))
        self.custom_tool_button = QPushButton("Launch Wizard")
        self.custom_tool_button.clicked.connect(self.launch_custom_tool_wizard)
        custom_tool_layout.addWidget(self.custom_tool_button)
        tool_group_layout.addLayout(custom_tool_layout)

        self.main_layout.addLayout(tool_group_layout)

    def create_published_prompts_group(self):
        prompts_group_layout = QVBoxLayout()
        prompts_group_layout.addWidget(QLabel("<h3>Published Prompts Library</h3>"))

        # Category filter
        category_layout = QHBoxLayout()
        category_layout.addWidget(QLabel("Category:"))
        self.category_combo = QComboBox()
        self.category_combo.addItem("All Categories")
        for category in self.prompt_library.get_all_categories():
            self.category_combo.addItem(category)
        self.category_combo.currentTextChanged.connect(self.filter_prompts_by_category)
        category_layout.addWidget(self.category_combo)
        prompts_group_layout.addLayout(category_layout)

        # Prompt selection
        prompt_selection_layout = QHBoxLayout()
        prompt_selection_layout.addWidget(QLabel("Select Prompt:"))
        self.published_prompt_combo = QComboBox()
        self.populate_prompt_combo()
        self.published_prompt_combo.currentTextChanged.connect(self.on_prompt_selected)
        prompt_selection_layout.addWidget(self.published_prompt_combo)

        self.browse_prompts_button = QPushButton("Preview")
        self.browse_prompts_button.clicked.connect(self.preview_selected_prompt)
        prompt_selection_layout.addWidget(self.browse_prompts_button)
        prompts_group_layout.addLayout(prompt_selection_layout)

        # Prompt description
        self.prompt_description_label = QLabel("Select a prompt to see its description")
        self.prompt_description_label.setWordWrap(True)
        self.prompt_description_label.setStyleSheet("color: #888; font-style: italic; padding: 10px;")
        prompts_group_layout.addWidget(self.prompt_description_label)

        self.main_layout.addLayout(prompts_group_layout)

    def populate_prompt_combo(self):
        """Populate the prompt combo box with all available prompts."""
        self.published_prompt_combo.clear()
        for prompt_name in self.prompt_library.get_prompt_names():
            self.published_prompt_combo.addItem(prompt_name)
    
    def filter_prompts_by_category(self, category):
        """Filter prompts by selected category."""
        self.published_prompt_combo.clear()
        if category == "All Categories":
            self.populate_prompt_combo()
        else:
            prompts = self.prompt_library.get_prompts_by_category(category)
            for prompt in prompts.values():
                self.published_prompt_combo.addItem(prompt["name"])
    
    def on_prompt_selected(self, prompt_name):
        """Update description when a prompt is selected."""
        if prompt_name:
            prompt = self.prompt_library.get_prompt_by_name(prompt_name)
            if prompt:
                self.prompt_description_label.setText(f"<b>{prompt['category']}</b>: {prompt['description']}")
                # Auto-fill system prompt
                self.system_prompt_edit.setPlainText(prompt["system_prompt"])
    
    def preview_selected_prompt(self):
        """Show a preview dialog of the selected prompt."""
        prompt_name = self.published_prompt_combo.currentText()
        if prompt_name:
            prompt = self.prompt_library.get_prompt_by_name(prompt_name)
            if prompt:
                preview_dialog = QDialog(self)
                preview_dialog.setWindowTitle(f"Preview: {prompt['name']}")
                preview_dialog.setGeometry(200, 200, 600, 400)
                
                layout = QVBoxLayout(preview_dialog)
                
                # Header
                header_label = QLabel(f"<h2>{prompt['name']}</h2>")
                layout.addWidget(header_label)
                
                category_label = QLabel(f"<b>Category:</b> {prompt['category']}")
                layout.addWidget(category_label)
                
                desc_label = QLabel(f"<b>Description:</b> {prompt['description']}")
                desc_label.setWordWrap(True)
                layout.addWidget(desc_label)
                
                tags_label = QLabel(f"<b>Tags:</b> {', '.join(prompt['tags'])}")
                layout.addWidget(tags_label)
                
                # System prompt
                prompt_label = QLabel("<b>System Prompt:</b>")
                layout.addWidget(prompt_label)
                
                prompt_text = QTextEdit()
                prompt_text.setPlainText(prompt["system_prompt"])
                prompt_text.setReadOnly(True)
                layout.addWidget(prompt_text)
                
                # Use button
                use_button = QPushButton("Use This Prompt")
                use_button.clicked.connect(lambda: self.use_prompt(prompt, preview_dialog))
                layout.addWidget(use_button)
                
                preview_dialog.exec()
    
    def use_prompt(self, prompt, dialog):
        """Use the selected prompt and close preview dialog."""
        self.system_prompt_edit.setPlainText(prompt["system_prompt"])
        self.published_prompt_combo.setCurrentText(prompt["name"])
        dialog.accept()
    
    def browse_prompt_library(self):
        """Legacy method - now handled by preview."""
        self.preview_selected_prompt()

    def create_workflow_settings_group(self):
        workflow_group_layout = QVBoxLayout()
        workflow_group_layout.addWidget(QLabel("<h3>Workflow Settings (Visual Editor Placeholder)</h3>"))

        # Placeholder for the visual workflow editor
        self.workflow_editor_placeholder = QLabel("Visual workflow editor will go here.")
        self.workflow_editor_placeholder.setAlignment(Qt.AlignCenter)
        self.workflow_editor_placeholder.setStyleSheet("border: 1px dashed #ccc; padding: 50px;")
        workflow_group_layout.addWidget(self.workflow_editor_placeholder)

        self.main_layout.addLayout(workflow_group_layout)

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

        model_full_text = self.model_combo.currentText()
        if ": " in model_full_text:
            provider, model = model_full_text.split(": ", 1)
        else:
            provider = "Unknown"
            model = model_full_text
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
        voice_profile = self.voice_profile_combo.currentText()
        published_prompt = self.published_prompt_combo.currentText()

        # Collect selected tools
        selected_tools = []
        for tool_id in self.tools_data.keys():
            checkbox = getattr(self, f"{tool_id}_tool_checkbox")
            if checkbox.isChecked():
                selected_tools.append(tool_id)

        # Placeholder for saving workflow data
        print("Workflow data would be saved here.")

        # Save agent profile using ConfigManager
        agent_config = {
            "name": agent_name,
            "profile_picture": profile_pic_path,
            "system_prompt": system_prompt,
            "llm": {
                "model": model,
                "api_base": api_base,
                "api_key": api_key,
                "context_window": context_window,
                "max_tokens": max_tokens,
                "supports_functions": supports_functions,
                "supports_vision": supports_vision,
            },
            "interpreter": {
                "offline": offline,
                "loop": loop,
                "auto_run": auto_run,
                "os_mode": os_mode,
                "import_computer_api": import_computer_api,
            },
            "voice": {
                "profile": voice_profile,
            },
            "tools": selected_tools,
            "custom_instructions": custom_instructions,
            "published_prompt": published_prompt,
        }
        self.config_manager.set(f"agents.{agent_name}", agent_config)
        QMessageBox.information(self, "Success", f"Agent profile '{agent_name}' saved successfully.")
        self.accept() # Close dialog on success

        