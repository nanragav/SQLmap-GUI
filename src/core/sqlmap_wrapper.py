#!/usr/bin/env python3
"""
Complete SQLmap Wrapper Rebuild
Fix all the critical issues and make it production-ready
"""

import os
import sys
import subprocess
import re
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass
from enum import Enum
import json
import threading
import time
from queue import Queue, Empty

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

class ValidationLevel(Enum):
    ERROR = "error"
    WARNING = "warning" 
    INFO = "info"

@dataclass
class ValidationIssue:
    level: ValidationLevel
    parameter: str
    message: str
    suggestion: Optional[str] = None
    risk_level: Optional[str] = None
    flag: Optional[str] = None  # For compatibility with validation dialog

# Alias for backward compatibility with validation dialog
ValidationResult = ValidationIssue

@dataclass
class CommandValidation:
    is_valid: bool
    errors: List[ValidationIssue]
    warnings: List[ValidationIssue] 
    command: List[str]
    infos: List[ValidationIssue] = None  # For compatibility with validation dialog
    suggested_command: Optional[str] = None  # For compatibility with validation dialog
    
    def __post_init__(self):
        if self.infos is None:
            self.infos = []
        if self.suggested_command is None and self.command:
            self.suggested_command = ' '.join(self.command)
    
    @property
    def results(self) -> List[ValidationIssue]:
        """Combined results for compatibility"""
        return self.errors + self.warnings + self.infos
    
class SqlmapProcess:
    """Manages SQLmap process execution and monitoring"""
    
    def __init__(self, command: List[str], sudo_password: str = None, output_callback: Optional[callable] = None):
        self.command = command
        self.sudo_password = sudo_password
        self.process = None
        self.output_callback = output_callback
        self.is_running = False
        self.output_queue = Queue()
        self.error_queue = Queue()
        self.start_time = None
        self.end_time = None
        
    def start(self) -> bool:
        """Start the SQLmap process"""
        try:
            self.start_time = time.time()
            # Use environment similar to manual execution
            env = os.environ.copy()
            
            self.process = subprocess.Popen(
                self.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True,
                env=env,
                cwd=os.getcwd()  # Use current working directory
            )
            
            self.is_running = True
            
            # Handle sudo password if needed
            if self.sudo_password and self.command[0] == 'sudo':
                self._handle_sudo_password()
            
            # Start output monitoring threads
            threading.Thread(target=self._monitor_output, daemon=True).start()
            threading.Thread(target=self._monitor_error, daemon=True).start()
            
            return True
        except Exception as e:
            print(f"Error starting SQLmap process: {e}")
            return False
    
    def _handle_sudo_password(self):
        """Handle sudo password input with proper timing and error handling"""
        def send_password():
            try:
                # Wait for sudo to be ready for password input
                time.sleep(1)
                
                # Check if process is still running
                if self.process.poll() is not None:
                    print(f"Sudo process terminated early with code: {self.process.returncode}")
                    return False
                
                # Send password with newline
                try:
                    self.process.stdin.write(self.sudo_password + '\n')
                    self.process.stdin.flush()
                    print("Sudo password sent successfully")
                except BrokenPipeError:
                    # This is expected - sudo closes stdin after authentication
                    print("Sudo password sent (stdin closed as expected)")
                
                # Wait a moment for authentication
                time.sleep(1)
                
                # Check if sudo accepted the password by looking for process status
                if self.process.poll() is None:
                    # Process still running, likely authentication successful
                    return True
                else:
                    # Process terminated, check exit code
                    return_code = self.process.returncode
                    if return_code == 0:
                        print("Sudo authentication successful")
                        return True
                    else:
                        print(f"Sudo authentication failed with return code: {return_code}")
                        return False
                        
            except Exception as e:
                print(f"Error sending sudo password: {e}")
                return False
        
        # Send password in a separate thread to avoid blocking
        password_thread = threading.Thread(target=send_password, daemon=True)
        password_thread.start()
    
    def stop(self) -> bool:
        """Stop the SQLmap process"""
        if self.process and self.is_running:
            try:
                # Try graceful termination first
                self.process.terminate()
                
                # Wait for process to terminate
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    # Force kill if not terminated
                    self.process.kill()
                    self.process.wait()
                
                self.is_running = False
                self.end_time = time.time()
                return True
            except Exception as e:
                print(f"Error stopping SQLmap process: {e}")
                return False
        return False
    
    def send_input(self, input_text: str) -> bool:
        """Send input to the SQLmap process"""
        if self.process and self.is_running:
            try:
                self.process.stdin.write(input_text + '\n')
                self.process.stdin.flush()
                return True
            except Exception as e:
                print(f"Error sending input: {e}")
                return False
        return False
    
    def _monitor_output(self):
        """Monitor stdout in a separate thread"""
        if not self.process:
            return
        
        try:
            for line in iter(self.process.stdout.readline, ''):
                if line:
                    self.output_queue.put(line.rstrip())
                    if self.output_callback and callable(self.output_callback):
                        self.output_callback(line.rstrip())
        except Exception as e:
            print(f"Error monitoring output: {e}")
        finally:
            if self.process:
                self.process.stdout.close()
    
    def _monitor_error(self):
        """Monitor stderr in a separate thread"""
        if not self.process:
            return
        
        try:
            for line in iter(self.process.stderr.readline, ''):
                if line:
                    self.error_queue.put(line.rstrip())
        except Exception as e:
            print(f"Error monitoring error output: {e}")
        finally:
            if self.process:
                self.process.stderr.close()
    
    def get_output(self) -> List[str]:
        """Get all available output lines"""
        lines = []
        try:
            while True:
                line = self.output_queue.get_nowait()
                lines.append(line)
        except Empty:
            pass
        return lines
    
    def get_errors(self) -> List[str]:
        """Get all available error lines"""
        lines = []
        try:
            while True:
                line = self.error_queue.get_nowait()
                lines.append(line)
        except Empty:
            pass
        return lines
    
    def get_status(self) -> Dict[str, Any]:
        """Get current process status"""
        status = {
            'running': self.is_running,
            'pid': self.process.pid if self.process else None,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'duration': None,
            'return_code': None,
            'memory_mb': 0,
            'cpu_percent': 0
        }
        
        if self.start_time:
            end_time = self.end_time or time.time()
            status['duration'] = end_time - self.start_time
        
        if self.process:
            status['return_code'] = self.process.returncode
            
            # Get resource usage if process is running
            if self.is_running and self.process.pid and HAS_PSUTIL:
                try:
                    proc = psutil.Process(self.process.pid)
                    status['memory_mb'] = proc.memory_info().rss / 1024 / 1024
                    status['cpu_percent'] = proc.cpu_percent()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        
        return status
    
    def get_exit_code(self) -> Optional[int]:
        """Get the process exit code"""
        if self.process:
            return self.process.returncode
        return None
    
    def read_output(self) -> Optional[str]:
        """Read available output from the process"""
        try:
            if not self.output_queue.empty():
                return self.output_queue.get_nowait()
        except:
            pass
        return None
    
    def read_error(self) -> Optional[str]:
        """Read available error output from the process"""
        try:
            if not self.error_queue.empty():
                return self.error_queue.get_nowait()
        except:
            pass
        return None

class SqlmapWrapper:
    """Complete SQLmap wrapper with full parameter support"""
    
    def __init__(self, sqlmap_path: str = "sqlmap"):
        self.sqlmap_path = sqlmap_path
        self._check_sqlmap_availability()
        self._load_all_parameters()
        self._load_target_params()
        self._load_mutual_exclusions()
        self._load_high_risk_params()
        self._check_python_availability()
    
    def _check_python_availability(self):
        """Check Python availability and set the correct interpreter"""
        # Check for python3 first, then python
        self.python_cmd = None
        
        for cmd in ['python3', 'python']:
            try:
                result = subprocess.run([cmd, '--version'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    self.python_cmd = cmd
                    print(f"Found Python interpreter: {cmd} - {result.stdout.strip()}")
                    break
            except (FileNotFoundError, subprocess.TimeoutExpired):
                continue
        
        if not self.python_cmd:
            print("Warning: No Python interpreter found!")
    
    def _check_sqlmap_availability(self):
        """Check if sqlmap is available and get its version"""
        try:
            # Try running sqlmap directly first
            result = subprocess.run([self.sqlmap_path, '--version'], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print(f"SQLmap found: {result.stdout.strip()}")
                return
            
            # If direct execution fails, try with python interpreter
            if self.python_cmd and hasattr(self, 'python_cmd'):
                result = subprocess.run([self.python_cmd, self.sqlmap_path, '--version'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print(f"SQLmap found (via {self.python_cmd}): {result.stdout.strip()}")
                    # Use python interpreter to run sqlmap
                    self.sqlmap_path = [self.python_cmd, self.sqlmap_path]
                else:
                    print(f"Warning: SQLmap returned non-zero exit code: {result.returncode}")
                    if result.stderr:
                        print(f"SQLmap stderr: {result.stderr.strip()}")
            else:
                print(f"Warning: SQLmap not found at path: {self.sqlmap_path}")
                print("Make sure SQLmap is installed and in your PATH")
                
        except FileNotFoundError:
            print(f"Warning: SQLmap not found at path: {self.sqlmap_path}")
            print("Make sure SQLmap is installed and in your PATH")
        except subprocess.TimeoutExpired:
            print("Warning: SQLmap --version command timed out")
        except Exception as e:
            print(f"Warning: Error checking SQLmap availability: {e}")
    
    def _load_all_parameters(self):
        """Load ALL SQLmap parameters with proper mappings"""
        import shlex
        
        # Complete parameter mappings from SQLmap -hh
        self.all_params = {
            # TARGET PARAMETERS
            'url': {'flag': '-u', 'type': 'quoted_arg', 'long': '--url'},
            'direct': {'flag': '-d', 'type': 'quoted_arg'},
            'log_file': {'flag': '-l', 'type': 'quoted_arg'},
            'bulk_file': {'flag': '-m', 'type': 'quoted_arg'},
            'request_file': {'flag': '-r', 'type': 'quoted_arg'},
            
            # REQUEST PARAMETERS
            'method': {'flag': '--method', 'type': 'quoted_arg'},
            'data': {'flag': '--data', 'type': 'quoted_arg'},
            'cookie': {'flag': '--cookie', 'type': 'quoted_arg'},
            'load_cookies': {'flag': '--load-cookies', 'type': 'quoted_arg'},
            'random_agent': {'flag': '--random-agent', 'type': 'flag'},
            'user_agent': {'flag': '--user-agent', 'type': 'quoted_arg'},
            'host': {'flag': '--host', 'type': 'quoted_arg'},
            'referer': {'flag': '--referer', 'type': 'quoted_arg'},
            'headers': {'flag': '--headers', 'type': 'quoted_arg'},
            'auth_type': {'flag': '--auth-type', 'type': 'quoted_arg'},
            'auth_cred': {'flag': '--auth-cred', 'type': 'quoted_arg'},
            'proxy': {'flag': '--proxy', 'type': 'quoted_arg'},
            'tor': {'flag': '--tor', 'type': 'flag'},
            'tor_port': {'flag': '--tor-port', 'type': 'quoted_arg'},
            'tor_type': {'flag': '--tor-type', 'type': 'quoted_arg'},
            'check_tor': {'flag': '--check-tor', 'type': 'flag'},
            
            # INJECTION PARAMETERS
            'testable_parameter': {'flag': '-p', 'type': 'quoted_arg'},
            'skip': {'flag': '--skip', 'type': 'quoted_arg'},
            'skip_static': {'flag': '--skip-static', 'type': 'flag'},
            'dbms': {'flag': '--dbms', 'type': 'quoted_arg'},
            'os': {'flag': '--os', 'type': 'quoted_arg'},
            'invalid_bignum': {'flag': '--invalid-bignum', 'type': 'flag'},
            'invalid_logical': {'flag': '--invalid-logical', 'type': 'flag'},
            'invalid_string': {'flag': '--invalid-string', 'type': 'flag'},
            'no_cast': {'flag': '--no-cast', 'type': 'flag'},
            'no_escape': {'flag': '--no-escape', 'type': 'flag'},
            'prefix': {'flag': '--prefix', 'type': 'quoted_arg'},
            'suffix': {'flag': '--suffix', 'type': 'quoted_arg'},
            'tamper': {'flag': '--tamper', 'type': 'quoted_arg'},
            
            # BOOLEAN-BASED BLIND (CORRECTED mappings)
            'string': {'flag': '--string', 'type': 'quoted_arg'},
            'not_string': {'flag': '--not-string', 'type': 'quoted_arg'},
            
            # TECHNIQUE PARAMETERS
            'technique': {'flag': '--technique', 'type': 'quoted_arg'},
            'union_cols': {'flag': '--union-cols', 'type': 'quoted_arg'},
            'union_char': {'flag': '--union-char', 'type': 'quoted_arg'},
            'union_from': {'flag': '--union-from', 'type': 'quoted_arg'},
            'dns_domain': {'flag': '--dns-domain', 'type': 'quoted_arg'},
            'second_url': {'flag': '--second-url', 'type': 'quoted_arg'},
            'second_req': {'flag': '--second-req', 'type': 'quoted_arg'},
            'time_sec': {'flag': '--time-sec', 'type': 'quoted_arg'},
            
            # DETECTION PARAMETERS
            'level': {'flag': '--level', 'type': 'quoted_arg'},
            'risk': {'flag': '--risk', 'type': 'quoted_arg'},
            'regexp': {'flag': '--regexp', 'type': 'quoted_arg'},
            'code': {'flag': '--code', 'type': 'quoted_arg'},
            'text_only': {'flag': '--text-only', 'type': 'flag'},
            'titles': {'flag': '--titles', 'type': 'flag'},
            'smart': {'flag': '--smart', 'type': 'flag'},
            
            # ENUMERATION PARAMETERS
            'all': {'flag': '--all', 'type': 'flag'},
            'banner': {'flag': '--banner', 'type': 'flag'},
            'current_user': {'flag': '--current-user', 'type': 'flag'},
            'current_db': {'flag': '--current-db', 'type': 'flag'},
            'hostname': {'flag': '--hostname', 'type': 'flag'},
            'is_dba': {'flag': '--is-dba', 'type': 'flag'},
            'users': {'flag': '--users', 'type': 'flag'},
            'passwords': {'flag': '--passwords', 'type': 'flag'},
            'privileges': {'flag': '--privileges', 'type': 'flag'},
            'roles': {'flag': '--roles', 'type': 'flag'},
            'dbs': {'flag': '--dbs', 'type': 'flag'},
            'tables': {'flag': '--tables', 'type': 'flag'},
            'columns': {'flag': '--columns', 'type': 'flag'},
            'schema': {'flag': '--schema', 'type': 'flag'},
            'count': {'flag': '--count', 'type': 'flag'},
            'dump': {'flag': '--dump', 'type': 'flag'},
            'dump_all': {'flag': '--dump-all', 'type': 'flag'},
            'search': {'flag': '--search', 'type': 'flag'},
            'comments': {'flag': '--comments', 'type': 'flag'},
            'statements': {'flag': '--statements', 'type': 'flag'},
            'db': {'flag': '-D', 'type': 'quoted_arg'},
            'tbl': {'flag': '-T', 'type': 'quoted_arg'},
            'col': {'flag': '-C', 'type': 'quoted_arg'},
            'user': {'flag': '-U', 'type': 'quoted_arg'},
            'where': {'flag': '--where', 'type': 'quoted_arg'},
            'start': {'flag': '--start', 'type': 'quoted_arg'},
            'stop': {'flag': '--stop', 'type': 'quoted_arg'},
            'first': {'flag': '--first', 'type': 'quoted_arg'},
            'last': {'flag': '--last', 'type': 'quoted_arg'},
            'sql_query': {'flag': '--sql-query', 'type': 'quoted_arg'},
            'sql_shell': {'flag': '--sql-shell', 'type': 'flag'},
            'sql_file': {'flag': '--sql-file', 'type': 'quoted_arg'},
            'common_tables': {'flag': '--common-tables', 'type': 'flag'},
            'common_columns': {'flag': '--common-columns', 'type': 'flag'},
            'common_files': {'flag': '--common-files', 'type': 'flag'},
            
            # FILE SYSTEM ACCESS
            'file_read': {'flag': '--file-read', 'type': 'quoted_arg'},
            'file_write': {'flag': '--file-write', 'type': 'quoted_arg'},
            'file_dest': {'flag': '--file-dest', 'type': 'quoted_arg'},
            
            # OS ACCESS
            'os_cmd': {'flag': '--os-cmd', 'type': 'quoted_arg'},
            'os_shell': {'flag': '--os-shell', 'type': 'flag'},
            'os_pwn': {'flag': '--os-pwn', 'type': 'flag'},
            'os_smbrelay': {'flag': '--os-smbrelay', 'type': 'flag'},
            'os_bof': {'flag': '--os-bof', 'type': 'flag'},
            'priv_esc': {'flag': '--priv-esc', 'type': 'flag'},
            'msf_path': {'flag': '--msf-path', 'type': 'quoted_arg'},
            'tmp_path': {'flag': '--tmp-path', 'type': 'quoted_arg'},
            
            # WINDOWS REGISTRY
            'reg_read': {'flag': '--reg-read', 'type': 'flag'},
            'reg_add': {'flag': '--reg-add', 'type': 'flag'},
            'reg_del': {'flag': '--reg-del', 'type': 'flag'},
            'reg_key': {'flag': '--reg-key', 'type': 'quoted_arg'},
            'reg_value': {'flag': '--reg-value', 'type': 'quoted_arg'},
            'reg_data': {'flag': '--reg-data', 'type': 'quoted_arg'},
            
            # UDF INJECTION
            'udf_inject': {'flag': '--udf-inject', 'type': 'flag'},
            'shared_lib': {'flag': '--shared-lib', 'type': 'quoted_arg'},
            
            # GENERAL OPTIONS
            'batch': {'flag': '--batch', 'type': 'flag'},
            'abort_on_empty': {'flag': '--abort-on-empty', 'type': 'flag'},
            'flush_session': {'flag': '--flush-session', 'type': 'flag'},
            'fresh_queries': {'flag': '--fresh-queries', 'type': 'flag'},
            'cleanup': {'flag': '--cleanup', 'type': 'flag'},
            'answers': {'flag': '--answers', 'type': 'quoted_arg'},
            'forms': {'flag': '--forms', 'type': 'flag'},
            'crawl': {'flag': '--crawl', 'type': 'quoted_arg'},
            'crawl_exclude': {'flag': '--crawl-exclude', 'type': 'quoted_arg'},
            'charset': {'flag': '--charset', 'type': 'quoted_arg'},
            'encoding': {'flag': '--encoding', 'type': 'quoted_arg'},
            'base64': {'flag': '--base64', 'type': 'quoted_arg'},
            'base64_safe': {'flag': '--base64-safe', 'type': 'flag'},
            'web_root': {'flag': '--web-root', 'type': 'quoted_arg'},
            'force_ssl': {'flag': '--force-ssl', 'type': 'flag'},
            
            # MISCELLANEOUS
            'alert': {'flag': '--alert', 'type': 'quoted_arg'},
            'beep': {'flag': '--beep', 'type': 'flag'},
            'dependencies': {'flag': '--dependencies', 'type': 'flag'},
            'disable_coloring': {'flag': '--disable-coloring', 'type': 'flag'},
            'offline': {'flag': '--offline', 'type': 'flag'},
            'purge': {'flag': '--purge', 'type': 'flag'},
            'skip_heuristics': {'flag': '--skip-heuristics', 'type': 'flag'},
            'skip_waf': {'flag': '--skip-waf', 'type': 'flag'},
            'unstable': {'flag': '--unstable', 'type': 'flag'},
            'session_file': {'flag': '-s', 'type': 'quoted_arg'},
            'traffic_file': {'flag': '--traffic-file', 'type': 'quoted_arg'},
            'output_dir': {'flag': '-o', 'type': 'quoted_arg'},
            'fingerprint': {'flag': '--fingerprint', 'type': 'flag'},
            'keep_alive': {'flag': '--keep-alive', 'type': 'flag'},
            'null_connection': {'flag': '--null-connection', 'type': 'flag'},
            'optimize': {'flag': '-o', 'type': 'flag'},
            'threads': {'flag': '--threads', 'type': 'quoted_arg'},
            'timeout': {'flag': '--timeout', 'type': 'quoted_arg'},
            'retries': {'flag': '--retries', 'type': 'quoted_arg'},
            'delay': {'flag': '--delay', 'type': 'quoted_arg'},
            'hpp': {'flag': '--hpp', 'type': 'flag'},
            'chunked': {'flag': '--chunked', 'type': 'flag'},
            
            # GUI-specific options (valid)
            'auto_batch': {'flag': '--batch', 'type': 'flag'},
            'tamper_custom': {'flag': '--tamper', 'type': 'quoted_arg'},
            'list_tampers_btn': {'flag': '--list-tampers', 'type': 'flag'},
            
            # TECHNIQUE CHECKBOXES (GUI mappings to build --technique string)
            'boolean_blind': {'flag': '--technique', 'type': 'technique', 'value': 'B'},
            'error_based': {'flag': '--technique', 'type': 'technique', 'value': 'E'},
            'union_based': {'flag': '--technique', 'type': 'technique', 'value': 'U'},
            'stacked_queries': {'flag': '--technique', 'type': 'technique', 'value': 'S'},
            'time_based': {'flag': '--technique', 'type': 'technique', 'value': 'T'},
            'inline_queries': {'flag': '--technique', 'type': 'technique', 'value': 'Q'}
        }
    
    def _load_target_params(self):
        """Load target parameter definitions"""
        self.target_params = {
            'url': {'flag': '-u', 'type': 'quoted_arg', 'description': 'Target URL'},
            'direct': {'flag': '-d', 'type': 'quoted_arg', 'description': 'Direct connection string'},
            'log_file': {'flag': '-l', 'type': 'quoted_arg', 'description': 'Parse targets from Burp/ZAP proxy log'},
            'bulk_file': {'flag': '-m', 'type': 'quoted_arg', 'description': 'Scan multiple targets from file'},
            'request_file': {'flag': '-r', 'type': 'quoted_arg', 'description': 'Load HTTP request from file'},
            'google_dork': {'flag': '-g', 'type': 'quoted_arg', 'description': 'Process Google dork results'}
        }
    
    def _load_mutual_exclusions(self):
        """Load mutual exclusion groups"""
        self.mutual_exclusions = {
            'target_input': ['url', 'direct', 'log_file', 'bulk_file', 'request_file', 'google_dork'],
            'user_agent_type': ['user_agent', 'random_agent', 'mobile'],
            'proxy_type': ['proxy', 'tor'],
            'shell_access': ['sql_shell', 'os_shell', 'os_cmd'],
            'data_output': ['dump_all', 'sql_query', 'dump'],
            'crawl_vs_threads': ['crawl', 'threads'],
            'batch_vs_wizard': ['batch', 'wizard']
        }
    
    def _load_high_risk_params(self):
        """Load high-risk parameter definitions"""
        self.high_risk_params = {
            'os_shell': {
                'risk_level': 'HIGH RISK',
                'warning': 'OS shell access can compromise the target system',
                'flag': '--os-shell'
            },
            'os_cmd': {
                'risk_level': 'HIGH RISK', 
                'warning': 'OS command execution can compromise the target system',
                'flag': '--os-cmd'
            },
            'os_pwn': {
                'risk_level': 'HIGH RISK',
                'warning': 'OS takeover can completely compromise the target system',
                'flag': '--os-pwn'
            },
            'priv_esc': {
                'risk_level': 'HIGH RISK',
                'warning': 'Privilege escalation can lead to full system compromise',
                'flag': '--priv-esc'
            },
            'file_write': {
                'risk_level': 'MEDIUM RISK',
                'warning': 'File writing can modify target system files',
                'flag': '--file-write'
            },
            'sql_shell': {
                'risk_level': 'MEDIUM RISK',
                'warning': 'SQL shell access allows arbitrary database queries',
                'flag': '--sql-shell'
            },
            'dump_all': {
                'risk_level': 'MEDIUM RISK',
                'warning': 'Dumping all data can expose sensitive information',
                'flag': '--dump-all'
            }
        }
    
    def build_command(self, options: Dict[str, Any], force_batch: bool = True) -> List[str]:
        """Build complete SQLmap command with smart parameter handling"""
        import shlex
        
        # Handle sqlmap_path being a list (when using python interpreter)
        if isinstance(self.sqlmap_path, list):
            cmd = self.sqlmap_path.copy()
        else:
            cmd = [self.sqlmap_path]
        
        # Handle auto-batch
        if force_batch and not options.get('batch'):
            if options.get('auto_batch', True):
                options = options.copy()
                options['batch'] = True
        
        # Remove GUI-specific options
        gui_options = {'auto_batch', '_metadata'}
        processed_options = {k: v for k, v in options.items() if k not in gui_options}
        
        # Add flags to ensure non-interactive operation
        if force_batch:
            processed_options['batch'] = True
            processed_options['disable_coloring'] = True  # Disable ANSI color codes
            processed_options['purge'] = False  # Don't purge session files in batch mode
        
        # Track flags already added to avoid duplicates
        flags_added = set()
        
        # No special handling needed for prefix/suffix conflicts anymore since
        # bool_true/bool_false now map to --string/--not-string correctly
        
        # Handle technique parameters - build technique string from checkboxes
        technique_chars = []
        if processed_options.get('boolean_blind'):
            technique_chars.append('B')
        if processed_options.get('error_based'):
            technique_chars.append('E')
        if processed_options.get('union_based'):
            technique_chars.append('U')
        if processed_options.get('stacked_queries'):
            technique_chars.append('S')
        if processed_options.get('time_based'):
            technique_chars.append('T')
        if processed_options.get('inline_queries'):
            technique_chars.append('Q')
        
        # Add technique parameter if any techniques selected
        if technique_chars and '--technique' not in flags_added:
            technique_string = ''.join(technique_chars)
            cmd.extend(['--technique', technique_string])
            flags_added.add('--technique')
        
        # Process all other parameters
        for param_name, param_value in processed_options.items():
            if param_name in self.all_params and param_value is not None:
                param_def = self.all_params[param_name]
                flag = param_def['flag']
                param_type = param_def['type']
                
                # Skip if this flag was already handled in special cases
                if flag in flags_added:
                    continue
                
                # Skip GUI-only parameters that don't have SQLmap equivalents
                if param_type == 'gui_only':
                    continue
                
                # Skip technique checkboxes (handled above)
                if param_type == 'technique':
                    continue
                
                # No need to skip anything special anymore
                
                if param_type == 'flag':
                    # Boolean flag - add if True
                    if param_value:
                        cmd.append(flag)
                        flags_added.add(flag)
                        
                elif param_type in ['quoted_arg', 'arg']:
                    # Value parameter - add if not empty
                    value_str = str(param_value).strip()
                    if value_str:
                        # Special handling for URLs and similar parameters - don't quote them
                        if param_name in ['url', 'direct', 'second_url', 'proxy']:
                            cmd.extend([flag, value_str])
                        else:
                            # Use shlex.quote for other arguments
                            quoted_value = shlex.quote(value_str)
                            cmd.extend([flag, quoted_value])
                        flags_added.add(flag)
                        
                elif param_type == 'special':
                    # Special parameters like technique flags
                    if param_value:
                        # Extract the flag (e.g., '--technique=B' becomes '--technique' and 'B')
                        flag_parts = flag.split('=')
                        if len(flag_parts) == 2:
                            cmd.extend([flag_parts[0], flag_parts[1]])
                            flags_added.add(flag_parts[0])
                        else:
                            cmd.append(flag)
                            flags_added.add(flag)
        
        return cmd
    
    def get_supported_parameters(self) -> List[str]:
        """Get list of all supported parameters"""
        return list(self.all_params.keys())
    
    def get_parameter_info(self, param_name: str) -> Optional[Dict]:
        """Get information about a specific parameter"""
        return self.all_params.get(param_name)
    
    def _get_flag_for_parameter(self, param_name: str) -> Optional[str]:
        """Get the SQLmap flag for a parameter name"""
        if param_name in self.all_params and 'flag' in self.all_params[param_name]:
            return self.all_params[param_name]['flag']
        return None
    
    def validate_options(self, options: Dict[str, Any]) -> CommandValidation:
        """Comprehensive options validation"""
        errors = []
        warnings = []
        
        # Check for required target parameter
        target_found = False
        target_params_found = []
        
        for target_param in self.target_params.keys():
            if options.get(target_param):
                target_found = True
                target_params_found.append(target_param)
        
        if not target_found:
            errors.append(ValidationIssue(
                ValidationLevel.ERROR,
                "target", 
                "No target specified. Must provide at least one of: --url, -d, -l, -m, -r, -g",
                "Add a target URL or other target specification"
            ))
        
        # Check for multiple target specifications
        if len(target_params_found) > 1:
            errors.append(ValidationIssue(
                ValidationLevel.ERROR,
                "target",
                f"Multiple target specifications found: {', '.join(target_params_found)}",
                "Use only one target specification method"
            ))
        
        # Check mutual exclusions
        self._check_mutual_exclusions(options, errors)
        
        # Validate individual parameters
        self._validate_individual_params(options, errors, warnings)
        
        # Check high-risk parameters
        self._check_high_risk_params(options, warnings)
        
        # Check file paths
        self._validate_file_paths(options, errors, warnings)
        
        # Generate info suggestions
        infos = []
        self._generate_suggestions(options, infos)
        
        is_valid = len(errors) == 0
        
        # Build command for suggested_command
        try:
            command_list = self.build_command(options) if is_valid else [self.sqlmap_path, '--help']
            suggested_command = ' '.join(command_list)
        except Exception:
            command_list = [self.sqlmap_path, '--help']
            suggested_command = ' '.join(command_list)
        
        return CommandValidation(is_valid, errors, warnings, command_list, infos, suggested_command)
    
    def _check_mutual_exclusions(self, options: Dict[str, Any], errors: List[ValidationIssue]):
        """Check for mutually exclusive options"""
        for group_name, param_list in self.mutual_exclusions.items():
            found_params = [param for param in param_list if options.get(param)]
            if len(found_params) > 1:
                flag_list = [self._get_flag_for_parameter(p) or p for p in found_params]
                errors.append(ValidationIssue(
                    ValidationLevel.ERROR,
                    group_name,
                    f"Mutually exclusive flags found: {', '.join(found_params)}",
                    f"Use only one of: {', '.join(param_list)}",
                    flag=', '.join(filter(None, flag_list))
                ))
    
    def _validate_individual_params(self, options: Dict[str, Any], errors: List[ValidationIssue], warnings: List[ValidationIssue]):
        """Validate individual parameter values"""
        
        # Validate threads
        if 'threads' in options and options['threads'] is not None and str(options['threads']).strip():
            try:
                threads = int(options['threads'])
                if threads < 1 or threads > 10:
                    errors.append(ValidationIssue(
                        ValidationLevel.ERROR,
                        'threads',
                        f"Invalid thread count: {threads}. Must be between 1-10",
                        "Use a reasonable thread count (1-10)",
                        flag=self._get_flag_for_parameter('threads')
                    ))
            except ValueError:
                errors.append(ValidationIssue(
                    ValidationLevel.ERROR,
                    'threads',
                    f"Invalid thread value: {options['threads']}. Must be an integer",
                    "Provide a valid integer for thread count",
                    flag=self._get_flag_for_parameter('threads')
                ))
        
        # Validate delay
        if 'delay' in options and options['delay'] is not None and str(options['delay']).strip():
            try:
                delay = float(options['delay'])
                if delay < 0:
                    errors.append(ValidationIssue(
                        ValidationLevel.ERROR,
                        'delay',
                        f"Invalid delay: {delay}. Must be positive",
                        "Use a positive delay value"
                    ))
            except ValueError:
                errors.append(ValidationIssue(
                    ValidationLevel.ERROR,
                    'delay',
                    f"Invalid delay value: {options['delay']}. Must be a number",
                    "Provide a valid number for delay"
                ))
        
        # Validate level and risk
        for param in ['level', 'risk']:
            if param in options and options[param] is not None and str(options[param]).strip():
                try:
                    value = int(options[param])
                    if value < 1 or value > 5:
                        errors.append(ValidationIssue(
                            ValidationLevel.ERROR,
                            param,
                            f"Invalid {param}: {value}. Must be between 1-5",
                            f"Use a valid {param} value (1-5)"
                        ))
                except ValueError:
                    errors.append(ValidationIssue(
                        ValidationLevel.ERROR,
                        param,
                        f"Invalid {param} value: {options[param]}. Must be an integer",
                        f"Provide a valid integer for {param}"
                    ))
    
    def _check_high_risk_params(self, options: Dict[str, Any], warnings: List[ValidationIssue]):
        """Check for high-risk parameters and add warnings"""
        for param_name, param_def in self.high_risk_params.items():
            if options.get(param_name):
                warnings.append(ValidationIssue(
                    ValidationLevel.WARNING,
                    param_name,
                    f"{param_def['risk_level']} RISK: {param_def['warning']}",
                    "Ensure you have authorization before using this parameter",
                    param_def['risk_level']
                ))
    
    def _validate_file_paths(self, options: Dict[str, Any], errors: List[ValidationIssue], warnings: List[ValidationIssue]):
        """Validate file path parameters"""
        file_params = {
            'log_file': 'Log file',
            'bulk_file': 'Bulk file', 
            'request_file': 'Request file',
            'config_file': 'Config file',
            'load_cookies': 'Cookie file',
            'auth_file': 'Auth file',
            'proxy_file': 'Proxy file',
            'sql_file': 'SQL file',
            'shared_lib': 'Shared library',
            'file_read': 'File to read',
            'file_write': 'File to write'
        }
        
        for param_name, param_desc in file_params.items():
            if options.get(param_name):
                filepath = options[param_name]
                if not os.path.exists(filepath) and param_name in ['log_file', 'bulk_file', 'request_file', 'config_file']:
                    errors.append(ValidationIssue(
                        ValidationLevel.ERROR,
                        param_name,
                        f"{param_desc} not found: {filepath}",
                        "Provide a valid file path that exists"
                    ))
    
    # Validation helper methods
    def _validate_url(self, url: str) -> bool:
        """Validate URL format"""
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url_pattern.match(url) is not None
    
    def _validate_connection_string(self, conn_str: str) -> bool:
        """Validate database connection string"""
        # Basic format: dbms://user:pass@host:port/db
        conn_pattern = re.compile(r'^[a-zA-Z]+://[^:]+:[^@]+@[^:]+:\d+/\w+$')
        return conn_pattern.match(conn_str) is not None
    
    def _validate_file_exists(self, filepath: str) -> bool:
        """Validate file exists"""
        return os.path.exists(filepath)
    
    def _validate_google_dork(self, dork: str) -> bool:
        """Validate Google dork format"""
        return len(dork.strip()) > 0
    
    def _validate_http_method(self, method: str) -> bool:
        """Validate HTTP method"""
        return method.upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']
    
    def _validate_post_data(self, data: str) -> bool:
        """Validate POST data format"""
        return len(data.strip()) > 0
    
    def _validate_delimiter(self, delimiter: str) -> bool:
        """Validate parameter delimiter"""
        return len(delimiter) == 1
    
    def _validate_cookie_string(self, cookie: str) -> bool:
        """Validate cookie string format"""
        return '=' in cookie
    
    def _validate_user_agent(self, ua: str) -> bool:
        """Validate user agent string"""
        return len(ua.strip()) > 0
    
    def _validate_headers(self, headers: str) -> bool:
        """Validate header string format"""
        return ':' in headers
    
    def _validate_threads(self, threads: Any) -> bool:
        """Validate thread count"""
        try:
            t = int(threads)
            return 1 <= t <= 10
        except:
            return False
    
    def _validate_delay(self, delay: Any) -> bool:
        """Validate delay value"""
        try:
            d = float(delay)
            return d >= 0
        except:
            return False
    
    def _validate_timeout(self, timeout: Any) -> bool:
        """Validate timeout value"""
        try:
            t = int(timeout)
            return 1 <= t <= 3600
        except:
            return False
    
    def _validate_retries(self, retries: Any) -> bool:
        """Validate retry count"""
        try:
            r = int(retries)
            return 0 <= r <= 10
        except:
            return False
    
    def _validate_proxy_url(self, proxy: str) -> bool:
        """Validate proxy URL format"""
        proxy_pattern = re.compile(r'^https?://[^:]+:\d+$')
        return proxy_pattern.match(proxy) is not None
    
    def _validate_crawl(self, crawl: Any) -> bool:
        """Validate crawl depth"""
        try:
            c = int(crawl)
            return 1 <= c <= 10
        except:
            return False
    
    def _generate_suggestions(self, options: Dict[str, Any], infos: List[ValidationIssue]):
        """Generate helpful suggestions for optimization"""
        
        # Suggest batch mode if not set
        if not options.get('batch'):
            infos.append(ValidationIssue(
                ValidationLevel.INFO,
                "batch",
                "Consider using --batch mode to avoid interactive prompts",
                "Add --batch flag for automated execution",
                flag="--batch"
            ))
        
        # Suggest reasonable thread count if not set
        if not options.get('threads'):
            infos.append(ValidationIssue(
                ValidationLevel.INFO,
                "threads",
                "Consider setting thread count for better performance",
                "Add --threads=3 for moderate performance",
                flag="--threads"
            ))
        
        # Suggest delay for high thread counts
        if options.get('threads') and int(str(options['threads'])) > 5:
            if not options.get('delay'):
                infos.append(ValidationIssue(
                    ValidationLevel.INFO,
                    "delay",
                    "High thread count detected - consider adding delay to avoid blocking",
                    "Add --delay=1 to be more respectful to target server"
                ))
        
        # Suggest verbosity level
        if not options.get('verbose'):
            infos.append(ValidationIssue(
                ValidationLevel.INFO,
                "verbose",
                "Consider setting verbosity level for better output",
                "Add --verbose=1 for detailed output"
            ))

    def create_process(self, options: Dict[str, Any], use_sudo: bool = False, sudo_password: str = None) -> Optional[SqlmapProcess]:
        """Create a new SqlmapProcess with given options"""
        try:
            command = self.build_command(options)
            
            # Add sudo if required
            if use_sudo:
                if not self._check_sudo_available():
                    print("Warning: sudo not available on this system")
                    return None
                
                command = ['sudo', '-S'] + command
                print(f"Using sudo command: {' '.join(command)}")
            
            # Create process
            process = SqlmapProcess(command, sudo_password if use_sudo else None)
            
            return process
            
        except Exception as e:
            print(f"Error creating SqlmapProcess: {e}")
            return None
    
    def _check_sudo_available(self) -> bool:
        """Check if sudo is available on the system"""
        try:
            result = subprocess.run(['which', 'sudo'], capture_output=True, text=True)
            return result.returncode == 0
        except Exception:
            return False

def main():
    """Test the new wrapper"""
    print("🚀 Testing New SQLmap Wrapper V2")
    print("=" * 50)
    
    wrapper = SqlmapWrapper()
    
    # Test with problematic options from user
    test_options = {
        'url': 'http://testphp.vulnweb.com/artists.php?artist=1',
        'threads': 6,
        'delay': 34.0,
        'timeout': 665,
        'retries': 7,
        'level': 5,
        'risk': 2,
        'batch': True
    }
    
    print("Testing with clean options:")
    validation = wrapper.validate_options(test_options)
    
    print(f"Valid: {validation.is_valid}")
    print(f"Errors: {len(validation.errors)}")
    print(f"Warnings: {len(validation.warnings)}")
    
    if validation.errors:
        print("\nErrors:")
        for error in validation.errors:
            print(f"  - {error.parameter}: {error.message}")
    
    if validation.warnings:
        print("\nWarnings:")
        for warning in validation.warnings:
            print(f"  - {warning.parameter}: {warning.message}")
    
    if validation.is_valid:
        command = wrapper.build_command(test_options)
        print(f"\nGenerated command:")
        print(' '.join(command))

if __name__ == "__main__":
    main()
