from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QListWidget, QLabel, QComboBox, QPushButton
from PySide6.QtCore import Signal, Qt

class ModelSelector(QWidget):
    model_selected = Signal(str)

    def __init__(self, model_manager, parent=None):
        super().__init__(parent)
        self.model_manager = model_manager
        self.layout = QVBoxLayout(self)

        # Search Bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search models...")
        self.search_input.textChanged.connect(self.filter_models)
        self.layout.addWidget(self.search_input)

        # Provider Filter (Coming Soon)
        self.provider_filter_combo = QComboBox()
        self.provider_filter_combo.addItem("All Providers")
        self.provider_filter_combo.setEnabled(False) # Placeholder for future functionality
        self.layout.addWidget(self.provider_filter_combo)

        # Model List
        self.model_list_widget = QListWidget()
        self.model_list_widget.itemClicked.connect(self.on_model_selected)
        self.layout.addWidget(self.model_list_widget)

        # Model Details (Coming Soon)
        self.model_details_label = QLabel("Select a model to see details and configuration options.")
        self.model_details_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.model_details_label)

        self.populate_model_list()

    def populate_model_list(self):
        self.model_list_widget.clear()
        models = self.model_manager.list_all_models()
        for model in models:
            self.model_list_widget.addItem(f"{model['name']} ({model['source']})")

    def filter_models(self, text):
        # This will be implemented later to filter the list based on search text and provider
        pass

    def on_model_selected(self, item):
        model_name = item.text().split(" (")[0]
        self.model_selected.emit(model_name)
        self.model_details_label.setText(f"Selected Model: {model_name}\nDetails and configuration options will appear here.")

if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    import sys
    from services.model_manager import ModelManager

    app = QApplication(sys.argv)
    model_manager = ModelManager() # Create a dummy ModelManager for testing
    selector = ModelSelector(model_manager)
    selector.show()
    sys.exit(app.exec())