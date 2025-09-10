#!/bin/bash

# SQLmap GUI Launcher Script
# This script activates the virtual environment and starts the GUI

echo "Starting SQLmap GUI..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Please run setup first:"
    echo "python -m venv .venv"
    echo "source .venv/bin/activate"
    echo "pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Check if dependencies are installed
python -c "import PyQt6" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Dependencies not installed. Installing now..."
    pip install -r requirements.txt
fi

# Start the GUI
echo "Launching SQLmap GUI..."
python main.py

echo "SQLmap GUI closed."
