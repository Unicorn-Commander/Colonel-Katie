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


def create_openwebui_server(interpreter, host="localhost", port=8264, auth_token=None):
    """Create FastAPI server for Open WebUI integration"""
    
    app = FastAPI(
        title="The_Colonel API",
        description="API for The_Colonel as a chat endpoint and tool server in Open WebUI",
        version="0.1.0"
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
        """Serve OpenAPI specification"""
        openapi_path = Path(__file__).parent.parent.parent / "openapi.json"
        if openapi_path.exists():
            return FileResponse(openapi_path, media_type="application/json")
        else:
            raise HTTPException(status_code=404, detail="OpenAPI specification not found")
    
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