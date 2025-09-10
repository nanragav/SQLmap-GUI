"""
Brute Force Tab - Dictionary-based attacks
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QGroupBox,
    QCheckBox, QLineEdit, QPushButton, QSpinBox, QDoubleSpinBox,
    QFileDialog
)
from PyQt6.QtCore import pyqtSignal
from typing import Dict, Any

from ..widgets.custom_widgets import OptionGroup
from .base_tab import BaseTab


class BruteForceTab(BaseTab):
    """Brute force tab for common tables/columns/files discovery"""
    
    def __init__(self, parent=None, mutual_exclusion_manager=None):
        super().__init__(parent, mutual_exclusion_manager)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Brute force common discovery
        discovery_group = QGroupBox("Common Discovery")
        discovery_layout = QVBoxLayout(discovery_group)
        
        self.common_tables = QCheckBox("Check for common table names")
        self.common_tables.setToolTip("Check for common table names (--common-tables)")
        discovery_layout.addWidget(self.common_tables)
        
        self.common_columns = QCheckBox("Check for common column names")
        self.common_columns.setToolTip("Check for common column names (--common-columns)")
        discovery_layout.addWidget(self.common_columns)
        
        self.common_files = QCheckBox("Check for common file names")
        self.common_files.setToolTip("Check for common file names (--common-files)")
        discovery_layout.addWidget(self.common_files)
        
        layout.addWidget(discovery_group)
        
        layout.addStretch()
        
        # Connect signals
        self.connect_signals()
    
    def browse_file(self, line_edit):
        """Browse for file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Wordlist File", "", "Text files (*.txt);;All files (*.*)"
        )
        if file_path:
            line_edit.setText(file_path)
    
    def connect_signals(self):
        """Connect widget signals"""
        self.common_tables.toggled.connect(self.options_changed)
        self.common_columns.toggled.connect(self.options_changed)
        self.common_files.toggled.connect(self.options_changed)
    
    def get_options(self):
        """Get brute force options"""
        options = {}
        
        if self.common_tables.isChecked():
            options['common_tables'] = True
        
        if self.common_columns.isChecked():
            options['common_columns'] = True
        
        if self.common_files.isChecked():
            options['common_files'] = True
        
        return options
    
    def set_options(self, options):
        """Set brute force options"""
        self.common_tables.setChecked(options.get('common_tables', False))
        self.common_columns.setChecked(options.get('common_columns', False))
        self.common_files.setChecked(options.get('common_files', False))
    
    def reset_options(self):
        """Reset brute force options to defaults"""
        self.common_tables.setChecked(False)
        self.common_columns.setChecked(False)
        self.common_files.setChecked(False)
