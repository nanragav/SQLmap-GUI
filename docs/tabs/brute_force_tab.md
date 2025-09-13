# Brute Force Tab - Credential Brute Force and Security Testing

The Brute Force tab provides options for brute force attacks on database credentials, hash cracking, and other security mechanisms that require systematic testing of multiple values.

## 📋 Overview

The Brute Force tab contains four main sections:
1. **Credential Brute Force** - Username/password attacks
2. **Hash Cracking** - Password hash attacks
3. **Dictionary Attacks** - Wordlist-based attacks
4. **Advanced Options** - Attack customization

## 🔐 Credential Brute Force Options

### Brute-Force DBMS Login
**Parameter:** `--brute-force`
**Description:** Brute-force database login credentials
**Behavior:** Attempts multiple username/password combinations
**Requirements:** Valid database connection details
**Use Cases:**
- Default credential testing
- Weak password discovery
- Access credential recovery

### User to Brute-Force
**Parameter:** `-U USERNAME`
**Description:** Specific username to brute-force
**Examples:**
```
-U admin
-U root
-U sa
-U system
```
**Use Cases:**
- Known username, unknown password
- Specific user account testing
- Targeted credential attacks

### Password to Use
**Parameter:** `-P PASSWORD`
**Description:** Specific password to test
**Examples:**
```
-P password123
-P admin123
-P letmein
-P qwerty
```
**Use Cases:**
- Known password, unknown username
- Password policy testing
- Credential verification

### Load Users from File
**Parameter:** `-U /path/to/users.txt`
**Description:** Load usernames from file
**Format:** One username per line
**Examples:**
```
admin
root
user
test
guest
```
**Use Cases:**
- Large username lists
- Common username testing
- Dictionary-based attacks

### Load Passwords from File
**Parameter:** `-P /path/to/passwords.txt`
**Description:** Load passwords from file
**Format:** One password per line
**Examples:**
```
password
123456
admin
letmein
qwerty
welcome
```
**Use Cases:**
- Large password lists
- Dictionary attacks
- Comprehensive testing

## 🔑 Hash Cracking Options

### Crack DBMS User Password Hashes
**Parameter:** `--crack`
**Description:** Crack password hashes using built-in algorithms
**Behavior:** Attempts to crack hashes using common algorithms
**Supported Algorithms:**
- MD5
- SHA1
- SHA256
- SHA512
- MySQL-specific hashes
- MSSQL password hashes

**Use Cases:**
- Password recovery
- Security assessment
- Hash analysis

### Dictionary File for Cracking
**Parameter:** `--dict=FILE`
**Description:** Use custom dictionary for hash cracking
**Format:** One word per line
**Examples:**
```
/path/to/rockyou.txt
/path/to/custom_dict.txt
/path/to/company_words.txt
```
**Use Cases:**
- Custom wordlists
- Company-specific passwords
- Targeted cracking

### Hash File to Crack
**Parameter:** `--hash-file=FILE`
**Description:** File containing hashes to crack
**Format:** One hash per line, optionally with username:salt
**Examples:**
```
5f4dcc3b5aa765d61d8327deb882cf99
admin:5f4dcc3b5aa765d61d8327deb882cf99
user:abc123:5f4dcc3b5aa765d61d8327deb882cf99
```
**Use Cases:**
- Batch hash cracking
- Multiple user hashes
- Salted hash support

## 📚 Dictionary and Wordlist Options

### Common Usernames Dictionary
**Parameter:** `--common-user`
**Description:** Use built-in common usernames
**Behavior:** Tests common usernames like admin, root, user
**Use Cases:**
- Default account discovery
- Common username testing
- Quick reconnaissance

### Common Passwords Dictionary
**Parameter:** `--common-pass`
**Description:** Use built-in common passwords
**Behavior:** Tests common passwords like password, 123456, admin
**Use Cases:**
- Weak password detection
- Default credential testing
- Basic security assessment

### Custom Usernames File
**Parameter:** `--user-file=FILE`
**Description:** Custom usernames wordlist
**Format:** One username per line
**Use Cases:**
- Organization-specific usernames
- Custom username patterns
- Targeted testing

### Custom Passwords File
**Parameter:** `--pass-file=FILE`
**Description:** Custom passwords wordlist
**Format:** One password per line
**Use Cases:**
- Company password policies
- Custom password patterns
- Industry-specific passwords

## ⚙️ Advanced Brute Force Options

### Threads for Brute-Force
**Parameter:** `--threads=NUM`
**Description:** Number of threads for brute force attacks
**Default:** 1
**Range:** 1-10 (depending on system)
**Examples:**
```
--threads=4
--threads=8
--threads=16
```
**Use Cases:**
- Performance optimization
- Resource management
- Speed vs stability balance

### Delay Between Requests
**Parameter:** `--delay=SECONDS`
**Description:** Delay between brute force attempts
**Default:** 0
**Examples:**
```
--delay=1
--delay=0.5
--delay=2
```
**Use Cases:**
- Anti-brute-force bypass
- Rate limiting evasion
- Resource management

### Maximum Retries
**Parameter:** `--retries=NUM`
**Description:** Maximum retries for failed attempts
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
- Error handling

### Timeout for Requests
**Parameter:** `--timeout=SECONDS`
**Description:** Timeout for each brute force attempt
**Default:** 30
**Examples:**
```
--timeout=10
--timeout=60
--timeout=120
```
**Use Cases:**
- Slow networks
- High-latency targets
- Connection issues

## 📝 Usage Examples

### Basic Credential Brute Force
```
Brute Force Login: ✓ Enabled
User File: /path/to/users.txt
Password File: /path/to/passwords.txt
Threads: 4
Delay: 1 second
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/login.php" --brute-force -U /path/to/users.txt -P /path/to/passwords.txt --threads=4 --delay=1
```

### Hash Cracking
```
Crack Password Hashes: ✓ Enabled
Dictionary File: /path/to/rockyou.txt
Hash File: /path/to/hashes.txt
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/admin.php?id=1" --crack --dict=/path/to/rockyou.txt --hash-file=/path/to/hashes.txt
```

### Common Credentials Testing
```
Common Usernames: ✓ Enabled
Common Passwords: ✓ Enabled
Threads: 2
Delay: 0.5 seconds
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/auth.php" --common-user --common-pass --threads=2 --delay=0.5
```

### Advanced Brute Force Configuration
```
User: admin
Password File: /path/to/passwords.txt
Threads: 8
Delay: 2 seconds
Retries: 5
Timeout: 60 seconds
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/login.php" -U admin -P /path/to/passwords.txt --threads=8 --delay=2 --retries=5 --timeout=60
```

### Dictionary-Based Hash Cracking
```
Crack Password Hashes: ✓ Enabled
Dictionary File: /path/to/custom_dict.txt
Threads: 4
```
**Generated Command:**
```bash
sqlmap -u "http://example.com/user.php?id=1" --crack --dict=/path/to/custom_dict.txt --threads=4
```

## ⚠️ Important Considerations

### Legal and Ethical Issues
- **Authorization required**: Only test systems you own or have permission to test
- **Service disruption**: Brute force can cause account lockouts or service denial
- **Legal compliance**: Ensure compliance with local laws and regulations
- **Responsible disclosure**: Report findings through proper channels

### Performance and Resource Management
- **Thread limits**: Don't use too many threads to avoid overwhelming the target
- **Delay settings**: Use appropriate delays to avoid detection and blocking
- **Resource usage**: Brute force can consume significant CPU and memory
- **Network impact**: Consider bandwidth and network capacity

### Dictionary Quality
- **Comprehensive wordlists**: Use large, comprehensive dictionaries
- **Custom dictionaries**: Include organization-specific words and patterns
- **Regular updates**: Keep dictionaries current with new password trends
- **Quality over quantity**: Better quality dictionaries yield better results

### Detection Evasion
- **Rate limiting**: Many systems have brute force protection
- **IP rotation**: Consider using proxies for large-scale testing
- **Timing patterns**: Vary delays to avoid detection algorithms
- **Account lockout**: Be aware of account lockout policies

## 🔧 Troubleshooting

### Brute Force Not Working
**Problem:** Brute force attempts failing or not connecting
**Solutions:**
1. Verify target URL and parameters
2. Check for CAPTCHA or other protections
3. Reduce thread count and increase delays
4. Test with known credentials first

### Slow Brute Force Performance
**Problem:** Brute force taking too long or hanging
**Solutions:**
1. Increase thread count (if system allows)
2. Reduce delay between attempts
3. Use smaller, more targeted wordlists
4. Check network connectivity and latency

### Account Lockouts
**Problem:** Brute force causing account lockouts
**Solutions:**
1. Increase delays between attempts
2. Use different IP addresses/proxies
3. Test lockout policies first
4. Use smaller batches of attempts

### Hash Cracking Issues
**Problem:** Hash cracking not working or producing no results
**Solutions:**
1. Verify hash format and algorithm
2. Check if hashes are salted
3. Use appropriate dictionary/wordlist
4. Try different cracking tools if needed

### Memory/Resource Issues
**Problem:** Brute force consuming too many resources
**Solutions:**
1. Reduce thread count
2. Use smaller wordlists
3. Increase delays between attempts
4. Monitor system resources during operation

### False Positives/Negatives
**Problem:** Incorrect results from brute force attempts
**Solutions:**
1. Test with known valid credentials
2. Verify authentication mechanism
3. Check for multi-factor authentication
4. Review application logs for clues

## 📚 Related Tabs

- **[Enumeration Tab](enumeration_tab.md)**: User and password hash discovery
- **[Fingerprint Tab](fingerprint_tab.md)**: Database type identification for hash format
- **[General Tab](general_tab.md)**: Output and logging options
- **[Request Tab](request_tab.md)**: HTTP request customization for authentication</content>
<parameter name="filePath">/home/devil/Desktop/SQLmap-GUI-Advanced-SQL-Injection-Testing-Interface/docs/tabs/brute_force.md
