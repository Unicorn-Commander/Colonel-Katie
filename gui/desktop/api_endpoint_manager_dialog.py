from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
from PySide6.QtCore import Qt
import json
import os
from interpreter.core.credential_manager import CredentialManager

class ApiEndpointManagerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("API Endpoint Management")
        self.setGeometry(200, 200, 800, 500)

        self.config_file = os.path.join(os.path.dirname(__file__), "api_endpoints.json")
        self.endpoints = self.load_endpoints()

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.create_endpoint_table()
        self.create_input_fields()
        self.create_action_buttons()

        self.load_endpoints_to_table()

    def load_endpoints(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                return json.load(f)
        return []

    def save_endpoints(self):
        with open(self.config_file, "w") as f:
            json.dump(self.endpoints, f, indent=4)
        print("API endpoints saved.")

    def create_endpoint_table(self):
        self.endpoint_table = QTableWidget()
        self.endpoint_table.setColumnCount(3)
        self.endpoint_table.setHorizontalHeaderLabels(["Service", "URL", "API Key (Partial)"])
        self.endpoint_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.endpoint_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.endpoint_table.setSelectionMode(QTableWidget.SingleSelection)
        self.endpoint_table.itemSelectionChanged.connect(self.load_selected_endpoint)
        self.main_layout.addWidget(self.endpoint_table)

    def create_input_fields(self):
        form_layout = QVBoxLayout()

        service_layout = QHBoxLayout()
        service_layout.addWidget(QLabel("Service:"))
        self.service_edit = QLineEdit()
        service_layout.addWidget(self.service_edit)
        form_layout.addLayout(service_layout)

        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel("URL:"))
        self.url_edit = QLineEdit()
        self.url_edit.setPlaceholderText("e.g., https://api.openai.com/v1")
        url_layout.addWidget(self.url_edit)
        form_layout.addLayout(url_layout)

        api_key_layout = QHBoxLayout()
        api_key_layout.addWidget(QLabel("API Key:"))
        self.api_key_edit = QLineEdit()
        self.api_key_edit.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.api_key_edit.setPlaceholderText("Enter full API Key (will be stored securely)")
        api_key_layout.addWidget(self.api_key_edit)
        form_layout.addLayout(api_key_layout)

        self.main_layout.addLayout(form_layout)

    def create_action_buttons(self):
        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Add Endpoint")
        self.add_button.clicked.connect(self.add_endpoint)
        button_layout.addWidget(self.add_button)

        self.update_button = QPushButton("Update Endpoint")
        self.update_button.clicked.connect(self.update_endpoint)
        button_layout.addWidget(self.update_button)

        self.delete_button = QPushButton("Delete Endpoint")
        self.delete_button.clicked.connect(self.delete_endpoint)
        button_layout.addWidget(self.delete_button)

        self.clear_button = QPushButton("Clear Fields")
        self.clear_button.clicked.connect(self.clear_fields)
        button_layout.addWidget(self.clear_button)

        self.main_layout.addLayout(button_layout)

    def load_endpoints_to_table(self):
        self.endpoint_table.setRowCount(0)
        for endpoint in self.endpoints:
            row_position = self.endpoint_table.rowCount()
            self.endpoint_table.insertRow(row_position)
            self.endpoint_table.setItem(row_position, 0, QTableWidgetItem(endpoint["service"]))
            self.endpoint_table.setItem(row_position, 1, QTableWidgetItem(endpoint["url"]))
            # Display partial API key for security
            partial_key = CredentialManager.get_api_key(endpoint["service"])
            if partial_key:
                partial_key = partial_key[:4] + "..." + partial_key[-4:]
            else:
                partial_key = ""
            self.endpoint_table.setItem(row_position, 2, QTableWidgetItem(partial_key))

    def add_endpoint(self):
        service = self.service_edit.text().strip()
        url = self.url_edit.text().strip()
        api_key = self.api_key_edit.text().strip()

        if not service or not url:
            QMessageBox.warning(self, "Input Error", "Service and URL cannot be empty.")
            return

        new_endpoint = {"service": service, "url": url}
        self.endpoints.append(new_endpoint)
        self.save_endpoints()
        CredentialManager.set_api_key(service, api_key)
        self.load_endpoints_to_table()
        self.clear_fields()
        QMessageBox.information(self, "Success", "Endpoint added successfully.")

    def update_endpoint(self):
        selected_row = self.endpoint_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Selection Error", "Please select an endpoint to update.")
            return

        service = self.service_edit.text().strip()
        url = self.url_edit.text().strip()
        api_key = self.api_key_edit.text().strip()

        if not service or not url:
            QMessageBox.warning(self, "Input Error", "Service and URL cannot be empty.")
            return

        self.endpoints[selected_row]["service"] = service
        self.endpoints[selected_row]["url"] = url
        if api_key: # Only update API key if a new one is entered
            CredentialManager.set_api_key(service, api_key)

        self.save_endpoints()
        self.load_endpoints_to_table()
        self.clear_fields()
        QMessageBox.information(self, "Success", "Endpoint updated successfully.")

    def delete_endpoint(self):
        selected_row = self.endpoint_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Selection Error", "Please select an endpoint to delete.")
            return

        reply = QMessageBox.question(self, "Confirm Delete", "Are you sure you want to delete this endpoint?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            service_to_delete = self.endpoints[selected_row]["service"]
            del self.endpoints[selected_row]
            self.save_endpoints()
            CredentialManager.delete_api_key(service_to_delete)
            self.load_endpoints_to_table()
            self.clear_fields()
            QMessageBox.information(self, "Success", "Endpoint deleted successfully.")

    def load_selected_endpoint(self):
        selected_row = self.endpoint_table.currentRow()
        if selected_row != -1:
            endpoint = self.endpoints[selected_row]
            self.service_edit.setText(endpoint["service"])
            self.url_edit.setText(endpoint["url"])
            self.api_key_edit.clear() # Clear API key field for security

    def clear_fields(self):
        self.service_edit.clear()
        self.url_edit.clear()
        self.api_key_edit.clear()
        self.endpoint_table.clearSelection()

if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    dialog = ApiEndpointManagerDialog()
    dialog.exec()
    sys.exit(app.exec())