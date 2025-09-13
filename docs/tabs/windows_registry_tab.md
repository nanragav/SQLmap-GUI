# Windows Registry Tab - Windows Registry Access and Manipulation

The Windows Registry tab controls how SQLmap accesses and manipulates the Windows registry on target systems, enabling registry key reading, writing, and system configuration changes.

## 📋 Overview

The Windows Registry tab contains three main sections:
1. **Registry Reading** - Read registry keys and values
2. **Registry Writing** - Write to registry keys and values
3. **Registry Operations** - Advanced registry operations

## 📖 Registry Reading Options

### Read a Windows Registry Key Value
**Parameter:** `--reg-read`
**Description:** Read a Windows registry key value
**Behavior:** Retrieves registry key data from the target system
**Examples:**
```
--reg-read="HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
--reg-read="HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer"
--reg-read="HKLM\SYSTEM\CurrentControlSet\Services"
```
**Use Cases:**
- System configuration analysis
- Software installation tracking
- Security settings review
- Startup program enumeration

### Registry Key Path
**Parameter:** `--reg-key=KEY_PATH`
**Description:** Specify the registry key path to read
**Format:** `HKEY\Path\To\Key`
**Examples:**
```
--reg-key="HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion"
--reg-key="HKCU\Software\Classes"
--reg-key="HKLM\SYSTEM\CurrentControlSet\Control"
```
**Use Cases:**
- Specific key targeting
- Hierarchical navigation
- Configuration analysis

### Registry Value Name
**Parameter:** `--reg-val=VALUE_NAME`
**Description:** Specify the registry value name to read
**Examples:**
```
--reg-val="ProductName"
--reg-val="InstallDate"
--reg-val="SystemRoot"
--reg-val="ProgramFilesDir"
```
**Use Cases:**
- Specific value extraction
- Configuration parameter reading
- System information gathering

## ✏️ Registry Writing Options

### Write to a Windows Registry Key Value
**Parameter:** `--reg-write`
**Description:** Write a value to a Windows registry key
**Behavior:** Modifies or creates registry entries
**Examples:**
```
--reg-write --reg-key="HKCU\Software\MyApp" --reg-val="Setting" --reg-data="Value"
--reg-write --reg-key="HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" --reg-val="MyProgram" --reg-data="C:\program.exe"
```
**Use Cases:**
- Configuration modification
- Startup entry creation
- System settings changes
- Persistence mechanism setup

### Registry Data to Write
**Parameter:** `--reg-data=DATA`
**Description:** Data to write to the registry value
**Examples:**
```
--reg-data="C:\Windows\System32\cmd.exe"
--reg-data="1"
--reg-data="Enabled"
--reg-data="192.168.1.100"
```
**Use Cases:**
- Executable paths
- Configuration values
- IP addresses
- Settings and preferences

### Registry Data Type
**Parameter:** `--reg-type=TYPE`
**Description:** Data type for the registry value
**Supported Types:**
- **REG_SZ**: String value (default)
- **REG_DWORD**: 32-bit integer
- **REG_QWORD**: 64-bit integer
- **REG_BINARY**: Binary data
- **REG_MULTI_SZ**: Multi-string value
- **REG_EXPAND_SZ**: Expandable string

**Examples:**
```
--reg-type=REG_SZ --reg-data="Hello World"
--reg-type=REG_DWORD --reg-data="1"
--reg-type=REG_BINARY --reg-data="DEADBEEF"
```
**Use Cases:**
- Type-specific data storage
- System compatibility
- Application requirements

## 🔧 Advanced Registry Operations

### Add to Windows Registry Key
**Parameter:** `--reg-add`
**Description:** Add a new registry key
**Behavior:** Creates new registry keys
**Examples:**
```
--reg-add --reg-key="HKCU\Software\NewApp"
--reg-add --reg-key="HKLM\SOFTWARE\Company\Product"
```
**Use Cases:**
- Application configuration setup
- Software installation simulation
- Registry structure creation

### Delete Windows Registry Key
**Parameter:** `--reg-del`
**Description:** Delete a registry key or value
**Behavior:** Removes registry entries
**Examples:**
```
--reg-del --reg-key="HKCU\Software\OldApp"
--reg-del --reg-key="HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" --reg-val="Malware"
```
**Use Cases:**
- Cleanup operations
- Malware removal
- Configuration reset
- System maintenance

### Enumerate Windows Registry Keys
**Parameter:** `--reg-enum`
**Description:** Enumerate registry keys and subkeys
**Behavior:** Lists registry key contents
**Examples:**
```
--reg-enum --reg-key="HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
--reg-enum --reg-key="HKCU\Software"
```
**Use Cases:**
- Software inventory
- System configuration discovery
- Registry structure analysis

## 📊 Common Registry Locations

### System Information
```
HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion
HKLM\HARDWARE\DESCRIPTION\System
HKLM\SYSTEM\CurrentControlSet\Control
```

### Software Inventory
```
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall
HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall
HKLM\SOFTWARE\Classes\Installer\Products
```

### Startup Programs
```
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
HKCU\Software\Microsoft\Windows\CurrentVersion\Run
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce
```

### Security Settings
```
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies
HKCU\Software\Microsoft\Windows\CurrentVersion\Policies
HKLM\SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy
```

### User Information
```
HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer
HKCU\Software\Classes
HKCU\Software\Microsoft\Internet Explorer
```

## 📝 Usage Examples

### Read System Information
```
Registry Key: HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion
Registry Value: ProductName
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/page.php?id=1" --reg-read --reg-key="HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion" --reg-val="ProductName"
```

### Check Installed Software
```
Registry Key: HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall
Enumerate: ✓ Enabled
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/admin.php?id=1" --reg-enum --reg-key="HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
```

### Add Startup Program
```
Registry Key: HKCU\Software\Microsoft\Windows\CurrentVersion\Run
Registry Value: MyApp
Registry Data: C:\Program Files\MyApp\app.exe
Registry Type: REG_SZ
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/startup.php?id=1" --reg-write --reg-key="HKCU\Software\Microsoft\Windows\CurrentVersion\Run" --reg-val="MyApp" --reg-data="C:\Program Files\MyApp\app.exe" --reg-type=REG_SZ
```

### Read Firewall Settings
```
Registry Key: HKLM\SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\DomainProfile
Registry Value: EnableFirewall
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/firewall.php?id=1" --reg-read --reg-key="HKLM\SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\DomainProfile" --reg-val="EnableFirewall"
```

### Create Registry Key
```
Registry Key: HKCU\Software\MyCompany\MyApp
Add Key: ✓ Enabled
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/create.php?id=1" --reg-add --reg-key="HKCU\Software\MyCompany\MyApp"
```

### Delete Registry Value
```
Registry Key: HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
Registry Value: OldProgram
Delete: ✓ Enabled
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/cleanup.php?id=1" --reg-del --reg-key="HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" --reg-val="OldProgram"
```

### Enumerate User Software
```
Registry Key: HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall
Enumerate: ✓ Enabled
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/software.php?id=1" --reg-enum --reg-key="HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall"
```

## ⚠️ Important Considerations

### Registry Permissions
- **Administrator privileges**: Most registry operations require admin rights
- **User vs System hive**: HKCU vs HKLM access differences
- **Access control**: Registry keys have ACLs (Access Control Lists)
- **Virtualization**: Some keys may be virtualized for compatibility

### Registry Structure
- **Hierarchical organization**: Keys contain subkeys and values
- **Data types**: Different value types for different data
- **Case sensitivity**: Registry is case-insensitive but preserves case
- **Backup considerations**: Registry changes can affect system stability

### System Impact
- **Critical keys**: Modifying system keys can crash the system
- **Startup impact**: Changes to Run keys affect boot time
- **Security implications**: Registry changes can disable security features
- **Rollback capability**: Some changes may require system restore

### Performance Considerations
- **Registry size**: Large registry enumerations can be slow
- **Memory usage**: Loading large registry hives consumes memory
- **Network latency**: Remote registry access affected by network
- **Concurrent access**: Multiple processes accessing registry simultaneously

## 🔧 Troubleshooting

### Access Denied Errors
**Problem:** Registry operations failing due to permissions
**Solutions:**
1. Verify administrator privileges
2. Check registry key permissions
3. Try HKCU instead of HKLM
4. Use privilege escalation techniques

### Key Not Found
**Problem:** Specified registry key doesn't exist
**Solutions:**
1. Verify key path spelling
2. Check if key exists on target system
3. Use --reg-enum to explore structure
4. Try different registry paths

### Invalid Data Type
**Problem:** Registry data type mismatch
**Solutions:**
1. Verify correct data type for value
2. Check existing value type
3. Use appropriate --reg-type parameter
4. Convert data to correct format

### System Instability
**Problem:** Registry changes causing system issues
**Solutions:**
1. Create system restore point first
2. Test changes in virtual environment
3. Make incremental changes
4. Have backup/rollback plan

### Remote Registry Issues
**Problem:** Remote registry access not working
**Solutions:**
1. Verify Remote Registry service status
2. Check firewall settings
3. Ensure proper authentication
4. Test local registry access first

### Performance Problems
**Problem:** Registry operations taking too long
**Solutions:**
1. Limit enumeration scope
2. Use specific key paths instead of broad searches
3. Close unnecessary registry handles
4. Monitor system resources

## 📚 Related Tabs

- **[OS Access Tab](os_access_tab.md)**: Operating system command execution
- **[File System Tab](file_system_tab.md)**: File system operations
- **[Enumeration Tab](enumeration_tab.md)**: Database structure discovery
- **[General Tab](general_tab.md)**: Output and logging options</content>
<parameter name="filePath">/home/devil/Desktop/SQLmap-GUI-Advanced-SQL-Injection-Testing-Interface/docs/tabs/windows_registry.md
