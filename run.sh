#!/bin/bash

# Check if the venv directory exists and if a virtual environment is not already active
if [ -d "venv" ] && [ -z "$VIRTUAL_ENV" ]; then
  echo "Activating virtual environment..."
  source venv/bin/activate
fi

# Run the application
python3 src/main.py
