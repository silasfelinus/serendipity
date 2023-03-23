import asyncio
import quart
from gradio import Interface
from quart import Quart, render_template

app = Quart(__name__)

@app.route("/")
async def home():
    return await render_template("index.html")

# Define your Gradio interface
def gradio_interface(x):
    return x[::-1]


async def run_gradio():
    iface = Interface(
    fn=gradio_interface,
    inputs="text",
    outputs="text",
    title="Gradio Interface",
    description="Enter some text to reverse it!"
)  # define your Gradio interface here
    await iface.launch(server_name="0.0.0.0", port=5001, start_server=True)

async def run_quart():
    await app.run(host="0.0.0.0", port=5000)

async def main():
    gradio_task = asyncio.create_task(run_gradio())
    quart_task = asyncio.create_task(run_quart())

    await asyncio.gather(gradio_task, quart_task)

if __name__ == "__main__":
    asyncio.run(main())