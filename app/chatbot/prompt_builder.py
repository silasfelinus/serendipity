# Define the PromptBuilder class for constructing conversation prompts
class PromptBuilder:
    def __init__(self, bot_config, user_input=None):
        self.bot_config = bot_config
        self.user_input = user_input
        self.conversation_history = []

    # Function to get chatbot configuration by ID, merging with the default chatbot if available
    def get_chatbot_by_id(chatbot_id, config):
        default_chatbot = None
        target_chatbot = None

        # Iterate through chatbots to find the default and target chatbots
        for chatbot in config['chatbots']:
            if chatbot['id'] == 'default':
                default_chatbot = chatbot
            if chatbot['id'] == chatbot_id:
                target_chatbot = chatbot

        # If both default and target chatbots are found, merge their configurations
        if default_chatbot and target_chatbot:
            merged_chatbot = {**default_chatbot, **target_chatbot}
            return merged_chatbot
        return None
    
    # Function to build the conversation prompt
    def build_prompt(self):
        # Set of default keys for chatbot configuration
        default_keys = set([
            "id", "name", "human", "pronouns", "job", "personality", "directive",
            "likes", "dialect", "intro", "greeting"
        ])

        # If there is no conversation history, use the chatbot's intro and greeting
        if not self.conversation_history:
            prompt = self.chatbot['intro'].format(**self.chatbot)

            # Add any additional chatbot traits to the prompt
            additional_traits = {k: v for k, v in self.chatbot.items() if k not in default_keys}

            if additional_traits:
                prompt += "\n\nExtra traits:"
                for key, value in additional_traits.items():
                    prompt += f" - {key.capitalize()}: {value}"

            prompt += f"\n\n{self.chatbot['greeting'].format(**self.chatbot)}"
        else:
            prompt = ""

        # Add conversation history to the prompt
        for turn in self.conversation_history:
            prompt += f"\n\n{turn['user']}: {turn['input']}"
            prompt += f"\n\n{turn['chatbot']}: {turn['response']}"

        # Add the user's input to the prompt
        prompt += f"\n\n{self.chatbot['human']}: {self.user_input}"

        return prompt
