"""
Enumeration Tab - Database enumeration options
Handles database, table, column, and data extraction options
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                            QCheckBox, QComboBox, QSpinBox, QTextEdit, QGroupBox,
                            QScrollArea, QPushButton, QFileDialog, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import Dict, Any

from ..widgets.custom_widgets import OptionGroup, ValidatedLineEdit


class EnumerationTab(QWidget):
    """Tab for database enumeration options"""
    
    options_changed = pyqtSignal()
    
    def __init__(self, parent=None, mutual_exclusion_manager=None):
        super().__init__(parent)
        self.mutual_exclusion_manager = mutual_exclusion_manager
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the enumeration tab UI"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        
        layout = QVBoxLayout()
        
        # Basic enumeration group
        basic_group = self.create_basic_group()
        layout.addWidget(basic_group)
        
        # Database structure group
        structure_group = self.create_structure_group()
        layout.addWidget(structure_group)
        
        # Data extraction group
        data_group = self.create_data_group()
        layout.addWidget(data_group)
        
        # Advanced enumeration group
        advanced_group = self.create_advanced_group()
        layout.addWidget(advanced_group)
        
        layout.addStretch()
        scroll_content.setLayout(layout)
        scroll_area.setWidget(scroll_content)
        
        tab_layout = QVBoxLayout()
        tab_layout.addWidget(scroll_area)
        self.setLayout(tab_layout)
    
    def create_basic_group(self) -> QGroupBox:
        """Create basic enumeration options"""
        basic_options = [
            {
                'name': 'all',
                'type': 'checkbox',
                'label': 'Retrieve Everything'
            },
            {
                'name': 'banner',
                'type': 'checkbox',
                'label': 'Retrieve DBMS Banner'
            },
            {
                'name': 'current_user',
                'type': 'checkbox',
                'label': 'Retrieve DBMS Current User'
            },
            {
                'name': 'current_db',
                'type': 'checkbox',
                'label': 'Retrieve DBMS Current Database'
            },
            {
                'name': 'hostname',
                'type': 'checkbox',
                'label': 'Retrieve DBMS Server Hostname'
            },
            {
                'name': 'is_dba',
                'type': 'checkbox',
                'label': 'Detect if Current User is DBA'
            },
            {
                'name': 'users',
                'type': 'checkbox',
                'label': 'Enumerate DBMS Users'
            },
            {
                'name': 'passwords',
                'type': 'checkbox',
                'label': 'Enumerate DBMS Users Password Hashes'
            },
            {
                'name': 'privileges',
                'type': 'checkbox',
                'label': 'Enumerate DBMS Users Privileges'
            },
            {
                'name': 'roles',
                'type': 'checkbox',
                'label': 'Enumerate DBMS Users Roles'
            },
            {
                'name': 'dbs',
                'type': 'checkbox',
                'label': 'Enumerate DBMS Databases'
            }
        ]
        
        return OptionGroup("Basic Enumeration", basic_options, self.mutual_exclusion_manager)
    
    def create_structure_group(self) -> QGroupBox:
        """Create database structure enumeration options"""
        structure_options = [
            {
                'name': 'tables',
                'type': 'checkbox',
                'label': 'Enumerate DBMS Database Tables'
            },
            {
                'name': 'columns',
                'type': 'checkbox',
                'label': 'Enumerate DBMS Database Table Columns'
            },
            {
                'name': 'schema',
                'type': 'checkbox',
                'label': 'Enumerate DBMS Schema'
            },
            {
                'name': 'count',
                'type': 'checkbox',
                'label': 'Retrieve Number of Entries for Tables'
            },
            {
                'name': 'dump',
                'type': 'checkbox',
                'label': 'Dump DBMS Database Table Entries'
            },
            {
                'name': 'dump_all',
                'type': 'checkbox',
                'label': 'Dump All DBMS Databases Tables Entries'
            },
            {
                'name': 'search',
                'type': 'checkbox',
                'label': 'Search Column(s), Table(s) and/or Database Name(s)'
            },
            {
                'name': 'comments',
                'type': 'checkbox',
                'label': 'Check for DBMS Comments During Enumeration'
            },
            {
                'name': 'statements',
                'type': 'checkbox',
                'label': 'Retrieve SQL Statements Being Run on DBMS'
            }
        ]
        
        return OptionGroup("Database Structure", structure_options, self.mutual_exclusion_manager)
    
    def create_data_group(self) -> QGroupBox:
        """Create data extraction options"""
        data_options = [
            {
                'name': 'db',
                'type': 'text',
                'label': 'DBMS Database to Enumerate',
                'placeholder': 'database_name'
            },
            {
                'name': 'tbl',
                'type': 'text',
                'label': 'DBMS Database Table(s) to Enumerate',
                'placeholder': 'table1,table2'
            },
            {
                'name': 'col',
                'type': 'text',
                'label': 'DBMS Database Table Column(s) to Enumerate',
                'placeholder': 'column1,column2'
            },
            {
                'name': 'user',
                'type': 'text',
                'label': 'DBMS User to Enumerate',
                'placeholder': 'username'
            },
            {
                'name': 'where',
                'type': 'text',
                'label': 'Use WHERE Condition While Dumping',
                'placeholder': 'id>100'
            },
            {
                'name': 'start',
                'type': 'number',
                'label': 'First Dump Table Entry to Retrieve',
                'min': 1,
                'max': 999999
            },
            {
                'name': 'stop',
                'type': 'number',
                'label': 'Last Dump Table Entry to Retrieve',
                'min': 1,
                'max': 999999
            },
            {
                'name': 'first',
                'type': 'number',
                'label': 'First Query Output Word Character to Retrieve',
                'min': 1,
                'max': 999999
            },
            {
                'name': 'last',
                'type': 'number',
                'label': 'Last Query Output Word Character to Retrieve',
                'min': 1,
                'max': 999999
            }
        ]
        
        return OptionGroup("Data Extraction", data_options, self.mutual_exclusion_manager)
    
    def create_advanced_group(self) -> QGroupBox:
        """Create advanced enumeration options"""
        advanced_options = [
            {
                'name': 'sql_query',
                'type': 'text',
                'label': 'Run Custom SQL Statement',
                'placeholder': 'SELECT * FROM users WHERE id=1'
            },
            {
                'name': 'sql_shell',
                'type': 'checkbox',
                'label': 'Prompt for Interactive SQL Shell'
            },
            {
                'name': 'sql_file',
                'type': 'file',
                'label': 'Execute SQL Statements from File',
                'filter': 'SQL Files (*.sql);;Text Files (*.txt);;All Files (*)'
            },
            {
                'name': 'common_tables',
                'type': 'checkbox',
                'label': 'Check Existence of Common Tables'
            },
            {
                'name': 'common_columns',
                'type': 'checkbox',
                'label': 'Check Existence of Common Columns'
            },
            {
                'name': 'common_files',
                'type': 'checkbox',
                'label': 'Check Existence of Common Files'
            },
            {
                'name': 'udf_inject',
                'type': 'checkbox',
                'label': 'Inject Custom User-Defined Functions'
            },
            {
                'name': 'shared_lib',
                'type': 'file',
                'label': 'Local Path of Shared Library',
                'filter': 'Library Files (*.so *.dll);;All Files (*)'
            }
        ]
        
        return OptionGroup("Advanced Enumeration", advanced_options, self.mutual_exclusion_manager)
    
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
        
        # Check for conflicting options
        if options.get('dump_all') and (options.get('db') or options.get('tbl')):
            errors.append("Warning: dump-all option will override specific database/table selections")
        
        # Validate range options
        start = options.get('start')
        stop = options.get('stop')
        if start and stop and start > stop:
            errors.append("Start entry number cannot be greater than stop entry number")
        
        first = options.get('first')
        last = options.get('last')
        if first and last and first > last:
            errors.append("First character position cannot be greater than last character position")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'options': options
        }
