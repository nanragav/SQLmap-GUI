# SQLmap GUI - Windows Installation Guide

## Quick Start (Automatic Installation)

### Option 1: One-Click Installer (Recommended)

1. Download or clone this repository
2. Double-click `install_windows.bat`
3. Follow the prompts - the installer will handle everything automatically

### Option 2: PowerShell Script (Advanced Users)

1. Open PowerShell as Administrator
2. Navigate to the SQLmap-GUI directory
3. Run: `.\start_gui.ps1`

### Option 3: Batch Script

1. Double-click `start_gui.bat`
2. The script will check and install dependencies automatically

## What Gets Installed Automatically

### Python Installation

- **Version**: Python 3.12.0 (latest stable)
- **Location**: `%USERPROFILE%\AppData\Local\Programs\Python\Python312`
- **Features**:
  - Added to system PATH
  - pip package manager included
  - File associations configured

### SQLmap Installation

- **Source**: Latest version from GitHub
- **Location**: `sqlmap-master/` in the script directory
- **Type**: Portable installation (no system changes)

### Python Dependencies

- **PyQt6**: GUI framework (>=6.5.0)
- **psutil**: System process monitoring (>=5.9.0)
- **requests**: HTTP library (>=2.28.0)
- **Virtual Environment**: Isolated environment in `.venv/`

## System Requirements

- **Operating System**: Windows 10/11 (64-bit)
- **RAM**: Minimum 4GB, Recommended 8GB
- **Storage**: 500MB free space
- **Internet**: Required for initial setup
- **Permissions**: Standard user (no admin required)

## Manual Installation (If Automatic Fails)

### 1. Install Python

```cmd
# Download from: https://www.python.org/downloads/
# Choose "Add Python to PATH" during installation
python --version
```

### 2. Install SQLmap

```cmd
# Download from: https://github.com/sqlmapproject/sqlmap
# Extract to sqlmap-master/ folder
```

### 3. Install Dependencies

```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Run GUI

```cmd
python main.py
```

## Troubleshooting

### Common Issues

#### 1. "Python not found"

**Solution**:

- Run `install_windows.bat` again
- Or manually install Python from python.org
- Ensure "Add Python to PATH" is checked

#### 2. "Module 'PyQt6' not found"

**Solution**:

```cmd
.venv\Scripts\activate
pip install PyQt6
```

#### 3. "SQLmap not found"

**Solution**:

- Run the installer again
- Or manually download SQLmap to `sqlmap-master/` folder

#### 4. "Permission denied"

**Solution**:

- Run as Administrator
- Or use PowerShell with execution policy bypass:

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\start_gui.ps1
```

#### 5. "Virtual environment creation failed"

**Solution**:

```cmd
python -m pip install virtualenv
python -m virtualenv .venv
```

### Advanced Troubleshooting

#### Check Python Installation

```cmd
python --version
python -m pip --version
```

#### Check PyQt6 Installation

```cmd
python -c "import PyQt6; print('PyQt6 is working')"
```

#### Check SQLmap

```cmd
# If sqlmap is in PATH:
sqlmap --version

# If using local installation:
python sqlmap-master\sqlmap.py --version
```

#### Reset Installation

```cmd
rmdir /s .venv
del requirements.txt
# Run installer again
```

## Configuration

### Custom Python Installation

If you have a specific Python version installed, edit the scripts:

- In `start_gui.bat`: Change `PYTHON_VERSION` variable
- In `start_gui.ps1`: Use `-PythonVersion` parameter

### Custom SQLmap Location

If you have SQLmap installed elsewhere:

1. Edit `src/utils/config.py`
2. Set `SQLMAP_PATH` to your SQLmap location

### Proxy Configuration

For corporate networks:

```cmd
set HTTP_PROXY=http://proxy:port
set HTTPS_PROXY=http://proxy:port
pip install --proxy http://proxy:port PyQt6
```

## File Structure After Installation

```
SQLmap-GUI/
├── main.py                    # Main application entry
├── start_gui.bat             # Windows batch launcher
├── start_gui.ps1             # PowerShell launcher
├── install_windows.bat       # One-click installer
├── requirements.txt          # Python dependencies
├── .venv/                    # Virtual environment
│   └── Scripts/
│       ├── activate.bat      # Activation script
│       └── python.exe        # Isolated Python
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

- **Desktop**: Double-click "SQLmap GUI" shortcut
- **File Explorer**: Double-click `start_gui.bat`
- **Command Line**: `python main.py`
- **PowerShell**: `.\start_gui.ps1`

### First Time Setup

1. The GUI will automatically detect your Python and SQLmap
2. All dependencies are managed in an isolated virtual environment
3. No system-wide changes are made (except Python installation if needed)

## Uninstallation

### Remove SQLmap GUI

```cmd
# Delete the entire SQLmap-GUI folder
rmdir /s SQLmap-GUI
```

### Remove Python (Optional)

- Use "Add or Remove Programs" in Windows Settings
- Look for "Python 3.12.0" and uninstall

### Remove Desktop Shortcut

- Delete "SQLmap GUI.lnk" from Desktop

## Security Notes

- All downloads are from official sources (python.org, github.com)
- Virtual environment isolates dependencies
- No administrator privileges required for normal operation
- SQLmap runs in portable mode (no system installation)

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Run with verbose output: `start_gui.bat` (shows detailed logs)
3. Check the main project documentation
4. Report issues on the GitHub repository

## Performance Tips

- **SSD Storage**: Install on SSD for better performance
- **Antivirus**: Add SQLmap folder to antivirus exclusions
- **Firewall**: Allow Python.exe through Windows Firewall
- **Resources**: Close unnecessary applications during intensive scans
