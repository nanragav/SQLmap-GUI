"""
SQLmap GUI Configuration Manager
Handles all configuration settings and validations
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from configparser import ConfigParser

class ConfigManager:
    def __init__(self):
        self.config_dir = Path.home() / '.sqlmap-gui'
        self.config_file = self.config_dir / 'config.json'
        self.profiles_dir = self.config_dir / 'profiles'
        
        # Create directories if they don't exist
        self.config_dir.mkdir(exist_ok=True)
        self.profiles_dir.mkdir(exist_ok=True)
        
        # Default configuration
        self.default_config = {
            'ui': {
                'theme': 'dark',
                'language': 'en',
                'remember_window_size': True,
                'window_width': 1200,
                'window_height': 800,
                'show_tooltips': True,
                'auto_save_profiles': True
            },
            'sqlmap': {
                'path': 'sqlmap',
                'default_threads': 1,
                'default_timeout': 30,
                'default_retries': 3,
                'output_dir': str(Path.home() / 'sqlmap-gui-output')
            },
            'advanced': {
                'max_log_lines': 10000,
                'auto_scroll_logs': True,
                'save_traffic_logs': True,
                'confirm_dangerous_ops': True
            }
        }
        
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or return defaults"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                # Merge with defaults to ensure all keys exist
                return self._merge_configs(self.default_config, config)
            else:
                return self.default_config.copy()
        except Exception as e:
            print(f"Error loading config: {e}")
            return self.default_config.copy()
    
    def save_config(self) -> bool:
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def _merge_configs(self, default: Dict, user: Dict) -> Dict:
        """Recursively merge user config with defaults"""
        result = default.copy()
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        return result
    
    def get(self, key_path: str, default=None):
        """Get configuration value using dot notation (e.g., 'ui.theme')"""
        keys = key_path.split('.')
        value = self.config
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value: Any):
        """Set configuration value using dot notation"""
        keys = key_path.split('.')
        config = self.config
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        config[keys[-1]] = value
    
    def save_profile(self, name: str, options: Dict[str, Any]) -> bool:
        """Save a configuration profile"""
        try:
            profile_file = self.profiles_dir / f"{name}.json"
            with open(profile_file, 'w') as f:
                json.dump(options, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving profile: {e}")
            return False
    
    def load_profile(self, name: str) -> Optional[Dict[str, Any]]:
        """Load a configuration profile"""
        try:
            profile_file = self.profiles_dir / f"{name}.json"
            if profile_file.exists():
                with open(profile_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading profile: {e}")
        return None
    
    def list_profiles(self) -> List[str]:
        """List all available profiles"""
        try:
            return [f.stem for f in self.profiles_dir.glob('*.json')]
        except Exception:
            return []
    
    def delete_profile(self, name: str) -> bool:
        """Delete a profile"""
        try:
            profile_file = self.profiles_dir / f"{name}.json"
            if profile_file.exists():
                profile_file.unlink()
                return True
        except Exception as e:
            print(f"Error deleting profile: {e}")
        return False
    
    def validate_options(self, options: Dict[str, Any]) -> Dict[str, Any]:
        """Validate SQLmap options for conflicts and dependencies"""
        errors = []
        warnings = []
        
        # Check for required target
        target_options = ['url', 'direct', 'log_file', 'bulk_file', 'request_file', 'google_dork']
        if not any(options.get(opt) for opt in target_options):
            errors.append("At least one target must be specified (URL, direct connection, log file, etc.)")
        
        # Check for conflicting options using SqlmapOptions
        sqlmap_opts = SqlmapOptions()
        for option, conflicts in sqlmap_opts.CONFLICTS.items():
            if options.get(option):
                for conflict in conflicts:
                    if options.get(conflict):
                        errors.append(f"Options '{option}' and '{conflict}' cannot be used together")
        
        # Check dependencies
        for option, deps in sqlmap_opts.DEPENDENCIES.items():
            if options.get(option):
                for dep in deps:
                    if not options.get(dep):
                        warnings.append(f"Option '{option}' works best with '{dep}' option")
        
        # Validate specific option values
        if options.get('level'):
            level = options.get('level')
            if not isinstance(level, int) or level < 1 or level > 5:
                errors.append("Level must be between 1 and 5")
        
        if options.get('risk'):
            risk = options.get('risk')
            if not isinstance(risk, int) or risk < 1 or risk > 3:
                errors.append("Risk must be between 1 and 3")
        
        if options.get('threads'):
            threads = options.get('threads')
            if not isinstance(threads, int) or threads < 1 or threads > 10:
                errors.append("Threads must be between 1 and 10")
        
        # URL validation
        url = options.get('url')
        if url and not (url.startswith('http://') or url.startswith('https://')):
            errors.append("URL must start with http:// or https://")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'options': options
        }


class SqlmapOptions:
    """
    Manages SQLmap options and their relationships/dependencies
    """
    
    # Define option categories
    CATEGORIES = {
        'target': ['url', 'direct', 'logfile', 'bulkfile', 'requestfile', 'googledork', 'configfile'],
        'request': ['user_agent', 'header', 'method', 'data', 'param_del', 'cookie', 'cookie_del',
                   'live_cookies', 'load_cookies', 'drop_set_cookie', 'http1_0', 'http2',
                   'mobile', 'random_agent', 'host', 'referer', 'headers', 'auth_type',
                   'auth_cred', 'auth_file', 'abort_code', 'ignore_code', 'ignore_proxy',
                   'ignore_redirects', 'ignore_timeouts', 'proxy', 'proxy_cred', 'proxy_file',
                   'proxy_freq', 'tor', 'tor_port', 'tor_type', 'check_tor', 'delay',
                   'timeout', 'retries', 'retry_on', 'randomize', 'safe_url', 'safe_post',
                   'safe_req', 'safe_freq', 'skip_urlencode', 'csrf_token', 'csrf_url',
                   'csrf_method', 'csrf_data', 'csrf_retries', 'force_ssl', 'chunked',
                   'hpp', 'eval'],
        'optimization': ['optimize', 'predict_output', 'keep_alive', 'null_connection', 'threads'],
        'injection': ['testparameter', 'skip', 'skip_static', 'param_exclude', 'param_filter',
                     'dbms', 'dbms_cred', 'os', 'invalid_bignum', 'invalid_logical',
                     'invalid_string', 'no_cast', 'no_escape', 'prefix', 'suffix', 'tamper'],
        'detection': ['level', 'risk', 'string', 'not_string', 'regexp', 'code', 'smart',
                     'text_only', 'titles'],
        'techniques': ['technique', 'time_sec', 'disable_stats', 'union_cols', 'union_char',
                      'union_from', 'union_values', 'dns_domain', 'second_url', 'second_req'],
        'fingerprint': ['fingerprint'],
        'enumeration': ['all', 'banner', 'current_user', 'current_db', 'hostname', 'is_dba',
                       'users', 'passwords', 'privileges', 'roles', 'dbs', 'tables', 'columns',
                       'schema', 'count', 'dump', 'dump_all', 'search', 'comments', 'statements',
                       'database', 'table', 'column', 'exclude', 'user', 'exclude_sysdbs',
                       'pivot_column', 'where', 'start', 'stop', 'first', 'last', 'sql_query',
                       'sql_shell', 'sql_file', 'abort_on_empty'],
        'brute_force': ['common_tables', 'common_columns', 'common_files'],
        'udf': ['udf_inject', 'shared_lib'],
        'file_system': ['file_read', 'file_write', 'file_dest'],
        'os_access': ['os_cmd', 'os_shell', 'os_pwn', 'os_smbrelay', 'os_bof', 'priv_esc',
                     'msf_path', 'tmp_path'],
        'registry': ['reg_read', 'reg_add', 'reg_del', 'reg_key', 'reg_value', 'reg_data',
                    'reg_type'],
        'general': ['sessionfile', 'trafficfile', 'answers', 'base64', 'base64_safe', 'batch',
                   'binary_fields', 'check_internet', 'charset', 'cleanup', 'crawl',
                   'crawl_exclude', 'csv_del', 'dump_file', 'dump_format', 'encoding', 'eta',
                   'flush_session', 'forms', 'fresh_queries', 'gpage', 'har', 'hex',
                   'output_dir', 'parse_errors', 'preprocess', 'postprocess', 'repair',
                   'save', 'scope', 'skip_heuristics', 'skip_waf', 'table_prefix',
                   'test_filter', 'test_skip', 'time_limit', 'unsafe_naming', 'web_root'],
        'miscellaneous': ['mnemonics', 'alert', 'beep', 'dependencies', 'disable_coloring',
                         'disable_hashing', 'list_tampers', 'no_logging', 'no_truncate',
                         'offline', 'purge', 'results_file', 'shell', 'tmp_dir', 'unstable',
                         'update', 'wizard']
    }
    
    # Define conflicting options
    CONFLICTS = {
        'url': ['direct', 'logfile', 'bulkfile', 'requestfile', 'googledork'],
        'direct': ['url', 'logfile', 'bulkfile', 'requestfile', 'googledork'],
        'logfile': ['url', 'direct', 'bulkfile', 'requestfile', 'googledork'],
        'bulkfile': ['url', 'direct', 'logfile', 'requestfile', 'googledork'],
        'requestfile': ['url', 'direct', 'logfile', 'bulkfile', 'googledork'],
        'googledork': ['url', 'direct', 'logfile', 'bulkfile', 'requestfile'],
        'tor': ['proxy'],
        'proxy': ['tor'],
        'batch': ['wizard'],
        'wizard': ['batch'],
        'offline': ['crawl', 'forms', 'check_internet']
    }
    
    # Define dependencies (option requires other options)
    DEPENDENCIES = {
        'csrf_token': ['forms'],
        'csrf_url': ['forms'],
        'proxy_cred': ['proxy'],
        'proxy_freq': ['proxy_file'],
        'tor_port': ['tor'],
        'tor_type': ['tor'],
        'check_tor': ['tor'],
        'safe_post': ['safe_url'],
        'safe_req': ['safe_url'],
        'safe_freq': ['safe_url'],
        'database': ['dbs', 'tables', 'columns', 'dump', 'count', 'schema'],
        'table': ['tables', 'columns', 'dump', 'count'],
        'column': ['columns', 'dump'],
        'where': ['dump'],
        'start': ['dump'],
        'stop': ['dump'],
        'first': ['dump'],
        'last': ['dump'],
        'reg_value': ['reg_key'],
        'reg_data': ['reg_add'],
        'reg_type': ['reg_add'],
        'shared_lib': ['udf_inject'],
        'file_dest': ['file_write'],
        'msf_path': ['os_pwn', 'os_smbrelay']
    }
    
    @classmethod
    def get_category(cls, option: str) -> Optional[str]:
        """Get the category of an option"""
        for category, options in cls.CATEGORIES.items():
            if option in options:
                return category
        return None
    
    @classmethod
    def get_conflicts(cls, option: str) -> List[str]:
        """Get list of conflicting options"""
        return cls.CONFLICTS.get(option, [])
    
    @classmethod
    def get_dependencies(cls, option: str) -> List[str]:
        """Get list of required options"""
        return cls.DEPENDENCIES.get(option, [])
    
    @classmethod
    def validate_options(cls, options: Dict[str, Any]) -> List[str]:
        """Validate option combinations and return list of errors"""
        errors = []
        
        # Check for conflicting options
        for option, value in options.items():
            if value:  # Only check enabled options
                conflicts = cls.get_conflicts(option)
                for conflict in conflicts:
                    if options.get(conflict):
                        errors.append(f"Option '{option}' conflicts with '{conflict}'")
        
        # Check dependencies
        for option, value in options.items():
            if value:  # Only check enabled options
                dependencies = cls.get_dependencies(option)
                for dep in dependencies:
                    if not options.get(dep):
                        errors.append(f"Option '{option}' requires '{dep}' to be enabled")
        
        # Check target requirements
        target_options = ['url', 'direct', 'logfile', 'bulkfile', 'requestfile', 'googledork']
        if not any(options.get(opt) for opt in target_options):
            errors.append("At least one target option must be specified")
        
        return errors
