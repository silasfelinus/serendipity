import openai
import os

# Set the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to generate a response from OpenAI's GPT model based on the given prompt
def generate_response(prompt):
    # Call the OpenAI API to generate a completion with the provided prompt
    response = openai.Completion.create(
        engine="davinci",  # Use the "davinci" engine for generating responses
        prompt=prompt,  # Pass in the conversation prompt
        max_tokens=1024,  # Set the maximum number of tokens for the generated response
        n=1,  # Number of responses to generate
        stop=None,  # Stop token for truncating the response
        temperature=0.5,  # Sampling temperature to control randomness
    )

    # Return the generated response text, stripping any leading/trailing whitespace
    return response.choices[0].text.strip()