import sqlite3
import json
import os
from mem0 import Memory

class MemoryService:
    def __init__(self, api_key=None, user_id="default_user", use_mem0=True):
        self.user_id = user_id
        self.use_mem0 = use_mem0
        self.mem0_instance = None
        if self.use_mem0:
            try:
                self.mem0_instance = Memory(api_key=api_key) # Initialize mem0
            except Exception as e:
                print(f"Failed to initialize mem0: {e}. Falling back to local memory.")
                self.use_mem0 = False

        self.db_path = os.path.expanduser(f"~/.colonel-katie/memory_{user_id}.db")
        self._initialize_local_db()

    def _initialize_local_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS local_memories (
                id TEXT PRIMARY KEY,
                data TEXT NOT NULL,
                metadata TEXT,
                timestamp TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def _add_local_memory(self, memory_id, data, metadata=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        timestamp = datetime.now().isoformat()
        metadata_json = json.dumps(metadata) if metadata else "{}"
        cursor.execute("INSERT INTO local_memories (id, data, metadata, timestamp) VALUES (?, ?, ?, ?)",
                       (memory_id, data, metadata_json, timestamp))
        conn.commit()
        conn.close()

    def _get_local_memories(self, query, limit=5):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Simple keyword search for local memories
        cursor.execute("SELECT id, data, metadata, timestamp FROM local_memories WHERE data LIKE ? LIMIT ?",
                       (f'%{query}%', limit))
        memories = []
        for row in cursor.fetchall():
            memories.append({"id": row[0], "data": row[1], "metadata": json.loads(row[2]), "timestamp": row[3]})
        conn.close()
        return memories

    def _update_local_memory(self, memory_id, new_data, new_metadata=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        metadata_json = json.dumps(new_metadata) if new_metadata else "{}"
        cursor.execute("UPDATE local_memories SET data = ?, metadata = ? WHERE id = ?",
                       (new_data, metadata_json, memory_id))
        conn.commit()
        conn.close()

    def _delete_local_memory(self, memory_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM local_memories WHERE id = ?", (memory_id,))
        conn.commit()
        conn.close()

    def _delete_all_local_memories(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM local_memories")
        conn.commit()
        conn.close()

    def add_memory(self, data, metadata=None):
        if self.use_mem0 and self.mem0_instance:
            try:
                memory = self.mem0_instance.add(data, user_id=self.user_id, metadata=metadata)
                print(f"Memory added to mem0: {memory}")
                return memory
            except Exception as e:
                print(f"Error adding memory to mem0: {e}. Falling back to local memory.")
                self.use_mem0 = False # Disable mem0 for this session if it fails

        # Fallback to local memory
        memory_id = str(uuid.uuid4())
        self._add_local_memory(memory_id, data, metadata)
        print(f"Memory added to local DB: {memory_id}")
        return {"id": memory_id, "data": data, "metadata": metadata}

    def get_memories(self, query, limit=5):
        if self.use_mem0 and self.mem0_instance:
            try:
                memories = self.mem0_instance.get(query, user_id=self.user_id, limit=limit)
                print(f"Retrieved memories from mem0: {memories}")
                return memories
            except Exception as e:
                print(f"Error retrieving memories from mem0: {e}. Falling back to local memory.")
                self.use_mem0 = False # Disable mem0 for this session if it fails

        # Fallback to local memory
        return self._get_local_memories(query, limit)

    def update_memory(self, memory_id, new_data, new_metadata=None):
        if self.use_mem0 and self.mem0_instance:
            try:
                updated_memory = self.mem0_instance.update(memory_id, new_data, user_id=self.user_id, metadata=new_metadata)
                print(f"Memory updated in mem0: {updated_memory}")
                return updated_memory
            except Exception as e:
                print(f"Error updating memory in mem0: {e}. Falling back to local memory.")
                self.use_mem0 = False

        # Fallback to local memory
        self._update_local_memory(memory_id, new_data, new_metadata)
        print(f"Memory {memory_id} updated in local DB.")
        return {"id": memory_id, "data": new_data, "metadata": new_metadata}

    def delete_memory(self, memory_id):
        if self.use_mem0 and self.mem0_instance:
            try:
                self.mem0_instance.delete(memory_id, user_id=self.user_id)
                print(f"Memory {memory_id} deleted from mem0.")
                return True
            except Exception as e:
                print(f"Error deleting memory from mem0: {e}. Falling back to local memory.")
                self.use_mem0 = False

        # Fallback to local memory
        self._delete_local_memory(memory_id)
        print(f"Memory {memory_id} deleted from local DB.")
        return True

    def delete_all_memories(self):
        if self.use_mem0 and self.mem0_instance:
            try:
                self.mem0_instance.delete_all(user_id=self.user_id)
                print("All memories deleted from mem0.")
                return True
            except Exception as e:
                print(f"Error deleting all memories from mem0: {e}. Falling back to local memory.")
                self.use_mem0 = False

        # Fallback to local memory
        self._delete_all_local_memories()
        print("All memories deleted from local DB.")
        return True
