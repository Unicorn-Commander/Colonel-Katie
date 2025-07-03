import uuid
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QHBoxLayout, QLabel, QDialog, QProgressBar
from PySide6.QtCore import Signal, Qt, QTimer
from PySide6.QtGui import QTextCharFormat, QTextCursor, QColor, QFont
from .services.settings_manager import SettingsManager
from markdown_it import MarkdownIt
from pygments import highlight
from pygments.lexers import get_lexer_by_name, ClassNotFound
from pygments.formatters import HtmlFormatter

from .services.function_registry import FunctionRegistry
from .quick_settings_panel import QuickSettingsPanel

class ChatHeader(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 5, 10, 5)
        self.layout.setSpacing(10)
        self.layout.setAlignment(Qt.AlignLeft)

        self.model_indicator = QLabel("Model: N/A")
        self.model_indicator.setObjectName("chatHeaderLabel")
        self.layout.addWidget(self.model_indicator)

        self.token_usage = QLabel("Tokens: N/A")
        self.token_usage.setObjectName("chatHeaderLabel")
        self.layout.addWidget(self.token_usage)

    def update_token_usage(self, used_tokens, max_tokens):
        self.token_usage.setText(f"Tokens: {used_tokens}/{max_tokens}")

        self.connection_status = QLabel("Status: Idle")
        self.connection_status.setObjectName("chatHeaderLabel")
        self.layout.addWidget(self.connection_status)

        self.layout.addStretch() # Pushes content to the left

    def update_model_indicator(self, model_name):
        self.model_indicator.setText(f"Model: {model_name}")

    def update_token_usage(self, used, total):
        self.token_usage.setText(f"Tokens: {used}/{total}")

    def update_connection_status(self, status):
        self.connection_status.setText(f"Status: {status}")

class ChatActionBar(QWidget):
    settings_button_clicked = Signal()
    voice_button_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)
        self.layout.setAlignment(Qt.AlignLeft)

        # Add buttons: 📄 Files, 🔍 Search, 🧠 RAG, 🎙️ Voice, ⚙️ Settings
        # Placeholder buttons for now
        self.files_button = QPushButton("📄 Files")
        self.search_button = QPushButton("🔍 Search")
        self.rag_button = QPushButton("🧠 RAG")
        self.voice_button = QPushButton("🎙️ Voice")
        self.settings_button = QPushButton("⚙️ Settings")

        self.layout.addWidget(self.files_button)
        self.layout.addWidget(self.search_button)
        self.layout.addWidget(self.rag_button)
        self.layout.addWidget(self.voice_button)
        self.layout.addStretch() # Pushes settings button to the right
        self.layout.addWidget(self.settings_button)

        self.settings_button.clicked.connect(self.settings_button_clicked.emit)
        self.voice_button.clicked.connect(self.voice_button_clicked.emit)

class PTTModal(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Push to Talk")
        self.setModal(True)
        self.setFixedSize(200, 100)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint) # Make it frameless and always on top

        layout = QVBoxLayout(self)
        self.mic_label = QLabel("🎙️")
        self.mic_label.setAlignment(Qt.AlignCenter)
        self.mic_label.setStyleSheet("font-size: 48px;")
        layout.addWidget(self.mic_label)

        self.status_label = QLabel("Press and hold SPACE to talk")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

class ChatWindow(QWidget):
    send_command_signal = Signal(str)
    speak_message_signal = Signal(str)

    def __init__(self, chat_manager, function_registry, parent=None):
        super().__init__(parent)
        self.chat_manager = chat_manager
        self.function_registry = function_registry
        self.stt_service = None # Will be set from main_window
        self.tts_service = None # Will be set from main_window
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)

        self.chat_header = ChatHeader()
        self.layout.addWidget(self.chat_header)

        self.message_data = {} # Stores message content by ID

        

        self.settings_manager = SettingsManager()
        font_size = self.settings_manager.get_setting("FONT_SIZE", "11") # Default to 11 if not set

        font = QFont()
        font.setPointSize(int(font_size))

        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)
        self.output_display.setObjectName("chatOutputDisplay") # For styling
        self.output_display.setFont(font)
        self.output_display.setContextMenuPolicy(Qt.CustomContextMenu)
        self.output_display.customContextMenuRequested.connect(self.show_message_context_menu)
        # Note: QTextEdit doesn't have anchorClicked, using mouse events instead
        # self.output_display.anchorClicked.connect(self.handle_anchor_click)
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

        self.typing_indicator = QLabel("AI is typing...")
        self.typing_indicator.setObjectName("typingIndicator")
        self.typing_indicator.setAlignment(Qt.AlignCenter)
        self.typing_indicator.hide() # Hidden by default
        self.layout.addWidget(self.typing_indicator)

        self.chat_action_bar = ChatActionBar()
        self.layout.addWidget(self.chat_action_bar)

        self.quick_settings_panel = QuickSettingsPanel(self.chat_manager.model_manager)
        self.quick_settings_panel.hide() # Initially hidden
        self.layout.addWidget(self.quick_settings_panel)

        self.chat_action_bar.settings_button_clicked.connect(self.toggle_quick_settings_panel)
        self.chat_action_bar.voice_button_clicked.connect(self.toggle_voice_input)
        self.quick_settings_panel.settings_changed.connect(self.chat_manager.update_chat_settings)

        self.ptt_modal = PTTModal(self)
        self.ptt_modal.hide()

        self.md = MarkdownIt()
        self.formatter = HtmlFormatter(noclasses=True, style="monokai") # Using 'monokai' for dark theme
        self.current_assistant_response_buffer = ""
        self.in_code_block = False # State variable for code block formatting
        self.code_lang = "python" # Default language for code blocks

    def toggle_voice_input(self):
        if self.stt_service.is_recording:
            audio_file_path = self.stt_service.stop_recording()
            self.voice_button.setText("🎙️ Voice")
            self.voice_button.setStyleSheet("") # Clear recording style
            self.typing_indicator.hide()
            if audio_file_path:
                self.append_output({"type": "message", "content": "Transcribing audio..."})
                transcribed_text = self.stt_service.transcribe_audio(audio_file_path)
                if transcribed_text:
                    self.input_field.setText(transcribed_text)
                    self.send_command() # Send the transcribed text as a command
                else:
                    self.append_output({"type": "error", "content": "Failed to transcribe audio."})
        else:
            self.stt_service.start_recording()
            self.voice_button.setText("🔴 Recording...")
            self.voice_button.setStyleSheet("background-color: red;") # Indicate recording
            self.typing_indicator.setText("Listening...")
            self.typing_indicator.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space and not event.isAutoRepeat():
            if not self.stt_service.is_recording:
                self.stt_service.start_recording()
                self.ptt_modal.show()
                self.ptt_modal.status_label.setText("Recording...")
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Space and not event.isAutoRepeat():
            if self.stt_service.is_recording:
                audio_file_path = self.stt_service.stop_recording()
                self.ptt_modal.hide()
                self.ptt_modal.status_label.setText("Press and hold SPACE to talk")
                if audio_file_path:
                    self.append_output({"type": "message", "content": "Transcribing audio..."})
                    transcribed_text = self.stt_service.transcribe_audio(audio_file_path)
                    if transcribed_text:
                        self.input_field.setText(transcribed_text)
                        self.send_command() # Send the transcribed text as a command
                    else:
                        self.append_output({"type": "error", "content": "Failed to transcribe audio."})
        super().keyReleaseEvent(event)

    def toggle_quick_settings_panel(self):
        if self.quick_settings_panel.isVisible():
            self.quick_settings_panel.hide()
        else:
            self.quick_settings_panel.show()

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
            message_id = str(uuid.uuid4())
            # Display user command
            user_message_html = f"<div id='{message_id}' class='user-message'><p style='color:#00CED1; font-weight:bold;'>&gt;&gt;&gt; {command}</p></div>"
            self.output_display.append(user_message_html)
            self.message_data[message_id] = {"role": "user", "content": command}

            self.input_field.clear()
            print(f"ChatWindow: Emitting send_command_signal with command: {command}")
            self.send_command_signal.emit(command)

            # Clear buffer for new assistant response
            self.current_assistant_response_buffer = ""
            # Add a placeholder for the assistant's response
            self.output_display.append("<div id='assistant_response_placeholder'></div>")
        except Exception as e:
            self.append_output({"type": "error", "content": f"Error sending command: {e}"})

    def append_output(self, chunk):
        # Ensure chunk is a dictionary. If it's a string, convert it to a message dictionary.
        if isinstance(chunk, str):
            chunk = {"type": "message", "content": chunk}

        content = chunk.get("content", "")
        msg_type = chunk.get("type", "message")
        msg_format = chunk.get("format", None)
        message_id = chunk.get("id", str(uuid.uuid4())) # Get ID if exists, otherwise create new

        # Store message data
        if message_id not in self.message_data:
            self.message_data[message_id] = {"role": "assistant", "content": "", "type": msg_type, "format": msg_format}
        self.message_data[message_id]["content"] += content # Append content to stored message

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

        if chunk.get("role") == "assistant" and msg_type == "message":
            # Don't speak here, will be handled by speak button click
            pass
        self._update_last_assistant_message(message_id)

    def _update_last_assistant_message(self, message_id):
        # Get the full HTML content of the QTextEdit
        full_html = self.output_display.toHtml()

        # Find the placeholder for the assistant's response
        placeholder_tag = "<div id=\"assistant_response_placeholder\"></div>"
        placeholder_index = full_html.rfind(placeholder_tag)

        if placeholder_index != -1:
            # Replace the placeholder with the rendered content
            rendered_content = self._render_markdown_with_code(self.current_assistant_response_buffer, message_id)
            new_html = full_html[:placeholder_index] + rendered_content + full_html[placeholder_index + len(placeholder_tag):]
            self.output_display.setHtml(new_html)
        else:
            # Fallback if placeholder not found (shouldn't happen with current logic)
            self.output_display.setHtml(full_html + self._render_markdown_with_code(self.current_assistant_response_buffer, message_id))

        self.output_display.verticalScrollBar().setValue(self.output_display.verticalScrollBar().maximum())

    def handle_anchor_click(self, url):
        if url.scheme() == "speak":
            message_id = url.host()
            self.speak_message_signal.emit(message_id)

    def show_typing_indicator(self, show):
        if show:
            self.typing_indicator.show()
        else:
            self.typing_indicator.hide()

    def _render_markdown_with_code(self, markdown_text, message_id=None):
        # Use a temporary MarkdownIt instance for rendering to avoid state issues
        md = MarkdownIt()
        html_content = []
        for block in md.parse(markdown_text):
            if block.type == 'fence' and block.info:
                lang = block.info.strip()
                code = block.content
                try:
                    lexer = get_lexer_by_name(lang)
                    formatter = HtmlFormatter(noclasses=True, style="monokai") # Ensure formatter is consistent
                    highlighted_code = highlight(code, lexer, formatter)
                    html_content.append(f'<pre><code class="language-{lang}">{highlighted_code}</code></pre>')
                except ClassNotFound:
                    html_content.append(f'<pre><code class="language-{lang}">{code}</code></pre>')
            elif block.type == 'paragraph':
                html_content.append(f'<p>{block.content}</p>')
            elif block.type == 'text':
                html_content.append(block.content)
            # Add more markdown block types as needed
        
        if message_id:
            return f"<div id='{message_id}' class='assistant-message'>{"".join(html_content)}<a href='speak://{message_id}' style='text-decoration:none;'>🔊</a></div>"
        return "".join(html_content)

    def show_message_context_menu(self, pos):
        cursor = self.output_display.textCursor()
        # Get the HTML element under the cursor
        # This is a simplified approach; a more robust solution might involve
        # parsing the HTML or using a custom QTextDocument layout.
        # For now, we'll rely on the cursor's position to infer the message.
        
        # Move cursor to the start of the block (paragraph or div)
        cursor.select(QTextCursor.BlockUnderCursor)
        block_html = cursor.selectedHtml()
        
        # Extract message ID from the HTML
        message_id = None
        import re
        match = re.search(r'id=["\']([^"\']+)["\']', block_html)
        if match:
            message_id = match.group(1)

        if message_id and message_id in self.message_data:
            message = self.message_data[message_id]
            menu = QMenu(self)

            copy_action = menu.addAction("Copy")
            copy_action.triggered.connect(lambda: self.copy_message_content(message_id))
            
            # Only allow editing/regenerating assistant messages
            if message["role"] == "assistant":
                edit_action = menu.addAction("Edit")
                edit_action.triggered.connect(lambda: self.edit_message(message_id))
                
                regenerate_action = menu.addAction("Regenerate")
                regenerate_action.triggered.connect(lambda: self.regenerate_message(message_id))
            
            delete_action = menu.addAction("Delete")
            delete_action.triggered.connect(lambda: self.delete_message(message_id))

            # Add a "React" submenu
            react_menu = menu.addMenu("React")
            react_menu.addAction("👍 Thumbs Up").triggered.connect(lambda: self.react_to_message(message_id, "👍"))
            react_menu.addAction("👎 Thumbs Down").triggered.connect(lambda: self.react_to_message(message_id, "👎"))
            react_menu.addAction("😂 Laugh").triggered.connect(lambda: self.react_to_message(message_id, "😂"))
            react_menu.addAction("🤔 Thinking").triggered.connect(lambda: self.react_to_message(message_id, "🤔"))

            menu.exec(self.output_display.mapToGlobal(pos))

    def copy_message_content(self, message_id):
        if message_id in self.message_data:
            content = self.message_data[message_id].get("content", "")
            self.output_display.textCursor().insertText(content) # This copies to clipboard
            print(f"Copied message {message_id} content.")

    def edit_message(self, message_id):
        if message_id in self.message_data:
            message = self.message_data[message_id]
            # For simplicity, we'll just print the message content to the input field
            # In a real app, you'd want a more sophisticated editing UI
            self.input_field.setText(message.get("content", ""))
            print(f"Editing message {message_id}.")

    def regenerate_message(self, message_id):
        if message_id in self.message_data:
            message = self.message_data[message_id]
            # Simulate regenerating the message by sending its content as a new command
            self.send_command_signal.emit(message.get("content", ""))
            print(f"Regenerating message {message_id}.")

    def delete_message(self, message_id):
        if message_id in self.message_data:
            # Remove from internal data
            del self.message_data[message_id]
            
            # Remove from display (simplified: clear and re-display history)
            # A more efficient way would be to manipulate the QTextDocument directly
            self.display_history(list(self.message_data.values())) # This will re-render everything
            print(f"Deleted message {message_id}.")

    def react_to_message(self, message_id, reaction):
        if message_id in self.message_data:
            # In a real application, you'd update the message data and re-render
            # For now, just print to console
            print(f"Reacted to message {message_id} with: {reaction}")

    def display_history(self, messages):
        self.output_display.clear()
        self.message_data = {} # Clear existing message data
        full_conversation_html = ""
        for message in messages:
            message_id = str(uuid.uuid4())
            self.message_data[message_id] = message # Store message data
            role = message.get("role", "unknown")
            content = message.get("content", "")
            msg_type = message.get("type", "message")
            msg_format = message.get("format", None)
            
            if role == "user":
                full_conversation_html += f"<div id='{message_id}' class='user-message'><p style='color:#00CED1; font-weight:bold;'>&gt;&gt;&gt; {content}</p></div>"
            elif role == "assistant" and msg_type == "message":
                full_conversation_html += f"<div id='{message_id}' class='assistant-message'><p style='color:#E0E0E0;'>{content}</p></div>"
            elif role == "computer" and msg_type == "console":
                full_conversation_html += f"<div id='{message_id}' class='computer-message'><pre><code class='console'>{content}</code></pre></div>"
            elif role == "assistant" and msg_type == "code":
                full_conversation_html += f"<div id='{message_id}' class='assistant-code-message'><pre><code class='language-{msg_format if msg_format else 'python'}'>{content}</code></pre></div>"
            elif role == "server" and msg_type == "error":
                full_conversation_html += f"<div id='{message_id}' class='error-message'><span style='color:#FF6347; font-weight:bold;'>Error: {content}</span></div>"
            else:
                full_conversation_html += f"<div id='{message_id}' class='unknown-message'><span style='color:#E0E0E0;'>[{role.upper()}:{msg_type}] {content}</span></div>"
        
        self.output_display.setHtml(full_conversation_html)
        self.output_display.verticalScrollBar().setValue(self.output_display.verticalScrollBar().maximum())