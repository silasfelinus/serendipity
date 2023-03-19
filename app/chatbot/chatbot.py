from .bot_config import BotConfig
from .conversation_handler import ConversationHandler
from .messaging_manager import MessagingManager
from .prompt_builder import PromptBuilder
from .response_handler import ResponseHandler

class Chatbot:
    def __init__(self, config_file_path):
        bot_config = BotConfig(config_file_path)
        self.conversation_handler = ConversationHandler(bot_config)
        self.messaging_manager = MessagingManager(bot_config)
        self.prompt_builder = PromptBuilder(bot_config)
        self.response_handler = ResponseHandler(bot_config)

    def response(self, user_input, chatbot_id, conversation_history):
        prompt = self.prompt_builder.build_prompt()
        processed_response = self.messaging_manager.generate_response(user_input, chatbot_id, conversation_history, prompt)
        self.conversation_handler.handle_conversation(user_input, chatbot_id, conversation_history)
        return processed_response
