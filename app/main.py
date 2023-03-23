#./app/main.py

# Set up logging
from .logging_config import setup_logging
logger = setup_logging()

from quart import Quart, render_template
from app.interface.gradio import iface
import asyncio

app = Quart(__name__)

@app.route('/')
async def home():
    return await render_template('index.html')

@app.route('/wonderwidgets')
async def api():
    return await render_template('wonderwidgets.html')

def start_gradio_interface():
    iface.launch()

async def start_quart_app():
    await app.run_task(host='0.0.0.0', port=5000)

async def main():
    loop = asyncio.get_event_loop()

    # Start Gradio interface using run_in_executor
    gradio_task = loop.run_in_executor(None, start_gradio_interface)

    # Start Quart app
    quart_task = asyncio.create_task(start_quart_app())

    # Wait for tasks to complete
    await asyncio.gather(gradio_task, quart_task)

if __name__ == "__main__":
    asyncio.run(main())