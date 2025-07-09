#!/bin/bash

# QR Frame Scanner - Mobile Demo Setup
echo "📱 Setting up QR Frame Scanner for Mobile Testing"
echo "================================================="

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "⚠️  ngrok not found. Installing via Homebrew..."
    if command -v brew &> /dev/null; then
        brew install ngrok
    else
        echo "❌ Homebrew not found. Please install ngrok manually:"
        echo "   Visit: https://ngrok.com/download"
        echo "   Or install Homebrew first: https://brew.sh"
        exit 1
    fi
fi

echo "✅ ngrok found"

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source /Users/siddarth/qr_scanner_env/bin/activate

# Start Streamlit in background
echo "🚀 Starting Streamlit app..."
streamlit run /Users/siddarth/streamlit_qr_app.py --server.headless true --server.port 8501 &
STREAMLIT_PID=$!

# Wait for Streamlit to start
echo "⏳ Waiting for Streamlit to start..."
sleep 5

# Start ngrok tunnel
echo "🌐 Creating HTTPS tunnel with ngrok..."
ngrok http 8501 &
NGROK_PID=$!

# Wait for ngrok to start
sleep 3

echo ""
echo "🎉 Mobile Demo Setup Complete!"
echo "=============================="
echo ""
echo "📱 HTTPS URL for mobile testing:"
echo "   Check ngrok output above for the HTTPS URL"
echo "   Example: https://abc123.ngrok.io"
echo ""
echo "📋 Mobile Testing Steps:"
echo "   1. Copy the HTTPS URL from ngrok output"
echo "   2. Open URL on your mobile device"
echo "   3. Select '📷 Live Camera Capture'"
echo "   4. Allow camera permission when prompted"
echo "   5. Position QR codes in camera view"
echo "   6. Tap capture to scan!"
echo ""
echo "🔧 To stop the demo:"
echo "   Press Ctrl+C to stop this script"
echo "   Or run: kill $STREAMLIT_PID $NGROK_PID"
echo ""
echo "💡 Troubleshooting:"
echo "   - Ensure good lighting for QR codes"
echo "   - Hold device steady when capturing"
echo "   - Use landscape mode for wide frames"
echo "   - Check browser supports camera (Chrome/Safari recommended)"

# Keep script running
echo ""
echo "🏃 Demo is running... Press Ctrl+C to stop"
wait
