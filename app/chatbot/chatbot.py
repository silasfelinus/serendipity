from .bot_config import BotConfig
from .conversation_handler import ConversationHandler
from .messaging_manager import MessagingManager
from .prompt_builder import PromptBuilder
from .response_handler import ResponseHandler

class Chatbot:
    def __init__(self, config_file_path):
        conversation_handler = ConversationHandler()
        self.conversation_handler = ConversationHandler()
        self.messaging_manager = MessagingManager(bot_config)
        self.prompt_builder = PromptBuilder(bot_config)
        self.response_handler = ResponseHandler(bot_config)

    def response(self, user_input, chatbot_id, conversation_history):
        conversation = self.conversation_handler.get_conversation(chatbot_id, conversation_history)
        prompt = self.prompt_builder.build_prompt(conversation, user_input)
        response = self.messaging_manager.send_message(prompt)
        processed_response = self.response_handler.process_response(response)
        self.conversation_handler.update_conversation(chatbot_id, user_input, processed_response)
        return processed_response
