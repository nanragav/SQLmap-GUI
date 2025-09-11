"""
Request Tab - HTTP request customization options
Handles methods, headers, timing, and request optimization
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                            QCheckBox, QComboBox, QSpinBox, QTextEdit, QGroupBox,
                            QScrollArea, QPushButton, QFileDialog, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import Dict, Any

from ..widgets.custom_widgets import OptionGroup, ValidatedLineEdit


class RequestTab(QWidget):
    """Tab for HTTP request customization options"""
    
    options_changed = pyqtSignal()
    
    def __init__(self, parent=None, mutual_exclusion_manager=None):
        super().__init__(parent)
        self.mutual_exclusion_manager = mutual_exclusion_manager
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the request tab UI"""
        # Create scroll area for the tab content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        
        layout = QVBoxLayout()
        
        # HTTP optimization group
        optimization_group = self.create_optimization_group()
        layout.addWidget(optimization_group)
        
        # Timing options group
        timing_group = self.create_timing_group()
        layout.addWidget(timing_group)
        
        # HTTP options group
        http_group = self.create_http_group()
        layout.addWidget(http_group)
        
        # SSL/TLS options group
        ssl_group = self.create_ssl_group()
        layout.addWidget(ssl_group)
        
        # Tor options group
        tor_group = self.create_tor_group()
        layout.addWidget(tor_group)
        
        layout.addStretch()
        scroll_content.setLayout(layout)
        scroll_area.setWidget(scroll_content)
        
        # Main tab layout
        tab_layout = QVBoxLayout()
        tab_layout.addWidget(scroll_area)
        self.setLayout(tab_layout)
        
        # Connect tor checkbox signal
        self.connect_tor_signals()
    
    def create_optimization_group(self) -> QGroupBox:
        """Create HTTP optimization options"""
        optimization_options = [
            {
                'name': 'optimize',
                'type': 'checkbox',
                'label': 'Turn on All Optimization Switches'
            },
            {
                'name': 'keep_alive',
                'type': 'checkbox',
                'label': 'Use Persistent HTTP(s) Connections'
            },
            {
                'name': 'null_connection',
                'type': 'checkbox',
                'label': 'Retrieve Page Length Without HTTP Response Body'
            },
            {
                'name': 'threads',
                'type': 'number',
                'label': 'Max Number of Concurrent HTTP(s) Requests',
                'min': 1,
                'max': 10,
                'default': 1
            },
            {
                'name': 'batch',
                'type': 'checkbox',
                'label': 'Never Ask for User Input (Use Default Behavior)'
            },
            {
                'name': 'tor',
                'type': 'checkbox',
                'label': 'Use Tor Anonymizer'
            }
        ]
        
        group = OptionGroup("Optimization", optimization_options, self.mutual_exclusion_manager)
        # Store reference to the group for tor checkbox access
        self.optimization_group = group
        return group
    
    def create_timing_group(self) -> QGroupBox:
        """Create timing and delay options"""
        timing_options = [
            {
                'name': 'delay',
                'type': 'number',
                'label': 'Delay Between HTTP Requests (seconds)',
                'min': 0,
                'max': 3600,
                'default': 0,
                'decimal': True,
                'decimals': 1
            },
            {
                'name': 'timeout',
                'type': 'number',
                'label': 'Seconds to Wait Before Timeout',
                'min': 1,
                'max': 3600,
                'default': 30
            },
            {
                'name': 'retries',
                'type': 'number',
                'label': 'Retries When Connection Timeouts',
                'min': 0,
                'max': 10,
                'default': 3
            }
        ]
        
        return OptionGroup("Request Timing", timing_options, self.mutual_exclusion_manager)
    
    def create_http_group(self) -> QGroupBox:
        """Create HTTP-specific options"""
        http_options = [
            {
                'name': 'charset',
                'type': 'combo',
                'label': 'Blind SQL Injection Charset',
                'items': [
                    {'label': 'Default', 'value': ''},
                    {'label': 'Numeric (0123456789)', 'value': '0123456789'},
                    {'label': 'Alphanumeric', 'value': 'abcdefghijklmnopqrstuvwxyz0123456789'},
                    {'label': 'Alphabetic', 'value': 'abcdefghijklmnopqrstuvwxyz'},
                    {'label': 'Uppercase', 'value': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'},
                    {'label': 'Hexadecimal', 'value': '0123456789abcdef'},
                    {'label': 'Binary', 'value': '01'}
                ]
            },
            {
                'name': 'encoding',
                'type': 'combo',
                'label': 'Character Encoding',
                'items': [
                    {'label': 'Default', 'value': ''},
                    {'label': 'UTF-8', 'value': 'utf-8'},
                    {'label': 'ISO-8859-1', 'value': 'iso-8859-1'},
                    {'label': 'Windows-1252', 'value': 'windows-1252'},
                    {'label': 'ASCII', 'value': 'ascii'}
                ]
            },
            {
                'name': 'base64',
                'type': 'text',
                'label': 'Parameter(s) Containing Base64 Encoded Data',
                'placeholder': 'param1,param2'
            },
            {
                'name': 'base64_safe',
                'type': 'checkbox',
                'label': 'Use URL and Filename Safe Base64 Alphabet (RFC 4648)'
            }
        ]
        
        return OptionGroup("HTTP Options", http_options, self.mutual_exclusion_manager)
    
    def create_ssl_group(self) -> QGroupBox:
        """Create SSL/TLS options"""
        ssl_options = [
            {
                'name': 'force_ssl',
                'type': 'checkbox',
                'label': 'Force Usage of SSL/HTTPS'
            },
            {
                'name': 'cors',
                'type': 'checkbox',
                'label': 'Add CORS Headers to Requests'
            }
        ]
        
        return OptionGroup("Advanced Request Options", ssl_options, self.mutual_exclusion_manager)
    
    def create_tor_group(self) -> QGroupBox:
        """Create Tor options"""
        tor_options = [
            {
                'name': 'tor_port',
                'type': 'number',
                'label': 'Tor Proxy Port',
                'min': 1,
                'max': 65535,
                'default': 9050
            },
            {
                'name': 'tor_type',
                'type': 'combo',
                'label': 'Tor Proxy Type',
                'items': [
                    {'label': 'SOCKS4', 'value': 'SOCKS4'},
                    {'label': 'SOCKS5', 'value': 'SOCKS5'},
                    {'label': 'HTTP', 'value': 'HTTP'}
                ]
            }
        ]
        
        group = OptionGroup("Tor Options", tor_options, self.mutual_exclusion_manager)
        # Store reference to the group for conditional visibility
        self.tor_group = group
        return group
    
    def get_options(self) -> Dict[str, Any]:
        """Get all options from this tab"""
        options = {}
        
        # Collect from all option groups
        for i in range(self.layout().itemAt(0).widget().widget().layout().count()):
            item = self.layout().itemAt(0).widget().widget().layout().itemAt(i)
            if item and item.widget() and isinstance(item.widget(), OptionGroup):
                group_options = item.widget().get_values()
                options.update(group_options)
        
        # Only include tor_port and tor_type if tor is enabled
        if not options.get('tor', False):
            options.pop('tor_port', None)
            options.pop('tor_type', None)
        
        # Filter out empty values
        return {k: v for k, v in options.items() if v is not None and v != ''}
    
    def set_options(self, options: Dict[str, Any]):
        """Set options in this tab"""
        for i in range(self.layout().itemAt(0).widget().widget().layout().count()):
            item = self.layout().itemAt(0).widget().widget().layout().itemAt(i)
            if item and item.widget() and isinstance(item.widget(), OptionGroup):
                item.widget().set_values(options)
    
    def reset_options(self):
        """Reset all options to defaults"""
        for i in range(self.layout().itemAt(0).widget().widget().layout().count()):
            item = self.layout().itemAt(0).widget().widget().layout().itemAt(i)
            if item and item.widget() and isinstance(item.widget(), OptionGroup):
                item.widget().set_values({})
    
    def connect_tor_signals(self):
        """Connect tor checkbox signal to show/hide tor options"""
        # Find the tor checkbox in the optimization group
        if hasattr(self, 'optimization_group') and hasattr(self.optimization_group, 'widgets'):
            tor_checkbox = self.optimization_group.widgets.get('tor')
            if tor_checkbox and isinstance(tor_checkbox, QCheckBox):
                tor_checkbox.toggled.connect(self.on_tor_toggled)
                # Set initial state
                self.on_tor_toggled(tor_checkbox.isChecked())
    
    def on_tor_toggled(self, checked):
        """Handle tor checkbox state change"""
        if hasattr(self, 'tor_group'):
            self.tor_group.setVisible(checked)
