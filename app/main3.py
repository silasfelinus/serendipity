import threading
import quart
from gradio import Interface
from quart import Quart, render_template
import asyncio

app = Quart(__name__)

@app.route("/")
async def home():
    return await render_template("index.html")

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
    iface.launch(server_name="0.0.0.0", share=True, server_port=5001, disable_signal_handler=True)

def run_quart():
    app.run(host="0.0.0.0", port=5000)

def main():
    gradio_thread = threading.Thread(target=run_gradio)
    quart_thread = threading.Thread(target=run_quart)

    gradio_thread.start()
    quart_thread.start()

    gradio_thread.join()
    quart_thread.join()

if __name__ == "__main__":
    main()
