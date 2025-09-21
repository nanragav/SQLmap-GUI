# Auto-Installation Scripts Guide

This document explains the automatic installation scripts for SQLmap GUI and their administrator requirements.

## 📋 Overview

SQLmap GUI provides automated installation scripts for both Linux and Windows that handle all dependencies automatically:

- **Linux**: `install_linux.sh` and `start_gui.sh`
- **Windows**: `install_windows.bat` and `start_gui.ps1`

## 🐧 Linux Scripts

### `install_linux.sh` - One-Click Installer

**Purpose**: Complete setup wizard with user-friendly interface

**Features**:

- Runs the enhanced `start_gui.sh` script
- Creates desktop shortcuts
- Creates application menu entries
- Provides installation summary

**Usage**:

```bash
./install_linux.sh
```

### `start_gui.sh` - Enhanced Auto-Launcher

**Purpose**: Intelligent dependency detection and installation

**Features**:

- **Python Detection**: Checks for Python 3.8+ compatibility
- **Automatic Installation**: Installs Python if missing or incompatible
- **SQLmap Management**: Downloads and installs SQLmap automatically
- **Virtual Environment**: Creates isolated Python environment
- **Dependency Management**: Installs PyQt6, psutil, requests
- **Distribution Support**: Ubuntu, Debian, Fedora, CentOS, RHEL, Arch, openSUSE
- **Error Recovery**: Multiple fallback methods for installations

**Distribution Detection**:

- Ubuntu/Debian → `apt install`
- Fedora → `dnf install`
- CentOS/RHEL → `yum install`
- Arch/Manjaro → `pacman -S`
- openSUSE → `zypper install`

**Usage**:

```bash
./start_gui.sh
```

## 🪟 Windows Scripts

### `install_windows.bat` - One-Click Installer

**Purpose**: User-friendly installation wizard

**Features**:

- Runs the main setup script
- Creates desktop shortcuts
- Creates launcher scripts
- Installation confirmation

**Usage**:

```cmd
install_windows.bat
```

### `start_gui.bat` - Batch Auto-Launcher

**Purpose**: Automatic dependency management for Windows

**Features**:

- Python version detection and installation
- SQLmap download and setup
- Virtual environment creation
- Dependency installation with fallbacks
- Environment variable refresh

**Usage**:

```cmd
start_gui.bat
```

### `start_gui.ps1` - PowerShell Auto-Launcher

**Purpose**: Advanced Windows installation with better error handling

**Features**:

- Enhanced download progress tracking
- Colored output and status indicators
- Force reinstall option (`-Force`)
- Better error recovery
- PowerShell execution policy handling

**Usage**:

```powershell
.\start_gui.ps1
# Or with force reinstall:
.\start_gui.ps1 -Force
```

## 🔐 Administrator Requirements

### Linux Systems

#### When Sudo is Required:

1. **Python Installation** (if not present or too old):

   ```bash
   sudo apt install python3 python3-pip python3-venv python3-dev  # Ubuntu/Debian
   sudo dnf install python3 python3-pip python3-virtualenv        # Fedora
   sudo yum install python3 python3-pip python3-virtualenv        # CentOS/RHEL
   sudo pacman -S python python-pip python-virtualenv             # Arch
   ```

2. **System Utilities** (if not present):
   ```bash
   sudo apt install git unzip wget  # Ubuntu/Debian
   ```

#### When Sudo is NOT Required:

- Virtual environment creation (user space)
- Python package installation (virtual environment)
- SQLmap download and setup (user directory)
- GUI execution (regular user)
- Configuration and settings

#### Security Model:

- **One-time Setup**: System packages installed with sudo
- **Ongoing Use**: Everything runs as regular user
- **Isolation**: Virtual environment prevents system-wide changes
- **Portability**: Can be moved between systems without reinstallation

### Windows Systems

#### No Administrator Rights Needed:

- **Python Installation**: Installs to user profile (`%USERPROFILE%\AppData\Local\Programs\Python`)
- **SQLmap Setup**: Downloads to application directory
- **Dependencies**: Installed in virtual environment
- **Shortcuts**: Created in user's desktop and start menu

#### What Gets Modified:

- **User PATH**: Python added to user PATH (not system-wide)
- **File Associations**: Python file associations (user-level)
- **Desktop**: Shortcut creation
- **No System Changes**: No modifications to system directories

#### Security Model:

- **User-Scoped**: All installations in user directories
- **Portable**: Can be copied to other systems
- **No Elevation**: Standard user privileges sufficient
- **Reversible**: Uninstall by deleting folder

## 🚀 Installation Flow

### Linux Installation Process:

1. **System Check**: Detect Linux distribution
2. **Python Check**: Verify Python 3.8+ availability
3. **Package Installation**: Install missing system packages (requires sudo)
4. **SQLmap Setup**: Download and extract SQLmap (user space)
5. **Virtual Environment**: Create Python virtual environment (user space)
6. **Dependencies**: Install Python packages (virtual environment)
7. **Launch**: Start GUI application (regular user)

### Windows Installation Process:

1. **Python Check**: Verify Python installation and version
2. **Python Install**: Download and install Python if needed (user space)
3. **SQLmap Setup**: Download and extract SQLmap (user space)
4. **Virtual Environment**: Create Python virtual environment (user space)
5. **Dependencies**: Install Python packages (virtual environment)
6. **Shortcuts**: Create desktop and menu shortcuts
7. **Launch**: Start GUI application (regular user)

## 🛠️ Troubleshooting

### Linux Issues

#### "Permission denied when installing packages"

**Solution**: Run script as regular user, it will prompt for sudo when needed:

```bash
./start_gui.sh  # Will ask for sudo password when needed
```

#### "Distribution not supported"

**Solution**: Install Python manually, then run script:

```bash
# Install Python 3.8+ for your distribution
./start_gui.sh  # Will detect existing Python
```

### Windows Issues

#### "Execution Policy" error in PowerShell

**Solution**: Allow script execution for current session:

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\start_gui.ps1
```

#### "Download failed" errors

**Solution**: Check internet connection and try again, or install manually:

- Download Python from python.org
- Download SQLmap from GitHub
- Run script again

## 📊 Comparison Matrix

| Feature              | Linux Auto            | Windows Auto          | Manual Install |
| -------------------- | --------------------- | --------------------- | -------------- |
| Python Install       | ✅ Auto               | ✅ Auto               | ❌ Manual      |
| SQLmap Install       | ✅ Auto               | ✅ Auto               | ❌ Manual      |
| Dependencies         | ✅ Auto               | ✅ Auto               | ❌ Manual      |
| Shortcuts            | ✅ Auto               | ✅ Auto               | ❌ Manual      |
| Updates              | ✅ Auto               | ✅ Auto               | ❌ Manual      |
| Sudo Required        | ⚠️ Initial Only       | ❌ Never              | ⚠️ Varies      |
| Distribution Support | ✅ 6+ Distros         | ✅ Windows 10+        | ✅ All         |
| Error Recovery       | ✅ Multiple Fallbacks | ✅ Multiple Fallbacks | ❌ Manual      |

## 🔄 Update Process

### Updating SQLmap GUI:

```bash
# Linux
cd SQLmap-GUI
git pull origin main
./start_gui.sh  # Reinstalls dependencies if needed

# Windows
cd SQLmap-GUI
git pull origin main
start_gui.bat   # Reinstalls dependencies if needed
```

### Force Reinstall:

```bash
# Linux
rm -rf .venv sqlmap-master
./start_gui.sh

# Windows
rmdir /s .venv sqlmap-master
start_gui.bat

# PowerShell (Windows)
.\start_gui.ps1 -Force
```

## 📝 Best Practices

1. **First Time Setup**: Use the installer scripts (`install_linux.sh` or `install_windows.bat`)
2. **Regular Usage**: Use the launcher scripts (`start_gui.sh` or `start_gui.bat`)
3. **Updates**: Pull from git and run launcher script to update dependencies
4. **Troubleshooting**: Check error messages and refer to distribution-specific solutions
5. **Security**: Never run scripts as root/administrator unless specifically documented
