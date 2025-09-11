"""
Miscellaneous Tab - Miscellaneous options
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QGroupBox,
    QCheckBox, QLineEdit, QPushButton, QTextEdit, QComboBox, QSpinBox
)
from PyQt6.QtCore import pyqtSignal
from typing import Dict, Any

from ..widgets.custom_widgets import OptionGroup
from .base_tab import BaseTab


class MiscellaneousTab(BaseTab):
    """Miscellaneous options tab"""
    
    def __init__(self, parent=None, mutual_exclusion_manager=None):
        super().__init__(parent, mutual_exclusion_manager)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # WAF/IPS options
        waf_group = QGroupBox("WAF/IPS Detection & Evasion")
        waf_layout = QFormLayout(waf_group)
        

        

        
        self.skip_waf = QCheckBox("Skip heuristic detection of WAF/IPS protection")
        self.skip_waf.setToolTip("Skip heuristic detection of WAF/IPS protection (--skip-waf)")
        waf_layout.addRow("", self.skip_waf)
        
        layout.addWidget(waf_group)
        
        # Removed empty Page Analysis group
        
        # Traffic options
        traffic_group = QGroupBox("Traffic Control")
        traffic_layout = QFormLayout(traffic_group)
        
        self.flush_session = QCheckBox("Flush session files for current target")
        self.flush_session.setToolTip("Flush session files for current target (--flush-session)")
        traffic_layout.addRow("", self.flush_session)
        
        self.skip_heuristics = QCheckBox("Skip heuristic detection of SQLi vulnerabilities")
        self.skip_heuristics.setToolTip("Skip heuristic detection of SQLi vulnerabilities (--skip-heuristics)")
        traffic_layout.addRow("", self.skip_heuristics)
        
        layout.addWidget(traffic_group)
        
        # Removed empty Advanced Parsing group
        
        # System interaction
        system_group = QGroupBox("System Interaction")
        system_layout = QFormLayout(system_group)
        
        self.alert = QLineEdit()
        self.alert.setPlaceholderText("Command to run when injection found")
        self.alert.setToolTip("Run shell command when injection is found (--alert)")
        system_layout.addRow("Alert command:", self.alert)
        
        self.beep = QCheckBox("Beep on question and/or when injection is found")
        self.beep.setToolTip("Beep on question and/or when injection is found (--beep)")
        system_layout.addRow("", self.beep)
        
        layout.addWidget(system_group)
        
        # Miscellaneous advanced
        advanced_group = QGroupBox("Advanced Miscellaneous")
        advanced_layout = QFormLayout(advanced_group)
        
        self.dependencies = QCheckBox("Check for missing (optional) SQLmap dependencies")
        self.dependencies.setToolTip("Check for missing (optional) SQLmap dependencies (--dependencies)")
        advanced_layout.addRow("", self.dependencies)
        
        self.disable_coloring = QCheckBox("Disable console output coloring")
        self.disable_coloring.setToolTip("Disable console output coloring (--disable-coloring)")
        advanced_layout.addRow("", self.disable_coloring)
        
        self.offline = QCheckBox("Work in offline mode (only use session data)")
        self.offline.setToolTip("Work in offline mode (only use session data) (--offline)")
        advanced_layout.addRow("", self.offline)
        
        layout.addWidget(advanced_group)
        
        layout.addStretch()
        
        # Connect signals
        self.connect_signals()
    
    def connect_signals(self):
        """Connect widget signals"""
        self.skip_waf.toggled.connect(self.options_changed)
        self.flush_session.toggled.connect(self.options_changed)
        self.skip_heuristics.toggled.connect(self.options_changed)
        self.alert.textChanged.connect(self.options_changed)
        self.beep.toggled.connect(self.options_changed)
        self.dependencies.toggled.connect(self.options_changed)
        self.disable_coloring.toggled.connect(self.options_changed)
        self.offline.toggled.connect(self.options_changed)
    
    def get_options(self):
        """Get miscellaneous options"""
        options = {}
        
        if self.skip_waf.isChecked():
            options['skip_waf'] = True
        
        if self.flush_session.isChecked():
            options['flush_session'] = True
        
        if self.skip_heuristics.isChecked():
            options['skip_heuristics'] = True
        
        if self.alert.text().strip():
            options['alert'] = self.alert.text().strip()
        
        if self.beep.isChecked():
            options['beep'] = True
        
        if self.dependencies.isChecked():
            options['dependencies'] = True
        
        if self.disable_coloring.isChecked():
            options['disable_coloring'] = True
        
        if self.offline.isChecked():
            options['offline'] = True
        
        return options
    
    def set_options(self, options):
        """Set miscellaneous options"""
        self.skip_waf.setChecked(options.get('skip_waf', False))
        self.flush_session.setChecked(options.get('flush_session', False))
        self.skip_heuristics.setChecked(options.get('skip_heuristics', False))
        self.alert.setText(options.get('alert', ''))
        self.beep.setChecked(options.get('beep', False))
        self.dependencies.setChecked(options.get('dependencies', False))
        self.disable_coloring.setChecked(options.get('disable_coloring', False))
        self.offline.setChecked(options.get('offline', False))
    
    def reset_options(self):
        """Reset miscellaneous options to defaults"""
        self.skip_waf.setChecked(False)
        self.flush_session.setChecked(False)
        self.skip_heuristics.setChecked(False)
        self.alert.clear()
        self.beep.setChecked(False)
        self.dependencies.setChecked(False)
        self.disable_coloring.setChecked(False)
        self.offline.setChecked(False)
