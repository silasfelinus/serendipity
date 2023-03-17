# Import the required libraries
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import uvicorn
from app.routes.routes import routes
from app.gradio.interface import create_interface
from serendipity.app.logging_config import setup_logging

logger = setup_logging()

# Now, you can use the logger object to log messages in your application.
logger.info("You found the secret message. Also, logger works!")

# Load environment variables from the .env file
load_dotenv()

# Create a Flask application instance
app = Flask(__name__)
# Register the routes blueprint
app.register_blueprint(routes)

# Main entry point of the application
if __name__ == "__main__":
    # Get the port number from the environment variable or use the default value
    port = int(os.environ.get("PORT", 7860))
    
    # Create the Gradio interface for the chatbot
    interface = create_interface()
    
    # Run the application using the Uvicorn ASGI server
    uvicorn.run(app, host="0.0.0.0", port=port)
