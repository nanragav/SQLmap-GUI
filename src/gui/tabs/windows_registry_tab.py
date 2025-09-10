"""
Windows Registry Tab - Windows registry access options
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QGroupBox,
    QCheckBox, QLineEdit, QPushButton, QTextEdit, QComboBox
)
from PyQt6.QtCore import pyqtSignal
from typing import Dict, Any

from ..widgets.custom_widgets import OptionGroup
from .base_tab import BaseTab


class WindowsRegistryTab(BaseTab):
    """Windows registry access tab"""
    
    def __init__(self, parent=None, mutual_exclusion_manager=None):
        super().__init__(parent, mutual_exclusion_manager)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Registry operations
        ops_group = QGroupBox("Registry Operations")
        ops_layout = QFormLayout(ops_group)
        
        self.reg_read = QCheckBox("Read a Windows registry key value")
        self.reg_read.setToolTip("Read a Windows registry key value (--reg-read)")
        ops_layout.addRow("", self.reg_read)
        
        self.reg_add = QCheckBox("Write a Windows registry key value data")
        self.reg_add.setToolTip("Write a Windows registry key value data (--reg-add)")
        ops_layout.addRow("", self.reg_add)
        
        self.reg_del = QCheckBox("Delete a Windows registry key value")
        self.reg_del.setToolTip("Delete a Windows registry key value (--reg-del)")
        ops_layout.addRow("", self.reg_del)
        
        layout.addWidget(ops_group)
        
        # Registry key specification
        key_group = QGroupBox("Registry Key Details")
        key_layout = QFormLayout(key_group)
        
        self.reg_key = QLineEdit()
        self.reg_key.setPlaceholderText("Registry key (e.g., HKEY_LOCAL_MACHINE\\SOFTWARE\\...)")
        self.reg_key.setToolTip("Windows registry key (--reg-key)")
        key_layout.addRow("Registry key:", self.reg_key)
        
        self.reg_value = QLineEdit()
        self.reg_value.setPlaceholderText("Registry key value name")
        self.reg_value.setToolTip("Windows registry key value (--reg-value)")
        key_layout.addRow("Value name:", self.reg_value)
        
        self.reg_data = QLineEdit()
        self.reg_data.setPlaceholderText("Registry key value data")
        self.reg_data.setToolTip("Windows registry key value data (--reg-data)")
        key_layout.addRow("Value data:", self.reg_data)
        
        layout.addWidget(key_group)
        
        # Information section
        info_group = QGroupBox("Information")
        info_layout = QVBoxLayout(info_group)
        
        info_text = QLabel("""
<b>Windows Registry Access:</b><br>
• <b>Read:</b> Query registry key values<br>
• <b>Write:</b> Create or modify registry key values<br>
• <b>Delete:</b> Remove registry key values<br>
• Requires administrative privileges on target system<br>
• <b>Warning:</b> Registry modifications can affect system stability<br><br>
<b>Supported:</b> Windows systems with SQL Server using xp_regread/xp_regwrite
        """)
        info_text.setWordWrap(True)
        info_text.setStyleSheet("QLabel { color: #666; font-size: 10pt; }")
        info_layout.addWidget(info_text)
        
        layout.addWidget(info_group)
        
        layout.addStretch()
        
        # Connect signals
        self.connect_signals()
    
    def connect_signals(self):
        """Connect widget signals"""
        self.reg_read.toggled.connect(self.options_changed)
        self.reg_add.toggled.connect(self.options_changed)
        self.reg_del.toggled.connect(self.options_changed)
    
    def get_options(self):
        """Get Windows registry options"""
        options = {}
        
        if self.reg_read.isChecked():
            options['reg_read'] = True
        
        if self.reg_add.isChecked():
            options['reg_add'] = True
        
        if self.reg_del.isChecked():
            options['reg_del'] = True
        
        if self.reg_key.text().strip():
            options['reg_key'] = self.reg_key.text().strip()
        
        if self.reg_value.text().strip():
            options['reg_value'] = self.reg_value.text().strip()
        
        if self.reg_data.text().strip():
            options['reg_data'] = self.reg_data.text().strip()
        
        return options
    
    def set_options(self, options):
        """Set Windows registry options"""
        self.reg_read.setChecked(options.get('reg_read', False))
        self.reg_add.setChecked(options.get('reg_add', False))
        self.reg_del.setChecked(options.get('reg_del', False))
        self.reg_key.setText(options.get('reg_key', ''))
        self.reg_value.setText(options.get('reg_value', ''))
        self.reg_data.setText(options.get('reg_data', ''))
    
    def reset_options(self):
        """Reset Windows registry options to defaults"""
        self.reg_read.setChecked(False)
        self.reg_add.setChecked(False)
        self.reg_del.setChecked(False)
        self.reg_key.clear()
        self.reg_value.clear()
        self.reg_data.clear()
