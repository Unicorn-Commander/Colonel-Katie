Below is the plan and the complete openapi.json in a markdown format that you can easily copy and paste into a file on your computer (e.g., unicorn-interpreter-plan.md). The markdown includes the implementation steps and the OpenAPI specification, formatted for clarity and easy use.
markdown
# The_Colonel Integration Plan for Open WebUI

This plan outlines how to integrate your The_Colonel fork (https://github.com/Unicorn-Commander/The_Colonel) with Open WebUI as both a chat endpoint and a tool server, using a single OpenAPI specification. The server will run on port 8264, support profile selection for chat, and expose tools as individual endpoints, with optional authentication for remote access.

## Final Plan

- **Single OpenAPI Specification**: One `openapi.json` with:
  - Chat endpoint at `/v1/chat/completions` for Open WebUI’s model settings, supporting profile selection via a query parameter (`?profile=profile_name`).
  - Tool endpoints under `/v1/tools/*` (e.g., `/v1/tools/execute/python`, `/v1/tools/files/read`) for Open WebUI’s “Tools” settings, exposed as individual tools.
- **Port**: Use 8264 to avoid conflicts with common ports like 8000.
- **Access**:
  - `localhost:8264` without authentication for local use.
  - `0.0.0.0:8264` with optional Bearer Token authentication for remote access.
- **Open WebUI Setup**:
  - LLM connection: `http://localhost:8264/v1` for chat.
  - Tool server: `http://localhost:8264` with the `openapi.json`.

## Steps to Implement

1. **Update OpenAPI JSON**:
   - Save the `openapi.json` below to your The_Colonel project (e.g., `The_Colonel/openapi.json`).
   - Host it at `http://localhost:8264/openapi.json` when the server runs.

2. **Modify Server Implementation**:
   - Ensure your FastAPI-based server implements the new endpoints (`/v1/chat/completions`, `/v1/tools/*`).
   - Add profile selection logic for `/v1/chat/completions` using the `profile` query parameter, loading profiles from the `profiles` folder.
   - Implement optional authentication (disabled for `localhost`, enabled for `0.0.0.0`).

3. **Run the Server**:
   - **Localhost**: `interpreter --server --host localhost --port 8264 --no-auth`
   - **Remote**: `interpreter --server --host 0.0.0.0 --port 8264 --auth`

4. **Configure Open WebUI**:
   - **LLM Connection**: In model settings, set the API base URL to `http://localhost:8264/v1`.
   - **Tool Server**: In user settings under “Tools,” add `http://localhost:8264` with the `openapi.json`.

5. **Test**:
   - Verify chat interactions via Open WebUI’s chat interface (e.g., select a profile and send prompts).
   - Check that tools (e.g., “Execute Python Code,” “Read File”) appear in Open WebUI’s tool settings and work when invoked.

## Complete OpenAPI JSON

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "The_Colonel API",
    "description": "API for The_Colonel as a chat endpoint and tool server in Open WebUI",
    "version": "0.1.0"
  },
  "servers": [
    {
      "url": "http://localhost:8264",
      "description": "Local server (no authentication required)"
    },
    {
      "url": "http://0.0.0.0:8264",
      "description": "Remote server (authentication recommended)"
    }
  ],
  "paths": {
    "/v1/chat/completions": {
      "post": {
        "summary": "Create Chat Completion",
        "description": "OpenAI-compatible chat endpoint with profile selection for Open WebUI",
        "operationId": "create_chat_completion",
        "parameters": [
          {
            "name": "profile",
            "in": "query",
            "description": "Profile name from the profiles folder (defaults to default profile)",
            "required": false,
            "schema": {
              "type": "string"
            }
          }
        ],
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/ChatCompletionRequest"
              }
            }
          },
          "required": true
        },
        "responses": {
          "200": {
            "description": "Successful chat completion",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ChatCompletionResponse"
                }
              },
              "text/event-stream": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "choices": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "delta": {
                            "type": "object",
                            "properties": {
                              "content": {
                                "type": "string",
                                "nullable": true
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          },
          "422": {
            "description": "Validation error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        },
        "security": [
          {
            "BearerAuth": []
          },
          {}
        ]
      }
    },
    "/v1/tools/execute/python": {
      "post": {
        "summary": "Execute Python Code",
        "description": "Execute Python code locally and return the output",
        "operationId": "execute_python",
        "request': {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "code": {
                    "type": "string",
                    "description": "Python code to execute"
                  }
                },
                "required": ["code"]
              }
            }
          },
          "required": true
        },
        "responses": {
          "200": {
            "description": "Execution result",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "output": {
                      "type": "string",
                      "description": "Execution output"
                    },
                    "error": {
                      "type": "string",
                      "nullable": true,
                      "description": "Error message, if any"
                    }
                  }
                }
              }
            }
          },
          "422": {
            "description": "Validation error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        },
        "security": [
          {
            "BearerAuth": []
          },
          {}
        ]
      }
    },
    "/v1/tools/execute/shell": {
      "post": {
        "summary": "Execute Shell Command",
        "description": "Execute a shell command locally and return the output",
        "operationId": "execute_shell",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "command": {
                    "type": "string",
                    "description": "Shell command to execute"
                  }
                },
                "required": ["command"]
              }
            }
          },
          "required": true
        },
        "responses": {
          "200": {
            "description": "Execution result",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "output": {
                      "type": "string",
                      "description": "Command output"
                    },
                    "error": {
                      "type": "string",
                      "nullable": true,
                      "description": "Error message, if any"
                    }
                  }
                }
              }
            }
          },
          "422": {
            "description": "Validation error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        },
        "security": [
          {
            "BearerAuth": []
          },
          {}
        ]
      }
    },
    "/v1/tools/files/read": {
      "post": {
        "summary": "Read File",
        "description": "Read the contents of a file at the specified path",
        "operationId": "read_file",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "path": {
                    "type": "string",
                    "description": "File path to read"
                  }
                },
                "required": ["path"]
              }
            }
          },
          "required": true
        },
        "responses": {
          "200": {
            "description": "File contents",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "content": {
                      "type": "string",
                      "description": "File contents"
                    },
                    "error": {
                      "type": "string",
                      "nullable": true,
                      "description": "Error message, if any"
                    }
                  }
                }
              }
            }
          },
          "422": {
            "description": "Validation error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        },
        "security": [
          {
            "BearerAuth": []
          },
          {}
        ]
      }
    },
    "/v1/tools/files/write": {
      "post": {
        "summary": "Write File",
        "description": "Write content to a file at the specified path",
        "operationId": "write_file",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
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
            }
          },
          "required": true
        },
        "responses": {
          "200": {
            "description": "Write result",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "success": {
                      "type": "boolean",
                      "description": "Whether the write was successful"
                    },
                    "error": {
                      "type": "string",
                      "nullable": true,
                      "description": "Error message, if any"
                    }
                  }
                }
              }
            }
          },
          "422": {
            "description": "Validation error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        },
        "security": [
          {
            "BearerAuth": []
          },
          {}
        ]
      }
    },
    "/v1/tools/files/upload": {
      "post": {
        "summary": "Upload File",
        "description": "Upload a file and return its metadata",
        "operationId": "upload_file",
        "requestBody": {
          "content": {
            "multipart/form-data": {
              "schema": {
                "type": "object",
                "properties": {
                  "file": {
                    "type": "string",
                    "format": "binary",
                    "description": "File to upload"
                  }
                },
                "required": ["file"]
              }
            }
          },
          "required": true
        },
        "responses": {
          "200": {
            "description": "File upload result",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "file_id": {
                      "type": "string",
                      "description": "Unique identifier for the uploaded file"
                    },
                    "filename": {
                      "type": "string",
                      "description": "Name of the uploaded file"
                    },
                    "metadata": {
                      "type": "object",
                      "description": "File metadata (e.g., size, type)"
                    },
                    "error": {
                      "type": "string",
                      "nullable": true,
                      "description": "Error message, if any"
                    }
                  }
                }
              }
            }
          },
          "422": {
            "description": "Validation error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        },
        "security": [
          {
            "BearerAuth": []
          },
          {}
        ]
      }
    }
  },
  "components": {
    "schemas": {
      "ChatCompletionRequest": {
        "type": "object",
        "properties": {
          "model": {
            "type": "string",
            "default": "unicorn-interpreter",
            "description": "Model identifier"
          },
          "messages": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/ChatMessage"
            },
            "description": "List of messages in the conversation"
          },
          "max_tokens": {
            "type": "integer",
            "nullable": true,
            "description": "Maximum tokens to generate"
          },
          "temperature": {
            "type": "number",
            "nullable": true,
            "description": "Sampling temperature"
          },
          "stream": {
            "type": "boolean",
            "default": false,
            "description": "Whether to stream the response"
          }
        },
        "required": ["messages"]
      },
      "ChatMessage": {
        "type": "object",
        "properties": {
          "role": {
            "type": "string",
            "enum": ["user", "assistant", "system"],
            "description": "Role of the message sender"
          },
          "content": {
            "type": "string",
            "description": "Message content"
          }
        },
        "required": ["role", "content"]
      },
      "ChatCompletionResponse": {
        "type": "object",
        "properties": {
          "id": {
            "type": "string",
            "description": "Unique identifier for the completion"
          },
          "object": {
            "type": "string",
            "enum": ["chat.completion"],
            "description": "Object type"
          },
          "created": {
            "type": "integer",
            "description": "Timestamp of creation"
          },
          "model": {
            "type": "string",
            "description": "Model used"
          },
          "choices": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "message": {
                  "$ref": "#/components/schemas/ChatMessage"
                },
                "index": {
                  "type": "integer",
                  "description": "Index of the choice"
                },
                "finish_reason": {
                  "type": "string",
                  "enum": ["stop", "length", "error"],
                  "description": "Reason for completion end"
                }
              }
            },
            "description": "List of completion choices"
          }
        },
        "required": ["id", "object", "created", "model", "choices"]
      },
      "HTTPValidationError": {
        "type": "object",
        "properties": {
          "detail": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/ValidationError"
            },
            "description": "List of validation errors"
          }
        }
      },
      "ValidationError": {
        "type": "object",
        "properties": {
          "loc": {
            "type": "array",
            "items": {
              "type": "string"
            },
            "description": "Location of the error"
          },
          "msg": {
            "type": "string",
            "description": "Error message"
          },
          "type": {
            "type": "string",
            "description": "Error type"
          }
        },
        "required": ["loc", "msg", "type"]
      }
    },
    "securitySchemes": {
      "BearerAuth": {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
        "description": "Bearer token for authentication (optional for localhost, required for 0.0.0.0)"
      }
    }
  }
}
Implementation Notes
Profile Selection: The /v1/chat/completions endpoint uses a profile query parameter (e.g., ?profile=my_profile). The server should load profiles from the profiles folder (e.g., The_Colonel/profiles/) and use a default profile if none is specified.
Tool Endpoints: Includes endpoints for Python execution, shell commands, file read/write, and file upload, based on interpreter/computer_use/tools. Add more endpoints if your fork includes additional tools.
Authentication: The security: [{"BearerAuth": []}, {}] syntax makes authentication optional, allowing localhost to skip it while enforcing it for 0.0.0.0.
Server Code: Update the FastAPI server to handle these endpoints and profile logic.
Open WebUI Configuration
LLM Connection:
Base URL: http://localhost:8264/v1
This points to /v1/chat/completions for chat interactions.
Optionally specify a profile in the prompt or via a custom header if needed.
Tool Server:
In “Tools” settings, add:
Base URL: http://localhost:8264
OpenAPI JSON: Upload the JSON above or point to http://localhost:8264/openapi.json.
Tools like “Execute Python Code,” “Execute Shell Command,” etc., will appear for selection.
Testing
Chat: In Open WebUI, send a prompt like “Hello, using profile=my_profile” and verify the response uses the correct profile.
Tools: Test tools via Open WebUI’s interface (e.g., “Run this Python code: print('Test')” or “Read file.txt”). Ensure each tool appears separately in the tool settings.
Remote Access: Run on 0.0.0.0:8264 with auth and test with a Bearer Token.
Next Steps
Save openapi.json: Place it in your project and ensure the server serves it at /openapi.json.
Update Server: Modify your server code to implement the new endpoints and profile logic.
Need Code?: Request example FastAPI code or help with specific tool logic.
Troubleshooting: Share details of any issues (e.g., profile loading, tool execution) for assistance.

---

### How to Use
1. **Copy the Markdown**:
   - Copy the entire markdown content above.
   - Paste it into a file named `unicorn-interpreter-plan.md` on your computer using a text editor (e.g., VS Code, Notepad, or any code editor).

2. **Extract `openapi.json`**:
   - To create the `openapi.json` file, copy the JSON content from the “Complete OpenAPI JSON” section.
   - Save it as `openapi.json` in your `The_Colonel` project directory.

3. **Follow the Steps**:
   - Use the implementation steps to update your server and configure Open WebUI.
   - Run the server with the specified commands for `localhost` or `0.0.0.0`.

If you need help with the server code implementation (e.g., FastAPI endpoints) or run into issues, let me know, and I’ll provide further assistance! 🦄💪