#!/bin/bash

# Create the virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3.8 -m venv venv
fi

# Activate the virtual environment
if [ "$(uname)" == "Darwin" ] || [ "$(uname)" == "Linux" ]; then
    # macOS or Linux
    source venv/bin/activate
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ] || [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
    # Windows (Git Bash)
    source venv/Scripts/activate
else
    # Unsupported system
    echo "Unsupported system. Please run the commands manually."
    exit 1
fi

# Install the required packages
#pip install -r requirements.txt

# Source environment variables
if [ -f .env ]; then
    source ./.env
else
    echo "No .env file found, skipping sourcing environment variables."
fi

export PYTHONPATH=app
#DEVOPTION-comment to turn off testing before launch
pytest
# Run the application
python app/main.py