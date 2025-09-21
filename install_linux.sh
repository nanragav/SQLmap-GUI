#!/bin/bash

# SQLmap GUI Linux Installer
# Run this script to automatically set up everything needed for SQLmap GUI

echo "============================================"
echo "    SQLmap GUI Linux Installer"
echo "============================================"
echo
echo "This installer will:"
echo "- Check and install Python if needed"
echo "- Download and setup SQLmap"
echo "- Install required Python packages"
echo "- Create desktop shortcuts"
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Ask for confirmation
read -p "Do you want to continue? (Y/n): " continue_install
if [[ $continue_install =~ ^[Nn]$ ]]; then
    echo "Installation cancelled."
    exit 0
fi

echo
print_info "Starting installation..."

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESKTOP_DIR="$HOME/Desktop"

# Run the main setup script
echo
print_info "Running main setup script..."
bash "$SCRIPT_DIR/start_gui.sh"

if [ $? -ne 0 ]; then
    echo
    print_error "Installation encountered errors."
    exit 1
fi

echo
echo "============================================"
print_info "Creating desktop shortcuts..."

# Create launcher script
LAUNCHER="$SCRIPT_DIR/SQLmap_GUI.sh"
cat > "$LAUNCHER" << 'EOF'
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
bash start_gui.sh
EOF

chmod +x "$LAUNCHER"

# Create desktop entry
if [ -d "$DESKTOP_DIR" ]; then
    DESKTOP_FILE="$DESKTOP_DIR/SQLmap GUI.desktop"
    cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=SQLmap GUI
Comment=SQL Injection Testing Tool
Exec=bash $LAUNCHER
Icon=$SCRIPT_DIR/icon.png
Terminal=true
Categories=Development;Security;
StartupNotify=true
Path=$SCRIPT_DIR
EOF
    
    chmod +x "$DESKTOP_FILE"
    
    if [ -f "$DESKTOP_FILE" ]; then
        print_status "Desktop shortcut created"
    else
        print_error "Failed to create desktop shortcut"
    fi
else
    print_info "Desktop directory not found, skipping shortcut creation"
fi

# Create menu entry for supported desktop environments
APPLICATIONS_DIR="$HOME/.local/share/applications"
if [ -d "$APPLICATIONS_DIR" ] || mkdir -p "$APPLICATIONS_DIR"; then
    MENU_FILE="$APPLICATIONS_DIR/sqlmap-gui.desktop"
    cat > "$MENU_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=SQLmap GUI
Comment=Advanced SQL Injection Testing Interface
Exec=bash $LAUNCHER
Icon=$SCRIPT_DIR/icon.png
Terminal=true
Categories=Development;Security;Network;
StartupNotify=true
Path=$SCRIPT_DIR
Keywords=sql;injection;testing;security;penetration;
EOF
    
    chmod +x "$MENU_FILE"
    print_status "Application menu entry created"
fi

echo
echo "============================================"
print_status "Installation completed successfully!"
echo
echo "You can now:"
echo "1. Double-click 'SQLmap GUI' on your desktop"
echo "2. Run './start_gui.sh' from this directory"
echo "3. Find 'SQLmap GUI' in your applications menu"
echo
echo "The GUI will automatically:"
echo "- Detect and use your installed Python"
echo "- Use the downloaded SQLmap"
echo "- Manage dependencies in a virtual environment"
echo
echo "Note: No administrator privileges are required for normal operation."
echo "System packages are only installed when Python/dependencies are missing."
echo