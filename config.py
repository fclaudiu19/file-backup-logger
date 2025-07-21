import json
import os

class ConfigManager:
    def __init__(self, config_path='config.json'):
        self.config_path = config_path
        self.default_config = {
            "source": "",
            "destination": "",
            "version": "v1",
            "zip": False
        }
        self.config = self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_path):
            self.save_config(self.default_config)
        with open(self.config_path, 'r') as f:
            return json.load(f)

    def save_config(self, config):
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=4)
        self.config = config
