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
@api.route("/chatbot", methods=["POST"])
def chatbot_route():
    # Extract user input and chatbot_id from the incoming JSON request
    user_input = request.json['user_input']
    chatbot_id = request.json['chatbot_id']
    
    # Get the chatbot response based on user_input and chatbot_id
    response = chatbot.response(user_input, chatbot_id)
    
    # Return the response as a JSON object
    return jsonify({'response': response})
