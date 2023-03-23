# ./app/main.py

from quart import Quart, render_template
from .logging_config import setup_logging
from app.interface.gradio import predict, inputs, outputs
import gradio as gr
from gradio.components import Textbox
import asyncio

# Set up logging
logger = setup_logging()

# Create Quart app
app = Quart(__name__)

@app.route('/')
async def home():
    logger.info("Home route accessed.")
    return "Welcome to the application!"

@app.route('/api')
async def api():
    return await render_template('api.html')

async def start_gradio_interface():
    iface = gr.Interface(fn=predict, inputs=inputs, outputs=outputs, title="My API Web Service")
    await iface.run()

async def start_quart_app():
    await app.run_task(host='0.0.0.0', port=5000)

async def main():
    logger.info("Starting the application...")

    # Start Gradio interface
    gradio_task = asyncio.create_task(start_gradio_interface())

    # Start Quart app
    quart_task = asyncio.create_task(start_quart_app())

    # Wait for tasks to complete
    await asyncio.gather(gradio_task, quart_task)

if __name__ == "__main__":
    asyncio.run(main())