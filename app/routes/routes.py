# app/routes/routes.py
import os
from flask import Blueprint, jsonify, request, render_template
from app.chatbot.chatbot import Chatbot

# Get the path to the config file
config_file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.yaml')

# Initialize the Chatbot instance with the config file
chatbot = Chatbot(config_file_path)

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
