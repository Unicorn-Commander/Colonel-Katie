"""
GPT-4.1-mini profile for The_Colonel with embedded API key
"""

from interpreter import interpreter
from datetime import date

today = date.today()

interpreter.llm.model = "gpt-4o-mini"
interpreter.llm.context_window = 128000
interpreter.llm.max_tokens = 16384
interpreter.llm.api_base = "https://api.openai.com/v1"
interpreter.llm.api_key = "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"
interpreter.llm.temperature = 0.1
interpreter.llm.supports_functions = True
interpreter.llm.supports_vision = True

interpreter.offline = False
interpreter.loop = False
interpreter.auto_run = True
interpreter.os = True
interpreter.computer.import_computer_api = True

# Custom instructions to help with screen capture issues
interpreter.custom_instructions = """When taking screenshots, if you encounter errors with pywinctl or getActiveWindow, 
try using computer.display.screenshot(active_app_only=False) instead to capture the full screen."""