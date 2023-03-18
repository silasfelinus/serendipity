from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import uvicorn
from asgiref.wsgi import WsgiToAsgi
from routes.routes import api
from interface.gradio import create_interface
from logging_config import logger

# Log an informational message
logger.info("Hello, world!")

# Log a warning message
logger.warning("Something's not right here...")

# Log an error message with an exception
try:
    1 / 0
except Exception as e:
    logger.error("Error dividing by zero", exc_info=e)

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
