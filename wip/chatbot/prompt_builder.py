#./app/chatbot/prompt_builder.py

class PromptBuilder:
    def __init__(self, bot_config, conversation_history):
        self.bot_config = bot_config
        self.conversation_history = conversation_history

    def build_prompt(self, user_input):
        chatbot_id = self.bot_config.get_config('id')
        intro = self.bot_config.get_config('intro', chatbot_id=chatbot_id)
        if intro is not None:
            prompt = intro.format(**self.bot_config.config)
        else:
            prompt = ""

        prompt += f"\n\n{self.bot_config.get_config('greeting', chatbot_id=chatbot_id).format(**self.bot_config.config)}"

        for turn in self.conversation_history:
            prompt += f"\n\n{turn['user']}: {turn['input']}"
            prompt += f"\n\n{turn['chatbot']}: {turn['response']}"

        prompt += f"\n\n{self.bot_config.get_config('human')}: {user_input}"

        return prompt