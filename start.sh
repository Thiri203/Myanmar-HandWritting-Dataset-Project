#!/bin/bash

# Myanmar Syllable Handwritten Collector - Quick Start
# This script starts the Flask server on your Mac

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8 or later."
    exit 1
fi

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "📦 Installing Flask..."
    pip3 install -q Flask==2.3.2 Werkzeug==2.3.6
    echo "✓ Flask installed"
fi

# Get local IP
echo ""
echo "🔍 Finding your Mac's IP address..."

# Try to get WiFi IP
IP=$(ifconfig | grep -A1 "en0:" | grep "inet " | awk '{print $2}' 2>/dev/null || echo "")

if [ -z "$IP" ]; then
    IP=$(hostname -I 2>/dev/null || echo "localhost")
fi

echo ""
echo "════════════════════════════════════════════════════"
echo "  Myanmar Syllable Handwritten Collector - Web"
echo "════════════════════════════════════════════════════"
echo ""
echo "✓ Server starting on: http://localhost:5001"
echo ""
echo "📱 To access from iPad:"
echo "   1. Connect to same WiFi as this Mac"
echo "   2. Make sure Mac and iPad are on same network"
echo "   3. Open browser on iPad"
echo "   4. Go to: http://$IP:5001"
echo ""
echo "📊 Data saved to: $SCRIPT_DIR/dataset/"
echo ""
echo "Note: Press Ctrl+C to stop the server"
echo ""
echo "════════════════════════════════════════════════════"
echo ""

# Start Flask
python3 app.py
