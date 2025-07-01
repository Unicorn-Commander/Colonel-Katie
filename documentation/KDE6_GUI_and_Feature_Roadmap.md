# Colonel Katie: KDE6 GUI and Feature Roadmap

This document outlines the strategic vision for "Colonel Katie," a KDE6-specific fork of "The Colonel," aiming to achieve feature parity with Open WebUI in a native desktop environment, while laying the groundwork for future web and mobile applications.

## 1. Features & Functionality (Open WebUI Parity for Desktop)

"Colonel Katie" will provide a rich, interactive experience for Large Language Models (LLMs), adapted for a native KDE6 desktop context. Key functionalities include:

*   **Core Conversational Interface:** Multi-turn chat, rich Markdown rendering, code highlighting, image display, dynamic input area, and LLM generation indicators.
*   **LLM Management & Configuration:** Seamless switching between local (Ollama, LM Studio) and remote (OpenAI, Gemini, custom API) LLMs, with user-friendly controls for model parameters (temperature, top_p, max_tokens, etc.) and secure API key management.
*   **Tool & Plugin Integration (Leveraging KDE):** Robust mechanism for LLM to invoke external tools, clear display of tool outputs, support for user-defined tools, and deep integration with KDE-specific actions (KRunner, KWin scripting, Plasma widgets, system settings, application launching).
*   **Context & Memory Management:** Persistent conversation history, strategies for handling long contexts (summarization, RAG), integration with vector databases (`interpreter/memory`) for Retrieval Augmented Generation (RAG), and local file indexing (`interpreter/file_indexing`).
*   **File Handling & Multimedia:** Drag-and-drop file attachment, processing of file contents by LLMs, and integration of voice input (Speech-to-Text) and voice output (Text-to-Speech).
*   **User Experience & Customization:** Theming (light/dark modes, KDE themes), comprehensive keyboard shortcuts, conversation export/import, and robust offline mode support for local LLMs.

## 2. GUI Plan for a Top-Notch KDE6 Experience

The GUI for "Colonel Katie" will be native, performant, and adhere strictly to KDE's Human Interface Guidelines (HIG).

**Recommended GUI Stack:**
*   **Primary Framework:** PySide6
*   **UI Toolkit:** QtQuick (QML) with Kirigami (for native KDE look and feel).

**Phased GUI Development Plan:**

### Phase 1: Foundation & Core Chat (QML/Kirigami First)
*   **UX Research & Wireframing:** Analyze Open WebUI patterns, study KDE HIG, and create detailed wireframes for a clean, intuitive KDE-native layout.
*   **Project Setup:** Establish clear project structure for QML, Python backend, and data models; set up PySide6/QML build integration.
*   **Main Window & Layout:** Implement using `Kirigami.ApplicationWindow`, responsive layout with `Kirigami.Page` and `Kirigami.SplitView`, including left sidebar for history and right sidebar for settings.
*   **Core Chat View:** Develop custom QML component for message display with Markdown rendering, syntax highlighting, image display, smooth scrolling, and an interactive input area with "Stop Generation" button.

### Phase 2: LLM & Tool Management
*   **Model Selection UI:** Dedicated section for LLM selection and clear indication of active model.
*   **Parameter Controls:** Implement interactive controls (sliders, spinboxes, text fields) for LLM parameters with real-time feedback.
*   **Tool Output Integration:** Design clear presentation of tool calls and outputs within chat, potentially with a dedicated "Tool Log" view.
*   **KDE-Specific Tool UI:** Create intuitive dialogs/overlays using Kirigami for tools requiring user interaction (e.g., window selection).

### Phase 3: Advanced Features & Polish
*   **Settings Dialog:** Comprehensive settings using `Kirigami.SettingsPage` for general, LLM APIs, tool configuration, memory/RAG, and KDE integration.
*   **File Handling:** Implement drag-and-drop, visual cues for attached files, and `FileDialog` integration.
*   **Voice Integration:** Microphone icon for STT and speaker icon for TTS.
*   **Memory & RAG UI:** Visual representation and management controls for indexed knowledge bases.
*   **Theming & Accessibility:** Full compatibility with KDE's Breeze theme, system-wide dark/light modes, and accessibility features.
*   **Performance Optimization:** Asynchronous LLM calls and tool execution, and QML rendering optimization for UI responsiveness.

## 3. Architectural Considerations for Cross-Platform Parity

To ensure future parity with web and phone applications, a strong **separation of concerns** will be maintained:

*   **Core Logic (Backend):** All LLM interaction, tool execution, memory management, and file processing logic will reside in the `interpreter/` directory, implemented as framework-agnostic Python code.
*   **API Layer:** The core logic will be exposed via a well-defined API (e.g., FastAPI, Flask), serving as the communication bridge for all frontends.
*   **GUI (Frontend):** The `gui/` directory will contain platform-specific UI code (PySide6/QML for desktop, React/Vue for web, Flutter/Compose Multiplatform for mobile), all communicating with the shared API layer.

This architectural approach ensures reusability, maintainability, and a unified experience across all target platforms.
