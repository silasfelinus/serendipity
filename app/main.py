# ./app/main.py

from flask import Flask, render_template
from .logging_config import setup_logging
from app.interface.gradio import predict, inputs, outputs
import gradio as gr
import threading

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

def start_flask_app():
    app.run(host='0.0.0.0', port=5000)
    
def start_gradio_interface():
    iface = gr.Interface(fn=predict, inputs=inputs, outputs=outputs, title="Wonderwidgets Unleashed")
    iface.launch(share=True)

def main():
    logger.info("Starting the application...")
    flask_thread = threading.Thread(target=start_flask_app)
    flask_thread.start()

    gradio_thread = threading.Thread(target=start_gradio_interface)
    gradio_thread.start()
    app.run(host='0.0.0.0', port=5000)
    logger.info("Finished executing the application.")

if __name__ == "__main__":
    main()
