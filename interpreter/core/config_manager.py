import json
import os

class ConfigManager:
    CONFIG_FILE = os.path.expanduser("~/.colonel-katie/config.json")

    def __init__(self):
        self.config = self._load_config()

    def _load_config(self):
        if os.path.exists(self.CONFIG_FILE):
            with open(self.CONFIG_FILE, "r") as f:
                return json.load(f)
        return {}

    def _save_config(self):
        os.makedirs(os.path.dirname(self.CONFIG_FILE), exist_ok=True)
        with open(self.CONFIG_FILE, "w") as f:
            json.dump(self.config, f, indent=4)

    def get(self, key, default=None):
        keys = key.split(".")
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def set(self, key, value):
        keys = key.split(".")
        target = self.config
        for i, k in enumerate(keys):
            if i == len(keys) - 1:
                target[k] = value
            else:
                if k not in target or not isinstance(target[k], dict):
                    target[k] = {}
                target = target[k]
        self._save_config()

# Example Usage (for testing)
if __name__ == "__main__":
    config_manager = ConfigManager()

    # Set a value
    config_manager.set("general.theme", "dark")
    config_manager.set("llm.default_model", "openai/gpt-4o")
    config_manager.set("audio.volume", 0.8)

    # Get a value
    theme = config_manager.get("general.theme")
    print(f"Current theme: {theme}")

    default_model = config_manager.get("llm.default_model")
    print(f"Default LLM model: {default_model}")

    volume = config_manager.get("audio.volume", 0.5) # With default
    print(f"Audio volume: {volume}")

    # Get a non-existent key
    non_existent = config_manager.get("non_existent.key", "default_value")
    print(f"Non-existent key: {non_existent}")

    # Update a value
    config_manager.set("audio.volume", 0.9)
    print(f"Updated audio volume: {config_manager.get("audio.volume")}")
