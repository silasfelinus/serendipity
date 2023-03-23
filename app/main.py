# ./app/main.py

from flask import Flask, render_template
from .logging_config import setup_logging
from interface.gradio import gradio as gr

# Set up logging
logger = setup_logging()

# Create Flask app
app = Flask(__name__)

@app.route('/')
def home():
    logger.info("Home route accessed.")
    return "Welcome to the application!"

@app.route('/api')
def api():
    return render_template('api.html')

def main():
    logger.info("Starting the application...")
    iface.launch(share=True, app_name="Webapp WonderWidgets", interface_name="API Web Service")
    app.run(host='0.0.0.0', port=5000)
    logger.info("Finished executing the application.")

if __name__ == "__main__":
    main()