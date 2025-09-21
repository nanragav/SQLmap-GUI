# SQLmap-GUI: Advanced SQL Injection Testing Interface

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.0+-green.svg)](https://pypi.org/project/PyQt6/)
[![SQLmap](https://img.shields.io/badge/SQLmap-Latest-red.svg)](https://sqlmap.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/Documentation-GitHub%2### Documentation

### Online Documentation

Comprehensive documentation is available at our GitHub Pages site:

🔗 **[SQLmap GUI Documentation](https://nanragav.github.io/SQLmap-GUI/)**

### Platform-Specific Guides

- 🐧 **[Linux Installation Guide](README_LINUX.md)** - Comprehensive Linux setup guide with distribution-specific instructions
- 🪟 **[Windows Installation Guide](README_WINDOWS.md)** - Complete Windows setup guide with troubleshooting
- 📱 **[Auto-Installation Guide](docs/auto_installation_guide.md)** - Detailed explanation of automated setup scripts

### Complete Documentationblue.svg)](https://nanragav.github.io/SQLmap-GUI/)

A comprehensive, user-friendly graphical interface for SQLmap - the world's most powerful SQL injection testing tool. Built with Python and PyQt6 for professional penetration testers and security researchers.

## 🎯 Features

- **Complete SQLmap Integration**: Access all SQLmap parameters through an intuitive GUI
- **🆕 Auto-Installation Scripts**: One-click setup for Linux and Windows with automatic dependency management
- **Modular Tab Interface**: Organized tabs for different testing phases (Target, Injection, Enumeration, File System, OS Access, etc.)
- **Real-time Validation**: Built-in parameter validation with helpful error messages
- **Batch Processing**: Automated batch mode for efficient scanning
- **Advanced Options**: Support for tamper scripts, custom payloads, and advanced injection techniques
- **Session Management**: Save and load testing sessions
- **Cross-platform**: Works on Windows, Linux, and macOS
- **Clean Interface**: Only valid SQLmap parameters - no confusing non-existent options
- **🔒 Security-First**: No administrator privileges required for normal operation

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Quick Installation (Recommended)](#-quick-installation-recommended)
  - [Manual Installation (Development)](#️-manual-installation-development)
    - [Linux Installation](#linux-installation)
    - [Windows Installation](#windows-installation)
    - [macOS Installation](#macos-installation)
- [SQLmap Installation](#sqlmap-installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Documentation](#documentation)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Security](#security)
- [License](#license)

## 📋 Prerequisites

### System Requirements

- **Python**: 3.8 or higher
- **RAM**: Minimum 2GB, recommended 4GB+
- **Disk Space**: 500MB free space
- **Operating System**: Windows 10+, Ubuntu 18.04+, macOS 10.14+

### Required Software

- **SQLmap**: Latest version installed and accessible via command line
- **Git**: For cloning the repository
- **Python Virtual Environment**: Recommended for dependency management

### 🔐 Administrator Requirements

#### Linux Systems

- **Initial Setup Only**: `sudo` access required for installing system packages
  - Python 3.8+ and development tools (`python3-dev`, `python3-venv`)
  - Basic utilities (`git`, `unzip`, `wget`)
  - Distribution-specific package installation (`apt`, `yum`, `dnf`, `pacman`)
- **Normal Operation**: Runs as regular user with no elevated privileges
- **Virtual Environment**: Created in user space (no system modifications)

#### Windows Systems

- **No Administrator Rights Required**: All installations go to user directories
  - Python installed to `%USERPROFILE%\AppData\Local\Programs\Python`
  - SQLmap downloaded to application folder
  - Virtual environment in `.venv` subfolder
- **Normal Operation**: Standard user privileges sufficient
- **System Changes**: Only PATH modification (optional, user-level only)

#### Security Notes

- Scripts never require permanent elevation
- All installations are user-scoped and portable
- Virtual environments isolate dependencies
- SQLmap runs in portable mode (no system installation required)

## 🚀 Installation

### 📦 Quick Installation (Recommended)

#### Option 1: Auto-Installation Scripts (Easiest)

**🐧 Linux:**

```bash
# One-click installer (recommended)
git clone https://github.com/nanragav/SQLmap-GUI.git
cd SQLmap-GUI
./install_linux.sh

# Or use the enhanced launcher directly
./start_gui.sh
```

**🪟 Windows:**

```cmd
# Download the repository, then run:
install_windows.bat

# Or use the auto-launcher directly:
start_gui.bat
# Or PowerShell version:
start_gui.ps1
```

**🔐 Administrator Requirements:**

- **Linux**: Sudo access required only for installing system packages (Python, unzip, wget)
- **Windows**: No administrator rights needed (installs to user directory)
- **Normal Operation**: Both platforms run as regular user after initial setup

#### Option 2: Pre-built Executables

**Download pre-built executables** - No Python setup required!

1. Go to [Releases](https://github.com/nanragav/SQLmap-GUI/releases)
2. Download the appropriate file for your system:

   **Windows:** `SQLmap-GUI-windows.zip`

   - Extract the zip file
   - Run `SQLmap-GUI.exe`

   **Linux:** `SQLmap-GUI-linux.tar.gz`

   - Extract: `tar -xzf SQLmap-GUI-linux.tar.gz`
   - Make executable: `chmod +x SQLmap-GUI`
   - Run: `./SQLmap-GUI`

   **macOS:** `SQLmap-GUI-macos.zip`

   - Extract the zip file
   - Run `SQLmap-GUI.app`
   - Note: Right-click and select "Open" the first time due to macOS security settings

3. **Install SQLmap separately** (if not already installed):
   - See [SQLmap Installation](#-sqlmap-installation) section below

> **Note:** Pre-built binaries include all Python dependencies. You only need to install SQLmap separately.

---

### 🛠️ Manual Installation (Development)

If you want to run from source or contribute to development:

### Linux Installation

#### Auto-Installation (Recommended)

**Using the Installer Script:**

```bash
# Clone the repository
git clone https://github.com/nanragav/SQLmap-GUI.git
cd SQLmap-GUI

# Run the one-click installer
./install_linux.sh
```

**Using the Enhanced Launcher:**

```bash
# The enhanced launcher automatically handles all dependencies
./start_gui.sh
```

**What Gets Installed Automatically:**

- **Python 3.8+** (if not present) - uses distribution package manager
- **SQLmap** (latest) - downloaded to `sqlmap-master/` folder
- **System Dependencies** - unzip, wget, python3-dev, python3-venv
- **Python Dependencies** - PyQt6, psutil, requests in virtual environment
- **Desktop Shortcuts** - `.desktop` files for easy access

**Administrator Requirements:**

- **Initial Setup**: `sudo` access needed for installing system packages only
- **Normal Operation**: Runs as regular user, no elevated privileges required
- **Virtual Environment**: Created in user space (`.venv/` folder)

#### Manual Installation (Advanced Users)

**Step 1: Install System Dependencies**

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv python3-dev git unzip wget

# CentOS/RHEL/Fedora
sudo yum install python3 python3-pip git unzip wget  # CentOS/RHEL
sudo dnf install python3 python3-pip git unzip wget  # Fedora

# Arch Linux
sudo pacman -S python python-pip git unzip wget
```

**Step 2: Clone and Setup Project**

```bash
# Clone the repository
git clone https://github.com/nanragav/SQLmap-GUI.git
cd SQLmap-GUI

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

**Step 3: Make Scripts Executable**

```bash
chmod +x start_gui.sh
chmod +x install_linux.sh
```

### Windows Installation

#### Step 1: Install Python

1. Download Python 3.8+ from [python.org](https://python.org)
2. During installation, **check**:
   - ✅ "Add Python to PATH"
   - ✅ "Install pip"
   - ✅ "Install for all users" (recommended)

#### Step 2: Install Git

1. Download Git from [git-scm.com](https://git-scm.com/)
2. Install with default settings

#### Step 3: Clone and Setup Project

```cmd
# Open Command Prompt or PowerShell
git clone https://github.com/nanragav/SQLmap-GUI.git
cd sqlmap-gui

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### macOS Installation

#### Step 1: Install Homebrew (if not already installed)

```bash
# Install Homebrew package manager
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Add Homebrew to PATH (follow the instructions shown after installation)
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

#### Step 2: Install Python and Git

```bash
# Install Python 3.8+ and Git
brew install python git

# Verify installations
python3 --version
git --version
```

#### Step 3: Clone and Setup Project

```bash
# Clone the repository
git clone https://github.com/nanragav/SQLmap-GUI.git
cd sqlmap-gui

# Create virtual environment using Python 3
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

#### macOS-Specific Notes

- **Apple Silicon (M1/M2/M3)**: All dependencies are compatible with ARM64 architecture
- **Security**: You may need to allow the application in System Preferences > Security & Privacy
- **Python Path**: Use `python3` instead of `python` on macOS to avoid conflicts with system Python 2.x
- **Permissions**: If you encounter permission issues, avoid using `sudo` with pip. Use virtual environments instead

## 🛠️ SQLmap Installation

### Linux Installation

#### Option 1: Using Package Manager (Recommended)

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install sqlmap

# CentOS/RHEL
sudo yum install sqlmap

# Arch Linux
sudo pacman -S sqlmap
```

#### Option 2: Manual Installation

```bash
# Clone SQLmap repository
git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git sqlmap-dev

# Make it executable
cd sqlmap-dev
chmod +x sqlmap.py

# Test installation
./sqlmap.py --version
```

### Windows Installation

#### Option 1: Using pip (Recommended)

```cmd
# Install SQLmap via pip
pip install sqlmap

# Test installation
sqlmap --version
```

#### Option 2: Manual Installation

```cmd
# Clone SQLmap repository
git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git sqlmap-dev

# Test installation
cd sqlmap-dev
python sqlmap.py --version
```

### Environment Variables

#### Linux

Add SQLmap to your PATH (if installed manually):

```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'export PATH="$PATH:/path/to/sqlmap-dev"' >> ~/.bashrc
source ~/.bashrc
```

#### Windows

1. **For pip installation**: SQLmap should be automatically added to PATH
2. **For manual installation**: Add the sqlmap directory to your PATH:
   - Right-click "This PC" → Properties → Advanced system settings
   - Click "Environment Variables"
   - Under "System variables", find "Path" and click "Edit"
   - Add: `C:\path\to\sqlmap-dev`
   - Click OK and restart Command Prompt

#### Verification

Test that SQLmap is properly installed:

```bash
sqlmap --version
# Should output: sqlmap version X.X.X
```

## 🎮 Quick Start

### Auto-Installation (Easiest)

**Linux:**

```bash
git clone https://github.com/nanragav/SQLmap-GUI.git
cd SQLmap-GUI
./install_linux.sh  # One-click installer
# or
./start_gui.sh      # Enhanced auto-launcher
```

**Windows:**

```cmd
# Download repository, then run:
install_windows.bat  # One-click installer
# or
start_gui.bat       # Auto-launcher
# or
start_gui.ps1       # PowerShell version
```

### Manual Launch (After Installation)

**Linux:**

```bash
cd SQLmap-GUI
source .venv/bin/activate
python main.py
```

**Windows:**

```cmd
cd SQLmap-GUI
.venv\Scripts\activate
python main.py
```

### Using Startup Scripts

**Linux:**

```bash
./start_gui.sh      # Enhanced auto-setup launcher
```

**Windows:**

```cmd
start_gui.bat       # Batch file launcher
start_gui.ps1       # PowerShell launcher
```

## 📖 Usage

### Basic Workflow

1. **Start the GUI** using one of the methods above
2. **Configure Target**:
   - Go to "Target" tab
   - Enter target URL: `http://example.com/page.php?id=1`
3. **Set Options**:
   - Choose injection techniques in "Techniques" tab
   - Configure detection level in "Detection" tab
   - Select enumeration options in "Enumeration" tab
4. **Execute Scan**:
   - Review command in the preview panel
   - Click "Start Scan"
   - Monitor progress in the output panel

### Advanced Usage

#### Custom Profiles

- Save your common configurations as profiles
- Load profiles for different types of assessments
- Share profiles with team members

#### Batch Processing

- Use the batch mode for automated scanning
- Configure multiple targets
- Schedule scans for off-hours

## 📚 Documentation

### Online Documentation

Comprehensive documentation is available at our GitHub Pages site:

🔗 **[SQLmap GUI Documentation](https://nanragav.github.io/SQLmap-GUI/)**

The documentation includes:

- **Complete User Manual**: Step-by-step guide for all GUI features
- **Tab-by-Tab Documentation**: Detailed explanation of all 15 tabs and their options
- **Practical Examples**: Real-world SQL injection testing scenarios
- **Advanced Techniques**: Complex exploitation methods and WAF bypass
- **Troubleshooting Guide**: Solutions for common issues and problems
- **API Reference**: Developer documentation for extending the GUI

### Documentation Sections

- **Installation Guide**: Platform-specific setup instructions
- **Quick Start Guide**: Get up and running in 5 minutes
- **Configuration Guide**: Advanced settings and customization
- **Examples Directory**: Practical usage scenarios and tutorials
- **API Documentation**: For developers extending the GUI
- **Release Guide**: How to create and distribute binary releases ([RELEASES.md](RELEASES.md))
- **Build Guide**: Building from source for all platforms ([BUILDING.md](BUILDING.md))

### Getting Started with Documentation

1. Visit the [documentation site](https://nanragav.github.io/SQLmap-GUI/)
2. Start with the [Quick Start Guide](https://nanragav.github.io/SQLmap-GUI/quick_start.html)
3. Explore the [User Manual](https://nanragav.github.io/SQLmap-GUI/user_manual.html)
4. Check out [Practical Examples](https://nanragav.github.io/SQLmap-GUI/examples/)

## 🏗️ Project Structure

```
sqlmap-gui/
├── src/
│   ├── main.py                    # Application entry point
│   ├── gui/
│   │   ├── main_window.py         # Main application window
│   │   ├── tabs/                  # GUI tabs
│   │   │   ├── target_tab.py
│   │   │   ├── injection_tab.py
│   │   │   ├── enumeration_tab.py
│   │   │   └── ...
│   │   └── widgets/
│   │       └── custom_widgets.py
│   ├── core/
│   │   └── sqlmap_wrapper.py      # SQLmap integration
│   └── utils/
│       └── config.py              # Configuration management
├── requirements.txt               # Python dependencies
├── start_gui.sh                  # Linux startup script
├── run_gui.sh                    # Alternative Linux startup
├── README.md                     # This file
└── SQLmap_GUI_Plan.md           # Development documentation
```

## 🔧 Troubleshooting

### Common Issues

#### 1. "ModuleNotFoundError: No module named 'PyQt6'"

**Solution**:

```bash
# Linux
source .venv/bin/activate
pip install PyQt6

# Windows
.venv\Scripts\activate
pip install PyQt6
```

#### 2. "sqlmap: command not found"

**Solution**: Ensure SQLmap is installed and in PATH

```bash
# Check if SQLmap is installed
which sqlmap  # Linux
where sqlmap  # Windows

# If not found, reinstall SQLmap
```

#### 3. "Permission denied" when running scripts

**Linux**:

```bash
chmod +x start_gui.sh
chmod +x run_gui.sh
```

#### 4. GUI doesn't start on Windows

**Solution**: Install Microsoft Visual C++ Redistributable

- Download from: https://aka.ms/vs/17/release/vc_redist.x64.exe

#### 5. High CPU/Memory usage

**Solution**:

- Close other applications
- Use batch mode for large scans
- Monitor resource usage in the GUI

### Debug Mode

Enable debug logging:

```bash
# Linux
export SQLMAP_GUI_DEBUG=1
python src/main.py

# Windows
set SQLMAP_GUI_DEBUG=1
python src\main.py
```

### Getting Help

- Check the [Issues](https://github.com/nanragav/SQLmap-GUI/issues) page
- Review the [SQLmap documentation](https://sqlmap.org/)
- Join security communities for SQL injection discussions

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/nanragav/SQLmap-GUI.git`
3. **Create** a feature branch: `git checkout -b feature-name`
4. **Make** your changes following the existing code style
5. **Test** thoroughly on both Linux and Windows
6. **Commit** your changes: `git commit -m "Add feature description"`
7. **Push** to your fork: `git push origin feature-name`
8. **Create** a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add docstrings to new functions
- Test on multiple platforms (Linux, Windows)
- Update documentation for new features
- Ensure backward compatibility

## 🔒 Security

### Important Security Considerations

- **Authorized Use Only**: Only test systems you own or have explicit permission to test
- **Legal Compliance**: Ensure compliance with local laws and regulations
- **Responsible Disclosure**: Report vulnerabilities through proper channels
- **Data Protection**: Be aware that SQLmap can extract sensitive data

### Best Practices

1. **Use appropriate risk levels**: Start with low risk (1) and increase gradually
2. **Monitor resource usage**: SQLmap can be resource-intensive
3. **Backup target systems**: Some operations may modify data
4. **Use in controlled environments**: Test in isolated environments first
5. **Keep software updated**: Regularly update SQLmap and this GUI

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is designed for **educational and authorized security testing purposes only**. The developers assume no liability for misuse of this software. Users are responsible for:

- Obtaining proper authorization before testing any system
- Complying with applicable laws and regulations
- Using the tool ethically and responsibly
- Understanding the potential impact of SQL injection testing

**By using this software, you agree to use it responsibly and only on systems you are authorized to test.**

---

## 🙏 Acknowledgments

- [SQLmap](https://sqlmap.org/) - The core SQL injection testing engine
- [PyQt6](https://pypi.org/project/PyQt6/) - Modern GUI framework
- The security research community for their contributions

## 📞 Support

### Documentation

- **Online Documentation**: [GitHub Pages](https://nanragav.github.io/SQLmap-GUI/)
- **Technical Details**: See [SQLmap_GUI_Plan.md](SQLmap_GUI_Plan.md) for technical details

### Contact Information

- **Email**: [sriragavendrabharath@outlook.com](mailto:sriragavendrabharath@outlook.com)
- **GitHub Issues**: [Report bugs and request features](https://github.com/nanragav/SQLmap-GUI/issues)
- **GitHub Discussions**: Join community discussions

### Community Support

- **SQLmap Official**: [sqlmap.org](https://sqlmap.org/)
- **Security Communities**: OWASP, Bug Bounty forums
- **Documentation Issues**: Report documentation problems via GitHub

---

**Made with ❤️ for the security community**

_SQLmap-GUI v1.0.0 - Professional SQL Injection Testing Interface_
