# ./app/gradio_app.py

import asyncio
from gradio import Interface

def gradio_interface(x):
    return x[::-1]

def run_gradio(find_available_port, server_port):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    iface = Interface(
        fn=gradio_interface,
        inputs="text",
        outputs="text",
        title="Gradio Interface",
        description="Enter some text to reverse it!"
    )
    available_port = find_available_port(server_port)
    iface.launch(server_name="0.0.0.0", share=True, server_port=available_port)