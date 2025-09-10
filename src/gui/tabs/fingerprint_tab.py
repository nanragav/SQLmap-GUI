"""
Fingerprint Tab - DBMS fingerprinting options
Handles fingerprinting and database detection options
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                            QCheckBox, QComboBox, QSpinBox, QTextEdit, QGroupBox,
                            QScrollArea, QPushButton, QFileDialog, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import Dict, Any

from ..widgets.custom_widgets import OptionGroup, ValidatedLineEdit


class FingerprintTab(QWidget):
    """Tab for DBMS fingerprinting options"""
    
    options_changed = pyqtSignal()
    
    def __init__(self, parent=None, mutual_exclusion_manager=None):
        super().__init__(parent)
        self.mutual_exclusion_manager = mutual_exclusion_manager
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the fingerprint tab UI"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        
        layout = QVBoxLayout()
        
        # Fingerprint options group
        fingerprint_group = self.create_fingerprint_group()
        layout.addWidget(fingerprint_group)
        
        # DBMS detection group
        detection_group = self.create_detection_group()
        layout.addWidget(detection_group)
        
        layout.addStretch()
        scroll_content.setLayout(layout)
        scroll_area.setWidget(scroll_content)
        
        tab_layout = QVBoxLayout()
        tab_layout.addWidget(scroll_area)
        self.setLayout(tab_layout)
    
    def create_fingerprint_group(self) -> QGroupBox:
        """Create fingerprinting options"""
        fingerprint_options = [
            {
                'name': 'fingerprint',
                'type': 'checkbox',
                'label': 'Perform Extensive DBMS Version Fingerprinting'
            },
            {
                'name': 'banner',
                'type': 'checkbox',
                'label': 'Retrieve DBMS Banner'
            },
            {
                'name': 'hostname',
                'type': 'checkbox',
                'label': 'Retrieve DBMS Server Hostname'
            },
            {
                'name': 'current_user',
                'type': 'checkbox',
                'label': 'Retrieve DBMS Current User'
            },
            {
                'name': 'current_db',
                'type': 'checkbox',
                'label': 'Retrieve DBMS Current Database'
            },
            {
                'name': 'is_dba',
                'type': 'checkbox',
                'label': 'Detect if Current User is DBA'
            }
        ]
        
        return OptionGroup("Fingerprinting", fingerprint_options, self.mutual_exclusion_manager)
    
    def create_detection_group(self) -> QGroupBox:
        """Create DBMS detection options"""
        detection_options = [
            {
                'name': 'dbms',
                'type': 'combo',
                'label': 'Force Back-end DBMS',
                'items': [
                    {'label': 'Auto-detect', 'value': ''},
                    {'label': 'MySQL', 'value': 'mysql'},
                    {'label': 'PostgreSQL', 'value': 'postgresql'},
                    {'label': 'Microsoft SQL Server', 'value': 'mssql'},
                    {'label': 'Oracle', 'value': 'oracle'},
                    {'label': 'SQLite', 'value': 'sqlite'},
                    {'label': 'Microsoft Access', 'value': 'access'},
                    {'label': 'Firebird', 'value': 'firebird'},
                    {'label': 'IBM DB2', 'value': 'db2'},
                    {'label': 'SAP MaxDB', 'value': 'maxdb'},
                    {'label': 'Sybase', 'value': 'sybase'},
                    {'label': 'Informix', 'value': 'informix'},
                    {'label': 'HSQLDB', 'value': 'hsqldb'},
                    {'label': 'H2', 'value': 'h2'}
                ]
            },
            {
                'name': 'os',
                'type': 'combo',
                'label': 'Force Back-end OS',
                'items': [
                    {'label': 'Auto-detect', 'value': ''},
                    {'label': 'Linux', 'value': 'linux'},
                    {'label': 'Windows', 'value': 'windows'},
                    {'label': 'Unix', 'value': 'unix'}
                ]
            }
        ]
        
        return OptionGroup("DBMS Detection", detection_options, self.mutual_exclusion_manager)
    
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
