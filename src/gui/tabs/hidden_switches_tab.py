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
        
        self.force_ssl = QCheckBox("Force usage of SSL/HTTPS")
        self.force_ssl.setToolTip("Force usage of SSL/HTTPS (--force-ssl)")
        http_advanced_layout.addRow("", self.force_ssl)
        
        self.cors = QCheckBox("Add CORS headers to requests")
        self.cors.setToolTip("Add CORS headers to requests (--cors)")
        http_advanced_layout.addRow("", self.cors)
        
        layout.addWidget(http_advanced_group)
        
        # Web root options
        web_group = QGroupBox("Web Options")
        web_layout = QFormLayout(web_group)
        
        self.web_root = QLineEdit()
        self.web_root.setPlaceholderText("Web server document root directory")
        self.web_root.setToolTip("Web server document root directory (--web-root)")
        web_layout.addRow("Web root:", self.web_root)
        
        self.scope = QLineEdit()
        self.scope.setPlaceholderText("Regexp to filter targets from provided proxy log")
        self.scope.setToolTip("Regexp to filter targets from provided proxy log (--scope)")
        web_layout.addRow("Scope filter:", self.scope)
        
        layout.addWidget(web_group)
        
        # Testing options
        testing_group = QGroupBox("Advanced Testing")
        testing_layout = QFormLayout(testing_group)
        
        self.test_parameter = QLineEdit()
        self.test_parameter.setPlaceholderText("Testable parameter(s)")
        self.test_parameter.setToolTip("Testable parameter(s) (--test-parameter)")
        testing_layout.addRow("Test parameter:", self.test_parameter)
        
        self.unstable = QCheckBox("Adjust delays in unstable connections")
        self.unstable.setToolTip("Adjust delays in unstable connections (--unstable)")
        testing_layout.addRow("", self.unstable)
        
        layout.addWidget(testing_group)
        
        # Development/Debug options
        debug_group = QGroupBox("Development/Debug")
        debug_layout = QFormLayout(debug_group)
        
        self.profile = QCheckBox("Turn on profiler")
        self.profile.setToolTip("Turn on profiler (--profile)")
        debug_layout.addRow("", self.profile)
        
        layout.addWidget(debug_group)
        
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
        self.force_ssl.toggled.connect(self.options_changed)
        self.cors.toggled.connect(self.options_changed)
        self.web_root.textChanged.connect(self.options_changed)
        self.scope.textChanged.connect(self.options_changed)
        self.test_parameter.textChanged.connect(self.options_changed)
        self.unstable.toggled.connect(self.options_changed)
        self.profile.toggled.connect(self.options_changed)
    
    def get_options(self):
        """Get advanced/hidden options"""
        options = {}
        

        

        

        
        if self.hpp.isChecked():
            options['hpp'] = True
        
        if self.chunked.isChecked():
            options['chunked'] = True
        
        if self.force_ssl.isChecked():
            options['force_ssl'] = True
        
        if self.cors.isChecked():
            options['cors'] = True
        
        if self.web_root.text().strip():
            options['web_root'] = self.web_root.text().strip()
        
        if self.scope.text().strip():
            options['scope'] = self.scope.text().strip()
        
        if self.unstable.isChecked():
            options['unstable'] = True
        
        if self.profile.isChecked():
            options['profile'] = True
        
        return options
    
    def set_options(self, options):
        """Set advanced/hidden options"""



        self.hpp.setChecked(options.get('hpp', False))
        self.chunked.setChecked(options.get('chunked', False))
        self.force_ssl.setChecked(options.get('force_ssl', False))
        self.cors.setChecked(options.get('cors', False))
        self.web_root.setText(options.get('web_root', ''))
        self.scope.setText(options.get('scope', ''))
        self.test_parameter.setText(options.get('test_parameter', ''))
        self.unstable.setChecked(options.get('unstable', False))
        self.profile.setChecked(options.get('profile', False))
    
    def reset_options(self):
        """Reset advanced/hidden options to defaults"""



        self.hpp.setChecked(False)
        self.chunked.setChecked(False)
        self.force_ssl.setChecked(False)
        self.cors.setChecked(False)
        self.web_root.clear()
        self.scope.clear()
        self.test_parameter.clear()
        self.unstable.setChecked(False)
        self.profile.setChecked(False)
