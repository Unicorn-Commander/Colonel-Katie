# Project Summary: Unicorn-Interpreter Integration with Open WebUI

## Intent
The goal is to integrate the Unicorn-Interpreter fork (https://github.com/Unicorn-Commander/Unicorn-Interpreter), a modified version of Open Interpreter, with Open WebUI to provide a seamless interface for conversational interactions and tool execution. This enables users to interact with Unicorn-Interpreter’s capabilities (e.g., code execution, file operations) through Open WebUI’s UI, replicating the terminal experience while leveraging Open WebUI’s model and tool server integrations.

## Objectives
- **Chat Endpoint**: Provide an OpenAI-compatible chat endpoint (`/v1/chat/completions`) for conversational interactions in Open WebUI, supporting profile selection from the `profiles` folder to customize settings or models.
- **Tool Server**: Expose Unicorn-Interpreter’s tools (e.g., Python execution, shell commands, file read/write) as individual endpoints (e.g., `/v1/tools/execute/python`) for Open WebUI’s “Tools” settings, allowing the LLM to invoke them.
- **Flexible Access**: Support local access on `localhost:8264` without authentication and remote access on `0.0.0.0:8264` with optional Bearer Token authentication.
- **Single OpenAPI Specification**: Use one `openapi.json` to define both chat and tool endpoints, ensuring compatibility with Open WebUI’s LLM and tool server configurations.

## Technical Approach
- **OpenAPI Specification**:
  - **Chat Endpoint**: `/v1/chat/completions` with a `profile` query parameter for selecting profiles from the `profiles` folder, supporting OpenAI-compatible request/response formats and streaming (`text/event-stream`).
  - **Tool Endpoints**: `/v1/tools/*` endpoints (e.g., `/v1/tools/execute/python`, `/v1/tools/files/read`) based on tools in `interpreter/computer_use/tools`, exposed as individual tools in Open WebUI.
  - **Authentication**: Optional Bearer Token authentication (`securitySchemes: BearerAuth`), enabled for remote access, skippable for `localhost`.
- **Server**: Run Unicorn-Interpreter’s FastAPI-based server on port 8264 to avoid conflicts with common ports.
- **Open WebUI Configuration**:
  - **LLM Connection**: Set base URL to `http://localhost:8264/v1` for chat interactions.
  - **Tool Server**: Configure `http://localhost:8264` with the `openapi.json` in Open WebUI’s “Tools” settings.
- **Profile Selection**: Allow users to specify a profile (e.g., `?profile=my_profile`) for chat interactions, defaulting to a standard profile if unspecified.

## Implementation Plan
1. **Save OpenAPI JSON**:
   - Store the provided `openapi.json` in the project directory and serve it at `http://localhost:8264/openapi.json`.
2. **Update Server**:
   - Implement `/v1/chat/completions` with profile loading from the `profiles` folder.
   - Add tool endpoints (e.g., `/v1/tools/execute/python`) using logic from `interpreter/computer_use/tools`.
   - Enable optional authentication for `0.0.0.0:8264`.
3. **Run Server**:
   - Local: `interpreter --server --host localhost --port 8264 --no-auth`
   - Remote: `interpreter --server --host 0.0.0.0 --port 8264 --auth`
4. **Configure Open WebUI**:
   - LLM: Set `http://localhost:8264/v1` in model settings.
   - Tools: Add `http://localhost:8264` with the `openapi.json` in “Tools” settings.
5. **Test**:
   - Verify chat functionality with profile selection.
   - Ensure tools appear individually in Open WebUI and execute correctly (e.g., run Python code, read files).

## Key Details
- **Port**: 8264 to avoid conflicts.
- **Tools**: Python execution, shell commands, file read/write, and file upload, extensible for additional tools in the fork.
- **Security**: Optional Bearer Token for remote access, disabled for local use.
- **Profiles**: Support for user-defined profiles in the `profiles` folder, selectable via query parameter.
- **Repository**: https://github.com/Unicorn-Commander/Unicorn-Interpreter

## Expected Outcome
Users can interact with Unicorn-Interpreter via Open WebUI’s UI, chatting as they would in the terminal (with profile customization) and invoking tools like code execution or file operations, all running locally or remotely with a single, unified API specification.

## Notes
- Ensure the server implements all specified endpoints and handles profile loading.
- Test tool endpoints to confirm they align with Open WebUI’s expectations for individual tool selection.
- For further assistance, refer to the detailed `openapi.json` and implementation steps in the project plan.