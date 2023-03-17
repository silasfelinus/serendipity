from flask import Blueprint, jsonify, request
from app.chatbot.chatbot import Chatbot

# Initialize the Chatbot instance with a configuration file
chatbot = Chatbot("config.json", "config.json")

# Create a Blueprint object for route handling
bp = Blueprint("routes", __name__, url_prefix="/")

# Route for handling chatbot requests
@bp.route("/chatbot", methods=["POST"])
def chatbot_route():
    # Extract user input and chatbot_id from the incoming JSON request
    user_input = request.json['user_input']
    chatbot_id = request.json['chatbot_id']
    
    # Get the chatbot response based on user_input and chatbot_id
    response = chatbot.response(user_input, chatbot_id)
    
    # Return the response as a JSON object
    return jsonify({'response': response})