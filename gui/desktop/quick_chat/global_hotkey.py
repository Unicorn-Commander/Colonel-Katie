from pynput import keyboard
from PySide6.QtCore import QObject, Signal

class GlobalHotkey(QObject):
    activated = Signal()

    def __init__(self, hotkey="<ctrl>+<space>", parent=None):
        super().__init__(parent)
        self.hotkey_str = hotkey
        self.hotkey = keyboard.GlobalHotKey(hotkey, self._on_activate)

    def _on_activate(self):
        print(f"Hotkey {self.hotkey_str} activated!")
        self.activated.emit()

    def start(self):
        self.hotkey.start()
        print(f"Global hotkey '{self.hotkey_str}' registered.")

    def stop(self):
        self.hotkey.stop()
        print(f"Global hotkey '{self.hotkey_str}' unregistered.")
