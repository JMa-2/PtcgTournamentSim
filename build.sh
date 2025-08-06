#!/bin/bash

# This script builds the PtcgTournamentSim application for the current platform.

# --- Configuration ---
# Main script to be bundled
MAIN_SCRIPT="src/main.py"

# Virtual environment directory
VENV_DIR="venv"

# Output directory for the final executable
DIST_DIR="dist"

# --- Build Process ---
echo "--- Starting PtcgTournamentSim Build ---"

# 1. Activate Virtual Environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"
if [ $? -ne 0 ]; then
    echo "Error: Failed to activate virtual environment. Make sure it exists at '$VENV_DIR'."
    exit 1
fi

# 2. Generate Dynamic Filename
# Format: PtcgSim_YYYYMMDD_HHMMSS
FILENAME="PtcgSim_$(date +'%Y%m%d_%H%M%S')"
echo "Generated executable name: $FILENAME"

# 3. Run PyInstaller
echo "Running PyInstaller..."
pyinstaller \
    --name "$FILENAME" \
    --onefile \
    --noconsole \
    --distpath "$DIST_DIR" \
    "$MAIN_SCRIPT"

if [ $? -ne 0 ]; then
    echo "Error: PyInstaller build failed."
    deactivate
    exit 1
fi

# 4. Deactivate Virtual Environment
echo "Deactivating virtual environment..."
deactivate

echo "--- Build Successful ---"
echo "Executable created at: $DIST_DIR/$FILENAME"
