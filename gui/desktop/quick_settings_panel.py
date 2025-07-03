from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QComboBox, QSpinBox, QPushButton, QCheckBox
from PySide6.QtCore import Qt, Signal
from .services.rag_config import RAGConfig

class QuickSettingsPanel(QWidget):
    settings_changed = Signal(dict)

    def __init__(self, model_manager, parent=None):
        super().__init__(parent)
        self.model_manager = model_manager
        self.setFixedWidth(250) # Fixed width for the slide-out panel
        self.setObjectName("quickSettingsPanel") # For styling

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        # Model Selection
        self.model_label = QLabel("Model:")
        self.model_combo = QComboBox()
        self.populate_models()
        self.model_combo.currentIndexChanged.connect(self._emit_settings_changed)
        self.layout.addWidget(self.model_label)
        self.layout.addWidget(self.model_combo)

        # Temperature Slider
        self.temperature_label = QLabel("Temperature: 0.7")
        self.temperature_slider = QSlider(Qt.Horizontal)
        self.temperature_slider.setRange(0, 100) # 0.0 to 1.0, scaled by 100
        self.temperature_slider.setValue(70) # Default 0.7
        self.temperature_slider.valueChanged.connect(self._update_temperature_label)
        self.temperature_slider.sliderReleased.connect(self._emit_settings_changed)
        self.layout.addWidget(self.temperature_label)
        self.layout.addWidget(self.temperature_slider)

        # Max Tokens SpinBox
        self.max_tokens_label = QLabel("Max Tokens:")
        self.max_tokens_spinbox = QSpinBox()
        self.max_tokens_spinbox.setRange(1, 8192) # Example range
        self.max_tokens_spinbox.setValue(4096) # Default
        self.max_tokens_spinbox.valueChanged.connect(self._emit_settings_changed)
        self.layout.addWidget(self.max_tokens_label)
        self.layout.addWidget(self.max_tokens_spinbox)

        # Language Selection
        self.language_label = QLabel("Language:")
        self.language_combo = QComboBox()
        self.populate_languages()
        self.language_combo.currentIndexChanged.connect(self._emit_settings_changed)
        self.layout.addWidget(self.language_label)
        self.layout.addWidget(self.language_combo)

        # RAG Presets
        self.rag_preset_label = QLabel("RAG Preset:")
        self.rag_preset_combo = QComboBox()
        self.populate_rag_presets()
        self.rag_preset_combo.currentIndexChanged.connect(self._apply_rag_preset)
        self.layout.addWidget(self.rag_preset_label)
        self.layout.addWidget(self.rag_preset_combo)

        # RAG Configuration
        self.rag_config_label = QLabel("RAG Configuration:")
        self.layout.addWidget(self.rag_config_label)

        self.embedding_model_label = QLabel("Embedding Model:")
        self.embedding_model_combo = QComboBox()
        self.embedding_model_combo.addItem("all-MiniLM-L6-v2") # Default
        self.embedding_model_combo.addItem("sentence-transformers/all-mpnet-base-v2") # Example
        self.embedding_model_combo.currentIndexChanged.connect(self._emit_settings_changed)
        self.layout.addWidget(self.embedding_model_label)
        self.layout.addWidget(self.embedding_model_combo)

        self.vector_db_label = QLabel("Vector Database:")
        self.vector_db_combo = QComboBox()
        self.vector_db_combo.addItem("chromadb") # Default
        self.vector_db_combo.addItem("qdrant") # Placeholder
        self.vector_db_combo.addItem("faiss") # Placeholder
        self.vector_db_combo.currentIndexChanged.connect(self._emit_settings_changed)
        self.layout.addWidget(self.vector_db_label)
        self.layout.addWidget(self.vector_db_combo)

        self.chunking_strategy_label = QLabel("Chunking Strategy:")
        self.chunking_strategy_combo = QComboBox()
        self.chunking_strategy_combo.addItem("sliding_window")
        self.chunking_strategy_combo.addItem("semantic")
        self.chunking_strategy_combo.addItem("hierarchical")
        self.chunking_strategy_combo.addItem("code_aware")
        self.chunking_strategy_combo.currentIndexChanged.connect(self._emit_settings_changed)
        self.layout.addWidget(self.chunking_strategy_label)
        self.layout.addWidget(self.chunking_strategy_combo)

        self.chunk_size_label = QLabel("Chunk Size:")
        self.chunk_size_spinbox = QSpinBox()
        self.chunk_size_spinbox.setRange(100, 2000)
        self.chunk_size_spinbox.setValue(500)
        self.chunk_size_spinbox.valueChanged.connect(self._emit_settings_changed)
        self.layout.addWidget(self.chunk_size_label)
        self.layout.addWidget(self.chunk_size_spinbox)

        self.chunk_overlap_label = QLabel("Chunk Overlap:")
        self.chunk_overlap_spinbox = QSpinBox()
        self.chunk_overlap_spinbox.setRange(0, 500)
        self.chunk_overlap_spinbox.setValue(50)
        self.chunk_overlap_spinbox.valueChanged.connect(self._emit_settings_changed)
        self.layout.addWidget(self.chunk_overlap_label)
        self.layout.addWidget(self.chunk_overlap_spinbox)

        self.retrieval_top_k_label = QLabel("Retrieval Top K:")
        self.retrieval_top_k_spinbox = QSpinBox()
        self.retrieval_top_k_spinbox.setRange(1, 20)
        self.retrieval_top_k_spinbox.setValue(5)
        self.retrieval_top_k_spinbox.valueChanged.connect(self._emit_settings_changed)
        self.layout.addWidget(self.retrieval_top_k_label)
        self.layout.addWidget(self.retrieval_top_k_spinbox)

        self.retrieval_similarity_threshold_label = QLabel("Similarity Threshold:")
        self.retrieval_similarity_threshold_slider = QSlider(Qt.Horizontal)
        self.retrieval_similarity_threshold_slider.setRange(0, 100) # 0.0 to 1.0
        self.retrieval_similarity_threshold_slider.setValue(70) # Default 0.7
        self.retrieval_similarity_threshold_slider.valueChanged.connect(self._update_retrieval_similarity_threshold_label)
        self.retrieval_similarity_threshold_slider.sliderReleased.connect(self._emit_settings_changed)
        self.layout.addWidget(self.retrieval_similarity_threshold_label)
        self.layout.addWidget(self.retrieval_similarity_threshold_slider)

        # Global TTS Toggle
        self.tts_toggle = QCheckBox("Enable Text-to-Speech")
        self.tts_toggle.setChecked(True) # Default to enabled
        self.tts_toggle.stateChanged.connect(self._emit_settings_changed)
        self.layout.addWidget(self.tts_toggle)

        # Speech Speed Control
        self.speech_speed_label = QLabel("Speech Speed: 1.0x")
        self.speech_speed_slider = QSlider(Qt.Horizontal)
        self.speech_speed_slider.setRange(50, 200) # 0.5x to 2.0x, scaled by 100
        self.speech_speed_slider.setValue(100) # Default 1.0x
        self.speech_speed_slider.valueChanged.connect(self._update_speech_speed_label)
        self.speech_speed_slider.sliderReleased.connect(self._emit_settings_changed)
        self.layout.addWidget(self.speech_speed_label)
        self.layout.addWidget(self.speech_speed_slider)

        # Speech Pitch Control
        self.speech_pitch_label = QLabel("Speech Pitch: 1.0x")
        self.speech_pitch_slider = QSlider(Qt.Horizontal)
        self.speech_pitch_slider.setRange(50, 150) # 0.5x to 1.5x, scaled by 100
        self.speech_pitch_slider.setValue(100) # Default 1.0x
        self.speech_pitch_slider.valueChanged.connect(self._update_speech_pitch_label)
        self.speech_pitch_slider.sliderReleased.connect(self._emit_settings_changed)
        self.layout.addWidget(self.speech_pitch_label)
        self.layout.addWidget(self.speech_pitch_slider)

        # Wake Word Detection Toggle
        self.wake_word_toggle = QCheckBox("Enable Wake Word (Hey Colonel)")
        self.wake_word_toggle.setChecked(False) # Default to disabled
        self.wake_word_toggle.stateChanged.connect(self._emit_settings_changed)
        self.layout.addWidget(self.wake_word_toggle)

        self.layout.addStretch()

    def populate_models(self):
        self.model_combo.clear()
        models = self.model_manager.list_all_models()
        for model in models:
            self.model_combo.addItem(f"{model['name']} ({model['source']})")

    def populate_languages(self):
        # ISO 639-1 codes for common languages supported by Whisper
        languages = {
            "English": "en",
            "Spanish": "es",
            "French": "fr",
            "German": "de",
            "Italian": "it",
            "Portuguese": "pt",
            "Russian": "ru",
            "Chinese": "zh",
            "Japanese": "ja",
            "Korean": "ko"
        }
        for lang_name, lang_code in languages.items():
            self.language_combo.addItem(lang_name, lang_code)

    def populate_rag_presets(self):
        self.rag_preset_combo.clear()
        presets = RAGConfig.get_presets()
        for name in presets.keys():
            self.rag_preset_combo.addItem(name)

    def _apply_rag_preset(self):
        selected_preset_name = self.rag_preset_combo.currentText()
        presets = RAGConfig.get_presets()
        if selected_preset_name in presets:
            preset_config = presets[selected_preset_name]
            # Apply preset to RAGManager (this signal will be handled by ChatManager)
            settings = self._get_current_settings()
            settings["rag_config"] = preset_config.to_dict()
            self.settings_changed.emit(settings)

    def _update_retrieval_similarity_threshold_label(self, value):
        self.retrieval_similarity_threshold_label.setText(f"Similarity Threshold: {value / 100.0}")

    def _update_speech_speed_label(self, value):
        self.speech_speed_label.setText(f"Speech Speed: {value / 100.0}x")

    def _update_speech_pitch_label(self, value):
        self.speech_pitch_label.setText(f"Speech Pitch: {value / 100.0}x")

    def _update_temperature_label(self, value):
        self.temperature_label.setText(f"Temperature: {value / 100.0}")

    def _emit_settings_changed(self):
        settings = self._get_current_settings()
        self.settings_changed.emit(settings)

    def _get_current_settings(self):
        return {
            "model": self.model_combo.currentText(),
            "temperature": self.temperature_slider.value() / 100.0,
            "max_tokens": self.max_tokens_spinbox.value(),
            "language": self.language_combo.currentData(),
            "tts_enabled": self.tts_toggle.isChecked(),
            "speech_speed": self.speech_speed_slider.value() / 100.0,
            "speech_pitch": self.speech_pitch_slider.value() / 100.0,
            "wake_word_enabled": self.wake_word_toggle.isChecked(),
            "rag_config": {
                "embedding_model_name": self.embedding_model_combo.currentText(),
                "vector_database_type": self.vector_db_combo.currentText(),
                "chunking_strategy": self.chunking_strategy_combo.currentText(),
                "chunk_size": self.chunk_size_spinbox.value(),
                "chunk_overlap": self.chunk_overlap_spinbox.value(),
                "retrieval_top_k": self.retrieval_top_k_spinbox.value(),
                "retrieval_similarity_threshold": self.retrieval_similarity_threshold_slider.value() / 100.0
            }
        }

    def set_settings(self, settings):
        if "model" in settings:
            index = self.model_combo.findText(settings["model"])
            if index != -1:
                self.model_combo.setCurrentIndex(index)
        if "temperature" in settings:
            self.temperature_slider.setValue(int(settings["temperature"] * 100))
        if "max_tokens" in settings:
            self.max_tokens_spinbox.setValue(settings["max_tokens"])
        if "language" in settings:
            index = self.language_combo.findData(settings["language"])
            if index != -1:
                self.language_combo.setCurrentIndex(index)
        if "tts_enabled" in settings:
            self.tts_toggle.setChecked(settings["tts_enabled"])
        if "speech_speed" in settings:
            self.speech_speed_slider.setValue(int(settings["speech_speed"] * 100))
        if "speech_pitch" in settings:
            self.speech_pitch_slider.setValue(int(settings["speech_pitch"] * 100))
        if "wake_word_enabled" in settings:
            self.wake_word_toggle.setChecked(settings["wake_word_enabled"])
        if "rag_config" in settings:
            rag_config_dict = settings["rag_config"]
            self.embedding_model_combo.setCurrentText(rag_config_dict.get("embedding_model_name", "all-MiniLM-L6-v2"))
            self.vector_db_combo.setCurrentText(rag_config_dict.get("vector_database_type", "chromadb"))
            self.chunking_strategy_combo.setCurrentText(rag_config_dict.get("chunking_strategy", "sliding_window"))
            self.chunk_size_spinbox.setValue(rag_config_dict.get("chunk_size", 500))
            self.chunk_overlap_spinbox.setValue(rag_config_dict.get("chunk_overlap", 50))
            self.retrieval_top_k_spinbox.setValue(rag_config_dict.get("retrieval_top_k", 5))
            self.retrieval_similarity_threshold_slider.setValue(int(rag_config_dict.get("retrieval_similarity_threshold", 0.7) * 100))

            # Find the preset in the combo box and set it
            preset_dict = settings["rag_config"]
            for i in range(self.rag_preset_combo.count()):
                preset_name = self.rag_preset_combo.itemText(i)
                if RAGConfig.get_presets()[preset_name].to_dict() == preset_dict:
                    self.rag_preset_combo.setCurrentIndex(i)
                    break
