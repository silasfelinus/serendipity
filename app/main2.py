# Import required libraries
import threading
import gradio as gr
from quart import Quart, render_template, websocket
import asyncio

# Define your Gradio interface
def gradio_interface(x):
    return x[::-1]

gradio_interface = gr.Interface(
    fn=gradio_interface,
    inputs="text",
    outputs="text",
    title="Gradio Interface",
    description="Enter some text to reverse it!"
)

# Define your Quart app
app = Quart(__name__)

@app.route('/')
async def index():
    return await render_template('index.html')

# Define a WebSocket route for the Quart app
@app.websocket("/ws")
async def ws():
    while True:
        data = await websocket.receive()
        await websocket.send(data[::-1])
 
def gradio_task():
    iface = gr.Interface(...)
    iface.launch("0.0.0.0:5001", debug=True, share=True)       

def run_quart():
    app.run(host="0.0.0.0", port=5000)

# Define your main function to run both services
async def main():
    # Run the Gradio interface in the main thread
    gradio_thread = threading.Thread(target=gradio_interface.launch)
    gradio_thread.start()

    # Run the Quart app in a separate thread
    quart_thread = threading.Thread(target=run_quart)
    quart_thread.start()

    # Wait for both threads to finish
    gradio_thread.join()
    quart_thread.join()

# Run the main function
if __name__ == '__main__':
    main()
