"""
Configuration Manager for SQLmap GUI
Handles configuration, profiles, and validation
"""

import json
import os
from typing import Dict, Any, List
from pathlib import Path


class ConfigManager:
    """Configuration manager for SQLmap GUI"""
    
    def __init__(self):
        self.config_dir = Path.home() / '.sqlmap-gui'
        self.profiles_file = self.config_dir / 'profiles.json'
        self.config_file = self.config_dir / 'config.json'
        
        # Create config directory if it doesn't exist
        self.config_dir.mkdir(exist_ok=True)
        
        # Load existing profiles
        self.profiles = self.load_profiles()
    
    def save_profile(self, name: str, options: Dict[str, Any]) -> bool:
        """Save a profile with given options"""
        try:
            if name not in self.profiles:
                self.profiles[name] = {}
            
            self.profiles[name] = {
                'name': name,
                'options': options,
                'created_at': self._get_timestamp()
            }
            
            # Save to file
            with open(self.profiles_file, 'w') as f:
                json.dump(self.profiles, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Error saving profile: {e}")
            return False
    
    def load_profile(self, name: str) -> Dict[str, Any]:
        """Load a profile by name"""
        return self.profiles.get(name, {}).get('options', {})
    
    def load_profiles(self) -> Dict[str, Any]:
        """Load all profiles from file"""
        try:
            if self.profiles_file.exists():
                with open(self.profiles_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Error loading profiles: {e}")
            return {}
    
    def get_profiles(self) -> Dict[str, Any]:
        """Get all available profiles"""
        return self.profiles
    
    def delete_profile(self, name: str) -> bool:
        """Delete a profile"""
        try:
            if name in self.profiles:
                del self.profiles[name]
                with open(self.profiles_file, 'w') as f:
                    json.dump(self.profiles, f, indent=2)
                return True
            return False
        except Exception as e:
            print(f"Error deleting profile: {e}")
            return False
    
    def validate_options(self, options: Dict[str, Any]) -> Dict[str, Any]:
        """Validate SQLmap options"""
        validation_result = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Check for required options
        target_options = ['url', 'direct', 'log_file', 'bulk_file', 'request_file', 'google_dork', 'config_file']
        has_target = any(options.get(opt) for opt in target_options)
        
        if not has_target:
            validation_result['errors'].append("At least one target option must be specified (URL, direct connection, etc.)")
            validation_result['valid'] = False
        
        # Validate URL format if provided
        if options.get('url'):
            url = options['url']
            if not (url.startswith('http://') or url.startswith('https://')):
                validation_result['warnings'].append("URL should start with http:// or https://")
        
        # Validate level and risk values
        if options.get('level'):
            try:
                level = int(options['level'])
                if not 1 <= level <= 5:
                    validation_result['errors'].append("Level must be between 1 and 5")
                    validation_result['valid'] = False
            except (ValueError, TypeError):
                validation_result['errors'].append("Level must be a valid integer")
                validation_result['valid'] = False
        
        if options.get('risk'):
            try:
                risk = int(options['risk'])
                if not 1 <= risk <= 3:
                    validation_result['errors'].append("Risk must be between 1 and 3")
                    validation_result['valid'] = False
            except (ValueError, TypeError):
                validation_result['errors'].append("Risk must be a valid integer")
                validation_result['valid'] = False
        
        # Validate threads
        if options.get('threads'):
            try:
                threads = int(options['threads'])
                if threads < 1 or threads > 100:
                    validation_result['warnings'].append("Threads should be between 1 and 100")
            except (ValueError, TypeError):
                validation_result['errors'].append("Threads must be a valid integer")
                validation_result['valid'] = False
        
        # Validate timeout
        if options.get('timeout'):
            try:
                timeout = int(options['timeout'])
                if timeout < 1:
                    validation_result['errors'].append("Timeout must be greater than 0")
                    validation_result['valid'] = False
            except (ValueError, TypeError):
                validation_result['errors'].append("Timeout must be a valid integer")
                validation_result['valid'] = False
        
        # Validate retries
        if options.get('retries'):
            try:
                retries = int(options['retries'])
                if retries < 0:
                    validation_result['errors'].append("Retries must be 0 or greater")
                    validation_result['valid'] = False
            except (ValueError, TypeError):
                validation_result['errors'].append("Retries must be a valid integer")
                validation_result['valid'] = False
        
        # Validate technique string
        if options.get('technique'):
            technique = str(options['technique']).upper()
            valid_techniques = set('BEUSTQ')
            invalid_chars = set(technique) - valid_techniques
            if invalid_chars:
                validation_result['errors'].append(f"Invalid technique characters: {', '.join(invalid_chars)}. Valid: B,E,U,S,T,Q")
                validation_result['valid'] = False
        
        # Validate file paths
        file_options = ['request_file', 'log_file', 'bulk_file', 'config_file', 'load_cookies', 'auth_file']
        for opt in file_options:
            if options.get(opt):
                file_path = Path(options[opt])
                if not file_path.exists():
                    validation_result['warnings'].append(f"File not found: {options[opt]}")
        
        # Validate proxy format
        if options.get('proxy'):
            proxy = options['proxy']
            if not ('://' in proxy and any(proxy.startswith(proto) for proto in ['http://', 'https://', 'socks4://', 'socks5://'])):
                validation_result['warnings'].append("Proxy format should be protocol://host:port")
        
        return validation_result
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """Save general configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def load_config(self) -> Dict[str, Any]:
        """Load general configuration"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Error loading config: {e}")
            return {}
