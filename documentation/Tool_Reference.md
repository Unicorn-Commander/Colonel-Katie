# The_Colonel Tool Reference

**Individual automation tools for Open WebUI integration**

The_Colonel provides a comprehensive suite of specialized tools for automation, development, and system control. Each tool is designed as an independent service that can be integrated with Open WebUI for seamless AI-powered operations.

## 🐍 Python Code Executor

**Execute Python code with full interpreter capabilities**

### Configuration
```
Tool Server URL: http://your-ip:8264/python
API Key: your-auth-token
OpenAPI JSON: http://your-ip:8264/python/openapi.json
```

### Capabilities
- **Code Execution**: Run Python scripts with full library access
- **Data Analysis**: Process datasets, perform calculations, generate visualizations
- **File Processing**: Read, manipulate, and analyze files programmatically
- **API Integration**: Make HTTP requests, interact with web services
- **Machine Learning**: Use scikit-learn, pandas, numpy for data science tasks

### Example Use Cases
- "Calculate the average of these numbers: [1,2,3,4,5]"
- "Read this CSV file and show me the top 10 rows"
- "Create a bar chart from this data"
- "Install and import the requests library, then fetch data from an API"

### Request Format
```json
{
  "code": "print('Hello World')\nresult = 2 + 2\nprint(f'Result: {result}')"
}
```

### Response Format
```json
{
  "output": "Hello World\nResult: 4",
  "error": null
}
```

---

## 🔧 Shell Command Executor

**Execute shell/bash commands for system operations**

### Configuration
```
Tool Server URL: http://your-ip:8264/shell
API Key: your-auth-token
OpenAPI JSON: http://your-ip:8264/shell/openapi.json
```

### Capabilities
- **System Administration**: Manage processes, services, and system resources
- **File Operations**: Navigate directories, manage permissions, archive files
- **Network Operations**: Test connectivity, download files, manage network settings
- **Development Tools**: Git operations, build processes, package management
- **Monitoring**: Check system status, resource usage, log analysis

### Example Use Cases
- "Show me the current directory contents"
- "Check the system disk usage"
- "Download a file from this URL"
- "Create a backup archive of this directory"
- "Check if port 8080 is open"

### Request Format
```json
{
  "command": "ls -la /home/user"
}
```

### Response Format
```json
{
  "output": "total 24\ndrwxr-xr-x 3 user user 4096 Dec  1 10:00 .\ndrwxr-xr-x 3 root root 4096 Dec  1 09:00 ..",
  "error": null
}
```

---

## 📁 File Operations

**Read, write, and manage files on the local filesystem**

### Configuration
```
Tool Server URL: http://your-ip:8264/files
API Key: your-auth-token
OpenAPI JSON: http://your-ip:8264/files/openapi.json
```

### Capabilities
- **File Reading**: Read text files, configuration files, logs, data files
- **File Writing**: Create documents, save data, generate reports
- **Content Management**: Append to files, modify content, backup files
- **Format Support**: Plain text, JSON, CSV, XML, YAML, and more
- **Path Management**: Automatic directory creation, path validation

### Available Operations

#### Read File
Read the contents of any file from the filesystem.

**Endpoint**: `POST /files/read`

**Use Cases**:
- "Read the contents of /etc/hosts"
- "Show me what's in the config.json file"
- "Display the last log entries from application.log"

**Request Format**:
```json
{
  "path": "/path/to/file.txt"
}
```

**Response Format**:
```json
{
  "content": "File contents here...",
  "error": null
}
```

#### Write File
Write or create files with specified content.

**Endpoint**: `POST /files/write`

**Use Cases**:
- "Create a new README.md file with project documentation"
- "Save this JSON data to a configuration file"
- "Write a shell script to automate this task"

**Request Format**:
```json
{
  "path": "/path/to/newfile.txt",
  "content": "Content to write to the file"
}
```

**Response Format**:
```json
{
  "success": true,
  "error": null
}
```

---

## 🖥️ Computer Control

**Control mouse, keyboard, and screen capture for automation**

### Configuration
```
Tool Server URL: http://your-ip:8264/computer
API Key: your-auth-token
OpenAPI JSON: http://your-ip:8264/computer/openapi.json
```

### Capabilities
- **Screen Capture**: Take screenshots for analysis and documentation
- **Mouse Control**: Click at specific coordinates for UI automation
- **Keyboard Input**: Type text and send keystrokes to applications
- **GUI Automation**: Interact with desktop applications and web interfaces
- **Visual Analysis**: Capture and analyze screen content

### Available Operations

#### Screenshot Capture
Take screenshots of the current desktop or active window.

**Endpoint**: `POST /computer/screenshot`

**Use Cases**:
- "Take a screenshot of the current screen"
- "Capture the desktop for documentation"
- "Show me what's currently displayed"

**Request Format**:
```json
{}
```

**Response Format**:
```json
{
  "output": "Screenshot saved to /tmp/screenshot.png",
  "error": null
}
```

#### Mouse Click
Perform mouse clicks at specific screen coordinates.

**Endpoint**: `POST /computer/click`

**Use Cases**:
- "Click on the button at coordinates (100, 200)"
- "Click the submit button"
- "Automate clicking through a UI workflow"

**Request Format**:
```json
{
  "x": 100,
  "y": 200
}
```

**Response Format**:
```json
{
  "output": "Clicked at coordinates (100, 200)",
  "error": null
}
```

#### Keyboard Input
Type text at the current cursor position.

**Endpoint**: `POST /computer/type`

**Use Cases**:
- "Type this text into the active form field"
- "Fill out form data automatically"
- "Enter text in the current application"

**Request Format**:
```json
{
  "text": "Hello, this is automated text input!"
}
```

**Response Format**:
```json
{
  "output": "Typed text successfully",
  "error": null
}
```

---

## 🔐 Security & Authentication

All tools require authentication when accessed remotely:

### Authentication Headers
```
Authorization: Bearer your-auth-token-here
```

### Local Development
- **Localhost access** (127.0.0.1, localhost) does not require authentication
- **Remote access** (0.0.0.0, external IPs) requires Bearer token authentication

### Security Best Practices
- Use strong, randomly generated auth tokens for production
- Limit network access to trusted sources
- Monitor tool usage and access logs
- Regularly rotate authentication tokens

---

## 🛠️ Integration Guide

### Open WebUI Setup

1. **Navigate to Tool Servers** in Open WebUI admin panel
2. **Add each tool separately** using the configurations above
3. **Test connectivity** by using each tool in a conversation
4. **Enable/disable tools** as needed for different use cases

### Tool Server Management

**Start The_Colonel server**:
```bash
./start_server_auth.sh
```

**Server endpoints**:
- Main chat: `http://localhost:8264/v1/chat/completions`
- Python tool: `http://localhost:8264/python/*`
- Shell tool: `http://localhost:8264/shell/*`
- Files tool: `http://localhost:8264/files/*`
- Computer tool: `http://localhost:8264/computer/*`

### Environment Configuration

Ensure your `.env` file contains:
```env
# API Keys
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
XAI_API_KEY=your_xai_key_here
DEEPSEEK_API_KEY=your_deepseek_key_here

# Server Configuration
DEFAULT_PROFILE=The_Colonel.py
SERVER_HOST=0.0.0.0
SERVER_PORT=8264
AUTH_TOKEN=your_secure_random_token

# General Settings
DISABLE_TELEMETRY=true
AUTO_RUN=false
SAFE_MODE=off
```

---

## 🚀 Advanced Usage

### Combining Tools
Tools can be used together in complex workflows:

1. **Use Shell tool** to list directory contents
2. **Use Files tool** to read specific files
3. **Use Python tool** to process and analyze the data
4. **Use Computer tool** to capture results

### Error Handling
All tools return consistent error formats:
```json
{
  "output": "",
  "error": "Detailed error message describing what went wrong"
}
```

### Performance Considerations
- Tools maintain isolated state to prevent interference
- Each tool execution preserves your main conversation context
- Heavy operations (large file processing, complex Python scripts) may take time
- Screenshots and computer control operations require GUI access

---

## 🌐 Browser Automation Tool

**Selenium-based web browser automation and control**

### Configuration
```
Tool Server URL: http://your-ip:8264/browser
API Key: your-auth-token
OpenAPI JSON: http://your-ip:8264/browser/openapi.json
```

### Capabilities
- **Navigation**: Go to URLs, reload pages, navigate browser history
- **Element Interaction**: Click buttons, fill forms, extract content
- **Web Scraping**: Extract text, HTML, and attributes from web pages
- **Web Search**: Perform Google searches and get structured results
- **Screenshots**: Capture browser screenshots for verification

### Available Endpoints
- `/navigate` - Navigate to a URL
- `/click` - Click web elements using CSS selectors or XPath
- `/fill` - Fill form fields with text
- `/extract` - Extract content from web elements or full page
- `/search` - Perform web searches
- `/screenshot` - Take browser screenshots

### Example Use Cases
- "Go to google.com and search for 'AI automation'"
- "Fill out this contact form with my information"
- "Extract all the product prices from this shopping page"
- "Take a screenshot of the current page"

---

## 📋 Clipboard Operations Tool

**Cross-platform clipboard content management**

### Configuration
```
Tool Server URL: http://your-ip:8264/clipboard
API Key: your-auth-token
OpenAPI JSON: http://your-ip:8264/clipboard/openapi.json
```

### Capabilities
- **Read Content**: Get current clipboard content
- **Write Content**: Copy text to clipboard
- **Paste Action**: Simulate keyboard paste operation
- **Cross-Platform**: Works on Windows, macOS, and Linux

### Available Endpoints
- `/read` - Read current clipboard content
- `/write` - Write text to clipboard
- `/paste` - Paste clipboard content using keyboard shortcut

### Example Use Cases
- "Copy this text to clipboard: 'Hello World'"
- "What's currently in my clipboard?"
- "Paste the clipboard content"

---

## 🚀 JavaScript Execution Tool

**Node.js JavaScript code execution environment**

### Configuration
```
Tool Server URL: http://your-ip:8264/javascript
API Key: your-auth-token
OpenAPI JSON: http://your-ip:8264/javascript/openapi.json
```

### Capabilities
- **Modern JavaScript**: ES6+ syntax support
- **Node.js Libraries**: Access to npm packages and Node.js APIs
- **Async Operations**: Promise and async/await support
- **JSON Processing**: Native JSON manipulation
- **File System**: Node.js fs module access

### Available Endpoints
- `/execute` - Execute JavaScript/Node.js code

### Example Use Cases
- "Create a simple HTTP server using Node.js"
- "Parse this JSON data and extract specific fields"
- "Generate a random UUID using crypto module"
- "Read and process a JSON file"

---

## 📊 R Programming Tool

**Statistical computing and data analysis with R**

### Configuration
```
Tool Server URL: http://your-ip:8264/r
API Key: your-auth-token
OpenAPI JSON: http://your-ip:8264/r/openapi.json
```

### Capabilities
- **Statistical Analysis**: Comprehensive statistical functions
- **Data Visualization**: Create plots and charts
- **Data Manipulation**: Process datasets with dplyr, tidyr
- **Machine Learning**: Statistical modeling and prediction
- **Bioinformatics**: Specialized packages for life sciences

### Available Endpoints
- `/execute` - Execute R statistical code

### Example Use Cases
- "Perform a linear regression analysis on this dataset"
- "Create a histogram of these values"
- "Calculate correlation matrix for these variables"
- "Generate summary statistics for this data"

---

## 🍎 AppleScript Automation Tool

**macOS system automation using AppleScript**

### Configuration
```
Tool Server URL: http://your-ip:8264/applescript
API Key: your-auth-token
OpenAPI JSON: http://your-ip:8264/applescript/openapi.json
```

### Capabilities
- **Application Control**: Automate macOS applications
- **System Operations**: Control system preferences and settings
- **UI Automation**: Interact with application interfaces
- **File Management**: Advanced file operations through Finder
- **Workflow Integration**: Connect different macOS applications

### Available Endpoints
- `/execute` - Execute AppleScript automation code

### Example Use Cases
- "Open Safari and navigate to a specific webpage"
- "Create a new document in Pages with specific content"
- "Send an email through Mail app"
- "Control iTunes/Music app playback"

**Note**: Only available on macOS systems

---

## 📱 SMS/Messages Tool

**SMS and iMessage operations for macOS**

### Configuration
```
Tool Server URL: http://your-ip:8264/sms
API Key: your-auth-token
OpenAPI JSON: http://your-ip:8264/sms/openapi.json
```

### Capabilities
- **Send Messages**: Send SMS and iMessages to contacts
- **Message History**: Retrieve conversation history
- **Contact Integration**: Work with macOS Contacts
- **Search Messages**: Find messages by content or contact
- **Full Disk Access**: Secure access to Messages database

### Available Endpoints
- `/send` - Send SMS/iMessage to a contact
- `/get` - Retrieve message history with filters

### Example Use Cases
- "Send a text message to John saying 'Meeting at 3pm'"
- "Get my last 10 messages from Mom"
- "Find all messages containing 'project deadline'"
- "Send an iMessage with meeting details"

**Note**: Only available on macOS. Requires Full Disk Access permission.

---

## 👁️ Computer Vision & OCR Tool

**AI-powered image analysis and text recognition**

### Configuration
```
Tool Server URL: http://your-ip:8264/vision
API Key: your-auth-token
OpenAPI JSON: http://your-ip:8264/vision/openapi.json
```

### Capabilities
- **Image Analysis**: AI-powered image description and analysis
- **OCR (Optical Character Recognition)**: Extract text from images
- **Screenshot Analysis**: Take and analyze screenshots automatically
- **Multi-format Support**: Process various image formats
- **Custom Prompts**: Directed analysis with specific questions

### Available Endpoints
- `/analyze` - Analyze image content with AI
- `/ocr` - Extract text from images using OCR
- `/screenshot_analyze` - Take screenshot and analyze with AI

### Example Use Cases
- "Analyze this screenshot and tell me what's happening"
- "Extract all text from this image of a document"
- "Take a screenshot and describe the current desktop"
- "What products are shown in this product catalog image?"

---

## 📚 Examples & Workflows

### Data Analysis Workflow
1. **Shell**: List available data files
2. **Files**: Read CSV data file
3. **Python**: Process data with pandas, create visualizations
4. **R**: Perform statistical analysis and create professional plots
5. **Files**: Save processed results

### Web Automation Workflow
1. **Browser**: Navigate to target website
2. **Browser**: Search for specific content
3. **Browser**: Extract relevant data from results
4. **Clipboard**: Copy extracted data for further processing
5. **Python**: Process and analyze the extracted data

### Cross-Platform Development Workflow
1. **Python**: Write core algorithm
2. **JavaScript**: Create Node.js implementation
3. **R**: Add statistical analysis capabilities
4. **Files**: Save implementations in different languages
5. **Shell**: Test all implementations

### macOS Automation Workflow
1. **Vision**: Take screenshot to analyze current state
2. **AppleScript**: Open required applications
3. **SMS**: Send status notifications
4. **Clipboard**: Transfer data between applications
5. **AppleScript**: Complete automation tasks

### System Administration Workflow
1. **Shell**: Check system status and logs
2. **Files**: Read configuration files
3. **Python**: Parse and analyze configuration
4. **Files**: Write updated configuration
5. **Shell**: Restart services

### Document Processing Workflow
1. **Vision**: Take screenshot of document or use OCR on image
2. **Clipboard**: Copy extracted text
3. **Python**: Process and clean extracted text
4. **Files**: Save cleaned document
5. **R**: Perform text analysis if needed

### GUI Automation Workflow
1. **Computer**: Take screenshot to see current state
2. **Computer**: Click specific UI elements
3. **Computer**: Type required information
4. **Vision**: Verify completion by analyzing final screenshot

---

## 🔧 Troubleshooting

### Common Issues

**Tool not responding**:
- Verify auth token is correct
- Check network connectivity to The_Colonel server
- Ensure server is running on correct port

**Permission errors**:
- File operations require appropriate filesystem permissions
- Computer control requires GUI/desktop access
- Shell commands may need sudo for system operations

**Python execution errors**:
- Check if required libraries are installed
- Verify Python syntax and logic
- Some operations may require additional dependencies

### Debug Information

**Check tool server status**:
```bash
curl -H "Authorization: Bearer your-token" http://localhost:8264/python/openapi.json
```

**Test individual tool**:
```bash
curl -X POST -H "Content-Type: application/json" \
     -H "Authorization: Bearer your-token" \
     -d '{"code": "print(\"Hello World\")"}' \
     http://localhost:8264/python/execute
```

---

*For additional support, configuration details, and advanced usage examples, see the main [Technical Implementation Guide](Technical_Implementation_Guide.md) and [Project Summary](Project_Summary.md).*