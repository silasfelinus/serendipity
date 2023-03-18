#./app/chatbot/conversation_handler.py
from app.chatbot.bot_config import BotConfig
from .messaging_manager import MessagingManager

class ConversationHandler:
    def __init__(self, bot_config):
        self.messaging_manager = MessagingManager(bot_config)

    def handle_conversation(self, user_input, chatbot_id, conversation_history):
        return self.messaging_manager.generate_response(user_input, chatbot_id, conversation_history)

    def start_conversation(self, user_input):
        # Add the user's input to the conversation history
        self.conversation_history.append({
            "user": self.bot_config.get_config("user_name"),
            "input": user_input,
            "chatbot": self.bot_config.get_config("chatbot_name"),
            "response": "",
        })

        # Build the conversation prompt
        prompt = self.messaging_manager.build_prompt(user_input, self.conversation_history)

        # Get the chatbot's response
        chatbot_response = self.messaging_manager.get_chatbot_response(prompt, self.bot_config.get_config("chatbot_id"))

        # Add the chatbot's response to the conversation history
        self.conversation_history[-1]["response"] = chatbot_response

        return chatbot_response
