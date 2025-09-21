"""
General Tab - General SQLmap options
Handles verbosity, output, session, and other general settings
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                            QCheckBox, QComboBox, QSpinBox, QTextEdit, QGroupBox,
                            QScrollArea, QPushButton, QFileDialog, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from typing import Dict, Any

from ..widgets.custom_widgets import OptionGroup, ValidatedLineEdit


class GeneralTab(QWidget):
    """Tab for general SQLmap options"""
    
    options_changed = pyqtSignal()
    
    def __init__(self, parent=None, mutual_exclusion_manager=None):
        super().__init__(parent)
        self.mutual_exclusion_manager = mutual_exclusion_manager
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the general tab UI"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        
        layout = QVBoxLayout()
        
        # Session and output options
        session_group = self.create_session_group()
        layout.addWidget(session_group)
        
        # Behavior options
        behavior_group = self.create_behavior_group()
        layout.addWidget(behavior_group)
        
        # Crawling options
        crawl_group = self.create_crawl_group()
        layout.addWidget(crawl_group)
        
        # Advanced options
        advanced_group = self.create_advanced_group()
        layout.addWidget(advanced_group)
        
        layout.addStretch()
        scroll_content.setLayout(layout)
        scroll_area.setWidget(scroll_content)
        
        tab_layout = QVBoxLayout()
        tab_layout.addWidget(scroll_area)
        self.setLayout(tab_layout)
    
    def create_session_group(self) -> QGroupBox:
        """Create session and output options"""
        session_options = [
            {
                'name': 'session_file',
                'type': 'file',
                'label': 'Load Session from Stored File',
                'filter': 'Session Files (*.sqlite);;All Files (*)',
                'tooltip': 'Load session from a stored (.sqlite) file (-s SESSIONFILE or --session=SESSIONFILE)'
            },
            {
                'name': 'traffic_file',
                'type': 'file',
                'label': 'Log All HTTP Traffic into File',
                'filter': 'Text Files (*.txt);;All Files (*)',
                'tooltip': 'Log all HTTP traffic into a textual file (--traffic-file=FILE)'
            },
            {
                'name': 'output_dir',
                'type': 'directory',
                'label': 'Custom Output Directory Path',
                'tooltip': 'Custom output directory path (-o DIR or --output-dir=DIR)'
            }
        ]
        
        return OptionGroup("Session and Output", session_options, self.mutual_exclusion_manager)
    
    def create_behavior_group(self) -> QGroupBox:
        """Create behavior options"""
        behavior_options = [
            {
                'name': 'verbose',
                'type': 'number',
                'label': 'Verbosity Level',
                'min': 0,
                'max': 6,
                'default': 1,
                'tooltip': 'Verbosity level: 0-6 (default 1) (-v VERBOSE)'
            },
            {
                'name': 'batch',
                'type': 'checkbox',
                'label': 'Never Ask for User Input, Use Default Behavior',
                'tooltip': 'Never ask for user input, use the default behavior (--batch)'
            },
            {
                'name': 'abort_on_empty',
                'type': 'checkbox',
                'label': 'Abort Data Retrieval on Empty Results',
                'tooltip': 'Abort data retrieval on empty results (--abort-on-empty)'
            },
            {
                'name': 'fresh_queries',
                'type': 'checkbox',
                'label': 'Ignore Query Results Stored in Session File',
                'tooltip': 'Ignore query results stored in session file (--fresh-queries)'
            },
            {
                'name': 'cleanup',
                'type': 'checkbox',
                'label': 'Clean Up the DBMS from SQLmap Specific UDF and Tables',
                'tooltip': 'Clean up the DBMS from sqlmap specific UDF and tables (--cleanup)'
            },
            {
                'name': 'answers',
                'type': 'text',
                'label': 'Set Predefined Answers',
                'placeholder': 'e.g. "quit=N,follow=N"',
                'tooltip': 'Set predefined answers (e.g. "quit=N,follow=N") (--answers=ANSWERS)'
            }
        ]
        
        return OptionGroup("Behavior Options", behavior_options, self.mutual_exclusion_manager)
    
    def create_crawl_group(self) -> QGroupBox:
        """Create crawling options"""
        crawl_options = [
            {
                'name': 'forms',
                'type': 'checkbox',
                'label': 'Parse and Test Forms on Target URL',
                'tooltip': 'Parse and test forms on target URL (--forms)'
            },
            {
                'name': 'crawl',
                'type': 'number',
                'label': 'Crawl Depth',
                'min': 0,
                'max': 10,
                'default': 0,
                'tooltip': 'Crawl the website starting from the target URL (--crawl=CRAWLDEPTH)'
            },
            {
                'name': 'crawl_exclude',
                'type': 'text',
                'label': 'Regexp to Exclude Pages from Crawling',
                'placeholder': 'e.g. "logout"',
                'tooltip': 'Regexp to exclude pages from crawling (--crawl-exclude=REGEXP)'
            }
        ]
        
        return OptionGroup("Crawling Options", crawl_options, self.mutual_exclusion_manager)
    
    def create_advanced_group(self) -> QGroupBox:
        """Create advanced options"""
        advanced_options = [
            {
                'name': 'web_root',
                'type': 'text',
                'label': 'Web Server Document Root Directory',
                'placeholder': '/var/www/html',
                'tooltip': 'Web server document root directory (--web-root=WEBROOT)'
            }
        ]
        
        return OptionGroup("Advanced Options", advanced_options, self.mutual_exclusion_manager)
    
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

