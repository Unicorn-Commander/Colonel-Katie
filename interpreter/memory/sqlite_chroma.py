import sqlite3
import numpy as np
from sklearn.neighbors import NearestNeighbors
from typing import Any, List
from .base import BaseMemoryBackend

class SQLiteChromaBackend(BaseMemoryBackend):
    def __init__(self, db_path='memory.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS structured_memory (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS semantic_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text_chunk TEXT,
                embedding BLOB
            )
        ''')
        self.conn.commit()
        self.nn_model = None
        self.embeddings_cache = []
        self.texts_cache = []
        self._load_semantic_memory_to_cache()

    def _load_semantic_memory_to_cache(self):
        self.cursor.execute("SELECT text_chunk, embedding FROM semantic_memory")
        rows = self.cursor.fetchall()
        self.embeddings_cache = [np.frombuffer(row[1], dtype=np.float32) for row in rows]
        self.texts_cache = [row[0] for row in rows]
        if self.embeddings_cache:
            self.nn_model = NearestNeighbors(n_neighbors=min(len(self.embeddings_cache), 5), metric='cosine')
            self.nn_model.fit(np.array(self.embeddings_cache))

    def save_structured_memory(self, key: str, value: Any):
        self.cursor.execute("INSERT OR REPLACE INTO structured_memory (key, value) VALUES (?, ?)", (key, str(value)))
        self.conn.commit()

    def get_structured_memory(self, key: str) -> Any:
        self.cursor.execute("SELECT value FROM structured_memory WHERE key = ?", (key,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def add_semantic_memory(self, text_chunk: str, embedding: List[float]):
        embedding_np = np.array(embedding, dtype=np.float32)
        self.cursor.execute("INSERT INTO semantic_memory (text_chunk, embedding) VALUES (?, ?)", (text_chunk, embedding_np.tobytes()))
        self.conn.commit()
        self.embeddings_cache.append(embedding_np)
        self.texts_cache.append(text_chunk)
        self.nn_model = NearestNeighbors(n_neighbors=min(len(self.embeddings_cache), 5), metric='cosine')
        self.nn_model.fit(np.array(self.embeddings_cache))

    def search_semantic_memory(self, query_embedding: List[float], top_k: int) -> List[str]:
        if not self.embeddings_cache:
            return []
        query_embedding_np = np.array(query_embedding, dtype=np.float32).reshape(1, -1)
        distances, indices = self.nn_model.kneighbors(query_embedding_np, n_neighbors=min(len(self.embeddings_cache), top_k))
        return [self.texts_cache[i] for i in indices[0]]