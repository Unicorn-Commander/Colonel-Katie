"""Open Interpreter profile optimized for DeepSeek-R1"""
from interpreter import interpreter
from datetime import datetime

# Disable unused features
interpreter.tts = None
interpreter.llm.supports_functions = False  # DeepSeek doesn't support function calling
interpreter.llm.supports_vision = False

# Configure for DeepSeek-R1
interpreter.llm.model = "deepseek-reasoner"  # Official model name for R1
interpreter.llm.context_window = 128000  # Full 128k context support
interpreter.llm.max_tokens = 4096
interpreter.llm.api_base = "https://api.deepseek.com/v1"  # Verified API endpoint
interpreter.llm.api_key = os.getenv("DEEPSEEK_API_KEY")  # Add your DeepSeek API key here
interpreter.llm.temperature = 0.3  # Slightly higher for better reasoning
interpreter.llm.top_p = 0.95  # Better for complex reasoning tasks

# Skills configuration
skill_path = "./skills"
interpreter.computer.skills.path = skill_path

# Computer API settings
interpreter.computer.import_computer_api = True
interpreter.computer.import_skills = True

# System message optimized for DeepSeek-R1's reasoning strengths
interpreter.system_message = f"""Today is {datetime.now().strftime('%Y-%m-%d %H:%M')}. You are 01, an autonomous CLI assistant.
## Core Principles
- Execute Python code directly to solve problems (you have full permission)
- Install packages ONLY when necessary
- Be extremely concise (1 sentence responses when possible)
- NEVER use placeholders - all code must be executable as-is
- Break complex tasks into sequential steps
- Learn from output and iterate
- User CANNOT see code blocks - respond ONLY in plain text

## Special Instructions
1. When stuck: "Please provide more information."
2. Use skills with `computer.skills.new_skill()` when learning new procedures
3. Prefer incremental execution with verification
"""

# Execution settings optimized for reasoning
interpreter.auto_run = True  # Still valuable for rapid iteration
interpreter.loop = True
interpreter.max_output = 800  # Prevent verbose outputs from confusing R1

# Enhanced loop control
interpreter.loop_message = """Continue task execution. Use these EXACT responses when:
- Task complete: "The task is done."
- Impossible: "The task is impossible."
- Need input: "Please provide more information."
- No task: "Let me know what you'd like to do next."
Otherwise continue reasoning and executing step-by-step.
"""

interpreter.loop_breakers = [
    "The task is done.",
    "The task is impossible.",
    "Let me know what you'd like to do next.",
    "Please provide more information.",
]

# R1-specific optimizations
interpreter.llm.response_format = {"type": "text"}  # Ensure plain text responses
interpreter.auto_verify = True  # Add verification step for critical operations