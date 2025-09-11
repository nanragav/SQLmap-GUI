# General Tab - Output Formatting, Logging, and General Options

The General tab controls output formatting, logging behavior, verbosity levels, and other general SQLmap options that affect how results are displayed and stored.

## 📋 Overview

The General tab contains four main sections:
1. **Output Control** - Result formatting and display options
2. **Logging Options** - Log file configuration and management
3. **Verbosity Settings** - Detail level of output information
4. **General Configuration** - Miscellaneous SQLmap settings

## 📝 Output Control Options

### Output Directory
**Parameter:** `--output-dir=DIR`
**Description:** Custom output directory for all SQLmap results
**Default:** `./output/`
**Examples:**
```
--output-dir=/path/to/results/
--output-dir=C:\sqlmap_results\
--output-dir=./pentest_output/
```
**Use Cases:**
- Organized result storage
- Multi-target testing
- Report generation
- Evidence collection

### Output File Prefix
**Parameter:** `--output-prefix=PREFIX`
**Description:** Prefix for output files
**Examples:**
```
--output-prefix=target1_
--output-prefix=client_project_
--output-prefix=test_run_
```
**Use Cases:**
- File organization
- Multiple scan differentiation
- Automated processing

### Save Everything to File
**Parameter:** `--save=SAVE_CONFIG`
**Description:** Save all command output to files
**Behavior:** Saves all output including errors and warnings
**Use Cases:**
- Complete audit trails
- Debugging information
- Compliance reporting

### CSV Format Output
**Parameter:** `--csv`
**Description:** Save dump data in CSV format
**Behavior:** Exports database dumps as CSV files
**Use Cases:**
- Data analysis
- Spreadsheet import
- Reporting tools
- Database migration

### HTML Format Output
**Parameter:** `--html`
**Description:** Save output in HTML format
**Behavior:** Generates HTML reports
**Use Cases:**
- Web-based reporting
- Executive summaries
- Client presentations
- Documentation

## 📄 Logging Options

### Log File
**Parameter:** `--log-file=FILE`
**Description:** Log all HTTP traffic and errors to file
**Examples:**
```
--log-file=/var/log/sqlmap.log
--log-file=C:\logs\sqlmap_debug.log
--log-file=./session.log
```
**Use Cases:**
- Session recording
- Debugging analysis
- Audit trails
- Error tracking

### Flush Session File
**Parameter:** `--flush-session`
**Description:** Flush session file for current target
**Behavior:** Clears stored session data
**Use Cases:**
- Fresh scan start
- Cache clearing
- Memory management
- State reset

### Session File
**Parameter:** `--session-file=FILE`
**Description:** Load/save session data from/to file
**Examples:**
```
--session-file=./target.session
--session-file=/sessions/client1.sql
--session-file=C:\temp\scan_state.dat
```
**Use Cases:**
- Scan resumption
- State persistence
- Multi-session testing
- Progress tracking

### Save Configuration
**Parameter:** `--save-config=FILE`
**Description:** Save current configuration to file
**Examples:**
```
--save-config=./my_config.conf
--save-config=/configs/advanced_scan.ini
--save-config=C:\sqlmap\settings.cfg
```
**Use Cases:**
- Configuration backup
- Reusable settings
- Team sharing
- Automation scripts

### Load Configuration
**Parameter:** `--load-config=FILE`
**Description:** Load configuration from file
**Examples:**
```
--load-config=./production.conf
--load-config=/configs/pentest.ini
--load-config=C:\sqlmap\default.cfg
```
**Use Cases:**
- Standardized testing
- Environment-specific settings
- Quick configuration switching

## 🔊 Verbosity Settings

### Verbose Level
**Parameter:** `-v LEVEL`
**Description:** Verbosity level (0-6)
**Levels:**
- **0**: Only Python tracebacks, errors, and critical messages
- **1**: Also warnings
- **2**: Also informational messages
- **3**: Also debug messages
- **4**: Also payload injections
- **5**: Also HTTP requests
- **6**: Also HTTP responses (very verbose)

**Examples:**
```
-v 0  # Minimal output
-v 3  # Standard debugging
-v 6  # Maximum verbosity
```
**Use Cases:**
- Debugging issues
- Learning SQL injection
- Detailed analysis
- Troubleshooting

### Suppress Output
**Parameter:** `--suppress-suppress`
**Description:** Suppress unimportant output
**Behavior:** Reduces noise in output
**Use Cases:**
- Clean reports
- Automated processing
- Large-scale scanning

### Progress Bar
**Parameter:** `--progress-bar`
**Description:** Display progress bar
**Behavior:** Shows scan progress visually
**Use Cases:**
- Long-running scans
- User feedback
- Time estimation

## ⚙️ General Configuration Options

### Batch Mode
**Parameter:** `--batch`
**Description:** Never ask for user input, use defaults
**Behavior:** Automated execution with default values
**Use Cases:**
- Automated scanning
- CI/CD integration
- Unattended execution
- Script integration

### Interactive Mode
**Parameter:** `--interactive`
**Description:** Interactive mode for advanced users
**Behavior:** Prompts for advanced options
**Use Cases:**
- Expert analysis
- Custom configurations
- Learning purposes

### Wizard Mode
**Parameter:** `--wizard`
**Description:** Simple wizard interface
**Behavior:** Guided setup for beginners
**Use Cases:**
- First-time users
- Quick assessments
- Educational purposes

### Update SQLmap
**Parameter:** `--update`
**Description:** Update SQLmap to latest version
**Behavior:** Downloads and installs latest release
**Use Cases:**
- Staying current
- Bug fixes
- New features
- Security updates

### Check for Updates
**Parameter:** `--check-update`
**Description:** Check for SQLmap updates
**Behavior:** Checks version without updating
**Use Cases:**
- Version verification
- Update planning
- Compatibility checking

### Purge Output Directory
**Parameter:** `--purge-output`
**Description:** Safely remove all content from output directory
**Behavior:** Cleans output directory
**Use Cases:**
- Disk space management
- Clean environment
- Privacy protection

### Cleanup
**Parameter:** `--cleanup`
**Description:** Clean up SQLmap temporary files
**Behavior:** Removes temporary files and cache
**Use Cases:**
- Disk cleanup
- Memory management
- System maintenance

## 📊 Output Formatting Examples

### Standard Output with Logging
```
Output Directory: /pentest/results/
Log File: /pentest/results/scan.log
Verbose Level: 3
Save Everything: ✓ Enabled
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/page.php?id=1" --output-dir=/pentest/results/ --log-file=/pentest/results/scan.log -v 3 --save
```

### CSV Export for Data Analysis
```
CSV Format: ✓ Enabled
Output Directory: ./data_export/
Output Prefix: client_data_
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/db.php?id=1" --csv --output-dir=./data_export/ --output-prefix=client_data_
```

### HTML Report Generation
```
HTML Format: ✓ Enabled
Output Directory: /reports/
Verbose Level: 2
Progress Bar: ✓ Enabled
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/admin.php?id=1" --html --output-dir=/reports/ -v 2 --progress-bar
```

### Session Management
```
Session File: ./target_session.sql
Load Config: ./advanced_config.conf
Batch Mode: ✓ Enabled
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/page.php?id=1" --session-file=./target_session.sql --load-config=./advanced_config.conf --batch
```

### Maximum Verbosity for Debugging
```
Verbose Level: 6
Log File: ./debug.log
Save Config: ./debug_config.conf
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/debug.php?id=1" -v 6 --log-file=./debug.log --save-config=./debug_config.conf
```

## ⚠️ Important Considerations

### Output Management
- **Disk space**: Large dumps can consume significant space
- **File organization**: Use descriptive prefixes and directories
- **Privacy**: Output may contain sensitive information
- **Backup**: Important results should be backed up

### Logging Strategy
- **Log rotation**: Large log files can become unmanageable
- **Log levels**: Choose appropriate verbosity for the task
- **Security**: Logs may contain sensitive information
- **Retention**: Consider log retention policies

### Performance Impact
- **Verbose output**: Higher verbosity levels slow down scanning
- **File I/O**: Writing to files adds overhead
- **Memory usage**: Large outputs consume memory
- **Network impact**: Verbose HTTP logging increases traffic

### Configuration Management
- **Version control**: Track configuration changes
- **Security**: Configurations may contain sensitive data
- **Sharing**: Be careful sharing configurations
- **Validation**: Test configurations before production use

## 🔧 Troubleshooting

### Output Directory Issues
**Problem:** Cannot write to output directory
**Solutions:**
1. Check directory permissions
2. Create directory if it doesn't exist
3. Use absolute paths
4. Check disk space

### Log File Problems
**Problem:** Logging not working properly
**Solutions:**
1. Verify file permissions
2. Check disk space
3. Use absolute paths
4. Test with simple log file

### Verbosity Too High/Low
**Problem:** Output level not suitable for task
**Solutions:**
1. Adjust -v level appropriately
2. Use --suppress-suppress for clean output
3. Redirect output to files for analysis
4. Use --batch for automated runs

### Configuration Loading Issues
**Problem:** Configuration files not loading
**Solutions:**
1. Verify file path and permissions
2. Check configuration file format
3. Test with simple configuration
4. Validate configuration syntax

### Memory/Resource Issues
**Problem:** High memory usage with verbose output
**Solutions:**
1. Reduce verbosity level
2. Use file output instead of console
3. Limit output size
4. Monitor system resources

### File Organization Problems
**Problem:** Output files disorganized
**Solutions:**
1. Use --output-prefix for naming
2. Create structured directory hierarchy
3. Use --output-dir for organization
4. Implement post-processing scripts

## 📚 Related Tabs

- **[Target Tab](target.md)**: Target specification and configuration
- **[Request Tab](request.md)**: HTTP request customization
- **[Enumeration Tab](enumeration.md)**: Database structure discovery
- **[Injection Tab](injection.md)**: Parameter selection and payload customization</content>
<parameter name="filePath">/home/devil/Desktop/SQLmap-GUI-Advanced-SQL-Injection-Testing-Interface/docs/tabs/general.md
