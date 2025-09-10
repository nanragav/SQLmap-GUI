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
        session_group = QGroupBox("Session and Output")
        session_layout = QVBoxLayout(session_group)
        
        # Session file
        session_file_layout = QHBoxLayout()
        self.session_file = QLineEdit()
        self.session_file.setPlaceholderText("Load session from a stored (.sqlite) file")
        self.session_file.setToolTip("Load session from a stored (.sqlite) file (-s)")
        browse_session_btn = QPushButton("Browse")
        browse_session_btn.clicked.connect(lambda: self.browse_file(self.session_file, "SQLite files (*.sqlite);;All files (*.*)"))
        session_file_layout.addWidget(QLabel("Session file:"))
        session_file_layout.addWidget(self.session_file)
        session_file_layout.addWidget(browse_session_btn)
        session_layout.addLayout(session_file_layout)
        
        # Traffic file
        traffic_file_layout = QHBoxLayout()
        self.traffic_file = QLineEdit()
        self.traffic_file.setPlaceholderText("Log all HTTP traffic into a textual file")
        self.traffic_file.setToolTip("Log all HTTP traffic into a textual file (-t)")
        browse_traffic_btn = QPushButton("Browse")
        browse_traffic_btn.clicked.connect(lambda: self.browse_save_file(self.traffic_file, "Text files (*.txt);;All files (*.*)"))
        traffic_file_layout.addWidget(QLabel("Traffic file:"))
        traffic_file_layout.addWidget(self.traffic_file)
        traffic_file_layout.addWidget(browse_traffic_btn)
        session_layout.addLayout(traffic_file_layout)
        
        # Output directory
        output_dir_layout = QHBoxLayout()
        self.output_dir = QLineEdit()
        self.output_dir.setPlaceholderText("Custom output directory path")
        self.output_dir.setToolTip("Custom output directory path (--output-dir)")
        browse_output_btn = QPushButton("Browse")
        browse_output_btn.clicked.connect(lambda: self.browse_directory(self.output_dir))
        output_dir_layout.addWidget(QLabel("Output directory:"))
        output_dir_layout.addWidget(self.output_dir)
        output_dir_layout.addWidget(browse_output_btn)
        session_layout.addLayout(output_dir_layout)
        
        layout.addWidget(session_group)
        
        # Behavior options
        behavior_group = QGroupBox("Behavior Options")
        behavior_layout = QVBoxLayout(behavior_group)
        
        self.batch = QCheckBox("Never ask for user input, use default behavior")
        self.batch.setToolTip("Never ask for user input, use the default behavior (--batch)")
        behavior_layout.addWidget(self.batch)
        
        self.abort_on_empty = QCheckBox("Abort data retrieval on empty results")
        self.abort_on_empty.setToolTip("Abort data retrieval on empty results (--abort-on-empty)")
        behavior_layout.addWidget(self.abort_on_empty)
        
        self.flush_session = QCheckBox("Flush session files for current target")
        self.flush_session.setToolTip("Flush session files for current target (--flush-session)")
        behavior_layout.addWidget(self.flush_session)
        
        self.fresh_queries = QCheckBox("Ignore query results stored in session file")
        self.fresh_queries.setToolTip("Ignore query results stored in session file (--fresh-queries)")
        behavior_layout.addWidget(self.fresh_queries)
        
        self.cleanup = QCheckBox("Clean up the DBMS from sqlmap specific UDF and tables")
        self.cleanup.setToolTip("Clean up the DBMS from sqlmap specific UDF and tables (--cleanup)")
        behavior_layout.addWidget(self.cleanup)
        
        # Answers field
        answers_layout = QHBoxLayout()
        self.answers = QLineEdit()
        self.answers.setPlaceholderText('Set predefined answers (e.g. "quit=N,follow=N")')
        self.answers.setToolTip('Set predefined answers (e.g. "quit=N,follow=N") (--answers)')
        answers_layout.addWidget(QLabel("Answers:"))
        answers_layout.addWidget(self.answers)
        behavior_layout.addLayout(answers_layout)
        
        layout.addWidget(behavior_group)
        
        # Crawling options
        crawl_group = QGroupBox("Crawling Options")
        crawl_layout = QVBoxLayout(crawl_group)
        
        self.forms = QCheckBox("Parse and test forms on target URL")
        self.forms.setToolTip("Parse and test forms on target URL (--forms)")
        crawl_layout.addWidget(self.forms)
        
        # Crawl depth
        crawl_layout_h = QHBoxLayout()
        self.crawl = QSpinBox()
        self.crawl.setRange(0, 10)
        self.crawl.setToolTip("Crawl the website starting from the target URL (--crawl)")
        crawl_layout_h.addWidget(QLabel("Crawl depth:"))
        crawl_layout_h.addWidget(self.crawl)
        crawl_layout.addLayout(crawl_layout_h)
        
        layout.addWidget(crawl_group)
        
        # Advanced options
        advanced_group = QGroupBox("Advanced Options")
        advanced_layout = QVBoxLayout(advanced_group)
        
        # Charset
        charset_layout = QHBoxLayout()
        self.charset = QLineEdit()
        self.charset.setPlaceholderText('Blind SQL injection charset (e.g. "0123456789abcdef")')
        self.charset.setToolTip('Blind SQL injection charset (e.g. "0123456789abcdef") (--charset)')
        charset_layout.addWidget(QLabel("Charset:"))
        charset_layout.addWidget(self.charset)
        advanced_layout.addLayout(charset_layout)
        
        # Encoding
        encoding_layout = QHBoxLayout()
        self.encoding = QLineEdit()
        self.encoding.setPlaceholderText("Character encoding used for data retrieval (e.g. GBK)")
        self.encoding.setToolTip("Character encoding used for data retrieval (e.g. GBK) (--encoding)")
        encoding_layout.addWidget(QLabel("Encoding:"))
        encoding_layout.addWidget(self.encoding)
        advanced_layout.addLayout(encoding_layout)
        
        # Base64 parameter
        base64_layout = QHBoxLayout()
        self.base64 = QLineEdit()
        self.base64.setPlaceholderText("Parameter(s) containing Base64 encoded data")
        self.base64.setToolTip("Parameter(s) containing Base64 encoded data (--base64)")
        base64_layout.addWidget(QLabel("Base64 param:"))
        base64_layout.addWidget(self.base64)
        advanced_layout.addLayout(base64_layout)
        
        # URL and filename safe Base64 alphabet
        self.base64_safe = QCheckBox("Use URL and filename safe Base64 alphabet (RFC 4648)")
        self.base64_safe.setToolTip("Use URL and filename safe Base64 alphabet (RFC 4648) (--base64-safe)")
        advanced_layout.addWidget(self.base64_safe)
        
        layout.addWidget(advanced_group)
        
        layout.addStretch()
        
        scroll_content.setLayout(layout)
        scroll_area.setWidget(scroll_content)
        
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        
        # Connect signals
        self.connect_signals()
    
    def browse_file(self, line_edit, file_filter="All files (*.*)"):
        """Browse for a file to open"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", file_filter)
        if file_path:
            line_edit.setText(file_path)
    
    def browse_save_file(self, line_edit, file_filter="All files (*.*)"):
        """Browse for a file to save"""
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", file_filter)
        if file_path:
            line_edit.setText(file_path)
    
    def browse_directory(self, line_edit):
        """Browse for a directory"""
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dir_path:
            line_edit.setText(dir_path)
    
    def connect_signals(self):
        """Connect all widget signals"""
        # Session and output
        self.session_file.textChanged.connect(self.options_changed)
        self.traffic_file.textChanged.connect(self.options_changed)
        self.output_dir.textChanged.connect(self.options_changed)
        
        # Behavior
        self.batch.toggled.connect(self.options_changed)
        self.abort_on_empty.toggled.connect(self.options_changed)
        self.flush_session.toggled.connect(self.options_changed)
        self.fresh_queries.toggled.connect(self.options_changed)
        self.cleanup.toggled.connect(self.options_changed)
        self.answers.textChanged.connect(self.options_changed)
        
        # Crawling
        self.forms.toggled.connect(self.options_changed)
        self.crawl.valueChanged.connect(self.options_changed)
        
        # Advanced
        self.charset.textChanged.connect(self.options_changed)
        self.encoding.textChanged.connect(self.options_changed)
        self.base64.textChanged.connect(self.options_changed)
    
    def get_options(self) -> Dict[str, Any]:
        """Get all general options"""
        options = {}
        
        # Session and output
        if self.session_file.text().strip():
            options['session_file'] = self.session_file.text().strip()
        if self.traffic_file.text().strip():
            options['traffic_file'] = self.traffic_file.text().strip()
        if self.output_dir.text().strip():
            options['output_dir'] = self.output_dir.text().strip()
        
        # Behavior
        if self.batch.isChecked():
            options['batch'] = True
        if self.abort_on_empty.isChecked():
            options['abort_on_empty'] = True
        if self.flush_session.isChecked():
            options['flush_session'] = True
        if self.fresh_queries.isChecked():
            options['fresh_queries'] = True
        if self.cleanup.isChecked():
            options['cleanup'] = True
        if self.answers.text().strip():
            options['answers'] = self.answers.text().strip()
        
        # Crawling
        if self.forms.isChecked():
            options['forms'] = True
        if self.crawl.value() > 0:
            options['crawl'] = self.crawl.value()
        
        # Advanced
        if self.charset.text().strip():
            options['charset'] = self.charset.text().strip()
        if self.encoding.text().strip():
            options['encoding'] = self.encoding.text().strip()
        if self.base64.text().strip():
            options['base64'] = self.base64.text().strip()
        
        return options
    
    def set_options(self, options: Dict[str, Any]):
        """Set options from dictionary"""
        # Session and output
        self.session_file.setText(options.get('session_file', ''))
        self.traffic_file.setText(options.get('traffic_file', ''))
        self.output_dir.setText(options.get('output_dir', ''))
        
        # Behavior
        self.batch.setChecked(options.get('batch', False))
        self.abort_on_empty.setChecked(options.get('abort_on_empty', False))
        self.flush_session.setChecked(options.get('flush_session', False))
        self.fresh_queries.setChecked(options.get('fresh_queries', False))
        self.cleanup.setChecked(options.get('cleanup', False))
        self.answers.setText(options.get('answers', ''))
        
        # Crawling
        self.forms.setChecked(options.get('forms', False))
        self.crawl.setValue(options.get('crawl', 0))
        
        # Advanced
        self.charset.setText(options.get('charset', ''))
        self.encoding.setText(options.get('encoding', ''))
        self.base64.setText(options.get('base64', ''))
    
    def reset_options(self):
        """Reset all options to defaults"""
        # Session and output
        self.session_file.clear()
        self.traffic_file.clear()
        self.output_dir.clear()
        
        # Behavior
        self.batch.setChecked(False)
        self.abort_on_empty.setChecked(False)
        self.flush_session.setChecked(False)
        self.fresh_queries.setChecked(False)
        self.cleanup.setChecked(False)
        self.answers.clear()
        
        # Crawling
        self.forms.setChecked(False)
        self.crawl.setValue(0)
        
        # Advanced
        self.charset.clear()
        self.encoding.clear()
        self.base64.clear()
        self.base64_safe.setChecked(False)
    
    def create_session_group(self) -> QGroupBox:
        """Create session and traffic options"""
        session_options = [
            {
                'name': 'flush_session',
                'type': 'checkbox',
                'label': 'Flush Session Files for Current Target'
            },
            {
                'name': 'fresh_queries',
                'type': 'checkbox',
                'label': 'Ignore Query Results Stored in Session File'
            },
            {
                'name': 'har',
                'type': 'file',
                'label': 'Log All HTTP Traffic into HAR File',
                'filter': 'HAR Files (*.har);;All Files (*)'
            },
            {
                'name': 'save',
                'type': 'text',
                'label': 'Save Options to Configuration INI File',
                'placeholder': 'config.ini'
            },
            {
                'name': 'session_file',
                'type': 'file',
                'label': 'Load Session from Stored File',
                'filter': 'Session Files (*.sqlite);;All Files (*)'
            },
            {
                'name': 'traffic_file',
                'type': 'file',
                'label': 'Log All HTTP Traffic into File',
                'filter': 'Text Files (*.txt);;All Files (*)'
            }
        ]
        
        return OptionGroup("Session & Traffic", session_options, self.mutual_exclusion_manager)
    
    def create_misc_group(self) -> QGroupBox:
        """Create miscellaneous options"""
        misc_options = [
            {
                'name': 'beep',
                'type': 'checkbox',
                'label': 'Beep on Question and/or When Vulnerability Found'
            },
            {
                'name': 'dependencies',
                'type': 'checkbox',
                'label': 'Check for Missing Dependencies'
            },
            {
                'name': 'disable_coloring',
                'type': 'checkbox',
                'label': 'Disable Console Output Coloring'
            },
            {
                'name': 'offline',
                'type': 'checkbox',
                'label': 'Work in Offline Mode (Only Use Session Data)'
            },
            {
                'name': 'shell',
                'type': 'checkbox',
                'label': 'Prompt for Interactive Shell'
            },
            {
                'name': 'update',
                'type': 'checkbox',
                'label': 'Update SQLmap'
            },
            {
                'name': 'wizard',
                'type': 'checkbox',
                'label': 'Simple Wizard Interface for Beginner Users'
            }
        ]
        
        return OptionGroup("Miscellaneous", misc_options, self.mutual_exclusion_manager)
    
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

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

