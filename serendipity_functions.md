# Serendipity Functions and Classes

**./trawler.py**
- def read_gitignore():
- def traverse_directory(gitignore_set, output_file, dir_path="."):
- def main():

---

**app/utils.py**
# Load configurations from global_config_file and bot_presets_file
- def load_config(global_config_file, bot_presets_file):
- def generate_response(prompt, config):

---

**app/logging_config.py**
- def setup_logging():
# Create a logger object

---

**app/utils/utils.py**
# Load configurations from global_config_file and bot_presets_file
- def load_config(global_config_file, bot_presets_file):
- def generate_response(prompt, config):

---

**app/interface/gradio.py**
# Initialize the Chatbot instance with a configuration file
- def chatbot_response(user_input, chatbot_id="serendipity-fairy", conversation_history=None):
- def create_interface():
---
**app/test/test_main.py**
# app/test/test_main.py
- def client():
- def test_main_route(client):
- def test_logger():
- def test_create_interface(mocker):

---

**app/chatbot/conversation.py**
# Import the PromptBuilder class
- def build_prompt(chatbot, user_input, conversation_history=None):

---

**app/chatbot/chatbot.py**
# Import the generate_response function from the response module
- class Chatbot:
- def __init__(self, config_file, chatbot_id="default"):
- def load_config(self):
- def response(self, user_input, chatbot_id):

---

**app/chatbot/response.py**
# Set the OpenAI API key
- def generate_response(prompt):

---

**app/chatbot/prompt_builder.py**
# Define the PromptBuilder class for constructing conversation prompts
- class PromptBuilder:
- def __init__(self, chatbot, user_input, conversation_history=None):
- def get_chatbot_by_id(chatbot_id, config):
- def build_prompt(self):

---

**app/routes/routes.py**
# app/routes/routes.py
- def main_page():
- def chatbot_route():

---

