"""
Hidden Switches Tab - Advanced/hidden SQLmap options
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QGroupBox,
    QCheckBox, QLineEdit, QPushButton, QTextEdit, QComboBox, QSpinBox
)
from PyQt6.QtCore import pyqtSignal
from typing import Dict, Any

from ..widgets.custom_widgets import OptionGroup
from .base_tab import BaseTab


class HiddenSwitchesTab(BaseTab):
    """Advanced/hidden SQLmap options tab"""
    
    def __init__(self, parent=None, mutual_exclusion_manager=None):
        super().__init__(parent, mutual_exclusion_manager)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # HTTP parameter pollution
        hpp_group = QGroupBox("HTTP Parameter Pollution")
        hpp_layout = QFormLayout(hpp_group)
        
        self.hpp = QCheckBox("Use HTTP parameter pollution method")
        self.hpp.setToolTip("Use HTTP parameter pollution method (--hpp)")
        hpp_layout.addRow("", self.hpp)
        
        layout.addWidget(hpp_group)
        
        # Advanced HTTP options
        http_advanced_group = QGroupBox("Advanced HTTP Options")
        http_advanced_layout = QFormLayout(http_advanced_group)
        
        self.chunked = QCheckBox("Use HTTP chunked transfer encoded requests")
        self.chunked.setToolTip("Use HTTP chunked transfer encoded requests (--chunked)")
        http_advanced_layout.addRow("", self.chunked)
        
        # Removed force_ssl and cors (moved to Request tab)
        
        layout.addWidget(http_advanced_group)
        
        # Removed Web Options group and scope filter
        
        # Testing options
        testing_group = QGroupBox("Advanced Testing")
        testing_layout = QFormLayout(testing_group)
        
        # Removed test_parameter
        
        self.unstable = QCheckBox("Adjust delays in unstable connections")
        self.unstable.setToolTip("Adjust delays in unstable connections (--unstable)")
        testing_layout.addRow("", self.unstable)
        
        layout.addWidget(testing_group)
        
        # Removed Development/Debug group and profile option
        
        # Information section
        info_group = QGroupBox("Information")
        info_layout = QVBoxLayout(info_group)
        
        info_text = QLabel("""
<b>Hidden/Advanced Switches:</b><br>
• These options are for advanced users and specific scenarios<br>
• Many of these options are experimental or rarely needed<br>
• Use with caution and only if you understand their purpose<br>
• Some options may affect SQLmap's stability or performance<br><br>
<b>Warning:</b> Advanced options can cause unexpected behavior
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
        self.hpp.toggled.connect(self.options_changed)
        self.chunked.toggled.connect(self.options_changed)
        # Removed force_ssl and cors signal connections (moved to Request tab)
        # Removed scope signal connection
        # Removed test_parameter signal connection
        self.unstable.toggled.connect(self.options_changed)
        # Removed profile signal connection
    
    def get_options(self):
        """Get advanced/hidden options"""
        options = {}
        
        if self.hpp.isChecked():
            options['hpp'] = True
        
        if self.chunked.isChecked():
            options['chunked'] = True
        
        # Removed force_ssl and cors (moved to Request tab)
        
        # Removed scope
        
        # Removed test_parameter
        
        if self.unstable.isChecked():
            options['unstable'] = True
        
        # Removed profile
        
        return options
    
    def set_options(self, options):
        """Set advanced/hidden options"""
        self.hpp.setChecked(options.get('hpp', False))
        self.chunked.setChecked(options.get('chunked', False))
        # Removed force_ssl and cors (moved to Request tab)
        # Removed scope
        # Removed test_parameter
        self.unstable.setChecked(options.get('unstable', False))
        # Removed profile
    
    def reset_options(self):
        """Reset advanced/hidden options to defaults"""
        self.hpp.setChecked(False)
        self.chunked.setChecked(False)
        # Removed force_ssl and cors (moved to Request tab)
        # Removed scope
        # Removed test_parameter
        self.unstable.setChecked(False)
        # Removed profile
