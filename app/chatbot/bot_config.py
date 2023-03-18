import os
import yaml

class BotConfig:
    def __init__(self):
        # Get the path to the config file from the environment variable
        config_file_path = os.environ.get('GLOBAL_CONFIG_FILE')
        
        # Load the configuration
        with open(config_file_path, 'r') as config_file:
            self.config = yaml.safe_load(config_file)

    def get_chatbot_config(self):
        return self.config_data["chatbot"]

    def get_api_key(self):
        return os.environ.get("OPEN_AI_API_KEY")
