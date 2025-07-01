import asyncio
import json
import os
import tempfile
import time
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Union

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        print(f"📝 Loaded environment variables from {env_path}")
except ImportError:
    print("📝 python-dotenv not installed, using system environment variables only")

from fastapi import FastAPI, HTTPException, Request, Response, UploadFile, File, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel
import uvicorn

from ..core.utils.lazy_import import lazy_import

# Lazy imports for dependencies
uvicorn = lazy_import("uvicorn")
fastapi = lazy_import("fastapi")


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str = "the-colonel"
    messages: List[ChatMessage]
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    stream: bool = False


class ChatCompletionResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Dict]


class ExecuteCodeRequest(BaseModel):
    code: str


class ExecuteShellRequest(BaseModel):
    command: str


class FileReadRequest(BaseModel):
    path: str


class FileWriteRequest(BaseModel):
    path: str
    content: str


class BrowserNavigateRequest(BaseModel):
    url: str


class BrowserClickRequest(BaseModel):
    selector: str
    selector_type: str = "css"


class BrowserFillRequest(BaseModel):
    selector: str
    text: str
    clear_first: bool = True


class BrowserExtractRequest(BaseModel):
    selector: Optional[str] = None
    extract_type: str = "text"
    attribute: Optional[str] = None


class WebSearchRequest(BaseModel):
    query: str
    max_results: int = 10


class ClipboardWriteRequest(BaseModel):
    text: str


class SMSSendRequest(BaseModel):
    to: str
    message: str


class SMSGetRequest(BaseModel):
    contact: Optional[str] = None
    limit: int = 10
    substring: Optional[str] = None


class VisionAnalyzeRequest(BaseModel):
    image_path: Optional[str] = None
    image_base64: Optional[str] = None
    prompt: str = "Describe what you see in this image"


class VisionOCRRequest(BaseModel):
    image_path: Optional[str] = None
    image_base64: Optional[str] = None


class VisionScreenshotAnalyzeRequest(BaseModel):
    prompt: str = "Describe what you see in this screenshot"


def create_colonel_katie_server(interpreter, host="localhost", port=8264, auth_token=None):
    """Create FastAPI server for Open WebUI integration"""
    
    app = FastAPI(
        title="The_Colonel Tool Server",
        description="Individual tools for code execution, file operations, and computer control",
        version="0.1.0",
        openapi_url=None  # Disable auto-generated OpenAPI
    )
    
    # Enable CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Security
    security = HTTPBearer(auto_error=False) if auth_token else None
    
    def verify_auth(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)):
        """Verify authentication for remote access"""
        if host == "localhost" or host == "127.0.0.1":
            return True  # No auth required for localhost
        
        if auth_token and (not credentials or credentials.credentials != auth_token):
            raise HTTPException(status_code=401, detail="Invalid authentication")
        return True
    
    def load_profile(profile_name: Optional[str] = None):
        """Load profile configuration (defaults to fast.yaml for gpt-4o-mini)"""
        if not profile_name:
            profile_name = "fast.yaml"  # Default to fast profile with gpt-4o-mini
            
        # Look for profile in profiles directory
        profiles_dir = Path(__file__).parent.parent / "terminal_interface" / "profiles" / "defaults"
        
        # Try both .py and .yaml/.yml extensions
        for ext in [".py", ".yaml", ".yml"]:
            profile_file = profiles_dir / f"{profile_name.replace('.yaml', '').replace('.yml', '')}{ext}"
            if profile_file.exists():
                break
        else:
            # If no profile file found, try the built-in profile loading
            try:
                from interpreter.terminal_interface.profiles.profiles import profile
                profile(interpreter, profile_name)
                print(f"Loaded profile: {profile_name}")
                return True
            except Exception as e:
                print(f"Error loading profile {profile_name}: {e}")
                return None
        
        if profile_file.exists():
            try:
                # Import and return profile configuration
                import importlib.util
                spec = importlib.util.spec_from_file_location(profile_name, profile_file)
                profile_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(profile_module)
                
                # Apply profile settings to interpreter
                if hasattr(profile_module, 'interpreter'):
                    profile_config = profile_module.interpreter
                    for key, value in profile_config.items():
                        if hasattr(interpreter, key):
                            setattr(interpreter, key, value)
                        elif hasattr(interpreter.llm, key):
                            setattr(interpreter.llm, key, value)
                            
                return profile_config
            except Exception as e:
                print(f"Error loading profile {profile_name}: {e}")
        
        return None
    
    @app.get("/openapi.json")
    async def get_openapi():
        """Serve custom OpenAPI specification"""
        openapi_path = Path(__file__).parent.parent.parent / "openapi.json"
        if openapi_path.exists():
            import json
            with open(openapi_path, 'r') as f:
                custom_spec = json.load(f)
            return custom_spec
        else:
            raise HTTPException(status_code=404, detail="OpenAPI specification not found")
    
    @app.get("/tools/openapi.json")
    async def get_tools_openapi():
        """Serve Tools-only OpenAPI specification for Open WebUI"""
        simple_tools_path = Path(__file__).parent.parent.parent / "simple_tools.json"
        if simple_tools_path.exists():
            import json
            with open(simple_tools_path, 'r') as f:
                tools_spec = json.load(f)
            return tools_spec
        else:
            raise HTTPException(status_code=404, detail="Simple tools OpenAPI specification not found")
    
    # Individual tool OpenAPI specifications
    @app.get("/python/openapi.json")
    async def get_python_openapi():
        """Python tool OpenAPI specification"""
        spec_path = Path(__file__).parent.parent.parent / "python_tool_spec.json"
        if spec_path.exists():
            import json
            with open(spec_path, 'r') as f:
                spec = json.load(f)
                # Update server URL to match current host/port
                spec["servers"] = [{"url": f"http://{host}:{port}/python"}]
            return spec
        else:
            raise HTTPException(status_code=404, detail="Python tool specification not found")
    
    @app.get("/browser/openapi.json")
    async def get_browser_openapi():
        """Browser automation tool OpenAPI specification"""
        spec_path = Path(__file__).parent.parent.parent / "browser_tool_spec.json"
        if spec_path.exists():
            import json
            with open(spec_path, 'r') as f:
                spec = json.load(f)
                spec["servers"] = [{"url": f"http://{host}:{port}/browser"}]
            return spec
        else:
            raise HTTPException(status_code=404, detail="Browser tool specification not found")
    
    @app.get("/clipboard/openapi.json")
    async def get_clipboard_openapi():
        """Clipboard operations tool OpenAPI specification"""
        spec_path = Path(__file__).parent.parent.parent / "clipboard_tool_spec.json"
        if spec_path.exists():
            import json
            with open(spec_path, 'r') as f:
                spec = json.load(f)
                spec["servers"] = [{"url": f"http://{host}:{port}/clipboard"}]
            return spec
        else:
            raise HTTPException(status_code=404, detail="Clipboard tool specification not found")
    
    @app.get("/javascript/openapi.json")
    async def get_javascript_openapi():
        """JavaScript execution tool OpenAPI specification"""
        spec_path = Path(__file__).parent.parent.parent / "javascript_tool_spec.json"
        if spec_path.exists():
            import json
            with open(spec_path, 'r') as f:
                spec = json.load(f)
                spec["servers"] = [{"url": f"http://{host}:{port}/javascript"}]
            return spec
        else:
            raise HTTPException(status_code=404, detail="JavaScript tool specification not found")
    
    @app.get("/r/openapi.json")
    async def get_r_openapi():
        """R programming tool OpenAPI specification"""
        spec_path = Path(__file__).parent.parent.parent / "r_tool_spec.json"
        if spec_path.exists():
            import json
            with open(spec_path, 'r') as f:
                spec = json.load(f)
                spec["servers"] = [{"url": f"http://{host}:{port}/r"}]
            return spec
        else:
            raise HTTPException(status_code=404, detail="R tool specification not found")
    
    @app.get("/applescript/openapi.json")
    async def get_applescript_openapi():
        """AppleScript automation tool OpenAPI specification"""
        spec_path = Path(__file__).parent.parent.parent / "applescript_tool_spec.json"
        if spec_path.exists():
            import json
            with open(spec_path, 'r') as f:
                spec = json.load(f)
                spec["servers"] = [{"url": f"http://{host}:{port}/applescript"}]
            return spec
        else:
            raise HTTPException(status_code=404, detail="AppleScript tool specification not found")
    
    @app.get("/sms/openapi.json")
    async def get_sms_openapi():
        """SMS/Messages tool OpenAPI specification"""
        spec_path = Path(__file__).parent.parent.parent / "sms_tool_spec.json"
        if spec_path.exists():
            import json
            with open(spec_path, 'r') as f:
                spec = json.load(f)
                spec["servers"] = [{"url": f"http://{host}:{port}/sms"}]
            return spec
        else:
            raise HTTPException(status_code=404, detail="SMS tool specification not found")
    
    @app.get("/vision/openapi.json")
    async def get_vision_openapi():
        """Computer vision & OCR tool OpenAPI specification"""
        spec_path = Path(__file__).parent.parent.parent / "vision_tool_spec.json"
        if spec_path.exists():
            import json
            with open(spec_path, 'r') as f:
                spec = json.load(f)
                spec["servers"] = [{"url": f"http://{host}:{port}/vision"}]
            return spec
        else:
            raise HTTPException(status_code=404, detail="Vision tool specification not found")
    
    @app.get("/shell/openapi.json")
    async def get_shell_openapi():
        """Shell tool OpenAPI specification"""
        spec_path = Path(__file__).parent.parent.parent / "shell_tool_spec.json"
        if spec_path.exists():
            import json
            with open(spec_path, 'r') as f:
                spec = json.load(f)
                spec["servers"] = [{"url": f"http://{host}:{port}/shell"}]
            return spec
        else:
            raise HTTPException(status_code=404, detail="Shell tool specification not found")
    
    @app.get("/files/openapi.json")
    async def get_files_openapi():
        """Files tool OpenAPI specification"""
        spec_path = Path(__file__).parent.parent.parent / "files_tool_spec.json"
        if spec_path.exists():
            import json
            with open(spec_path, 'r') as f:
                spec = json.load(f)
                spec["servers"] = [{"url": f"http://{host}:{port}/files"}]
            return spec
        else:
            raise HTTPException(status_code=404, detail="Files tool specification not found")
    
    @app.get("/computer/openapi.json")
    async def get_computer_openapi():
        """Computer control tool OpenAPI specification"""
        spec_path = Path(__file__).parent.parent.parent / "computer_tool_spec.json"
        if spec_path.exists():
            import json
            with open(spec_path, 'r') as f:
                spec = json.load(f)
                spec["servers"] = [{"url": f"http://{host}:{port}/computer"}]
            return spec
        else:
            raise HTTPException(status_code=404, detail="Computer tool specification not found")
    
    @app.get("/api/v1/tools/")
    async def list_tools(_: bool = Depends(verify_auth)):
        """List available tools for Open WebUI discovery"""
        return [
            {
                "id": "python_executor",
                "name": "Python Code Executor", 
                "description": "Execute Python code with full interpreter capabilities",
                "url": f"http://{host}:{port}/v1/tools/execute/python",
                "method": "POST",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "Python code to execute"
                        }
                    },
                    "required": ["code"]
                }
            },
            {
                "id": "shell_executor",
                "name": "Shell Command Executor",
                "description": "Execute shell/bash commands", 
                "url": f"http://{host}:{port}/v1/tools/execute/shell",
                "method": "POST",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string", 
                            "description": "Shell command to execute"
                        }
                    },
                    "required": ["command"]
                }
            },
            {
                "id": "file_reader",
                "name": "File Reader",
                "description": "Read contents of any file",
                "url": f"http://{host}:{port}/v1/tools/files/read", 
                "method": "POST",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "File path to read"
                        }
                    },
                    "required": ["path"]
                }
            },
            {
                "id": "file_writer", 
                "name": "File Writer",
                "description": "Write or create files",
                "url": f"http://{host}:{port}/v1/tools/files/write",
                "method": "POST",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "File path to write to"
                        },
                        "content": {
                            "type": "string",
                            "description": "Content to write"
                        }
                    },
                    "required": ["path", "content"]
                }
            },
            {
                "id": "screenshot_capture",
                "name": "Screenshot Capture", 
                "description": "Take screenshots of the desktop",
                "url": f"http://{host}:{port}/v1/tools/computer/screenshot",
                "method": "POST",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "id": "mouse_click",
                "name": "Mouse Click",
                "description": "Click at screen coordinates",
                "url": f"http://{host}:{port}/v1/tools/computer/click",
                "method": "POST", 
                "parameters": {
                    "type": "object",
                    "properties": {
                        "x": {
                            "type": "integer",
                            "description": "X coordinate"
                        },
                        "y": {
                            "type": "integer", 
                            "description": "Y coordinate"
                        }
                    },
                    "required": ["x", "y"]
                }
            },
            {
                "id": "keyboard_input",
                "name": "Keyboard Input",
                "description": "Type text input",
                "url": f"http://{host}:{port}/v1/tools/computer/type",
                "method": "POST",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "Text to type"
                        }
                    },
                    "required": ["text"]
                }
            },
            {
                "id": "key_press",
                "name": "Key Press",
                "description": "Send key presses and shortcuts", 
                "url": f"http://{host}:{port}/v1/tools/computer/key",
                "method": "POST",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "key": {
                            "type": "string",
                            "description": "Key or combination to press"
                        }
                    },
                    "required": ["key"]
                }
            },
            {
                "id": "browser_navigate",
                "name": "Browser Navigate",
                "description": "Navigate browser to a URL",
                "url": f"http://{host}:{port}/browser/navigate",
                "method": "POST",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "URL to navigate to"
                        }
                    },
                    "required": ["url"]
                }
            },
            {
                "id": "browser_click",
                "name": "Browser Click",
                "description": "Click web elements",
                "url": f"http://{host}:{port}/browser/click",
                "method": "POST",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "selector": {
                            "type": "string",
                            "description": "CSS selector or XPath"
                        },
                        "selector_type": {
                            "type": "string",
                            "default": "css",
                            "description": "Type of selector"
                        }
                    },
                    "required": ["selector"]
                }
            },
            {
                "id": "web_search",
                "name": "Web Search",
                "description": "Search the web using Google",
                "url": f"http://{host}:{port}/browser/search",
                "method": "POST",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query"
                        },
                        "max_results": {
                            "type": "integer",
                            "default": 10,
                            "description": "Maximum results"
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "id": "clipboard_read",
                "name": "Clipboard Read",
                "description": "Read clipboard content",
                "url": f"http://{host}:{port}/clipboard/read",
                "method": "GET"
            },
            {
                "id": "clipboard_write",
                "name": "Clipboard Write",
                "description": "Write text to clipboard",
                "url": f"http://{host}:{port}/clipboard/write",
                "method": "POST",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "Text to copy"
                        }
                    },
                    "required": ["text"]
                }
            },
            {
                "id": "javascript_execute",
                "name": "JavaScript Execute",
                "description": "Execute JavaScript/Node.js code",
                "url": f"http://{host}:{port}/javascript/execute",
                "method": "POST",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "JavaScript code to execute"
                        }
                    },
                    "required": ["code"]
                }
            },
            {
                "id": "r_execute",
                "name": "R Execute",
                "description": "Execute R statistical code",
                "url": f"http://{host}:{port}/r/execute",
                "method": "POST",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "R code to execute"
                        }
                    },
                    "required": ["code"]
                }
            },
            {
                "id": "applescript_execute",
                "name": "AppleScript Execute",
                "description": "Execute AppleScript for macOS automation",
                "url": f"http://{host}:{port}/applescript/execute",
                "method": "POST",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "AppleScript code to execute"
                        }
                    },
                    "required": ["code"]
                }
            },
            {
                "id": "sms_send",
                "name": "SMS Send",
                "description": "Send SMS/iMessage (macOS)",
                "url": f"http://{host}:{port}/sms/send",
                "method": "POST",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "to": {
                            "type": "string",
                            "description": "Phone number or contact"
                        },
                        "message": {
                            "type": "string",
                            "description": "Message to send"
                        }
                    },
                    "required": ["to", "message"]
                }
            },
            {
                "id": "vision_analyze",
                "name": "Vision Analyze",
                "description": "AI-powered image analysis",
                "url": f"http://{host}:{port}/vision/analyze",
                "method": "POST",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "image_path": {
                            "type": "string",
                            "description": "Path to image file"
                        },
                        "prompt": {
                            "type": "string",
                            "default": "Describe what you see",
                            "description": "Analysis prompt"
                        }
                    }
                }
            },
            {
                "id": "vision_ocr",
                "name": "Vision OCR",
                "description": "Extract text from images",
                "url": f"http://{host}:{port}/vision/ocr",
                "method": "POST",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "image_path": {
                            "type": "string",
                            "description": "Path to image file"
                        }
                    }
                }
            }
        ]
    
    # Individual tool discovery endpoints for Open WebUI
    @app.get("/python_executor")
    async def python_executor_info(_: bool = Depends(verify_auth)):
        """Python Code Executor tool info"""
        return {
            "id": "python_executor",
            "name": "Python Code Executor",
            "description": "Execute Python code with full interpreter capabilities",
            "url": f"http://{host}:{port}/v1/tools/execute/python",
            "method": "POST"
        }
    
    @app.get("/shell_executor") 
    async def shell_executor_info(_: bool = Depends(verify_auth)):
        """Shell Command Executor tool info"""
        return {
            "id": "shell_executor",
            "name": "Shell Command Executor", 
            "description": "Execute shell/bash commands",
            "url": f"http://{host}:{port}/v1/tools/execute/shell",
            "method": "POST"
        }
    
    @app.get("/file_reader")
    async def file_reader_info(_: bool = Depends(verify_auth)):
        """File Reader tool info"""
        return {
            "id": "file_reader",
            "name": "File Reader",
            "description": "Read contents of any file", 
            "url": f"http://{host}:{port}/v1/tools/files/read",
            "method": "POST"
        }
    
    @app.get("/file_writer")
    async def file_writer_info(_: bool = Depends(verify_auth)):
        """File Writer tool info"""
        return {
            "id": "file_writer",
            "name": "File Writer",
            "description": "Write or create files",
            "url": f"http://{host}:{port}/v1/tools/files/write", 
            "method": "POST"
        }
    
    @app.get("/screenshot_capture")
    async def screenshot_capture_info(_: bool = Depends(verify_auth)):
        """Screenshot Capture tool info"""
        return {
            "id": "screenshot_capture",
            "name": "Screenshot Capture",
            "description": "Take screenshots of the desktop",
            "url": f"http://{host}:{port}/v1/tools/computer/screenshot",
            "method": "POST"
        }
    
    @app.get("/mouse_click")
    async def mouse_click_info(_: bool = Depends(verify_auth)):
        """Mouse Click tool info"""
        return {
            "id": "mouse_click", 
            "name": "Mouse Click",
            "description": "Click at screen coordinates",
            "url": f"http://{host}:{port}/v1/tools/computer/click",
            "method": "POST"
        }
    
    @app.get("/keyboard_input")
    async def keyboard_input_info(_: bool = Depends(verify_auth)):
        """Keyboard Input tool info"""
        return {
            "id": "keyboard_input",
            "name": "Keyboard Input", 
            "description": "Type text input",
            "url": f"http://{host}:{port}/v1/tools/computer/type",
            "method": "POST"
        }
    
    @app.get("/key_press")
    async def key_press_info(_: bool = Depends(verify_auth)):
        """Key Press tool info"""
        return {
            "id": "key_press",
            "name": "Key Press",
            "description": "Send key presses and shortcuts", 
            "url": f"http://{host}:{port}/v1/tools/computer/key",
            "method": "POST"
        }
    
    # Individual tool endpoints
    @app.post("/python/execute")
    async def python_tool_execute(request: ExecuteCodeRequest, _: bool = Depends(verify_auth)):
        """Python Code Executor - Execute Python code"""
        try:
            # Save current state
            saved_messages = interpreter.messages.copy()
            interpreter.messages = []
            result_chunks = []
            
            for chunk in interpreter.chat(f"```python\n{request.code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            
            # Restore previous state
            interpreter.messages = saved_messages
            
            output = "".join(result_chunks)
            return {"output": output, "error": None}
            
        except Exception as e:
            return {"output": "", "error": str(e)}
    
    @app.post("/shell/execute")
    async def shell_tool_execute(request: ExecuteShellRequest, _: bool = Depends(verify_auth)):
        """Shell Command Executor - Execute shell commands"""
        try:
            # Save current state
            saved_messages = interpreter.messages.copy()
            interpreter.messages = []
            result_chunks = []
            
            for chunk in interpreter.chat(f"```bash\n{request.command}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            
            # Restore previous state
            interpreter.messages = saved_messages
            
            output = "".join(result_chunks)
            return {"output": output, "error": None}
            
        except Exception as e:
            return {"output": "", "error": str(e)}
    
    @app.post("/files/read")
    async def files_tool_read(request: FileReadRequest, _: bool = Depends(verify_auth)):
        """Read file contents"""
        try:
            with open(request.path, 'r', encoding='utf-8') as f:
                content = f.read()
            return {"content": content, "error": None}
        except Exception as e:
            return {"content": "", "error": str(e)}
    
    @app.post("/files/write")
    async def files_tool_write(request: FileWriteRequest, _: bool = Depends(verify_auth)):
        """Write file contents"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(request.path), exist_ok=True)
            
            with open(request.path, 'w', encoding='utf-8') as f:
                f.write(request.content)
            return {"success": True, "error": None}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @app.post("/v1/tools/files/upload")
    async def upload_file(file: UploadFile = File(...), _: bool = Depends(verify_auth)):
        """Upload and save file"""
        try:
            # Create temporary file
            temp_dir = tempfile.gettempdir()
            file_id = uuid.uuid4().hex
            file_path = os.path.join(temp_dir, f"{file_id}_{file.filename}")
            
            # Save uploaded file
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)
            
            # Get file metadata
            file_size = len(content)
            file_type = file.content_type or "application/octet-stream"
            
            return {
                "file_id": file_id,
                "filename": file.filename,
                "metadata": {
                    "size": file_size,
                    "type": file_type,
                    "path": file_path
                },
                "error": None
            }
        except Exception as e:
            return {
                "file_id": None,
                "filename": None,
                "metadata": None,
                "error": str(e)
            }

    # Computer control tools
    @app.post("/v1/tools/computer/screenshot")
    async def take_screenshot(_: bool = Depends(verify_auth)):
        """Take a screenshot"""
        try:
            result_chunks = []
            for chunk in interpreter.chat("```python\ncomputer.display.screenshot()\n```", stream=True, display=False):
                if chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            
            output = "".join(result_chunks)
            return {"output": output, "error": None}
        except Exception as e:
            return {"output": "", "error": str(e)}

    @app.post("/v1/tools/computer/click")
    async def click_coordinate(request: dict, _: bool = Depends(verify_auth)):
        """Click at coordinates"""
        try:
            x = request.get("x")
            y = request.get("y")
            if x is None or y is None:
                return {"output": "", "error": "x and y coordinates required"}
            
            result_chunks = []
            for chunk in interpreter.chat(f"```python\ncomputer.mouse.click({x}, {y})\n```", stream=True, display=False):
                if chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            
            output = "".join(result_chunks)
            return {"output": output, "error": None}
        except Exception as e:
            return {"output": "", "error": str(e)}

    @app.post("/v1/tools/computer/type")
    async def type_text(request: dict, _: bool = Depends(verify_auth)):
        """Type text"""
        try:
            text = request.get("text", "")
            
            result_chunks = []
            for chunk in interpreter.chat(f"```python\ncomputer.keyboard.write({repr(text)})\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            
            output = "".join(result_chunks)
            return {"output": output, "error": None}
        except Exception as e:
            return {"output": "", "error": str(e)}

    @app.post("/v1/tools/computer/key")
    async def press_key(request: dict, _: bool = Depends(verify_auth)):
        """Press a key or key combination"""
        try:
            key = request.get("key", "")
            
            result_chunks = []
            for chunk in interpreter.chat(f"```python\ncomputer.keyboard.press({repr(key)})\n```", stream=True, display=False):
                if chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            
            output = "".join(result_chunks)
            return {"output": output, "error": None}
        except Exception as e:
            return {"output": "", "error": str(e)}

    # KDE Tools Integration
    class ClipboardSetRequest(BaseModel):
        text: str

    class FileWriteRequestKDE(BaseModel):
        path: str
        content: str

    class FileReadRequestKDE(BaseModel):
        path: str

    class FileAppendRequestKDE(BaseModel):
        path: str
        content: str

    class FileCreateDirectoryRequestKDE(BaseModel):
        path: str

    class FileDeleteRequestKDE(BaseModel):
        path: str

    class FileMoveCopyRequestKDE(BaseModel):
        source_path: str
        destination_path: str

    class NotificationSendRequest(BaseModel):
        summary: str
        body: Optional[str] = ""
        app_name: Optional[str] = ""
        app_icon: Optional[str] = ""
        timeout: Optional[int] = 5000

    class PlasmaEvaluateScriptRequest(BaseModel):
        script: str

    class VirtualDesktopCreateRequest(BaseModel):
        position: int
        name: str

    class VirtualDesktopRemoveRequest(BaseModel):
        desktop_id: str

    class VirtualDesktopSetNameRequest(BaseModel):
        desktop_id: str
        name: str

    class WindowInfoRequest(BaseModel):
        window_id: str

    class WindowSetCurrentDesktopRequest(BaseModel):
        desktop: int

    @app.post("/kde/clipboard/get")
    async def kde_clipboard_get(_: bool = Depends(verify_auth)):
        """Get clipboard contents using KDE tools."""
        try:
            code = "print(computer.kde_clipboard.get_contents())"
            result_chunks = []
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            output = "".join(result_chunks)
            return {"output": output, "error": None}
        except Exception as e:
            return {"output": "", "error": str(e)}

    @app.post("/kde/clipboard/set")
    async def kde_clipboard_set(request: ClipboardSetRequest, _: bool = Depends(verify_auth)):
        """Set clipboard contents using KDE tools."""
        try:
            code = f"computer.kde_clipboard.set_contents({repr(request.text)})"
            result_chunks = []
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            output = "".join(result_chunks)
            return {"output": output, "error": None}
        except Exception as e:
            return {"output": "", "error": str(e)}

    @app.post("/kde/file/write")
    async def kde_file_write(request: FileWriteRequestKDE, _: bool = Depends(verify_auth)):
        """Write content to a file using KDE tools."""
        try:
            code = f"computer.kde_file_operations.write_file_content({repr(request.path)}, {repr(request.content)})"
            result_chunks = []
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            output = "".join(result_chunks)
            return {"output": output, "error": None}
        except Exception as e:
            return {"output": "", "error": str(e)}

    @app.post("/kde/file/read")
    async def kde_file_read(request: FileReadRequestKDE, _: bool = Depends(verify_auth)):
        """Read content from a file using KDE tools."""
        try:
            code = f"print(computer.kde_file_operations.read_file_content({repr(request.path)}))"
            result_chunks = []
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            output = "".join(result_chunks)
            return {"output": output, "error": None}
        except Exception as e:
            return {"output": "", "error": str(e)}

    @app.post("/kde/file/append")
    async def kde_file_append(request: FileAppendRequestKDE, _: bool = Depends(verify_auth)):
        """Append content to a file using KDE tools."""
        try:
            code = f"computer.kde_file_operations.append_file_content({repr(request.path)}, {repr(request.content)})"
            result_chunks = []
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            output = "".join(result_chunks)
            return {"output": output, "error": None}
        except Exception as e:
            return {"output": "", "error": str(e)}

    @app.post("/kde/file/create_directory")
    async def kde_file_create_directory(request: FileCreateDirectoryRequestKDE, _: bool = Depends(verify_auth)):
        """Create a new directory using KDE tools."""
        try:
            code = f"computer.kde_file_operations.create_directory({repr(request.path)})"
            result_chunks = []
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            output = "".join(result_chunks)
            return {"output": output, "error": None}
        except Exception as e:
            return {"output": "", "error": str(e)}

    @app.post("/kde/file/delete_file")
    async def kde_file_delete_file(request: FileDeleteRequestKDE, _: bool = Depends(verify_auth)):
        """Delete a file using KDE tools."""
        try:
            code = f"computer.kde_file_operations.delete_file({repr(request.path)})"
            result_chunks = []
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            output = "".join(result_chunks)
            return {"output": output, "error": None}
        except Exception as e:
            return {"output": "", "error": str(e)}

    @app.post("/kde/file/delete_directory")
    async def kde_file_delete_directory(request: FileDeleteRequestKDE, _: bool = Depends(verify_auth)):
        """Delete a directory using KDE tools."""
        try:
            code = f"computer.kde_file_operations.delete_directory({repr(request.path)})"
            result_chunks = []
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            output = "".join(result_chunks)
            return {"output": output, "error": None}
        except Exception as e:
            return {"output": "", "error": str(e)}

    @app.post("/kde/file/list_directory")
    async def kde_file_list_directory(request: FileReadRequestKDE, _: bool = Depends(verify_auth)):
        """List contents of a directory using KDE tools."""
        try:
            code = f"print(computer.kde_file_operations.list_directory_contents({repr(request.path)}))"
            result_chunks = []
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            output = "".join(result_chunks)
            return {"output": output, "error": None}
        except Exception as e:
            return {"output": "", "error": str(e)}

    @app.post("/kde/file/move")
    async def kde_file_move(request: FileMoveCopyRequestKDE, _: bool = Depends(verify_auth)):
        """Move a file or directory using KDE tools."""
        try:
            code = f"computer.kde_file_operations.move_item({repr(request.source_path)}, {repr(request.destination_path)})"
            result_chunks = []
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            output = "".join(result_chunks)
            return {"output": output, "error": None}
        except Exception as e:
            return {"output": "", "error": str(e)}

    @app.post("/kde/file/copy")
    async def kde_file_copy(request: FileMoveCopyRequestKDE, _: bool = Depends(verify_auth)):
        """Copy a file or directory using KDE tools."""
        try:
            code = f"computer.kde_file_operations.copy_item({repr(request.source_path)}, {repr(request.destination_path)})"
            result_chunks = []
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            output = "".join(result_chunks)
            return {"output": output, "error": None}
        except Exception as e:
            return {"output": "", "error": str(e)}

    @app.post("/kde/notifications/send")
    async def kde_notifications_send(request: NotificationSendRequest, _: bool = Depends(verify_auth)):
        """Send a desktop notification using KDE tools."""
        try:
            code = f"computer.kde_notifications.send_notification(summary={repr(request.summary)}, body={repr(request.body)}, app_name={repr(request.app_name)}, app_icon={repr(request.app_icon)}, timeout={request.timeout})"
            result_chunks = []
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            output = "".join(result_chunks)
            return {"output": output, "error": None}
        except Exception as e:
            return {"output": "", "error": str(e)}

    @app.post("/kde/plasma/evaluate_script")
    async def kde_plasma_evaluate_script(request: PlasmaEvaluateScriptRequest, _: bool = Depends(verify_auth)):
        """Evaluate a JavaScript script in the Plasma Shell using KDE tools."""
        try:
            code = f"print(computer.kde_plasma_shell.evaluate_script({repr(request.script)}))"
            result_chunks = []
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            output = "".join(result_chunks)
            return {"output": output, "error": None}
        except Exception as e:
            return {"output": "", "error": str(e)}

    @app.post("/kde/virtual_desktops/get_count")
    async def kde_virtual_desktops_get_count(_: bool = Depends(verify_auth)):
        """Get the number of virtual desktops using KDE tools."""
        try:
            code = "print(computer.kde_virtual_desktops.get_desktop_count())"
            result_chunks = []
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            output = "".join(result_chunks)
            return {"output": output, "error": None}
        except Exception as e:
            return {"output": "", "error": str(e)}

    @app.post("/kde/virtual_desktops/get_current")
    async def kde_virtual_desktops_get_current(_: bool = Depends(verify_auth)):
        """Get the ID of the current virtual desktop using KDE tools."""
        try:
            code = "print(computer.kde_virtual_desktops.get_current_desktop())"
            result_chunks = []
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            output = "".join(result_chunks)
            return {"output": output, "error": None}
        except Exception as e:
            return {"output": "", "error": str(e)}

    @app.post("/kde/virtual_desktops/create")
    async def kde_virtual_desktops_create(request: VirtualDesktopCreateRequest, _: bool = Depends(verify_auth)):
        """Create a new virtual desktop using KDE tools."""
        try:
            code = f"computer.kde_virtual_desktops.create_desktop(position={request.position}, name={repr(request.name)})"
            result_chunks = []
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            output = "".join(result_chunks)
            return {"output": output, "error": None}
        except Exception as e:
            return {"output": "", "error": str(e)}

    @app.post("/kde/virtual_desktops/remove")
    async def kde_virtual_desktops_remove(request: VirtualDesktopRemoveRequest, _: bool = Depends(verify_auth)):
        """Remove a virtual desktop using KDE tools."""
        try:
            code = f"computer.kde_virtual_desktops.remove_desktop(desktop_id={repr(request.desktop_id)})"
            result_chunks = []
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            output = "".join(result_chunks)
            return {"output": output, "error": None}
        except Exception as e:
            return {"output": "", "error": str(e)}

    @app.post("/kde/virtual_desktops/set_name")
    async def kde_virtual_desktops_set_name(request: VirtualDesktopSetNameRequest, _: bool = Depends(verify_auth)):
        """Set the name of a virtual desktop using KDE tools."""
        try:
            code = f"computer.kde_virtual_desktops.set_desktop_name(desktop_id={repr(request.desktop_id)}, name={repr(request.name)})"
            result_chunks = []
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            output = "".join(result_chunks)
            return {"output": output, "error": None}
        except Exception as e:
            return {"output": "", "error": str(e)}

    @app.post("/kde/windows/get_info")
    async def kde_windows_get_info(request: WindowInfoRequest, _: bool = Depends(verify_auth)):
        """Get information about a specific window using KDE tools."""
        try:
            code = f"print(computer.kde_windows.get_window_info(window_id={repr(request.window_id)}))"
            result_chunks = []
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            output = "".join(result_chunks)
            return {"output": output, "error": None}
        except Exception as e:
            return {"output": "", "error": str(e)}

    @app.post("/kde/windows/query_info")
    async def kde_windows_query_info(_: bool = Depends(verify_auth)):
        """Get information about all windows using KDE tools."""
        try:
            code = "print(computer.kde_windows.query_window_info())"
            result_chunks = []
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            output = "".join(result_chunks)
            return {"output": output, "error": None}
        except Exception as e:
            return {"output": "", "error": str(e)}

    @app.post("/kde/windows/set_current_desktop")
    async def kde_windows_set_current_desktop(request: WindowSetCurrentDesktopRequest, _: bool = Depends(verify_auth)):
        """Switch to the specified virtual desktop using KDE tools."""
        try:
            code = f"computer.kde_windows.set_current_desktop(desktop={request.desktop})"
            result_chunks = []
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            output = "".join(result_chunks)
            return {"output": output, "error": None}
        except Exception as e:
            return {"output": "", "error": str(e)}

    @app.post("/kde/windows/next_desktop")
    async def kde_windows_next_desktop(_: bool = Depends(verify_auth)):
        """Switch to the next virtual desktop using KDE tools."""
        try:
            code = "computer.kde_windows.next_desktop()"
            result_chunks = []
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            output = "".join(result_chunks)
            return {"output": output, "error": None}
        except Exception as e:
            return {"output": "", "error": str(e)}

    @app.post("/kde/windows/previous_desktop")
    async def kde_windows_previous_desktop(_: bool = Depends(verify_auth)):
        """Switch to the previous virtual desktop using KDE tools."""
        try:
            code = "computer.kde_windows.previous_desktop()"
            result_chunks = []
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            output = "".join(result_chunks)
            return {"output": output, "error": None}
        except Exception as e:
            return {"output": "", "error": str(e)}
    
    # Browser Automation Tool Endpoints
    @app.post("/browser/navigate")
    async def browser_navigate(request: BrowserNavigateRequest, _: bool = Depends(verify_auth)):
        """Navigate browser to URL"""
        try:
            saved_messages = interpreter.messages.copy()
            interpreter.messages = []
            result_chunks = []
            
            code = f"""browser.navigate('{request.url}')
print(f"Navigated to: {browser.get_url()}")
print(f"Page title: {browser.get_title()}")"""
            
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            
            interpreter.messages = saved_messages
            output = "".join(result_chunks)
            return {"status": "success", "url": request.url, "output": output}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    @app.post("/browser/click")
    async def browser_click(request: BrowserClickRequest, _: bool = Depends(verify_auth)):
        """Click web element"""
        try:
            saved_messages = interpreter.messages.copy()
            interpreter.messages = []
            result_chunks = []
            
            if request.selector_type == "css":
                code = f"browser.click('{request.selector}')"
            elif request.selector_type == "xpath":
                code = f"browser.click_xpath('{request.selector}')"
            else:
                code = f"browser.click('{request.selector}')"
            
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            
            interpreter.messages = saved_messages
            output = "".join(result_chunks)
            return {"status": "success", "message": "Element clicked", "output": output}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    @app.post("/browser/fill")
    async def browser_fill(request: BrowserFillRequest, _: bool = Depends(verify_auth)):
        """Fill form field"""
        try:
            saved_messages = interpreter.messages.copy()
            interpreter.messages = []
            result_chunks = []
            
            clear_code = f"browser.clear('{request.selector}')" if request.clear_first else ""
            code = f"""{clear_code}
browser.fill('{request.selector}', '''{request.text}''')"""
            
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            
            interpreter.messages = saved_messages
            output = "".join(result_chunks)
            return {"status": "success", "message": "Field filled", "output": output}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    @app.post("/browser/extract")
    async def browser_extract(request: BrowserExtractRequest, _: bool = Depends(verify_auth)):
        """Extract content from page"""
        try:
            saved_messages = interpreter.messages.copy()
            interpreter.messages = []
            result_chunks = []
            
            if request.extract_type == "page_source":
                code = "print(browser.get_page_source())"
            elif request.selector:
                if request.extract_type == "text":
                    code = f"print(browser.get_text('{request.selector}'))"
                elif request.extract_type == "html":
                    code = f"print(browser.get_html('{request.selector}'))"
                elif request.extract_type == "attribute" and request.attribute:
                    code = f"print(browser.get_attribute('{request.selector}', '{request.attribute}'))"
                else:
                    code = f"print(browser.get_text('{request.selector}'))"
            else:
                code = "print(browser.get_page_source())"
            
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            
            interpreter.messages = saved_messages
            content = "".join(result_chunks)
            return {"status": "success", "content": content, "elements_found": 1 if content else 0}
        except Exception as e:
            return {"status": "error", "content": "", "elements_found": 0}
    
    @app.post("/browser/search")
    async def web_search(request: WebSearchRequest, _: bool = Depends(verify_auth)):
        """Perform web search"""
        try:
            saved_messages = interpreter.messages.copy()
            interpreter.messages = []
            result_chunks = []
            
            code = f"""import json
browser.navigate('https://www.google.com/search?q={request.query.replace(' ', '+')}')
results = browser.get_search_results({request.max_results})
print(json.dumps(results))"""
            
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            
            interpreter.messages = saved_messages
            output = "".join(result_chunks)
            
            try:
                results = json.loads(output)
            except:
                results = []
            
            return {"status": "success", "results": results}
        except Exception as e:
            return {"status": "error", "results": []}
    
    @app.post("/browser/screenshot")
    async def browser_screenshot(_: bool = Depends(verify_auth)):
        """Take browser screenshot"""
        try:
            saved_messages = interpreter.messages.copy()
            interpreter.messages = []
            result_chunks = []
            
            code = "screenshot = browser.screenshot()\nprint(screenshot)"
            
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            
            interpreter.messages = saved_messages
            screenshot_data = "".join(result_chunks)
            return {"status": "success", "screenshot": screenshot_data}
        except Exception as e:
            return {"status": "error", "screenshot": ""}
    
    # Clipboard Tool Endpoints
    @app.get("/clipboard/read")
    async def clipboard_read(_: bool = Depends(verify_auth)):
        """Read clipboard content"""
        try:
            saved_messages = interpreter.messages.copy()
            interpreter.messages = []
            result_chunks = []
            
            for chunk in interpreter.chat("```python\nprint(computer.clipboard.view())\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            
            interpreter.messages = saved_messages
            content = "".join(result_chunks)
            return {"status": "success", "content": content}
        except Exception as e:
            return {"status": "error", "content": ""}
    
    @app.post("/clipboard/write")
    async def clipboard_write(request: ClipboardWriteRequest, _: bool = Depends(verify_auth)):
        """Write to clipboard"""
        try:
            saved_messages = interpreter.messages.copy()
            interpreter.messages = []
            result_chunks = []
            
            for chunk in interpreter.chat(f"```python\ncomputer.clipboard.copy({repr(request.text)})\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            
            interpreter.messages = saved_messages
            return {"status": "success", "message": "Text copied to clipboard"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    @app.post("/clipboard/paste")
    async def clipboard_paste(_: bool = Depends(verify_auth)):
        """Paste clipboard content"""
        try:
            saved_messages = interpreter.messages.copy()
            interpreter.messages = []
            result_chunks = []
            
            for chunk in interpreter.chat("```python\ncomputer.clipboard.paste()\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            
            interpreter.messages = saved_messages
            return {"status": "success", "message": "Clipboard content pasted"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    # JavaScript Execution Tool Endpoint
    @app.post("/javascript/execute")
    async def javascript_execute(request: ExecuteCodeRequest, _: bool = Depends(verify_auth)):
        """Execute JavaScript code"""
        try:
            saved_messages = interpreter.messages.copy()
            interpreter.messages = []
            result_chunks = []
            
            for chunk in interpreter.chat(f"```javascript\n{request.code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            
            interpreter.messages = saved_messages
            output = "".join(result_chunks)
            return {"status": "success", "output": output, "error": None}
        except Exception as e:
            return {"status": "error", "output": "", "error": str(e)}
    
    # R Programming Tool Endpoint
    @app.post("/r/execute")
    async def r_execute(request: ExecuteCodeRequest, _: bool = Depends(verify_auth)):
        """Execute R code"""
        try:
            saved_messages = interpreter.messages.copy()
            interpreter.messages = []
            result_chunks = []
            
            for chunk in interpreter.chat(f"```r\n{request.code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            
            interpreter.messages = saved_messages
            output = "".join(result_chunks)
            return {"status": "success", "output": output, "error": None}
        except Exception as e:
            return {"status": "error", "output": "", "error": str(e)}
    
    # AppleScript Tool Endpoint
    @app.post("/applescript/execute")
    async def applescript_execute(request: ExecuteCodeRequest, _: bool = Depends(verify_auth)):
        """Execute AppleScript code"""
        try:
            saved_messages = interpreter.messages.copy()
            interpreter.messages = []
            result_chunks = []
            
            for chunk in interpreter.chat(f"```applescript\n{request.code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            
            interpreter.messages = saved_messages
            output = "".join(result_chunks)
            return {"status": "success", "output": output, "error": None}
        except Exception as e:
            return {"output": "", "error": str(e)}
    
    # SMS/Messages Tool Endpoints
    @app.post("/sms/send")
    async def sms_send(request: SMSSendRequest, _: bool = Depends(verify_auth)):
        """Send SMS/iMessage"""
        try:
            saved_messages = interpreter.messages.copy()
            interpreter.messages = []
            result_chunks = []
            
            code = f"""result = computer.sms.send('{request.to}', '''{request.message}''')
print(result)"""
            
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            
            interpreter.messages = saved_messages
            output = "".join(result_chunks)
            return {"status": "success", "message": output}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    @app.post("/sms/get")
    async def sms_get(request: SMSGetRequest, _: bool = Depends(verify_auth)):
        """Get SMS/iMessage history"""
        try:
            saved_messages = interpreter.messages.copy()
            interpreter.messages = []
            result_chunks = []
            
            contact_param = f"'{request.contact}'" if request.contact else "None"
            substring_param = f"'{request.substring}'" if request.substring else "None"
            
            code = f"""import json
messages = computer.sms.get(contact={contact_param}, limit={request.limit}, substring={substring_param})
print(json.dumps(messages, default=str))"""
            
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            
            interpreter.messages = saved_messages
            output = "".join(result_chunks)
            
            try:
                messages = json.loads(output)
            except:
                messages = []
            
            return {"status": "success", "messages": messages}
        except Exception as e:
            return {"status": "error", "messages": []}
    
    # Vision & OCR Tool Endpoints
    @app.post("/vision/analyze")
    async def vision_analyze(request: VisionAnalyzeRequest, _: bool = Depends(verify_auth)):
        """Analyze image with AI"""
        try:
            saved_messages = interpreter.messages.copy()
            interpreter.messages = []
            result_chunks = []
            
            if request.image_path:
                code = f"""result = computer.vision.analyze('{request.image_path}', '{request.prompt}')
print(result)"""
            elif request.image_base64:
                code = f"""import base64
result = computer.vision.analyze_base64('{request.image_base64}', '{request.prompt}')
print(result)"""
            else:
                return {"status": "error", "analysis": "No image provided"}
            
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            
            interpreter.messages = saved_messages
            analysis = "".join(result_chunks)
            return {"status": "success", "analysis": analysis}
        except Exception as e:
            return {"status": "error", "analysis": str(e)}
    
    @app.post("/vision/ocr")
    async def vision_ocr(request: VisionOCRRequest, _: bool = Depends(verify_auth)):
        """Extract text from image"""
        try:
            saved_messages = interpreter.messages.copy()
            interpreter.messages = []
            result_chunks = []
            
            if request.image_path:
                code = f"""result = computer.vision.ocr('{request.image_path}')
print(result)"""
            elif request.image_base64:
                code = f"""import base64
result = computer.vision.ocr_base64('{request.image_base64}')
print(result)"""
            else:
                return {"status": "error", "text": "No image provided"}
            
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            
            interpreter.messages = saved_messages
            text = "".join(result_chunks)
            return {"status": "success", "text": text}
        except Exception as e:
            return {"status": "error", "text": str(e)}
    
    @app.post("/vision/screenshot_analyze")
    async def vision_screenshot_analyze(request: VisionScreenshotAnalyzeRequest, _: bool = Depends(verify_auth)):
        """Take screenshot and analyze"""
        try:
            saved_messages = interpreter.messages.copy()
            interpreter.messages = []
            result_chunks = []
            
            code = f"""import base64
screenshot = computer.display.screenshot()
analysis = computer.vision.analyze_screenshot('{request.prompt}')
print(f"screenshot:{screenshot}")
print(f"analysis:{analysis}")"""
            
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            
            interpreter.messages = saved_messages
            output = "".join(result_chunks)
            
            # Parse screenshot and analysis from output
            screenshot = ""
            analysis = ""
            for line in output.split("\n"):
                if line.startswith("screenshot:"):
                    screenshot = line[11:]
                elif line.startswith("analysis:"):
                    analysis = line[9:]
            
            return {"status": "success", "screenshot": screenshot, "analysis": analysis}
        except Exception as e:
            return {"status": "error", "screenshot": "", "analysis": str(e)}

    # Memory Management Endpoints
    class StructuredMemorySaveRequest(BaseModel):
        key: str
        value: str

    class StructuredMemoryGetRequest(BaseModel):
        key: str

    class SemanticMemoryAddRequest(BaseModel):
        text_chunk: str
        embedding: List[float]

    class SemanticMemorySearchRequest(BaseModel):
        query_embedding: List[float]
        top_k: int = 5

    @app.post("/memory/structured/save")
    async def save_structured_memory(request: StructuredMemorySaveRequest, _: bool = Depends(verify_auth)):
        """Save structured memory."""
        try:
            code = f"interpreter.memory.save_structured_memory(key={repr(request.key)}, value={repr(request.value)})"
            result_chunks = []
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            output = "".join(result_chunks)
            return {"output": output, "error": None}
        except Exception as e:
            return {"output": "", "error": str(e)}

    @app.post("/memory/structured/get")
    async def get_structured_memory(request: StructuredMemoryGetRequest, _: bool = Depends(verify_auth)):
        """Get structured memory."""
        try:
            code = f"print(interpreter.memory.get_structured_memory(key={repr(request.key)}))"
            result_chunks = []
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            output = "".join(result_chunks)
            return {"output": output, "error": None}
        except Exception as e:
            return {"output": "", "error": str(e)}

    @app.post("/memory/semantic/add")
    async def add_semantic_memory(request: SemanticMemoryAddRequest, _: bool = Depends(verify_auth)):
        """Add semantic memory."""
        try:
            code = f"interpreter.memory.add_semantic_memory(text_chunk={repr(request.text_chunk)}, embedding={request.embedding})"
            result_chunks = []
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            output = "".join(result_chunks)
            return {"output": output, "error": None}
        except Exception as e:
            return {"output": "", "error": str(e)}

    @app.post("/memory/semantic/search")
    async def search_semantic_memory(request: SemanticMemorySearchRequest, _: bool = Depends(verify_auth)):
        """Search semantic memory."""
        try:
            code = f"print(interpreter.memory.search_semantic_memory(query_embedding={request.query_embedding}, top_k={request.top_k}))"
            result_chunks = []
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            output = "".join(result_chunks)
            return {"output": output, "error": None}
        except Exception as e:
            return {"output": "", "error": str(e)}

    # File Indexing Endpoints
    class FileIndexDirectoryRequest(BaseModel):
        directory_path: str
        extensions: Optional[List[str]] = None

    class FileIndexSearchRequest(BaseModel):
        query: str
        top_k: int = 5

    @app.post("/file_indexing/index_directory")
    async def index_directory(request: FileIndexDirectoryRequest, _: bool = Depends(verify_auth)):
        """Index a directory for file content search."""
        try:
            extensions_str = f", extensions={request.extensions}" if request.extensions else ""
            code = f"interpreter.file_indexer.index_directory(directory_path={repr(request.directory_path)}{extensions_str})"
            result_chunks = []
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            output = "".join(result_chunks)
            return {"output": output, "error": None}
        except Exception as e:
            return {"output": "", "error": str(e)}

    @app.post("/file_indexing/search_indexed_files")
    async def search_indexed_files(request: FileIndexSearchRequest, _: bool = Depends(verify_auth)):
        """Search indexed files semantically."""
        try:
            code = f"print(interpreter.file_indexer.search_indexed_files(query={repr(request.query)}, top_k={request.top_k}))"
            result_chunks = []
            for chunk in interpreter.chat(f"```python\n{code}\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            output = "".join(result_chunks)
            return {"output": output, "error": None}
        except Exception as e:
            return {"output": "", "error": str(e)}

    return app
