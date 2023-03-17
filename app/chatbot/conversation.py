# Import the PromptBuilder class
from .prompt_builder import PromptBuilder

# Function to build a prompt using the PromptBuilder class
def build_prompt(chatbot, user_input, conversation_history=None):
    # Create a PromptBuilder instance with the chatbot, user input, and conversation history
    prompt_builder = PromptBuilder(chatbot, user_input, conversation_history)
    
    # Return the built prompt using the PromptBuilder instance
    return prompt_builder.build_prompt()
