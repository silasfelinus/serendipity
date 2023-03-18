import json
import openai

# Load configurations from global_config_file and bot_presets_file
def load_config(global_config_file, bot_presets_file):
    # Read global_config_file and load its content as JSON
    with open(global_config_file) as f:
        global_config = json.load(f)

    # Read bot_presets_file and load its content as JSON
    with open(bot_presets_file) as f:
        bot_presets = json.load(f)

    # Merge the two JSON objects and return the result
    return {**global_config, **bot_presets}

# Generate a response using OpenAI's API based on the given prompt and configuration
def generate_response(prompt, config, stop=["Human:", "AI:"]):
    response = openai.Completion.create(
        model=config["model"],
        prompt=prompt,
        temperature=config["temperature"],
        max_tokens=config["max_tokens"],
        top_p=config["top_p"],
        frequency_penalty=config["frequency_penalty"],
        presence_penalty=config["presence_penalty"],
        stop=stop
    )
    # Return the generated response text, stripped of any leading/trailing whitespace
    return response.choices[0].text.strip()