from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QTextCharFormat, QTextCursor, QColor, QFont
from markdown_it import MarkdownIt
from pygments import highlight
from pygments.lexers import get_lexer_by_name, ClassNotFound
from pygments.formatters import HtmlFormatter

class ChatWindow(QWidget):
    send_command_signal = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)
        self.output_display.setObjectName("chatOutputDisplay") # For styling
        self.layout.addWidget(self.output_display)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type your command here...")
        self.input_field.returnPressed.connect(self.send_command)
        self.input_field.setObjectName("chatInputField") # For styling
        self.layout.addWidget(self.input_field)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_command)
        self.send_button.setObjectName("chatSendButton") # For styling
        self.layout.addWidget(self.send_button)

        self.in_code_block = False # State variable for code block formatting

    def send_command(self):
        command = self.input_field.text()
        if not command.strip():
            return

        # Display user command
        cursor = self.output_display.textCursor()
        format_user_input = QTextCharFormat()
        format_user_input.setForeground(QColor("#00CED1")) # Teal for user input
        format_user_input.setFontWeight(QFont.Bold)
        cursor.insertText(f">>> {command}\n", format_user_input)
        self.output_display.setTextCursor(cursor)

        self.input_field.clear()
        self.send_command_signal.emit(command)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)
        self.output_display.setObjectName("chatOutputDisplay") # For styling
        self.layout.addWidget(self.output_display)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type your command here...")
        self.input_field.returnPressed.connect(self.send_command)
        self.input_field.setObjectName("chatInputField") # For styling
        self.layout.addWidget(self.input_field)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_command)
        self.send_button.setObjectName("chatSendButton") # For styling
        self.layout.addWidget(self.send_button)

        self.md = MarkdownIt()
        self.formatter = HtmlFormatter(noclasses=True, style="monokai") # Using 'monokai' for dark theme
        self.current_assistant_response_buffer = ""
        self.in_code_block = False # State variable for code block formatting
        self.code_lang = "python" # Default language for code blocks

    def send_command(self):
        command = self.input_field.text()
        if not command.strip():
            return

        # Display user command
        self.output_display.append(f"<p style='color:#00CED1; font-weight:bold;'>&gt;&gt;&gt; {command}</p>")
        self.input_field.clear()
        self.send_command_signal.emit(command)

        # Clear buffer for new assistant response
        self.current_assistant_response_buffer = ""
        # Add a placeholder for the assistant's response
        self.output_display.append("<p id='assistant_response_placeholder'></p>")

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

    def _render_markdown_with_code(self, text):
        # This function processes markdown and highlights code blocks
        # It needs to handle the streaming nature, so it processes the current buffer
        rendered_html = ""
        temp_md = MarkdownIt() # Use a temporary MarkdownIt instance for rendering
        
        # Pygments formatter for code blocks
        def highlight_code(lexer_name, code):
            try:
                lexer = get_lexer_by_name(lexer_name)
                return highlight(code, lexer, self.formatter)
            except ClassNotFound:
                return f"<pre>{code}</pre>" # Fallback if lexer not found
            except Exception as e:
                return f"<pre>Error highlighting: {e}\n{code}</pre>"

        # Custom renderer for code blocks
        temp_md.add_render_rule("fence", lambda tokens, idx, options, env: highlight_code(tokens[idx].info, tokens[idx].content))

        # Render the markdown
        rendered_html = temp_md.render(text)
        return rendered_html

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