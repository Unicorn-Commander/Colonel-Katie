from fastapi import FastAPI
import uvicorn

from interpreter.core.core import OpenInterpreter
from interpreter.api.server import create_colonel_katie_server

# Initialize the OpenInterpreter instance
interpreter_instance = OpenInterpreter()

# Create the FastAPI app using the adapted server function
app = create_colonel_katie_server(interpreter_instance)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)