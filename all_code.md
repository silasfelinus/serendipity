/home/silasfelinus/code/serendipity/app/logging_config.py
import logging
import sys

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("serendipity.log")
        ]
    )
    return logging.getLogger("serendipity")

logger = setup_logging()

-
/home/silasfelinus/code/serendipity/app/main.py
import os
from dotenv import load_dotenv
# Load environment variables from the .env file
load_dotenv()
config_path = os.environ.get('GLOBAL_CONFIG_FILE')

from flask import Flask, render_template, request, jsonify
import uvicorn
from asgiref.wsgi import WsgiToAsgi
from app.routes.routes import api
from app.interface.gradio import create_interface
from logging_config import logger
from app.livechat import livechat_bp, socketio
from app.chatbot import chatbot_bp

# Log an informational message
logger.info("Hello, world!")


# Create a Flask application instance
app = Flask(__name__)
# Register the routes blueprints
app.register_blueprint(api)
app.register_blueprint(livechat_bp, url_prefix='/livechat')
app.register_blueprint(chatbot_bp, url_prefix='/chatbot')

socketio.init_app(app)

# Create the Gradio interface for the chatbot
interface = create_interface()

# Main entry point of the application
if __name__ == "__main__":
    # Get the port number from the environment variable or use the default value
    port = int(os.environ.get("PORT", 7860))

    if os.environ.get("FLASK_ENV") == "development":
        app.run(host="0.0.0.0", port=port)
    else:
        interface.launch()  # Launch the Gradio interface
        uvicorn.run(WsgiToAsgi(app), host="0.0.0.0", port=port, log_level="info")

-
/home/silasfelinus/code/serendipity/app/__init__.py

-
/home/silasfelinus/code/serendipity/app/interface/gradio.py
import gradio as gr
from app.chatbot.routes.chatbot_routes import Chatbot

# Initialize the Chatbot instance with a configuration file
chatbot = Chatbot('config.yaml')

# Function to get a chatbot response based on user input, chatbot_id, and conversation history
def chatbot_response(user_input, chatbot_id="serendipity-fairy", conversation_history=None):
    # Generate a response using the Chatbot instance
    response = chatbot.response(user_input, chatbot_id, conversation_history)
    return response

# Function to create a Gradio interface for the chatbot
def create_interface():
    # Define the Gradio interface with input, output, title, and other information
    iface = gr.Interface(
        fn=chatbot_response,  # Function to call for generating chatbot responses
        inputs=[
        gr.components.Textbox(lines=2, label="Your message"),
        gr.components.Radio(choices=["serendipity-fairy", "serendipity-assistant"], label="Chatbot")
         ],
        outputs=gr.components.Textbox(label="Chatbot's response"),
        title="AI Chatbot",  # Title of the interface
        description="A chatbot with different personalities.",  # Description of the interface
        examples=[  # Example inputs and responses for users
            ["Can you tell me a joke?", "Sure, why did the tomato turn red? Because it saw the salad dressing!"],
            ["What's your favorite color?", "I don't have eyes, so I don't have a favorite color."]
        ]
    )
    return iface

-
/home/silasfelinus/code/serendipity/app/interface/__init__.py

-
/home/silasfelinus/code/serendipity/app/livechat/events.py
from flask_socketio import join_room, leave_room, send
from . import socketio

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(username + ' has entered the room.', room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)

@socketio.on('message')
def on_message(data):
    send(data['message'], room=data['room'])
-
/home/silasfelinus/code/serendipity/app/livechat/livechat.py

-
/home/silasfelinus/code/serendipity/app/livechat/routes.py
from flask import render_template
from . import livechat_bp

@livechat_bp.route('/')
def livechat():
    return render_template('livechat.html')
-
/home/silasfelinus/code/serendipity/app/livechat/__init__.py
from flask import Blueprint
from flask_socketio import SocketIO

livechat_bp = Blueprint('livechat', __name__)
socketio = SocketIO()

from . import routes, events

-
/home/silasfelinus/code/serendipity/app/test/test_main.py
# app/test/test_main.py
import os
import pytest
from app.main import app
from app.interface.gradio import create_interface

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_main_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Serendipity - Digital AI Assistant" in response.data

def test_logger():
    from app.logging_config import setup_logging
    logger = setup_logging()
    assert logger is not None

def test_create_interface(mocker):
    # Mock Gradio's Library
    mocker.patch('gradio.Interface')

    # Call the create_interface function
    interface = create_interface()

    # Check if the interface is not None
    assert interface is not None
-
/home/silasfelinus/code/serendipity/app/test/__init__.py

-
/home/silasfelinus/code/serendipity/app/chatbot/chatbot.py
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

-
/home/silasfelinus/code/serendipity/app/chatbot/conversation_handler.py
from app.chatbot.bot_config import BotConfig
from .messaging_manager import MessagingManager

class ConversationHandler:
    def __init__(self, bot_config):
        self.bot_config = BotConfig()
        self.messaging_manager = MessagingManager()

        # Define conversation history as a list
        self.conversation_history = []

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

-
/home/silasfelinus/code/serendipity/app/chatbot/bot_config.py
import os
import yaml

class BotConfig:
    def __init__(self):
        config_file_path = os.environ.get('GLOBAL_CONFIG_FILE')
        if config_file_path is None:
            raise ValueError("GLOBAL_CONFIG_FILE environment variable not found.")
        
        with open(config_file_path, 'r') as config_file:
            self.config = yaml.safe_load(config_file) or {}

    def get_config(self, key):
        return self.config.get(key)

    def get_api_key(self):
        return os.environ.get("OPEN_AI_API_KEY")
-
/home/silasfelinus/code/serendipity/app/chatbot/response_handler.py
class ResponseHandler:
    def __init__(self, bot_config):
        self.bot_name = bot_config["bot_name"]

    def process_response(self, response):
        # Remove the chatbot's name from the response, if it is present
        if response.startswith(self.bot_name + ":"):
            response = response[len(self.bot_name) + 1:].strip()

        return response

-
/home/silasfelinus/code/serendipity/app/chatbot/messaging_manager.py
from app.chatbot.prompt_builder import PromptBuilder
import openai

class MessagingManager:
    def __init__(self, bot_config):
        self.prompt_builder = PromptBuilder(bot_config)
        self.openai = openai(api_key=bot_config['api_key'])

    def build_prompt(self, user_input, conversation_history):
        return self.prompt_builder.build_prompt(user_input, conversation_history)

    def get_chatbot_response(self, prompt, chatbot_id):
        response = self.openai.Completion.create(
            engine=chatbot_id,
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response.choices[0].text.strip()

-
/home/silasfelinus/code/serendipity/app/chatbot/__init__.py
# app/chatbot/__init__.py

from .routes.chatbot_routes import chatbot_bp
-
/home/silasfelinus/code/serendipity/app/chatbot/prompt_builder.py
# Define the PromptBuilder class for constructing conversation prompts
class PromptBuilder:
    def __init__(self, bot_config, user_input=None):
        self.bot_config = bot_config
        self.user_input = user_input
        self.conversation_history = []

    # Function to get chatbot configuration by ID, merging with the default chatbot if available
    def get_chatbot_by_id(chatbot_id, config):
        default_chatbot = None
        target_chatbot = None

        # Iterate through chatbots to find the default and target chatbots
        for chatbot in config['chatbots']:
            if chatbot['id'] == 'default':
                default_chatbot = chatbot
            if chatbot['id'] == chatbot_id:
                target_chatbot = chatbot

        # If both default and target chatbots are found, merge their configurations
        if default_chatbot and target_chatbot:
            merged_chatbot = {**default_chatbot, **target_chatbot}
            return merged_chatbot
        return None
    
    # Function to build the conversation prompt
    def build_prompt(self):
        # Set of default keys for chatbot configuration
        default_keys = set([
            "id", "name", "human", "pronouns", "job", "personality", "directive",
            "likes", "dialect", "intro", "greeting"
        ])

        # If there is no conversation history, use the chatbot's intro and greeting
        if not self.conversation_history:
            prompt = self.chatbot['intro'].format(**self.chatbot)

            # Add any additional chatbot traits to the prompt
            additional_traits = {k: v for k, v in self.chatbot.items() if k not in default_keys}

            if additional_traits:
                prompt += "\n\nExtra traits:"
                for key, value in additional_traits.items():
                    prompt += f" - {key.capitalize()}: {value}"

            prompt += f"\n\n{self.chatbot['greeting'].format(**self.chatbot)}"
        else:
            prompt = ""

        # Add conversation history to the prompt
        for turn in self.conversation_history:
            prompt += f"\n\n{turn['user']}: {turn['input']}"
            prompt += f"\n\n{turn['chatbot']}: {turn['response']}"

        # Add the user's input to the prompt
        prompt += f"\n\n{self.chatbot['human']}: {self.user_input}"

        return prompt

-
/home/silasfelinus/code/serendipity/app/chatbot/routes/chatbot_routes.py
from flask import Blueprint, jsonify, request, render_template
from app.chatbot.conversation_handler import ConversationHandler
from app.chatbot.bot_config import BotConfig
import os

# Initialize the BotConfig instance with the config file
bot_config = BotConfig()

# Initialize the ConversationHandler instance with the bot configuration
conversation_handler = ConversationHandler()

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

-
/home/silasfelinus/code/serendipity/app/routes/routes.py
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

-
/home/silasfelinus/code/serendipity/app/routes/__init__.py


-
