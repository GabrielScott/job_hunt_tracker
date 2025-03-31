#!/bin/bash

# launcher.command - Script to launch the Job Hunt & Study Tracker application
# Put this file in the root directory of the application

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Activate the virtual environment if it exists
if [ -d "$DIR/venv" ]; then
    source "$DIR/venv/bin/activate"
fi

# Install requirements if needed (uncomment if you want automatic updates)
# pip install -r "$DIR/requirements.txt"

# Launch the Streamlit app
echo "Starting Job Hunt & Study Tracker..."
streamlit run "$DIR/app/main.py"