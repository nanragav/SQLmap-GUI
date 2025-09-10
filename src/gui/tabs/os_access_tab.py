"""
OS Access Tab - Operating system access options
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QGroupBox,
    QCheckBox, QLineEdit, QPushButton, QTextEdit, QComboBox, QSpinBox, 
    QSizePolicy, QFileDialog
)
from PyQt6.QtCore import pyqtSignal
from typing import Dict, Any

from ..widgets.custom_widgets import OptionGroup
from .base_tab import BaseTab


class OsAccessTab(BaseTab):
    """Operating system access tab"""
    
    def __init__(self, parent=None, mutual_exclusion_manager=None):
        super().__init__(parent, mutual_exclusion_manager)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # OS command execution
        cmd_group = QGroupBox("Command Execution")
        cmd_layout = QFormLayout(cmd_group)
        
        self.os_cmd = QLineEdit()
        self.os_cmd.setPlaceholderText("Operating system command to execute")
        self.os_cmd.setToolTip("Execute an operating system command (--os-cmd)")
        cmd_layout.addRow("OS Command:", self.os_cmd)
        
        self.os_shell = QCheckBox("Prompt for an interactive OS shell")
        self.os_shell.setToolTip("Prompt for an interactive operating system shell (--os-shell)")
        cmd_layout.addRow("", self.os_shell)
        
        layout.addWidget(cmd_group)
        
        # OS takeover options
        takeover_group = QGroupBox("OS Takeover")
        takeover_layout = QFormLayout(takeover_group)
        
        self.os_pwn = QCheckBox("Prompt for an OOB shell, Meterpreter or VNC")
        self.os_pwn.setToolTip("Prompt for an out-of-band shell, Meterpreter or VNC (--os-pwn)")
        takeover_layout.addRow("", self.os_pwn)
        
        self.os_smbrelay = QCheckBox("One click prompt for an OOB shell, Meterpreter or VNC")
        self.os_smbrelay.setToolTip("One click prompt for an OOB shell, Meterpreter or VNC (--os-smbrelay)")
        takeover_layout.addRow("", self.os_smbrelay)
        
        self.os_bof = QCheckBox("Stored procedure buffer overflow exploitation")
        self.os_bof.setToolTip("Stored procedure buffer overflow exploitation (--os-bof)")
        takeover_layout.addRow("", self.os_bof)
        
        layout.addWidget(takeover_group)
        
        # Privilege escalation
        privesc_group = QGroupBox("Privilege Escalation")
        privesc_layout = QFormLayout(privesc_group)
        
        self.priv_esc = QCheckBox("Database process user privilege escalation")
        self.priv_esc.setToolTip("Database process user privilege escalation (--priv-esc)")
        privesc_layout.addRow("", self.priv_esc)
        
        layout.addWidget(privesc_group)
        
        # Metasploit options
        msf_group = QGroupBox("Metasploit Integration")
        msf_layout = QFormLayout(msf_group)
        
        self.msf_path = QLineEdit()
        self.msf_path.setPlaceholderText("Local path to Metasploit Framework")
        self.msf_path.setToolTip("Local path where Metasploit Framework is installed (--msf-path)")
        browse_msf_btn = QPushButton("Browse")
        browse_msf_btn.clicked.connect(lambda: self.browse_directory(self.msf_path))
        msf_layout_h = QHBoxLayout()
        msf_layout_h.addWidget(self.msf_path)
        msf_layout_h.addWidget(browse_msf_btn)
        msf_layout.addRow("MSF Path:", msf_layout_h)
        
        layout.addWidget(msf_group)
        
        # Temporary paths
        temp_group = QGroupBox("Temporary Paths")
        temp_layout = QFormLayout(temp_group)
        
        self.tmp_path = QLineEdit()
        self.tmp_path.setPlaceholderText("Remote absolute path of temporary files directory")
        self.tmp_path.setToolTip("Remote absolute path of temporary files directory (--tmp-path)")
        temp_layout.addRow("Temp Path:", self.tmp_path)
        
        layout.addWidget(temp_group)
        
        # Advanced options
        advanced_group = QGroupBox("Advanced Options")
        advanced_layout = QFormLayout(advanced_group)
        
        # Remove payload_encoding as it's not a valid SQLmap parameter
        # Instead, add a note about OS command execution
        self.os_note = QLabel("Note: OS command execution requires database admin privileges")
        self.os_note.setStyleSheet("QLabel { color: #666; font-style: italic; margin: 5px; }")
        advanced_layout.addRow("", self.os_note)
        
        layout.addWidget(advanced_group)
        
        # Command output preview
        output_group = QGroupBox("Command Output")
        output_layout = QVBoxLayout(output_group)
        
        self.output_preview = QTextEdit()
        self.output_preview.setReadOnly(True)
        self.output_preview.setMaximumHeight(150)
        self.output_preview.setPlaceholderText("Command output will be displayed here...")
        output_layout.addWidget(self.output_preview)
        
        layout.addWidget(output_group)
        
        # Information section
        info_group = QGroupBox("Information")
        info_layout = QVBoxLayout(info_group)
        
        info_text = QLabel("""
<b>Operating System Access:</b><br>
• <b>Command Execution:</b> Execute system commands on the database server<br>
• <b>Shell Access:</b> Interactive shell access to the operating system<br>
• <b>Privilege Escalation:</b> Attempt to escalate database user privileges<br>
• <b>Warning:</b> These features can be highly intrusive - use only on authorized systems<br><br>
<b>Requirements:</b> Database admin privileges, stored procedure execution rights
        """)
        info_text.setWordWrap(True)
        info_text.setStyleSheet("QLabel { color: #666; font-size: 10pt; }")
        info_layout.addWidget(info_text)
        
        layout.addWidget(info_group)
        
        layout.addStretch()
        
        # Connect signals
        self.connect_signals()
    
    def browse_directory(self, line_edit):
        """Browse for directory"""
        from PyQt6.QtWidgets import QFileDialog
        dir_path = QFileDialog.getExistingDirectory(
            self, "Select Directory"
        )
        if dir_path:
            line_edit.setText(dir_path)
    
    def connect_signals(self):
        """Connect widget signals"""
        self.os_cmd.textChanged.connect(self.options_changed)
        self.os_shell.toggled.connect(self.options_changed)
        self.os_pwn.toggled.connect(self.options_changed)
        self.os_smbrelay.toggled.connect(self.options_changed)
        self.os_bof.toggled.connect(self.options_changed)
        self.priv_esc.toggled.connect(self.options_changed)
        self.msf_path.textChanged.connect(self.options_changed)
        self.tmp_path.textChanged.connect(self.options_changed)

    
    def get_options(self):
        """Get OS access options"""
        options = {}
        
        if self.os_cmd.text().strip():
            options['os_cmd'] = self.os_cmd.text().strip()
        
        if self.os_shell.isChecked():
            options['os_shell'] = True
        
        if self.os_pwn.isChecked():
            options['os_pwn'] = True
        
        if self.os_smbrelay.isChecked():
            options['os_smbrelay'] = True
        
        if self.os_bof.isChecked():
            options['os_bof'] = True
        
        if self.priv_esc.isChecked():
            options['priv_esc'] = True
        
        if self.msf_path.text().strip():
            options['msf_path'] = self.msf_path.text().strip()
        
        if self.tmp_path.text().strip():
            options['tmp_path'] = self.tmp_path.text().strip()
        
        return options
    
    def set_options(self, options):
        """Set OS access options"""
        self.os_cmd.setText(options.get('os_cmd', ''))
        self.os_shell.setChecked(options.get('os_shell', False))
        self.os_pwn.setChecked(options.get('os_pwn', False))
        self.os_smbrelay.setChecked(options.get('os_smbrelay', False))
        self.os_bof.setChecked(options.get('os_bof', False))
        self.priv_esc.setChecked(options.get('priv_esc', False))
        self.msf_path.setText(options.get('msf_path', ''))
        self.tmp_path.setText(options.get('tmp_path', ''))
    
    def reset_options(self):
        """Reset OS access options to defaults"""
        self.os_cmd.clear()
        self.os_shell.setChecked(False)
        self.os_pwn.setChecked(False)
        self.os_smbrelay.setChecked(False)
        self.os_bof.setChecked(False)
        self.priv_esc.setChecked(False)
        self.msf_path.clear()
        self.tmp_path.clear()
        self.output_preview.clear()
