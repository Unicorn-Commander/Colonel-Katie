from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QPushButton, QLineEdit, QComboBox, QTabWidget, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
from PySide6.QtCore import Qt
from .services.permission_service import PermissionService
import uuid

class PermissionManagementDialog(QDialog):
    def __init__(self, permission_service, parent=None):
        super().__init__(parent)
        self.permission_service = permission_service
        self.setWindowTitle("Permission Management")
        self.setGeometry(100, 100, 800, 600)

        self.main_layout = QVBoxLayout(self)

        self.tab_widget = QTabWidget()
        self.main_layout.addWidget(self.tab_widget)

        self.create_users_tab()
        self.create_roles_permissions_tab()
        self.create_document_acls_tab()
        self.create_kb_acls_tab()
        self.create_audit_log_tab()

        self.tab_widget.addTab(self.users_tab, "Users")
        self.tab_widget.addTab(self.roles_permissions_tab, "Roles & Permissions")
        self.tab_widget.addTab(self.document_acls_tab, "Document ACLs")
        self.tab_widget.addTab(self.kb_acls_tab, "KB ACLs")
        self.tab_widget.addTab(self.audit_log_tab, "Audit Log")

        self.load_data()

    def create_users_tab(self):
        self.users_tab = QWidget()
        layout = QVBoxLayout(self.users_tab)

        # Add User section
        add_user_group = QGroupBox("Add New User")
        add_user_layout = QVBoxLayout(add_user_group)
        
        username_layout = QHBoxLayout()
        username_layout.addWidget(QLabel("Username:"))
        self.new_username_edit = QLineEdit()
        add_user_layout.addLayout(username_layout)
        username_layout.addWidget(self.new_username_edit)

        password_layout = QHBoxLayout()
        password_layout.addWidget(QLabel("Password (Hash):"))
        self.new_password_hash_edit = QLineEdit()
        add_user_layout.addLayout(password_layout)
        password_layout.addWidget(self.new_password_hash_edit)

        role_layout = QHBoxLayout()
        role_layout.addWidget(QLabel("Role:"))
        self.new_user_role_combo = QComboBox()
        self.new_user_role_combo.addItems(["user", "admin", "guest"]) # Example roles
        add_user_layout.addLayout(role_layout)
        role_layout.addWidget(self.new_user_role_combo)

        add_user_button = QPushButton("Add User")
        add_user_button.clicked.connect(self.add_new_user)
        add_user_layout.addWidget(add_user_button)
        layout.addWidget(add_user_group)

        # User List
        layout.addWidget(QLabel("<h3>Existing Users</h3>"))
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(3)
        self.users_table.setHorizontalHeaderLabels(["ID", "Username", "Role"])
        self.users_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.users_table)

    def create_roles_permissions_tab(self):
        self.roles_permissions_tab = QWidget()
        layout = QVBoxLayout(self.roles_permissions_tab)

        layout.addWidget(QLabel("<h3>Roles and Permissions</h3>"))
        self.roles_permissions_table = QTableWidget()
        self.roles_permissions_table.setColumnCount(2)
        self.roles_permissions_table.setHorizontalHeaderLabels(["Role", "Permissions"])
        self.roles_permissions_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.roles_permissions_table)

    def create_document_acls_tab(self):
        self.document_acls_tab = QWidget()
        layout = QVBoxLayout(self.document_acls_tab)

        layout.addWidget(QLabel("<h3>Document Access Control Lists</h3>"))
        self.document_acls_table = QTableWidget()
        self.document_acls_table.setColumnCount(3)
        self.document_acls_table.setHorizontalHeaderLabels(["Document ID", "User ID", "Permission"])
        self.document_acls_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.document_acls_table)

    def create_kb_acls_tab(self):
        self.kb_acls_tab = QWidget()
        layout = QVBoxLayout(self.kb_acls_tab)

        layout.addWidget(QLabel("<h3>Knowledge Base Access Control Lists</h3>"))
        self.kb_acls_table = QTableWidget()
        self.kb_acls_table.setColumnCount(3)
        self.kb_acls_table.setHorizontalHeaderLabels(["KB ID", "User ID", "Permission"])
        self.kb_acls_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.kb_acls_table)

    def create_audit_log_tab(self):
        self.audit_log_tab = QWidget()
        layout = QVBoxLayout(self.audit_log_tab)

        layout.addWidget(QLabel("<h3>Audit Log</h3>"))
        self.audit_log_table = QTableWidget()
        self.audit_log_table.setColumnCount(6)
        self.audit_log_table.setHorizontalHeaderLabels(["Timestamp", "User ID", "Action", "Resource Type", "Resource ID", "Details"])
        self.audit_log_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.audit_log_table)

    def load_data(self):
        self.load_users()
        self.load_roles_permissions()
        self.load_document_acls()
        self.load_kb_acls()
        self.load_audit_log()

    def load_users(self):
        users = self.permission_service.get_all_users() # Assuming this method exists
        self.users_table.setRowCount(len(users))
        for row_idx, user in enumerate(users):
            self.users_table.setItem(row_idx, 0, QTableWidgetItem(user["id"]))
            self.users_table.setItem(row_idx, 1, QTableWidgetItem(user["username"]))
            self.users_table.setItem(row_idx, 2, QTableWidgetItem(user["role"]))

    def load_roles_permissions(self):
        # Placeholder: In a real app, you'd fetch roles and their assigned permissions
        self.roles_permissions_table.setRowCount(3)
        self.roles_permissions_table.setItem(0, 0, QTableWidgetItem("admin"))
        self.roles_permissions_table.setItem(0, 1, QTableWidgetItem("all"))
        self.roles_permissions_table.setItem(1, 0, QTableWidgetItem("user"))
        self.roles_permissions_table.setItem(1, 1, QTableWidgetItem("read, write"))
        self.roles_permissions_table.setItem(2, 0, QTableWidgetItem("guest"))
        self.roles_permissions_table.setItem(2, 1, QTableWidgetItem("read"))

    def load_document_acls(self):
        # Placeholder: Fetch document ACLs
        self.document_acls_table.setRowCount(0)

    def load_kb_acls(self):
        # Placeholder: Fetch knowledge base ACLs
        self.kb_acls_table.setRowCount(0)

    def load_audit_log(self):
        logs = self.permission_service.get_audit_log()
        self.audit_log_table.setRowCount(len(logs))
        for row_idx, log in enumerate(logs):
            self.audit_log_table.setItem(row_idx, 0, QTableWidgetItem(log["timestamp"]))
            self.audit_log_table.setItem(row_idx, 1, QTableWidgetItem(log["user_id"]))
            self.audit_log_table.setItem(row_idx, 2, QTableWidgetItem(log["action"]))
            self.audit_log_table.setItem(row_idx, 3, QTableWidgetItem(log["resource_type"]))
            self.audit_log_table.setItem(row_idx, 4, QTableWidgetItem(log["resource_id"]))
            self.audit_log_table.setItem(row_idx, 5, QTableWidgetItem(str(log["details"])))

    def add_new_user(self):
        username = self.new_username_edit.text()
        password_hash = self.new_password_hash_edit.text()
        role = self.new_user_role_combo.currentText()

        if not username or not password_hash:
            QMessageBox.warning(self, "Input Error", "Username and Password cannot be empty.")
            return

        user_id = str(uuid.uuid4())
        if self.permission_service.add_user(user_id, username, password_hash, role):
            QMessageBox.information(self, "Success", f"User {username} added successfully.")
            self.new_username_edit.clear()
            self.new_password_hash_edit.clear()
            self.load_users()
        else:
            QMessageBox.warning(self, "Error", f"Failed to add user {username}.")