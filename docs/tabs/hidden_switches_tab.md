# Hidden Switches Tab - Advanced and Specialized SQLmap Features

The Hidden Switches tab contains advanced, specialized, and less commonly used SQLmap options that provide fine-grained control over injection techniques, evasion methods, and experimental features.

## 📋 Overview

The Hidden Switches tab contains five main sections:
1. **Advanced Injection** - Sophisticated injection techniques
2. **Evasion Techniques** - Advanced WAF and IDS bypass
3. **Network Manipulation** - Low-level network control
4. **Debugging Tools** - Advanced debugging and analysis
5. **Experimental Options** - Cutting-edge and beta features

## 💉 Advanced Injection Options

### Skip Parameter Check
**Parameter:** `--skip-parameter-check`
**Description:** Skip parameter validity check
**Behavior:** Tests all parameters regardless of format
**Use Cases:**
- Unusual parameter formats
- Custom encoding schemes
- Non-standard input validation

### Skip DBMS Banner Check
**Parameter:** `--skip-dbms-banner`
**Description:** Skip DBMS banner retrieval
**Behavior:** Assumes DBMS type without verification
**Use Cases:**
- Known environments
- Performance optimization
- Custom DBMS identification

### Skip Dynamic Parameters
**Parameter:** `--skip-dynamic`
**Description:** Skip dynamic parameters
**Behavior:** Ignores parameters that change between requests
**Use Cases:**
- CSRF tokens
- Timestamp parameters
- Non-static content

### Force Parameter Check
**Parameter:** `--force-parameter=PARAM`
**Description:** Force test of specific parameter
**Examples:**
```
--force-parameter=id
--force-parameter=username,password
--force-parameter=custom_param
```
**Use Cases:**
- Specific parameter targeting
- Known vulnerable parameters
- Focused testing

### Ignore 401 Unauthorized
**Parameter:** `--ignore-401`
**Description:** Ignore HTTP 401 Unauthorized responses
**Behavior:** Continues testing despite authentication errors
**Use Cases:**
- Authentication bypass testing
- Multi-stage authentication
- Error page analysis

### Ignore Redirects
**Parameter:** `--ignore-redirects`
**Description:** Ignore HTTP redirects
**Behavior:** Doesn't follow 3xx responses
**Use Cases:**
- Redirect-based WAF
- Authentication flows
- Custom redirect handling

### Ignore Timeout
**Parameter:** `--ignore-timeouts`
**Description:** Ignore connection timeouts
**Behavior:** Continues despite timeout errors
**Use Cases:**
- Unreliable connections
- Slow responses
- Network issues

## 🛡️ Advanced Evasion Techniques

### Skip WAF Detection
**Parameter:** `--skip-waf`
**Description:** Skip WAF detection
**Behavior:** Assumes no WAF present
**Use Cases:**
- Known clean environments
- Performance optimization
- Custom WAF handling

### Disable Payload Encoding
**Parameter:** `--disable-precon`
**Description:** Disable payload pre-connect test
**Behavior:** Skips payload validation
**Use Cases:**
- Custom payload testing
- Performance optimization
- Known working payloads

### Skip All Checks
**Parameter:** `--skip-all`
**Description:** Skip all optimization checks
**Behavior:** Maximum performance, minimum safety
**Use Cases:**
- Known vulnerable targets
- Performance-critical scanning
- Automated environments

### Flush HTTP Cache
**Parameter:** `--flush-cache`
**Description:** Flush HTTP cache
**Behavior:** Clears cached responses
**Use Cases:**
- Dynamic content testing
- Cache poisoning
- Fresh response analysis

### Fresh HTTP Cache
**Parameter:** `--fresh-cache`
**Description:** Generate fresh HTTP cache
**Behavior:** Ignores existing cache
**Use Cases:**
- Cache bypass
- Fresh content testing
- State-dependent testing

### HTTP Cache Directory
**Parameter:** `--cache-dir=DIR`
**Description:** HTTP cache directory
**Examples:**
```
--cache-dir=/tmp/sqlmap_cache/
--cache-dir=C:\sqlmap\cache\
--cache-dir=./.cache/
```
**Use Cases:**
- Cache management
- Multi-session persistence
- Performance optimization

## 🌐 Network Manipulation Options

### Force HTTP Method
**Parameter:** `--force-method=METHOD`
**Description:** Force HTTP method
**Supported Methods:** GET, POST, PUT, DELETE, HEAD, OPTIONS, TRACE, PATCH
**Examples:**
```
--force-method=POST
--force-method=PUT
--force-method=DELETE
```
**Use Cases:**
- REST API testing
- Method-specific vulnerabilities
- HTTP method bypass

### HTTP Method Tampering
**Parameter:** `--method-tamper=METHOD`
**Description:** Tamper HTTP method
**Behavior:** Modifies HTTP method in request
**Use Cases:**
- Method restriction bypass
- WAF evasion
- Protocol testing

### Custom User-Agent
**Parameter:** `--user-agent=AGENT`
**Description:** Custom User-Agent header
**Examples:**
```
--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
--user-agent="sqlmap/1.6.5#stable (https://sqlmap.org)"
--user-agent="Googlebot/2.1 (+http://www.google.com/bot.html)"
```
**Use Cases:**
- User-Agent filtering bypass
- Bot detection evasion
- Custom identification

### Random User-Agent
**Parameter:** `--random-agent`
**Description:** Use random User-Agent
**Behavior:** Rotates User-Agent headers
**Use Cases:**
- Anti-bot measures
- Request fingerprinting evasion
- Anonymity

### Host Header
**Parameter:** `--host=HOST`
**Description:** Custom Host header
**Examples:**
```
--host=example.com
--host=internal.example.com
--host=127.0.0.1
```
**Use Cases:**
- Virtual host testing
- Host header injection
- Internal network access

### Referer Header
**Parameter:** `--referer=REFERER`
**Description:** Custom Referer header
**Examples:**
```
--referer="http://google.com"
--referer="http://example.com/login.php"
--referer="http://malicious.com"
```
**Use Cases:**
- Referer validation bypass
- CSRF protection testing
- Origin spoofing

## 🔍 Debugging and Analysis Tools

### Debug HTTP Traffic
**Parameter:** `--debug`
**Description:** Debug HTTP traffic
**Behavior:** Shows detailed HTTP request/response information
**Use Cases:**
- Protocol analysis
- WAF rule understanding
- Network troubleshooting

### Traffic File
**Parameter:** `--traffic-file=FILE`
**Description:** Log all HTTP traffic to file
**Examples:**
```
--traffic-file=./traffic.log
--traffic-file=/var/log/sqlmap_traffic.txt
--traffic-file=C:\logs\http_traffic.log
```
**Use Cases:**
- Traffic analysis
- Debugging sessions
- Compliance logging

### Save HTTP Traffic
**Parameter:** `--save-traffic=FILE`
**Description:** Save HTTP traffic to file
**Behavior:** Records all HTTP communications
**Use Cases:**
- Forensic analysis
- Replay attacks
- Request analysis

### Hex Dump
**Parameter:** `--hex`
**Description:** Use hex representation for data
**Behavior:** Shows data in hexadecimal format
**Use Cases:**
- Binary data analysis
- Encoding issues
- Payload debugging

### Smart Mode
**Parameter:** `--smart`
**Description:** Conduct thorough tests only if positive heuristic
**Behavior:** Conservative scanning approach
**Use Cases:**
- Production environments
- Risk-averse testing
- Resource conservation

### Dry Run
**Parameter:** `--dry-run`
**Description:** Dry run, only show what would be done
**Behavior:** Shows planned actions without executing
**Use Cases:**
- Planning and verification
- Risk assessment
- Command validation

## 🧪 Experimental and Advanced Options

### Tor Proxy
**Parameter:** `--tor`
**Description:** Use Tor anonymity network
**Behavior:** Routes traffic through Tor
**Use Cases:**
- Anonymity
- IP rotation
- Geo-blocking bypass

### Tor Type
**Parameter:** `--tor-type=TYPE`
**Description:** Tor proxy type
**Options:** HTTP, SOCKS4, SOCKS5
**Examples:**
```
--tor-type=SOCKS5
--tor-type=HTTP
```
**Use Cases:**
- Tor compatibility
- Proxy configuration
- Network requirements

### Tor Port
**Parameter:** `--tor-port=PORT`
**Description:** Tor proxy port
**Default:** 9050
**Examples:**
```
--tor-port=9050
--tor-port=9150
```
**Use Cases:**
- Custom Tor setup
- Port configuration
- Network setup

### Check Tor
**Parameter:** `--check-tor`
**Description:** Check Tor connection
**Behavior:** Verifies Tor connectivity
**Use Cases:**
- Tor troubleshooting
- Connection validation
- Setup verification

### Delay Between Requests
**Parameter:** `--delay=SECONDS`
**Description:** Delay between each HTTP request
**Examples:**
```
--delay=1
--delay=0.5
--delay=2.5
```
**Use Cases:**
- Rate limiting bypass
- Anti-DoS protection
- Resource management

### Timeout
**Parameter:** `--timeout=SECONDS`
**Description:** Seconds to wait for each response
**Default:** 30
**Examples:**
```
--timeout=10
--timeout=60
--timeout=120
```
**Use Cases:**
- Slow connections
- Large responses
- Network latency

### Retries
**Parameter:** `--retries=NUM`
**Description:** Retries when connection timeout occurs
**Default:** 3
**Examples:**
```
--retries=1
--retries=5
--retries=10
```
**Use Cases:**
- Unreliable connections
- Network issues
- Error recovery

### Randomize Parameters
**Parameter:** `--randomize=PARAM`
**Description:** Randomize value for given parameter
**Examples:**
```
--randomize=id
--randomize=session
--randomize=token
```
**Use Cases:**
- Cache busting
- Dynamic content
- Anti-caching measures

### Skip Character Set
**Parameter:** `--skip-charsets`
**Description:** Skip payload character set checks
**Behavior:** Uses all character sets
**Use Cases:**
- International applications
- Unicode testing
- Character encoding bypass

## 📝 Usage Examples

### Advanced Evasion Configuration
```
Skip WAF Detection: ✓ Enabled
Skip All Checks: ✓ Enabled
Flush HTTP Cache: ✓ Enabled
Random User-Agent: ✓ Enabled
Delay: 2 seconds
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/page.php?id=1" --skip-waf --skip-all --flush-cache --random-agent --delay=2
```

### Network Manipulation
```
Force HTTP Method: POST
Custom User-Agent: sqlmap/1.6.5
Host Header: internal.example.com
Referer: http://google.com
Tor: ✓ Enabled
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/api.php" --force-method=POST --user-agent="sqlmap/1.6.5" --host=internal.example.com --referer="http://google.com" --tor
```

### Debugging and Analysis
```
Debug: ✓ Enabled
Traffic File: ./debug_traffic.log
Hex Dump: ✓ Enabled
Dry Run: ✓ Enabled
Smart Mode: ✓ Enabled
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/debug.php?id=1" --debug --traffic-file=./debug_traffic.log --hex --dry-run --smart
```

### Performance and Reliability
```
Timeout: 60 seconds
Retries: 5
Randomize: session
Skip Character Set: ✓ Enabled
Fresh Cache: ✓ Enabled
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/unstable.php?id=1" --timeout=60 --retries=5 --randomize=session --skip-charsets --fresh-cache
```

### Comprehensive Hidden Switches
```
Skip Parameter Check: ✓ Enabled
Ignore Redirects: ✓ Enabled
Force Method: PUT
Random Agent: ✓ Enabled
Tor: ✓ Enabled
Debug: ✓ Enabled
Smart: ✓ Enabled
Delay: 1.5 seconds
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/advanced.php?id=1" --skip-parameter-check --ignore-redirects --force-method=PUT --random-agent --tor --debug --smart --delay=1.5
```

## ⚠️ Important Considerations

### Performance Impact
- **Debugging overhead**: Debug options significantly slow scanning
- **Traffic logging**: Large log files can consume disk space
- **Network latency**: Tor and delays increase response times
- **Resource usage**: Advanced options require more system resources

### Detection and Evasion
- **WAF interaction**: Some options may trigger advanced WAF rules
- **IDS alerts**: Unusual traffic patterns may trigger intrusion detection
- **Legal implications**: Tor usage may have legal considerations
- **Anonymity**: Tor doesn't guarantee complete anonymity

### Stability and Compatibility
- **Experimental features**: May not work in all environments
- **Version dependencies**: Some options require specific SQLmap versions
- **Platform limitations**: Certain features may not work on all platforms
- **Network requirements**: Some options require specific network configurations

### Security and Ethics
- **System impact**: Some options can affect target system stability
- **Data exposure**: Debug and traffic logging may expose sensitive data
- **Legal compliance**: Ensure all usage complies with applicable laws
- **Authorization**: Only use on systems you have permission to test

## 🔧 Troubleshooting

### Tor Connection Issues
**Problem:** Tor connection failing
**Solutions:**
1. Verify Tor installation and configuration
2. Check Tor port and type settings
3. Test Tor connectivity independently
4. Use --check-tor to diagnose

### Performance Degradation
**Problem:** Scanning significantly slower
**Solutions:**
1. Disable debug and traffic logging
2. Reduce delay settings
3. Disable Tor if not required
4. Use --smart mode for optimization

### Network Timeouts
**Problem:** Frequent connection timeouts
**Solutions:**
1. Increase --timeout value
2. Increase --retries count
3. Check network connectivity
4. Reduce concurrent threads

### WAF False Positives
**Problem:** Legitimate requests blocked by WAF
**Solutions:**
1. Adjust tamper script combinations
2. Modify delay and timing
3. Use different User-Agent
4. Try different HTTP methods

### Debug Output Too Verbose
**Problem:** Debug output overwhelming
**Solutions:**
1. Use --traffic-file for logging
2. Reduce verbosity level
3. Use --dry-run for planning
4. Filter output with grep

## 📚 Related Tabs

- **[Miscellaneous Tab](miscellaneous_tab.md)**: Additional advanced options
- **[Request Tab](request_tab.md)**: HTTP request customization
- **[Injection Tab](injection_tab.md)**: Parameter selection and payload customization
- **[General Tab](general_tab.md)**: Output and logging options</content>
<parameter name="filePath">/home/devil/Desktop/SQLmap-GUI-Advanced-SQL-Injection-Testing-Interface/docs/tabs/hidden_switches.md
