import json
import os

class QuickSettings:
    def __init__(self, config_file="quick_chat_settings.json"):
        self.config_file = config_file
        self.settings = self._load_settings()

    def _load_settings(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {"window_position": {"x": 100, "y": 100}, "window_size": {"width": 400, "height": 300}, "hotkey": "<ctrl>+<space>"}

    def _save_settings(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def get_setting(self, key, default=None):
        return self.settings.get(key, default)

    def set_setting(self, key, value):
        self.settings[key] = value
        self._save_settings()
