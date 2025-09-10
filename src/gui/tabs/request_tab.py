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
        
        layout.addStretch()
        scroll_content.setLayout(layout)
        scroll_area.setWidget(scroll_content)
        
        # Main tab layout
        tab_layout = QVBoxLayout()
        tab_layout.addWidget(scroll_area)
        self.setLayout(tab_layout)
    
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
            }
        ]
        
        return OptionGroup("Optimization", optimization_options, self.mutual_exclusion_manager)
    
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
            }
        ]
        
        return OptionGroup("Advanced Request Options", ssl_options, self.mutual_exclusion_manager)
    
    def get_options(self) -> Dict[str, Any]:
        """Get all options from this tab"""
        options = {}
        
        # Collect from all option groups
        for i in range(self.layout().itemAt(0).widget().widget().layout().count()):
            item = self.layout().itemAt(0).widget().widget().layout().itemAt(i)
            if item and item.widget() and isinstance(item.widget(), OptionGroup):
                group_options = item.widget().get_values()
                options.update(group_options)
        
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
    
    def validate_options(self) -> Dict[str, Any]:
        """Validate current options"""
        options = self.get_options()
        errors = []
        
        # Validate threading
        threads = options.get('threads', 1)
        if threads > 1:
            errors.append("Warning: Using multiple threads may cause instability")
        
        # Validate delay
        delay = options.get('delay', 0)
        if delay > 0:
            timeout = options.get('timeout', 30)
            if delay > timeout:
                errors.append("Delay should not exceed timeout value")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'options': options
        }
