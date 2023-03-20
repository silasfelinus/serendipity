# app/routes/routes.py
import os
from flask import Blueprint, jsonify, request, render_template
from app.chatbot.chatbot import Chatbot

# Get the path to the config file
config_file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.yaml')

# Initialize the Chatbot instance with the config file
chatbot = Chatbot(config_file_path)

# Create a Blueprint object for route handling
api = Blueprint("routes", __name__, url_prefix="/api")

# Route for the main page
@api.route("/api", methods=["GET"])
def main_page():
    return render_template("index.html")