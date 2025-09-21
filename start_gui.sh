#!/bin/bash

# SQLmap GUI Launcher Script for Linux
# This script automatically installs Python, SQLmap, and dependencies if needed

echo "Starting SQLmap GUI for Linux..."
echo

# Set variables
PYTHON_MIN_VERSION="3.8"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"
SQLMAP_DIR="$SCRIPT_DIR/sqlmap-master"
SQLMAP_URL="https://github.com/sqlmapproject/sqlmap/archive/master.zip"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to compare version numbers
version_greater_equal() {
    printf '%s\n%s\n' "$2" "$1" | sort -V -C
}

# Function to detect Linux distribution
detect_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        DISTRO=$ID
        VERSION=$VERSION_ID
    elif [ -f /etc/redhat-release ]; then
        DISTRO="rhel"
    elif [ -f /etc/debian_version ]; then
        DISTRO="debian"
    else
        DISTRO="unknown"
    fi
}

# Function to install Python on different distributions
install_python() {
    print_info "Installing Python..."
    
    detect_distro
    
    case $DISTRO in
        "ubuntu"|"debian")
            if command_exists apt; then
                echo "Updating package list..."
                sudo apt update
                echo "Installing Python and dependencies..."
                sudo apt install -y python3 python3-pip python3-venv python3-dev
            else
                print_error "apt package manager not found"
                return 1
            fi
            ;;
        "fedora")
            if command_exists dnf; then
                echo "Installing Python and dependencies..."
                sudo dnf install -y python3 python3-pip python3-virtualenv python3-devel
            else
                print_error "dnf package manager not found"
                return 1
            fi
            ;;
        "centos"|"rhel")
            if command_exists yum; then
                echo "Installing Python and dependencies..."
                sudo yum install -y python3 python3-pip python3-virtualenv python3-devel
            else
                print_error "yum package manager not found"
                return 1
            fi
            ;;
        "arch"|"manjaro")
            if command_exists pacman; then
                echo "Installing Python and dependencies..."
                sudo pacman -S --noconfirm python python-pip python-virtualenv
            else
                print_error "pacman package manager not found"
                return 1
            fi
            ;;
        "opensuse"|"sles")
            if command_exists zypper; then
                echo "Installing Python and dependencies..."
                sudo zypper install -y python3 python3-pip python3-virtualenv python3-devel
            else
                print_error "zypper package manager not found"
                return 1
            fi
            ;;
        *)
            print_error "Unsupported distribution: $DISTRO"
            print_info "Please install Python 3.8+ manually and run this script again"
            return 1
            ;;
    esac
}

# Function to check Python installation
check_python() {
    print_info "Checking for Python installation..."
    
    PYTHON_CMD=""
    
    # Check for python3 command
    if command_exists python3; then
        PYTHON_CMD="python3"
        print_status "Python3 found"
    elif command_exists python; then
        # Check if python points to Python 3
        PYTHON_VERSION=$(python --version 2>&1 | cut -d' ' -f2)
        if [[ $PYTHON_VERSION == 3.* ]]; then
            PYTHON_CMD="python"
            print_status "Python found"
        else
            print_error "Python 2 detected. Python 3 is required."
            return 1
        fi
    else
        print_error "Python not found"
        return 1
    fi
    
    # Check Python version
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
    print_info "Current Python version: $PYTHON_VERSION"
    
    if version_greater_equal "$PYTHON_VERSION" "$PYTHON_MIN_VERSION"; then
        print_status "Python version is compatible ($PYTHON_MIN_VERSION+)"
        return 0
    else
        print_error "Python version is too old (need $PYTHON_MIN_VERSION+)"
        return 1
    fi
}

# Function to install SQLmap
install_sqlmap() {
    print_info "Installing SQLmap..."
    
    # Check if wget or curl is available
    if command_exists wget; then
        DOWNLOAD_CMD="wget -O"
    elif command_exists curl; then
        DOWNLOAD_CMD="curl -L -o"
    else
        print_error "Neither wget nor curl found. Installing wget..."
        detect_distro
        case $DISTRO in
            "ubuntu"|"debian")
                sudo apt install -y wget
                ;;
            "fedora")
                sudo dnf install -y wget
                ;;
            "centos"|"rhel")
                sudo yum install -y wget
                ;;
            "arch"|"manjaro")
                sudo pacman -S --noconfirm wget
                ;;
            *)
                print_error "Cannot install wget automatically"
                return 1
                ;;
        esac
        DOWNLOAD_CMD="wget -O"
    fi
    
    # Create temp directory
    TEMP_DIR=$(mktemp -d)
    cd "$TEMP_DIR"
    
    # Download SQLmap
    print_info "Downloading SQLmap..."
    $DOWNLOAD_CMD sqlmap.zip "$SQLMAP_URL"
    
    if [ $? -ne 0 ]; then
        print_error "Failed to download SQLmap"
        return 1
    fi
    
    # Check if unzip is available
    if ! command_exists unzip; then
        print_info "Installing unzip..."
        case $DISTRO in
            "ubuntu"|"debian")
                sudo apt install -y unzip
                ;;
            "fedora")
                sudo dnf install -y unzip
                ;;
            "centos"|"rhel")
                sudo yum install -y unzip
                ;;
            "arch"|"manjaro")
                sudo pacman -S --noconfirm unzip
                ;;
        esac
    fi
    
    # Extract SQLmap
    print_info "Extracting SQLmap..."
    unzip -q sqlmap.zip
    
    if [ -d "sqlmap-master" ]; then
        # Remove existing sqlmap directory if it exists
        if [ -d "$SQLMAP_DIR" ]; then
            rm -rf "$SQLMAP_DIR"
        fi
        
        # Move to script directory
        mv sqlmap-master "$SQLMAP_DIR"
        print_status "SQLmap installed successfully"
        
        # Make sqlmap.py executable
        chmod +x "$SQLMAP_DIR/sqlmap.py"
    else
        print_error "Failed to extract SQLmap"
        return 1
    fi
    
    # Clean up
    cd "$SCRIPT_DIR"
    rm -rf "$TEMP_DIR"
    
    return 0
}

# Function to check for SQLmap
check_sqlmap() {
    print_info "Checking for SQLmap..."
    
    # Check if sqlmap is in PATH
    if command_exists sqlmap; then
        print_status "SQLmap found in PATH"
        return 0
    fi
    
    # Check if sqlmap.py exists in script directory
    if [ -f "$SCRIPT_DIR/sqlmap.py" ]; then
        print_status "SQLmap found in script directory"
        return 0
    fi
    
    # Check if sqlmap-master directory exists
    if [ -f "$SQLMAP_DIR/sqlmap.py" ]; then
        print_status "SQLmap found in sqlmap-master directory"
        return 0
    fi
    
    print_error "SQLmap not found"
    return 1
}

# Function to setup virtual environment
setup_venv() {
    print_info "Setting up virtual environment..."
    
    if [ -d "$VENV_DIR" ]; then
        print_status "Virtual environment already exists"
    else
        print_info "Creating virtual environment..."
        $PYTHON_CMD -m venv "$VENV_DIR"
        
        if [ $? -ne 0 ]; then
            print_error "Failed to create virtual environment"
            print_info "Trying with virtualenv..."
            
            # Try installing virtualenv
            $PYTHON_CMD -m pip install virtualenv
            $PYTHON_CMD -m virtualenv "$VENV_DIR"
            
            if [ $? -ne 0 ]; then
                print_error "Failed to create virtual environment"
                return 1
            fi
        fi
        
        print_status "Virtual environment created"
    fi
    
    # Activate virtual environment
    print_info "Activating virtual environment..."
    source "$VENV_DIR/bin/activate"
    
    if [ $? -eq 0 ]; then
        print_status "Virtual environment activated"
    else
        print_error "Failed to activate virtual environment"
        return 1
    fi
    
    return 0
}

# Function to install Python dependencies
install_dependencies() {
    print_info "Installing Python dependencies..."
    
    # Create requirements.txt if it doesn't exist
    if [ ! -f "$SCRIPT_DIR/requirements.txt" ]; then
        print_info "Creating requirements.txt..."
        cat > "$SCRIPT_DIR/requirements.txt" << EOF
PyQt6>=6.5.0
psutil>=5.9.0
requests>=2.28.0
EOF
    fi
    
    # Upgrade pip
    python -m pip install --upgrade pip
    
    # Install dependencies
    python -m pip install -r "$SCRIPT_DIR/requirements.txt"
    
    if [ $? -ne 0 ]; then
        print_error "Failed to install dependencies from requirements.txt"
        print_info "Trying individual installations..."
        
        python -m pip install PyQt6
        python -m pip install psutil
        python -m pip install requests
    fi
    
    # Verify PyQt6 installation
    python -c "import PyQt6" 2>/dev/null
    if [ $? -eq 0 ]; then
        print_status "Dependencies installed successfully"
    else
        print_error "Failed to install PyQt6"
        print_info "Trying alternative installation..."
        
        python -m pip install PyQt6 --index-url https://pypi.org/simple/
        python -c "import PyQt6" 2>/dev/null
        
        if [ $? -ne 0 ]; then
            print_error "Failed to install PyQt6. Please install manually."
            return 1
        else
            print_status "PyQt6 installed successfully"
        fi
    fi
    
    return 0
}

# Main execution flow
main() {
    echo "============================================"
    echo "    SQLmap GUI Auto-Setup for Linux"
    echo "============================================"
    echo
    
    # Check if running as root
    if [ "$EUID" -eq 0 ]; then
        print_warning "Running as root detected"
        print_info "This script will install system packages using sudo when needed"
        print_info "The virtual environment and GUI will run as regular user"
        echo
    fi
    
    # Check and install Python
    if ! check_python; then
        print_info "Python installation required"
        if install_python; then
            # Recheck Python after installation
            if ! check_python; then
                print_error "Python installation failed"
                exit 1
            fi
        else
            print_error "Failed to install Python"
            exit 1
        fi
    fi
    
    # Check and install SQLmap
    if ! check_sqlmap; then
        if install_sqlmap; then
            print_status "SQLmap setup completed"
        else
            print_error "Failed to install SQLmap"
            exit 1
        fi
    fi
    
    # Setup virtual environment
    if setup_venv; then
        print_status "Virtual environment setup completed"
    else
        print_error "Virtual environment setup failed"
        exit 1
    fi
    
    # Install dependencies
    if install_dependencies; then
        print_status "Dependencies installation completed"
    else
        print_error "Dependencies installation failed"
        exit 1
    fi
    
    # Launch GUI
    echo
    print_info "Launching SQLmap GUI..."
    echo
    
    if [ -f "$SCRIPT_DIR/main.py" ]; then
        python "$SCRIPT_DIR/main.py"
        
        if [ $? -eq 0 ]; then
            echo
            print_status "SQLmap GUI closed successfully"
        else
            echo
            print_error "SQLmap GUI encountered an error"
            print_info "Check the error messages above for details"
        fi
    else
        print_error "main.py not found in script directory"
        exit 1
    fi
}

# Run main function
main "$@"
