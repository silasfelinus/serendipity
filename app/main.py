#./app/main.py

import os
from dotenv import load_dotenv
# Load environment variables from the .env file
load_dotenv()
config_path = os.environ.get('GLOBAL_CONFIG_FILE')

from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo
import uvicorn
from asgiref.wsgi import WsgiToAsgi
from app.routes.routes import api
from app.interface.gradio import create_interface
from .logging_config import logger
from app.livechat import livechat_bp, socketio
from app.chatbot.routes.chatbot_routes import chatbot_bp

# Log an informational message
logger.info("Hello, world!")

# Create a Flask application instance
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://192.168.4.3:27017/serendipity"
mongo = PyMongo(app)

# Register the routes blueprints
app.register_blueprint(api)
app.register_blueprint(livechat_bp, url_prefix='/livechat')
app.register_blueprint(chatbot_bp, url_prefix='/chatbot')

socketio.init_app(app)

# Create the Gradio interface for the chatbot
interface = create_interface()

# Define routes and view functions here

if __name__ == "__main__":
    # Get the port number from the environment variable or use the default value
    port = int(os.environ.get("PORT", 7860))

    if os.environ.get("FLASK_ENV") == "development":
        app.run(host="0.0.0.0", port=port)
    else:
        interface.launch()  # Launch the Gradio interface
        uvicorn.run(WsgiToAsgi(app), host="0.0.0.0", port=port, log_level="info")