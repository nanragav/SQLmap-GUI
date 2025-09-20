#!/bin/bash

echo "Building SQLmap GUI for macOS (cross-platform compatible)..."

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

# Create a macOS-compatible spec file
cat > sqlmap_gui_mac.spec << 'EOF'
# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Get application info
app_name = 'SQLmap-GUI'
main_script = 'main.py'

# Collect all data files and submodules
datas = []
datas += collect_data_files('PyQt6')

# Add source code directories
datas += [('src', 'src')]

# Collect hidden imports
hiddenimports = []
hiddenimports += collect_submodules('PyQt6')
hiddenimports += [
    'PyQt6.QtCore',
    'PyQt6.QtGui', 
    'PyQt6.QtWidgets',
    'configparser',
    'psutil',
    'colorlog',
    'requests',
    'pathlib2',
    'qdarkstyle'
]

a = Analysis(
    [main_script],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=app_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=app_name,
)
EOF

# Build executable
echo "Building macOS-compatible executable..."
pyinstaller sqlmap_gui_mac.spec

# Check if build was successful
if [ -f "dist/SQLmap-GUI/SQLmap-GUI" ]; then
    echo ""
    echo "✅ Build successful!"
    echo "Executable created: dist/SQLmap-GUI/SQLmap-GUI"
    echo ""
    echo "Creating macOS distribution archive..."
    
    # Create a proper macOS directory structure
    mkdir -p dist/SQLmap-GUI-macOS/SQLmap-GUI.app/Contents/MacOS
    mkdir -p dist/SQLmap-GUI-macOS/SQLmap-GUI.app/Contents/Resources
    
    # Copy the executable
    cp -r dist/SQLmap-GUI/* dist/SQLmap-GUI-macOS/SQLmap-GUI.app/Contents/MacOS/
    
    # Create Info.plist for macOS app bundle
    cat > dist/SQLmap-GUI-macOS/SQLmap-GUI.app/Contents/Info.plist << 'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>SQLmap-GUI</string>
    <key>CFBundleIdentifier</key>
    <string>com.nanragav.sqlmap-gui</string>
    <key>CFBundleName</key>
    <string>SQLmap-GUI</string>
    <key>CFBundleDisplayName</key>
    <string>SQLmap GUI</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>NSRequiresAquaSystemAppearance</key>
    <false/>
</dict>
</plist>
PLIST
    
    # Create launcher script for easier execution
    cat > dist/SQLmap-GUI-macOS/SQLmap-GUI.app/Contents/MacOS/SQLmap-GUI-launcher << 'LAUNCHER'
#!/bin/bash
# Get the directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
# Execute the main application
exec "$DIR/SQLmap-GUI" "$@"
LAUNCHER
    
    chmod +x dist/SQLmap-GUI-macOS/SQLmap-GUI.app/Contents/MacOS/SQLmap-GUI-launcher
    chmod +x dist/SQLmap-GUI-macOS/SQLmap-GUI.app/Contents/MacOS/SQLmap-GUI
    
    # Create README for Mac users
    cat > dist/SQLmap-GUI-macOS/README-macOS.txt << 'README'
SQLmap GUI for macOS
===================

Installation Instructions:
1. Extract this archive
2. Copy SQLmap-GUI.app to your Applications folder (optional)
3. Right-click on SQLmap-GUI.app and select "Open" 
4. Click "Open" when macOS asks about running an app from an unidentified developer

Note: The first time you run the app, macOS may show a security warning because 
the app is not signed with an Apple Developer certificate. This is normal for 
open-source applications.

If you encounter issues:
- Make sure you have sqlmap installed on your system
- Check that Python 3.8+ is available
- Ensure you have necessary permissions to run the application

For support, visit: https://github.com/nanragav/SQLmap-GUI
README
    
    # Create the archive
    cd dist
    tar -czf SQLmap-GUI-macOS.tar.gz SQLmap-GUI-macOS/
    cd ..
    mv dist/SQLmap-GUI-macOS.tar.gz ./
    
    echo "Archive created: SQLmap-GUI-macOS.tar.gz"
    echo ""
    echo "Mac users should:"
    echo "1. Download and extract SQLmap-GUI-macOS.tar.gz"
    echo "2. Copy SQLmap-GUI.app to Applications folder"
    echo "3. Right-click and select 'Open' the first time"
else
    echo ""
    echo "❌ Build failed!"
    echo "Check the output above for errors."
    exit 1
fi
