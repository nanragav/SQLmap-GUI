# Techniques Tab - Advanced SQL Injection Technique Configuration

The Techniques tab provides fine-grained control over SQL injection techniques, allowing users to customize detection methods, payload behavior, and exploitation strategies beyond the basic Detection tab options.

## 📋 Overview

The Techniques tab contains advanced options for:
1. **Technique-Specific Settings** - Fine-tune individual techniques
2. **Payload Customization** - Advanced payload options
3. **Detection Refinement** - Precision detection controls

## 🎯 Technique-Specific Settings

### Boolean-Based Blind Options

#### Comparison of True/False Responses
**Parameter:** `--string=STRING`
**Description:** String that appears only when query evaluates to True
**Examples:**
```
--string="Welcome back"
--string="<div class='admin'>"
--string="You have 5 messages"
```
**Use Cases:**
- Custom application responses
- Specific success indicators
- Unique content markers

#### Comparison of True/False Responses (Regex)
**Parameter:** `--regexp=REGEXP`
**Description:** Regular expression for True condition matching
**Examples:**
```
--regexp="Welcome.*admin"
--regexp="User.*logged.*in"
--regexp="Access.*granted"
```
**Use Cases:**
- Pattern-based detection
- Dynamic content matching
- Complex response patterns

#### Comparison of True/False Responses (Inverse)
**Parameter:** `--not-string=STRING`
**Description:** String that appears when query evaluates to False
**Examples:**
```
--not-string="Access denied"
--not-string="Invalid credentials"
--not-string="Error occurred"
```
**Use Cases:**
- Error message detection
- Negative condition indicators
- Failure state identification

#### Comparison of True/False Responses (Inverse Regex)
**Parameter:** `--not-regexp=REGEXP`
**Description:** Regex for False condition matching
**Examples:**
```
--not-regexp="Error.*denied"
--not-regexp="Access.*forbidden"
--not-regexp="Invalid.*request"
```
**Use Cases:**
- Error pattern matching
- Negative response detection
- Failure condition identification

### Error-Based Technique Options

#### DBMS Error Messages in Response
**Parameter:** `--dbms-errors`
**Description:** Force DBMS to throw error messages
**Behavior:** Injects payloads that cause database errors
**Examples:**
- Division by zero: `AND 1/0`
- Type conversion errors: `AND 'a'='b'`
- Invalid function calls: `AND SLEEP(-1)`

### Union Query-Based Options

#### Number of Columns to Test
**Parameter:** `--union-cols=COLS`
**Description:** Number of columns to test for UNION injection
**Default:** Automatic detection
**Examples:**
```
--union-cols=5
--union-cols=10-15
--union-cols=1,3,5
```
**Use Cases:**
- Known column count
- Range testing
- Specific column testing

#### Characters to Use for Brute-Forcing Number of Columns
**Parameter:** `--union-char=CHAR`
**Description:** Character to use in UNION column enumeration
**Default:** NULL
**Examples:**
```
--union-char=NULL
--union-char="test"
--union-char=123
```
**Use Cases:**
- Custom column fillers
- Specific data type requirements
- Application-specific values

#### Table to Use in UNION Injection
**Parameter:** `--union-from=TABLE`
**Description:** Table to use in FROM clause of UNION queries
**Examples:**
```
--union-from=users
--union-from=dual
--union-from=sysobjects
```
**Use Cases:**
- Known existing tables
- DBMS-specific system tables
- Custom table references

### Time-Based Blind Options

#### Seconds to Delay Query Execution
**Parameter:** `--time-sec=SECONDS`
**Description:** Time delay for time-based blind injection
**Default:** 5 seconds
**Examples:**
```
--time-sec=3
--time-sec=10
--time-sec=1
```
**Use Cases:**
- Fast networks: shorter delays
- Slow networks: longer delays
- High-latency targets: extended delays

#### Number of Retries for Time-Based Injection
**Parameter:** `--retries=NUM`
**Description:** Number of retries for failed time-based tests
**Default:** 3
**Examples:**
```
--retries=1
--retries=5
--retries=10
```
**Use Cases:**
- Unreliable connections
- High-latency networks
- Noisy environments

### Stacked Query Options

#### Disable Stacked Queries
**Parameter:** `--disable-stacked`
**Description:** Disable stacked query support
**Use Cases:**
- DBMS doesn't support stacked queries
- Application filters semicolons
- Security restrictions

#### Force Stacked Queries
**Parameter:** `--force-stacked`
**Description:** Force use of stacked queries
**Use Cases:**
- Known stacked query support
- Advanced exploitation scenarios
- Multi-statement injections

## 💉 Advanced Payload Options

### Payload Level
**Parameter:** `--level=LEVEL`
**Description:** Payload level for advanced injections
**Range:** 1-5 (higher = more complex payloads)
**Use Cases:**
- Bypassing basic filters
- Advanced WAF evasion
- Complex injection scenarios

### Payload Risk
**Parameter:** `--risk=RISK`
**Description:** Risk level for payload generation
**Range:** 1-3 (higher = more dangerous payloads)
**Use Cases:**
- Safe testing: Risk 1
- Thorough testing: Risk 2
- Aggressive testing: Risk 3

### Use Heuristic Detection for Union
**Parameter:** `--union-heuristic`
**Description:** Use heuristic detection for UNION injection
**Behavior:** Attempts to detect UNION injection without full column enumeration
**Use Cases:**
- Fast UNION detection
- Large column counts
- Unknown table structures

### Use All Available Union Techniques
**Parameter:** `--union-test-all`
**Description:** Test all possible UNION injection techniques
**Behavior:** Exhaustive UNION testing
**Use Cases:**
- Maximum detection coverage
- Complex applications
- Unknown injection points

## 🔧 Detection Refinement

### Optimize for Speed
**Parameter:** `--optimize`
**Description:** Optimize payloads for speed
**Behavior:** Uses faster but potentially less reliable payloads
**Use Cases:**
- Quick assessments
- Large-scale scanning
- Time-constrained testing

### Optimize for Reliability
**Parameter:** `--reliable`
**Description:** Optimize payloads for reliability
**Behavior:** Uses slower but more reliable payloads
**Use Cases:**
- Critical applications
- High-confidence results
- Production environments

### Use Binary Search Instead of Linear Search
**Parameter:** `--binary-search`
**Description:** Use binary search for data extraction
**Behavior:** Faster data retrieval using binary search algorithms
**Use Cases:**
- Large data sets
- Performance optimization
- Quick data extraction

### Use Adaptive Search
**Parameter:** `--adaptive`
**Description:** Use adaptive search techniques
**Behavior:** Dynamically adjusts search strategies
**Use Cases:**
- Unknown data characteristics
- Mixed content types
- Complex data structures

## 📝 Usage Examples

### Advanced Boolean Detection
```
String Match: "Welcome admin"
Not String Match: "Access denied"
Regexp Match: "User.*logged"
Not Regexp Match: "Error.*occurred"
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/admin.php?id=1" --string="Welcome admin" --not-string="Access denied" --regexp="User.*logged" --not-regexp="Error.*occurred"
```

### Time-Based Optimization
```
Time Delay: 3 seconds
Retries: 5
Binary Search: ✓ Enabled
Adaptive Search: ✓ Enabled
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/search.php?q=test" --time-sec=3 --retries=5 --binary-search --adaptive
```

### Union Query Customization
```
Union Columns: 5-10
Union Character: NULL
Union From Table: users
Union Heuristic: ✓ Enabled
Union Test All: ✓ Enabled
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/product.php?id=1" --union-cols=5-10 --union-char=NULL --union-from=users --union-heuristic --union-test-all
```

### Performance Optimization
```
Optimize: ✓ Enabled
Binary Search: ✓ Enabled
Adaptive: ✓ Enabled
Level: 3
Risk: 2
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/page.php?id=1" --optimize --binary-search --adaptive --level=3 --risk=2
```

### Stacked Query Control
```
Disable Stacked: ✗ Disabled
Force Stacked: ✓ Enabled
Level: 4
Risk: 3
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/admin.php?id=1" --force-stacked --level=4 --risk=3
```

## ⚠️ Important Considerations

### Technique Selection Strategy
- **Start simple**: Use basic Detection tab options first
- **Add specificity**: Use Techniques tab for fine-tuning
- **Test combinations**: Different techniques work better for different targets
- **Consider performance**: Advanced options can slow down scanning

### Custom String/Regex Matching
- **Unique identifiers**: Choose strings unique to the application
- **Test manually**: Verify strings appear/disappear as expected
- **Case sensitivity**: Consider case variations
- **Dynamic content**: Account for changing content (timestamps, counters)

### Time-Based Considerations
- **Network latency**: Adjust time delays based on connection speed
- **Server load**: Busy servers may have inconsistent response times
- **Proxy interference**: Proxies can add unpredictable delays
- **Accuracy vs speed**: Shorter delays are faster but less reliable

### Union Query Optimization
- **Column enumeration**: Let SQLmap auto-detect when possible
- **Known structures**: Specify columns/tables when known
- **Performance trade-offs**: Heuristic detection is faster but less thorough
- **Compatibility**: Some DBMS have different UNION syntax

## 🔧 Troubleshooting

### Boolean Detection Not Working
**Problem:** True/false conditions not detected properly
**Solutions:**
1. Verify string matches manually
2. Use regex instead of exact strings
3. Check for dynamic content interference
4. Try different string combinations

### Time-Based Detection Unreliable
**Problem:** Time delays inconsistent or not working
**Solutions:**
1. Increase time delay: `--time-sec=10`
2. Increase retries: `--retries=5`
3. Check network stability
4. Verify target supports SLEEP-like functions

### Union Injection Failing
**Problem:** UNION queries not working despite vulnerability
**Solutions:**
1. Specify column count: `--union-cols=5`
2. Use different union character: `--union-char="test"`
3. Try union heuristic: `--union-heuristic`
4. Check for ORDER/GROUP BY interference

### Slow Performance with Advanced Options
**Problem:** Advanced techniques causing slow scanning
**Solutions:**
1. Enable optimization: `--optimize`
2. Use binary search: `--binary-search`
3. Reduce level/risk temporarily
4. Focus on specific techniques

### Stacked Queries Not Working
**Problem:** Multiple statements not executing
**Solutions:**
1. Check DBMS support for stacked queries
2. Verify semicolon filtering
3. Try different statement separators
4. Use single statement techniques instead

## 📚 Related Tabs

- **[Detection Tab](detection_tab.md)**: Basic detection level and technique selection
- **[Injection Tab](injection_tab.md)**: Parameter selection and payload customization
- **[Enumeration Tab](enumeration_tab.md)**: Database structure discovery techniques
- **[Fingerprint Tab](fingerprint_tab.md)**: Database type identification</content>
<parameter name="filePath">/home/devil/Desktop/SQLmap-GUI-Advanced-SQL-Injection-Testing-Interface/docs/tabs/techniques.md
