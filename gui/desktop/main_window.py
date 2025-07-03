
import os
import json
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QMenuBar, QSplitter, QLabel, QSystemTrayIcon
from PySide6.QtGui import QTextCharFormat, QTextCursor, QColor, QFont, QAction, QIcon, QKeySequence
from PySide6.QtWidgets import QMenu
from PySide6.QtCore import Qt
from interpreter import OpenInterpreter
from dotenv import load_dotenv

from .feature_toggles import is_feature_enabled, ENABLE_RAG, ENABLE_MANY_MODELS_CONVERSATIONS
from .modern_theme import MODERN_STYLESHEET

from .settings_dialog import SettingsDialog
from .profiles_dialog import ProfilesDialog
from .conversation_history import ConversationHistory
from .chat_window import ChatWindow
from .worker import InterpreterWorker, IndexingWorker
from .right_sidebar import RightSidebar
from .services.model_manager import ModelManager
from .services.chat_manager import ChatManager
from .services.global_config import GlobalConfig
from .agent_builder_dialog import AgentBuilderDialog
from .components.model_selector import ModelSelector

load_dotenv()

class ColonelKDEApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialize OpenInterpreter and services
        self.interpreter = OpenInterpreter()
        self.model_manager = ModelManager()
        self.chat_manager = ChatManager(self.model_manager, self.interpreter)
        
        self.setWindowTitle("Colonel Katie (LtCol Katie) - AI Assistant")
        self.setMinimumSize(800, 600) # Set minimum window size
        self.setGeometry(100, 100, 1200, 800) # Increased size for three columns
        self.setWindowIcon(QIcon("/home/ucadmin/Development/Colonel-Katie/colonel-katie-icon.png"))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(15)

        # Use QSplitter for resizable sections
        self.splitter = QSplitter(Qt.Horizontal)
        self.main_layout.addWidget(self.splitter)

        # Left Sidebar for Conversation History
        self.conversation_history = ConversationHistory()
        self.conversation_history.setFixedWidth(200) # Fixed width for sidebar
        self.splitter.addWidget(self.conversation_history)

        # Right Sidebar for Settings/Context (create first so chat_window can reference it)
        self.right_sidebar = RightSidebar(self.interpreter)
        self.right_sidebar.setFixedWidth(200) # Fixed width for sidebar

        # Main Content Area (Chat Window)
        self.chat_window = ChatWindow(self.chat_manager, self.right_sidebar.function_registry)
        self.splitter.addWidget(self.chat_window)
        
        # Add right sidebar to splitter
        self.splitter.addWidget(self.right_sidebar)

        # Set initial sizes for the splitter sections
        self.splitter.setSizes([200, 800, 200]) # Example sizes

        # Connect signals and slots
        self.chat_window.send_command_signal.connect(self.send_command)
        self.conversation_history.conversation_selected.connect(self.load_conversation)
        self.right_sidebar.index_button.clicked.connect(self.start_indexing)
        self.right_sidebar.model_selected_signal.connect(self.chat_manager.set_current_model)
        self.right_sidebar.send_message_to_chat_signal.connect(self.chat_window.append_output)

        # Connect resize event for responsive design
        self.resizeEvent = self.on_resize_event

        self.create_menu_bar()
        self.apply_stylesheet()

    def on_resize_event(self, event):
        # Auto-collapse sidebars on narrow screens
        if self.width() < 1200:
            self.conversation_history.hide()
            self.right_sidebar.hide()
        else:
            self.conversation_history.show()
            self.right_sidebar.show()
        super().resizeEvent(event)

        # Example of using a feature toggle
        if is_feature_enabled(ENABLE_RAG):
            print("RAG feature is enabled!")
        else:
            print("RAG feature is disabled.")

        # System Tray Icon - Colonel Katie
        self.tray_icon = QSystemTrayIcon(self)
        katie_icon = QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "colonel-katie-icon.png"))
        self.tray_icon.setIcon(katie_icon)
        self.tray_icon.setToolTip("Colonel Katie (LtCol Katie) - Your AI Assistant")

        tray_menu = QMenu()
        
        # Main actions
        show_hide_action = QAction("Show/Hide Colonel Katie", self)
        show_hide_action.triggered.connect(self.toggle_visibility)
        tray_menu.addAction(show_hide_action)
        
        # Quick Chat action (for future implementation)
        quick_chat_action = QAction("Quick Chat (Ctrl+Space)", self)
        quick_chat_action.setEnabled(False)  # Placeholder for now
        tray_menu.addAction(quick_chat_action)
        
        tray_menu.addSeparator()
        
        # Settings
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.show_settings)
        tray_menu.addAction(settings_action)
        
        tray_menu.addSeparator()
        
        # About
        about_action = QAction("About Colonel Katie", self)
        about_action.triggered.connect(self.show_about_dialog)
        tray_menu.addAction(about_action)
        
        # Quit
        quit_action = QAction("Quit Colonel Katie", self)
        quit_action.triggered.connect(self.close)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def toggle_visibility(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.raise_()
            self.activateWindow()
    
    def show_about_dialog(self):
        from PySide6.QtWidgets import QMessageBox
        about = QMessageBox(self)
        about.setWindowTitle("About Colonel Katie")
        about.setTextFormat(Qt.RichText)
        about.setText("""
        <h2>Colonel Katie (LtCol Katie)</h2>
        <p><b>Your Personal AI Assistant</b></p>
        <p>A powerful AI assistant built on The Colonel codebase with advanced features:</p>
        <ul>
        <li>Multi-model conversations</li>
        <li>RAG document processing</li>
        <li>Web search integration</li>
        <li>Quick chat overlay (Ctrl+Space)</li>
        <li>System tray integration</li>
        </ul>
        <p><i>Serving you with honor and efficiency!</i> 🦄⚡</p>
        """)
        about.setStandardButtons(QMessageBox.Ok)
        about.exec()

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        # File Menu
        file_menu = menu_bar.addMenu("&File")
        exit_action = file_menu.addAction("&Exit")
        exit_action.triggered.connect(self.close)
        exit_action.setToolTip("Exit the application")
        exit_action.setShortcut(QKeySequence.Quit)

        # Options Menu (Settings and Profiles will be moved to a dedicated settings page later)
        options_menu = menu_bar.addMenu("&Options")

        many_models_action = options_menu.addAction("Many Models Conversations")
        many_models_action.setToolTip("Engage with multiple models simultaneously (Coming Soon)")
        if not is_feature_enabled(ENABLE_MANY_MODELS_CONVERSATIONS):
            many_models_action.setEnabled(False)

        agent_builder_action = options_menu.addAction("Agent Builder")
        agent_builder_action.triggered.connect(self.show_agent_builder)
        agent_builder_action.setToolTip("Create and manage AI agent profiles")

    def show_settings(self):
        dialog = SettingsDialog(self)
        dialog.settings_saved.connect(self.chat_window.output_display.clear) # Clear chat on settings change for now
        dialog.settings_saved.connect(self.right_sidebar.update_session_details) # Update right sidebar
        dialog.exec()

    def show_profiles(self):
        dialog = ProfilesDialog(self)
        dialog.exec()

    def show_agent_builder(self):
        dialog = AgentBuilderDialog(self)
        dialog.exec()

    def apply_modern_stylesheet(self):
        """Apply cutting-edge modern theme"""
        self.setStyleSheet(MODERN_STYLESHEET)
    
    def apply_old_stylesheet(self):
        # Legacy stylesheet - replaced by modern theme
        return
    
    def apply_stylesheet(self):
        """Use the modern cutting-edge theme"""
        self.apply_modern_stylesheet()
    
    def apply_stylesheet_old(self):
        # This method is disabled - contains old stylesheet
        return
        #         self.setStyleSheet("""
        #             QMainWindow {
        #                 background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
        #                     stop:0 #0a0a0f, stop:0.5 #1a1a2e, stop:1 #0f0f1a);
        #                 color: #f8f9fa;
        #                 border-radius: 12px;
        #                 font-family: "Inter", "SF Pro Display", "Segoe UI Variable", "Helvetica Neue", system-ui, sans-serif;
        #                 font-size: 11pt;
        #                 font-weight: 400;
        #                 letter-spacing: -0.01em;
        #             }
        #             QWidget#central_widget {
        #                 background: transparent;
        #                 border-radius: 12px;
        #             }
        #             /* Sidebar Styling - Glass morphism effect */
        #             ConversationHistory, QWidget#right_sidebar {
        #                 background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        #                     stop:0 rgba(255, 255, 255, 0.05),
        #                     stop:1 rgba(255, 255, 255, 0.02));
        #                 border: 1px solid rgba(255, 255, 255, 0.1);
        #                 border-radius: 16px;
        #                 backdrop-filter: blur(20px);
        #                 margin: 8px;
        #             }
        #             QLabel#sidebarLabel {
        #                 color: #00CED1; /* Teal for sidebar labels */
        #                 font-weight: bold;
        #                 padding: 10px;
        #             }
        #             QListWidget {
        #                 background-color: #121220;
        #                 color: #E0E0E0;
        #                 border: none;
        #                 padding: 5px;
        #             }
        #             QListWidget::item {
        #                 padding: 8px; /* Increased padding */
        #                 border-radius: 4px;
        #                 margin-bottom: 3px;
        #             }
        #             QListWidget::item:selected {
        #                 background-color: #8A2BE2; /* Magic Unicorn Purple */
        #                 color: #FFFFFF;
        #             }
        #             QListWidget::item:hover {
        #                 background-color: #1A1A2E; /* Subtle hover effect */
        #             }
        #             QPushButton, QDialog QPushButton {
        #                 background-color: #8A2BE2; /* BlueViolet - Magic Unicorn Purple */
        #                 color: #FFFFFF;
        #                 border: none;
        #                 padding: 12px 24px; /* Increased padding */
        #                 border-radius: 6px; /* More rounded corners */
        #                 font-weight: bold;
        #                 transition: background-color 0.3s ease-in-out, transform 0.1s ease-in-out;
        #             }
        #             QPushButton:hover, QDialog QPushButton:hover {
        #                 background-color: #6A1BA0; /* Darker purple on hover */
        #                 transform: translateY(-1px); /* Subtle lift effect */
        #             }
        #             QPushButton:pressed, QDialog QPushButton:pressed {
        #                 background-color: #4A0F70; /* Even darker when pressed */
        #                 transform: translateY(0); /* Reset lift */
        #             }
        #             QPushButton:disabled {
        #                 background-color: #3A3A5A;
        #                 color: #808080;
        #             }
        #             QTextEdit#chatOutputDisplay {
        #                 background-color: #121220; /* Even darker for output area */
        #                 color: #E0E0E0;
        #                 border: 1px solid #3A3A5A;
        #                 padding: 15px; /* Increased padding */
        #                 font-family: "JetBrains Mono", "Fira Code", monospace; /* Modern monospace font */
        #                 font-size: 10pt;
        #                 border-radius: 8px; /* More rounded corners */
        #             }
        #             QTextEdit QScrollBar:vertical {
        #                 border: none;
        #                 background: #1A1A2E;
        #                 width: 12px; /* Wider scrollbar */
        #                 margin: 0px;
        #             }
        #             QTextEdit QScrollBar::handle:vertical {
        #                 background: #8A2BE2; /* Magic Unicorn Purple */
        #                 min-height: 30px;
        #                 border-radius: 6px;
        #             }
        #             QTextEdit QScrollBar::add-line:vertical, QTextEdit QScrollBar::sub-line:vertical {
        #                 background: none;
        #             }
        #             QTextEdit QScrollBar::add-page:vertical, QTextEdit QScrollBar::sub-page:vertical {
        #                 background: none;
        #             }
        #             QLineEdit#chatInputField, QDialog QLineEdit {
        #                 background-color: #2C2C4A; /* Slightly lighter dark for input */
        #                 color: #FFFFFF;
        #                 border: 1px solid #5A5A7A;
        #                 padding: 10px; /* Increased padding */
        #                 font-size: 10pt;
        #                 border-radius: 6px; /* More rounded corners */
        #                 transition: border-color 0.3s ease-in-out;
        #             }
        #             QLineEdit#chatInputField:focus, QDialog QLineEdit:focus {
        #                 border: 1px solid #00CED1; /* Teal glow on focus */
        #             }
        #             QMenuBar {
        #                 background-color: #1A1A2E;
        #                 color: #E0E0E0;
        #             }
        #             QMenuBar::item:selected {
        #                 background-color: #8A2BE2;
        #             }
        #             QMenu {
        #                 background-color: #1A1A2E;
        #                 color: #E0E0E0;
        #                 border: 1px solid #3A3A5A;
        #             }
        #             QMenu::item:selected {
        #                 background-color: #8A2BE2;
        #             }
        #             QDialog {
        #                 background-color: #1A1A2E;
        #                 color: #E0E0E0;
        #                 border-radius: 8px;
        #             }
        #             QDialog QLabel {
        #                 color: #E0E0E0;
        #             }
        #             QDialog QCheckBox {
        #                 color: #E0E0E0;
        #             }
        #             QComboBox {
        #                 background-color: #2C2C4A;
        #                 color: #FFFFFF;
        #                 border: 1px solid #5A5A7A;
        #                 padding: 5px;
        #                 border-radius: 3px;
        #             }
        #             QComboBox::drop-down {
        #                 subcontrol-origin: padding;
        #                 subcontrol-position: top right;
        #                 width: 20px;
        #                 border-left-width: 1px;
        #                 border-left-color: #5A5A7A;
        #                 border-left-style: solid;
        #                 border-top-right-radius: 3px;
        #                 border-bottom-right-radius: 3px;
        #             }
        #             QComboBox::down-arrow {
        #                 image: url(down_arrow.png); /* You might need to provide an actual arrow image */
        #             }
        #             /* Coming Soon Labels */
        #             QLabel#coming-soon {
        #                 color: rgba(255, 255, 255, 0.5);
        #                 font-style: italic;
        #                 font-weight: 300;
        #                 font-size: 9pt;
        #             }
        #             
        #             /* Collapsible Section Headers */
        #             QToolButton {
        #                 background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        #                     stop:0 rgba(255, 255, 255, 0.05),
        #                     stop:1 rgba(255, 255, 255, 0.02));
        #                 border: 1px solid rgba(255, 255, 255, 0.1);
        #                 border-radius: 8px;
        #                 padding: 12px 16px;
        #                 font-weight: 600;
        #                 font-size: 10pt;
        #                 color: #f8f9fa;
        #                 text-align: left;
        #             }
        #             QToolButton:hover {
        #                 background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        #                     stop:0 rgba(255, 255, 255, 0.08),
        #                     stop:1 rgba(255, 255, 255, 0.04));
        #             }
        #             
        #             /* Tooltips */
        #             QToolTip {
        #                 background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        #                     stop:0 rgba(10, 10, 15, 0.95),
        #                     stop:1 rgba(26, 26, 46, 0.95));
        #                 color: #f8f9fa;
        #                 border: 1px solid rgba(255, 255, 255, 0.1);
        #                 border-radius: 8px;
        #                 padding: 8px 12px;
        #                 font-size: 10pt;
        #                 backdrop-filter: blur(20px);
        #             }
        #         \"\"\" )
        # 
    def send_command(self, command):
        try:
            print(f"MainWindow: Received command: {command}")
            self.worker = InterpreterWorker(self.interpreter, command)
            print(f"MainWindow: Initialized InterpreterWorker: {self.worker}")
            self.worker.new_chunk.connect(self.chat_window.append_output)
            print("MainWindow: Connected worker.new_chunk to chat_window.append_output.")
            self.worker.finished.connect(self.worker.deleteLater)
            print("MainWindow: Connected worker.finished to worker.deleteLater.")
            self.worker.finished.connect(self.update_connection_status)
            self.worker.error.connect(self.chat_window.append_output) # Display errors in chat window
            print("MainWindow: Connected worker.error to chat_window.append_output.")
            self.worker.error.connect(self.update_connection_status)
            self.worker.memories_extracted.connect(self.right_sidebar.update_memory_summary) # Update memory summary
            self.worker.start()
            print("MainWindow: Started InterpreterWorker.")
            self.connection_status_label.setText("Status: Processing...")
        except Exception as e:
            self.chat_window.append_output({"type": "error", "content": f"Error sending command from main window: {e}\n"})
            self.connection_status_label.setText("Status: Error")

    def update_connection_status(self):
        if self.worker.isRunning():
            self.connection_status_label.setText("Status: Processing...")
        else:
            self.connection_status_label.setText("Status: Idle")

    def load_conversation(self, file_path):
        try:
            with open(file_path, 'r') as f:
                messages = json.load(f)
            self.chat_window.display_history(messages)
            self.interpreter.messages = messages # Set interpreter's messages to the loaded history
            self.interpreter.conversation_filename = os.path.basename(file_path) # Set the current conversation filename
            self.interpreter.last_messages_count = len(messages) # Update last_messages_count for proper new message tracking
        except Exception as e:
            self.chat_window.append_output({"type": "error", "content": f"Error loading conversation: {e}\n"})

    def start_indexing(self):
        self.chat_window.append_output({"type": "message", "content": ">>> Starting file indexing...\n"})
        # Run indexing in a separate thread to avoid freezing the GUI
        self.indexing_worker = IndexingWorker(self.interpreter, os.getcwd()) # Index current working directory
        self.indexing_worker.indexing_finished.connect(self.on_indexing_finished)
        self.indexing_worker.indexing_error.connect(self.on_indexing_error)
        self.indexing_worker.start()

    def on_indexing_finished(self):
        self.chat_window.append_output({"type": "message", "content": ">>> File indexing complete!\n"})

    def on_indexing_error(self, error_message):
        self.chat_window.append_output({"type": "error", "content": f"Error during indexing: {error_message}\n"})

    def show_splash_screen(self):
        # Placeholder for professional splash screen with progress bar
        print("Showing splash screen...")

    def initialize_services_async(self):
        # Placeholder for async service initialization with status updates
        print("Initializing services asynchronously...")

    def lazy_load_components(self):
        # Placeholder for lazy loading of non-essential components
        print("Lazy loading components...")

    def cache_data(self):
        # Placeholder for caching frequently accessed data
        print("Caching data...")

    def reduce_memory_footprint(self):
        # Placeholder for reducing initial memory footprint
        print("Reducing initial memory footprint...")

    def handle_network_failure(self, error_message):
        # Placeholder for automatic retry mechanisms for network failures
        print(f"Network failure: {error_message}. Attempting retry...")

    def provide_recovery_suggestions(self, error_type):
        # Placeholder for recovery suggestions for common issues
        print(f"Providing recovery suggestions for {error_type}...")

    def toggle_debug_mode(self):
        # Placeholder for debug mode toggle for advanced users
        print("Toggling debug mode...")

    def graceful_degradation(self, service_name):
        # Placeholder for graceful degradation when services unavailable
        print(f"Graceful degradation for {service_name}...")
