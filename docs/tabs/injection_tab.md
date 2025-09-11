# Injection Tab - SQL Injection Payload Configuration

The Injection tab controls how SQL injection payloads are crafted and delivered, including parameter selection, DBMS targeting, payload customization, and tamper scripts for WAF bypass.

## 📋 Overview

The Injection tab contains three main sections:
1. **Parameter Testing** - Which parameters to test and how
2. **Injection Options** - Payload customization and invalidation
3. **Payload Customization** - Prefix/suffix configuration

## 🎯 Parameter Testing Options

### Testable Parameter(s)
**Parameter:** `-p PARAMS, --testable=PARAMS`
**Description:** Specify which parameters to test for SQL injection
**Format:** Comma-separated parameter names
**Examples:**
```
id,user,password
username,email,phone
param1,param2,param3
```
**Notes:**
- If not specified, all parameters are tested
- Useful for large forms with many parameters
- Reduces scan time by focusing on specific parameters

### Skip Testing Parameter(s)
**Parameter:** `--skip=PARAMS`
**Description:** Parameters to exclude from testing
**Format:** Comma-separated parameter names
**Examples:**
```
csrf_token,session_id
timestamp,nonce
captcha_code,verification
```
**Use Cases:**
- Known safe parameters (CSRF tokens, timestamps)
- Parameters that cause issues when tested
- Large parameters that slow down scanning

### Skip Testing Parameters with Static Values
**Parameter:** `--skip-static`
**Description:** Skip parameters with unchanging values
**Behavior:**
- Identifies parameters with identical values across requests
- Automatically excludes them from testing
- Reduces false positives from static content

### Force Back-end DBMS
**Parameter:** `--dbms=DBMS`
**Description:** Specify target database management system
**Supported DBMS:**
- **MySQL**: Most common web database
- **PostgreSQL**: Advanced open-source database
- **Microsoft SQL Server**: Enterprise Windows database
- **Oracle**: Enterprise database system
- **SQLite**: Lightweight embedded database
- **Microsoft Access**: Desktop database
- **Firebird**: Open-source relational database
- **IBM DB2**: Enterprise database platform
- **SAP MaxDB**: SAP's database system
- **Sybase**: Legacy enterprise database
- **Informix**: IBM's database system
- **HSQLDB**: Java-based database
- **H2**: Java SQL database
- **MariaDB**: MySQL fork with enhancements

### Force Back-end OS
**Parameter:** `--os=OS`
**Description:** Specify target operating system
**Options:**
- **Linux**: Most common web server OS
- **Windows**: Windows-based servers
- **Unix**: Generic Unix-like systems

## 💉 Injection Options

### Use Big Numbers for Invalidating Values
**Parameter:** `--invalid-bignum`
**Description:** Use large numbers to invalidate parameter values
**Example:** `id=99999999999999999999`
**Use Case:** Bypass filters that block common invalid values

### Use Logical Operations for Invalidating Values
**Parameter:** `--invalid-logical`
**Description:** Use logical operations to create invalid values
**Examples:** `id=1 AND 1=2`, `id=1 OR 1=1`
**Use Case:** Test logical expression handling

### Use Random Strings for Invalidating Values
**Parameter:** `--invalid-string`
**Description:** Use random strings to invalidate parameter values
**Example:** `id=abcXYZ123random`
**Use Case:** Test string validation and sanitization

### Turn Off Payload Casting Mechanism
**Parameter:** `--no-cast`
**Description:** Disable automatic payload type casting
**Behavior:** Payloads remain as strings
**Use Case:** When casting interferes with injection

### Turn Off String Escaping Mechanism
**Parameter:** `--no-escape`
**Description:** Disable automatic string escaping
**Behavior:** Special characters are not escaped
**Use Case:** Manual control over escaping

### Injection Payload Prefix String
**Parameter:** `--prefix=PREFIX`
**Description:** String to prepend to injection payloads
**Examples:**
```
' OR '1'='1
'); --
' UNION SELECT
```
**Use Cases:**
- Complete broken SQL statements
- Bypass input validation
- Create valid SQL syntax

### Injection Payload Suffix String
**Parameter:** `--suffix=SUFFIX`
**Description:** String to append to injection payloads
**Examples:**
```
-- -
' AND '1'='1
' LIMIT 0,1
```
**Use Cases:**
- Close SQL statements
- Add conditions or limits
- Complete injection syntax

### Use Tamper Scripts
**Parameter:** `--tamper=TAMPERS`
**Description:** Apply tamper scripts to bypass WAF/filtering
**Format:** Comma-separated tamper names

#### Available Tamper Scripts:

**Character Encoding:**
- **apostrophemask**: Replace apostrophes with UTF-8 fullwidth
- **charencode**: URL-encode characters
- **randomcase**: Random character case

**Space Manipulation:**
- **space2comment**: Replace spaces with `/**/` comments
- **space2dash**: Replace spaces with `--` comments
- **space2hash**: Replace spaces with `#` comments
- **space2plus**: Replace spaces with `+` characters

**Keyword Obfuscation:**
- **equaltolike**: Replace `=` with `LIKE`
- **versionedkeywords**: Use MySQL versioned comment keywords

**Common Combinations:**
- **space2comment,randomcase**: Basic WAF bypass
- **apostrophemask,base64encode**: Advanced filtering bypass
- **space2comment,versionedkeywords**: MySQL-specific bypass

### Custom Tamper Scripts
**Parameter:** `--tamper=SCRIPTS`
**Description:** Use custom tamper scripts from file
**Format:** Path to Python tamper script
**Requirements:** Must follow SQLmap tamper script format

## 📝 Payload Customization

### Payload Prefix
**Parameter:** `--prefix=PREFIX`
**Description:** Custom prefix for injection payloads
**Examples:**
```
' OR
");--
' UNION SELECT NULL,
```

### Payload Suffix
**Parameter:** `--suffix=SUFFIX`
**Description:** Custom suffix for injection payloads
**Examples:**
```
-- -
AND '1'='1
LIMIT 0,1 -- -
```

## 🔍 Usage Examples

### Basic Parameter Testing
```
Testable Parameters: id,category
Skip Parameters: csrf_token
Skip Static: ✓ Enabled
DBMS: MySQL
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/product.php?id=1&category=1" -p "id,category" --skip="csrf_token" --skip-static --dbms=mysql
```

### Advanced Payload Customization
```
Prefix: ' OR
Suffix: -- -
Invalid BigNum: ✓ Enabled
Invalid Logical: ✓ Enabled
No Cast: ✓ Enabled
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/login.php?id=1" --prefix="' OR " --suffix=" -- -" --invalid-bignum --invalid-logical --no-cast
```

### WAF Bypass with Tamper Scripts
```
Tamper Scripts: space2comment,randomcase
DBMS: MySQL
OS: Linux
Prefix: ' UNION SELECT
Suffix: -- -
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/search.php?q=test" --tamper=space2comment,randomcase --dbms=mysql --os=linux --prefix="' UNION SELECT " --suffix=" -- -"
```

### Custom Parameter Selection
```
Testable Parameters: username,password,email
Skip Static: ✓ Enabled
Invalid String: ✓ Enabled
No Escape: ✓ Enabled
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/register.php" -p "username,password,email" --skip-static --invalid-string --no-escape
```

## ⚠️ Important Considerations

### Parameter Selection Strategy
- **Test all parameters first** to identify vulnerabilities
- **Use --testable** for focused testing on known parameters
- **Use --skip** for parameters known to be safe or problematic
- **Enable --skip-static** to reduce noise from static content

### DBMS Selection
- **Let SQLmap auto-detect** when possible
- **Specify DBMS only when confident** of the target
- **Wrong DBMS selection** can cause false negatives
- **Use fingerprinting** to confirm DBMS type

### Tamper Script Usage
- **Start with common scripts**: `space2comment,randomcase`
- **Test scripts individually** to identify effective ones
- **Combine scripts carefully** - some combinations conflict
- **Custom scripts** require Python knowledge

### Payload Prefix/Suffix
- **Match target syntax**: Use quotes, parentheses appropriately
- **Test manually first**: Verify prefix/suffix work with target
- **Start simple**: Use basic prefixes before complex ones
- **Consider context**: Different injection points need different syntax

## 🔧 Troubleshooting

### No Injection Points Found
**Problem:** SQLmap reports no injection vulnerabilities
**Solutions:**
1. Increase detection level: `--level=5`
2. Try different techniques: `--technique=BEUSTQ`
3. Check parameter selection: `-p param1,param2`
4. Verify target is actually vulnerable

### WAF Blocking Payloads
**Problem:** Web Application Firewall blocks injection attempts
**Solutions:**
1. Use tamper scripts: `--tamper=space2comment,randomcase`
2. Try different encodings: `--charencode`
3. Use custom prefix/suffix combinations
4. Reduce detection level temporarily

### Wrong DBMS Detected
**Problem:** SQLmap identifies wrong database type
**Solutions:**
1. Force correct DBMS: `--dbms=mysql`
2. Check with fingerprinting: `--fingerprint`
3. Verify with manual testing
4. Use `--banner` to get database version

### Payload Syntax Errors
**Problem:** Injection payloads cause SQL syntax errors
**Solutions:**
1. Adjust prefix/suffix strings
2. Use different invalidation methods
3. Check target SQL dialect
4. Test payloads manually with SQL client

## 📚 Related Tabs

- **[Detection Tab](detection.md)**: Detection level and technique configuration
- **[Techniques Tab](techniques.md)**: Injection technique selection
- **[Enumeration Tab](enumeration.md)**: Database structure discovery
- **[Fingerprint Tab](fingerprint.md)**: Database type identification</content>
<parameter name="filePath">/home/devil/Desktop/SQLmap-GUI-Advanced-SQL-Injection-Testing-Interface/docs/tabs/injection.md
