# Changelog

All notable changes to The_Colonel project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Memory System:**
    - Implemented a flexible memory system with `BaseMemoryBackend` interface.
    - Added `SQLiteChromaBackend` for structured and semantic memory (using SQLite and custom vector store).
    - Added `PostgreSQL/Qdrant Backend`: Developed `PostgresQdrantBackend` for scalable structured and semantic memory, integrating with PostgreSQL and Qdrant.
    - Integrated `MemoryManager` into `OpenInterpreter` for persistent, adaptive memory.
    - Implemented basic LLM-driven memory extraction in `Llm.extract_memories`.
- **Graphical User Interface (GUI):**
    - Developed a new modular desktop GUI (`gui/desktop`) with a three-column layout.
    - Implemented modern, Unicorn Commander-themed styling.
    - Added conversation history loading and display.
    - Developed a functional right sidebar with session details and collapsible categories.
    - Enhanced chat window with `markdown-it-py` and `Pygments` for robust markdown and code block rendering.
    - Implemented a GUI trigger for file indexing in the right sidebar.
- **File Indexing:**
    - Implemented a custom file indexing and embedding system (`FileIndexer`).
    - Integrated `FileIndexer` into `OpenInterpreter` for project-aware context.
- **Roadmap Updates:**
    - Added "Web GUI Development" to the future roadmap.

### Changed
- `sentence-transformers` is now a core dependency.
- `numpy` compatibility addressed by replacing `chromadb` with a custom SQLite vector store.
- `profiles_dialog.py` updated to correctly reference `chat_window.output_display`.
- `interpreter/core/core.py` updated for robust conversation saving and memory extraction logic.
- Moved `kde_tools` directory into `interpreter/kde_tools` for proper package structure.
- Refactored `interpreter/api/server.py` to integrate server logic (from `async_core.py`) and use the `Server` class.
- Modified `interpreter/core/computer/computer.py` to use absolute imports for `interpreter.kde_tools.wrappers`.
- Refactored `interpreter/__init__.py` to remove direct `OpenInterpreter` instantiation and `--os` logic, resolving circular imports.

### Fixed
- `AttributeError: 'ColonelKDEApp' object has no attribute 'output_display'` in `profiles_dialog.py`.
- `NameError: name 'QLabel' is not defined` in `main_window.py`.
- Resolved `ModuleNotFoundError: No module named 'interpreter.kde_tools'` by moving `kde_tools` into `interpreter/`.
- Resolved `ImportError: cannot import name 'QVariant' from 'PySide6.QtCore'` by removing `QVariant` import from `kde_tools` modules.
- Resolved `ModuleNotFoundError: No module named 'inquirer'` by ensuring `uvicorn` runs in the correct virtual environment.
- Resolved `ModuleNotFoundError: No module named 'sentence_transformers'` by installing the package.
- Resolved `ModuleNotFoundError: No module named 'psycopg2'` by installing `psycopg2-binary`.
- Resolved `ModuleNotFoundError: No module named 'qdrant_client'` by installing the package.
- Resolved `ImportError: cannot import name 'interpreter' from partially initialized module 'interpreter'` by refactoring `interpreter/__init__.py` and decoupling `async_core.py`.

## [2.0.1] - 2025-07-01 - Critical Server Fixes

### Fixed - Circular Import Resolution
- **Circular Import in computer.py**: Fixed absolute import `from interpreter.kde_tools.wrappers` to use relative import `from ...kde_tools.wrappers`
- **Circular Import in file_indexing**: Removed unnecessary `from interpreter import interpreter` import causing circular dependency
- **Missing get_storage_path import**: Added proper import for `get_storage_path` from terminal interface utils in core.py
- **Initialization Order Issue**: Fixed FileIndexer initialization to occur after conversation_history_path is set in OpenInterpreter constructor
- **Missing Import Path**: Fixed lazy_import path from `.utils.lazy_import` to `..core.utils.lazy_import` in server.py
- **Missing Return Statement**: Added `return app` at the end of create_colonel_katie_server function
- **Empty async_core.py**: Deleted problematic empty file that was causing circular import issues

### Added - Dependency Management
- **Required Dependencies**: Added installation instructions for `sentence_transformers`, `psycopg2-binary`, `qdrant-client`, `fastapi`, `uvicorn`, `python-multipart`
- **Platform Support**: Added `platformdirs` dependency for cross-platform storage path management

### Changed - Server Architecture
- **Server Function**: create_colonel_katie_server now properly returns FastAPI app instance
- **Import Structure**: Cleaned up import paths to prevent circular dependencies
- **Initialization Logic**: Reorganized OpenInterpreter initialization order for proper dependency resolution

### Verified - Server Functionality ✅
- **Server Startup**: FastAPI server now starts successfully on port 8000
- **API Endpoints**: OpenAPI specification endpoint responding correctly (HTTP 200)
- **Import Resolution**: All modules import successfully without circular dependency errors
- **Error Handling**: Robust error handling maintained throughout fix process

### Removed
- `AsyncInterpreter` class and server-related logic from `interpreter/core/async_core.py` (file is now empty).

## [2.0.0] - 2025-06-30 - KDE6 Integration Complete

### Added - Major KDE6 Enhancement
- **Complete PySide6 Migration**: All KDE tools migrated from `qdbus6` subprocess calls to native PySide6 D-Bus communication
- **Enhanced KDE Integration Class**: Comprehensive `kde.py` class with full KDE desktop functionality
- **Process Management**: System process monitoring, listing, killing, and finding capabilities
- **Application Launching**: Native KDE application launching with argument support
- **Advanced Desktop Control**: Full desktop environment automation capabilities
- **Enhanced Error Handling**: Native Qt error handling and exception management
- **Advanced Computer Control**: Added process management (list, kill, find), application launching, and file opening with specific applications.
- **Conversation State Management**: Implemented in-memory storage for conversation history using `conversation_id`.
- **Future Development Roadmap**: Created `Future_Development_Roadmap.md` outlining next steps for AI integration.
- **Cognitive Companion Integration**: `The_Colonel` can now serve as the AI backend for the `cognitive-companion` desktop application.
- PySide6 GUI Development: Initiated development of a native PySide6 GUI with direct `OpenInterpreter` integration. Implemented basic chat interface with Markdown and code highlighting, persistent settings management (API key, model selection), model display, and short-term memory using Redis. A detailed `GUI_Development_Plan.md` has been created.

### Changed - Performance & Architecture
- **Performance Improvements**: Removed subprocess overhead with direct D-Bus communication
- **Enhanced Reliability**: Better connection management and error recovery  
- **Future-Ready Architecture**: Foundation for advanced KDE6 GUI development
- **Updated project documentation**: Complete documentation refresh reflecting KDE6 integration
- **Refactored chunk processing logic**: Enhanced multi-message streaming in `openwebui_server.py`
- **Optimized error logging**: Improved logging system using Python's `logging` module

### Fixed - KDE Integration Issues
- **Import Errors**: Fixed missing subprocess and function imports in `kde.py`
- **Duplicate Methods**: Removed duplicate method definitions in KDE class
- **Syntax Errors**: Fixed syntax error on line 317 (`set_screensaver_active`)
- **Missing Dependencies**: Added all required clipboard and file operation imports
- **Testing environment setup issues**: Completely resolved
- **pytest execution**: Now fully functional in virtual environment
- **poetry PATH resolution**: Confirmed working
- **Module import stability**: janus and FastAPI verified
- **API key configuration**: Properly set up for testing

## [2025-06-30] - Testing Environment Resolution

### Fixed
- **Testing Infrastructure**: Resolved all persistent pytest execution issues
- **Dependencies**: Confirmed all required modules (janus, FastAPI) are properly installed
- **API Configuration**: Set up valid OpenAI and Anthropic API keys for testing
- **Import Stability**: Verified async_core.py and files.py imports work correctly
- **Test Suite**: All core module tests (8/8) now passing successfully

### Testing Results
- Core Module Tests: 8/8 PASSING
- File Operations Tests: 3/3 PASSING  
- Computer Tools Tests: 2/2 PASSING
- Async Core Tests: 3/3 PASSING

### Impact
The testing environment is now fully operational and ready for continuous integration and development workflows.

## [2025-06-29] - Native KDE6 GUI Development Complete

### Added
- **Native KDE6 GUI**: Complete PySide6-based graphical user interface
- **PySide6 Integration**: Full Qt6 Python bindings (v6.9.1) installed and functional
- **KDE Plasma Integration**: JavaScript evaluation and desktop notifications
- **Window Management**: Virtual desktop control and window information queries
- **Clipboard Operations**: Native KDE clipboard integration

### Enhanced
- **kde_tools/**: All modules refactored to use native PySide6 D-Bus communication
- **Desktop Integration**: Seamless integration with KDE Plasma desktop environment

## [2025-06-03] - Core OpenWebUI Integration

### Added
- **FastAPI Server**: Complete OpenWebUI-compatible server implementation
- **Individual Tool Servers**: 4 specialized tool servers for focused functionality
- **OpenAPI Specification**: Comprehensive API documentation with live serving
- **Profile System**: Dynamic profile loading with hot-swapping capabilities
- **Authentication System**: Bearer token authentication for remote access
- **Streaming Support**: Real-time Server-Sent Events for live response updates

### Technical Features
- OpenAI-compatible `/v1/chat/completions` endpoint
- Tool execution endpoints for Python, Shell, Files, and Computer control
- Environment-based API key management
- Robust error handling and recovery mechanisms
- CORS support for cross-origin requests

### Infrastructure
- Virtual environment setup with all dependencies
- CLI integration with `--openwebui_server` flag
- Development and production deployment modes
- Comprehensive documentation and usage examples

---

## Project Milestones

### Completed ✅
1. **Core OpenWebUI Integration** (2025-06-03)
2. **Native KDE6 GUI Development** (2025-06-29) 
3. **Testing Environment Setup** (2025-06-30)
4. **KDE6 Integration Complete** (2025-06-30) - All PySide6 migration completed

### Next Steps 🚀
Refer to `documentation/GUI_Development_Plan.md` for detailed GUI development roadmap and `documentation/Future_Development_Roadmap.md` for overall project direction.

---

*This changelog is maintained to provide clear visibility into project progress and changes.*