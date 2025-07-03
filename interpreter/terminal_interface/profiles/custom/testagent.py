"""This is a custom generated Open Interpreter profile.
"""

# Import the interpreter
from interpreter import interpreter

# You can import other libraries too
from datetime import date

# You can set variables
today = date.today()

# Agent Metadata
interpreter.agent_name = "TestAgent"
interpreter.profile_picture = "/path/to/test_pic.png"

# System Prompt
interpreter.system_prompt = f"""    This is a test system prompt.
    """

# LLM Settings
interpreter.llm.model = "groq/llama-3.1-70b-versatile"
interpreter.llm.context_window = 110000
interpreter.llm.max_tokens = 4096
interpreter.llm.api_base = "https://api.example.com"
interpreter.llm.api_key = "your_api_key_here"
interpreter.llm.supports_functions = False
interpreter.llm.supports_vision = False


# Interpreter Settings
interpreter.offline = False
interpreter.loop = True
interpreter.auto_run = False

# Toggle OS Mode - https://docs.openinterpreter.com/guides/os-mode
interpreter.os = False

# Import Computer API - https://docs.openinterpreter.com/code-execution/computer-api
interpreter.computer.import_computer_api = True

# Tools
interpreter.tools = ['shell', 'files']

# Set Custom Instructions to improve your Interpreter's performance at a given task
interpreter.custom_instructions = f"""    These are test custom instructions.
    """
