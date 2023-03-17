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
    def response(self, user_input, conversation_history=None):
        prompt = self.build_prompt(user_input, conversation_history)
        response = generate_response(prompt)
        return response

    # Build the prompt to be sent to the response generator
    def build_prompt(self, user_input, conversation_history=None):
        # Define a set of default keys for the chatbot configuration
        default_keys = set([
            "id", "name", "human", "pronouns", "job", "personality", "directive",
            "likes", "dialect", "intro", "greeting"
        ])

        # Initialize conversation_history if not provided
        if conversation_history is None:
            conversation_history = []

        # Create an introduction prompt if no conversation history is available
        if not conversation_history:
            prompt = self.config['intro'].format(**self.config)

            # Add extra traits to the prompt if available
            additional_traits = {k: v for k, v in self.config.items() if k not in default_keys}

            if additional_traits:
                prompt += "\n\nExtra traits:"
                for key, value in additional_traits.items():
                    prompt += f" - {key.capitalize()}: {value}"

            prompt += f"\n\n{self.config['greeting'].format(**self.config)}"
        else:
            prompt = ""

        # Add previous conversation history to the prompt
        for turn in conversation_history:
            prompt += f"\n\n{turn['user']}: {turn['input']}"
            prompt += f"\n\n{turn['chatbot']}: {turn['response']}"

        # Add the user's input to the prompt
        prompt += f"\n\n{self.config['human']}: {user_input}"

        return prompt
