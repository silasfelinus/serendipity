class ResponseHandler:
    def __init__(self, bot_config):
        self.bot_name = bot_config["bot_name"]

    def process_response(self, response):
        # Remove the chatbot's name from the response, if it is present
        if response.startswith(self.bot_name + ":"):
            response = response[len(self.bot_name) + 1:].strip()

        return response
