#./app/main.py

import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()
config_path = os.environ.get('GLOBAL_CONFIG_FILE')

from flask import Flask, jsonify
from flask_pymongo import PyMongo
from threading import Thread
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

def launch_gradio():
    interface = create_interface()
    interface.launch()

# Define routes and view functions here
@app.route('/testmongo', methods=['GET'])
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
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))

    # Launch the Gradio interface in a separate thread
    gradio_thread = Thread(target=launch_gradio)
    gradio_thread.start()

    # Run the Flask app
    app.run(host="0.0.0.0", port=port)