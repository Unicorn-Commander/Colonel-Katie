
from .sqlite_chroma import SQLiteChromaBackend
from .postgres_qdrant import PostgresQdrantBackend

class MemoryManager:
    def __init__(self, backend='sqlite_chroma', **kwargs):
        if backend == 'sqlite_chroma':
            self.backend = SQLiteChromaBackend(**kwargs)
        elif backend == 'postgres_qdrant':
            self.backend = PostgresQdrantBackend(**kwargs)
        else:
            raise ValueError(f"Unknown backend: {backend}")

    def save_structured_memory(self, key: str, value: any):
        self.backend.save_structured_memory(key, value)

    def get_structured_memory(self, key: str) -> any:
        return self.backend.get_structured_memory(key)

    def add_semantic_memory(self, text_chunk: str, embedding: list[float]):
        self.backend.add_semantic_memory(text_chunk, embedding)

    def search_semantic_memory(self, query_embedding: list[float], top_k: int) -> list[str]:
        return self.backend.search_semantic_memory(query_embedding, top_k)
