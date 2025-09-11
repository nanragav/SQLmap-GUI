"""
Target Tab - Contains all target specification options
Handles URL, request file, direct connection, and related options
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                            QCheckBox, QComboBox, QSpinBox, QTextEdit, QGroupBox,
                            QScrollArea, QPushButton, QFileDialog, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import Dict, Any

from ..widgets.custom_widgets import OptionGroup, ValidatedLineEdit
from .base_tab import BaseTab


class TargetTab(BaseTab):
    """Tab for target specification options"""
    
    options_changed = pyqtSignal()
    
    def __init__(self, parent=None, mutual_exclusion_manager=None):
        super().__init__(parent)
        self.mutual_exclusion_manager = mutual_exclusion_manager
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the target tab UI"""
        # Create scroll area for the tab content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        
        layout = QVBoxLayout()
        
        # Target specification group
        target_group = self.create_target_group()
        layout.addWidget(target_group)
        
        # Request options group
        request_group = self.create_request_group()
        layout.addWidget(request_group)
        
        # Connection options group
        connection_group = self.create_connection_group()
        layout.addWidget(connection_group)
        
        layout.addStretch()
        scroll_content.setLayout(layout)
        scroll_area.setWidget(scroll_content)
        
        # Main tab layout
        tab_layout = QVBoxLayout()
        tab_layout.addWidget(scroll_area)
        self.setLayout(tab_layout)
    
    def create_target_group(self) -> QGroupBox:
        """Create target specification options"""
        target_options = [
            {
                'name': 'url',
                'type': 'text',
                'label': 'Target URL',
                'validator': 'url',
                'placeholder': 'http://example.com/page.php?id=1'
            },
            {
                'name': 'direct',
                'type': 'text',
                'label': 'Direct Database Connection',
                'placeholder': 'DBMS://USER:PASSWORD@DBMSIP:DBMSPORT/DBMSDB'
            },
            {
                'name': 'log_file',
                'type': 'file',
                'label': 'Parse Targets from Burp/WebScarab Log',
                'filter': 'Log Files (*.log);;All Files (*)'
            },
            {
                'name': 'bulk_file',
                'type': 'file',
                'label': 'Scan Multiple Targets from File',
                'filter': 'Text Files (*.txt);;All Files (*)'
            },
            {
                'name': 'request_file',
                'type': 'file',
                'label': 'Load HTTP Request from File',
                'filter': 'Text Files (*.txt);;All Files (*)'
            }
        ]
        
        return OptionGroup("Target Specification", target_options, self.mutual_exclusion_manager)
    
    def create_request_group(self) -> QGroupBox:
        """Create request options"""
        request_options = [
            {
                'name': 'method',
                'type': 'combo',
                'label': 'HTTP Method',
                'items': [
                    {'label': 'GET (default)', 'value': 'GET'},
                    {'label': 'POST', 'value': 'POST'},
                    {'label': 'PUT', 'value': 'PUT'},
                    {'label': 'DELETE', 'value': 'DELETE'},
                    {'label': 'PATCH', 'value': 'PATCH'},
                    {'label': 'HEAD', 'value': 'HEAD'},
                    {'label': 'OPTIONS', 'value': 'OPTIONS'}
                ]
            },
            {
                'name': 'data',
                'type': 'text',
                'label': 'Data String (POST)',
                'placeholder': 'id=1&user=admin'
            },
            {
                'name': 'cookie',
                'type': 'text',
                'label': 'HTTP Cookie Header',
                'placeholder': 'PHPSESSID=abc123; security=low'
            },
            {
                'name': 'load_cookies',
                'type': 'file',
                'label': 'Load Cookies from File',
                'filter': 'Text Files (*.txt);;All Files (*)'
            },
            {
                'name': 'random_agent',
                'type': 'checkbox',
                'label': 'Use Random HTTP User-Agent'
            },
            {
                'name': 'user_agent',
                'type': 'text',
                'label': 'HTTP User-Agent Header',
                'placeholder': 'Mozilla/5.0 ...'
            },
            {
                'name': 'host',
                'type': 'text',
                'label': 'HTTP Host Header',
                'placeholder': 'example.com'
            },
            {
                'name': 'referer',
                'type': 'text',
                'label': 'HTTP Referer Header',
                'validator': 'url',
                'placeholder': 'http://example.com/referer.php'
            }
        ]
        
        return OptionGroup("Request Options", request_options, self.mutual_exclusion_manager)
    
    def create_connection_group(self) -> QGroupBox:
        """Create connection options"""
        connection_options = [
            {
                'name': 'headers',
                'type': 'text',
                'label': 'Extra HTTP Headers',
                'placeholder': 'X-Custom-Header: value\\nAuthorization: Bearer token'
            },
            {
                'name': 'auth_type',
                'type': 'combo',
                'label': 'HTTP Authentication Type',
                'items': [
                    {'label': 'None', 'value': ''},
                    {'label': 'Basic', 'value': 'Basic'},
                    {'label': 'Digest', 'value': 'Digest'},
                    {'label': 'NTLM', 'value': 'NTLM'},
                    {'label': 'PKI', 'value': 'PKI'}
                ]
            },
            {
                'name': 'auth_cred',
                'type': 'text',
                'label': 'HTTP Authentication Credentials',
                'placeholder': 'username:password'
            },
            {
                'name': 'proxy',
                'type': 'text',
                'label': 'HTTP Proxy',
                'placeholder': 'http://127.0.0.1:8080'
            }
            # Removed tor option (moved to Request tab)
        ]
        
        return OptionGroup("Connection Options", connection_options, self.mutual_exclusion_manager)
    
    # Methods inherited from BaseTab: get_options, set_options, reset_options
    
    def validate_options(self) -> Dict[str, Any]:
        """Validate current options"""
        options = self.get_options()
        errors = []
        
        # Check if at least one target is specified
        target_specified = any([
            options.get('url'),
            options.get('direct'),
            options.get('log_file'),
            options.get('bulk_file'),
            options.get('request_file'),
            options.get('google_dork')
        ])
        
        if not target_specified:
            errors.append("At least one target must be specified (URL, direct connection, log file, etc.)")
        
        # Validate URL if provided
        url = options.get('url')
        if url and not (url.startswith('http://') or url.startswith('https://')):
            errors.append("URL must start with http:// or https://")
        
        # Validate proxy format if provided
        proxy = options.get('proxy')
        if proxy and not (proxy.startswith('http://') or proxy.startswith('https://') or proxy.startswith('socks')):
            errors.append("Proxy must be in format http://host:port or socks://host:port")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'options': options
        }
