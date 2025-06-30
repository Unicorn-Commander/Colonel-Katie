
from abc import ABC, abstractmethod
from typing import Any, List

class BaseMemoryBackend(ABC):
    @abstractmethod
    def save_structured_memory(self, key: str, value: Any):
        pass

    @abstractmethod
    def get_structured_memory(self, key: str) -> Any:
        pass

    @abstractmethod
    def add_semantic_memory(self, text_chunk: str, embedding: List[float]):
        pass

    @abstractmethod
    def search_semantic_memory(self, query_embedding: List[float], top_k: int) -> List[str]:
        pass
