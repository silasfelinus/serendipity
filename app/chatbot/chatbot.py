import yaml
import os
from .conversation import build_prompt

# Import the generate_response function from the response module
from .response import generate_response

# Define the Chatbot class
class Chatbot:
    def __init__(self, config_file, chatbot_id="default"):
        self.config_file = config_file
        self.chatbot_id = chatbot_id
        self.config = self.load_config()

    # Load chatbot configuration from the given config file
    def load_config(self):
        file_path = self.config_file
        try:
            with open(file_path, 'r') as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file {file_path} not found.")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing config file {file_path}: {str(e)}")
        return config

    # Generate a chatbot response based on the user input and conversation history
    def response(self, user_input, chatbot_id, conversation_history):
        prompt = build_prompt(self, user_input, conversation_history)
        response = generate_response(prompt)
        return response