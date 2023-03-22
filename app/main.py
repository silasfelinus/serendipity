# ./app/main.py

from flask import Flask
from .logging_config import setup_logging

# Set up logging
logger = setup_logging()

# Create Flask app
app = Flask(__name__)

@app.route('/')
def home():
    logger.info("Home route accessed.")
    return "Welcome to the application!"

def main():
    logger.info("Starting the application...")
    app.run(host='0.0.0.0', port=5000)
    logger.info("Finished executing the application.")

if __name__ == "__main__":
    main()