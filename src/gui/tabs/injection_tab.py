"""
Injection Tab - SQL injection testing parameters
Handles parameter specification, injection types, and payload customization
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                            QCheckBox, QComboBox, QSpinBox, QTextEdit, QGroupBox,
                            QScrollArea, QPushButton, QFileDialog, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import Dict, Any

from ..widgets.custom_widgets import OptionGroup, ValidatedLineEdit


class InjectionTab(QWidget):
    """Tab for injection testing options"""
    
    options_changed = pyqtSignal()
    
    def __init__(self, parent=None, mutual_exclusion_manager=None):
        super().__init__(parent)
        self.mutual_exclusion_manager = mutual_exclusion_manager
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the injection tab UI"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        
        layout = QVBoxLayout()
        
        # Parameter testing group
        parameter_group = self.create_parameter_group()
        layout.addWidget(parameter_group)
        
        # Injection testing group
        injection_group = self.create_injection_group()
        layout.addWidget(injection_group)
        
        # Payload customization group
        payload_group = self.create_payload_group()
        layout.addWidget(payload_group)
        
        layout.addStretch()
        scroll_content.setLayout(layout)
        scroll_area.setWidget(scroll_content)
        
        tab_layout = QVBoxLayout()
        tab_layout.addWidget(scroll_area)
        self.setLayout(tab_layout)
    
    def create_parameter_group(self) -> QGroupBox:
        """Create parameter testing options"""
        parameter_options = [
            {
                'name': 'testable_parameter',
                'type': 'text',
                'label': 'Testable Parameter(s)',
                'placeholder': 'id,user,password (comma-separated)'
            },
            {
                'name': 'skip',
                'type': 'text',
                'label': 'Skip Testing Parameter(s)',
                'placeholder': 'csrf_token,session_id'
            },
            {
                'name': 'skip_static',
                'type': 'checkbox',
                'label': 'Skip Testing Parameters with Static Values'
            },
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
        
        return OptionGroup("Parameter Testing", parameter_options, self.mutual_exclusion_manager)
    
    def create_injection_group(self) -> QGroupBox:
        """Create injection testing options"""
        injection_options = [
            {
                'name': 'invalid_bignum',
                'type': 'checkbox',
                'label': 'Use Big Numbers for Invalidating Values'
            },
            {
                'name': 'invalid_logical',
                'type': 'checkbox',
                'label': 'Use Logical Operations for Invalidating Values'
            },
            {
                'name': 'invalid_string',
                'type': 'checkbox',
                'label': 'Use Random Strings for Invalidating Values'
            },
            {
                'name': 'no_cast',
                'type': 'checkbox',
                'label': 'Turn Off Payload Casting Mechanism'
            },
            {
                'name': 'no_escape',
                'type': 'checkbox',
                'label': 'Turn Off String Escaping Mechanism'
            },
            {
                'name': 'prefix',
                'type': 'text',
                'label': 'Injection Payload Prefix String',
                'placeholder': '\'); --'
            },
            {
                'name': 'suffix',
                'type': 'text',
                'label': 'Injection Payload Suffix String',
                'placeholder': '-- -'
            },
            {
                'name': 'tamper',
                'type': 'combo',
                'label': 'Use Tamper Scripts',
                'items': [
                    {'label': 'None', 'value': ''},
                    {'label': 'apostrophemask - UTF-8 fullwidth apostrophe', 'value': 'apostrophemask'},
                    {'label': 'base64encode - Base64 encode payload', 'value': 'base64encode'},
                    {'label': 'between - Replace comparison operators', 'value': 'between'},
                    {'label': 'charencode - URL-encode characters', 'value': 'charencode'},
                    {'label': 'equaltolike - Replace equals with LIKE', 'value': 'equaltolike'},
                    {'label': 'randomcase - Random case characters', 'value': 'randomcase'},
                    {'label': 'space2comment - Replace space with comments', 'value': 'space2comment'},
                    {'label': 'space2dash - Replace space with dash comments', 'value': 'space2dash'},
                    {'label': 'space2hash - Replace space with hash comments', 'value': 'space2hash'},
                    {'label': 'space2plus - Replace space with plus', 'value': 'space2plus'},
                    {'label': 'versionedkeywords - MySQL comment keywords', 'value': 'versionedkeywords'},
                    {'label': 'Common: space2comment,randomcase', 'value': 'space2comment,randomcase'},
                    {'label': 'WAF Bypass: apostrophemask,base64encode', 'value': 'apostrophemask,base64encode'},
                    {'label': 'MySQL: space2comment,versionedkeywords', 'value': 'space2comment,versionedkeywords'}
                ]
            },
            {
                'name': 'list_tampers_btn',
                'type': 'button',
                'label': 'Show All Available Tamper Scripts',
                'button_text': 'List Tampers',
                'action': 'show_available_tampers'
            },
            {
                'name': 'tamper_custom',
                'type': 'text',
                'label': 'Custom Tamper Scripts (comma-separated)',
                'placeholder': 'e.g., space2comment,randomcase,charencode'
            }
        ]
        
        return OptionGroup("Injection Options", injection_options, self.mutual_exclusion_manager)
    
    def create_payload_group(self) -> QGroupBox:
        """Create payload customization options"""
        payload_options = [
            {
                'name': 'prefix',
                'type': 'text',
                'label': 'Payload Prefix',
                'placeholder': "'"
            },
            {
                'name': 'suffix',
                'type': 'text',
                'label': 'Payload Suffix',
                'placeholder': "'"
            }
        ]
        
        return OptionGroup("Payload Customization", payload_options, self.mutual_exclusion_manager)
    
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
    
    def validate_options(self) -> Dict[str, Any]:
        """Validate current options"""
        options = self.get_options()
        errors = []
        
        # Check level and risk values
        level = options.get('level', 1)
        risk = options.get('risk', 1)
        
        if level > 3:
            errors.append("Warning: High test level may generate excessive requests")
        
        if risk > 2:
            errors.append("Warning: High risk level may perform destructive tests")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'options': options
        }
    
    def show_available_tampers(self):
        """Show all available tamper scripts using SQLmap --list-tampers"""
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QProgressBar, QLabel
        from PyQt6.QtCore import QThread, pyqtSignal
        import subprocess
        
        class TamperListThread(QThread):
            """Thread to get tamper scripts list"""
            finished_signal = pyqtSignal(str)
            error_signal = pyqtSignal(str)
            
            def run(self):
                try:
                    # Run sqlmap --list-tampers
                    result = subprocess.run(['sqlmap', '--list-tampers'], 
                                          capture_output=True, text=True, timeout=30)
                    if result.returncode == 0:
                        self.finished_signal.emit(result.stdout)
                    else:
                        self.error_signal.emit(f"Error: {result.stderr}")
                except subprocess.TimeoutExpired:
                    self.error_signal.emit("Timeout: SQLmap took too long to respond")
                except Exception as e:
                    self.error_signal.emit(f"Error executing SQLmap: {str(e)}")
        
        # Create dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Available Tamper Scripts")
        dialog.setMinimumSize(800, 600)
        
        layout = QVBoxLayout()
        
        # Status label
        status_label = QLabel("Loading tamper scripts...")
        layout.addWidget(status_label)
        
        # Progress bar
        progress = QProgressBar()
        progress.setRange(0, 0)  # Indeterminate
        layout.addWidget(progress)
        
        # Text area for results
        text_area = QTextEdit()
        text_area.setReadOnly(True)
        text_area.hide()  # Hide initially
        layout.addWidget(text_area)
        
        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.close)
        layout.addWidget(close_button)
        
        dialog.setLayout(layout)
        
        # Thread to get tamper scripts
        thread = TamperListThread()
        
        def on_finished(output):
            progress.hide()
            status_label.hide()
            text_area.show()
            text_area.setPlainText(output)
            
        def on_error(error_msg):
            progress.hide()
            status_label.setText(f"Error: {error_msg}")
            
        thread.finished_signal.connect(on_finished)
        thread.error_signal.connect(on_error)
        thread.start()
        
        dialog.exec()
