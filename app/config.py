import yaml
from typing import List


def load_config_files(config_files: List[str]) -> dict:
    config = {}
    for config_file in config_files:
        with open(config_file, 'r') as file:
            config.update(yaml.safe_load(file))
    return config


# Generate a response using OpenAI's API based on the given prompt and configuration
def generate_response(prompt, config):
    response = openai.Completion.create(
        model=config["model"],
        prompt=prompt,
        temperature=config["temperature"],
        max_tokens=config["max_tokens"],
        top_p=config["top_p"],
        frequency_penalty=config["frequency_penalty"],
        presence_penalty=config["presence_penalty"],
        stop=["Human:", "AI:"]
    )
    # Return the generated response text, stripped of any leading/trailing whitespace
    return response.choices[0].text.strip()
