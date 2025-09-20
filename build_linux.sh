#!/bin/bash

echo "Building SQLmap GUI for Linux..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf dist build

# Build executable
echo "Building executable..."
pyinstaller sqlmap_gui.spec

# Check if build was successful
if [ -f "dist/SQLmap-GUI" ]; then
    echo ""
    echo "✅ Build successful!"
    echo "Executable created: dist/SQLmap-GUI"
    echo ""
    echo "To distribute:"
    echo "1. tar -czf SQLmap-GUI-linux.tar.gz -C dist SQLmap-GUI"
    echo "2. Upload SQLmap-GUI-linux.tar.gz to GitHub releases"
    echo ""
    echo "Creating distribution archive..."
    tar -czf SQLmap-GUI-linux.tar.gz -C dist SQLmap-GUI
    echo "Archive created: SQLmap-GUI-linux.tar.gz"
else
    echo ""
    echo "❌ Build failed!"
    echo "Check the output above for errors."
    exit 1
fi