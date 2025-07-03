import os
import sqlite3
import json
from datetime import datetime

class DocumentStorageService:
    def __init__(self, base_dir="~/.colonel-katie/documents"):
        self.base_dir = os.path.expanduser(base_dir)
        os.makedirs(self.base_dir, exist_ok=True)
        self.db_path = os.path.join(self.base_dir, "document_index.db")
        self._initialize_db()

    def _initialize_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY,
                filename TEXT NOT NULL,
                filepath TEXT NOT NULL,
                agent_id TEXT,
                upload_date TEXT NOT NULL,
                file_size INTEGER,
                file_type TEXT,
                metadata TEXT
            )
        """)
        conn.commit()
        conn.close()

    def get_agent_document_dir(self, agent_id):
        agent_dir = os.path.join(self.base_dir, agent_id)
        os.makedirs(agent_dir, exist_ok=True)
        return agent_dir

    def add_document_metadata(self, doc_id, filename, filepath, agent_id, file_size, file_type, metadata=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        upload_date = datetime.now().isoformat()
        metadata_json = json.dumps(metadata) if metadata else "{}"
        cursor.execute("""
            INSERT INTO documents (id, filename, filepath, agent_id, upload_date, file_size, file_type, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (doc_id, filename, filepath, agent_id, upload_date, file_size, file_type, metadata_json))
        conn.commit()
        conn.close()

    def get_document_metadata(self, doc_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            # Convert row to dictionary for easier access
            columns = [description[0] for description in cursor.description]
            doc_data = dict(zip(columns, row))
            doc_data['metadata'] = json.loads(doc_data['metadata'])
            return doc_data
        return None

    def list_documents_for_agent(self, agent_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, filename, upload_date, file_type FROM documents WHERE agent_id = ?", (agent_id,))
        rows = cursor.fetchall()
        conn.close()
        documents = []
        for row in rows:
            documents.append({"id": row[0], "filename": row[1], "upload_date": row[2], "file_type": row[3]})
        return documents

    def delete_document_metadata(self, doc_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
        conn.commit()
        conn.close()

