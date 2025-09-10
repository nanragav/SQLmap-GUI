"""
Techniques Tab - SQL injection techniques selection
Handles Boolean-based, Time-based, Union-based, Error-based, and Stacked queries
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                            QCheckBox, QComboBox, QSpinBox, QTextEdit, QGroupBox,
                            QScrollArea, QPushButton, QFileDialog, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import Dict, Any

from ..widgets.custom_widgets import OptionGroup, ValidatedLineEdit


class TechniquesTab(QWidget):
    """Tab for SQL injection techniques selection"""
    
    options_changed = pyqtSignal()
    
    def __init__(self, parent=None, mutual_exclusion_manager=None):
        super().__init__(parent)
        self.mutual_exclusion_manager = mutual_exclusion_manager
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the techniques tab UI"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        
        layout = QVBoxLayout()
        
        # Technique selection group
        technique_group = self.create_technique_group()
        layout.addWidget(technique_group)
        
        # Boolean-based options
        boolean_group = self.create_boolean_group()
        layout.addWidget(boolean_group)
        
        # Time-based options
        time_group = self.create_time_group()
        layout.addWidget(time_group)
        
        # Union-based options
        union_group = self.create_union_group()
        layout.addWidget(union_group)
        
        # Error-based options
        error_group = self.create_error_group()
        layout.addWidget(error_group)
        
        # Out-of-Band options
        oob_group = self.create_oob_group()
        layout.addWidget(oob_group)
        
        layout.addStretch()
        scroll_content.setLayout(layout)
        scroll_area.setWidget(scroll_content)
        
        tab_layout = QVBoxLayout()
        tab_layout.addWidget(scroll_area)
        self.setLayout(tab_layout)
    
    def create_technique_group(self) -> QGroupBox:
        """Create technique selection options"""
        technique_options = [
            {
                'name': 'technique',
                'type': 'text',
                'label': 'SQL Injection Techniques to Use',
                'placeholder': 'BEUSTQ (B=Boolean, E=Error, U=Union, S=Stacked, T=Time, Q=Inline)'
            },
            {
                'name': 'boolean_blind',
                'type': 'checkbox',
                'label': 'Boolean-based Blind SQL Injection'
            },
            {
                'name': 'error_based',
                'type': 'checkbox',
                'label': 'Error-based SQL Injection'
            },
            {
                'name': 'union_based',
                'type': 'checkbox',
                'label': 'UNION Query-based SQL Injection'
            },
            {
                'name': 'stacked_queries',
                'type': 'checkbox',
                'label': 'Stacked Queries SQL Injection'
            },
            {
                'name': 'time_based',
                'type': 'checkbox',
                'label': 'Time-based Blind SQL Injection'
            },
            {
                'name': 'inline_queries',
                'type': 'checkbox',
                'label': 'Inline Query SQL Injection'
            }
        ]
        
        return OptionGroup("Injection Techniques", technique_options, self.mutual_exclusion_manager)
    
    def create_boolean_group(self) -> QGroupBox:
        """Create Boolean-based blind injection options"""
        boolean_options = [
            {
                'name': 'bool_true',
                'type': 'text',
                'label': 'True Statement for Boolean Injection',
                'placeholder': '1=1'
            },
            {
                'name': 'bool_false',
                'type': 'text',
                'label': 'False Statement for Boolean Injection',
                'placeholder': '1=2'
            }
        ]
        
        return OptionGroup("Boolean-based Blind", boolean_options, self.mutual_exclusion_manager)
    
    def create_time_group(self) -> QGroupBox:
        """Create Time-based blind injection options"""
        time_options = [
            {
                'name': 'time_sec',
                'type': 'number',
                'label': 'Seconds to Delay DBMS Response',
                'min': 1,
                'max': 30,
                'default': 5
            }
        ]
        
        return OptionGroup("Time-based Blind", time_options, self.mutual_exclusion_manager)
    
    def create_union_group(self) -> QGroupBox:
        """Create UNION-based injection options"""
        union_options = [
            {
                'name': 'union_cols',
                'type': 'text',
                'label': 'Range of Columns to Test for UNION',
                'placeholder': '1-20'
            },
            {
                'name': 'union_char',
                'type': 'text',
                'label': 'Character for Bruteforcing Column Number',
                'placeholder': 'NULL'
            },
            {
                'name': 'union_from',
                'type': 'text',
                'label': 'Table to Use in FROM Part of UNION',
                'placeholder': 'information_schema.tables'
            },
            {
                'name': 'union_values',
                'type': 'text',
                'label': 'Column Values to Use in UNION',
                'placeholder': '1,2,3,4,5'
            }
        ]
        
        return OptionGroup("UNION Query-based", union_options, self.mutual_exclusion_manager)
    
    def create_error_group(self) -> QGroupBox:
        """Create Error-based injection options"""
        error_options = [
            {
                'name': 'error_dbms',
                'type': 'combo',
                'label': 'Target DBMS for Error-based',
                'items': [
                    {'label': 'Auto-detect', 'value': ''},
                    {'label': 'MySQL', 'value': 'mysql'},
                    {'label': 'PostgreSQL', 'value': 'postgresql'},
                    {'label': 'MSSQL', 'value': 'mssql'},
                    {'label': 'Oracle', 'value': 'oracle'}
                ]
            }
        ]
        
        return OptionGroup("Error-based", error_options, self.mutual_exclusion_manager)
    
    def create_oob_group(self) -> QGroupBox:
        """Create Out-of-Band attack options"""
        oob_options = [
            {
                'name': 'dns_domain',
                'type': 'text',
                'label': 'DNS Domain for OOB Attacks',
                'placeholder': 'subdomain.yourdomain.com',
                'tooltip': 'Domain name for DNS exfiltration and OOB attacks (--dns-domain)'
            },
            {
                'name': 'second_url',
                'type': 'text',
                'label': 'Second-order URL',
                'placeholder': 'http://example.com/page2.php',
                'tooltip': 'URL to test for second-order SQL injection (--second-url)'
            },
            {
                'name': 'second_req',
                'type': 'file',
                'label': 'Second-order Request File',
                'tooltip': 'Load second-order HTTP request from file (--second-req)'
            }
        ]
        
        return OptionGroup("Out-of-Band Attacks", oob_options, self.mutual_exclusion_manager)
    
    def get_options(self) -> Dict[str, Any]:
        """Get all options from this tab"""
        options = {}
        
        for i in range(self.layout().itemAt(0).widget().widget().layout().count()):
            item = self.layout().itemAt(0).widget().widget().layout().itemAt(i)
            if item and item.widget() and isinstance(item.widget(), OptionGroup):
                group_options = item.widget().get_values()
                options.update(group_options)
        
        # Build technique string from individual checkboxes
        techniques = []
        if options.pop('boolean_blind', False):
            techniques.append('B')
        if options.pop('error_based', False):
            techniques.append('E')
        if options.pop('union_based', False):
            techniques.append('U')
        if options.pop('stacked_queries', False):
            techniques.append('S')
        if options.pop('time_based', False):
            techniques.append('T')
        if options.pop('inline_queries', False):
            techniques.append('Q')
        
        if techniques:
            options['technique'] = ''.join(techniques)
        
        return {k: v for k, v in options.items() if v is not None and v != ''}
    
    def set_options(self, options: Dict[str, Any]):
        """Set options in this tab"""
        # Parse technique string into individual checkboxes
        technique = options.get('technique', '')
        if technique:
            parsed_options = options.copy()
            parsed_options['boolean_blind'] = 'B' in technique
            parsed_options['error_based'] = 'E' in technique
            parsed_options['union_based'] = 'U' in technique
            parsed_options['stacked_queries'] = 'S' in technique
            parsed_options['time_based'] = 'T' in technique
            parsed_options['inline_queries'] = 'Q' in technique
            options = parsed_options
        
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
