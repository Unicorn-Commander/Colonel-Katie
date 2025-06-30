
import os
import psycopg2
from qdrant_client import QdrantClient, models
from typing import Any, List
from .base import BaseMemoryBackend

class PostgresQdrantBackend(BaseMemoryBackend):
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.environ.get("POSTGRES_HOST"),
            database=os.environ.get("POSTGRES_DB"),
            user=os.environ.get("POSTGRES_USER"),
            password=os.environ.get("POSTGRES_PASSWORD")
        )
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS structured_memory (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        self.conn.commit()

        self.qdrant_client = QdrantClient(host=os.environ.get("QDRANT_HOST"), port=os.environ.get("QDRANT_PORT"))
        self.collection_name = "semantic_memory"
        self.qdrant_client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
        )

    def save_structured_memory(self, key: str, value: Any):
        self.cursor.execute("INSERT OR REPLACE INTO structured_memory (key, value) VALUES (%s, %s)", (key, str(value)))
        self.conn.commit()

    def get_structured_memory(self, key: str) -> Any:
        self.cursor.execute("SELECT value FROM structured_memory WHERE key = %s", (key,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def add_semantic_memory(self, text_chunk: str, embedding: List[float]):
        self.qdrant_client.upsert(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(
                    id=str(hash(text_chunk)),
                    vector=embedding,
                    payload={"text": text_chunk}
                )
            ]
        )

    def search_semantic_memory(self, query_embedding: List[float], top_k: int) -> List[str]:
        hits = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=top_k
        )
        return [hit.payload['text'] for hit in hits]
