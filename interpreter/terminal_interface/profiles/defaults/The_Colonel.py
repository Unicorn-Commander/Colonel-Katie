"""
The_Colonel profile - Default configuration for The_Colonel
"""

import os
from interpreter import interpreter
from datetime import date

today = date.today()

interpreter.llm.model = "gpt-4o-mini"
interpreter.llm.context_window = 128000
interpreter.llm.max_tokens = 16384
interpreter.llm.api_base = "https://api.openai.com/v1"
interpreter.llm.api_key = os.getenv("OPENAI_API_KEY")
interpreter.llm.temperature = 0.1
interpreter.llm.supports_functions = True
interpreter.llm.supports_vision = True

interpreter.offline = False
interpreter.loop = True
interpreter.auto_run = False
interpreter.os = True
interpreter.computer.import_computer_api = True

# Custom instructions to help with screen capture issues
interpreter.custom_instructions = """When taking screenshots, if you encounter errors with pywinctl or getActiveWindow, 
try using computer.display.screenshot(active_app_only=False) instead to capture the full screen."""