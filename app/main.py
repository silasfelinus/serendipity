#./app/main.py

# Set up logging and environment variables
from .logging_config import setup_logging
logger = setup_logging()

import multiprocessing
import quart
from gradio import Interface
from quart import Quart, render_template
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Quart(__name__)

@app.route("/")
async def home():
    logger.info("Home route accessed.")
    return await render_template("index.html")

@app.route('/livechat')
async def api():
    return await render_template('livechat.html')

@app.route('/wonderwidgets')
async def wonderwidgets():
    return await render_template('wonderwidgets.html')

@app.route('/gradio')
async def gradio_route():
    return await render_template('gradio.html')

# Define your Gradio interface
def gradio_interface(x):
    return x[::-1]

def run_gradio():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    iface = Interface(
        fn=gradio_interface,
        inputs="text",
        outputs="text",
        title="Gradio Interface",
        description="Enter some text to reverse it!"
    )
    iface.launch(server_name="localhost", share=True, server_port=int(os.getenv("GRADIOPORT")))

def run_quart():
    app.run(host="localhost", port=int(os.getenv("QUARTPORT")))

def main():
    gradio_process = multiprocessing.Process(target=run_gradio)
    quart_process = multiprocessing.Process(target=run_quart)

    gradio_process.start()
    quart_process.start()

    gradio_process.join()
    quart_process.join()

if __name__ == "__main__":
    main()