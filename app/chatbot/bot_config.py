#./app/chatbot/bot_config.py

import os
import yaml
from dotenv import load_dotenv
# Load environment variables from the .env file
load_dotenv()

class BotConfig:
    def __init__(self, config_file_path=None):
        if config_file_path is None:
            config_file_path = os.environ.get('GLOBAL_CONFIG_FILE')

        with open(config_file_path, 'r') as config_file:
            self.config = yaml.safe_load(config_file)

    def get_config(self, key, chatbot_id='default'):
        if chatbot_id == 'default':
            return self.config.get(key)

        chatbot_configs = self.config.get('bot', {}).get('chatbots', [])
        for chatbot_config in chatbot_configs:
            if chatbot_config['id'] == chatbot_id:
                return chatbot_config.get(key)

        return None
    
    def get_api_key(self):
        return os.environ.get('OPEN_AI_API_KEY')
