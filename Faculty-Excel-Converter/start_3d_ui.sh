#!/bin/bash

echo "🚀 Starting Faculty Excel Converter with Futuristic 3D UI..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -q -r requirements.txt

# Build frontend if dist doesn't exist
if [ ! -d "frontend/dist" ]; then
    echo "🏗️  Building frontend..."
    cd frontend
    npm install --legacy-peer-deps
    npm run build
    cd ..
fi

echo ""
echo "✨ Starting server on http://localhost:8080"
echo "Press Ctrl+C to stop"
echo ""

# Run the Flask application
python app_api.py
