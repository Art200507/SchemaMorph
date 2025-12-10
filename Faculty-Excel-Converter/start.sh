#!/bin/bash

echo "======================================"
echo "Faculty Excel Converter - Startup"
echo "======================================"
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created!"
    echo ""
fi

# Activate venv
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt
echo "Dependencies installed!"
echo ""

# Start the application
echo "======================================"
echo "Starting Flask application..."
echo "======================================"
echo ""
echo "Access the application at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""

python app.py
