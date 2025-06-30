
import os
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QMenuBar, QMenu, QSplitter, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCharFormat, QTextCursor, QColor, QFont
from interpreter import interpreter
from dotenv import load_dotenv

from .settings_dialog import SettingsDialog
from .profiles_dialog import ProfilesDialog
from .conversation_history import ConversationHistory
from .chat_window import ChatWindow
from .worker import InterpreterWorker
from .right_sidebar import RightSidebar

load_dotenv()

class ColonelKDEApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("The Colonel - Unicorn Commander")
        self.setGeometry(100, 100, 1200, 800) # Increased size for three columns

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        # Left Sidebar for Conversation History
        self.conversation_history = ConversationHistory()
        self.conversation_history.setFixedWidth(200) # Fixed width for sidebar
        self.main_layout.addWidget(self.conversation_history)

        # Main Content Area (Chat Window)
        self.chat_window = ChatWindow()
        self.main_layout.addWidget(self.chat_window)

        # Right Sidebar for Settings/Context
        self.right_sidebar = RightSidebar()
        self.right_sidebar.setFixedWidth(250) # Fixed width for sidebar
        self.main_layout.addWidget(self.right_sidebar)

        # Connect signals and slots
        self.chat_window.send_command_signal.connect(self.send_command)
        self.conversation_history.conversation_selected.connect(self.load_conversation)
        self.right_sidebar.index_button.clicked.connect(self.start_indexing)

        self.create_menu_bar()
        self.apply_stylesheet()

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        # File Menu
        file_menu = menu_bar.addMenu("&File")
        exit_action = file_menu.addAction("&Exit")
        exit_action.triggered.connect(self.close)

        # Options Menu
        options_menu = menu_bar.addMenu("&Options")
        settings_action = options_menu.addAction("&Settings")
        settings_action.triggered.connect(self.show_settings)
        profiles_action = options_menu.addAction("&Profiles")
        profiles_action.triggered.connect(self.show_profiles)

    def show_settings(self):
        dialog = SettingsDialog(self)
        dialog.settings_saved.connect(self.chat_window.output_display.clear) # Clear chat on settings change for now
        dialog.settings_saved.connect(self.right_sidebar.update_session_details) # Update right sidebar
        dialog.exec()

    def show_profiles(self):
        dialog = ProfilesDialog(self)
        dialog.exec()

    def apply_stylesheet(self):
        # Refined dark theme stylesheet with branding colors and subtle animations
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1A1A2E; /* Deep Indigo/Purple */
                color: #E0E0E0;
                border-radius: 8px;
            }
            QWidget#central_widget {
                background-color: #1A1A2E;
            }
            /* Sidebar Styling */
            ConversationHistory, QWidget#right_sidebar {
                background-color: #121220; /* Even darker for sidebars */
                border-right: 1px solid #3A3A5A;
                border-left: 1px solid #3A3A5A;
            }
            QLabel#sidebarLabel {
                color: #00CED1; /* Teal for sidebar labels */
                font-weight: bold;
                padding: 10px;
            }
            QListWidget {
                background-color: #121220;
                color: #E0E0E0;
                border: none;
                padding: 5px;
            }
            QListWidget::item {
                padding: 5px;
            }
            QListWidget::item:selected {
                background-color: #8A2BE2; /* Magic Unicorn Purple */
                color: #FFFFFF;
            }
            QPushButton#chatSendButton, QDialog QPushButton {
                background-color: #8A2BE2; /* BlueViolet - Magic Unicorn Purple */
                color: #FFFFFF;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                transition: background-color 0.3s ease-in-out;
            }
            QPushButton#chatSendButton:hover, QDialog QPushButton:hover {
                background-color: #6A1BA0; /* Darker purple on hover */
            }
            QPushButton#chatSendButton:pressed, QDialog QPushButton:pressed {
                background-color: #4A0F70; /* Even darker when pressed */
            }
            QTextEdit#chatOutputDisplay {
                background-color: #121220; /* Even darker for output area */
                color: #E0E0E0;
                border: 1px solid #3A3A5A;
                padding: 10px;
                font-family: "Fira Code", "Cascadia Code", "monospace";
                font-size: 10pt;
                border-radius: 5px;
            }
            QTextEdit QScrollBar:vertical {
                border: none;
                background: #1A1A2E;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QTextEdit QScrollBar::handle:vertical {
                background: #8A2BE2; /* Magic Unicorn Purple */
                min-height: 20px;
                border-radius: 5px;
            }
            QTextEdit QScrollBar::add-line:vertical, QTextEdit QScrollBar::sub-line:vertical {
                background: none;
            }
            QTextEdit QScrollBar::add-page:vertical, QTextEdit QScrollBar::sub-page:vertical {
                background: none;
            }
            QLineEdit#chatInputField, QDialog QLineEdit {
                background-color: #2C2C4A; /* Slightly lighter dark for input */
                color: #FFFFFF;
                border: 1px solid #5A5A7A;
                padding: 8px;
                font-size: 10pt;
                border-radius: 5px;
                transition: border 0.3s ease-in-out;
            }
            QLineEdit#chatInputField:focus, QDialog QLineEdit:focus {
                border: 1px solid #00CED1; /* Teal glow on focus */
            }
            QMenuBar {
                background-color: #1A1A2E;
                color: #E0E0E0;
            }
            QMenuBar::item:selected {
                background-color: #8A2BE2;
            }
            QMenu {
                background-color: #1A1A2E;
                color: #E0E0E0;
                border: 1px solid #3A3A5A;
            }
            QMenu::item:selected {
                background-color: #8A2BE2;
            }
            QDialog {
                background-color: #1A1A2E;
                color: #E0E0E0;
                border-radius: 8px;
            }
            QDialog QLabel {
                color: #E0E0E0;
            }
            QDialog QCheckBox {
                color: #E0E0E0;
            }
            QComboBox {
                background-color: #2C2C4A;
                color: #FFFFFF;
                border: 1px solid #5A5A7A;
                padding: 5px;
                border-radius: 3px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #5A5A7A;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png); /* You might need to provide an actual arrow image */
            }
        """)

    def send_command(self, command):
        self.worker = InterpreterWorker(command)
        self.worker.new_chunk.connect(self.chat_window.append_output)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.error.connect(self.chat_window.append_output) # Display errors in chat window
        self.worker.memories_extracted.connect(self.right_sidebar.update_memory_summary) # Update memory summary
        self.worker.start()

    def load_conversation(self, file_path):
        try:
            with open(file_path, 'r') as f:
                messages = json.load(f)
            self.chat_window.display_history(messages)
            interpreter.messages = messages # Set interpreter's messages to the loaded history
            interpreter.conversation_filename = os.path.basename(file_path) # Set the current conversation filename
            interpreter.last_messages_count = len(messages) # Update last_messages_count for proper new message tracking
        except Exception as e:
            self.chat_window.append_output(f"Error loading conversation: {e}\n")

    def start_indexing(self):
        self.chat_window.append_output(">>> Starting file indexing...\n")
        # Run indexing in a separate thread to avoid freezing the GUI
        self.indexing_worker = IndexingWorker(os.getcwd()) # Index current working directory
        self.indexing_worker.indexing_finished.connect(self.on_indexing_finished)
        self.indexing_worker.indexing_error.connect(self.on_indexing_error)
        self.indexing_worker.start()

    def on_indexing_finished(self):
        self.chat_window.append_output(">>> File indexing complete!\n")

    def on_indexing_error(self, error_message):
        self.chat_window.append_output(f"Error during indexing: {error_message}\n")
