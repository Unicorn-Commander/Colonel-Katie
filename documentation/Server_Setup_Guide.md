# The_Colonel API Server Setup Guide

## Current Status ✅

**As of 2025-07-01, all circular import issues have been resolved and the server is fully functional.**

## Quick Start

### 1. Basic Server Startup

```bash
# Navigate to project root
cd /path/to/The_Colonel

# Activate virtual environment
source venv/bin/activate

# Start the server
python -m interpreter.api.main
```

The server will start on `http://localhost:8000` by default.

### 2. Verify Server is Working

```bash
# Test server import
python -c "from interpreter.api.server import create_colonel_katie_server; print('✅ Server import successful')"

# Test API endpoint
curl http://localhost:8000/openapi.json
```

Expected response: HTTP 200 with OpenAPI specification JSON.

## Required Dependencies

The following packages are required and should be installed automatically:

```bash
pip install sentence_transformers psycopg2-binary qdrant-client fastapi uvicorn python-multipart platformdirs
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# API Keys
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# Server Configuration
DEFAULT_PROFILE=The_Colonel.py
SERVER_HOST=0.0.0.0
SERVER_PORT=8000

# Features
DISABLE_TELEMETRY=true
AUTO_RUN=false
SAFE_MODE=off
```

### Authentication

- **Localhost**: No authentication required for `127.0.0.1` and `localhost`
- **Remote Access**: Set `AUTH_TOKEN` environment variable for Bearer token authentication

## API Endpoints

### Core Endpoints

- `GET /openapi.json` - Complete API specification
- `POST /v1/chat/completions` - OpenAI-compatible chat endpoint
- `GET /api/v1/tools/` - List all available tools

### Tool Endpoints

#### Python Execution
- `POST /python/execute` - Execute Python code
- `GET /python/openapi.json` - Python tool specification

#### Shell Commands
- `POST /shell/execute` - Execute shell commands
- `GET /shell/openapi.json` - Shell tool specification

#### File Operations
- `POST /files/read` - Read file contents
- `POST /files/write` - Write file contents
- `GET /files/openapi.json` - Files tool specification

#### Computer Control
- `POST /computer/screenshot` - Take screenshot
- `POST /computer/click` - Click at coordinates
- `POST /computer/type` - Type text
- `GET /computer/openapi.json` - Computer tool specification

#### KDE Integration
- `POST /kde/clipboard/get` - Get clipboard contents
- `POST /kde/clipboard/set` - Set clipboard contents
- `POST /kde/notifications/send` - Send desktop notification

#### Memory Management
- `POST /memory/structured/save` - Save structured memory
- `POST /memory/structured/get` - Get structured memory
- `POST /memory/semantic/add` - Add semantic memory
- `POST /memory/semantic/search` - Search semantic memory

#### File Indexing
- `POST /file_indexing/index_directory` - Index directory for search
- `POST /file_indexing/search_indexed_files` - Search indexed files

## Open WebUI Integration

### LLM Configuration

In Open WebUI, add a new LLM with:
- **Base URL**: `http://localhost:8000/v1`
- **Model Name**: `the-colonel`
- **API Key**: Leave blank for localhost (or use AUTH_TOKEN for remote)

### Tool Integration

Add individual tools to Open WebUI:

1. **Python Tool**
   - Tool Server URL: `http://localhost:8000/python`
   - OpenAPI URL: `http://localhost:8000/python/openapi.json`

2. **Shell Tool**
   - Tool Server URL: `http://localhost:8000/shell`
   - OpenAPI URL: `http://localhost:8000/shell/openapi.json`

3. **Files Tool**
   - Tool Server URL: `http://localhost:8000/files`
   - OpenAPI URL: `http://localhost:8000/files/openapi.json`

4. **Computer Tool**
   - Tool Server URL: `http://localhost:8000/computer`
   - OpenAPI URL: `http://localhost:8000/computer/openapi.json`

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Verify all dependencies are installed
   pip install -r requirements.txt
   
   # Check for circular imports
   python -c "import interpreter.core.core; print('Core import OK')"
   ```

2. **Port Already in Use**
   ```bash
   # Find process using port 8000
   lsof -ti:8000
   
   # Kill process if needed
   lsof -ti:8000 | xargs kill -9
   ```

3. **Server Won't Start**
   ```bash
   # Check Python path
   which python
   
   # Verify virtual environment
   echo $VIRTUAL_ENV
   
   # Run with debug output
   python -m interpreter.api.main --debug
   ```

### Debug Mode

For verbose logging:
```bash
export PYTHONPATH=/path/to/The_Colonel:$PYTHONPATH
python -m interpreter.api.main
```

## Architecture Notes

### Fixed Issues (2025-07-01)

- ✅ Circular import in `computer.py` (kde_tools import path)
- ✅ Circular import in `file_indexing` module
- ✅ Missing `get_storage_path` import in `core.py`
- ✅ FileIndexer initialization order issue
- ✅ Missing return statement in `create_colonel_katie_server`
- ✅ Lazy import path correction in `server.py`
- ✅ Deleted empty `async_core.py` file

### Current Architecture

```
interpreter/
├── api/
│   ├── main.py              # FastAPI app entry point
│   └── server.py            # FastAPI server implementation
├── core/
│   ├── core.py              # OpenInterpreter class
│   └── computer/
│       └── computer.py      # Computer control integration
├── kde_tools/               # KDE desktop integration
├── memory/                  # Memory management
└── file_indexing/           # File indexing system
```

## Production Deployment

### Using Uvicorn Directly

```bash
uvicorn interpreter.api.main:app --host 0.0.0.0 --port 8000 --workers 1
```

### Using Gunicorn (Recommended for Production)

```bash
gunicorn interpreter.api.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install -e .

EXPOSE 8000
CMD ["python", "-m", "interpreter.api.main"]
```

## Security Considerations

- Always use authentication tokens for remote access
- Keep API keys secure in environment variables
- Review code execution requests in production
- Use HTTPS for remote deployments
- Implement rate limiting for production use

---

For more information, see the [Project Summary](Project_Summary.md) and [Technical Implementation Guide](Technical_Implementation_Guide.md).