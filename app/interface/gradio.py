import gradio as gr
from app.chatbot.routes.chatbot_routes import Chatbot

# Initialize the Chatbot instance with a configuration file
chatbot = Chatbot('config.yaml')

# Function to get a chatbot response based on user input, chatbot_id, and conversation history
def chatbot_response(user_input, chatbot_id="serendipity-fairy", conversation_history=None):
    # Generate a response using the Chatbot instance
    response = chatbot.response(user_input, chatbot_id, conversation_history)
    return response

# Function to create a Gradio interface for the chatbot
def create_interface():
    # Define the Gradio interface with input, output, title, and other information
    iface = gr.Interface(
        fn=chatbot_response,  # Function to call for generating chatbot responses
        inputs=[
        gr.components.Textbox(lines=2, label="Your message"),
        gr.components.Radio(choices=["serendipity-fairy", "serendipity-assistant"], label="Chatbot")
         ],
        outputs=gr.components.Textbox(label="Chatbot's response"),
        title="AI Chatbot",  # Title of the interface
        description="A chatbot with different personalities.",  # Description of the interface
        examples=[  # Example inputs and responses for users
            ["Can you tell me a joke?", "Sure, why did the tomato turn red? Because it saw the salad dressing!"],
            ["What's your favorite color?", "I don't have eyes, so I don't have a favorite color."]
        ]
    )
    return iface
