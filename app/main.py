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
    iface.launch(server_name='192.168.5.231', server_port=5101)


async def start_quart_app():
    await app.run_task(host='192.168.5.231', port=5100)

async def main():

    logger.info("Freeing worker from trapped wonderwidget...")

    # Start Gradio interface
    loop = asyncio.get_event_loop()
    gradio_task = loop.run_in_executor(None, start_gradio_interface)

    # Start Quart app
    quart_task = asyncio.create_task(start_quart_app())

    # Wait for tasks to complete
    await asyncio.gather(gradio_task, quart_task)


if __name__ == "__main__":
    asyncio.run(main())