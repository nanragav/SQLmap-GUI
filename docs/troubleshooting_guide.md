# Troubleshooting Guide

This comprehensive troubleshooting guide helps you resolve common issues encountered while using the SQLmap GUI for SQL injection testing.

## 🔍 Common Issues and Solutions

### Issue 1: GUI Performance Problems

**Symptoms:**
- GUI becomes unresponsive or slow
- High CPU usage
- Memory consumption keeps increasing
- Log widget fills up and causes freezing

**Solutions:**

#### Performance Mode Toggle
```
Help Menu → Performance Mode
├── Enable Performance Mode: ✓
├── CPU Monitoring Interval: 5 seconds
├── Log Size Limit: 1000 lines
└── Command Preview Throttling: 500ms
```

#### Manual Performance Fixes
1. **Clear Log Widget:**
   ```
   View Menu → Clear Log
   ```
   Or use keyboard shortcut: `Ctrl+L`

2. **Reset CPU Monitoring:**
   ```
   Help Menu → Debug CPU Monitoring → Reset Cache
   ```

3. **Enable Throttling:**
   ```
   Help Menu → Performance Settings → Enable Throttling
   ```

#### Advanced Performance Configuration
```python
# In main_window.py, adjust these values:
COMMAND_PREVIEW_DELAY = 1000  # Increase delay (ms)
CPU_UPDATE_INTERVAL = 10000   # Increase interval (ms)
LOG_MAX_LINES = 500          # Reduce max lines
```

### Issue 2: SQLmap Command Generation Errors

**Symptoms:**
- Invalid command syntax
- Parameters not being included
- Tamper scripts not applied
- DBMS-specific options missing

**Solutions:**

#### Check Parameter Configuration
```
Target Tab:
├── URL: Must be valid and accessible
├── Method: Match the actual HTTP method
├── Data: Required for POST requests
└── Cookies: Include session cookies if needed

Injection Tab:
├── Testable Parameters: Specify exact parameter names
├── DBMS: Select correct database type
├── Tamper Scripts: Verify file paths exist
└── Custom Options: Check syntax
```

#### Validate Command Preview
1. **Enable Real-time Preview:**
   ```
   View Menu → Command Preview → Real-time Updates
   ```

2. **Manual Command Validation:**
   ```
   Tools Menu → Validate Command
   ```

3. **Test Generated Command:**
   ```bash
   # Copy command from preview and test manually
   sqlmap [generated options] --batch --dry-run
   ```

### Issue 3: Connection and Network Issues

**Symptoms:**
- Connection timeouts
- Proxy errors
- SSL/TLS certificate issues
- Firewall blocking requests

**Solutions:**

#### Network Configuration
```
Request Tab:
├── Timeout: 30-120 seconds (depending on target)
├── Delay: 1-5 seconds (to avoid rate limiting)
├── Retries: 3-5 attempts
├── Keep Alive: ✓ (for persistent connections)
└── Chunked: ✓ (for large requests)
```

#### Proxy Setup
```
Request Tab:
├── Proxy: http://127.0.0.1:8080 (Burp Suite)
├── Proxy: socks5://127.0.0.1:9050 (Tor)
└── Ignore Proxy: ✓ (for direct connections)
```

#### SSL/TLS Configuration
```
Request Tab:
├── Certificate: /path/to/client.crt
├── Key: /path/to/client.key
├── CA Certificate: /path/to/ca.crt
└── Insecure: ✓ (for self-signed certificates)
```

### Issue 4: Detection Problems

**Symptoms:**
- False negatives (vulnerabilities not detected)
- False positives (non-vulnerabilities flagged)
- Detection taking too long
- WAF blocking detection attempts

**Solutions:**

#### Adjust Detection Sensitivity
```
Detection Tab:
├── Level: 3-5 (higher for thorough testing)
├── Risk: 2-3 (higher for aggressive testing)
├── Techniques: BEUSTQ (all techniques)
├── Time Delay: 2-5 seconds
└── Retries: 3-5 attempts
```

#### WAF Bypass Techniques
```
Injection Tab:
├── Tamper Scripts:
│   ├── space2comment
│   ├── randomcase
│   ├── apostrophemask
│   ├── base64encode
│   └── versionedkeywords
├── Prefix/Suffix: Custom evasion strings
├── Invalid Logical: ✓
└── No Escape: ✓
```

#### Time-Based Detection Issues
```
Detection Tab:
├── Time Delay: 1-10 seconds (adjust based on network)
├── Retries: 5+ for unreliable connections
└── Timeout: 60+ seconds for slow responses
```

### Issue 5: Database-Specific Issues

**Symptoms:**
- Incorrect DBMS detection
- Database-specific syntax errors
- Privilege escalation failures
- Data extraction problems

**Solutions:**

#### MySQL Issues
```
Injection Tab:
├── DBMS: MySQL
├── Union Character: NULL or numeric values
└── Tamper Scripts: space2comment, randomcase

Enumeration Tab:
├── Database: information_schema
├── Table: TABLES,COLUMNS
└── System Database: mysql
```

#### PostgreSQL Issues
```
Injection Tab:
├── DBMS: PostgreSQL
├── Union Character: NULL
└── Tamper Scripts: space2comment, randomcase

Enumeration Tab:
├── Database: pg_catalog
├── Table: pg_tables, pg_attribute
└── Current Database: current_database()
```

#### Microsoft SQL Server Issues
```
Injection Tab:
├── DBMS: MSSQL
├── Multiple Statements: ✓
├── Stacked Test: ✓
└── Tamper Scripts: space2comment, charencode

Enumeration Tab:
├── Database: master
├── Table: sys.tables, sys.columns
└── System Database: master
```

#### Oracle Issues
```
Injection Tab:
├── DBMS: Oracle
├── Union Character: NULL
└── Tamper Scripts: space2comment, randomcase

Enumeration Tab:
├── Database: ALL_TABLES, ALL_TAB_COLUMNS
├── Table: USER_TABLES
└── System Database: SYS
```

### Issue 6: Data Extraction Problems

**Symptoms:**
- Incomplete data dumps
- Large table extraction failures
- Memory issues during extraction
- Encoding problems

**Solutions:**

#### Large Dataset Handling
```
Enumeration Tab:
├── Start from Entry: 1
├── Stop at Entry: 10000 (limit chunk size)
├── Threads: 2-5 (parallel processing)
└── Count: ✓ (get total records first)

General Tab:
├── Batch: ✓ (automated processing)
├── Output Directory: ./extraction_output/
├── CSV Format: ✓
└── Threads: 3-5
```

#### Memory Optimization
```
General Tab:
├── Chunk Size: 1000 (records per chunk)
├── Memory Limit: 512MB
└── Temp Directory: /tmp/sqlmap_temp/
```

#### Encoding Issues
```
General Tab:
├── Charset: UTF-8 or target-specific encoding
├── Hex: ✓ (for binary data)
└── Safe Charset: ✓ (for problematic characters)
```

### Issue 7: Authentication and Session Issues

**Symptoms:**
- Session expiration during testing
- Authentication bypass failures
- Cookie handling problems
- Multi-factor authentication blocking

**Solutions:**

#### Session Management
```
Request Tab:
├── Safe URL: http://target.com/keepalive.php
├── Safe POST: session_refresh=1
├── Safe Freq: 300 (5 minutes)
└── Keep Alive: ✓

Target Tab:
├── Cookie: session_id=valid_session_value
├── Cookie Delimiter: ;
└── Drop Set Cookie: ✓
```

#### Authentication Bypass
```
Miscellaneous Tab:
├── Auth Type: Basic/Digest/NTLM
├── Auth Cred: username:password
├── Auth File: /path/to/auth_file.txt
└── Ignore Auth: ✓ (for testing auth bypass)
```

#### Multi-Factor Authentication
```
Request Tab:
├── 2FA Code: 123456 (if known)
├── 2FA Method: TOTP/HOTP
└── 2FA Delay: 30 (seconds between attempts)
```

### Issue 8: File System and OS Access Issues

**Symptoms:**
- File upload/download failures
- OS command execution errors
- Privilege escalation problems
- Web shell deployment issues

**Solutions:**

#### File System Access
```
File System Tab:
├── Read File: /etc/passwd
├── Write Local File: ./local_file.txt
├── Destination: /var/www/html/uploaded.php
├── Check File: /var/www/html/uploaded.php
└── Overwrite: ✓
```

#### OS Command Execution
```
OS Access Tab:
├── OS Command: whoami && id && uname -a
├── Interactive Shell: ✓
├── Shell: /bin/bash or /bin/sh
├── OS: Linux/Windows
└── Architecture: x86/x64
```

#### Privilege Escalation
```
UDF Tab:
├── UDF Drop: ✓
├── Shared Library: /path/to/udf_library.so
├── UDF Exec: sys_exec
├── UDF Args: 'command to execute'
└── DBMS: MySQL/PostgreSQL
```

### Issue 9: Log and Output Issues

**Symptoms:**
- Missing log files
- Incomplete output
- Log rotation problems
- Output formatting issues

**Solutions:**

#### Logging Configuration
```
General Tab:
├── Verbose Level: 2-4 (detailed logging)
├── Log File: ./sqlmap_log.txt
├── Output Directory: ./sqlmap_output/
├── HTML Format: ✓
├── CSV Format: ✓
└── JSON Format: ✓
```

#### Log Rotation
```
General Tab:
├── Log Rotation: ✓
├── Max Log Size: 10MB
├── Log Backup Count: 5
└── Compress Logs: ✓
```

#### Output Formatting
```
General Tab:
├── Table Format: ✓ (readable tables)
├── Color: ✓ (colored output)
├── Progress Bar: ✓
└── ETA: ✓ (estimated time)
```

### Issue 10: Python and Dependency Issues

**Symptoms:**
- Import errors
- Module not found errors
- Python version compatibility issues
- PyQt6/PySide6 conflicts

**Solutions:**

#### Python Environment Setup
```bash
# Check Python version
python3 --version

# Install required packages
pip3 install PyQt6 requests beautifulsoup4 lxml

# For conda environments
conda create -n sqlmap-gui python=3.10
conda activate sqlmap-gui
pip install -r requirements.txt
```

#### Virtual Environment Issues
```bash
# Create virtual environment
python3 -m venv sqlmap_gui_env

# Activate environment
source sqlmap_gui_env/bin/activate  # Linux/Mac
sqlmap_gui_env\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

#### PyQt6 Installation Issues
```bash
# Linux
sudo apt-get install python3-pyqt6 python3-pyqt6.qtwidgets

# macOS
brew install pyqt6

# Windows
pip install PyQt6
```

## 🔧 Advanced Troubleshooting

### Debug Mode Configuration
```python
# Enable debug logging in main_window.py
import logging
logging.basicConfig(level=logging.DEBUG,
                   filename='sqlmap_gui_debug.log',
                   format='%(asctime)s - %(levelname)s - %(message)s')
```

### Performance Profiling
```python
# Add to main_window.py for performance monitoring
import cProfile
import pstats

def profile_function(func):
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        result = func(*args, **kwargs)
        pr.disable()
        ps = pstats.Stats(pr)
        ps.sort_stats('cumulative').print_stats(10)
        return result
    return wrapper
```

### Memory Leak Detection
```python
# Add to main_window.py
import tracemalloc

tracemalloc.start()
# ... application code ...
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage: {current / 1024 / 1024:.1f} MB")
print(f"Peak memory usage: {peak / 1024 / 1024:.1f} MB")
```

### Network Debugging
```bash
# Use tcpdump to monitor network traffic
sudo tcpdump -i eth0 -w sqlmap_traffic.pcap host target.com

# Use Wireshark to analyze captured traffic
wireshark sqlmap_traffic.pcap
```

### SQLmap Core Debugging
```bash
# Run sqlmap with debug options
sqlmap -u "http://target.com/vuln.php?id=1" --debug --proxy=http://127.0.0.1:8080

# Enable SQLmap verbose logging
sqlmap -u "http://target.com/vuln.php?id=1" -v 6 --log-file=sqlmap_debug.log
```

## 📞 Getting Help

### Community Support
1. **GitHub Issues**: Report bugs and request features
2. **Documentation**: Check the comprehensive docs in `/docs/`
3. **Examples**: Review the example configurations in `/docs/examples/`

### Professional Support
1. **Security Consulting**: For complex enterprise environments
2. **Training**: SQL injection and web security training
3. **Custom Development**: Tailored solutions for specific needs

### Emergency Issues
- **Security Vulnerabilities**: Report via GitHub Security tab
- **Data Breaches**: Contact appropriate authorities
- **Legal Issues**: Consult legal professionals immediately

## 🚀 Prevention Best Practices

### Code Quality
- **Input Validation**: Implement proper input sanitization
- **Parameterized Queries**: Use prepared statements
- **Stored Procedures**: Avoid dynamic SQL when possible
- **Least Privilege**: Run database with minimal permissions

### Security Testing
- **Regular Scanning**: Automated vulnerability scanning
- **Penetration Testing**: Professional security assessments
- **Code Reviews**: Security-focused code review process
- **Training**: Developer security awareness training

### Monitoring and Response
- **Logging**: Comprehensive security event logging
- **Alerting**: Real-time security incident alerting
- **Incident Response**: Documented breach response procedures
- **Backup**: Regular data backups and recovery testing

---

## 📋 Quick Reference

### Most Common Fixes
1. **Performance Issues**: Enable Performance Mode, clear logs
2. **Detection Problems**: Adjust level/risk, use tamper scripts
3. **Connection Issues**: Configure proxy, adjust timeouts
4. **Database Issues**: Select correct DBMS, check privileges
5. **Authentication**: Use safe URLs, manage sessions

### Emergency Commands
```bash
# Stop all running processes
pkill -f sqlmap

# Clear temporary files
rm -rf /tmp/sqlmap*

# Reset GUI settings
rm ~/.config/sqlmap-gui/settings.json

# Check system resources
top -p $(pgrep python3)
```

Remember: When in doubt, start with the basics - check your configuration, validate your target, and test with simple payloads before moving to complex techniques.</content>
<parameter name="filePath">/home/devil/Desktop/SQLmap-GUI-Advanced-SQL-Injection-Testing-Interface/docs/troubleshooting.md
