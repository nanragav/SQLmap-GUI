"""
OS Access Tab - Operating system access options
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QGroupBox,
    QCheckBox, QLineEdit, QPushButton, QTextEdit, QComboBox, QSpinBox, 
    QSizePolicy, QFileDialog, QScrollArea
)
from PyQt6.QtCore import pyqtSignal, Qt
from typing import Dict, Any

from ..widgets.custom_widgets import OptionGroup
from .base_tab import BaseTab


class OsAccessTab(BaseTab):
    """Operating system access tab"""
    
    def __init__(self, parent=None, mutual_exclusion_manager=None):
        super().__init__(parent, mutual_exclusion_manager)
        self.init_ui()
    
    def init_ui(self):
        # Create main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Create scroll content widget
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)
        
        # OS command execution group
        cmd_options = [
            {
                'name': 'os_cmd',
                'type': 'text',
                'label': 'OS Command',
                'placeholder': 'Operating system command to execute',
                'tooltip': 'Execute an operating system command (--os-cmd)'
            },
            {
                'name': 'os_shell',
                'type': 'checkbox',
                'label': 'Prompt for an interactive OS shell',
                'tooltip': 'Prompt for an interactive operating system shell (--os-shell)'
            }
        ]
        cmd_group = OptionGroup("Command Execution", cmd_options)
        layout.addWidget(cmd_group)
        
        # OS takeover options group
        takeover_options = [
            {
                'name': 'os_pwn',
                'type': 'checkbox',
                'label': 'Prompt for an OOB shell, Meterpreter or VNC',
                'tooltip': 'Prompt for an out-of-band shell, Meterpreter or VNC (--os-pwn)'
            },
            {
                'name': 'os_smbrelay',
                'type': 'checkbox',
                'label': 'One click prompt for an OOB shell, Meterpreter or VNC',
                'tooltip': 'One click prompt for an OOB shell, Meterpreter or VNC (--os-smbrelay)'
            },
            {
                'name': 'os_bof',
                'type': 'checkbox',
                'label': 'Stored procedure buffer overflow exploitation',
                'tooltip': 'Stored procedure buffer overflow exploitation (--os-bof)'
            }
        ]
        takeover_group = OptionGroup("OS Takeover", takeover_options)
        layout.addWidget(takeover_group)
        
        # Privilege escalation group
        privesc_options = [
            {
                'name': 'priv_esc',
                'type': 'checkbox',
                'label': 'Database process user privilege escalation',
                'tooltip': 'Database process user privilege escalation (--priv-esc)'
            }
        ]
        privesc_group = OptionGroup("Privilege Escalation", privesc_options)
        layout.addWidget(privesc_group)
        
        # Metasploit integration group
        msf_options = [
            {
                'name': 'msf_path',
                'type': 'text',
                'label': 'MSF Path',
                'placeholder': 'Local path to Metasploit Framework',
                'tooltip': 'Local path where Metasploit Framework is installed (--msf-path)'
            }
        ]
        msf_group = OptionGroup("Metasploit Integration", msf_options)
        layout.addWidget(msf_group)
        
        # Temporary paths group
        temp_options = [
            {
                'name': 'tmp_path',
                'type': 'text',
                'label': 'Temp Path',
                'placeholder': 'Remote absolute path of temporary files directory',
                'tooltip': 'Remote absolute path of temporary files directory (--tmp-path)'
            }
        ]
        temp_group = OptionGroup("Temporary Paths", temp_options)
        layout.addWidget(temp_group)
        
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
        
        # Set up scroll area
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
        
        # Connect signals for all option groups
        self.connect_signals()
    
    def connect_signals(self):
        """Connect widget signals for all option groups"""
        # OptionGroups automatically emit the parent's options_changed signal
        # No manual connection needed since they emit through the parent hierarchy
        pass
    
    def get_options(self):
        """Get OS access options using BaseTab implementation"""
        return super().get_options()
    
    def set_options(self, options):
        """Set OS access options"""
        try:
            if self.layout() and self.layout().count() > 0:
                scroll_area = self.layout().itemAt(0).widget()
                if scroll_area and hasattr(scroll_area, 'widget'):
                    scroll_content = scroll_area.widget()
                    if scroll_content and hasattr(scroll_content, 'layout'):
                        content_layout = scroll_content.layout()
                        if content_layout:
                            for i in range(content_layout.count()):
                                item = content_layout.itemAt(i)
                                if item and item.widget() and isinstance(item.widget(), OptionGroup):
                                    item.widget().set_values(options)
        except Exception as e:
            print(f"Error setting options: {e}")
    
    def reset_options(self):
        """Reset OS access options to defaults"""
        try:
            if self.layout() and self.layout().count() > 0:
                scroll_area = self.layout().itemAt(0).widget()
                if scroll_area and hasattr(scroll_area, 'widget'):
                    scroll_content = scroll_area.widget()
                    if scroll_content and hasattr(scroll_content, 'layout'):
                        content_layout = scroll_content.layout()
                        if content_layout:
                            for i in range(content_layout.count()):
                                item = content_layout.itemAt(i)
                                if item and item.widget() and isinstance(item.widget(), OptionGroup):
                                    item.widget().reset_values()
        except Exception as e:
            print(f"Error resetting options: {e}")
