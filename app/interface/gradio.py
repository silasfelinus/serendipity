import gradio as gr

def predict(text):
    # Your API function goes here
    # It should take a string input and return a prediction
    prediction = "Hello, " + text + "!"
    return prediction

inputs = [
    gr.inputs.Textbox(label="Input text", placeholder="Enter your name here")
]

outputs = [
    gr.outputs.Textbox(label="Output text")
]

iface = gr.Interface(fn=predict, inputs=inputs, outputs=outputs, title="My API Web Service")
