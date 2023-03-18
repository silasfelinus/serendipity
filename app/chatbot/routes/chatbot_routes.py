from flask import Blueprint, jsonify, request, render_template
from app.chatbot.conversation_handler import ConversationHandler
from app.chatbot.bot_config import BotConfig
import os

# Get the path to the config file
config_file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.yaml')

# Initialize the BotConfig instance with the config file
bot_config = BotConfig(config_file_path)

# Initialize the ConversationHandler instance with the bot configuration
conversation_handler = ConversationHandler(bot_config)

# Create a Blueprint object for route handling
chatbot_bp = Blueprint("chatbot_routes", __name__, url_prefix="/")

# Route for handling chatbot requests
@chatbot_bp.route('/chatbot', methods=['POST'])
def chatbot_route():
    request_data = request.json
    user_input = request_data['user_input']
    chatbot_id = request_data['chatbot_id']
    conversation_history = request_data['conversation_history']
    response = conversation_handler.handle_conversation(user_input, chatbot_id, conversation_history)
    return jsonify({'response': response})
