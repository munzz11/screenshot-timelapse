#!/bin/bash

# Simple Timelapse Generator
# Usage: ./simple_timelapse.sh <screenshots_path>

set -e

# Check if path is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <screenshots_path>"
    echo "Example: $0 /path/to/screenshots"
    exit 1
fi

SCREENSHOTS_PATH="$1"

# Check if path exists
if [ ! -d "$SCREENSHOTS_PATH" ]; then
    echo "Error: Path does not exist: $SCREENSHOTS_PATH"
    exit 1
fi

# Check if Python and required packages are available
if ! python3 -c "import cv2, tqdm" 2>/dev/null; then
    echo "Installing required packages..."
    pip3 install -r simple_requirements.txt
fi

# Run the timelapse generator
echo "Starting timelapse generation..."
python3 simple_timelapse.py "$SCREENSHOTS_PATH"

echo "Done!" 