# ./app/main.py

from .logging_config import setup_logging
from .gradio_app import run_gradio
import multiprocessing
import quart
from quart import Quart, render_template
import jsonify
import socket
import os
from dotenv import load_dotenv
import glob

# Load environment variables from .env file
load_dotenv()

# Set up logging
logger = setup_logging()

app = Quart(__name__)

# Function to register HTML routes
def register_html_routes(app, template_folder):
    for html_file in glob.glob(os.path.join(template_folder, "*.html")):
        route_name = os.path.splitext(os.path.basename(html_file))[0]
        route_path = f'/{route_name}'

        async def _route():
            return await render_template(html_file)

        app.add_url_rule(route_path, route_name, _route)

# Register HTML routes
template_folder = os.path.join(os.path.dirname(__file__), "templates")
register_html_routes(app, template_folder)

def find_available_port(start_port: int = 5000):
    port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            result = sock.connect_ex(('localhost', port))
            if result != 0:  # Port is available
                return port
            port += 1

@app.route('/widgetdemo')
async def widgetdemo():
    wonderwidgets_data = {"name": "Wonderwidget 1", "description": "A fun and interactive widget!", "price": "$19.99"}
    return jsonify(wonderwidgets_data)


def run_quart():
    app.run(host="0.0.0.0", port=int(os.getenv("QUARTPORT")))

def main():
    gradio_process = multiprocessing.Process(target=run_gradio, args=(find_available_port, int(os.getenv("GRADIOPORT"))))
    quart_process = multiprocessing.Process(target=run_quart)

    gradio_process.start()
    quart_process.start()

    gradio_process.join()
    quart_process.join()

if __name__ == "__main__":
    main()