#./app/main.py

# Set up logging and environment variables
from .logging_config import setup_logging
logger = setup_logging()
from dotenv import load_dotenv
load_dotenv() 
import os


import multiprocessing
import quart
from gradio import Interface
from quart import Quart, render_template
import asyncio


# Create Quart app
app = Quart(__name__)

@app.route('/')
async def home():
    logger.info("Home route accessed.")
    return "Welcome to the application!"

@app.route('/livechat')
async def api():
    return await render_template('livechat.html')

@app.route('/wonderwidgets')
async def wonderwidgets():
    return await render_template('wonderwidgets.html')

@app.route('/gradio')
async def gradio_route():
    return await render_template('gradio.html')

async def start_gradio_interface():
    iface = gr.Interface(fn=predict, inputs=inputs, outputs=outputs, title="Wonderwidgets Unleashed!")
    iface.launch(server_name='0.0.0.0', server_port=5101)


async def start_quart_app():
    await app.run_task(host='0.0.0.0', port=5100)

async def main():
    logger.info("Freeing worker from trapped wonderwidget...")
    
    # Start Gradio interface
    gradio_task = asyncio.create_task(start_gradio_interface())
    
    # Start Quart app
    quart_task = asyncio.create_task(start_quart_app())

    # Wait for tasks to complete
    await asyncio.gather(quart_task, gradio_task)


if __name__ == "__main__":
    asyncio.run(main())