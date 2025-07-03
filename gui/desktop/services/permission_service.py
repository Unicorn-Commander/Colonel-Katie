import sqlite3
import json
import os
from datetime import datetime

class PermissionService:
    def __init__(self, db_path="~/.colonel-katie/permissions.db"):
        self.db_path = os.path.expanduser(db_path)
        self._initialize_db()

    def _initialize_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'user'
            )
        """)

        # Roles table (optional, for predefined roles)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS roles (
                name TEXT PRIMARY KEY,
                description TEXT
            )
        """)

        # Permissions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS permissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT
            )
        """)

        # Role-Permissions many-to-many table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS role_permissions (
                role_name TEXT NOT NULL,
                permission_name TEXT NOT NULL,
                PRIMARY KEY (role_name, permission_name),
                FOREIGN KEY (role_name) REFERENCES roles(name) ON DELETE CASCADE,
                FOREIGN KEY (permission_name) REFERENCES permissions(name) ON DELETE CASCADE
            )
        """)

        # Document ACLs (Access Control Lists)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS document_acls (
                document_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                permission_name TEXT NOT NULL,
                PRIMARY KEY (document_id, user_id, permission_name),
                FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (permission_name) REFERENCES permissions(name) ON DELETE CASCADE
            )
        """)

        # Knowledge Base ACLs
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS kb_acls (
                kb_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                permission_name TEXT NOT NULL,
                PRIMARY KEY (kb_id, user_id, permission_name),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (permission_name) REFERENCES permissions(name) ON DELETE CASCADE
            )
        """)

        # Audit Log
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                user_id TEXT,
                action TEXT NOT NULL,
                resource_type TEXT,
                resource_id TEXT,
                details TEXT
            )
        """)

        conn.commit()
        conn.close()

    def add_user(self, user_id, username, password_hash, role='user'):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (id, username, password_hash, role) VALUES (?, ?, ?, ?)",
                           (user_id, username, password_hash, role))
            conn.commit()
            self._log_audit(user_id, 'user_added', 'user', user_id, {'username': username, 'role': role})
            return True
        except sqlite3.IntegrityError:
            print(f"User {username} already exists.")
            return False
        finally:
            conn.close()

    def get_user(self, user_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, role FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()
        if user:
            return {"id": user[0], "username": user[1], "role": user[2]}
        return None

    def update_user_role(self, user_id, new_role):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET role = ? WHERE id = ?", (new_role, user_id))
        conn.commit()
        self._log_audit(user_id, 'user_role_updated', 'user', user_id, {'new_role': new_role})
        conn.close()

    def add_permission(self, name, description=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO permissions (name, description) VALUES (?, ?)", (name, description))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            print(f"Permission {name} already exists.")
            return False
        finally:
            conn.close()

    def assign_permission_to_role(self, role_name, permission_name):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO role_permissions (role_name, permission_name) VALUES (?, ?)",
                           (role_name, permission_name))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            print(f"Permission {permission_name} already assigned to role {role_name}.")
            return False
        finally:
            conn.close()

    def check_permission(self, user_id, permission_name, document_id=None, kb_id=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Check role-based permissions
        cursor.execute("SELECT T2.permission_name FROM users AS T1 JOIN role_permissions AS T2 ON T1.role = T2.role_name WHERE T1.id = ? AND T2.permission_name = ?",
                       (user_id, permission_name))
        if cursor.fetchone():
            conn.close()
            return True

        # Check document-level ACLs
        if document_id:
            cursor.execute("SELECT 1 FROM document_acls WHERE document_id = ? AND user_id = ? AND permission_name = ?",
                           (document_id, user_id, permission_name))
            if cursor.fetchone():
                conn.close()
                return True

        # Check knowledge base-level ACLs
        if kb_id:
            cursor.execute("SELECT 1 FROM kb_acls WHERE kb_id = ? AND user_id = ? AND permission_name = ?",
                           (kb_id, user_id, permission_name))
            if cursor.fetchone():
                conn.close()
                return True

        conn.close()
        return False

    def grant_document_access(self, document_id, user_id, permission_name):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO document_acls (document_id, user_id, permission_name) VALUES (?, ?, ?)",
                           (document_id, user_id, permission_name))
            conn.commit()
            self._log_audit(user_id, 'grant_doc_access', 'document', document_id, {'permission': permission_name})
            return True
        except sqlite3.IntegrityError:
            print(f"Access already granted for document {document_id} to user {user_id} with permission {permission_name}.")
            return False
        finally:
            conn.close()

    def revoke_document_access(self, document_id, user_id, permission_name):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM document_acls WHERE document_id = ? AND user_id = ? AND permission_name = ?",
                       (document_id, user_id, permission_name))
        conn.commit()
        self._log_audit(user_id, 'revoke_doc_access', 'document', document_id, {'permission': permission_name})
        conn.close()

    def grant_kb_access(self, kb_id, user_id, permission_name):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO kb_acls (kb_id, user_id, permission_name) VALUES (?, ?, ?)",
                           (kb_id, user_id, permission_name))
            conn.commit()
            self._log_audit(user_id, 'grant_kb_access', 'knowledge_base', kb_id, {'permission': permission_name})
            return True
        except sqlite3.IntegrityError:
            print(f"Access already granted for KB {kb_id} to user {user_id} with permission {permission_name}.")
            return False
        finally:
            conn.close()

    def revoke_kb_access(self, kb_id, user_id, permission_name):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM kb_acls WHERE kb_id = ? AND user_id = ? AND permission_name = ?",
                       (kb_id, user_id, permission_name))
        conn.commit()
        self._log_audit(user_id, 'revoke_kb_access', 'knowledge_base', kb_id, {'permission': permission_name})
        conn.close()

    def _log_audit(self, user_id, action, resource_type=None, resource_id=None, details=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        timestamp = datetime.now().isoformat()
        details_json = json.dumps(details) if details else "{}"
        cursor.execute("INSERT INTO audit_log (timestamp, user_id, action, resource_type, resource_id, details) VALUES (?, ?, ?, ?, ?, ?)",
                       (timestamp, user_id, action, resource_type, resource_id, details_json))
        conn.commit()
        conn.close()

    def get_audit_log(self, limit=100, offset=0):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM audit_log ORDER BY timestamp DESC LIMIT ? OFFSET ?", (limit, offset))
        logs = []
        for row in cursor.fetchall():
            columns = [description[0] for description in cursor.description]
            log_entry = dict(zip(columns, row))
            log_entry['details'] = json.loads(log_entry['details'])
            logs.append(log_entry)
        conn.close()
        return logs
