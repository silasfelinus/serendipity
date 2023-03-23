# ./run.py
import asyncio
from app.main import main
if __name__ == "__main__":
    asyncio.run(main())

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

@app.route('/livechat')
async def api():
    return await render_template('livechat.html')

@app.route('/wonderwidgets')
async def wonderwidgets():
    return await render_template('wonderwidgets.html')

async def start_gradio_interface():
    iface = gr.Interface(fn=predict, inputs=inputs, outputs=outputs, title="Wonderwidgets Unleashed!")
    iface.launch() 

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
    
    
    import gradio as gr
from gradio.components import Textbox

def predict(text):
    # Your API function goes here
    # It should take a string input and return a prediction
    prediction = "Hello, " + text + "!"
    return prediction

inputs = [
    Textbox(label="Input text", placeholder="Enter your name here")
]

outputs = [
    Textbox(label="Output text")
]

iface = gr.Interface(fn=predict, inputs=inputs, outputs=outputs, title="Wonderwidgets Unleashed!")
