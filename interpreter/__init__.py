from .core.core import OpenInterpreter

# This __init__.py is intentionally minimal to avoid circular imports and side effects.
# The OpenInterpreter class is exposed directly for import.
# Complex setup logic or command-line argument parsing should be handled in dedicated entry points (e.g., interpreter.api.main or CLI scripts).
