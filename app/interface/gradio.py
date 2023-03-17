import gradio
from app.chatbot.chatbot import Chatbot

# Initialize the Chatbot instance with a configuration file
chatbot = Chatbot("config.json", "config.json")

# Function to get a chatbot response based on user input, chatbot_id, and conversation history
def chatbot_response(user_input, chatbot_id="serendipity-fairy", conversation_history=None):
    # Generate a response using the Chatbot instance
    response = chatbot.response(user_input, chatbot_id, conversation_history)
    return response

# Function to create a Gradio interface for the chatbot
def create_interface():
    # Define the Gradio interface with input, output, title, and other information
    iface = gradio.Interface(
        fn=chatbot_response,  # Function to call for generating chatbot responses
        inputs=[
            gradio.inputs.Textbox(lines=2, label="Your message"),  # User input textbox
            gradio.inputs.Radio(["serendipity-fairy", "serendipity-assistant"], label="Chatbot")  # Chatbot selection radio
        ],
        outputs=gradio.outputs.Textbox(label="Chatbot's response"),  # Output textbox to display chatbot's response
        title="AI Chatbot",  # Title of the interface
        description="A chatbot with different personalities.",  # Description of the interface
        examples=[  # Example inputs and responses for users
            ["Can you tell me a joke?", "Sure, why did the tomato turn red? Because it saw the salad dressing!"],
            ["What's your favorite color?", "I don't have eyes, so I don't have a favorite color."]
        ]
    )
    return iface

if __name__ == "__main__":
    iface = create_interface()
    iface.launch()  # Launch the Gradio interface
