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

from .utils.lazy_import import lazy_import

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


def create_openwebui_server(interpreter, host="localhost", port=8264, auth_token=None):
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
        """File Reader - Read file contents"""
        try:
            with open(request.path, 'r', encoding='utf-8') as f:
                content = f.read()
            return {"content": content, "error": None}
        except Exception as e:
            return {"content": "", "error": str(e)}
    
    @app.post("/files/write")
    async def files_tool_write(request: FileWriteRequest, _: bool = Depends(verify_auth)):
        """File Writer - Write file contents"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(request.path), exist_ok=True)
            
            with open(request.path, 'w', encoding='utf-8') as f:
                f.write(request.content)
            return {"success": True, "error": None}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @app.post("/computer/screenshot")
    async def computer_tool_screenshot(_: bool = Depends(verify_auth)):
        """Screenshot Capture - Take a screenshot"""
        try:
            result_chunks = []
            for chunk in interpreter.chat("```python\ncomputer.display.screenshot()\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            
            output = "".join(result_chunks)
            return {"output": output, "error": None}
        except Exception as e:
            return {"output": "", "error": str(e)}
    
    @app.post("/computer/click")
    async def computer_tool_click(request: dict, _: bool = Depends(verify_auth)):
        """Mouse Click - Click at coordinates"""
        try:
            x = request.get("x")
            y = request.get("y")
            if x is None or y is None:
                return {"output": "", "error": "x and y coordinates required"}
            
            result_chunks = []
            for chunk in interpreter.chat(f"```python\ncomputer.mouse.click({x}, {y})\n```", stream=True, display=False):
                if isinstance(chunk, dict) and chunk.get("type") == "console" and "content" in chunk:
                    result_chunks.append(chunk["content"])
            
            output = "".join(result_chunks)
            return {"output": output, "error": None}
        except Exception as e:
            return {"output": "", "error": str(e)}
    
    @app.post("/computer/type")
    async def computer_tool_type(request: dict, _: bool = Depends(verify_auth)):
        """Keyboard Input - Type text"""
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
    
    @app.get("/v1/models")
    async def list_models():
        """List available models - required for Open WebUI"""
        return {
            "object": "list",
            "data": [
                {
                    "id": "the-colonel",
                    "object": "model",
                    "created": int(time.time()),
                    "owned_by": "the-colonel",
                    "permission": [],
                    "root": "the-colonel",
                    "parent": None
                }
            ]
        }
    
    @app.post("/v1/chat/completions")
    async def create_chat_completion(
        request: ChatCompletionRequest,
        profile: Optional[str] = Query(None),
        _: bool = Depends(verify_auth)
    ):
        """OpenAI-compatible chat completion endpoint"""
        
        # Load profile if specified
        if profile:
            load_profile(profile)
        
        # Convert messages to interpreter format and filter system messages
        messages = []
        system_message = None
        
        for msg in request.messages:
            if msg.role == "system":
                # Only keep the first system message, merge others into custom instructions
                if system_message is None:
                    system_message = msg.content
                else:
                    # Append additional system messages to custom instructions
                    if hasattr(interpreter, 'custom_instructions'):
                        interpreter.custom_instructions = (interpreter.custom_instructions or "") + "\n" + msg.content
                    else:
                        interpreter.custom_instructions = msg.content
            else:
                messages.append({
                    "role": msg.role,
                    "type": "message",  # Ensure all messages have a type
                    "content": msg.content
                })
        
        # Set system message if we found one
        if system_message:
            interpreter.system_message = system_message
        
        # Clear previous messages and set new ones
        interpreter.messages = []
        if len(messages) > 1:
            # Set conversation history (all but the last message)
            interpreter.messages = messages[:-1]
        
        # Get the last message to process
        last_message = messages[-1]["content"] if messages else ""
        
        completion_id = f"chatcmpl-{uuid.uuid4().hex}"
        created = int(time.time())
        
        if request.stream:
            # Streaming response
            async def generate():
                yield f"data: {json.dumps({'id': completion_id, 'object': 'chat.completion.chunk', 'created': created, 'model': request.model, 'choices': [{'index': 0, 'delta': {'role': 'assistant'}, 'finish_reason': None}]})}\n\n"
                
                content_buffer = ""
                try:
                    conversation_ended = False
                    in_code_block = False
                    in_console_block = False
                    
                    for chunk in interpreter.chat(last_message, stream=True, display=False):
                        # Robust chunk processing to handle various formats
                        try:
                            # Debug logging
                            print(f"🔍 Processing chunk: {type(chunk)} - {chunk}")
                            
                            # Handle different chunk types that can come from the interpreter
                            if isinstance(chunk, dict):
                                # Get chunk type safely, handle missing type field
                                chunk_type = chunk.get("type", "unknown")
                                chunk_role = chunk.get("role", "")
                                chunk_content = chunk.get("content", "")
                                
                                # Handle message chunks - primary text content
                                if chunk_type == "message" and chunk_role == "assistant":
                                    if chunk_content:
                                        content_buffer += chunk_content
                                        delta_data = {
                                            'id': completion_id,
                                            'object': 'chat.completion.chunk',
                                            'created': created,
                                            'model': request.model,
                                            'choices': [{
                                                'index': 0,
                                                'delta': {'content': chunk_content},
                                                'finish_reason': None
                                            }]
                                        }
                                        yield f"data: {json.dumps(delta_data)}\n\n"
                                    
                                    # Check for conversation end
                                    if chunk.get("end"):
                                        conversation_ended = True
                                        break
                                
                                # Handle code blocks
                                elif chunk_type == "code":
                                    if chunk.get("start"):
                                        in_code_block = True
                                        code_format = chunk.get("format", "python")
                                        delta_data = {
                                            'id': completion_id,
                                            'object': 'chat.completion.chunk',
                                            'created': created,
                                            'model': request.model,
                                            'choices': [{
                                                'index': 0,
                                                'delta': {'content': f"\n```{code_format}\n"},
                                                'finish_reason': None
                                            }]
                                        }
                                        yield f"data: {json.dumps(delta_data)}\n\n"
                                    elif chunk_content and in_code_block:
                                        delta_data = {
                                            'id': completion_id,
                                            'object': 'chat.completion.chunk',
                                            'created': created,
                                            'model': request.model,
                                            'choices': [{
                                                'index': 0,
                                                'delta': {'content': chunk_content},
                                                'finish_reason': None
                                            }]
                                        }
                                        yield f"data: {json.dumps(delta_data)}\n\n"
                                    elif chunk.get("end") and in_code_block:
                                        in_code_block = False
                                        delta_data = {
                                            'id': completion_id,
                                            'object': 'chat.completion.chunk',
                                            'created': created,
                                            'model': request.model,
                                            'choices': [{
                                                'index': 0,
                                                'delta': {'content': "\n```\n"},
                                                'finish_reason': None
                                            }]
                                        }
                                        yield f"data: {json.dumps(delta_data)}\n\n"
                                
                                # Handle console output
                                elif chunk_type == "console":
                                    if chunk.get("start"):
                                        in_console_block = True
                                        delta_data = {
                                            'id': completion_id,
                                            'object': 'chat.completion.chunk',
                                            'created': created,
                                            'model': request.model,
                                            'choices': [{
                                                'index': 0,
                                                'delta': {'content': "\nOutput:\n```\n"},
                                                'finish_reason': None
                                            }]
                                        }
                                        yield f"data: {json.dumps(delta_data)}\n\n"
                                    elif chunk_content and in_console_block:
                                        delta_data = {
                                            'id': completion_id,
                                            'object': 'chat.completion.chunk',
                                            'created': created,
                                            'model': request.model,
                                            'choices': [{
                                                'index': 0,
                                                'delta': {'content': str(chunk_content)},
                                                'finish_reason': None
                                            }]
                                        }
                                        yield f"data: {json.dumps(delta_data)}\n\n"
                                    elif chunk.get("end") and in_console_block:
                                        in_console_block = False
                                        delta_data = {
                                            'id': completion_id,
                                            'object': 'chat.completion.chunk',
                                            'created': created,
                                            'model': request.model,
                                            'choices': [{
                                                'index': 0,
                                                'delta': {'content': "\n```\n"},
                                                'finish_reason': None
                                            }]
                                        }
                                        yield f"data: {json.dumps(delta_data)}\n\n"
                                
                                # Handle chunks that might not have a type but have content
                                elif chunk_type == "unknown" and chunk_content:
                                    # This handles edge cases where chunks come without proper type
                                    if chunk_role == "assistant" or not chunk_role:
                                        delta_data = {
                                            'id': completion_id,
                                            'object': 'chat.completion.chunk',
                                            'created': created,
                                            'model': request.model,
                                            'choices': [{
                                                'index': 0,
                                                'delta': {'content': chunk_content},
                                                'finish_reason': None
                                            }]
                                        }
                                        yield f"data: {json.dumps(delta_data)}\n\n"
                                
                                # Skip chunks we don't recognize but log them
                                elif chunk_type not in ["message", "code", "console", "confirmation", "active_line", "unknown"]:
                                    print(f"⚠️ Unknown chunk type '{chunk_type}': {chunk}")
                            
                            elif isinstance(chunk, str):
                                # Handle plain string chunks
                                if chunk.strip():
                                    delta_data = {
                                        'id': completion_id,
                                        'object': 'chat.completion.chunk',
                                        'created': created,
                                        'model': request.model,
                                        'choices': [{
                                            'index': 0,
                                            'delta': {'content': chunk},
                                            'finish_reason': None
                                        }]
                                    }
                                    yield f"data: {json.dumps(delta_data)}\n\n"
                            
                            else:
                                # Handle any other unexpected types
                                print(f"⚠️ Unexpected chunk format: {type(chunk)} - {chunk}")
                        
                        except Exception as chunk_error:
                            print(f"⚠️ Error processing chunk: {chunk_error}")
                            print(f"   Problematic chunk: {chunk}")
                            # Continue processing other chunks
                    
                    # Always send final chunk to end the stream properly
                    if not conversation_ended:
                        final_data = {
                            'id': completion_id,
                            'object': 'chat.completion.chunk',
                            'created': created,
                            'model': request.model,
                            'choices': [{
                                'index': 0,
                                'delta': {},
                                'finish_reason': 'stop'
                            }]
                        }
                        yield f"data: {json.dumps(final_data)}\n\n"
                except Exception as e:
                    error_data = {
                        'id': completion_id,
                        'object': 'chat.completion.chunk',
                        'created': created,
                        'model': request.model,
                        'choices': [{
                            'index': 0,
                            'delta': {'content': f"\n\nError: {str(e)}"},
                            'finish_reason': 'error'
                        }]
                    }
                    yield f"data: {json.dumps(error_data)}\n\n"
                
                yield "data: [DONE]\n\n"
            
            return StreamingResponse(generate(), media_type="text/event-stream")
        
        else:
            # Non-streaming response
            try:
                full_response = ""
                for chunk in interpreter.chat(last_message, stream=True, display=False):
                    try:
                        # Debug logging
                        print(f"🔍 Non-streaming chunk: {type(chunk)} - {chunk}")
                        
                        if isinstance(chunk, dict):
                            chunk_type = chunk.get("type", "unknown")
                            chunk_role = chunk.get("role", "")
                            chunk_content = chunk.get("content", "")
                            
                            if chunk_type == "message" and chunk_role == "assistant" and chunk_content:
                                full_response += chunk_content
                            elif chunk_type == "code" and chunk_content:
                                code_format = chunk.get('format', 'python')
                                full_response += f"\n```{code_format}\n{chunk_content}\n```\n"
                            elif chunk_type == "console" and chunk_content:
                                full_response += f"\nOutput:\n```\n{chunk_content}\n```\n"
                            elif chunk_type == "unknown" and chunk_content:
                                # Handle chunks without type but with content
                                if chunk_role == "assistant" or not chunk_role:
                                    full_response += chunk_content
                        
                        elif isinstance(chunk, str):
                            full_response += chunk
                    
                    except Exception as chunk_error:
                        print(f"⚠️ Error processing non-streaming chunk: {chunk_error}")
                        continue
                
                response = ChatCompletionResponse(
                    id=completion_id,
                    object="chat.completion",
                    created=created,
                    model=request.model,
                    choices=[{
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": full_response
                        },
                        "finish_reason": "stop"
                    }]
                )
                return response
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/v1/tools/execute/python")
    async def execute_python(request: ExecuteCodeRequest, _: bool = Depends(verify_auth)):
        """Execute Python code"""
        try:
            # Use interpreter's Python execution capability
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
    
    @app.post("/v1/tools/execute/shell")
    async def execute_shell(request: ExecuteShellRequest, _: bool = Depends(verify_auth)):
        """Execute shell command"""
        try:
            # Use interpreter's shell execution capability
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
    
    @app.post("/v1/tools/files/read")
    async def read_file(request: FileReadRequest, _: bool = Depends(verify_auth)):
        """Read file contents"""
        try:
            with open(request.path, 'r', encoding='utf-8') as f:
                content = f.read()
            return {"content": content, "error": None}
        except Exception as e:
            return {"content": "", "error": str(e)}
    
    @app.post("/v1/tools/files/write")
    async def write_file(request: FileWriteRequest, _: bool = Depends(verify_auth)):
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
                if chunk.get("type") == "console" and "content" in chunk:
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
    
    # Browser Automation Tool Endpoints
    @app.post("/browser/navigate")
    async def browser_navigate(request: BrowserNavigateRequest, _: bool = Depends(verify_auth)):
        """Navigate browser to URL"""
        try:
            saved_messages = interpreter.messages.copy()
            interpreter.messages = []
            result_chunks = []
            
            code = f"""browser.navigate('{request.url}')
print(f"Navigated to: {{browser.get_url()}}")
print(f"Page title: {{browser.get_title()}}")"""
            
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
            return {"status": "error", "output": "", "error": str(e)}
    
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
    
    return app


def server(interpreter, host=None, port=None, auth_token=None, profile_name=None):
    """Start the Open WebUI compatible server"""
    # Use environment variables for defaults if not provided
    host = host or os.getenv("SERVER_HOST", "localhost")
    port = port or int(os.getenv("SERVER_PORT", 8264))
    auth_token = auth_token or os.getenv("AUTH_TOKEN")
    profile_name = profile_name or os.getenv("DEFAULT_PROFILE", "gpt-4.1-mini.py")
    
    app = create_openwebui_server(interpreter, host, port, auth_token)
    
    # Load the specified profile  
    try:
        from interpreter.terminal_interface.profiles.profiles import profile
        profile(interpreter, profile_name)
        print(f"🎯 Loaded profile: {profile_name}")
    except Exception as e:
        print(f"⚠️  Warning: Could not load profile {profile_name}: {e}")
        # Fallback to default profile
        try:
            profile(interpreter, "fast.yaml")
            print(f"🎯 Fallback: Loaded fast.yaml profile")
        except Exception as e2:
            print(f"⚠️  Warning: Could not load fallback profile: {e2}")
    
    print(f"\n🚀 The_Colonel Open WebUI Server starting...")
    print(f"📡 Chat endpoint: http://{host}:{port}/v1/chat/completions")
    print(f"🔧 Tools endpoint: http://{host}:{port}/v1/tools/*")
    print(f"📋 OpenAPI spec: http://{host}:{port}/openapi.json")
    
    if auth_token:
        print(f"🔐 Authentication: Bearer {auth_token}")
    else:
        print("🔓 Authentication: Disabled (localhost only)")
    
    print(f"\n📖 Open WebUI Configuration:")
    print(f"   LLM Base URL: http://{host}:{port}/v1")
    print(f"   Tool Server URL: http://{host}:{port}")
    print()
    
    uvicorn.run(app, host=host, port=port)