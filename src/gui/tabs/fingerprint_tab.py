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
        
        # Removed empty DBMS Detection group
        
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
            }
            # Removed duplicate enumeration options (already exist in Enumeration tab)
            # banner, hostname, current_user, current_db, is_dba
        ]
        
        return OptionGroup("Fingerprinting", fingerprint_options, self.mutual_exclusion_manager)
    
    # Removed create_detection_group method
    
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
