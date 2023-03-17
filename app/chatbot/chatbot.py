import json
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
        with open(self.config_file) as f:
            config = json.load(f)
        return config

    # Generate a chatbot response based on the user input and conversation history
    def response(self, user_input, chatbot_id):
        prompt = build_prompt(self, user_input, conversation_history)
        response = generate_response(prompt)
        return response