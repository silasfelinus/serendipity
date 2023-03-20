#!/bin/bash
#currently broken

#Manual Install For Windows:
# python3.8 -m venv venv
# source venv/Scripts/activate
# pip install -r requirements.txt
# source ./.env


# Check if Python 3.8 is installed
if ! command -v python3.8 &> /dev/null; then
    # Python 3.8 is not installed, so install it
    if [ "$(uname)" == "Darwin" ] || [ "$(uname)" == "Linux" ]; then
        # macOS or Linux
        echo 'sudo add-apt-repository ppa:deadsnakes/ppa'
        echo 'sudo apt-get update'
        echo 'sudo apt-get install python3.8'
        echo 'sudo apt-get install python3.8-venv'
    elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ] || [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
        # Windows (Git Bash)
        echo "Python 3.8 is not installed. Please install it manually."
        exit 1
    else
        # Unsupported system
        echo "Unsupported system. Please install Python 3.8 manually."
        exit 1
    fi
fi

# Create the virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo 'sudo apt-get install python3.8-venv -y'
    echo 'python3.8 -m venv venv'
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
echo "pip install -r requirements.txt"

# Source environment variables
if [ -f .env ]; then
    source ./.env
else
    echo "No .env file found, skipping sourcing environment variables."
fi


#comment to turn off testing
python -m pytest

# Run the application
python app/main.py
