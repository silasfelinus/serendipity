# Import the PromptBuilder class
from .prompt_builder import PromptBuilder

def build_prompt(chatbot, user_input, conversation_history=None):
    """
    Function to build a prompt using the PromptBuilder class.

    Args:
        chatbot: A Chatbot instance containing the chatbot's configuration.
        user_input: A string containing the user's input.
        conversation_history: A list of dictionaries representing the conversation history (optional).

    Returns:
        A string representing the built prompt for the chatbot.
    """
    # Create a PromptBuilder instance with the chatbot, user input, and conversation history
    prompt_builder = PromptBuilder(chatbot, user_input, conversation_history)
    
    # Return the built prompt using the PromptBuilder instance
    return prompt_builder.build_prompt()