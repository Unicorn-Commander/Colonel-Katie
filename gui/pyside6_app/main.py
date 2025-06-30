import sys
import json
import os
from PySide6.QtWidgets (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QPushButton, QHBoxLayout,
    QDialog, QFormLayout, QDialogButtonBox, QComboBox, QLabel
)
from PySide6.QtCore import QThread, Signal, QObject, Qt
from markdown_it import MarkdownIt
from pygments import highlight
from pygments.lexers import get_lexer_by_name, ClassNotFound
from pygments.formatters import HtmlFormatter

# Import OpenInterpreter directly
from interpreter import OpenInterpreter

# Define a path for settings file
SETTINGS_FILE = os.path.join(os.path.expanduser("~/.config/the_colonel"), "settings.json")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

class RedisMemoryManager:
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB):
        self.redis_client = None
        try:
            self.redis_client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
            self.redis_client.ping() # Test connection
            print(f"Connected to Redis at {host}:{port}")
        except redis.exceptions.ConnectionError as e:
            print(f"Could not connect to Redis: {e}")
            self.redis_client = None

    def save_conversation(self, conversation_id, messages):
        if self.redis_client:
            try:
                self.redis_client.set(f"conversation:{conversation_id}", json.dumps(messages))
            except Exception as e:
                print(f"Error saving conversation to Redis: {e}")

    def load_conversation(self, conversation_id):
        if self.redis_client:
            try:
                data = self.redis_client.get(f"conversation:{conversation_id}")
                if data:
                    return json.loads(data)
            except Exception as e:
                print(f"Error loading conversation from Redis: {e}")
        return []

class SettingsManager:
    settings_updated = Signal()

    def __init__(self):
        super().__init__()
        self._settings = self._load_settings()

    def _load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
        return {"api_key": "", "model": "the-colonel"}

    def save_settings(self, new_settings):
        os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(new_settings, f, indent=4)
        self._settings = new_settings
        self.settings_updated.emit()

    def get_setting(self, key):
        return self._settings.get(key)

class SettingsDialog(QDialog):
    def __init__(self, settings_manager, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.settings_manager = settings_manager

        self.layout = QFormLayout(self)

        self.api_key_input = QLineEdit(self.settings_manager.get_setting("api_key"))
        self.layout.addRow("API Key:", self.api_key_input)

        self.model_combo = QComboBox()
        self.model_combo.addItems(["the-colonel", "gpt-4o-mini", "claude-3-opus-20240229", "gemini-1.5-pro-latest"])
        self.model_combo.setCurrentText(self.settings_manager.get_setting("model"))
        self.layout.addRow("Model:", self.model_combo)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addRow(self.button_box)

    def accept(self):
        new_settings = {
            "api_key": self.api_key_input.text(),
            "model": self.model_combo.currentText()
        }
        self.settings_manager.save_settings(new_settings)
        super().accept()

class InterpreterWorker:
    message_received = Signal(str, str) # role, content
    stream_chunk_received = Signal(str) # content chunk
    request_finished = Signal()
    error_occurred = Signal(str)

    def __init__(self, interpreter_instance, user_message):
        super().__init__()
        self.interpreter = interpreter_instance
        self.user_message = user_message

    def run(self):
        try:
            # Directly call interpreter.chat()
            for chunk in self.interpreter.chat(self.user_message, stream=True, display=False):
                if isinstance(chunk, dict):
                    chunk_type = chunk.get("type", "unknown")
                    chunk_content = chunk.get("content", "")

                    if chunk_type == "message" and chunk_content:
                        self.stream_chunk_received.emit(chunk_content)
                    elif chunk_type == "code" and chunk.get("start"):
                        code_format = chunk.get("format", "python")
                        self.stream_chunk_received.emit(f"\n```{\ncode_format}\n")
                    elif chunk_type == "code" and chunk_content:
                        self.stream_chunk_received.emit(chunk_content)
                    elif chunk_type == "code" and chunk.get("end"):
                        self.stream_chunk_received.emit("\n```\n")
                    elif chunk_type == "console" and chunk.get("start"):
                        self.stream_chunk_received.emit("\nOutput:\n```\n")
                    elif chunk_type == "console" and chunk_content:
                        self.stream_chunk_received.emit(str(chunk_content))
                    elif chunk_type == "console" and chunk.get("end"):
                        self.stream_chunk_received.emit("\n```\n")
                    elif chunk_type == "confirmation":
                        # Handle confirmation if needed, for now, just log
                        print(f"Confirmation required: {chunk.get('content')}")
                    elif chunk_type == "unknown" and chunk_content:
                        self.stream_chunk_received.emit(chunk_content)
                    else:
                        print(f"Unknown chunk type: {chunk_type} - {chunk}")
                elif isinstance(chunk, str):
                    self.stream_chunk_received.emit(chunk)

        except Exception as e:
            self.error_occurred.emit(f"An error occurred during interpretation: {e}")
        finally:
            self.request_finished.emit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("The_Colonel GUI (PySide6)")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Chat display area
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)
        main_layout.addWidget(self.chat_display)

        # Model display label
        self.model_label = QLabel("Current Model: N/A")
        main_layout.addWidget(self.model_label)

        # Chat input area
        input_layout = QHBoxLayout()
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Type your message here...")
        self.chat_input.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.chat_input)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)

        main_layout.addLayout(input_layout)

        # Settings button
        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self.open_settings)
        main_layout.addWidget(self.settings_button)

        # Initialize OpenInterpreter
        self.interpreter = OpenInterpreter()
        # Set display to False as we handle display in GUI
        self.interpreter.display = False

        # Initialize SettingsManager and RedisMemoryManager
        self.settings_manager = SettingsManager()
        self.redis_memory_manager = RedisMemoryManager()
        self.conversation_id = "default_conversation" # Simple ID for now

        self._apply_settings_to_interpreter() # Apply initial settings
        self.settings_manager.settings_updated.connect(self._apply_settings_to_interpreter) # Update on settings change

        # Load conversation history from Redis
        self._load_conversation_history()

        # Markdown renderer and formatter
        self.md = MarkdownIt()
        self.formatter = HtmlFormatter(noclasses=True, style="default")
        self.current_assistant_response_buffer = ""

    def _load_conversation_history(self):
        messages = self.redis_memory_manager.load_conversation(self.conversation_id)
        for msg in messages:
            self.append_message(msg["role"], msg["content"], is_history=True)

    def _save_conversation_history(self):
        # Extract messages from interpreter's history
        messages_to_save = []
        for msg in self.interpreter.messages:
            if isinstance(msg, dict) and "role" in msg and "content" in msg:
                messages_to_save.append({"role": msg["role"], "content": msg["content"]})
        self.redis_memory_manager.save_conversation(self.conversation_id, messages_to_save)

    def _apply_settings_to_interpreter(self):
        api_key = self.settings_manager.get_setting("api_key")
        model = self.settings_manager.get_setting("model")

        if api_key:
            self.interpreter.llm.api_key = api_key
        else:
            self.interpreter.llm.api_key = None # Clear if empty

        if model:
            self.interpreter.llm.model = model
        
        self.model_label.setText(f"Current Model: {model}")
        self.chat_display.append(f"<br><i>Settings applied: Model={model}, API Key Set={bool(api_key)}</i>")

    def open_settings(self):
        dialog = SettingsDialog(self.settings_manager, self)
        dialog.exec()

    def send_message(self):
        user_message = self.chat_input.text().strip()
        if not user_message:
            return

        self.chat_input.clear()
        self.append_message("user", user_message)

        # Clear buffer for new assistant response
        self.current_assistant_response_buffer = ""
        self.append_message("assistant", "") # Add an empty assistant message to start

        self.send_button.setEnabled(False)
        self.chat_input.setEnabled(False)

        self.worker = InterpreterWorker(self.interpreter, user_message)
        self.thread = QThread()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.stream_chunk_received.connect(self.append_stream_chunk)
        self.worker.request_finished.connect(self.request_finished)
        self.worker.error_occurred.connect(self.display_error)

        self.thread.start()

    def append_message(self, role, content, is_history=False):
        html_content = ""
        if role == "user":
            html_content = f"<p><b>You:</b> {self.md.render(content)}</p>"
        elif role == "assistant":
            # For initial assistant message, just append a placeholder
            # The actual content will be streamed via append_stream_chunk
            html_content = f"<p><b>Assistant:</b></p>"

        self.chat_display.append(html_content)
        self.chat_display.verticalScrollBar().setValue(self.chat_display.verticalScrollBar().maximum())

    def append_stream_chunk(self, chunk):
        self.current_assistant_response_buffer += chunk
        self._update_last_assistant_message()

    def _update_last_assistant_message(self):
        # Get the full HTML content of the QTextEdit
        full_html = self.chat_display.toHtml()

        # Find the start of the last <p> tag for the assistant
        # This is a simplified approach and might need refinement for complex HTML structures
        last_p_start = full_html.rfind("<p><b>Assistant:</b>")
        if last_p_start != -1:
            # Extract the part before the last assistant message
            prefix_html = full_html[:last_p_start]

            # Render the buffered content
            rendered_content = self._render_markdown_with_code(self.current_assistant_response_buffer)
            
            # Construct the new HTML for the last assistant message
            new_assistant_html = f"<p><b>Assistant:</b> {rendered_content}</p>"

            # Set the entire HTML content back to QTextEdit
            self.chat_display.setHtml(prefix_html + new_assistant_html)
        else:
            # Fallback if no assistant message found (shouldn't happen with current logic)
            self.chat_display.setHtml(self.chat_display.toHtml() + self._render_markdown_with_code(self.current_assistant_response_buffer))

        self.chat_display.verticalScrollBar().setValue(self.chat_display.verticalScrollBar().maximum())

    def _render_markdown_with_code(self, text):
        # This function processes markdown and highlights code blocks
        # It needs to handle the streaming nature, so it processes the current buffer
        rendered_html = ""
        in_code_block = False
        code_lang = "python"
        code_buffer = []

        lines = text.splitlines(keepends=True)
        for i, line in enumerate(lines):
            if line.strip().startswith("```"):
                if in_code_block:
                    # End of code block
                    code_block = "".join(code_buffer)
                    try:
                        lexer = get_lexer_by_name(code_lang)
                        highlighted_code = highlight(code_block, lexer, self.formatter)
                        rendered_html += f"<pre style=\"background-color: #f0f0f0; padding: 5px;\">{highlighted_code}</pre>"
                    except ClassNotFound:
                        rendered_html += f"<pre>{code_block}</pre>"
                    except Exception as e:
                        rendered_html += f"<pre>Error highlighting code: {e}\n{code_block}</pre>"
                    code_buffer = []
                    in_code_block = False
                else:
                    # Start of code block
                    parts = line.strip().split(' ', 1)
                    if len(parts) > 1:
                        code_lang = parts[1].strip() or "python"
                    else:
                        code_lang = "python"
                    in_code_block = True
            elif in_code_block:
                code_buffer.append(line)
            else:
                # Render non-code lines as markdown
                rendered_html += self.md.render(line.strip()) # Render line by line
        
        # If a code block was open at the end, render it (for partial blocks during streaming)
        if in_code_block and code_buffer:
            code_block = "".join(code_buffer)
            try:
                lexer = get_lexer_by_name(code_lang)
                highlighted_code = highlight(code_block, lexer, self.formatter)
                rendered_html += f"<pre style=\"background-color: #f0f0f0; padding: 5px;\">{highlighted_code}</pre>"
            except ClassNotFound:
                rendered_html += f"<pre>{code_block}</pre>"
            except Exception as e:
                rendered_html += f"<pre>Error highlighting code: {e}\n{code_block}</pre>"

        return rendered_html

    def request_finished(self):
        self.send_button.setEnabled(True)
        self.chat_input.setEnabled(True)
        self.thread.quit()
        self.thread.wait()
        # Ensure the final message is fully rendered after stream ends
        self._update_last_assistant_message()
        self._save_conversation_history() # Save conversation after it finishes

    def display_error(self, error_message):
        self.chat_display.append(f"<font color=\"red\">Error: {error_message}</font>")
        self.request_finished()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())