# 🚀 Headless Features - Colonel Katie

Colonel Katie's headless installation includes powerful features for servers and automation.

## Core Features Available in Headless Mode

### ✅ Full AI/LLM Capabilities
- All language models (OpenAI, Anthropic, Google, Ollama, etc.)
- Code execution in multiple languages
- System command execution
- File operations
- Web automation

### ✅ RAG (Retrieval Augmented Generation)
The headless version includes full RAG capabilities:

```python
# Example: Document processing
from interpreter import interpreter

# Load documents
interpreter.computer.docs.load("report.pdf")
interpreter.computer.docs.load("data.xlsx")

# Query your documents
response = interpreter.chat("What are the key findings in the report?")
```

**Supported formats:**
- PDF documents (`PyPDF2`)
- Word documents (`python-docx`)
- Text files
- Markdown files
- Code files
- HTML documents

**Vector Database:**
- ChromaDB for embeddings storage
- Sentence Transformers for creating embeddings
- Semantic search across documents

### ✅ Memory System

Colonel Katie includes persistent memory across sessions:

```python
# Memory persists between sessions
interpreter.chat("My name is John and I work on AI projects")
# ... close and restart later ...
interpreter.chat("What's my name and what do I work on?")
# Response: "Your name is John and you work on AI projects"
```

**Memory Backends:**

1. **SQLite + ChromaDB** (Default)
   - No setup required
   - Good for single-user deployments
   - Stores in `~/.interpreter/memory.db`

2. **PostgreSQL + Qdrant** (Advanced)
   - Scalable for multiple users
   - Better performance
   - Requires external services

**Memory Types:**
- **Conversation Memory**: Remembers past conversations
- **Semantic Memory**: Stores and searches by meaning
- **Structured Memory**: Key-value storage for facts
- **Document Memory**: Indexes uploaded documents

### ✅ Embeddings and Semantic Search

Full embedding support for:
- Document chunking and indexing
- Semantic similarity search
- Context-aware responses
- Multi-document reasoning

```python
# Example: Semantic search
interpreter.chat("Find all mentions of budget constraints in my documents")
# Searches semantically, not just keywords
```

## Configuration for Headless Features

### Basic Configuration

Edit `~/.interpreter/config.yaml`:

```yaml
# Memory configuration
memory:
  enabled: true
  backend: sqlite_chroma  # or postgres_qdrant
  persist_conversations: true
  
# RAG configuration  
rag:
  enabled: true
  chunk_size: 1000
  chunk_overlap: 200
  
# Embedding model
embeddings:
  model: sentence-transformers/all-MiniLM-L6-v2
  dimension: 384
```

### Advanced Setup with External Services

#### Redis for Caching
```bash
# Install Redis
sudo apt install redis-server

# Configure in config.yaml
cache:
  backend: redis
  url: redis://localhost:6379
```

#### PostgreSQL + Qdrant for Scalable Memory
```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Create database
sudo -u postgres createuser colonel_katie
sudo -u postgres createdb -O colonel_katie katie_memory

# Run Qdrant
docker run -p 6333:6333 -v $(pwd)/qdrant_storage:/qdrant/storage qdrant/qdrant

# Configure in config.yaml
memory:
  backend: postgres_qdrant
  postgres_url: postgresql://colonel_katie:password@localhost/katie_memory
  qdrant_url: http://localhost:6333
```

## Usage Examples

### Document Analysis Pipeline
```python
#!/usr/bin/env python3
from interpreter import interpreter

# Configure for document analysis
interpreter.system_message = """You are a document analysis expert. 
When analyzing documents, provide structured summaries."""

# Load multiple documents
documents = ["report1.pdf", "report2.pdf", "data.xlsx"]
for doc in documents:
    interpreter.computer.docs.load(doc)

# Analyze
analysis = interpreter.chat("""
Analyze all loaded documents and provide:
1. Key findings
2. Common themes
3. Contradictions or conflicts
4. Recommendations
""")

print(analysis)
```

### Memory-Enhanced Chatbot
```python
#!/usr/bin/env python3
from interpreter import interpreter

# Enable memory
interpreter.memory.enabled = True

# First conversation
interpreter.chat("I'm working on a Python web scraping project using BeautifulSoup")
interpreter.chat("The target website is https://example.com")

# Later conversation (even after restart)
response = interpreter.chat("What project am I working on and what tools?")
# Will remember: Python web scraping with BeautifulSoup for example.com
```

### Semantic Document Search
```python
#!/usr/bin/env python3
from interpreter import interpreter

# Load knowledge base
knowledge_files = Path("knowledge_base").glob("*.md")
for file in knowledge_files:
    interpreter.computer.docs.load(str(file))

# Semantic search
results = interpreter.chat(
    "Find all information about error handling best practices",
    search_mode=True
)
```

## Performance Optimization

### For Large Document Sets
```yaml
# Optimize for many documents
rag:
  chunk_size: 500  # Smaller chunks
  max_chunks_per_query: 10
  similarity_threshold: 0.7
  
embeddings:
  batch_size: 32
  cache_embeddings: true
```

### For Limited Memory Systems
```yaml
# Reduce memory usage
memory:
  max_conversations: 100
  compress_old_conversations: true
  
rag:
  max_documents: 50
  cleanup_after_processing: true
```

## API Access to Features

When running as a server:

```bash
./interpreter-server.sh --port 8080
```

### RAG Endpoints
```bash
# Upload document
curl -X POST http://localhost:8080/documents \
  -F "file=@report.pdf"

# Query documents
curl -X POST http://localhost:8080/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the conclusions?"}'
```

### Memory Endpoints
```bash
# Save memory
curl -X POST http://localhost:8080/memory \
  -H "Content-Type: application/json" \
  -d '{"key": "user_name", "value": "John"}'

# Search memories
curl -X POST http://localhost:8080/memory/search \
  -H "Content-Type: application/json" \
  -d '{"query": "user information"}'
```

## Limitations in Headless Mode

While headless mode includes RAG and memory, some features require GUI:
- ❌ Visual Agent Builder
- ❌ Drag-and-drop document upload
- ❌ Real-time monitoring dashboard
- ❌ Voice interaction UI
- ❌ KDE desktop integration

However, all core functionality is available via:
- ✅ CLI commands
- ✅ Python API
- ✅ REST API
- ✅ Scripts and automation

## Best Practices

1. **Memory Management**
   - Periodically clean old conversations
   - Use structured memory for facts
   - Use semantic memory for context

2. **Document Processing**
   - Pre-process large PDFs
   - Use appropriate chunk sizes
   - Index documents before querying

3. **Performance**
   - Enable caching for embeddings
   - Use batch processing for multiple documents
   - Consider external services for scale

---

**Summary**: The headless version is fully featured for server deployments, including RAG, memory, and embeddings. The main difference from GUI installation is the interface, not the capabilities! 🦄⚡