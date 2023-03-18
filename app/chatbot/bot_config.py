import yaml
import os


class BotConfig:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.config_data = None
        self.load_config()

    def load_config(self):
        with open(self.config_file_path, "r") as config_file:
            self.config_data = yaml.safe_load(config_file)

    def get_chatbot_config(self):
        return self.config_data["chatbot"]

    def get_api_key(self):
        return os.environ.get("OPEN_AI_API_KEY")
