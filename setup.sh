#!/bin/bash

# This script sets up the necessary virtual environment and dependencies
# to build the PtcgTournamentSim application.

# --- Configuration ---
VENV_DIR="venv"

# --- Setup Process ---
echo "--- Starting Project Setup ---"

# 1. Check for and create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment not found. Creating one..."
    # Try python3 first, then fall back to python
    if command -v python3 &> /dev/null; then
        python3 -m venv "$VENV_DIR"
    elif command -v python &> /dev/null; then
        python -m venv "$VENV_DIR"
    else
        echo "Error: Neither 'python3' nor 'python' command found."
        exit 1
    fi

    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment."
        exit 1
    fi
else
    echo "Virtual environment already exists."
fi

# 2. Activate Virtual Environment (OS-agnostic)
echo "Activating virtual environment..."
if [ -f "$VENV_DIR/bin/activate" ]; then
    # Linux/macOS
    source "$VENV_DIR/bin/activate"
elif [ -f "$VENV_DIR/Scripts/activate" ]; then
    # Windows
    source "$VENV_DIR/Scripts/activate"
else
    echo "Error: Could not find activation script."
    exit 1
fi

# 3. Install Dependencies
echo "Installing PyInstaller..."
pip install pyinstaller
if [ $? -ne 0 ]; then
    echo "Error: Failed to install PyInstaller."
    deactivate
    exit 1
fi

# 4. Deactivate Virtual Environment
echo "Deactivating virtual environment..."
deactivate

echo "--- Setup Successful ---"
echo "Project is now ready to be built with ./build.sh"
