
import os
import json
from datetime import datetime

class FileIndexer:
    def __init__(self, interpreter_instance):
        self.interpreter = interpreter_instance
        self.indexed_files = {}
        self.index_file_path = os.path.join(self.interpreter.conversation_history_path, "file_index.json")
        self._load_index()

    def _load_index(self):
        if os.path.exists(self.index_file_path):
            with open(self.index_file_path, 'r') as f:
                self.indexed_files = json.load(f)

    def _save_index(self):
        with open(self.index_file_path, 'w') as f:
            json.dump(self.indexed_files, f, indent=4)

    def index_directory(self, directory_path, extensions=None):
        if not os.path.isdir(directory_path):
            print(f"Error: Directory not found: {directory_path}")
            return

        for root, _, files in os.walk(directory_path):
            for file_name in files:
                if extensions and not file_name.endswith(tuple(extensions)):
                    continue
                
                file_path = os.path.join(root, file_name)
                self._index_file(file_path)
        self._save_index()

    def _index_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Generate embedding for the content
            embedding = self.interpreter.llm.embed(content)
            
            # Store in semantic memory
            self.interpreter.memory.add_semantic_memory(content, embedding)
            
            # Update indexed files record
            self.indexed_files[file_path] = {
                "last_indexed": datetime.now().isoformat(),
                "size": os.path.getsize(file_path)
            }
            print(f"Indexed: {file_path}")

        except Exception as e:
            print(f"Error indexing {file_path}: {e}")

    def search_indexed_files(self, query, top_k=5):
        query_embedding = self.interpreter.llm.embed(query)
        results = self.interpreter.memory.search_semantic_memory(query_embedding, top_k)
        return results
