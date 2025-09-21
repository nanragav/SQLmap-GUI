"""
UDF Tab - User-defined function injection
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QGroupBox,
    QCheckBox, QLineEdit, QPushButton, QFileDialog
)
from PyQt6.QtCore import pyqtSignal
from typing import Dict, Any

from ..widgets.custom_widgets import OptionGroup
from .base_tab import BaseTab


class UdfTab(BaseTab):
    """UDF (User-Defined Function) injection tab"""
    
    def __init__(self, parent=None, mutual_exclusion_manager=None):
        super().__init__(parent, mutual_exclusion_manager)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # UDF injection options
        udf_group = QGroupBox("UDF Injection")
        udf_layout = QFormLayout(udf_group)
        
        self.udf_inject = QCheckBox("Inject user-defined functions")
        self.udf_inject.setToolTip("Inject user-defined functions (--udf-inject)")
        udf_layout.addRow("", self.udf_inject)
        
        self.shared_lib = QLineEdit()
        self.shared_lib.setPlaceholderText("Path to shared library file")
        self.shared_lib.setToolTip("Local path to the shared library (--shared-lib)")
        browse_lib_btn = QPushButton("Browse")
        browse_lib_btn.clicked.connect(lambda: self.browse_file(self.shared_lib, "Library files (*.so *.dll);;All files (*.*)"))
        lib_layout = QHBoxLayout()
        lib_layout.addWidget(self.shared_lib)
        lib_layout.addWidget(browse_lib_btn)
        udf_layout.addRow("Shared library:", lib_layout)
        
        layout.addWidget(udf_group)
        
        layout.addStretch()
        
        # Connect signals
        self.connect_signals()
    
    def browse_file(self, line_edit, file_filter="All files (*.*)"):
        """Browse for file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select File", "", file_filter
        )
        if file_path:
            line_edit.setText(file_path)
    
    def connect_signals(self):
        """Connect widget signals"""
        self.udf_inject.toggled.connect(self.options_changed)
        self.shared_lib.textChanged.connect(self.options_changed)
    
    def get_options(self):
        """Get UDF injection options"""
        options = {}
        
        if self.udf_inject.isChecked():
            options['udf_inject'] = True
        
        if self.shared_lib.text().strip():
            options['shared_lib'] = self.shared_lib.text().strip()
        
        return options
    
    def set_options(self, options):
        """Set UDF injection options"""
        self.udf_inject.setChecked(options.get('udf_inject', False))
        self.shared_lib.setText(options.get('shared_lib', ''))
    
    def reset_options(self):
        """Reset UDF injection options to defaults"""
        self.udf_inject.setChecked(False)
        self.shared_lib.clear()
