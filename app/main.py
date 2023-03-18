from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import uvicorn
from asgiref.wsgi import WsgiToAsgi
from app.routes.routes import api
from app.interface.gradio import create_interface
from logging_config import logger
from app.livechat import livechat_bp, socketio


# Log an informational message
logger.info("Hello, world!")


# Load environment variables from the .env file
load_dotenv()

# Create a Flask application instance
app = Flask(__name__)
# Register the routes blueprints
app.register_blueprint(api)
app.register_blueprint(livechat_bp, url_prefix='/livechat')

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
