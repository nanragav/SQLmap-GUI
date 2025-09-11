# SQLmap GUI - Advanced SQL Injection Testing Interface

[![GitHub Pages](https://img.shields.io/badge/GitHub-Pages-blue)](https://nanragav.github.io/SQLmap-GUI/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.6+-green)](https://pypi.org/project/PyQt6/)
[![SQLmap](https://img.shields.io/badge/SQLmap-1.9.9.1-red)](https://sqlmap.org/)

A comprehensive graphical user interface for SQLmap - the automatic SQL injection and database takeover tool. This GUI provides an intuitive, user-friendly interface to harness the full power of SQLmap without command-line complexity.

## 🚀 Features

- **Complete SQLmap Coverage**: All SQLmap options and features accessible through GUI
- **Real-time Command Preview**: See the exact SQLmap command being built
- **Profile Management**: Save and load configurations for different targets
- **Resource Monitoring**: Built-in CPU and memory usage monitoring
- **Performance Optimization**: Intelligent caching and throttling for smooth operation
- **Validation System**: Real-time option validation with helpful error messages
- **Multi-platform Support**: Works on Linux, Windows, and macOS

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [GUI Overview](#gui-overview)
- [Tab Reference](#tab-reference)
- [Examples](#examples)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🎯 Quick Start

### Prerequisites

- **Python 3.10+**
- **PyQt6** (GUI framework)
- **SQLmap** (command-line tool)
- **psutil** (system monitoring)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/nanragav/SQLmap-GUI.git
   cd SQLmap-GUI
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install SQLmap:**
   ```bash
   # Using apt (Ubuntu/Debian)
   sudo apt install sqlmap

   # Or download from https://sqlmap.org/
   ```

4. **Run the GUI:**
   ```bash
   ./start_gui.sh
   # or
   python3 main.py
   ```

### First Scan

1. **Target Tab**: Enter your target URL (e.g., `http://example.com/page.php?id=1`)
2. **Detection Tab**: Set Level to 3, Risk to 2 for thorough testing
3. **Techniques Tab**: Select desired injection techniques
4. **Enumeration Tab**: Choose what to enumerate (databases, tables, etc.)
5. **Click "Start Scan"**

## 🖥️ GUI Overview

The SQLmap GUI is organized into 15 specialized tabs, each handling different aspects of SQL injection testing:

### Main Interface Layout

```
┌─────────────────────────────────────────────────────────────┐
│ File  Tools  Help  [New] [Open] [Save] [Start] [Stop] [Validate] │
├─────────────────────────────────────────────────────────────┤
│ Target │ Request │ Injection │ Detection │ Techniques │ ... │
├─────────────────────────────────────────────────────────────┤
│ Target URL: http://example.com/page.php?id=1                │
│ Method: GET    Data:                    Cookie:             │
│ User-Agent: Mozilla/5.0...              Host: example.com   │
├─────────────────────────────────────────────────────────────┤
│ SQLmap Command:                                             │
│ sqlmap -u "http://example.com/page.php?id=1" --batch        │
├─────────────────────────────────────────────────────────────┤
│ [14:32:15] Starting SQL injection scan...                   │
│ [14:32:16] Testing for SQL injection...                     │
│ [14:32:17] SQL injection vulnerability found!               │
├─────────────────────────────────────────────────────────────┤
│ Memory: 45.2 MB                    CPU: 12.3%               │
└─────────────────────────────────────────────────────────────┘
```

### Key Components

1. **Menu Bar**: File operations, tools, and help
2. **Toolbar**: Quick access to common actions
3. **Tab Bar**: 15 specialized configuration tabs
4. **Command Preview**: Real-time SQLmap command generation
5. **Log Window**: Execution output and status messages
6. **Status Bar**: Resource monitoring and progress

## 📑 Tab Reference

### 1. [Target Tab](tabs/target_tab.md)
Configure target specifications and connection details.

**Key Options:**
- **Target URL**: Main target URL for testing
- **Direct Connection**: Direct database connection string
- **HTTP Method**: GET, POST, PUT, DELETE, etc.
- **Request Data**: POST data for form submissions
- **HTTP Headers**: Custom headers (Cookie, User-Agent, etc.)
- **Proxy Settings**: HTTP/SOCKS proxy configuration

### 2. [Request Tab](tabs/request_tab.md)
HTTP request customization and optimization.

**Key Options:**
- **Optimization**: Connection pooling, batch mode
- **Timing**: Request delays, timeouts, retries
- **Authentication**: Basic, Digest, NTLM authentication
- **SSL/TLS**: Force HTTPS, custom certificates
- **Tor Integration**: Anonymous scanning via Tor

### 3. [Injection Tab](tabs/injection_tab.md)
SQL injection payload configuration.

**Key Options:**
- **Parameter Selection**: Which parameters to test
- **DBMS Selection**: Force specific database type
- **Payload Customization**: Prefix/suffix strings
- **Tamper Scripts**: WAF bypass techniques
- **Invalidation Methods**: Big numbers, logical operations

### 4. [Detection Tab](tabs/detection_tab.md)
SQL injection detection parameters.

**Key Options:**
- **Test Level**: 1-5 (higher = more thorough)
- **Risk Level**: 1-3 (higher = more aggressive)
- **String Matching**: Custom success/failure patterns
- **UNION Testing**: Column range, character testing
- **Second-Order**: Multi-request injection testing

### 5. [Techniques Tab](tabs/techniques_tab.md)
Injection technique selection.

**Key Options:**
- **Boolean-based Blind**: True/false condition testing
- **Time-based Blind**: Delay-based detection
- **Error-based**: Database error exploitation
- **UNION-based**: Column enumeration and data extraction
- **Stacked Queries**: Multiple statement execution
- **Inline Queries**: Subquery injection

### 6. [Enumeration Tab](tabs/enumeration_tab.md)
Database structure and data extraction.

**Key Options:**
- **Basic Info**: Banner, users, databases, privileges
- **Structure**: Tables, columns, schemas
- **Data Extraction**: Dump tables, search data
- **Custom Queries**: Run arbitrary SQL statements
- **Range Selection**: Limit rows/characters retrieved

### 7. [Fingerprint Tab](tabs/fingerprint_tab.md)
Database fingerprinting and identification.

### 8. [Brute Force Tab](tabs/brute_force_tab.md)
Dictionary-based attacks and common name enumeration.

### 9. [UDF Tab](tabs/udf_tab.md)
User-defined function injection.

### 10. [File System Tab](tabs/file_system_tab.md)
File system access and manipulation.

### 11. [OS Access Tab](tabs/os_access_tab.md)
Operating system command execution.

### 12. [Windows Registry Tab](tabs/windows_registry_tab.md)
Windows registry access (Windows targets only).

### 13. [General Tab](tabs/general_tab.md)
General SQLmap configuration and behavior.

### 14. [Miscellaneous Tab](tabs/miscellaneous_tab.md)
Additional advanced options.

### 15. [Hidden Switches Tab](tabs/hidden_switches_tab.md)
Experimental and advanced features.

## 📚 Examples

### Basic SQL Injection Scan
```bash
# Target: http://example.com/product.php?id=1
# GUI Configuration:
# - Target Tab: URL = http://example.com/product.php?id=1
# - Detection Tab: Level = 3, Risk = 2
# - Techniques Tab: Boolean-based, Error-based, UNION-based
# - Enumeration Tab: Databases, Tables, Columns
```

**Generated Command:**
```bash
sqlmap -u "http://example.com/product.php?id=1" --level=3 --risk=2 --technique=BEU --dbs --tables --columns --batch
```

### Advanced Scan with Custom Options
```bash
# Target: Vulnerable login form
# GUI Configuration:
# - Target Tab: URL = http://example.com/login.php, Method = POST, Data = username=admin&password=test
# - Request Tab: User-Agent = Custom, Timeout = 10
# - Injection Tab: DBMS = MySQL, Tamper = space2comment
# - Enumeration Tab: Dump all data from users table
```

**Generated Command:**
```bash
sqlmap -u "http://example.com/login.php" --method=POST --data="username=admin&password=test" --dbms=mysql --tamper=space2comment --dump -T users --batch
```

### Anonymous Scanning with Tor
```bash
# GUI Configuration:
# - Request Tab: Tor = Enabled, Tor Port = 9050
# - Target Tab: URL = http://example.com/vuln.php?id=1
# - General Tab: Batch = Enabled
```

**Generated Command:**
```bash
sqlmap -u "http://example.com/vuln.php?id=1" --tor --tor-port=9050 --batch
```

## 🔧 API Documentation

### Core Classes

#### `SqlmapMainWindow`
Main application window containing all GUI components.

**Methods:**
- `get_options()`: Collect all options from all tabs
- `validate_options()`: Validate current configuration
- `start_scan()`: Begin SQL injection testing
- `save_profile()`: Save current configuration
- `load_profile()`: Load saved configuration

#### `SqlmapWrapper`
Handles SQLmap command generation and execution.

**Methods:**
- `build_command(options)`: Generate SQLmap command from GUI options
- `validate_options(options)`: Check option compatibility
- `create_process(options)`: Start SQLmap process

#### `MutualExclusionManager`
Manages conflicting option combinations.

**Methods:**
- `register_option(name, widget)`: Register option for conflict checking
- `update_option_state(name, value)`: Update option state and check conflicts

### Option Groups

Each tab contains multiple `OptionGroup` instances that handle:
- Widget creation and layout
- Value validation and formatting
- Signal emission for real-time updates
- Mutual exclusion checking

## 🐛 Troubleshooting

### Common Issues

#### GUI Won't Start
**Error:** `ModuleNotFoundError: No module named 'PyQt6'`
**Solution:**
```bash
pip install PyQt6 PyQt6-Qt6
```

#### SQLmap Not Found
**Error:** `sqlmap: command not found`
**Solution:**
```bash
# Install via package manager
sudo apt install sqlmap

# Or download from https://sqlmap.org/
```

#### Performance Issues
**Symptoms:** GUI is slow, unresponsive, or hanging
**Solutions:**
1. Use **Help → Performance → High Performance Mode**
2. Close other resource-intensive applications
3. Use **Help → Performance → Optimize Performance**
4. Restart the GUI application

#### CPU/Memory Usage High
**Solutions:**
1. Enable **Help → Performance → Pause Resource Monitoring**
2. Use **Help → Performance → High Performance Mode**
3. Close unnecessary tabs/windows
4. Monitor with **Help → Debug CPU Monitoring**

### Debug Information

Access debug information via:
- **Help → Debug Tabs**: Check tab integrity
- **Help → Debug CPU Monitoring**: System resource details
- **Help → Performance → Optimize Performance**: Manual cleanup

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

1. **Fork and clone:**
   ```bash
   git clone https://github.com/nanragav/SQLmap-GUI.git
   cd SQLmap-GUI
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
   ```

3. **Install development dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Run tests:**
   ```bash
   python -m pytest
   ```

### Code Structure

```
src/
├── gui/
│   ├── main_window.py      # Main application window
│   ├── main.py            # Application entry point
│   ├── widgets/           # Custom GUI components
│   │   ├── custom_widgets.py
│   │   └── __init__.py
│   └── tabs/              # Configuration tabs
│       ├── base_tab.py
│       ├── target_tab.py
│       ├── request_tab.py
│       └── ...
├── core/                  # Core functionality
│   ├── config_manager.py
│   ├── sqlmap_wrapper.py
│   └── mutual_exclusion_manager.py
└── utils/
    └── config.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and authorized security testing purposes only. Users are responsible for complying with applicable laws and regulations. Unauthorized use of this tool may violate laws in your jurisdiction.

## 🙏 Acknowledgments

- **SQLmap**: The powerful command-line SQL injection tool this GUI is built upon
- **PyQt6**: The excellent GUI framework that makes this interface possible
- **Open Source Community**: For the countless libraries and tools that make projects like this possible

---

**Happy SQL Injection Testing! 🔒🛡️**

For questions, issues, or contributions, please visit our [GitHub repository](https://github.com/nanragav/SQLmap-GUI).</content>
<parameter name="filePath">
