from pypdf import PdfReader
from docx import Document
import markdown
from bs4 import BeautifulSoup
import chromadb
import uuid
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from .rag_config import RAGConfig

import nltk
from nltk.tokenize import sent_tokenize

class RAGManager:
    _embedding_model_cache = {}

    def __init__(self, document_storage_service, permission_service, rag_config=None, embedding_model_name="all-MiniLM-L6-v2"):
        self.document_storage_service = document_storage_service
        self.permission_service = permission_service
        self.rag_config = rag_config if rag_config else RAGConfig(embedding_model_name=embedding_model_name)
        self.collections = {}
        self.active_collection = None
        self.embedding_model = self._get_embedding_model(self.rag_config.embedding_model_name)

        # Initialize a default collection
        self.create_collection("default", self.rag_config.embedding_model_name, agent_id="default_agent")
        self.switch_collection("default")

        try:
            nltk.data.find('tokenizers/punkt')
        except (LookupError, AttributeError):
            try:
                print("📦 Downloading NLTK punkt tokenizer...")
                nltk.download('punkt')
                print("✅ NLTK punkt downloaded successfully")
            except Exception as e:
                print(f"⚠️  NLTK download failed: {e}")
                print("   RAG features may be limited")

    def _get_embedding_model(self, model_name):
        if model_name not in self._embedding_model_cache:
            self._embedding_model_cache[model_name] = SentenceTransformer(model_name)
        return self._embedding_model_cache[model_name]

    def create_collection(self, name, embedding_model_name=None, agent_id=None):
        if name in self.collections:
            print(f"Collection '{name}' already exists.")
            return False
        
        # For simplicity, all collections use ChromaDB in this placeholder
        client = chromadb.Client()
        collection = client.get_or_create_collection(name=name)
        self.collections[name] = {
            "collection_obj": collection,
            "embedding_model_name": embedding_model_name if embedding_model_name else self.rag_config.embedding_model_name,
            "embedding_model": self._get_embedding_model(embedding_model_name if embedding_model_name else self.rag_config.embedding_model_name),
            "agent_id": agent_id # Store agent ID with the collection
        }
        print(f"Collection '{name}' created.")
        return True

    def switch_collection(self, name):
        if name not in self.collections:
            print(f"Collection '{name}' does not exist.")
            return False
        self.active_collection = self.collections[name]["collection_obj"]
        self.embedding_model = self.collections[name]["embedding_model"]
        print(f"Switched to collection '{name}'.")
        return True

    def list_collections(self, agent_id=None):
        if agent_id:
            return [name for name, details in self.collections.items() if details.get("agent_id") == agent_id]
        return list(self.collections.keys())

    def delete_collection(self, name):
        if name not in self.collections:
            print(f"Collection '{name}' does not exist.")
            return False
        
        # In a real scenario, you'd delete the actual ChromaDB collection
        del self.collections[name]
        if self.active_collection and self.active_collection.name == name:
            self.active_collection = None
            self.embedding_model = None
        print(f"Collection '{name}' deleted.")
        if self.active_collection and self.active_collection.name == name:
            self.active_collection = None
            self.embedding_model = None
        # Log document deletion
        self.permission_service._log_audit(
            user_id="system", # Assuming system action for now
            action="delete_collection",
            resource_type="collection",
            resource_id=name,
            details={'collection_name': name}
        )
        return True

    def add_document(self, text, metadata=None):
        if not self.active_collection:
            print("No active collection selected. Cannot add document.")
            return False
        try:
            chunks = self._chunk_text(text, self.chunk_size, self.chunk_overlap)
            embeddings = self.embedding_model.encode(chunks).tolist()
            ids = [str(uuid.uuid4()) for _ in chunks]
            metadatas = [metadata if metadata else {} for _ in chunks]

            # Check if document with this source already exists and delete it
            existing_docs = self.active_collection.get(where={"source": metadata.get("source")})
            if existing_docs and existing_docs['ids']:
                self.active_collection.delete(ids=existing_docs['ids'])
                self.document_storage_service.delete_document_metadata(existing_docs['ids'][0]) # Delete from SQLite

            self.active_collection.add(
                documents=chunks,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            # Store document metadata in the DocumentStorageService
            self.document_storage_service.add_document_metadata(
                doc_id=ids[0], # Use the first chunk's ID as the document ID
                filename=metadata.get("source", "unknown_file"),
                filepath=metadata.get("source", "unknown_path"),
                agent_id="default_agent", # Placeholder for now
                file_size=len(text.encode('utf-8')), # Approximate size
                file_type=metadata.get("type", "unknown"),
                metadata=metadata
            )
            # Log document addition
            self.permission_service._log_audit(
                user_id="system", # Assuming system action for now
                action="add_document",
                resource_type="document",
                resource_id=ids[0],
                details={'filename': metadata.get("source"), 'agent_id': "default_agent"}
            )
            return True
            # Log document addition
            self.permission_service._log_audit(
                user_id="system", # Assuming system action for now
                action="add_document",
                resource_type="document",
                resource_id=ids[0],
                details={'filename': metadata.get("source"), 'agent_id': "default_agent"}
            )
            return True
        except Exception as e:
            print(f"Error adding document to ChromaDB: {e}")
            return False

    def set_chunking_strategy(self, strategy, chunk_size=500, chunk_overlap=50):
        print(f"Setting chunking strategy to {strategy} with size {chunk_size} and overlap {chunk_overlap}")
        self.rag_config.chunking_strategy = strategy
        self.rag_config.chunk_size = chunk_size
        self.rag_config.chunk_overlap = chunk_overlap
        # In a real implementation, 'strategy' could dictate different chunking algorithms

    def set_embedding_model(self, model_name):
        print(f"Setting embedding model to {model_name}")
        self.rag_config.embedding_model_name = model_name
        self.embedding_model = self._get_embedding_model(model_name)
        # Update the active collection's embedding model
        if self.active_collection:
            self.collections[self.active_collection.name]["embedding_model_name"] = model_name
            self.collections[self.active_collection.name]["embedding_model"] = self.embedding_model

    def set_vector_database(self, db_type):
        print(f"Setting vector database to {db_type}")
        self.rag_config.vector_database_type = db_type
        # In a real implementation, this would involve re-initializing the client

    def set_retrieval_parameters(self, top_k, similarity_threshold):
        print(f"Setting retrieval parameters: top_k={top_k}, similarity_threshold={similarity_threshold}")
        self.rag_config.retrieval_top_k = top_k
        self.rag_config.retrieval_similarity_threshold = similarity_threshold

    def _chunk_text(self, text):
        if self.rag_config.chunking_strategy == "semantic":
            return self._semantic_chunking(text)
        elif self.rag_config.chunking_strategy == "sliding_window":
            return self._sliding_window_chunking(text)
        elif self.rag_config.chunking_strategy == "hierarchical":
            return self._hierarchical_chunking(text)
        elif self.rag_config.chunking_strategy == "code_aware":
            return self._code_aware_chunking(text)
        else:
            return self._sliding_window_chunking(text) # Default fallback

    def _semantic_chunking(self, text):
        sentences = sent_tokenize(text)
        chunks = []
        current_chunk = []
        current_length = 0

        for sentence in sentences:
            sentence_length = len(sentence.split())
            if current_length + sentence_length <= self.rag_config.chunk_size:
                current_chunk.append(sentence)
                current_length += sentence_length
            else:
                chunks.append(" ".join(current_chunk))
                current_chunk = [sentence]
                current_length = sentence_length
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        return chunks

    def _sliding_window_chunking(self, text):
        chunks = []
        words = text.split()
        i = 0
        while i < len(words):
            chunk = " ".join(words[i:i + self.rag_config.chunk_size])
            chunks.append(chunk)
            i += self.rag_config.chunk_size - self.rag_config.chunk_overlap
        return chunks

    def _hierarchical_chunking(self, text):
        # Placeholder for hierarchical chunking
        # This would involve splitting by sections, then chunking those sections
        print("Performing hierarchical chunking (placeholder).")
        return self._sliding_window_chunking(text) # Fallback for now

    def _code_aware_chunking(self, text):
        # Placeholder for code-aware chunking
        # This would involve parsing code structure (functions, classes) for chunks
        print("Performing code-aware chunking (placeholder).")
        return self._sliding_window_chunking(text) # Fallback for now

    def load_pdf(self, file_path):
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error loading PDF {file_path}: {e}")
            return None

    def load_docx(self, file_path):
        try:
            document = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in document.paragraphs])
            return text
        except Exception as e:
            print(f"Error loading DOCX {file_path}: {e}")
            return None

    def load_txt(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error loading TXT {file_path}: {e}")
            return None

    def load_md(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
                return markdown.markdown(md_content) # Converts markdown to HTML
        except Exception as e:
            print(f"Error loading MD {file_path}: {e}")
            return None

    def load_html(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
                soup = BeautifulSoup(html_content, 'html.parser')
                return soup.get_text() # Extracts text from HTML
        except Exception as e:
            print(f"Error loading HTML {file_path}: {e}")
            return None

    def query_documents(self, query_text, n_results=5):
        if not self.active_collection:
            print("No active collection selected. Cannot query documents.")
            return None
        # Log document query
        self.permission_service._log_audit(
            user_id="current_user", # Placeholder for current user
            action="query_documents",
            resource_type="collection",
            resource_id=self.active_collection.name,
            details={'query_text': query_text}
        )
        try:
            query_embedding = self.embedding_model.encode([query_text]).tolist()
            results = self.active_collection.query(
                query_embeddings=query_embedding,
                n_results=self.rag_config.retrieval_top_k,
                include=['documents', 'metadatas']
            )
            return results
        except Exception as e:
            print(f"Error querying documents: {e}")
            return None

    def hybrid_search(self, query_text):
        # Placeholder for hybrid search implementation
        # This would typically combine keyword-based search (like BM25) with
        # semantic search (using embeddings).
        print(f"Performing hybrid search for: {query_text}")
        # For now, just return semantic search results
        return self.query_documents(query_text, self.rag_config.retrieval_top_k)

    def generate_response(self, query, api_key):
        try:
            genai.configure(api_key=api_key)
            retrieved_docs = self.query_documents(query)
            
            context = ""
            if retrieved_docs and retrieved_docs['documents']:
                for doc_list in retrieved_docs['documents']:
                    for doc in doc_list:
                        context += doc + "\n\n"

            prompt = f"Given the following context, answer the query:\n\nContext:\n{context}\n\nQuery: {query}\n\nAnswer:"
            
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating RAG response: {e}")
            return None

    def create_workflow_builder_interface(self):
        # Placeholder for visual workflow builder
        print("Creating visual workflow builder interface.")

    def configure_multi_model_processing_chain(self, chain_config):
        # Placeholder for multi-model processing chains
        print(f"Configuring multi-model processing chain: {chain_config}")

    def add_conditional_logic_to_workflow(self, logic_config):
        # Placeholder for conditional logic and branching
        print(f"Adding conditional logic to workflow: {logic_config}")

    def schedule_workflow_execution(self, workflow_id, schedule_time):
        # Placeholder for scheduled execution system
        print(f"Scheduling workflow {workflow_id} for {schedule_time}.")

    def setup_trigger_based_automation(self, trigger_type, trigger_config):
        # Placeholder for trigger-based automation
        print(f"Setting up {trigger_type} trigger-based automation: {trigger_config}")
