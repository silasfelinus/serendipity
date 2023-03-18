from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import uvicorn
from asgiref.wsgi import WsgiToAsgi
from routes.routes import api
from interface.gradio import create_interface
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

# Main entry point of the application
if __name__ == "__main__":
    # Get the port number from the environment variable or use the default value
    port = int(os.environ.get("PORT", 7860))
    
    # Create the Gradio interface for the chatbot
    interface = create_interface()
    interface.launch()  # Launch the Gradio interface
    
if os.environ.get("FLASK_ENV") == "development":
        app.run(host="0.0.0.0", port=port)
else:
        uvicorn.run(WsgiToAsgi(app), host="0.0.0.0", port=port, log_level="info")