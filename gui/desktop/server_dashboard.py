from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTextEdit, QScrollArea, QWidget
from PySide6.QtCore import Qt, QTimer, Signal, QObject
import json
import os
from gui.desktop.api_endpoint_manager_dialog import ApiEndpointManagerDialog

class ServiceMonitor(QObject):
    status_updated = Signal(str, str) # service_name, status
    log_received = Signal(str) # log_message

    def __init__(self, parent=None):
        super().__init__(parent)
        self.services = {
            "RAG Service": "Stopped",
            "TTS Service": "Stopped",
            "STT Service": "Stopped",
            "Workflow Engine": "Stopped",
            "Memory Service": "Stopped",
        }
        self.log_buffer = []

        # Simulate real-time updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._simulate_updates)
        self.timer.start(1000) # Update every second

    def _simulate_updates(self):
        import random
        for service_name in list(self.services.keys()):
            # Simulate health check
            is_healthy = random.choice([True, False])
            if is_healthy:
                new_status = "Running"
                log_message = f"[{service_name}] - Healthy"
            else:
                new_status = "Error"
                log_message = f"[{service_name}] - Error: Service unresponsive!"
                self.log_received.emit(f"ALERT: {service_name} is unhealthy!") # Alert for errors

            self.services[service_name] = new_status
            self.status_updated.emit(service_name, new_status)
            self.log_buffer.append(log_message)
            self.log_received.emit(log_message)

    def get_service_status(self, service_name):
        return self.services.get(service_name, "Unknown")

    def get_all_service_statuses(self):
        return self.services

    def get_logs(self):
        return "\n".join(self.log_buffer)


class ServerDashboard(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Server Management Dashboard")
        self.setGeometry(100, 100, 1000, 700)

        self.config_file = os.path.join(os.path.dirname(__file__), "server_config.json")
        self.auto_start_settings = self.load_config()

        self.service_monitor = ServiceMonitor(self) # Instantiate the monitor
        self.service_monitor.status_updated.connect(self.update_service_status_label)
        self.service_monitor.log_received.connect(self.append_log_message)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.create_service_status_section()
        self.create_log_viewer_section()
        self.create_action_buttons()

        self.update_all_service_statuses() # Initial status update

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                return json.load(f).get("auto_start_services", {})
        return {}

    def save_config(self):
        config = {"auto_start_services": self.auto_start_settings}
        with open(self.config_file, "w") as f:
            json.dump(config, f, indent=4)
        print("Server configuration saved.")

    def create_service_status_section(self):
        status_group_layout = QVBoxLayout()
        status_group_layout.addWidget(QLabel("<h3>Service Status</h3>"))

        self.service_status_labels = {}
        self.services_list = ["RAG Service", "TTS Service", "STT Service", "Workflow Engine", "Memory Service"]
        for service_name in self.services_list:
            h_layout = QHBoxLayout()
            label = QLabel(f"{service_name}: <font color=\"orange\">Unknown</font>")
            self.service_status_labels[service_name] = label
            h_layout.addWidget(label)

            auto_start_checkbox = QCheckBox("Auto-start")
            auto_start_checkbox.setChecked(self.auto_start_settings.get(service_name, False))
            auto_start_checkbox.stateChanged.connect(lambda state, s=service_name: self.toggle_auto_start(s, state))
            h_layout.addWidget(auto_start_checkbox)

            h_layout.addStretch()
            status_group_layout.addLayout(h_layout)

        self.main_layout.addLayout(status_group_layout)

    def update_service_status_label(self, service_name, status):
        label = self.service_status_labels.get(service_name)
        if label:
            color = "green" if status == "Running" else ("red" if status == "Error" else "gray")
            label.setText(f"{service_name}: <font color=\"{color}\">{status}</font>")

    def update_all_service_statuses(self):
        for service_name, status in self.service_monitor.get_all_service_statuses().items():
            self.update_service_status_label(service_name, status)

    def append_log_message(self, message):
        self.log_text_edit.append(message)

    def create_log_viewer_section(self):
        log_group_layout = QVBoxLayout()
        log_group_layout.addWidget(QLabel("<h3>Service Logs</h3>"))

        self.log_text_edit = QTextEdit()
        self.log_text_edit.setReadOnly(True)
        self.log_text_edit.setPlaceholderText("Service logs will appear here...")
        log_group_layout.addWidget(self.log_text_edit)

        self.main_layout.addLayout(log_group_layout)

    def create_action_buttons(self):
        button_layout = QHBoxLayout()

        self.start_all_button = QPushButton("Start All Services")
        self.start_all_button.clicked.connect(self.start_all_services)
        button_layout.addWidget(self.start_all_button)

        self.stop_all_button = QPushButton("Stop All Services")
        self.stop_all_button.clicked.connect(self.stop_all_services)
        button_layout.addWidget(self.stop_all_button)

        self.restart_all_button = QPushButton("Restart All Services")
        self.restart_all_button.clicked.connect(self.restart_all_services)
        button_layout.addWidget(self.restart_all_button)

        self.manage_api_button = QPushButton("Manage API Endpoints")
        self.manage_api_button.clicked.connect(self.manage_api_endpoints)
        button_layout.addWidget(self.manage_api_button)

        self.main_layout.addLayout(button_layout)

    def start_all_services(self):
        print("Starting all services...")
        self.log_text_edit.append("Attempting to start all services...")
        # Placeholder for actual service start logic
        # self.update_service_status() # Simulate status update

    def stop_all_services(self):
        print("Stopping all services...")
        self.log_text_edit.append("Attempting to stop all services...")
        # Placeholder for actual service stop logic
        # self.update_service_status() # Simulate status update

    def restart_all_services(self):
        print("Restarting all services...")
        self.log_text_edit.append("Attempting to restart all services...")
        # Placeholder for actual service restart logic
        # self.update_service_status() # Simulate status update

    def manage_api_endpoints(self):
        dialog = ApiEndpointManagerDialog(self)
        dialog.exec()

if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    dashboard = ServerDashboard()
    dashboard.exec()
    sys.exit(app.exec())