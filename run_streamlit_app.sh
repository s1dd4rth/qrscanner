#!/bin/bash

# QR Frame Scanner - Streamlit App Launcher
echo "🚀 Starting QR Frame Scanner Web App"
echo "===================================="

# Activate virtual environment
source /Users/siddarth/qr_scanner_env/bin/activate

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit not found. Installing dependencies..."
    pip install -r /Users/siddarth/streamlit_requirements.txt
fi

echo "🌐 Launching Streamlit app..."
echo "📱 The app will open in your default browser"
echo "🔗 URL: http://localhost:8501"
echo ""
echo "💡 Upload an image with QR codes or use the camera to test the scanner!"
echo "📷 NEW: Live camera capture functionality available!"
echo "📤 Use Ctrl+C to stop the server"
echo ""

# Launch Streamlit app
streamlit run /Users/siddarth/streamlit_qr_app.py --server.address localhost --server.port 8501
