#!/bin/bash

# QR Frame Scanner - Easy Run Script
# This script activates the virtual environment and runs the QR scanner

echo "🔍 QR Frame Scanner"
echo "=================="

# Activate virtual environment
source /Users/siddarth/qr_scanner_env/bin/activate

# Check if arguments were provided
if [ $# -eq 0 ]; then
    echo "📖 Usage examples:"
    echo ""
    echo "Scan from camera (live):"
    echo "  ./run_qr_scanner.sh -l --pretty"
    echo ""
    echo "Scan from image file:"
    echo "  ./run_qr_scanner.sh -i your_image.jpg --pretty"
    echo ""
    echo "Save results to file:"
    echo "  ./run_qr_scanner.sh -i image.jpg -o results.json --pretty"
    echo ""
    echo "Show help:"
    echo "  ./run_qr_scanner.sh --help"
    echo ""
    echo "💡 Note: Press 's' to scan when using live camera mode, 'q' to quit"
else
    # Run the QR scanner with provided arguments
    python /Users/siddarth/qr_frame_scanner.py "$@"
fi

echo ""
echo "✅ QR Scanner session complete"
