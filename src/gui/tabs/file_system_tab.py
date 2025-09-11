"""
File System Tab - File system access options
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QGroupBox,
    QCheckBox, QLineEdit, QPushButton, QFileDialog, QTextEdit, QComboBox
)
from PyQt6.QtCore import pyqtSignal
from typing import Dict, Any

from ..widgets.custom_widgets import OptionGroup
from .base_tab import BaseTab


class FileSystemTab(BaseTab):
    """File system access tab"""
    
    def __init__(self, parent=None, mutual_exclusion_manager=None):
        super().__init__(parent, mutual_exclusion_manager)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # File read options
        read_group = QGroupBox("File Read")
        read_layout = QFormLayout(read_group)
        
        self.file_read = QLineEdit()
        self.file_read.setPlaceholderText("Path to file to read from back-end DBMS")
        self.file_read.setToolTip("Read a file from the back-end DBMS file system (--file-read)")
        browse_read_btn = QPushButton("Browse")
        browse_read_btn.clicked.connect(lambda: self.set_file_path(self.file_read))
        read_layout_h = QHBoxLayout()
        read_layout_h.addWidget(self.file_read)
        read_layout_h.addWidget(browse_read_btn)
        read_layout.addRow("File to read:", read_layout_h)
        
        layout.addWidget(read_group)
        
        # File write options
        write_group = QGroupBox("File Write")
        write_layout = QFormLayout(write_group)
        
        self.file_write = QLineEdit()
        self.file_write.setPlaceholderText("Local file to write to back-end DBMS")
        self.file_write.setToolTip("Write a local file to the back-end DBMS file system (--file-write)")
        browse_write_btn = QPushButton("Browse")
        browse_write_btn.clicked.connect(lambda: self.browse_local_file(self.file_write))
        write_layout_h = QHBoxLayout()
        write_layout_h.addWidget(self.file_write)
        write_layout_h.addWidget(browse_write_btn)
        write_layout.addRow("Local file:", write_layout_h)
        
        self.file_dest = QLineEdit()
        self.file_dest.setPlaceholderText("Destination path on back-end DBMS")
        self.file_dest.setToolTip("Back-end DBMS absolute filepath to write to (--file-dest)")
        write_layout.addRow("Destination:", self.file_dest)
        
        layout.addWidget(write_group)
        
        # File upload options - REMOVED (empty section)
        # upload_group = QGroupBox("File Upload")
        # upload_layout = QFormLayout(upload_group)
        # layout.addWidget(upload_group)
        
        # File permissions - REMOVED (empty section)
        # perms_group = QGroupBox("File Permissions")
        # perms_layout = QFormLayout(perms_group)
        # layout.addWidget(perms_group)
        
        # Advanced options - REMOVED (empty section)
        # advanced_group = QGroupBox("Advanced Options")
        # advanced_layout = QFormLayout(advanced_group)
        # layout.addWidget(advanced_group)
        
        # File content preview
        preview_group = QGroupBox("File Content Preview")
        preview_layout = QVBoxLayout(preview_group)
        
        self.content_preview = QTextEdit()
        self.content_preview.setReadOnly(True)
        self.content_preview.setMaximumHeight(150)
        self.content_preview.setPlaceholderText("File content will be displayed here when read...")
        preview_layout.addWidget(self.content_preview)
        
        layout.addWidget(preview_group)
        
        # Information section
        info_group = QGroupBox("Information")
        info_layout = QVBoxLayout(info_group)
        
        info_text = QLabel("""
<b>File System Access:</b><br>
• <b>File Read:</b> Read files from the database server's file system<br>
• <b>File Write:</b> Upload and write files to the database server<br>
• Requires appropriate database privileges (FILE privilege)<br>
• <b>Warning:</b> Use only on authorized systems<br><br>
<b>Supported Databases:</b> MySQL, PostgreSQL, SQL Server, Oracle
        """)
        info_text.setWordWrap(True)
        info_text.setStyleSheet("QLabel { color: #666; font-size: 10pt; }")
        info_layout.addWidget(info_text)
        
        layout.addWidget(info_group)
        
        layout.addStretch()
        
        # Connect signals
        self.connect_signals()
    
    def browse_local_file(self, line_edit):
        """Browse for local file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Local File", "", "All files (*.*)"
        )
        if file_path:
            line_edit.setText(file_path)
    
    def set_file_path(self, line_edit):
        """Set remote file path"""
        # This could be enhanced with a dialog for common paths
        from PyQt6.QtWidgets import QInputDialog
        path, ok = QInputDialog.getText(
            self, "Remote File Path", 
            "Enter the remote file path:",
            text=line_edit.text()
        )
        if ok and path:
            line_edit.setText(path)
    
    def connect_signals(self):
        """Connect widget signals"""
        self.file_read.textChanged.connect(self.options_changed)
        self.file_write.textChanged.connect(self.options_changed)
        self.file_dest.textChanged.connect(self.options_changed)
    
    def get_options(self):
        """Get file system options"""
        options = {}
        
        if self.file_read.text().strip():
            options['file_read'] = self.file_read.text().strip()
        
        if self.file_write.text().strip():
            options['file_write'] = self.file_write.text().strip()
        
        if self.file_dest.text().strip():
            options['file_dest'] = self.file_dest.text().strip()
        
        return options
    
    def set_options(self, options):
        """Set file system options"""
        self.file_read.setText(options.get('file_read', ''))
        self.file_write.setText(options.get('file_write', ''))
        self.file_dest.setText(options.get('file_dest', ''))
    
    def reset_options(self):
        """Reset file system options to defaults"""
        self.file_read.clear()
        self.file_write.clear()
        self.file_dest.clear()
        self.content_preview.clear()
