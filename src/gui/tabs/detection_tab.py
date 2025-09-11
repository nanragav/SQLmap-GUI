"""
Detection Tab - SQL injection detection options
Handles detection techniques, level, risk, and string matching
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                            QCheckBox, QComboBox, QSpinBox, QTextEdit, QGroupBox,
                            QScrollArea, QPushButton, QFileDialog, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import Dict, Any

from ..widgets.custom_widgets import OptionGroup, ValidatedLineEdit


class DetectionTab(QWidget):
    """Tab for SQL injection detection options"""
    
    options_changed = pyqtSignal()
    
    def __init__(self, parent=None, mutual_exclusion_manager=None):
        super().__init__(parent)
        self.mutual_exclusion_manager = mutual_exclusion_manager
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the detection tab UI"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        
        layout = QVBoxLayout()
        
        # Detection level and risk
        level_risk_group = self.create_level_risk_group()
        layout.addWidget(level_risk_group)
        
        # String matching group
        string_group = self.create_string_group()
        layout.addWidget(string_group)
        
        # Advanced detection group
        advanced_group = self.create_advanced_group()
        layout.addWidget(advanced_group)
        
        layout.addStretch()
        scroll_content.setLayout(layout)
        scroll_area.setWidget(scroll_content)
        
        tab_layout = QVBoxLayout()
        tab_layout.addWidget(scroll_area)
        self.setLayout(tab_layout)
    
    def create_level_risk_group(self) -> QGroupBox:
        """Create level and risk options"""
        level_risk_options = [
            {
                'name': 'level',
                'type': 'number',
                'label': 'Level of Tests (1-5)',
                'min': 1,
                'max': 5,
                'default': 1
            },
            {
                'name': 'risk',
                'type': 'number',
                'label': 'Risk of Tests (1-3)',
                'min': 1,
                'max': 3,
                'default': 1
            },
            {
                'name': 'smart',
                'type': 'checkbox',
                'label': 'Conduct Thorough Tests Only if Positive Heuristics'
            }
        ]
        
        return OptionGroup("Detection Level & Risk", level_risk_options, self.mutual_exclusion_manager)
    
    def create_string_group(self) -> QGroupBox:
        """Create string matching options"""
        string_options = [
            {
                'name': 'string',
                'type': 'text',
                'label': 'String to Match When Query is Valid',
                'placeholder': 'success|welcome|login'
            },
            {
                'name': 'not_string',
                'type': 'text',
                'label': 'String to Match When Query is Invalid',
                'placeholder': 'error|failed|invalid'
            },
            {
                'name': 'regexp',
                'type': 'text',
                'label': 'Regexp to Match When Query is Valid',
                'placeholder': 'User.*found|Welcome.*admin'
            },
            {
                'name': 'code',
                'type': 'text',
                'label': 'HTTP Code to Match When Query is Valid',
                'placeholder': '200,302'
            },
            {
                'name': 'text_only',
                'type': 'checkbox',
                'label': 'Compare Pages Based Only on Textual Content'
            },
            {
                'name': 'titles',
                'type': 'checkbox',
                'label': 'Compare Pages Based Only on Their Titles'
            }
        ]
        
        return OptionGroup("String Matching", string_options, self.mutual_exclusion_manager)
    
    def create_advanced_group(self) -> QGroupBox:
        """Create advanced detection options"""
        advanced_options = [
            # Removed duplicate invalidation options (already exist in Injection tab)
            # invalid_bignum, invalid_logical, invalid_string, no_cast, no_escape
            {
                'name': 'union_cols',
                'type': 'text',
                'label': 'Range of Columns to Test for UNION Query',
                'placeholder': '1-10'
            },
            {
                'name': 'union_char',
                'type': 'text',
                'label': 'Character to Use for Bruteforcing Column Number',
                'placeholder': 'NULL'
            },
            {
                'name': 'union_from',
                'type': 'text',
                'label': 'Table to Use in FROM Part of UNION Query',
                'placeholder': 'information_schema.tables'
            },
            {
                'name': 'dns_domain',
                'type': 'text',
                'label': 'Domain Name Used for DNS Exfiltration',
                'placeholder': 'attacker.com'
            },
            {
                'name': 'second_url',
                'type': 'text',
                'label': 'Resulting Page URL Searched for Second-Order Response',
                'validator': 'url',
                'placeholder': 'http://example.com/result.php'
            },
            {
                'name': 'second_req',
                'type': 'file',
                'label': 'Load Second-Order HTTP Request from File',
                'filter': 'Text Files (*.txt);;All Files (*)'
            }
        ]
        
        return OptionGroup("Advanced Detection", advanced_options, self.mutual_exclusion_manager)
    
    def get_options(self) -> Dict[str, Any]:
        """Get all options from this tab"""
        options = {}
        
        for i in range(self.layout().itemAt(0).widget().widget().layout().count()):
            item = self.layout().itemAt(0).widget().widget().layout().itemAt(i)
            if item and item.widget() and isinstance(item.widget(), OptionGroup):
                group_options = item.widget().get_values()
                options.update(group_options)
        
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
