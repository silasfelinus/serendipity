# app/routes/routes.py
from flask import Blueprint, jsonify, request, render_template
from chatbot.chatbot import Chatbot

# Initialize the Chatbot instance with global_config_file and bot_presets_file
chatbot = Chatbot("config.json", "bot_presets.json")

# Create a Blueprint object for route handling
api = Blueprint("routes", __name__, url_prefix="/")

# Route for the main page
@api.route("/", methods=["GET"])
def main_page():
    return render_template("index.html")

# Route for handling chatbot requests
@api.route('/chatbot', methods=['POST'])
def chatbot_route():
    request_data = request.json
    user_input = request_data['user_input']
    chatbot_id = request_data['chatbot_id']
    conversation_history = request_data['conversation_history']
    response = chatbot.response(user_input, chatbot_id, conversation_history)
    return jsonify({'response': response})


