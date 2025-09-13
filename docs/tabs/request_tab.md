# Request Tab - HTTP Request Customization and Optimization

The Request tab provides advanced HTTP configuration options, including optimization settings, timing controls, authentication, SSL/TLS configuration, and Tor integration for anonymous scanning.

## 📋 Overview

The Request tab contains four main sections:
1. **Optimization** - HTTP connection and performance settings
2. **Request Timing** - Delay, timeout, and retry configuration
3. **HTTP Options** - Character encoding and data handling
4. **Tor Options** - Anonymous scanning configuration

## ⚡ Optimization Options

### Turn on All Optimization Switches
**Parameter:** `--optimize`
**Description:** Enable all HTTP optimization features
**Includes:**
- Persistent HTTP connections
- Connection pooling
- Request batching
- Response caching
- Parallel processing

### Use Persistent HTTP(s) Connections
**Parameter:** `--keep-alive`
**Description:** Reuse HTTP connections for multiple requests
**Benefits:**
- Faster scanning (reduced connection overhead)
- Lower resource usage
- More realistic traffic patterns
**Default:** Enabled when `--optimize` is used

### Retrieve Page Length Without HTTP Response Body
**Parameter:** `--null-connection`
**Description:** Use HEAD requests or Range headers to get content length
**Use Cases:**
- Bandwidth conservation
- Faster initial detection
- Reduced network traffic
**Limitations:** May not work with all servers

### Max Number of Concurrent HTTP Requests
**Parameter:** `--threads=THREADS`
**Description:** Number of parallel HTTP connections
**Range:** 1-10
**Default:** 1
**Notes:**
- Higher values increase speed but may trigger rate limiting
- Some servers block concurrent connections
- Balance speed vs. detection avoidance

### Never Ask for User Input
**Parameter:** `--batch`
**Description:** Use default answers for all prompts
**Behavior:**
- Automatically selects default options
- No interactive prompts during scanning
- Ideal for automated/scripted usage
**Default:** Disabled (interactive mode)

### Use Tor Anonymizer
**Parameter:** `--tor`
**Description:** Route all traffic through Tor network
**Requirements:**
- Tor must be installed and running
- Tor control port accessible (default: 9050)
- Tor configuration must allow SQLmap traffic
**Notes:**
- Significantly slower due to Tor latency
- May be blocked by target websites
- Provides anonymity but not guaranteed security

## ⏱️ Request Timing Options

### Delay Between HTTP Requests
**Parameter:** `--delay=DELAY`
**Description:** Seconds to wait between requests
**Range:** 0-3600 seconds
**Default:** 0 (no delay)
**Use Cases:**
- Avoid rate limiting detection
- Reduce server load
- Simulate human browsing patterns
**Example:** `--delay=1.5` (1.5 second delay)

### Seconds to Wait Before Timeout
**Parameter:** `--timeout=TIMEOUT`
**Description:** HTTP request timeout in seconds
**Range:** 1-3600 seconds
**Default:** 30 seconds
**Notes:**
- Longer timeouts for slow networks
- Shorter timeouts for faster scanning
- Balance reliability vs. speed

### Retries When Connection Timeouts
**Parameter:** `--retries=RETRIES`
**Description:** Number of retry attempts for failed requests
**Range:** 0-10
**Default:** 3
**Behavior:**
- Retries only on connection timeouts
- Does not retry on HTTP errors (4xx, 5xx)
- Exponential backoff may be applied

## 🔤 HTTP Options

### Blind SQL Injection Charset
**Parameter:** `--charset=CHARSET`
**Description:** Character set for blind SQL injection
**Options:**
- **Default**: Automatic detection
- **Numeric**: `0123456789` (fastest)
- **Alphanumeric**: `abcdefghijklmnopqrstuvwxyz0123456789`
- **Alphabetic**: `abcdefghijklmnopqrstuvwxyz`
- **Uppercase**: `ABCDEFGHIJKLMNOPQRSTUVWXYZ`
- **Hexadecimal**: `0123456789abcdef`
- **Binary**: `01`

### Character Encoding
**Parameter:** `--encoding=ENCODING`
**Description:** Character encoding for payloads and responses
**Options:**
- **UTF-8**: Universal character encoding
- **ISO-8859-1**: Western European encoding
- **Windows-1252**: Windows Western encoding
- **ASCII**: 7-bit character encoding

### Base64 Encoded Parameters
**Parameter:** `--base64=PARAMS`
**Description:** Parameters containing Base64 encoded data
**Format:** Comma-separated parameter names
**Example:** `--base64=image,token,data`
**Purpose:** Proper handling of Base64 encoded values

### URL-safe Base64 Alphabet
**Parameter:** `--base64-safe`
**Description:** Use RFC 4648 URL-safe Base64 alphabet
**Characters:** Uses `-` and `_` instead of `+` and `/`
**Use Case:** Web applications using URL-safe Base64

## 🧅 Tor Options

### Tor Proxy Port
**Parameter:** `--tor-port=PORT`
**Description:** Tor SOCKS proxy port
**Default:** 9050
**Requirements:**
- Tor must be running on specified port
- Port must be accessible to SQLmap
- SOCKS5 proxy support required

### Tor Proxy Type
**Parameter:** `--tor-type=TYPE`
**Description:** Tor proxy protocol type
**Options:**
- **SOCKS4**: Legacy SOCKS protocol
- **SOCKS5**: Modern SOCKS protocol (recommended)
- **HTTP**: HTTP proxy protocol
**Default:** SOCKS5

## 🔍 Usage Examples

### Basic Optimization
```
Optimization: ✓ Turn on All Optimization Switches
Threads: 3
Batch: ✓ Never Ask for User Input
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/vuln.php?id=1" --optimize --threads=3 --batch
```

### Anonymous Scanning with Tor
```
Tor: ✓ Use Tor Anonymizer
Tor Port: 9050
Tor Type: SOCKS5
Delay: 2.0
Timeout: 60
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/vuln.php?id=1" --tor --tor-port=9050 --tor-type=SOCKS5 --delay=2 --timeout=60
```

### Bandwidth Optimization
```
Keep Alive: ✓ Use Persistent Connections
Null Connection: ✓ Retrieve Page Length Without Body
Threads: 1
Delay: 1.0
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/vuln.php?id=1" --keep-alive --null-connection --threads=1 --delay=1
```

### Custom Character Encoding
```
Encoding: UTF-8
Charset: Alphanumeric
Base64 Parameters: token,data
Base64 Safe: ✓ Use URL-safe Base64
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/vuln.php?id=1" --encoding=utf-8 --charset=abcdefghijklmnopqrstuvwxyz0123456789 --base64=token,data --base64-safe
```

## ⚠️ Important Considerations

### Performance vs. Detection
- **High threads + No delay**: Fast but easily detected
- **Low threads + High delay**: Slow but stealthy
- **Balance based on target sensitivity**

### Tor Usage
- **Pros:** Anonymity, bypass IP blocks
- **Cons:** Very slow, may be blocked, unreliable
- **Best for:** Research, testing, non-time-critical scans

### Timeout Settings
- **Fast networks:** 10-30 seconds
- **Slow networks:** 60-120 seconds
- **Very slow targets:** 300+ seconds

### Character Encoding
- **Always test target encoding first**
- **Mismatch can cause false negatives**
- **Use browser dev tools to check encoding**

## 🔧 Troubleshooting

### Tor Connection Issues
**Problem:** Cannot connect through Tor
**Solutions:**
1. Verify Tor is running: `systemctl status tor`
2. Check Tor port: `netstat -tlnp | grep 9050`
3. Test Tor connectivity: `curl --socks5 127.0.0.1:9050 https://check.torproject.org`
4. Configure Tor control port if needed

### Rate Limiting Problems
**Problem:** Getting blocked by rate limiting
**Solutions:**
1. Increase delay between requests
2. Reduce number of threads
3. Use random delays: `--delay=1-3`
4. Rotate User-Agent headers

### Encoding Issues
**Problem:** Incorrect character handling
**Solutions:**
1. Check target website encoding (browser dev tools)
2. Test with different encoding options
3. Use `--encoding=utf-8` for modern applications
4. Verify charset matches expected data types

### Connection Timeouts
**Problem:** Requests timing out frequently
**Solutions:**
1. Increase timeout value
2. Check network connectivity
3. Reduce concurrent threads
4. Use `--keep-alive` for connection reuse

## 📚 Related Tabs

- **[Target Tab](target_tab.md)**: Basic target and connection setup
- **[Detection Tab](detection_tab.md)**: SQL injection detection configuration
- **[Techniques Tab](techniques_tab.md)**: Injection technique selection
- **[General Tab](general_tab.md)**: Additional timing and behavior options</content>
<parameter name="filePath">/home/devil/Desktop/SQLmap-GUI-Advanced-SQL-Injection-Testing-Interface/docs/tabs/request.md
