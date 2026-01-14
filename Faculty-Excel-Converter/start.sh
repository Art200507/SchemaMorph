#!/bin/bash

echo "======================================"
echo "SchemaMorph - Unified Startup"
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

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -q -r requirements.txt
echo "Python dependencies installed!"
echo ""

# Build React frontend
echo "======================================"
echo "Building React 3D Frontend..."
echo "======================================"
echo ""
cd frontend
if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install
fi
echo "Building frontend..."
npm run build
cd ..
echo "Frontend build complete!"
echo ""

# Start the unified application
echo "======================================"
echo "Starting Unified Application..."
echo "======================================"
echo ""
echo "Access the 3D UI at: http://localhost:5001"
echo "Press Ctrl+C to stop the server"
echo ""

python app.py
