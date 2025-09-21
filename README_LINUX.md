# SQLmap GUI - Linux Installation Guide

## Quick Start (Automatic Installation)

### Option 1: One-Click Installer (Recommended)

1. Clone or download this repository
2. Run: `./install_linux.sh`
3. Follow the prompts - the installer will handle everything automatically

### Option 2: Enhanced Auto-Launcher (Advanced Users)

1. Open Terminal
2. Navigate to the SQLmap-GUI directory
3. Run: `./start_gui.sh`

### Option 3: PowerShell Alternative

For distributions with PowerShell Core installed:

```bash
pwsh -File start_gui.ps1
```

## What Gets Installed Automatically

### Python Installation

- **Detection**: Automatically detects Python 3.8+ installations
- **Installation**: Uses distribution package manager when needed
- **Distributions Supported**:
  - Ubuntu/Debian (apt)
  - Fedora (dnf)
  - CentOS/RHEL (yum)
  - Arch/Manjaro (pacman)
  - openSUSE/SLES (zypper)

### SQLmap Installation

- **Source**: Latest version from GitHub
- **Location**: `sqlmap-master/` in the script directory
- **Type**: Portable installation (no system changes)

### Python Dependencies

- **PyQt6**: GUI framework (>=6.5.0)
- **psutil**: System process monitoring (>=5.9.0)
- **requests**: HTTP library (>=2.28.0)
- **Virtual Environment**: Isolated environment in `.venv/`

### System Utilities

- **git**: Version control (for cloning)
- **unzip**: Archive extraction
- **wget/curl**: File downloading
- **python3-dev**: Python development headers
- **python3-venv**: Virtual environment support

## System Requirements

- **Operating System**: Linux with glibc 2.17+ (most modern distributions)
- **Architecture**: x86_64 (AMD64), ARM64 (AArch64) supported
- **RAM**: Minimum 2GB, Recommended 4GB
- **Storage**: 500MB free space
- **Internet**: Required for initial setup
- **Permissions**: Regular user with sudo access for package installation

## Supported Distributions

### Tier 1 Support (Fully Tested)

- **Ubuntu**: 18.04 LTS, 20.04 LTS, 22.04 LTS, 24.04 LTS
- **Debian**: 10 (Buster), 11 (Bullseye), 12 (Bookworm)
- **Fedora**: 36, 37, 38, 39, 40
- **CentOS**: 8, 9 (Stream)
- **RHEL**: 8, 9

### Tier 2 Support (Should Work)

- **Arch Linux**: Rolling release
- **Manjaro**: Stable, Testing
- **openSUSE**: Leap 15.x, Tumbleweed
- **SLES**: 15 SP3+
- **Pop!\_OS**: 20.04+, 22.04+
- **Linux Mint**: 20+, 21+

### Tier 3 Support (Manual Installation May Be Required)

- **Alpine Linux**: 3.15+
- **Void Linux**: Current
- **Gentoo**: Current
- **NixOS**: Current
- **Other**: Most glibc-based distributions

## Manual Installation (If Automatic Fails)

### 1. Install System Dependencies

#### Ubuntu/Debian:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv python3-dev git unzip wget
```

#### Fedora:

```bash
sudo dnf install python3 python3-pip python3-virtualenv python3-devel git unzip wget
```

#### CentOS/RHEL:

```bash
sudo yum install python3 python3-pip python3-virtualenv python3-devel git unzip wget
```

#### Arch/Manjaro:

```bash
sudo pacman -S python python-pip python-virtualenv git unzip wget
```

### 2. Install SQLmap

```bash
# Download and extract SQLmap
wget https://github.com/sqlmapproject/sqlmap/archive/master.zip
unzip master.zip
rm master.zip
```

### 3. Setup Python Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Run GUI

```bash
python main.py
```

## Troubleshooting

### Common Issues

#### 1. "sudo: command not found" or "User not in sudoers file"

**Solution**:

- Install sudo: `su -c "apt install sudo"` (Debian) or equivalent
- Add user to sudo group: `su -c "usermod -aG sudo $USER"`
- Log out and log back in

#### 2. "python3: command not found"

**Solution**:

```bash
# Ubuntu/Debian
sudo apt install python3

# Fedora
sudo dnf install python3

# CentOS/RHEL
sudo yum install python3
```

#### 3. "No module named 'venv'"

**Solution**:

```bash
# Ubuntu/Debian
sudo apt install python3-venv

# Fedora
sudo dnf install python3-virtualenv

# CentOS/RHEL
sudo yum install python3-virtualenv
```

#### 4. "Permission denied: ./start_gui.sh"

**Solution**:

```bash
chmod +x start_gui.sh install_linux.sh
./start_gui.sh
```

#### 5. "Package manager not found"

**Solution**: Install manually following the manual installation steps above

#### 6. "Failed to create virtual environment"

**Solution**:

```bash
# Try with virtualenv
pip3 install virtualenv
python3 -m virtualenv .venv
```

### Advanced Troubleshooting

#### Check Python Installation

```bash
python3 --version
python3 -m pip --version
which python3
```

#### Check PyQt6 Installation

```bash
source .venv/bin/activate
python -c "import PyQt6; print('PyQt6 is working')"
```

#### Check SQLmap

```bash
# If sqlmap is in PATH:
sqlmap --version

# If using local installation:
python sqlmap-master/sqlmap.py --version
```

#### Reset Installation

```bash
rm -rf .venv sqlmap-master
# Run installer again
./install_linux.sh
```

#### Debug Mode

```bash
# Enable verbose output
export SQLMAP_GUI_DEBUG=1
./start_gui.sh
```

## Configuration

### Custom Python Installation

If you have a specific Python version installed:

```bash
# Edit the script to use your Python
export PYTHON_CMD="/usr/local/bin/python3.11"
./start_gui.sh
```

### Custom SQLmap Location

If you have SQLmap installed elsewhere:

1. Edit `src/utils/config.py`
2. Set `SQLMAP_PATH` to your SQLmap location

### Proxy Configuration

For networks with proxy requirements:

```bash
export HTTP_PROXY=http://proxy:port
export HTTPS_PROXY=http://proxy:port
export PIP_PROXY=http://proxy:port
./start_gui.sh
```

### Desktop Integration

The installer creates desktop shortcuts automatically. For manual creation:

```bash
# Create desktop entry
cat > ~/.local/share/applications/sqlmap-gui.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=SQLmap GUI
Comment=Advanced SQL Injection Testing Interface
Exec=bash $(pwd)/start_gui.sh
Icon=$(pwd)/icon.png
Terminal=true
Categories=Development;Security;Network;
StartupNotify=true
Path=$(pwd)
EOF
```

## File Structure After Installation

```
SQLmap-GUI/
├── main.py                    # Main application entry
├── start_gui.sh              # Enhanced auto-launcher
├── install_linux.sh          # One-click installer
├── requirements.txt          # Python dependencies
├── .venv/                    # Virtual environment
│   ├── bin/
│   │   ├── activate          # Activation script
│   │   └── python            # Isolated Python
│   └── lib/                  # Python packages
├── sqlmap-master/            # SQLmap installation
│   ├── sqlmap.py            # SQLmap main script
│   └── lib/                 # SQLmap libraries
└── src/                     # Application source code
    ├── gui/                 # GUI components
    ├── core/                # Core functionality
    └── utils/               # Utilities
```

## Usage

### Starting the GUI

- **Auto-launcher**: `./start_gui.sh`
- **Desktop**: Click "SQLmap GUI" in applications menu
- **Manual**: `source .venv/bin/activate && python main.py`

### First Time Setup

1. The installer detects your system and installs requirements
2. All dependencies are managed in an isolated virtual environment
3. SQLmap is downloaded and configured automatically
4. Desktop shortcuts are created for easy access

## Administrator Requirements

### When Sudo is Required:

- **Initial Setup Only**: Installing system packages (Python, dev tools)
- **Package Management**: Using distribution package managers
- **System Dependencies**: Installing git, unzip, wget if missing

### When Sudo is NOT Required:

- **Normal Operation**: Running the GUI as regular user
- **Virtual Environment**: All Python packages installed in user space
- **Configuration**: All settings stored in user directories
- **SQLmap Usage**: Runs in portable mode

### Security Model:

- **Minimal Elevation**: Sudo only for system package installation
- **User Isolation**: Virtual environment prevents system-wide changes
- **Portable Setup**: Can be moved to other systems
- **No Persistent Changes**: Easy to uninstall by deleting folder

## Uninstallation

### Remove SQLmap GUI

```bash
# Delete the entire SQLmap-GUI folder
rm -rf SQLmap-GUI
```

### Remove System Packages (Optional)

```bash
# Only if you want to remove Python (not recommended)
# Ubuntu/Debian:
sudo apt remove python3 python3-pip python3-venv

# Note: This may break other Python applications
```

### Remove Desktop Integration

```bash
rm ~/.local/share/applications/sqlmap-gui.desktop
rm ~/Desktop/SQLmap\ GUI.desktop
```

## Performance Tips

- **SSD Storage**: Install on SSD for better performance
- **RAM**: 4GB+ recommended for large scan operations
- **CPU**: Multi-core systems handle concurrent scans better
- **Network**: Stable internet connection for SQLmap operations
- **Firewall**: Ensure Python can make outbound connections

## Security Notes

- All downloads are from official sources (GitHub, distribution repos)
- Virtual environment isolates dependencies from system Python
- SQLmap runs in portable mode (no system installation)
- Regular user privileges sufficient for normal operation
- No permanent system modifications (except optional package installation)

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Run with debug mode: `SQLMAP_GUI_DEBUG=1 ./start_gui.sh`
3. Check the main project documentation
4. Report issues on the GitHub repository

## Distribution-Specific Notes

### Ubuntu/Debian

- Works out of the box on most versions
- `python3-venv` package required for virtual environments
- May need `python3-dev` for some PyQt6 installations

### Fedora

- Uses `dnf` package manager
- `python3-virtualenv` instead of `python3-venv`
- Generally excellent compatibility

### CentOS/RHEL

- May need EPEL repository for some packages
- Older versions might need manual Python 3.8+ installation
- Consider using `python39` or `python311` packages

### Arch Linux

- Rolling release ensures latest packages
- `python-virtualenv` package name differs
- Excellent compatibility with latest software

### Alpine Linux

- Lightweight distribution may need additional packages
- `musl` libc instead of `glibc` may cause issues
- Consider using the manual installation method
