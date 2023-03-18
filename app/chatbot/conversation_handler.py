from app.chatbot.messaging_manager import MessagingManager

class ConversationHandler:
    def __init__(self, bot_config):
        self.messaging_manager = MessagingManager(bot_config)

    def handle_conversation(self, user_input, chatbot_id, conversation_history):
        # Generate a prompt based on the user's input and conversation history
        prompt = self.messaging_manager.build_prompt(user_input, conversation_history)

        # Send the prompt to the chatbot API and get the response
        response = self.messaging_manager.get_chatbot_response(prompt, chatbot_id)

        # Update the conversation history with the user's input and chatbot's response
        conversation_history.append({'role': 'user', 'content': user_input})
        conversation_history.append({'role': 'assistant', 'content': response})

        return response
