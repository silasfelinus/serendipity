from app.chatbot.prompt_builder import PromptBuilder
from openai import OpenAI

class MessagingManager:
    def __init__(self, bot_config):
        self.prompt_builder = PromptBuilder(bot_config)
        self.openai = OpenAI(api_key=bot_config['api_key'])

    def build_prompt(self, user_input, conversation_history):
        return self.prompt_builder.build_prompt(user_input, conversation_history)

    def get_chatbot_response(self, prompt, chatbot_id):
        response = self.openai.Completion.create(
            engine=chatbot_id,
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response.choices[0].text.strip()
