from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QComboBox, QHBoxLayout, QLabel
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QTextCharFormat, QTextCursor, QColor, QFont
from .services.settings_manager import SettingsManager
from markdown_it import MarkdownIt
from pygments import highlight
from pygments.lexers import get_lexer_by_name, ClassNotFound
from pygments.formatters import HtmlFormatter

from .services.function_registry import FunctionRegistry

class ChatWindow(QWidget):
    send_command_signal = Signal(str)

    def __init__(self, chat_manager, function_registry, parent=None):
        super().__init__(parent)
        self.chat_manager = chat_manager
        self.function_registry = function_registry
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)

        

        self.settings_manager = SettingsManager()
        font_size = self.settings_manager.get_setting("FONT_SIZE", "11") # Default to 11 if not set

        font = QFont()
        font.setPointSize(int(font_size))

        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)
        self.output_display.setObjectName("chatOutputDisplay") # For styling
        self.output_display.setFont(font)
        self.layout.addWidget(self.output_display)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type your command here...")
        self.input_field.returnPressed.connect(self.send_command)
        self.input_field.setObjectName("chatInputField") # For styling
        self.input_field.setFont(font)
        self.layout.addWidget(self.input_field)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_command)
        self.send_button.setObjectName("chatSendButton") # For styling
        self.send_button.setToolTip("Send your message or command to the AI.")
        self.layout.addWidget(self.send_button)

        # Chat Export/Import Buttons
        self.export_json_button = QPushButton("Export JSON")
        self.export_json_button.clicked.connect(lambda: self.chat_manager.export_conversation_json(self.chat_manager.current_conversation_id, "conversation.json"))
        self.layout.addWidget(self.export_json_button)

        self.import_json_button = QPushButton("Import JSON")
        self.import_json_button.clicked.connect(lambda: self.chat_manager.import_conversation_json("conversation.json"))
        self.layout.addWidget(self.import_json_button)

        # Advanced Chat Controls
        self.edit_message_button = QPushButton("Edit Message")
        self.edit_message_button.clicked.connect(lambda: print("Edit message clicked"))
        self.layout.addWidget(self.edit_message_button)

        self.regenerate_message_button = QPushButton("Regenerate Message")
        self.regenerate_message_button.clicked.connect(lambda: print("Regenerate message clicked"))
        self.layout.addWidget(self.regenerate_message_button)

        self.chat_templates_label = QLabel("Chat Templates (Coming Soon)")
        self.layout.addWidget(self.chat_templates_label)

        self.chat_branching_label = QLabel("Chat Branching (Coming Soon)")
        self.layout.addWidget(self.chat_branching_label)

        self.conversation_tagging_label = QLabel("Conversation Tagging (Coming Soon)")
        self.layout.addWidget(self.conversation_tagging_label)

        self.conversation_analytics_label = QLabel("Conversation Analytics (Coming Soon)")
        self.layout.addWidget(self.conversation_analytics_label)

        # Chat Header Enhancement Placeholders
        

        # Function Management
        self.function_registry_browser_label = QLabel("Function Registry Browser (Coming Soon)")
        self.layout.addWidget(self.function_registry_browser_label)

        self.custom_function_creation_button = QPushButton("Create Custom Function")
        self.custom_function_creation_button.clicked.connect(lambda: print("Create Custom Function clicked"))
        self.layout.addWidget(self.custom_function_creation_button)

        self.function_testing_button = QPushButton("Test Function")
        self.function_testing_button.clicked.connect(lambda: print("Test Function clicked"))
        self.layout.addWidget(self.function_testing_button)

        self.function_sharing_label = QLabel("Function Sharing & Templates (Coming Soon)")
        self.layout.addWidget(self.function_sharing_label)

        self.function_documentation_label = QLabel("Function Documentation (Coming Soon)")
        self.layout.addWidget(self.function_documentation_label)

        # Code Execution Enhancement
        self.code_execution_history_label = QLabel("Code Execution History (Coming Soon)")
        self.layout.addWidget(self.code_execution_history_label)

        self.code_sharing_button = QPushButton("Share Code")
        self.code_sharing_button.clicked.connect(lambda: print("Share Code clicked"))
        self.layout.addWidget(self.code_sharing_button)

        self.code_templates_label = QLabel("Code Templates & Snippets (Coming Soon)")
        self.layout.addWidget(self.code_templates_label)

        self.md = MarkdownIt()
        self.formatter = HtmlFormatter(noclasses=True, style="monokai") # Using 'monokai' for dark theme
        self.current_assistant_response_buffer = ""
        self.in_code_block = False # State variable for code block formatting
        self.code_lang = "python" # Default language for code blocks

    def _render_markdown_with_code(self, markdown_text):
        html = []
        for block in self.md.parse(markdown_text):
            if block.type == 'fence' and block.info:
                lang = block.info.strip()
                code = block.content
                try:
                    lexer = get_lexer_by_name(lang)
                    highlighted_code = highlight(code, lexer, self.formatter)
                    html.append(f'<pre><code class="language-{lang}">{highlighted_code}</code></pre>')
                except ClassNotFound:
                    html.append(f'<pre><code class="language-{lang}">{code}</code></pre>')
            elif block.type == 'paragraph':
                html.append(f'<p>{block.content}</p>')
            elif block.type == 'text':
                html.append(block.content)
            # Add more markdown block types as needed
        return "".join(html)

    def send_command(self):
        command = self.input_field.text()
        if not command.strip():
            return

        try:
            # Display user command
            self.append_output({"type": "message", "content": f"<p style='color:#00CED1; font-weight:bold;'>&gt;&gt;&gt; {command}</p>"})
            self.input_field.clear()
            print(f"ChatWindow: Emitting send_command_signal with command: {command}")
            self.send_command_signal.emit(command)

            # Clear buffer for new assistant response
            self.current_assistant_response_buffer = ""
            # Add a placeholder for the assistant's response
            self.output_display.append("<p id='assistant_response_placeholder'></p>")
        except Exception as e:
            self.append_output({"type": "error", "content": f"Error sending command: {e}"})

    def append_output(self, chunk):
        content = chunk.get("content", "")
        msg_type = chunk.get("type", "message")
        msg_format = chunk.get("format", None)

        if msg_type == "code":
            if "start" in chunk:
                self.in_code_block = True
                self.code_lang = msg_format if msg_format else "python"
                self.current_assistant_response_buffer += f"```{self.code_lang}\n"
            elif "end" in chunk:
                self.in_code_block = False
                self.current_assistant_response_buffer += content + "\n```\n"
            else:
                self.current_assistant_response_buffer += content
        elif msg_type == "console":
            if "start" in chunk:
                self.current_assistant_response_buffer += f"\nOutput:\n```console\n"
            elif "end" in chunk:
                self.current_assistant_response_buffer += content + "\n```\n"
            else:
                self.current_assistant_response_buffer += content
        elif msg_type == "message":
            self.current_assistant_response_buffer += content
        elif msg_type == "error":
            self.current_assistant_response_buffer += f"\n<span style='color:#FF6347; font-weight:bold;'>Error: {content}</span>\n"
        else:
            self.current_assistant_response_buffer += f"\n<span style='color:#E0E0E0;'>[{msg_type.upper()}] {content}</span>\n"

        self._update_last_assistant_message()

    def _update_last_assistant_message(self):
        # Get the full HTML content of the QTextEdit
        full_html = self.output_display.toHtml()

        # Find the placeholder for the assistant's response
        placeholder_tag = "<p id=\"assistant_response_placeholder\"></p>"
        placeholder_index = full_html.rfind(placeholder_tag)

        if placeholder_index != -1:
            # Replace the placeholder with the rendered content
            rendered_content = self._render_markdown_with_code(self.current_assistant_response_buffer)
            new_html = full_html[:placeholder_index] + rendered_content + full_html[placeholder_index + len(placeholder_tag):]
            self.output_display.setHtml(new_html)
        else:
            # Fallback if placeholder not found (shouldn't happen with current logic)
            self.output_display.setHtml(full_html + self._render_markdown_with_code(self.current_assistant_response_buffer))

        self.output_display.verticalScrollBar().setValue(self.output_display.verticalScrollBar().maximum())

    

    def ask_multiple_models(self, query):
        # Placeholder for asking multiple models
        print(f"Asking multiple models: {query}")
        # This would involve iterating through selected models and getting responses

    def show_model_comparison(self, responses):
        # Placeholder for model comparison view
        print("Showing model comparison:", responses)

    def create_model_specific_thread(self, model_name):
        # Placeholder for creating model-specific conversation threads
        print(f"Creating model-specific thread for {model_name}")

    def display_history(self, messages):
        self.output_display.clear()
        full_conversation_markdown = ""
        for message in messages:
            role = message.get("role", "unknown")
            content = message.get("content", "")
            msg_type = message.get("type", "message")
            msg_format = message.get("format", None)
            
            if role == "user":
                full_conversation_markdown += f"<p style='color:#00CED1; font-weight:bold;'>&gt;&gt;&gt; {content}</p>\n"
            elif role == "assistant" and msg_type == "message":
                full_conversation_markdown += f"<p style='color:#E0E0E0;'>{content}</p>\n"
            elif role == "computer" and msg_type == "console":
                full_conversation_markdown += f"\nOutput:\n```console\n{content}\n```\n"
            elif role == "assistant" and msg_type == "code":
                full_conversation_markdown += f"```{msg_format if msg_format else 'python'}\n{content}\n```\n"
            elif role == "server" and msg_type == "error":
                full_conversation_markdown += f"\n<span style='color:#FF6347; font-weight:bold;'>Error: {content}</span>\n"
            else:
                full_conversation_markdown += f"\n<span style='color:#E0E0E0;'>[{role.upper()}:{msg_type}] {content}</span>\n"
        
        self.output_display.setHtml(self._render_markdown_with_code(full_conversation_markdown))
        self.output_display.verticalScrollBar().setValue(self.output_display.verticalScrollBar().maximum())