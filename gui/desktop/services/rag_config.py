class RAGConfig:
    def __init__(self, 
                 embedding_model_name="all-MiniLM-L6-v2", 
                 vector_database_type="chromadb", 
                 chunking_strategy="sliding_window", 
                 chunk_size=500, 
                 chunk_overlap=50, 
                 retrieval_top_k=5, 
                 retrieval_similarity_threshold=0.7):
        
        self.embedding_model_name = embedding_model_name
        self.vector_database_type = vector_database_type
        self.chunking_strategy = chunking_strategy
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.retrieval_top_k = retrieval_top_k
        self.retrieval_similarity_threshold = retrieval_similarity_threshold

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, config_dict):
        return cls(**config_dict)

    @staticmethod
    def get_presets():
        return {
            "Default": RAGConfig(),
            "Code Analysis": RAGConfig(
                chunking_strategy="code_aware",
                chunk_size=1000,
                chunk_overlap=100,
                retrieval_top_k=10
            ),
            "Research Paper": RAGConfig(
                chunking_strategy="semantic",
                chunk_size=700,
                chunk_overlap=70,
                retrieval_top_k=7
            ),
            "General Chat": RAGConfig(
                chunking_strategy="sentence",
                chunk_size=200,
                chunk_overlap=20,
                retrieval_top_k=3
            )
        }
