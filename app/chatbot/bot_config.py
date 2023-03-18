#./app/chatbot/bot_config.py
import os
import yaml

class BotConfig:
    def __init__(self):
        config_file_path = os.environ.get('GLOBAL_CONFIG_FILE')
        if config_file_path is None:
            raise ValueError("GLOBAL_CONFIG_FILE environment variable not found.")
        
        with open(config_file_path, 'r') as config_file:
            self.config = yaml.safe_load(config_file) or {}

    def get_config(self, key):
        return self.config.get(key)

    def get_api_key(self):
        return os.environ.get("OPEN_AI_API_KEY")