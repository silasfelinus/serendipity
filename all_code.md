C:\Users\silas\code\serendipity\app\logging_config.py
import logging
import sys

def setup_logging():
    # Create a logger object
    logger = logging.getLogger("serendipity")
    logger.setLevel(logging.DEBUG)

    # Create a console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    # Create a file handler for logging to a file
    file_handler = logging.FileHandler("serendipity.log")
    file_handler.setLevel(logging.DEBUG)

    # Create a formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

-
C:\Users\silas\code\serendipity\app\main.py
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import uvicorn
from asgiref.wsgi import WsgiToAsgi
from .routes.routes import api
from .interface.gradio import create_interface
from logging_config import setup_logging

logger = setup_logging()

# Now, you can use the logger object to log messages in your application.
logger.info("You found the secret message. Also, logger works!")

# Load environment variables from the .env file
load_dotenv()

# Create a Flask application instance
app = Flask(__name__)
# Register the routes blueprint
app.register_blueprint(api)

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
C:\Users\silas\code\serendipity\app\__init__.py

-
C:\Users\silas\code\serendipity\app\chatbot\chatbot.py
import yaml
from .conversation import build_prompt

# Import the generate_response function from the response module
from .response import generate_response

# Define the Chatbot class
class Chatbot:
    def __init__(self, config_file, chatbot_id="default"):
        self.config_file = config_file
        self.chatbot_id = chatbot_id
        self.config = self.load_config()

    # Load chatbot configuration from the given config file
    def load_config(self):
        file_path = self.config_file
        try:
            with open(file_path, 'r') as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file {file_path} not found.")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing config file {file_path}: {str(e)}")
        return config

    # Generate a chatbot response based on the user input and conversation history
    def response(self, user_input, chatbot_id, conversation_history):
        prompt = build_prompt(self, user_input, conversation_history)
        response = generate_response(prompt)
        return response
-
C:\Users\silas\code\serendipity\app\chatbot\conversation.py
# Import the PromptBuilder class
from .prompt_builder import PromptBuilder

# Function to build a prompt using the PromptBuilder class
def build_prompt(chatbot, user_input, conversation_history=None):
    # Create a PromptBuilder instance with the chatbot, user input, and conversation history
    prompt_builder = PromptBuilder(chatbot, user_input, conversation_history)
    
    # Return the built prompt using the PromptBuilder instance
    return prompt_builder.build_prompt()

-
C:\Users\silas\code\serendipity\app\chatbot\prompt_builder.py
# Define the PromptBuilder class for constructing conversation prompts
class PromptBuilder:
    def __init__(self, chatbot, user_input, conversation_history=None):
        self.chatbot = chatbot
        self.user_input = user_input
        self.conversation_history = conversation_history or []

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
C:\Users\silas\code\serendipity\app\chatbot\response.py
import openai
import os
from logging_config import logger

# Set the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to generate a response from OpenAI's GPT model based on the given prompt
def generate_response(prompt):
    # Call the OpenAI API to generate a completion with the provided prompt
    try:
        response = openai.Completion.create(
        engine="davinci",  # Use the "davinci" engine for generating responses
        prompt=prompt,  # Pass in the conversation prompt
        max_tokens=1024,  # Set the maximum number of tokens for the generated response
        n=1,  # Number of responses to generate
        stop=None,  # Stop token for truncating the response
        temperature=0.5,  # Sampling temperature to control randomness
    )
        return response.choices[0].text.strip()
    except Exception as e:
        # Log the exception and return an error message
        logger.error(f"Error generating response from OpenAI: {e}")
        return "An error occurred while generating a response. Please try again."

    # Return the generated response text, stripping any leading/trailing whitespace
    return response.choices[0].text.strip()
-
C:\Users\silas\code\serendipity\app\chatbot\__init__.py


-
C:\Users\silas\code\serendipity\app\interface\gradio.py
import gradio as gr
from ..chatbot.chatbot import Chatbot

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
C:\Users\silas\code\serendipity\app\interface\__init__.py

-
C:\Users\silas\code\serendipity\app\routes\routes.py
# app/routes/routes.py
import os
from flask import Blueprint, jsonify, request, render_template
from ..chatbot.chatbot import Chatbot

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
C:\Users\silas\code\serendipity\app\routes\__init__.py


-
C:\Users\silas\code\serendipity\app\test\test_main.py
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
C:\Users\silas\code\serendipity\app\test\__init__.py

-
