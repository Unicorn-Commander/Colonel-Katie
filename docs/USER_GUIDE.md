# 📚 Colonel Katie - User Guide

**Complete guide for using the Colonel Katie AI Agent Development Platform**

---

## 🎯 Getting Started

### First Time Setup

1. **Launch Colonel Katie**: Run the application using your launcher script
2. **Welcome Screen**: You'll see a splash screen during initialization
3. **Interface Overview**: Familiarize yourself with the three-panel layout
4. **Model Selection**: Choose your first AI model from the right sidebar

### Interface Layout

Colonel Katie uses a three-panel design:

- **Left Panel**: Conversation history and saved chats
- **Center Panel**: Main chat interface for AI interaction
- **Right Panel**: Settings, model selection, and advanced features

---

## 🤖 Creating Your First AI Agent

### Using the Agent Builder

1. **Open Agent Builder**:
   - Press `Ctrl+Shift+A` 
   - Or go to `Options → Agent Builder`

2. **General Settings**:
   - **Agent Name**: Choose a unique name (used for the .py profile file)
   - **Profile Picture**: Select an avatar image (PNG, JPG, JPEG, SVG)

3. **Choose a Prompt Template**:
   - **Browse Categories**: Filter by General, Development, Writing, etc.
   - **Preview Templates**: Click "Preview" to see full prompt details
   - **Popular Templates**:
     - **Helpful AI Assistant**: General-purpose assistant
     - **Code Reviewer**: Expert code analysis and feedback
     - **Creative Writer**: Storytelling and creative content
     - **Data Analyst**: Data analysis and visualization
     - **Research Assistant**: Academic and professional research

4. **Model Configuration**:
   - **Provider**: Choose Ollama (local), OpenAI, HuggingFace, or custom
   - **Model**: Select specific model (e.g., gpt-4, llama3, mixtral)
   - **API Settings**: Configure API keys and endpoints
   - **Context Window**: Set token limits (1024-200000)
   - **Temperature**: Control creativity (0.0-2.0)

5. **Tool Selection**:
   - **Shell Tool**: Allow command execution
   - **Browser Tool**: Enable web browsing
   - **Files Tool**: File system operations
   - **Custom Tools**: Add specialized capabilities

6. **Voice Settings**:
   - **TTS Profile**: Choose text-to-speech voice
   - **Voice Speed**: Adjust speaking rate
   - **Voice Enabled**: Toggle voice features

7. **Advanced Options**:
   - **OS Mode**: System-level operations
   - **Auto Run**: Automatic code execution
   - **Loop Mode**: Continuous conversation
   - **Import Computer API**: Advanced system integration

8. **Save Your Agent**: Click "Save Agent Profile" to create the .py file

---

## 💬 Chat Interface Guide

### Basic Chat Operations

#### Sending Messages
- **Type & Enter**: Write your message and press Enter
- **Voice Input**: Hold Space bar to record voice messages
- **Voice Output**: Click 🔊 icon next to responses to hear them

#### Message Management
- **Right-click Messages**: Access context menu for:
  - **Copy**: Copy message text
  - **Edit**: Modify your messages
  - **Regenerate**: Get new AI response
  - **Delete**: Remove messages
  - **React**: Add emoji reactions (👍, 👎, 😂, 🤔)

### Advanced Chat Features

#### Quick Settings Panel
- **Access**: Click ⚙️ button in chat action bar
- **Model Switching**: Change models mid-conversation
- **Temperature**: Adjust creativity on the fly
- **Max Tokens**: Control response length

#### Chat Header Information
- **Model Indicator**: Shows current active model
- **Token Usage**: Displays used/total tokens
- **Connection Status**: Shows system status

#### Action Bar Features
- **📄 Files**: Access file operations
- **🔍 Search**: Web search integration
- **🧠 RAG**: Knowledge base queries
- **🎙️ Voice**: Voice input toggle
- **⚙️ Settings**: Quick settings panel

---

## 📖 Document Management & RAG

### Uploading Documents

#### Drag & Drop Method
1. **Open Knowledge Management**: Expand section in right sidebar
2. **Drag Files**: Drop documents directly into the upload area
3. **Supported Formats**: PDF, DOCX, TXT, MD, HTML, code files
4. **Processing**: Watch the status indicator during indexing

#### File Browser Method
1. **Click "Load Documents"**: Opens file selection dialog
2. **Select Multiple Files**: Choose documents to upload
3. **Confirm Upload**: Files are automatically processed

### Managing Knowledge Base

#### Document Collections
- **View Loaded Documents**: See list in Knowledge Management section
- **Document Status**: Check processing status and errors
- **Search Documents**: RAG automatically searches during conversations
- **Remove Documents**: Delete from knowledge base when needed

#### RAG Integration
- **Automatic Retrieval**: Relevant documents are pulled into context
- **Semantic Search**: Find documents based on meaning, not just keywords
- **Context Injection**: Document content enhances AI responses
- **Source Citation**: AI can reference specific documents

---

## 🎙️ Voice Features

### Push-to-Talk
- **Activation**: Hold Space bar
- **Recording Modal**: Visual feedback during recording
- **Release**: Stop recording and automatically transcribe
- **Auto-send**: Transcribed text is sent as message

### Text-to-Speech
- **Speak Button**: Click 🔊 next to any AI response
- **Voice Profiles**: Different voices available in Agent Builder
- **Speed Control**: Adjust speaking rate
- **Stop/Pause**: Control playback

### Voice Settings
- **Enable/Disable**: Toggle voice features globally
- **Microphone Setup**: Ensure proper microphone permissions
- **Audio Quality**: Adjust recording quality in settings

---

## 💾 Memory Management

### How Memory Works
Colonel Katie uses mem0ai for persistent memory across conversations:

- **Automatic Extraction**: Important information is saved automatically
- **Context Retrieval**: Past memories inform new conversations
- **Long-term Learning**: Agents remember preferences and context

### Memory Features
- **View Memories**: Check extracted memories in right sidebar
- **Memory Summary**: See key points from conversations
- **Manual Management**: Add, edit, or delete specific memories
- **Memory Search**: Find past information quickly

---

## 📊 System Monitoring

### Status Bar Information
- **System Status**: Ready, Processing, Error states
- **RAM Usage**: Real-time memory consumption with progress bar
- **Model Status**: Current active model and provider
- **Connection Status**: Online/offline indicator with color coding
- **Time Display**: Current system time

### Performance Monitoring
- **Memory Warnings**: Alerts when RAM usage is high
- **Connection Issues**: Visual indicators for network problems
- **Processing Status**: Shows when AI is thinking/responding

---

## ⌨️ Keyboard Shortcuts

### Essential Shortcuts
| Shortcut | Action | Description |
|----------|--------|-------------|
| `Ctrl+L` | Focus Input | Jump to chat input field |
| `Ctrl+K` | Clear Chat | Clear conversation history |
| `F9` | Toggle Sidebars | Show/hide left and right panels |
| `Ctrl+Shift+A` | Agent Builder | Open agent creation dialog |
| `Ctrl+E` | Export Chat | Save conversation to file |
| `Space` (hold) | Voice Input | Push-to-talk recording |
| `Ctrl+Q` | Quit | Exit Colonel Katie |

### Power User Tips
- **Escape**: Cancel current operation or close modals
- **Ctrl+Enter**: Send message without releasing focus
- **Tab**: Navigate between interface elements
- **F11**: Toggle fullscreen (if supported)

---

## 🔧 Configuration & Settings

### Environment Variables
Create a `.env` file in the application directory:

```bash
# API Keys
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
HUGGINGFACE_TOKEN=your_hf_token

# Default Settings
DEFAULT_MODEL=gpt-4
DEFAULT_PROVIDER=openai
TTS_ENABLED=true
STT_ENABLED=true
MEMORY_ENABLED=true
RAG_ENABLED=true
```

### Model Provider Setup

#### Ollama (Local Models)
1. **Install Ollama**: Download from https://ollama.ai
2. **Pull Models**: `ollama pull llama3`
3. **Auto-Discovery**: Colonel Katie finds models automatically

#### OpenAI
1. **Get API Key**: Sign up at https://platform.openai.com
2. **Set Environment Variable**: Add to .env file
3. **Select Models**: Choose from gpt-4, gpt-3.5-turbo, etc.

#### HuggingFace
1. **Create Account**: Sign up at https://huggingface.co
2. **Generate Token**: Create access token in settings
3. **Private Models**: Token required for private model access

---

**🦄⚡ Happy agent building with Colonel Katie! ⚡🦄**

*For additional support, check the GitHub repository and community discussions.*