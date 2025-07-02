import json
import os

class GlobalConfig:
    def __init__(self, config_file="global_config.json"):
        self.config_file = config_file
        self.config = self._load_config()

    def _load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)

    def get_setting(self, key, default=None):
        return self.config.get(key, default)

    def set_setting(self, key, value):
        self.config[key] = value
        self._save_config()
