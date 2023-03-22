#./app/main.py

import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()
config_path = os.environ.get('GLOBAL_CONFIG_FILE')

from flask import Flask, jsonify
from flask_pymongo import PyMongo
from app.routes.routes import api
from app.interface.gradio import create_interface
from app.config.logging_config import logger

# Set up logging
logger = setup_logging()

# Create a Flask application instance
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://192.168.4.3:27017/serendipity?directConnection=true"
mongo = PyMongo(app)

# Register the routes blueprints
app.register_blueprint(api)
app.register_blueprint(livechat_bp, url_prefix='/livechat')
app.register_blueprint(chatbot_bp, url_prefix='/chatbot')
# app/routes/routes.py
import os
from flask import Blueprint, jsonify, request, render_template

# Get the path to the config file
config_file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.yaml')

# Initialize the Chatbot instance with the config file
#chatbot = Chatbot(config_file_path)

# Create a Blueprint object for route handling
api = Blueprint("routes", __name__, url_prefix="/api")

# Route for the main page
@api.route("/api", methods=["GET"])
def main_page():
    return render_template("index.html")

socketio.init_app(app)

def launch_gradio():
    interface = create_interface()
    interface.launch()

# Define routes and view functions here
@app.route('/test_mongo', methods=['GET'])
def test_mongo():
    try:
        # Insert a sample document into the 'users' collection
        user = {
            "name": "Silas Knight",
            "email": "silasfelinus@gmail.com",
            "birthday": "09/08/1977"
        }
        inserted_id = mongo.db.users.insert_one(user).inserted_id

        # Retrieve the document from the 'users' collection using the inserted_id
        retrieved_user = mongo.db.users.find_one({"_id": inserted_id})

        # Convert the ObjectId to str to make it JSON serializable
        retrieved_user["_id"] = str(retrieved_user["_id"])

        # Return the retrieved document as JSON
        return jsonify(retrieved_user)

    except Exception as e:
        logger.error(f"Error in test_mongo: {str(e)}")
        return jsonify({"error": str(e)}), 500
def main():
    logger.info("Starting the application...")
    # Your application code here
    logger.info("Finished executing the application.")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))

    launch_gradio()

    # Run the Flask app
    app.run(host="0.0.0.0", port=port)