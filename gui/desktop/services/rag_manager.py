from pypdf import PdfReader
from docx import Document
import markdown
from bs4 import BeautifulSoup
import chromadb
import uuid
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

class RAGManager:
    def __init__(self, embedding_model_name="all-MiniLM-L6-v2"):
        self.collections = {}
        self.active_collection = None
        self.embedding_model_name = embedding_model_name
        self.embedding_model = SentenceTransformer(embedding_model_name)
        self.chunk_size = 500
        self.chunk_overlap = 50
        self.vector_database_type = "chromadb"
        self.retrieval_top_k = 5
        self.retrieval_similarity_threshold = 0.7

        # Initialize a default collection
        self.create_collection("default", self.embedding_model_name)
        self.switch_collection("default")

    def create_collection(self, name, embedding_model_name=None):
        if name in self.collections:
            print(f"Collection '{name}' already exists.")
            return False
        
        # For simplicity, all collections use ChromaDB in this placeholder
        client = chromadb.Client()
        collection = client.get_or_create_collection(name=name)
        self.collections[name] = {
            "collection_obj": collection,
            "embedding_model_name": embedding_model_name if embedding_model_name else self.embedding_model_name,
            "embedding_model": SentenceTransformer(embedding_model_name if embedding_model_name else self.embedding_model_name)
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

    def list_collections(self):
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

            self.active_collection.add(
                documents=chunks,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            return True
        except Exception as e:
            print(f"Error adding document to ChromaDB: {e}")
            return False

    def set_chunking_strategy(self, strategy, chunk_size=500, chunk_overlap=50):
        print(f"Setting chunking strategy to {strategy} with size {chunk_size} and overlap {chunk_overlap}")
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        # In a real implementation, 'strategy' could dictate different chunking algorithms

    def set_embedding_model(self, model_name):
        print(f"Setting embedding model to {model_name}")
        self.embedding_model_name = model_name
        self.embedding_model = SentenceTransformer(model_name)
        # Update the active collection's embedding model
        if self.active_collection:
            self.collections[self.active_collection.name]["embedding_model_name"] = model_name
            self.collections[self.active_collection.name]["embedding_model"] = self.embedding_model

    def set_vector_database(self, db_type):
        print(f"Setting vector database to {db_type}")
        self.vector_database_type = db_type
        # In a real implementation, this would involve re-initializing the client

    def set_retrieval_parameters(self, top_k, similarity_threshold):
        print(f"Setting retrieval parameters: top_k={top_k}, similarity_threshold={similarity_threshold}")
        self.retrieval_top_k = top_k
        self.retrieval_similarity_threshold = similarity_threshold

    def _chunk_text(self, text, chunk_size=500, chunk_overlap=50):
        # A very basic chunking strategy. More advanced strategies would use
        # sentence tokenization, recursive splitting, etc.
        chunks = []
        words = text.split()
        i = 0
        while i < len(words):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
            i += chunk_size - chunk_overlap
        return chunks

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
        try:
            query_embedding = self.embedding_model.encode([query_text]).tolist()
            results = self.active_collection.query(
                query_embeddings=query_embedding,
                n_results=n_results,
                include=['documents', 'metadatas']
            )
            return results
        except Exception as e:
            print(f"Error querying documents: {e}")
            return None

    def hybrid_search(self, query_text, n_results=5):
        # Placeholder for hybrid search implementation
        # This would typically combine keyword-based search (like BM25) with
        # semantic search (using embeddings).
        print(f"Performing hybrid search for: {query_text}")
        # For now, just return semantic search results
        return self.query_documents(query_text, n_results)

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
