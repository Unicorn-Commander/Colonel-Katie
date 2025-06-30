from PySide6.QtCore import QThread, Signal
from interpreter import interpreter

class InterpreterWorker(QThread):
    new_chunk = Signal(dict)
    finished = Signal()
    error = Signal(str)
    memories_extracted = Signal(list) # New signal to emit extracted memories

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        try:
            for chunk in interpreter.chat(self.command, stream=True):
                if isinstance(chunk, dict):
                    self.new_chunk.emit(chunk)
                elif isinstance(chunk, str):
                    # Wrap string chunks into a dict for consistency
                    self.new_chunk.emit({"type": "message", "content": chunk})
            
            # After interpreter.chat finishes, extract and emit memories
            if interpreter.messages:
                # Find the last user message to define the exchange for memory extraction
                last_user_message_index = -1
                for i in range(len(interpreter.messages) - 1, -1, -1):
                    if interpreter.messages[i].get("role") == "user":
                        last_user_message_index = i
                        break
                
                if last_user_message_index != -1:
                    # Get all messages from the last user message to the end
                    last_exchange_messages = interpreter.messages[last_user_message_index:]
                    last_exchange_content = "\n".join([m["content"] for m in last_exchange_messages if "content" in m])
                    
                    extracted_memories = interpreter.llm.extract_memories(last_exchange_content)
                    self.memories_extracted.emit(extracted_memories)

        except Exception as e:
            self.error.emit(f"\nError: {e}\n")
        finally:
            self.finished.emit()

class IndexingWorker(QThread):
    indexing_finished = Signal()
    indexing_error = Signal(str)

    def __init__(self, directory_path, extensions=None):
        super().__init__()
        self.directory_path = directory_path
        self.extensions = extensions

    def run(self):
        try:
            interpreter.index_files(self.directory_path, self.extensions)
            self.indexing_finished.emit()
        except Exception as e:
            self.indexing_error.emit(str(e))
