#!/bin/bash

# Check if Python 3.8 is installed
if ! command -v python3.8 &> /dev/null; then
    # Python 3.8 is not installed, so install it
    if [ "$(uname)" == "Darwin" ]; then
        # macOS
        echo "Python 3.8 is not installed. Please install it manually using Homebrew or another method."
        exit 1
    elif [ "$(uname)" == "Linux" ]; then
        # Linux
        echo "Installing Python 3.8 and venv..."
        sudo add-apt-repository ppa:deadsnakes/ppa
        sudo apt-get update
        sudo apt-get install python3.8 python3.8-venv -y
    else
        # Unsupported system
        echo "Unsupported system. Please install Python 3.8 manually."
        exit 1
    fi
fi

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

# Function to calculate the time difference
time_since_last_update() {
    if [ -f "$1" ]; then
        local last_update=$(cat "$1")
        local current_time=$(date +%s)
        local time_diff=$(( (current_time - last_update) / 86400 ))
        echo $time_diff
    else
        echo "NA"
    fi
}

# Check if it's been more than a day since the last update
timestamp_file=".last_requirements_update"
time_diff=$(time_since_last_update "$timestamp_file")

if [ "$time_diff" == "NA" ] || [ $time_diff -gt 0 ]; then
    # Install the required packages
    pip install -r requirements.txt
    # Update the timestamp file
    date +%s > "$timestamp_file"
else
    echo "Skipping requirements installation as it was updated less than a day ago."
fi

# Source environment variables
if [ -f .env ]; then
    source ./.env
else
    echo "No .env file found, skipping sourcing environment variables."
fi

# Run tests
python -m pytest

# Check if tests passed
if [ $? -eq 0 ]; then
    # Run the application
    python run.py
else
    echo "Tests failed. Fix the issues before running the application."
fi
