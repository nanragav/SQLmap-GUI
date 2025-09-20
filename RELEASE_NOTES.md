# SQLmap GUI Release Notes

## Version 1.0.0

This release includes cross-platform builds for Linux and macOS systems.

### 📦 Release Files

- **SQLmap-GUI-linux.tar.gz** - Linux executable (Ubuntu, Debian, CentOS, etc.)
- **SQLmap-GUI-macOS.tar.gz** - macOS application bundle (Intel & Apple Silicon compatible)

### 🖥️ Linux Installation

1. Download `SQLmap-GUI-linux.tar.gz`
2. Extract: `tar -xzf SQLmap-GUI-linux.tar.gz`
3. Run: `./SQLmap-GUI/SQLmap-GUI`

### 🍎 macOS Installation

1. Download `SQLmap-GUI-macOS.tar.gz`
2. Extract the archive
3. Copy `SQLmap-GUI.app` to your Applications folder (optional)
4. **Important**: Right-click on `SQLmap-GUI.app` and select "Open"
5. Click "Open" when macOS asks about running an unsigned application

### ⚠️ macOS Security Note

Due to Apple's security requirements, you may see a warning about running an unsigned application. This is normal for open-source software. Simply right-click and select "Open" to bypass this security warning.

### 📋 Prerequisites

- **SQLmap**: Must be installed and available in system PATH
- **Python**: 3.8 or higher (usually pre-installed on most systems)
- **Operating System**: 
  - Linux: Most modern distributions (Ubuntu 18.04+, Debian 10+, etc.)
  - macOS: 10.14+ (Mojave or newer)

### 🔧 Features

- Modern PyQt6-based GUI for SQLmap
- Easy-to-use interface for SQL injection testing
- Support for all major SQLmap features
- Dark/Light theme support
- Real-time command preview
- Comprehensive configuration options

### 🐛 Troubleshooting

If you encounter issues:

1. **Linux**: Ensure you have necessary system libraries:
   ```bash
   sudo apt update && sudo apt install python3 python3-pip
   ```

2. **macOS**: If the app won't open:
   - Check that you right-clicked and selected "Open"
   - Verify SQLmap is installed: `brew install sqlmap`
   - Ensure Python 3.8+ is available

3. **Both platforms**: Verify SQLmap installation:
   ```bash
   sqlmap --version
   ```

### 📊 File Information

| File | Size | SHA256 |
|------|------|---------|
| SQLmap-GUI-linux.tar.gz | ~97MB | [To be calculated] |
| SQLmap-GUI-macOS.tar.gz | ~97MB | [To be calculated] |

### 🔗 Links

- [Project Repository](https://github.com/nanragav/SQLmap-GUI)
- [Documentation](https://github.com/nanragav/SQLmap-GUI/tree/main/docs)
- [Issue Tracker](https://github.com/nanragav/SQLmap-GUI/issues)

---

For support, please visit our [GitHub Issues](https://github.com/nanragav/SQLmap-GUI/issues) page.
