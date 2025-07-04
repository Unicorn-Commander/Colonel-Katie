
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QToolButton, QSizePolicy, QPushButton, QComboBox, QTextEdit, QLineEdit
from PySide6.QtCore import Qt, QPropertyAnimation, QRect, QSize, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication # Import QApplication for processEvents
import os
from interpreter import OpenInterpreter
from .services.web_search import WebSearchService
from .services.rag_manager import RAGManager
from .services.model_manager import ModelManager

try:
    from interpreter.core.config_manager import ConfigManager
except ImportError:
    # Fallback for different open-interpreter versions
    class ConfigManager:
        def __init__(self):
            self.config = {}
        
        def get(self, key, default=None):
            return self.config.get(key, default)
        
        def set(self, key, value):
            self.config[key] = value
from .services.function_registry import FunctionRegistry
from .services.stt_service import STTService
from .services.tts_service import TTSService
from .services.document_storage_service import DocumentStorageService
from .services.permission_service import PermissionService
from .services.memory_service import MemoryService
from .components.document_manager import DocumentManager
from .components.memory_manager_component import MemoryManagerComponent
from .feature_toggles import is_feature_enabled, ENABLE_RAG, ENABLE_WEB_SEARCH, ENABLE_IMAGE_GENERATION, ENABLE_MODEL_BUILDER, ENABLE_MANY_MODELS_CONVERSATIONS

class CollapsibleSection(QWidget):
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.toggle_button = QToolButton(self)
        self.toggle_button.setStyleSheet("QToolButton { border: none; }")
        self.toggle_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(Qt.RightArrow)
        self.toggle_button.setText(title)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(False)

        self.content_area = QFrame(self)
        self.content_area.setMaximumHeight(0)
        self.content_area.setMinimumHeight(0)
        self.content_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.content_area.setStyleSheet("QFrame { background-color: #1A1A2E; border: none; }")

        self.toggle_button.clicked.connect(self.toggle_content)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.addWidget(self.toggle_button)
        self.main_layout.addWidget(self.content_area)

        self.animation = QPropertyAnimation(self.content_area, b"maximumHeight")
        self.animation.setDuration(300) # milliseconds

    def toggle_content(self):
        if self.toggle_button.isChecked():
            self.toggle_button.setArrowType(Qt.DownArrow)
            self.animation.setStartValue(self.content_area.height())
            self.animation.setEndValue(self.content_area.sizeHint().height())
        else:
            self.toggle_button.setArrowType(Qt.RightArrow)
            self.animation.setStartValue(self.content_area.height())
            self.animation.setEndValue(0)
        self.animation.start()

    def set_content_layout(self, layout):
        self.content_area.setLayout(layout)

class RightSidebar(QWidget):
    model_selected_signal = Signal(str)
    send_message_to_chat_signal = Signal(str)
    def __init__(self, interpreter_instance, config_manager, parent=None):
        super().__init__(parent)
        self.interpreter = interpreter_instance
        self.web_search_service = WebSearchService()
        self._rag_manager = None
        self._model_manager = None
        
        self.function_registry = FunctionRegistry()
        self.stt_service = STTService() # Initialize STTService
        self.tts_service = TTSService() # Initialize TTSService
        self.document_storage_service = DocumentStorageService() # Initialize DocumentStorageService
        self.permission_service = PermissionService() # Initialize PermissionService
        self.memory_service = MemoryService() # Initialize MemoryService
        self.config_manager = config_manager # Store ConfigManager instance
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop) # Align content to the top
        self.layout.setContentsMargins(5, 5, 5, 5)

        # Session Details Section
        self.session_details_section = CollapsibleSection("Session Details")
        self.session_details_layout = QVBoxLayout()
        self.session_details_layout.setContentsMargins(10, 5, 10, 5)
        self.session_details_layout.setSpacing(5)

        self.profile_label = QLabel("Profile: N/A")
        self.model_label = QLabel("Model: N/A")
        self.api_key_status_label = QLabel("API Key: Not Set")
        self.model_selection_combo = QComboBox(self)
        self.model_selection_combo.currentIndexChanged.connect(self.on_model_selected)

        self.session_details_layout.addWidget(self.profile_label)
        self.session_details_layout.addWidget(self.model_label)
        self.session_details_layout.addWidget(self.model_selection_combo)
        self.session_details_layout.addWidget(self.api_key_status_label)

        self.model_selected_signal.emit(self.model_selection_combo.currentText())
        self.model_selection_combo.currentIndexChanged.connect(lambda: self.model_selected_signal.emit(self.model_selection_combo.currentText()))

        self.session_details_section.set_content_layout(self.session_details_layout)
        self.layout.addWidget(self.session_details_section)

        # Memory Summary Section (Placeholder for now)
        self.memory_summary_section = CollapsibleSection("Memory Summary")
        self.memory_summary_layout = QVBoxLayout()
        self.memory_summary_layout.setContentsMargins(10, 5, 10, 5)
        self.memory_summary_layout.setSpacing(5)
        self.memory_summary_layout.addWidget(QLabel("Extracted memories will appear here."))
        self.memory_summary_section.set_content_layout(self.memory_summary_layout)
        self.layout.addWidget(self.memory_summary_section)

        # Memory Management Section
        self.memory_management_section = CollapsibleSection("Memory Management")
        self.memory_management_component = MemoryManagerComponent(self.memory_service) # Pass memory service
        self.memory_management_section.set_content_layout(self.memory_management_component.layout)
        self.layout.addWidget(self.memory_management_section)

        # File Indexing Section
        # Knowledge Management Section (Combined File Indexing and RAG Integration)
        self.knowledge_management_section = CollapsibleSection("Knowledge Management")
        self.knowledge_management_layout = QVBoxLayout()
        self.knowledge_management_layout.setContentsMargins(10, 5, 10, 5)
        self.knowledge_management_layout.setSpacing(5)

        self.index_button = QPushButton("Index Project Directory")
        self.index_button.setObjectName("indexButton") # For styling
        self.knowledge_management_layout.addWidget(self.index_button)

        self.load_documents_button = QPushButton("Load Documents")
        self.load_documents_button.clicked.connect(self.load_documents_for_rag)
        self.knowledge_management_layout.addWidget(self.load_documents_button)

        self.document_upload_button = QPushButton("Upload Document (Drag & Drop)")
        self.document_upload_button.setAcceptDrops(True)
        self.document_upload_button.dragEnterEvent = self.dragEnterEvent
        self.document_upload_button.dropEvent = self.dropEvent
        self.knowledge_management_layout.addWidget(self.document_upload_button)

        self.document_list_label = QLabel("Loaded Documents:")
        self.knowledge_management_layout.addWidget(self.document_list_label)

        self.document_list_display = QTextEdit(self)
        self.document_list_display.setReadOnly(True)
        self.document_list_display.setPlaceholderText("No documents loaded yet.")
        self.knowledge_management_layout.addWidget(self.document_list_display)

        # Replace existing document management UI with DocumentManager component
        self.document_manager_component = DocumentManager(self.document_storage_service, self.rag_manager)
        self.knowledge_management_layout.addWidget(self.document_manager_component)

        # Hide old components that exist
        if hasattr(self, 'document_list_label'):
            self.document_list_label.hide()
        if hasattr(self, 'document_list_display'):
            self.document_list_display.hide()
        # Note: Other components were replaced by DocumentManager

        self.knowledge_management_section.set_content_layout(self.knowledge_management_layout)
        self.layout.addWidget(self.knowledge_management_section)

        # Advanced Features Toggle
        self.advanced_features_toggle = QToolButton(self)
        self.advanced_features_toggle.setStyleSheet("QToolButton { border: none; }")
        self.advanced_features_toggle.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.advanced_features_toggle.setArrowType(Qt.RightArrow)
        self.advanced_features_toggle.setText("Show Advanced Features")
        self.advanced_features_toggle.setCheckable(True)
        self.advanced_features_toggle.setChecked(False)
        self.advanced_features_toggle.clicked.connect(self.toggle_advanced_features)
        self.layout.addWidget(self.advanced_features_toggle)

        self.advanced_features_container = QFrame(self)
        self.advanced_features_container.setMaximumHeight(0)
        self.advanced_features_container.setMinimumHeight(0)
        self.advanced_features_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.advanced_features_container.setStyleSheet("QFrame { background-color: #1A1A2E; border: none; }")
        self.layout.addWidget(self.advanced_features_container)

        self.advanced_features_layout = QVBoxLayout(self.advanced_features_container)
        self.advanced_features_layout.setContentsMargins(0, 0, 0, 0)
        self.advanced_features_layout.setSpacing(0)

        self.update_session_details()
        self.update_feature_visibility()
        self.populate_model_selection()

    @property
    def rag_manager(self):
        if self._rag_manager is None:
            self._rag_manager = RAGManager(self.document_storage_service, self.permission_service)
        return self._rag_manager

    @property
    def model_manager(self):
        if self._model_manager is None:
            self._model_manager = ModelManager()
        return self._model_manager

    def toggle_advanced_features(self):
        if self.advanced_features_toggle.isChecked():
            self.advanced_features_toggle.setArrowType(Qt.DownArrow)
            self.advanced_features_container.setMaximumHeight(self.advanced_features_container.sizeHint().height())
        else:
            self.advanced_features_toggle.setArrowType(Qt.RightArrow)
            self.advanced_features_container.setMaximumHeight(0)

        # Web Search Section
        self.web_search_section = CollapsibleSection("Web Search")
        self.web_search_layout = QVBoxLayout()
        self.web_search_layout.setContentsMargins(10, 5, 10, 5)
        self.web_search_layout.setSpacing(5)

        self.web_search_input = QLineEdit(self)
        self.web_search_input.setPlaceholderText("Enter search query...")
        self.web_search_layout.addWidget(self.web_search_input)

        self.web_search_button = QPushButton("Search Web")
        self.web_search_button.clicked.connect(self.perform_web_search)
        self.web_search_layout.addWidget(self.web_search_button)

        self.web_search_results_display = QTextEdit(self)
        self.web_search_results_display.setReadOnly(True)
        self.web_search_results_display.setPlaceholderText("Search results will appear here...")
        self.web_search_layout.addWidget(self.web_search_results_display)

        self.web_search_section.set_content_layout(self.web_search_layout)
        self.layout.addWidget(self.web_search_section)

        # Image Generation Section
        self.image_generation_section = CollapsibleSection("Image Generation")
        self.image_generation_layout = QVBoxLayout()
        self.image_generation_layout.setContentsMargins(10, 5, 10, 5)
        self.image_generation_layout.setSpacing(5)

        self.generate_image_button = QPushButton("Generate Image")
        self.generate_image_button.setObjectName("generateImageButton")
        self.generate_image_button.setToolTip("Generate images using AI (Coming Soon)")
        self.image_generation_layout.addWidget(self.generate_image_button)

        self.image_generation_coming_soon_label = QLabel("Coming Soon!")
        self.image_generation_coming_soon_label.setObjectName("coming-soon")
        self.image_generation_coming_soon_label.setAlignment(Qt.AlignCenter)
        self.image_generation_layout.addWidget(self.image_generation_coming_soon_label)

        self.image_generation_section.set_content_layout(self.image_generation_layout)
        self.layout.addWidget(self.image_generation_section)

        # Model Builder Section
        self.model_builder_section = CollapsibleSection("Model Builder")
        self.model_builder_layout = QVBoxLayout()
        self.model_builder_layout.setContentsMargins(10, 5, 10, 5)
        self.model_builder_layout.setSpacing(5)

        self.open_model_builder_button = QPushButton("Open Model Builder")
        self.open_model_builder_button.setObjectName("openModelBuilderButton")
        self.open_model_builder_button.setToolTip("Build custom AI models (Coming Soon)")
        self.model_builder_layout.addWidget(self.open_model_builder_button)

        self.model_discovery_label = QLabel("Discovered Models:")
        self.model_builder_layout.addWidget(self.model_discovery_label)

        self.model_list_display = QTextEdit(self)
        self.model_list_display.setReadOnly(True)
        self.model_list_display.setPlaceholderText("Models will appear here...")
        self.model_builder_layout.addWidget(self.model_list_display)

        self.model_builder_label = QLabel("Model Builder (Coming Soon)")
        self.model_builder_layout.addWidget(self.model_builder_label)

        self.model_testing_label = QLabel("Model Testing Playground (Coming Soon)")
        self.model_builder_layout.addWidget(self.model_testing_label)

        self.model_performance_label = QLabel("Model Performance Metrics (Coming Soon)")
        self.model_builder_layout.addWidget(self.model_performance_label)

        self.model_comparison_label = QLabel("Model Comparison (Coming Soon)")
        self.model_builder_layout.addWidget(self.model_comparison_label)

        self.model_builder_section.set_content_layout(self.model_builder_layout)
        self.layout.addWidget(self.model_builder_section)

        self.update_session_details()
        self.update_feature_visibility()
        self.populate_model_selection()

    def populate_model_selection(self):
        self.model_selection_combo.clear()
        models = self.model_manager.list_all_models()
        for model in models:
            self.model_selection_combo.addItem(f"{model['name']} ({model['source']})")

    def on_model_selected(self, index):
        selected_model_text = self.model_selection_combo.currentText()
        model_name = selected_model_text.split(" (")[0] # Extract model name
        # In a real application, you'd pass the actual model object or ID
        # to the chat manager, not just the name.
        # For now, we'll just update the label.
        self.model_label.setText(f"Model: {model_name}")
        # Here you would ideally call self.chat_manager.set_current_model(model_name)
        # but chat_manager is in main_window, so we'll need a signal for that.

    def update_feature_visibility(self):
        # Web Search (check if button exists first)
        if hasattr(self, 'web_search_button'):
            if is_feature_enabled(ENABLE_WEB_SEARCH):
                self.web_search_button.setEnabled(True)
                self.web_search_coming_soon_label.hide()
            else:
                self.web_search_button.setEnabled(False)
                self.web_search_coming_soon_label.show()

        # Image Generation (check if button exists first)
        if hasattr(self, 'generate_image_button'):
            if is_feature_enabled(ENABLE_IMAGE_GENERATION):
                self.generate_image_button.setEnabled(True)
                self.image_generation_coming_soon_label.hide()
            else:
                self.generate_image_button.setEnabled(False)
                self.image_generation_coming_soon_label.show()

        # Model Builder (check if button exists first)
        if hasattr(self, 'open_model_builder_button'):
            if is_feature_enabled(ENABLE_MODEL_BUILDER):
                self.open_model_builder_button.setEnabled(True)
                self.model_builder_coming_soon_label.hide()
            else:
                self.open_model_builder_button.setEnabled(False)
                self.model_builder_coming_soon_label.show()

    def update_session_details(self):
        # Update profile
        profile_name = self.config_manager.get("general.default_profile", "default.yaml")
        self.profile_label.setText(f"Profile: {profile_name}")
        self.profile_label.setToolTip(f"Current active profile: {profile_name}")

        # Update LLM model
        current_model = self.config_manager.get("llm.default_model", "N/A")
        self.model_label.setText(f"Model: {current_model}")
        self.model_label.setToolTip(f"Current LLM model: {current_model}")

        # Update API Key Status
        api_key_set = bool(self.config_manager.get(f"api_keys.{current_model.split(': ')[0].lower()}", None))
        self.api_key_status_label.setText(f"API Key: {"Set" if api_key_set else "Not Set"}")
        self.api_key_status_label.setToolTip(f"API Key Status: {"Set" if api_key_set else "Not Set"}")

        # Add tooltips to existing buttons
        self.index_button.setToolTip("Index the project directory for file-aware context.")

    def perform_web_search(self):
        query = self.web_search_input.text()
        if not query:
            self.web_search_results_display.setText("Please enter a search query.")
            return

        self.web_search_results_display.setText("Searching...")
        results = self.web_search_service.search(query)
        if results:
            formatted_results = ""
            for i, result in enumerate(results):
                formatted_results += f"<b>{i+1}. {result.get('title', 'No Title')}</b><br>"
                formatted_results += f"<a href='{result.get('url', '#')}'>{result.get('url', 'No URL')}</a><br>"
                formatted_results += f"{result.get('snippet', 'No Snippet')}<br><br>"
            self.web_search_results_display.setHtml(formatted_results)

            self.add_to_chat_button = QPushButton("Add Results to Chat")
            self.add_to_chat_button.clicked.connect(lambda: self.add_search_results_to_chat(results))
            self.web_search_layout.addWidget(self.add_to_chat_button)

            self.scrape_article_button = QPushButton("Scrape Article & Add to Context")
            self.scrape_article_button.clicked.connect(self.scrape_and_add_to_context)
            self.web_search_layout.addWidget(self.scrape_article_button)

        else:
            self.web_search_results_display.setText("No search results found or an error occurred.")

    def add_search_results_to_chat(self, results):
        formatted_message = "Here are the search results:\n\n"
        for i, result in enumerate(results):
            formatted_message += f"{i+1}. **{result.get('title', 'No Title')}**\n"
            formatted_message += f"URL: {result.get('url', 'No URL')}\n"
            formatted_message += f"Snippet: {result.get('snippet', 'No Snippet')}\n\n"
        self.send_message_to_chat_signal.emit(formatted_message)

    def scrape_and_add_to_context(self):
        # Placeholder for scraping and adding to RAG context
        print("Scraping article and adding to RAG context...")
        # This would typically get the URL from a selected search result
        # For now, simulate with a dummy URL
        dummy_url = "http://example.com"
        article_text = self.web_search_service.scrape_article(dummy_url)
        if article_text:
            self.rag_manager.add_document(article_text, {"source": dummy_url, "type": "scraped_article"})
            print(f"Scraped article from {dummy_url} and added to RAG.")
            self.send_message_to_chat_signal.emit(f"Scraped article from {dummy_url} and added to RAG context.")
        else:
            print(f"Failed to scrape article from {dummy_url}.")
            self.send_message_to_chat_signal.emit(f"Failed to scrape article from {dummy_url}.")

    def load_documents_for_rag(self):
        from PySide6.QtWidgets import QFileDialog
        print("Loading documents for RAG...")
        file_dialog = QFileDialog(self)
        file_paths, _ = file_dialog.getOpenFileNames(self, "Select Documents for RAG", "", "All Files (*.*);;PDF Files (*.pdf);;DOCX Files (*.docx);;Text Files (*.txt);;Markdown Files (*.md);;HTML Files (*.html)")
        if file_paths:
            for file_path in file_paths:
                self.document_processing_status_label.setText(f"Processing: {os.path.basename(file_path)}")
                QApplication.processEvents() # Update GUI
                self._process_document_for_rag(file_path)
            self.document_processing_status_label.setText("Processing Status: Idle")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            self._process_document_for_rag(file_path)
        event.acceptProposedAction()

    def _process_document_for_rag(self, file_path):
        print(f"Processing document for RAG: {file_path}")
        file_extension = os.path.splitext(file_path)[1].lower()
        file_type = "unknown"
        if file_extension == ".pdf":
            text = self.rag_manager.load_pdf(file_path)
            file_type = "pdf"
        elif file_extension == ".docx":
            text = self.rag_manager.load_docx(file_path)
            file_type = "docx"
        elif file_extension == ".txt":
            text = self.rag_manager.load_txt(file_path)
            file_type = "txt"
        elif file_extension == ".md":
            text = self.rag_manager.load_md(file_path)
            file_type = "markdown"
        elif file_extension == ".html":
            text = self.rag_manager.load_html(file_path)
            file_type = "html"
        # Add more file types for code files if needed
        elif file_extension in [".py", ".js", ".ts", ".java", ".cpp", ".h", ".c", ".cs", ".go", ".rs", ".rb", ".php", ".swift", ".kt", ".json", ".xml", ".yaml", ".yml", ".toml", ".ini", ".cfg"]:
            text = self.rag_manager.load_txt(file_path) # Treat code files as plain text for now
            file_type = "code"
        else:
            text = None
            print(f"Unsupported file type for RAG: {file_path}")

        if text:
            self.rag_manager.add_document(text, {"source": file_path, "type": file_type, "file_extension": file_extension})
            self.document_list_display.append(f"- Loaded: {os.path.basename(file_path)} (Type: {file_type})")
            print(f"Document {file_path} added to RAG.")
        else:
            self.document_list_display.append(f"- Failed to load: {os.path.basename(file_path)}")
            print(f"Failed to add document {file_path} to RAG.")

    def update_memory_summary(self, memories):
        # Clear existing memory summary
        for i in reversed(range(self.memory_summary_layout.count())):
            widget = self.memory_summary_layout.itemAt(i).widget()
            if widget is not None:
                self.memory_summary_layout.removeWidget(widget)
                widget.deleteLater()
        
        if memories:
            for memory in memories:
                self.memory_summary_layout.addWidget(QLabel(f"- {memory}"))
        else:
            self.memory_summary_layout.addWidget(QLabel("No extracted memories yet."))

        # Ensure the layout updates correctly after adding/removing widgets
        self.memory_summary_layout.update()
