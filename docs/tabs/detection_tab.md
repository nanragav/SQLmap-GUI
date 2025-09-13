# Detection Tab - SQL Injection Detection Configuration

The Detection tab controls how SQLmap detects and confirms SQL injection vulnerabilities, including detection levels, risk levels, and specific injection techniques.

## 📋 Overview

The Detection tab contains three main sections:
1. **Detection Level** - How thorough the detection should be
2. **Risk Level** - How aggressive the payloads should be
3. **Techniques** - Which injection techniques to use

## 🎯 Detection Level Options

### Detection Level
**Parameter:** `--level=LEVEL`
**Description:** Level of tests to perform (1-5)
**Default:** 1 (fastest, least thorough)

#### Level Details:

**Level 1 (Fastest):**
- Tests basic injection points
- Uses simple payloads
- Minimal false positives
- **Use Case:** Quick vulnerability assessment

**Level 2:**
- Tests more injection points
- Includes HTTP headers (Cookie, User-Agent, Referer)
- Adds basic time-based payloads
- **Use Case:** Standard web application testing

**Level 3:**
- Tests additional HTTP headers
- Includes more complex payloads
- Adds error-based detection
- **Use Case:** Thorough vulnerability detection

**Level 4:**
- Tests all HTTP headers
- Includes advanced payloads
- Adds heavy query payloads
- **Use Case:** Comprehensive security audit

**Level 5 (Slowest):**
- Tests all possible injection points
- Includes all payload variations
- Maximum detection coverage
- **Use Case:** Penetration testing with high confidence

### Risk Level
**Parameter:** `--risk=RISK`
**Description:** Risk of tests to perform (1-3)
**Default:** 1 (safest, least intrusive)

#### Risk Details:

**Risk 1 (Safest):**
- Uses safe, non-destructive payloads
- Minimal impact on target system
- Lowest false positive rate
- **Use Case:** Production environment testing

**Risk 2:**
- Uses potentially harmful payloads
- May cause temporary service disruption
- Higher detection rate
- **Use Case:** Staging/development testing

**Risk 3 (Most Aggressive):**
- Uses highly dangerous payloads
- May cause permanent damage
- Highest detection rate
- **Use Case:** Controlled testing environment only

## 💉 Injection Techniques

### Boolean-Based Blind
**Parameter:** `--technique=B`
**Description:** Use boolean-based blind SQL injection
**How it works:** Compares true/false responses
**Examples:**
- `AND 1=1` (true condition)
- `AND 1=2` (false condition)
**Detection:** Different responses for true vs false

### Error-Based
**Parameter:** `--technique=E`
**Description:** Use error-based SQL injection
**How it works:** Forces database errors to leak information
**Examples:**
- Division by zero: `AND 1/0`
- Invalid conversion: `AND 'a'='b'`
**Detection:** Database error messages in response

### Union Query-Based
**Parameter:** `--technique=U`
**Description:** Use union query SQL injection
**How it works:** Appends UNION SELECT to original query
**Examples:**
- `UNION SELECT NULL,NULL`
- `UNION SELECT 1,2,3`
**Detection:** Additional columns in result set

### Stacked Queries
**Parameter:** `--technique=S`
**Description:** Use stacked queries SQL injection
**How it works:** Executes multiple queries in one request
**Examples:**
- `; SELECT * FROM users; --`
- `; DROP TABLE temp; --`
**Detection:** Multiple query execution

### Time-Based Blind
**Parameter:** `--technique=T`
**Description:** Use time-based blind SQL injection
**How it works:** Uses time delays to infer information
**Examples:**
- `AND IF(1=1, SLEEP(5), 0)`
- `AND 1=IF(2>1, SLEEP(5), 0)`
**Detection:** Response time differences

### Inline Queries
**Parameter:** `--technique=Q`
**Description:** Use inline query SQL injection
**How it works:** Injects subqueries within the main query
**Examples:**
- `(SELECT * FROM users)`
- `(SELECT COUNT(*) FROM admin)`
**Detection:** Subquery results in response

## 🔧 Advanced Detection Options

### Page Comparison
**Parameter:** `--string=STRING`
**Description:** String to match when query is evaluated to True
**Example:** `--string="Welcome back"`
**Use Case:** Custom true condition detection

### Page Comparison (False)
**Parameter:** `--not-string=STRING`
**Description:** String to match when query is evaluated to False
**Example:** `--not-string="Access denied"`
**Use Case:** Custom false condition detection

### Page Comparison (Regular Expression)
**Parameter:** `--regexp=REGEXP`
**Description:** Regular expression to match when query is evaluated to True
**Example:** `--regexp="Welcome.*admin"`
**Use Case:** Pattern-based detection

### Page Comparison (Regular Expression - False)
**Parameter:** `--not-regexp=REGEXP`
**Description:** Regular expression to match when query is evaluated to False
**Example:** `--not-regexp="Error.*denied"`
**Use Case:** Pattern-based false detection

### HTTP Code to Match When Query is Evaluated to True
**Parameter:** `--code=CODE`
**Description:** HTTP status code indicating true condition
**Example:** `--code=200`
**Use Case:** Status code-based detection

### Titles to Match When Query is Evaluated to True
**Parameter:** `--titles`
**Description:** Match HTML page titles for true conditions
**Use Case:** Title-based blind detection

### Texts to Match When Query is Evaluated to True
**Parameter:** `--texts`
**Description:** Match HTML body text for true conditions
**Use Case:** Content-based blind detection

## 📝 Usage Examples

### Basic Detection Configuration
```
Detection Level: 3
Risk Level: 2
Techniques: BEUSTQ (All enabled)
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/page.php?id=1" --level=3 --risk=2 --technique=BEUSTQ
```

### Conservative Production Testing
```
Detection Level: 2
Risk Level: 1
Techniques: BEU (Boolean, Error, Union)
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/product.php?id=1" --level=2 --risk=1 --technique=BEU
```

### Aggressive Penetration Testing
```
Detection Level: 5
Risk Level: 3
Techniques: BEUSTQ (All enabled)
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/admin.php?id=1" --level=5 --risk=3 --technique=BEUSTQ
```

### Custom Response Detection
```
Detection Level: 3
Risk Level: 2
String Match: "Welcome admin"
Not String Match: "Access denied"
Techniques: BT (Boolean, Time-based)
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/login.php?id=1" --level=3 --risk=2 --string="Welcome admin" --not-string="Access denied" --technique=BT
```

### Time-Based Only Detection
```
Detection Level: 4
Risk Level: 2
Techniques: T (Time-based only)
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/search.php?q=test" --level=4 --risk=2 --technique=T
```

## ⚠️ Important Considerations

### Detection Level Selection
- **Level 1-2**: Use for production environments
- **Level 3-4**: Use for thorough testing
- **Level 5**: Use only when necessary (very slow)
- **Higher levels**: More comprehensive but slower

### Risk Level Selection
- **Risk 1**: Safe for production, lowest false positives
- **Risk 2**: Balanced approach, moderate impact
- **Risk 3**: Aggressive, may cause issues
- **Consider target environment** before selecting

### Technique Selection
- **Start with BEU**: Most common and reliable
- **Add T for blind**: When other techniques fail
- **Use S carefully**: Stacked queries can be destructive
- **Q for advanced**: Inline queries are less common

### Custom Detection Strings
- **Use unique strings**: Avoid generic content
- **Test manually first**: Verify strings work as expected
- **Consider encoding**: URL encoding may be needed
- **Multiple strings**: Use regex for complex patterns

## 🔧 Troubleshooting

### No Vulnerabilities Detected
**Problem:** SQLmap reports no injection points
**Solutions:**
1. Increase detection level: `--level=5`
2. Enable more techniques: `--technique=BEUSTQ`
3. Increase risk level: `--risk=3`
4. Check custom strings: `--string="unique content"`

### False Positives
**Problem:** SQLmap reports vulnerabilities that don't exist
**Solutions:**
1. Decrease risk level: `--risk=1`
2. Use specific techniques: `--technique=BEU`
3. Add exclusion strings: `--not-string="error"`
4. Verify manually with different tools

### Slow Detection
**Problem:** Detection phase takes too long
**Solutions:**
1. Reduce detection level: `--level=2`
2. Limit techniques: `--technique=BE`
3. Use batch processing: `--batch`
4. Focus on specific parameters: `-p param`

### WAF Blocking Detection
**Problem:** Web Application Firewall blocks detection payloads
**Solutions:**
1. Use tamper scripts: `--tamper=space2comment`
2. Reduce detection level temporarily
3. Try different techniques
4. Use custom prefix/suffix

### Time-Based Detection Issues
**Problem:** Time-based detection unreliable or slow
**Solutions:**
1. Adjust time delays: `--time-sec=10`
2. Check network latency
3. Use different time functions
4. Switch to other techniques

## 📚 Related Tabs

- **[Injection Tab](injection_tab.md)**: Parameter selection and payload customization
- **[Techniques Tab](techniques_tab.md)**: Advanced technique configuration
- **[Target Tab](target_tab.md)**: Target specification and configuration
- **[Request Tab](request_tab.md)**: HTTP request customization</content>
<parameter name="filePath">/home/devil/Desktop/SQLmap-GUI-Advanced-SQL-Injection-Testing-Interface/docs/tabs/detection.md
