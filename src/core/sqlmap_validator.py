#!/usr/bin/env python3
"""
SQLmap Command Validator - Comprehensive validation system for SQLmap commands
"""

import shlex
import re
import os
import json
from typing import Dict, List, Tuple, Optional, Any, Set
from dataclasses import dataclass
from enum import Enum


class ValidationLevel(Enum):
    """Validation severity levels"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    SUCCESS = "success"


@dataclass
class ValidationResult:
    """Individual validation result"""
    level: ValidationLevel
    message: str
    flag: Optional[str] = None
    suggestion: Optional[str] = None


@dataclass
class CommandValidation:
    """Complete command validation results"""
    is_valid: bool
    results: List[ValidationResult]
    errors: List[ValidationResult]
    warnings: List[ValidationResult]
    infos: List[ValidationResult]
    suggested_command: Optional[str] = None


class SqlmapValidator:
    """Comprehensive SQLmap command validator"""
    
    def __init__(self):
        self.initialize_validation_data()
    
    def initialize_validation_data(self):
        """Initialize validation rules and data"""
        
        # Target specification flags (at least one required)
        self.target_flags = {
            '-u', '--url',           # Target URL
            '-d', '--direct',        # Direct database connection
            '-l', '--logfile',       # Burp/WebScarab log file
            '-m', '--bulkfile',      # Multiple targets file
            '-r', '--requestfile',   # HTTP request file
            '-g', '--googledork',    # Google dork
            '-c', '--configfile'     # Configuration file
        }
        
        # Boolean flags (no values expected)
        self.boolean_flags = {
            '--batch', '--mobile', '--random-agent', '--force-ssl', '--chunked',
            '--hpp', '--forms', '--fresh-queries', '--hex', '--parse-errors',
            '--repair', '--skip-urlencode', '--skip-static', '--skip-heuristics',
            '--skip-waf', '--smart', '--text-only', '--titles', '--no-cast',
            '--no-escape', '--invalid-bignum', '--invalid-logical', '--invalid-string',
            '--optimize', '--predict-output', '--keep-alive', '--null-connection',
            '--all', '--banner', '--current-user', '--current-db', '--hostname',
            '--is-dba', '--users', '--passwords', '--privileges', '--roles',
            '--dbs', '--tables', '--columns', '--schema', '--count', '--dump',
            '--dump-all', '--search', '--comments', '--statements', '--common-tables',
            '--common-columns', '--common-files', '--udf-inject', '--os-shell',
            '--os-pwn', '--os-smbrelay', '--os-bof', '--priv-esc', '--sql-shell',
            '--reg-read', '--reg-add', '--reg-del', '--flush-session', '--cleanup',
            '--crawl-exclude', '--base64-safe', '--check-internet', '--eta',
            '--offline', '--purge', '--shell', '--unstable', '--update', '--wizard',
            '--beep', '--dependencies', '--disable-coloring', '--disable-hashing',
            '--list-tampers', '--no-logging', '--no-truncate', '--fingerprint',
            '--exclude-sysdbs', '--check-tor', '--ignore-proxy', '--ignore-redirects',
            '--ignore-timeouts', '--drop-set-cookie', '--tor'
        }
        
        # Flags that require values
        self.value_flags = {
            # Target and request
            '-u', '--url', '-d', '--direct', '-l', '--logfile', '-m', '--bulkfile',
            '-r', '--requestfile', '-g', '--googledork', '-c', '--configfile',
            '--method', '--data', '--param-del', '--cookie', '--cookie-del',
            '--live-cookies', '--load-cookies', '--host', '--referer', '--headers',
            '--auth-type', '--auth-cred', '--auth-file', '--abort-code', '--ignore-code',
            '--proxy', '--proxy-cred', '--proxy-file', '--proxy-freq', '--tor-port',
            '--tor-type', '--delay', '--timeout', '--retries', '--retry-on',
            '--randomize', '--safe-url', '--safe-post', '--safe-req', '--safe-freq',
            '--csrf-token', '--csrf-url', '--csrf-method', '--csrf-data', '--csrf-retries',
            '--eval', '--user-agent', '--encoding',
            
            # Injection
            '-p', '--skip', '--param-exclude', '--param-filter', '--dbms', '--dbms-cred',
            '--os', '--prefix', '--suffix', '--tamper',
            
            # Detection and techniques
            '--level', '--risk', '--string', '--not-string', '--regexp', '--code',
            '--technique', '--time-sec', '--union-cols', '--union-char', '--union-from',
            '--union-values', '--dns-domain', '--second-url', '--second-req',
            
            # Enumeration
            '-D', '--db', '-T', '--tbl', '-C', '--col', '-X', '--exclude',
            '-U', '--user', '--pivot-column', '--where', '--start', '--stop',
            '--first', '--last', '--sql-query', '--sql-file',
            
            # File system and OS
            '--file-read', '--file-write', '--file-dest', '--os-cmd', '--msf-path',
            '--tmp-path', '--shared-lib',
            
            # Registry
            '--reg-key', '--reg-value', '--reg-data', '--reg-type',
            
            # General
            '-s', '--sessionfile', '-t', '--trafficfile', '--answers', '--base64',
            '--binary-fields', '--charset', '--csv-del', '--dump-file', '--dump-format',
            '--output-dir', '--preprocess', '--postprocess', '--save', '--scope',
            '--test-filter', '--test-skip', '--time-limit', '--table-prefix',
            '--web-root', '--alert', '--results-file', '--tmp-dir', '--har',
            
            # Numeric flags
            '-v', '--verbose', '--threads', '--crawl', '--gpage'
        }
        
        # Numeric ranges for specific flags
        self.numeric_ranges = {
            '--level': (1, 5),
            '--risk': (1, 3),
            '-v': (0, 6),
            '--verbose': (0, 6),
            '--threads': (1, 100),
            '--timeout': (1, 3600),
            '--retries': (0, 50),
            '--delay': (0, 3600),
            '--time-sec': (1, 3600),
            '--safe-freq': (1, 1000),
            '--proxy-freq': (1, 1000),
            '--tor-port': (1, 65535),
            '--crawl': (0, 10),
            '--csrf-retries': (0, 10),
            '--start': (1, None),
            '--stop': (1, None),
            '--first': (1, None),
            '--last': (1, None),
            '--gpage': (1, None)
        }
        
        # Mutually exclusive flags
        self.mutually_exclusive = [
            {'--os-shell', '--sql-shell', '--os-cmd'},
            {'--dump', '--dump-all', '--sql-query'},
            {'--tor', '--proxy'},
            {'--batch', '--wizard'},
            {'--mobile', '--random-agent', '--user-agent'}
        ]
        
        # Dependent flags (flag -> required flags)
        self.dependencies = {
            '--proxy-freq': ['--proxy-file'],
            '--safe-freq': ['--safe-url', '--safe-post', '--safe-req'],
            '--dbms-cred': ['--dbms'],
            '--second-req': ['-r', '--requestfile'],
            '--second-url': ['-r', '--requestfile'],
            '--csrf-token': ['-u', '--url'],
            '--data': ['-u', '--url'],
            '--cookie': ['-u', '--url'],
            '--reg-key': ['--reg-read', '--reg-add', '--reg-del'],
            '--file-dest': ['--file-write'],
            '--pivot-column': ['--dump'],
            '--where': ['--dump'],
            '--start': ['--dump'],
            '--stop': ['--dump'],
            '--first': ['--dump'],
            '--last': ['--dump']
        }
        
        # High-risk flags requiring warnings
        self.high_risk_flags = {
            '--os-cmd': "Executes OS commands on target server",
            '--os-shell': "Provides interactive OS shell access",
            '--os-pwn': "Attempts to get Meterpreter/VNC access",
            '--os-smbrelay': "One-click shell/Meterpreter access",
            '--os-bof': "Buffer overflow exploitation",
            '--priv-esc': "Privilege escalation attempts",
            '--file-write': "Writes files to target system",
            '--file-read': "Reads files from target system",
            '--reg-add': "Modifies Windows registry",
            '--reg-del': "Deletes Windows registry entries",
            '--sql-shell': "Provides interactive SQL shell"
        }
        
        # Valid techniques
        self.valid_techniques = set('BEUSTQ')
        
        # Valid dump formats
        self.valid_dump_formats = {'CSV', 'HTML', 'SQLITE'}
        
        # Valid Tor types
        self.valid_tor_types = {'HTTP', 'SOCKS4', 'SOCKS5'}
        
        # Valid registry types
        self.valid_reg_types = {
            'REG_NONE', 'REG_SZ', 'REG_EXPAND_SZ', 'REG_BINARY',
            'REG_DWORD', 'REG_DWORD_BIG_ENDIAN', 'REG_LINK',
            'REG_MULTI_SZ', 'REG_RESOURCE_LIST'
        }
        
        # Valid HTTP methods
        self.valid_http_methods = {
            'GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS',
            'PATCH', 'CONNECT', 'TRACE'
        }
        
        # Valid auth types
        self.valid_auth_types = {
            'Basic', 'Digest', 'NTLM', 'PKI', 'Bearer'
        }
    
    def validate_command(self, command: str) -> CommandValidation:
        """Main validation method"""
        results = []
        suggested_command = None
        
        try:
            # 1. Basic command structure validation
            if not self._validate_base_command(command, results):
                return self._create_validation_result(results)
            
            # 2. Parse command into tokens
            tokens = self._parse_command(command, results)
            if not tokens:
                return self._create_validation_result(results)
            
            # 3. Extract flags and values
            flags_dict = self._extract_flags_and_values(tokens, results)
            
            # 4. Validate target specification
            self._validate_target_specification(flags_dict, results)
            
            # 5. Validate individual flags
            self._validate_flags_existence(flags_dict, results)
            
            # 6. Validate flag values
            self._validate_flag_values(flags_dict, results)
            
            # 7. Check logical compatibility
            self._validate_logical_compatibility(flags_dict, results)
            
            # 8. Check dependencies
            self._validate_dependencies(flags_dict, results)
            
            # 9. Security and risk assessment
            self._validate_security_risks(flags_dict, results)
            
            # 10. Performance and best practices
            self._validate_best_practices(flags_dict, results)
            
            # 11. Generate suggested improvements
            suggested_command = self._generate_suggestions(command, flags_dict, results)
            
        except Exception as e:
            results.append(ValidationResult(
                ValidationLevel.ERROR,
                f"Validation failed with error: {str(e)}"
            ))
        
        return self._create_validation_result(results, suggested_command)
    
    def _validate_base_command(self, command: str, results: List[ValidationResult]) -> bool:
        """Validate basic command structure"""
        if not command or not command.strip():
            results.append(ValidationResult(
                ValidationLevel.ERROR,
                "Command is empty"
            ))
            return False
        
        command = command.strip()
        
        # Check if it starts with sqlmap
        if not (command.startswith('sqlmap') or command.startswith('python sqlmap')):
            results.append(ValidationResult(
                ValidationLevel.WARNING,
                "Command should start with 'sqlmap' or 'python sqlmap'",
                suggestion="Ensure you're calling SQLmap correctly"
            ))
        
        return True
    
    def _parse_command(self, command: str, results: List[ValidationResult]) -> List[str]:
        """Parse command into tokens using shell-style parsing"""
        try:
            # Remove 'sqlmap' or 'python sqlmap.py' from the beginning
            if command.startswith('python sqlmap'):
                command = command[len('python sqlmap'):].lstrip()
            elif command.startswith('sqlmap'):
                command = command[len('sqlmap'):].lstrip()
            
            # Use shlex for proper shell-style parsing
            tokens = shlex.split(command)
            return tokens
            
        except ValueError as e:
            results.append(ValidationResult(
                ValidationLevel.ERROR,
                f"Failed to parse command: {str(e)}",
                suggestion="Check for unmatched quotes or invalid shell syntax"
            ))
            return []
    
    def _extract_flags_and_values(self, tokens: List[str], results: List[ValidationResult]) -> Dict[str, Any]:
        """Extract flags and their values from tokens"""
        flags_dict = {}
        i = 0
        
        while i < len(tokens):
            token = tokens[i]
            
            if token.startswith('-'):
                # Handle combined short flags like -uhttp://example.com
                if token.startswith('-') and not token.startswith('--') and len(token) > 2 and '=' not in token:
                    flag = token[:2]
                    value = token[2:]
                    flags_dict[flag] = value
                # Handle --flag=value format
                elif '=' in token:
                    flag, value = token.split('=', 1)
                    flags_dict[flag] = value
                # Handle --flag value format
                else:
                    flag = token
                    
                    # Check if this flag expects a value
                    if flag in self.boolean_flags:
                        flags_dict[flag] = True
                    elif flag in self.value_flags:
                        # Look for next token as value
                        if i + 1 < len(tokens) and not tokens[i + 1].startswith('-'):
                            i += 1
                            flags_dict[flag] = tokens[i]
                        else:
                            results.append(ValidationResult(
                                ValidationLevel.ERROR,
                                f"Flag '{flag}' requires a value but none provided",
                                flag=flag
                            ))
                            flags_dict[flag] = None
                    else:
                        # Unknown flag - will be caught in flag validation
                        flags_dict[flag] = True
            else:
                results.append(ValidationResult(
                    ValidationLevel.WARNING,
                    f"Unexpected token '{token}' - not a flag or value",
                    suggestion="Check command syntax"
                ))
            
            i += 1
        
        return flags_dict
    
    def _validate_target_specification(self, flags_dict: Dict[str, Any], results: List[ValidationResult]):
        """Validate that at least one target is specified"""
        found_targets = []
        
        for flag in flags_dict.keys():
            if flag in self.target_flags:
                found_targets.append(flag)
        
        if not found_targets:
            results.append(ValidationResult(
                ValidationLevel.ERROR,
                "No target specification found",
                suggestion="Add at least one target flag: -u, -d, -l, -m, -r, -g, or -c"
            ))
        elif len(found_targets) > 1:
            results.append(ValidationResult(
                ValidationLevel.WARNING,
                f"Multiple target specifications found: {', '.join(found_targets)}",
                suggestion="Use only one target specification method"
            ))
    
    def _validate_flags_existence(self, flags_dict: Dict[str, Any], results: List[ValidationResult]):
        """Validate that all flags are supported by SQLmap"""
        all_valid_flags = self.boolean_flags | self.value_flags | self.target_flags
        
        for flag in flags_dict.keys():
            if flag not in all_valid_flags:
                results.append(ValidationResult(
                    ValidationLevel.ERROR,
                    f"Unknown or unsupported flag: '{flag}'",
                    flag=flag,
                    suggestion="Check SQLmap help (sqlmap -hh) for valid flags"
                ))
    
    def _validate_flag_values(self, flags_dict: Dict[str, Any], results: List[ValidationResult]):
        """Validate individual flag values"""
        for flag, value in flags_dict.items():
            if flag in self.boolean_flags and value is not True:
                results.append(ValidationResult(
                    ValidationLevel.WARNING,
                    f"Boolean flag '{flag}' should not have a value",
                    flag=flag
                ))
            
            elif flag in self.value_flags and (value is None or value is True):
                results.append(ValidationResult(
                    ValidationLevel.ERROR,
                    f"Flag '{flag}' requires a value",
                    flag=flag
                ))
            
            elif value is not None and value is not True:
                self._validate_specific_flag_value(flag, value, results)
    
    def _validate_specific_flag_value(self, flag: str, value: str, results: List[ValidationResult]):
        """Validate specific flag values based on their type"""
        # Numeric range validation
        if flag in self.numeric_ranges:
            try:
                num_value = int(value)
                min_val, max_val = self.numeric_ranges[flag]
                
                if num_value < min_val:
                    results.append(ValidationResult(
                        ValidationLevel.ERROR,
                        f"Flag '{flag}' value {num_value} is below minimum {min_val}",
                        flag=flag
                    ))
                elif max_val is not None and num_value > max_val:
                    results.append(ValidationResult(
                        ValidationLevel.ERROR,
                        f"Flag '{flag}' value {num_value} exceeds maximum {max_val}",
                        flag=flag
                    ))
            except ValueError:
                results.append(ValidationResult(
                    ValidationLevel.ERROR,
                    f"Flag '{flag}' requires a numeric value, got '{value}'",
                    flag=flag
                ))
        
        # URL validation
        elif flag in ['-u', '--url']:
            if not self._validate_url(value):
                results.append(ValidationResult(
                    ValidationLevel.ERROR,
                    f"Invalid URL format: '{value}'",
                    flag=flag,
                    suggestion="URL should start with http:// or https://"
                ))
        
        # Technique validation
        elif flag == '--technique':
            invalid_chars = set(value.upper()) - self.valid_techniques
            if invalid_chars:
                results.append(ValidationResult(
                    ValidationLevel.ERROR,
                    f"Invalid technique characters: {', '.join(invalid_chars)}",
                    flag=flag,
                    suggestion="Valid techniques: B(Boolean), E(Error), U(Union), S(Stacked), T(Time), Q(Query)"
                ))
        
        # Dump format validation
        elif flag == '--dump-format':
            if value.upper() not in self.valid_dump_formats:
                results.append(ValidationResult(
                    ValidationLevel.ERROR,
                    f"Invalid dump format: '{value}'",
                    flag=flag,
                    suggestion=f"Valid formats: {', '.join(self.valid_dump_formats)}"
                ))
        
        # Tor type validation
        elif flag == '--tor-type':
            if value.upper() not in self.valid_tor_types:
                results.append(ValidationResult(
                    ValidationLevel.ERROR,
                    f"Invalid Tor type: '{value}'",
                    flag=flag,
                    suggestion=f"Valid types: {', '.join(self.valid_tor_types)}"
                ))
        
        # HTTP method validation
        elif flag == '--method':
            if value.upper() not in self.valid_http_methods:
                results.append(ValidationResult(
                    ValidationLevel.WARNING,
                    f"Uncommon HTTP method: '{value}'",
                    flag=flag,
                    suggestion=f"Common methods: {', '.join(sorted(self.valid_http_methods))}"
                ))
        
        # Registry type validation
        elif flag == '--reg-type':
            if value.upper() not in self.valid_reg_types:
                results.append(ValidationResult(
                    ValidationLevel.ERROR,
                    f"Invalid registry type: '{value}'",
                    flag=flag,
                    suggestion=f"Valid types: {', '.join(sorted(self.valid_reg_types))}"
                ))
        
        # File path validation
        elif flag in ['--tamper', '--auth-file', '-r', '--requestfile', '-l', '--logfile', 
                      '-m', '--bulkfile', '--sql-file', '--load-cookies', '--live-cookies']:
            if not os.path.isfile(value):
                results.append(ValidationResult(
                    ValidationLevel.WARNING,
                    f"File not found: '{value}'",
                    flag=flag,
                    suggestion="Ensure the file path is correct and accessible"
                ))
        
        # Directory path validation
        elif flag in ['--output-dir', '--tmp-dir']:
            if not os.path.isdir(value):
                results.append(ValidationResult(
                    ValidationLevel.WARNING,
                    f"Directory not found: '{value}'",
                    flag=flag,
                    suggestion="Ensure the directory path is correct and accessible"
                ))
    
    def _validate_logical_compatibility(self, flags_dict: Dict[str, Any], results: List[ValidationResult]):
        """Check for mutually exclusive flags"""
        for exclusive_group in self.mutually_exclusive:
            found_flags = [flag for flag in exclusive_group if flag in flags_dict]
            
            if len(found_flags) > 1:
                results.append(ValidationResult(
                    ValidationLevel.WARNING,
                    f"Mutually exclusive flags found: {', '.join(found_flags)}",
                    suggestion="Use only one of these flags at a time"
                ))
    
    def _validate_dependencies(self, flags_dict: Dict[str, Any], results: List[ValidationResult]):
        """Check flag dependencies"""
        # Create mapping of short to long flags for dependency checking
        flag_mapping = {
            '-u': '--url',
            '-d': '--direct',
            '-r': '--requestfile',
            '-l': '--logfile',
            '-m': '--bulkfile',
            '-g': '--googledork',
            '-c': '--configfile',
            '-s': '--sessionfile',
            '-t': '--trafficfile',
            '-v': '--verbose',
            '-D': '--db',
            '-T': '--tbl',
            '-C': '--col',
            '-U': '--user',
            '-X': '--exclude'
        }
        
        # Create reverse mapping and add both forms to check set
        all_flags = set(flags_dict.keys())
        for short, long_flag in flag_mapping.items():
            if short in flags_dict:
                all_flags.add(long_flag)
            if long_flag in flags_dict:
                all_flags.add(short)
        
        for flag, required_flags in self.dependencies.items():
            if flag in flags_dict:
                missing_deps = []
                for req_flag in required_flags:
                    # Check if any of the required flags (if it's a list) is present
                    if isinstance(req_flag, list):
                        if not any(rf in all_flags for rf in req_flag):
                            missing_deps.extend(req_flag)
                    elif req_flag not in all_flags:
                        missing_deps.append(req_flag)
                
                if missing_deps:
                    results.append(ValidationResult(
                        ValidationLevel.ERROR,
                        f"Flag '{flag}' requires one of: {', '.join(missing_deps)}",
                        flag=flag
                    ))
    
    def _validate_security_risks(self, flags_dict: Dict[str, Any], results: List[ValidationResult]):
        """Identify high-risk operations"""
        for flag, description in self.high_risk_flags.items():
            if flag in flags_dict:
                results.append(ValidationResult(
                    ValidationLevel.WARNING,
                    f"HIGH RISK: {description}",
                    flag=flag,
                    suggestion="Ensure you have proper authorization before using this flag"
                ))
    
    def _validate_best_practices(self, flags_dict: Dict[str, Any], results: List[ValidationResult]):
        """Suggest best practices"""
        # Suggest --batch for automation
        if '--batch' not in flags_dict and any(flag in flags_dict for flag in ['--dump', '--dump-all', '--sql-shell']):
            results.append(ValidationResult(
                ValidationLevel.INFO,
                "Consider adding --batch for non-interactive execution",
                suggestion="Add --batch to avoid prompts during automated scans"
            ))
        
        # Suggest --random-agent for WAF evasion
        if '-u' in flags_dict and '--random-agent' not in flags_dict and '--user-agent' not in flags_dict:
            results.append(ValidationResult(
                ValidationLevel.INFO,
                "Consider using --random-agent to evade WAF detection",
                suggestion="Add --random-agent for better evasion"
            ))
        
        # Suggest --level and --risk for thorough testing
        if '--level' not in flags_dict:
            results.append(ValidationResult(
                ValidationLevel.INFO,
                "Default level is 1. Consider increasing --level for more thorough testing",
                suggestion="Use --level 3-5 for comprehensive scans"
            ))
        
        # Performance suggestions
        if '--threads' not in flags_dict and '-u' in flags_dict:
            results.append(ValidationResult(
                ValidationLevel.INFO,
                "Consider using --threads to speed up testing",
                suggestion="Add --threads 5-10 for faster scans (be careful with server load)"
            ))
    
    def _validate_url(self, url: str) -> bool:
        """Validate URL format"""
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        return url_pattern.match(url) is not None
    
    def _generate_suggestions(self, original_command: str, flags_dict: Dict[str, Any], 
                            results: List[ValidationResult]) -> Optional[str]:
        """Generate improved command suggestions"""
        # This would contain logic to create an optimized version of the command
        # based on the validation results and best practices
        return None  # Placeholder for now
    
    def _create_validation_result(self, results: List[ValidationResult], 
                                suggested_command: Optional[str] = None) -> CommandValidation:
        """Create final validation result"""
        errors = [r for r in results if r.level == ValidationLevel.ERROR]
        warnings = [r for r in results if r.level == ValidationLevel.WARNING]
        infos = [r for r in results if r.level == ValidationLevel.INFO]
        
        is_valid = len(errors) == 0
        
        return CommandValidation(
            is_valid=is_valid,
            results=results,
            errors=errors,
            warnings=warnings,
            infos=infos,
            suggested_command=suggested_command
        )
    
    def format_validation_report(self, validation: CommandValidation) -> str:
        """Format validation results into a readable report"""
        report = []
        
        if validation.is_valid:
            report.append("✅ Command is valid!")
        else:
            report.append("❌ Command has errors and cannot be executed")
        
        if validation.errors:
            report.append("\n🚨 ERRORS:")
            for error in validation.errors:
                flag_info = f" ({error.flag})" if error.flag else ""
                report.append(f"  • {error.message}{flag_info}")
                if error.suggestion:
                    report.append(f"    💡 {error.suggestion}")
        
        if validation.warnings:
            report.append("\n⚠️  WARNINGS:")
            for warning in validation.warnings:
                flag_info = f" ({warning.flag})" if warning.flag else ""
                report.append(f"  • {warning.message}{flag_info}")
                if warning.suggestion:
                    report.append(f"    💡 {warning.suggestion}")
        
        if validation.infos:
            report.append("\n💡 SUGGESTIONS:")
            for info in validation.infos:
                report.append(f"  • {info.message}")
                if info.suggestion:
                    report.append(f"    💡 {info.suggestion}")
        
        if validation.suggested_command:
            report.append(f"\n🔧 SUGGESTED COMMAND:\n{validation.suggested_command}")
        
        return "\n".join(report)


# Example usage and testing
if __name__ == "__main__":
    validator = SqlmapValidator()
    
    # Test commands
    test_commands = [
        "sqlmap -u http://example.com/page.php?id=1 --batch",
        "sqlmap -u http://example.com --level 6",  # Invalid level
        "sqlmap --dump",  # Missing target
        "sqlmap -u http://example.com --os-shell --sql-shell",  # Mutually exclusive
        "sqlmap -u http://example.com --proxy-freq 1",  # Missing dependency
        "python sqlmap -u http://example.com --batch --random-agent --level 3"
    ]
    
    for cmd in test_commands:
        print(f"\n{'='*60}")
        print(f"Testing: {cmd}")
        print('='*60)
        
        validation = validator.validate_command(cmd)
        report = validator.format_validation_report(validation)
        print(report)
