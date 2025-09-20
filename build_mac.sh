#!/bin/bash

echo "Building SQLmap GUI for macOS..."

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

# Check if build was successful (macOS creates .app bundle)
if [ -d "dist/SQLmap-GUI.app" ]; then
    echo ""
    echo "✅ Build successful!"
    echo "App bundle created: dist/SQLmap-GUI.app"
    echo ""
    echo "To distribute:"
    echo "1. zip -r SQLmap-GUI-macos.zip dist/SQLmap-GUI.app"
    echo "2. Upload SQLmap-GUI-macos.zip to GitHub releases"
    echo ""
    echo "Creating distribution archive..."
    cd dist
    zip -r ../SQLmap-GUI-macos.zip SQLmap-GUI.app
    cd ..
    echo "Archive created: SQLmap-GUI-macos.zip"
    echo ""
    echo "Note: Users may need to right-click and select 'Open' the first time"
    echo "due to macOS security settings for unsigned applications."
elif [ -f "dist/SQLmap-GUI" ]; then
    echo ""
    echo "✅ Build successful!"
    echo "Executable created: dist/SQLmap-GUI"
    echo ""
    echo "Creating distribution archive..."
    tar -czf SQLmap-GUI-macos.tar.gz -C dist SQLmap-GUI
    echo "Archive created: SQLmap-GUI-macos.tar.gz"
else
    echo ""
    echo "❌ Build failed!"
    echo "Check the output above for errors."
    exit 1
fi