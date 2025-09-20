"""
Main Window for SQLmap GUI
Central application window with tabbed interface for all SQLmap options
"""

from PyQt6.QtWidgets import (QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout, 
                            QWidget, QPushButton, QSplitter, QMenuBar, QMenu, 
                            QStatusBar, QMessageBox, QDialog, QTextEdit, QLabel,
                            QGroupBox, QScrollArea, QFrame, QToolBar, QApplication,
                            QInputDialog, QLineEdit)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QTimer
from PyQt6.QtGui import QIcon, QKeySequence, QFont, QAction

import os
import sys
import datetime
import time
import re
from typing import Dict, Any, Optional

# Add parent directories to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.core.sqlmap_wrapper import SqlmapWrapper
from src.core.mutual_exclusion_manager import MutualExclusionManager
from src.utils.config import ConfigManager
from src.gui.widgets.custom_widgets import StatusBar, LogWidget, CollapsibleWidget
from src.gui.tabs.target_tab import TargetTab
from src.gui.tabs.request_tab import RequestTab
from src.gui.tabs.injection_tab import InjectionTab
from src.gui.tabs.detection_tab import DetectionTab
from src.gui.tabs.techniques_tab import TechniquesTab
from src.gui.tabs.fingerprint_tab import FingerprintTab
from src.gui.tabs.enumeration_tab import EnumerationTab
from src.gui.tabs.brute_force_tab import BruteForceTab
from src.gui.tabs.udf_tab import UdfTab
from src.gui.tabs.file_system_tab import FileSystemTab
from src.gui.tabs.os_access_tab import OsAccessTab
from src.gui.tabs.windows_registry_tab import WindowsRegistryTab
from src.gui.tabs.general_tab import GeneralTab
from src.gui.tabs.miscellaneous_tab import MiscellaneousTab
from src.gui.tabs.hidden_switches_tab import HiddenSwitchesTab
from src.gui.dialogs.validation_dialog import CommandValidationDialog


class SqlmapMainWindow(QMainWindow):
    """Main application window"""
    
    # Signals
    scan_started = pyqtSignal()
    scan_finished = pyqtSignal(bool)  # success/failure
    log_message = pyqtSignal(str, str)  # message, type
    
    def __init__(self):
        super().__init__()
        
        # Initialize core components
        self.config_manager = ConfigManager()
        self.sqlmap_wrapper = SqlmapWrapper()  # Fast initialization now
        self.mutual_exclusion_manager = MutualExclusionManager()
        self.current_scan_thread = None
        
        # Initialize UI
        self.setup_ui()
        self.setup_menu_bar()
        self.setup_tool_bar()
        self.setup_connections()
        
        # Load settings
        self.load_settings()
        
        # Show initial message and start async initialization
        self.log_widget.append_log("SQLmap GUI loaded successfully", "success")
        self.log_widget.append_log("Checking SQLmap and Python availability...", "info")
        
        # Start async initialization of SQLmap/Python
        self.start_async_initialization()
    
    def setup_ui(self):
        """Setup the main UI layout"""
        self.setWindowTitle("SQLmap GUI - SQL Injection Testing Tool")
        
        # Get screen size and set appropriate window size
        screen = QApplication.primaryScreen().geometry()
        screen_width = screen.width()
        screen_height = screen.height()
        
        # Calculate optimal window size (80% of screen size, but not larger than 1600x1000)
        optimal_width = min(int(screen_width * 0.8), 1600)
        optimal_height = min(int(screen_height * 0.8), 1000)
        
        # Set minimum size to ensure usability
        min_width = min(1200, optimal_width)
        min_height = min(800, optimal_height)
        
        self.setMinimumSize(min_width, min_height)
        self.resize(optimal_width, optimal_height)
        
        # Center the window on screen
        x = (screen_width - optimal_width) // 2
        y = (screen_height - optimal_height) // 2
        self.move(x, y)
        
        # Make window resizable
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowMaximizeButtonHint)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout - horizontal splitter
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left side - options tabs
        self.create_options_tabs()
        main_splitter.addWidget(self.tab_widget)
        
        # Right side - control panel and log
        right_panel = self.create_right_panel()
        main_splitter.addWidget(right_panel)
        
        # Set splitter proportions based on window size
        left_width = int(optimal_width * 0.6)  # 60% for tabs
        right_width = optimal_width - left_width
        main_splitter.setSizes([left_width, right_width])
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(main_splitter)
        central_widget.setLayout(layout)
        
        # Status bar
        self.status_bar = StatusBar()
        self.statusBar().addPermanentWidget(self.status_bar)
    
    def create_options_tabs(self):
        """Create tabbed interface for all SQLmap options"""
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        
        # Initialize all tabs
        self.tabs = {}
        
        # Target options
        self.tabs['target'] = TargetTab(mutual_exclusion_manager=self.mutual_exclusion_manager)
        self.tab_widget.addTab(self.tabs['target'], "Target")
        
        # Request options
        self.tabs['request'] = RequestTab(mutual_exclusion_manager=self.mutual_exclusion_manager)
        self.tab_widget.addTab(self.tabs['request'], "Request")
        
        # Injection options
        self.tabs['injection'] = InjectionTab(mutual_exclusion_manager=self.mutual_exclusion_manager)
        self.tab_widget.addTab(self.tabs['injection'], "Injection")
        
        # Detection options
        self.tabs['detection'] = DetectionTab(mutual_exclusion_manager=self.mutual_exclusion_manager)
        self.tab_widget.addTab(self.tabs['detection'], "Detection")
        
        # Techniques options
        self.tabs['techniques'] = TechniquesTab(mutual_exclusion_manager=self.mutual_exclusion_manager)
        self.tab_widget.addTab(self.tabs['techniques'], "Techniques")
        
        # Fingerprint options
        self.tabs['fingerprint'] = FingerprintTab(mutual_exclusion_manager=self.mutual_exclusion_manager)
        self.tab_widget.addTab(self.tabs['fingerprint'], "Fingerprint")
        
        # Enumeration options
        self.tabs['enumeration'] = EnumerationTab(mutual_exclusion_manager=self.mutual_exclusion_manager)
        self.tab_widget.addTab(self.tabs['enumeration'], "Enumeration")
        
        # Brute force options
        self.tabs['brute_force'] = BruteForceTab(mutual_exclusion_manager=self.mutual_exclusion_manager)
        self.tab_widget.addTab(self.tabs['brute_force'], "Brute Force")
        
        # UDF injection options
        self.tabs['udf'] = UdfTab(mutual_exclusion_manager=self.mutual_exclusion_manager)
        self.tab_widget.addTab(self.tabs['udf'], "UDF")
        
        # File system options
        self.tabs['file_system'] = FileSystemTab(mutual_exclusion_manager=self.mutual_exclusion_manager)
        self.tab_widget.addTab(self.tabs['file_system'], "File System")
        
        # OS access options
        self.tabs['os_access'] = OsAccessTab(mutual_exclusion_manager=self.mutual_exclusion_manager)
        self.tab_widget.addTab(self.tabs['os_access'], "OS Access")
        
        # Windows registry options
        self.tabs['windows_registry'] = WindowsRegistryTab(mutual_exclusion_manager=self.mutual_exclusion_manager)
        self.tab_widget.addTab(self.tabs['windows_registry'], "Registry")
        
        # General options
        self.tabs['general'] = GeneralTab(mutual_exclusion_manager=self.mutual_exclusion_manager)
        self.tab_widget.addTab(self.tabs['general'], "General")
        
        # Miscellaneous options
        self.tabs['miscellaneous'] = MiscellaneousTab(mutual_exclusion_manager=self.mutual_exclusion_manager)
        self.tab_widget.addTab(self.tabs['miscellaneous'], "Misc")
        
        # Hidden switches (advanced)
        self.tabs['hidden_switches'] = HiddenSwitchesTab(mutual_exclusion_manager=self.mutual_exclusion_manager)
        self.tab_widget.addTab(self.tabs['hidden_switches'], "Advanced")
    
    def create_right_panel(self):
        """Create right panel with controls and log"""
        panel = QWidget()
        layout = QVBoxLayout()
        
        # Control section
        control_group = QGroupBox("Control Panel")
        control_layout = QVBoxLayout()
        
        # Command preview
        command_group = CollapsibleWidget("Command Preview", self.create_command_preview())
        control_layout.addWidget(command_group)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.start_button = QPushButton("Start Scan")
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 11pt;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        
        self.start_sudo_button = QPushButton("Start with Sudo")
        self.start_sudo_button.setStyleSheet("""
            QPushButton {
                background-color: #FF5722;
                color: white;
                border: none;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 11pt;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #E64A19;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        
        self.stop_button = QPushButton("Stop Scan")
        self.stop_button.setEnabled(False)
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 11pt;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        
        self.clear_button = QPushButton("Clear Log")
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #ff9800;
                color: white;
                border: none;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 11pt;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #e68900;
            }
        """)
        
        # Add validate button
        self.validate_button = QPushButton("🔍 Validate Command")
        self.validate_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 11pt;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        
        button_layout.addWidget(self.validate_button)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.start_sudo_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addStretch()
        
        control_layout.addLayout(button_layout)
        control_group.setLayout(control_layout)
        
        # Log section
        log_group = QGroupBox("Execution Log")
        log_layout = QVBoxLayout()
        
        self.log_widget = LogWidget()
        log_layout.addWidget(self.log_widget)
        log_group.setLayout(log_layout)
        
        # Add to panel
        layout.addWidget(control_group)
        layout.addWidget(log_group, 1)  # Give log more space
        
        panel.setLayout(layout)
        return panel
    
    def create_command_preview(self):
        """Create command preview widget"""
        # Create container widget
        preview_widget = QWidget()
        preview_layout = QVBoxLayout(preview_widget)
        preview_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create header with copy button
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(5, 5, 5, 5)
        
        header_label = QLabel("SQLmap Command:")
        header_label.setStyleSheet("font-weight: bold; color: #fff;")
        header_layout.addWidget(header_label)
        
        header_layout.addStretch()
        
        copy_button = QPushButton("📋 Copy Command")
        copy_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
        """)
        copy_button.clicked.connect(self.copy_command_to_clipboard)
        header_layout.addWidget(copy_button)
        
        preview_layout.addLayout(header_layout)
        
        # Create command preview text area
        self.command_preview = QTextEdit()
        self.command_preview.setMinimumHeight(180)
        self.command_preview.setMaximumHeight(300)
        self.command_preview.setReadOnly(True)
        self.command_preview.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self.command_preview.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.command_preview.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Ensure the scroll area doesn't auto-scroll
        self.command_preview.setUndoRedoEnabled(False)
        self.command_preview.document().setDocumentMargin(10)
        self.command_preview.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 2px solid #444;
                border-radius: 5px;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 12pt;
                font-weight: bold;
                padding: 8px;
                selection-background-color: #0066cc;
            }
            QTextEdit:focus {
                border: 2px solid #0078d4;
            }
            QScrollBar:vertical {
                background-color: #2b2b2b;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #555;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #777;
            }
            QScrollBar:horizontal {
                background-color: #2b2b2b;
                height: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:horizontal {
                background-color: #555;
                border-radius: 6px;
                min-width: 20px;
            }
            QScrollBar::handle:horizontal:hover {
                background-color: #777;
            }
        """)
        
        preview_layout.addWidget(self.command_preview)
        
        # Update command preview when options change
        self.update_command_preview()
        
        return preview_widget
    
    def copy_command_to_clipboard(self):
        """Copy the current SQLmap command to clipboard"""
        try:
            command_text = self.command_preview.toPlainText()
            if command_text.strip():
                clipboard = QApplication.clipboard()
                clipboard.setText(command_text)
                self.status_bar.set_status("Command copied to clipboard")
                self.log_widget.append_log("SQLmap command copied to clipboard", "info")
            else:
                self.status_bar.set_status("No command to copy")
        except Exception as e:
            self.log_widget.append_log(f"Failed to copy command: {str(e)}", "error")
    
    def get_sudo_password(self):
        """Get sudo password from user"""
        password, ok = QInputDialog.getText(
            self, 
            'Sudo Password Required', 
            'Enter your sudo password:',
            QLineEdit.EchoMode.Password
        )
        
        if ok and password:
            return password.strip()
        return None
    
    def setup_menu_bar(self):
        """Setup application menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        new_action = QAction("New Profile", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self.new_profile)
        file_menu.addAction(new_action)
        
        open_action = QAction("Open Profile", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self.open_profile)
        file_menu.addAction(open_action)
        
        save_action = QAction("Save Profile", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self.save_profile)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("Save Profile As...", self)
        save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        save_as_action.triggered.connect(self.save_profile_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("Tools")
        
        validate_action = QAction("Validate Options", self)
        validate_action.triggered.connect(self.validate_options)
        tools_menu.addAction(validate_action)
        
        reset_action = QAction("Reset All Options", self)
        reset_action.triggered.connect(self.reset_options)
        tools_menu.addAction(reset_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        debug_action = QAction("Debug Tabs", self)
        debug_action.setShortcut(QKeySequence("Ctrl+D"))
        debug_action.triggered.connect(self.debug_tabs)
        help_menu.addAction(debug_action)
        
        # Add CPU monitoring debug action
        cpu_debug_action = QAction("Debug CPU Monitoring", self)
        cpu_debug_action.triggered.connect(self.debug_cpu_monitoring)
        help_menu.addAction(cpu_debug_action)
        
        # Add performance control actions
        help_menu.addSeparator()
        
        performance_menu = help_menu.addMenu("Performance")
        
        self.high_perf_action = QAction("High Performance Mode", self)
        self.high_perf_action.setCheckable(True)
        self.high_perf_action.setChecked(False)
        self.high_perf_action.triggered.connect(self.toggle_performance_mode)
        performance_menu.addAction(self.high_perf_action)
        
        pause_monitoring_action = QAction("Pause Resource Monitoring", self)
        pause_monitoring_action.triggered.connect(self.pause_resource_monitoring)
        performance_menu.addAction(pause_monitoring_action)
        
        resume_monitoring_action = QAction("Resume Resource Monitoring", self)
        resume_monitoring_action.triggered.connect(self.resume_resource_monitoring)
        performance_menu.addAction(resume_monitoring_action)
        
        optimize_action = QAction("Optimize Performance", self)
        optimize_action.triggered.connect(self.optimize_performance)
        performance_menu.addAction(optimize_action)
    
    def setup_tool_bar(self):
        """Setup application toolbar"""
        toolbar = QToolBar()
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.addToolBar(toolbar)

        # Profile actions
        new_action = toolbar.addAction("New Window", self.new_profile)
        new_action.setToolTip("Open a new SQLmap GUI window")

        toolbar.addSeparator()

        open_action = toolbar.addAction("Open", self.open_profile)
        open_action.setToolTip("Load profile from file")

        save_action = toolbar.addAction("Save", self.save_profile)
        save_action.setToolTip("Save current profile to file")

        toolbar.addSeparator()

        # Scan actions
        start_action = toolbar.addAction("Start Scan", lambda: self.start_scan(use_sudo=False))
        start_action.setToolTip("Start SQL injection scan")

        start_sudo_action = toolbar.addAction("Start (Sudo)", lambda: self.start_scan(use_sudo=True))
        start_sudo_action.setToolTip("Start SQL injection scan with sudo")

        stop_action = toolbar.addAction("Stop", self.stop_scan)
        stop_action.setToolTip("Stop current scan")

        toolbar.addSeparator()

        # Utility actions
        validate_action = toolbar.addAction("Validate", self.validate_options)
        validate_action.setToolTip("Validate current options")

        reset_action = toolbar.addAction("Reset", self.reset_options)
        reset_action.setToolTip("Reset all options to defaults")
    
    def setup_connections(self):
        """Setup signal connections"""
        # Button connections
        self.validate_button.clicked.connect(self.show_validation_dialog)
        self.start_button.clicked.connect(lambda: self.start_scan(use_sudo=False))
        self.start_sudo_button.clicked.connect(lambda: self.start_scan(use_sudo=True))
        self.stop_button.clicked.connect(self.stop_scan)
        self.clear_button.clicked.connect(self.log_widget.clear_log)
        
        # Tab change connection to update command preview
        self.tab_widget.currentChanged.connect(self.update_command_preview)
        
        # Connect tab signals for option changes with throttling
        for tab in self.tabs.values():
            if hasattr(tab, 'options_changed'):
                tab.options_changed.connect(self.schedule_command_preview_update)
        
        # Initialize command preview update timer with longer interval
        self.command_timer = QTimer()
        self.command_timer.timeout.connect(self.update_command_preview)
        self.command_timer.setSingleShot(True)  # Only run once when triggered
        
        # Initialize delayed update timer for throttling
        self.delayed_update_timer = QTimer()
        self.delayed_update_timer.timeout.connect(self.trigger_command_preview_update)
        self.delayed_update_timer.setSingleShot(True)
        
        # Flag to track if update is pending
        self.command_preview_update_pending = False
    
    def schedule_command_preview_update(self):
        """Schedule a throttled command preview update"""
        if not self.command_preview_update_pending:
            self.command_preview_update_pending = True
            # Delay update by 500ms to avoid excessive updates during rapid changes
            self.delayed_update_timer.start(500)
    
    def trigger_command_preview_update(self):
        """Trigger the actual command preview update"""
        self.command_preview_update_pending = False
        self.update_command_preview()
    
    def update_command_preview(self):
        """Update the command preview with current options - optimized version"""
        try:
            # Store current scroll position
            scrollbar = self.command_preview.verticalScrollBar()
            scroll_position = scrollbar.value()
            
            # Collect all options from tabs - optimized to avoid unnecessary work
            all_options = {}
            for tab_name, tab in self.tabs.items():
                if hasattr(tab, 'get_options'):
                    try:
                        tab_options = tab.get_options()
                        if tab_options:  # Only add non-empty options
                            all_options.update(tab_options)
                    except Exception as e:
                        # Log error but don't crash the entire update
                        print(f"Error getting options from {tab_name}: {e}")
                        continue
            
            # Build command using wrapper - respect user's batch preference
            command = self.sqlmap_wrapper.build_command(all_options, force_batch=False)
            
            # Display in preview with proper formatting
            formatted_command = ' '.join(command)
            
            # Only update if the command has actually changed
            current_text = self.command_preview.toPlainText()
            if formatted_command != current_text:
                self.command_preview.setPlainText(formatted_command)
            
            # Restore scroll position
            scrollbar.setValue(scroll_position)
            
        except Exception as e:
            error_msg = f"Error building command: {str(e)}"
            current_text = self.command_preview.toPlainText()
            if not current_text.startswith("Error"):
                self.command_preview.setPlainText(error_msg)
    
    def start_scan(self, use_sudo: bool = False):
        """Start SQLmap scan"""
        try:
            # Check if SQLmap is available before starting scan
            if not self.sqlmap_wrapper.sqlmap_available:
                QMessageBox.warning(self, "SQLmap Not Available", 
                                  "SQLmap is not available or initialization is still in progress.\n\n"
                                  "Please ensure SQLmap is installed and try again.")
                return
            
            # Collect options first
            all_options = {}
            for tab_name, tab in self.tabs.items():
                if hasattr(tab, 'get_options'):
                    tab_options = tab.get_options()
                    all_options.update(tab_options)
            
            # Only validate the command, don't execute yet
            validation_result = self.sqlmap_wrapper.validate_options(all_options)
            
            if not validation_result.is_valid:
                # Show validation dialog for errors
                command_list = self.sqlmap_wrapper.build_command(all_options, force_batch=False)
                command_string = ' '.join(command_list)
                
                reply = QMessageBox.critical(self, "Command Validation Failed", 
                                           f"The command has {len(validation_result.errors)} error(s) that must be fixed before execution.\n\n"
                                           f"Would you like to see the detailed validation report?",
                                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                
                if reply == QMessageBox.StandardButton.Yes:
                    dialog = CommandValidationDialog(validation_result, command_string, self)
                    dialog.command_fixed.connect(self.apply_command_fixes)
                    dialog.exec()
                
                return
            
            # If there's already a scan running, stop it first
            if hasattr(self, 'current_scan_thread') and self.current_scan_thread and self.current_scan_thread.isRunning():
                self.current_scan_thread.stop() 
                self.current_scan_thread.wait()
            
            # Get sudo password if needed
            sudo_password = None
            if use_sudo:
                # Check if sudo is actually needed for sqlmap
                reply = QMessageBox.question(self, "Sudo Confirmation", 
                                           "Are you sure you need to run SQLmap with sudo privileges?\n\n"
                                           "SQLmap typically doesn't require sudo unless you're:\n"
                                           "• Accessing privileged system resources\n"
                                           "• Binding to privileged ports (< 1024)\n"
                                           "• Running sqlmap with special system permissions\n\n"
                                           "Using sudo unnecessarily can be a security risk.",
                                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                
                if reply == QMessageBox.StandardButton.Yes:
                    sudo_password, ok = QInputDialog.getText(
                        self, 
                        "Sudo Password", 
                        "Enter sudo password:", 
                        QLineEdit.EchoMode.Password
                    )
                    if not ok or not sudo_password:
                        self.log_widget.append_log("Sudo password not provided - scan cancelled", "warning")
                        return
                else:
                    # User decided not to use sudo
                    use_sudo = False
                    self.log_widget.append_log("Sudo cancelled by user - running without sudo", "info")
            
            # Create and start the scan thread
            self.current_scan_thread = SqlmapScanThread(
                self.sqlmap_wrapper,
                all_options,
                use_sudo,
                sudo_password
            )
            
            # Connect thread signals
            self.current_scan_thread.log_message.connect(self.log_widget.append_log)
            self.current_scan_thread.scan_finished.connect(self.on_scan_finished)
            
            # Update UI state for scan start
            self.start_button.setEnabled(False)
            self.start_sudo_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.status_bar.set_status("Starting scan...")
            
            # Start the thread
            self.current_scan_thread.start()
            
            sudo_text = " with sudo" if use_sudo else ""
            self.log_widget.append_log(f"SQLmap scan thread starting{sudo_text} (command validated)", "success")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start scan: {str(e)}")
            self.log_widget.append_log(f"Failed to start scan: {str(e)}", "error")
            self.on_scan_finished(False)
    
    def stop_scan(self):
        """Stop current scan"""
        if self.current_scan_thread and self.current_scan_thread.isRunning():
            self.current_scan_thread.stop()
            self.log_widget.append_log("Stopping scan...", "warning")
    
    def on_scan_finished(self, success: bool):
        """Handle scan completion"""
        # Update UI state
        self.start_button.setEnabled(True)
        self.start_sudo_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.status_bar.show_progress(False)
        
        if success:
            self.status_bar.set_status("Scan completed successfully")
            self.log_widget.append_log("Scan completed successfully", "success")
        else:
            self.status_bar.set_status("Scan failed or was stopped")
            self.log_widget.append_log("Scan failed or was stopped", "error")
    
    def validate_options(self) -> bool:
        """Validate current options"""
        try:
            # Collect all options
            all_options = {}
            for tab_name, tab in self.tabs.items():
                if hasattr(tab, 'get_options'):
                    tab_options = tab.get_options()
                    all_options.update(tab_options)
            
            # Use sqlmap wrapper to validate (same as validation dialog)
            validation_result = self.sqlmap_wrapper.validate_options(all_options)
            
            if validation_result.is_valid:
                # Build command to show in success message
                command_list = self.sqlmap_wrapper.build_command(all_options, force_batch=False)
                command_string = ' '.join(command_list)
                
                QMessageBox.information(self, "Validation Success", 
                                      f"✅ All options are valid!\n\n"
                                      f"Generated command:\n{command_string}")
                return True
            else:
                # Show comprehensive validation dialog for errors
                command_list = self.sqlmap_wrapper.build_command(all_options, force_batch=False)
                command_string = ' '.join(command_list)
                
                reply = QMessageBox.question(self, "Validation Issues Found", 
                                           f"The command has {len(validation_result.errors)} error(s) and {len(validation_result.warnings)} warning(s).\n\n"
                                           f"Would you like to see the detailed validation report?",
                                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                
                if reply == QMessageBox.StandardButton.Yes:
                    dialog = CommandValidationDialog(validation_result, command_string, self)
                    dialog.command_fixed.connect(self.apply_command_fixes)
                    dialog.exec()
                
                return False
                
        except Exception as e:
            QMessageBox.critical(self, "Validation Error", f"Failed to validate options: {str(e)}")
            return False
    
    def show_validation_dialog(self):
        """Show comprehensive validation dialog"""
        try:
            # Collect all options
            all_options = {}
            for tab_name, tab in self.tabs.items():
                if hasattr(tab, 'get_options'):
                    tab_options = tab.get_options()
                    all_options.update(tab_options)
            
            # Get validation results from wrapper
            validation = self.sqlmap_wrapper.validate_options(all_options)
            
            # Get current command for display
            command_list = self.sqlmap_wrapper.build_command(all_options, force_batch=False)
            command_string = ' '.join(command_list)
            
            # Show validation dialog
            dialog = CommandValidationDialog(validation, command_string, self)
            dialog.command_fixed.connect(self.apply_command_fixes)
            dialog.exec()
            
        except Exception as e:
            QMessageBox.critical(self, "Validation Error", 
                               f"Failed to show validation dialog: {str(e)}")
    
    def apply_command_fixes(self, fixed_command: str):
        """Apply fixes from validation dialog"""
        try:
            # For now, just show the fixed command
            # In a full implementation, this would parse the command back to options
            QMessageBox.information(self, "Command Fixed", 
                                  f"Suggested command:\n\n{fixed_command}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to apply fixes: {str(e)}")
    
    def reset_options(self):
        """Reset all options to defaults"""
        reply = QMessageBox.question(self, "Reset Options",
                                   "Are you sure you want to reset all options to defaults?\n\n"
                                   "This will clear all current settings and restore default values.",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            try:
                reset_count = 0
                error_tabs = []

                # Reset each tab individually with error handling
                for tab_name, tab in self.tabs.items():
                    try:
                        if hasattr(tab, 'reset_options'):
                            tab.reset_options()
                            reset_count += 1
                    except Exception as e:
                        error_tabs.append(f"{tab_name}: {str(e)}")
                        print(f"Error resetting {tab_name}: {e}")

                # Reset mutual exclusion manager
                self.mutual_exclusion_manager.reset_all()
                
                # Clear command preview
                self.command_preview.clear()
                
                # Update command preview with reset values
                self.update_command_preview()

                # Report results
                if error_tabs:
                    error_msg = "\n".join(error_tabs)
                    QMessageBox.warning(self, "Reset Completed with Errors",
                                      f"Successfully reset {reset_count} tabs, but encountered errors in:\n\n{error_msg}")
                else:
                    QMessageBox.information(self, "Reset Complete",
                                          f"Successfully reset all {reset_count} tabs to default values.")

                self.log_widget.append_log(f"Reset {reset_count} tabs to defaults", "success")
                if error_tabs:
                    self.log_widget.append_log(f"Errors in {len(error_tabs)} tabs during reset", "warning")

            except Exception as e:
                QMessageBox.critical(self, "Reset Error", f"Failed to reset options: {str(e)}")
                self.log_widget.append_log(f"Failed to reset options: {str(e)}", "error")
    
    def new_profile(self):
        """Create new profile - opens a new window"""
        try:
            # Create a new instance of the main window
            new_window = SqlmapMainWindow()
            new_window.show()
            
            # Get screen geometry for proper positioning
            screen = QApplication.primaryScreen().geometry()
            new_window_rect = new_window.geometry()
            
            # Position new window slightly offset from current window
            current_pos = self.pos()
            offset_x = 30
            offset_y = 30
            
            # Ensure new window stays within screen bounds
            new_x = min(current_pos.x() + offset_x, screen.width() - new_window_rect.width())
            new_y = min(current_pos.y() + offset_y, screen.height() - new_window_rect.height())
            
            # If offset would go off-screen, center it instead
            if new_x + new_window_rect.width() > screen.width() or new_y + new_window_rect.height() > screen.height():
                new_x = (screen.width() - new_window_rect.width()) // 2
                new_y = (screen.height() - new_window_rect.height()) // 2
            
            new_window.move(new_x, new_y)
            
            self.log_widget.append_log("New SQLmap GUI window opened", "info")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create new window: {str(e)}")
            self.log_widget.append_log(f"Failed to create new window: {str(e)}", "error")
    
    def open_profile(self):
        """Open profile from file"""
        from PyQt6.QtWidgets import QFileDialog

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Profile",
            "",
            "JSON Files (*.json);;All Files (*)"
        )

        if file_path:
            self.load_profile_from_file(file_path)

    def load_profile_from_file(self, file_path: str):
        """Load profile from specified file"""
        try:
            import json

            # Load profile data
            with open(file_path, 'r', encoding='utf-8') as f:
                profile_data = json.load(f)

            # Check if this is a valid SQLmap GUI profile
            metadata = profile_data.get('_metadata', {})
            if metadata.get('created_by') != 'SQLmap GUI':
                reply = QMessageBox.question(self, "Unknown Profile Format",
                                           "This doesn't appear to be a SQLmap GUI profile.\n"
                                           "Try to load it anyway?",
                                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if reply != QMessageBox.StandardButton.Yes:
                    return

            # Load options into tabs with error handling
            loaded_tabs = 0
            error_tabs = []

            for tab_name, tab in self.tabs.items():
                try:
                    if hasattr(tab, 'set_options'):
                        tab_options = profile_data.get(tab_name, {})
                        tab.set_options(tab_options)
                        loaded_tabs += 1
                except Exception as e:
                    error_tabs.append(f"{tab_name}: {str(e)}")
                    print(f"Error loading {tab_name}: {e}")

            # Update command preview
            self.update_command_preview()

            # Report results
            version = metadata.get('version', 'Unknown')
            created = metadata.get('created_at', 'Unknown')

            if error_tabs:
                error_msg = "\n".join(error_tabs)
                QMessageBox.warning(self, "Profile Loaded with Errors",
                                  f"Profile loaded from {file_path}\n"
                                  f"Version: {version}\n"
                                  f"Created: {created}\n\n"
                                  f"Loaded {loaded_tabs} tabs successfully, but encountered errors in:\n\n{error_msg}")
            else:
                QMessageBox.information(self, "Profile Loaded",
                                      f"Profile loaded successfully from:\n{file_path}\n\n"
                                      f"Version: {version}\n"
                                      f"Created: {created}\n"
                                      f"Loaded options for all {loaded_tabs} tabs.")

            self.log_widget.append_log(f"Profile loaded from {file_path} ({loaded_tabs} tabs)", "success")
            if error_tabs:
                self.log_widget.append_log(f"Errors in {len(error_tabs)} tabs during load", "warning")

        except json.JSONDecodeError as e:
            QMessageBox.critical(self, "Invalid JSON", f"The selected file is not a valid JSON file:\n{str(e)}")
            self.log_widget.append_log(f"Invalid JSON file: {file_path}", "error")
        except Exception as e:
            QMessageBox.critical(self, "Load Error", f"Failed to load profile: {str(e)}")
            self.log_widget.append_log(f"Failed to load profile: {str(e)}", "error")
    
    def save_profile(self):
        """Save current profile"""
        from PyQt6.QtWidgets import QFileDialog
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Profile",
            "sqlmap_profile.json",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            self.save_profile_to_file(file_path)
    
    def save_profile_as(self):
        """Save profile with new name"""
        self.save_profile()  # Same as save_profile for now
        
    def save_profile_to_file(self, file_path: str):
        """Save current profile to specified file"""
        try:
            import json
            import datetime

            # Collect all options from tabs with error handling
            profile_data = {}
            saved_tabs = 0
            error_tabs = []

            for tab_name, tab in self.tabs.items():
                try:
                    if hasattr(tab, 'get_options'):
                        tab_options = tab.get_options()
                        if tab_options:  # Only save non-empty options
                            profile_data[tab_name] = tab_options
                        saved_tabs += 1
                except Exception as e:
                    error_tabs.append(f"{tab_name}: {str(e)}")
                    print(f"Error saving {tab_name}: {e}")

            # Add comprehensive metadata
            profile_data['_metadata'] = {
                'created_by': 'SQLmap GUI',
                'version': '1.0.0',
                'created_at': datetime.datetime.now().isoformat(),
                'total_tabs': len(self.tabs),
                'saved_tabs': saved_tabs,
                'errors': error_tabs if error_tabs else None,
                'command_preview': self.command_preview.toPlainText() if hasattr(self, 'command_preview') else None
            }

            # Save to file with pretty formatting
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, indent=2, ensure_ascii=False)

            # Report results
            if error_tabs:
                error_msg = "\n".join(error_tabs)
                QMessageBox.warning(self, "Save Completed with Errors",
                                  f"Profile saved to {file_path}\n\n"
                                  f"Saved {saved_tabs} tabs successfully, but encountered errors in:\n\n{error_msg}")
            else:
                QMessageBox.information(self, "Save Complete",
                                      f"Profile saved successfully to:\n{file_path}\n\n"
                                      f"Saved options from all {saved_tabs} tabs.")

            self.log_widget.append_log(f"Profile saved to {file_path} ({saved_tabs} tabs)", "success")
            if error_tabs:
                self.log_widget.append_log(f"Errors in {len(error_tabs)} tabs during save", "warning")

        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Failed to save profile: {str(e)}")
            self.log_widget.append_log(f"Failed to save profile: {str(e)}", "error")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
        <h2>SQLmap GUI</h2>
        <p>A comprehensive graphical interface for SQLmap - the automatic SQL injection and database takeover tool.</p>
        
        <p><b>Features:</b></p>
        <ul>
        <li>Complete SQLmap option coverage</li>
        <li>User-friendly interface</li>
        <li>Real-time validation</li>
        <li>Profile management</li>
        <li>Resource monitoring</li>
        </ul>
        
        <p><b>Built with:</b> Python 3.12, PyQt6</p>
        <p><b>SQLmap Version:</b> 1.9.9.1#dev</p>
        """
        
        QMessageBox.about(self, "About SQLmap GUI", about_text)
    
    def debug_tabs(self):
        """Debug tab integrity and functionality"""
        try:
            results = self.validate_tabs_integrity()

            debug_info = f"""
Tab Integrity Check Results:

Total Tabs: {results['total_tabs']}
Working Tabs: {results['working_tabs']}
Problem Tabs: {results['total_tabs'] - results['working_tabs']}

"""

            if results['issues']:
                debug_info += "Issues Found:\n" + "\n".join(f"• {issue}" for issue in results['issues'])
            else:
                debug_info += "✅ All tabs are working correctly!"

            # Show current options summary
            debug_info += "\n\nCurrent Options Summary:\n"
            total_options = 0
            for tab_name, tab in self.tabs.items():
                try:
                    options = tab.get_options()
                    option_count = len(options)
                    total_options += option_count
                    debug_info += f"• {tab_name}: {option_count} options\n"
                except Exception as e:
                    debug_info += f"• {tab_name}: Error - {str(e)}\n"

            debug_info += f"\nTotal Options Set: {total_options}"

            QMessageBox.information(self, "Tab Debug Results", debug_info)

        except Exception as e:
            QMessageBox.critical(self, "Debug Error", f"Failed to debug tabs: {str(e)}")
    
    def validate_tabs_integrity(self):
        """Validate that all tabs have required methods and are working properly"""
        try:
            validation_results = {
                'total_tabs': len(self.tabs),
                'working_tabs': 0,
                'issues': []
            }

            for tab_name, tab in self.tabs.items():
                tab_issues = []

                # Check if tab has required methods
                if not hasattr(tab, 'get_options'):
                    tab_issues.append("Missing get_options method")
                if not hasattr(tab, 'set_options'):
                    tab_issues.append("Missing set_options method")
                if not hasattr(tab, 'reset_options'):
                    tab_issues.append("Missing reset_options method")

                # Test get_options
                if hasattr(tab, 'get_options'):
                    try:
                        options = tab.get_options()
                        if not isinstance(options, dict):
                            tab_issues.append("get_options doesn't return a dictionary")
                    except Exception as e:
                        tab_issues.append(f"get_options error: {str(e)}")

                # Test reset_options
                if hasattr(tab, 'reset_options'):
                    try:
                        tab.reset_options()
                    except Exception as e:
                        tab_issues.append(f"reset_options error: {str(e)}")

                if tab_issues:
                    validation_results['issues'].append(f"{tab_name}: {', '.join(tab_issues)}")
                else:
                    validation_results['working_tabs'] += 1

            return validation_results

        except Exception as e:
            return {
                'total_tabs': len(self.tabs),
                'working_tabs': 0,
                'issues': [f"Validation error: {str(e)}"]
            }
    
    def toggle_performance_mode(self):
        """Toggle between normal and high performance mode"""
        if self.high_perf_action.isChecked():
            # High performance mode: reduce updates, disable monitoring
            self.pause_resource_monitoring()
            self.command_timer.stop()
            self.delayed_update_timer.stop()
            self.log_widget.append_log("High performance mode enabled - reduced updates", "info")
        else:
            # Normal mode: resume all updates
            self.resume_resource_monitoring()
            self.log_widget.append_log("Normal performance mode restored", "info")
    
    def pause_resource_monitoring(self):
        """Pause resource monitoring to improve performance"""
        try:
            self.status_bar.set_monitoring_enabled(False)
            self.log_widget.append_log("Resource monitoring paused", "info")
        except Exception as e:
            self.log_widget.append_log(f"Failed to pause monitoring: {str(e)}", "warning")
    
    def resume_resource_monitoring(self):
        """Resume resource monitoring"""
        try:
            self.status_bar.set_monitoring_enabled(True)
            self.log_widget.append_log("Resource monitoring resumed", "info")
        except Exception as e:
            self.log_widget.append_log(f"Failed to resume monitoring: {str(e)}", "warning")
    
    def optimize_performance(self):
        """Optimize application performance"""
        try:
            # Optimize log widget
            self.log_widget.optimize_log_size()
            
            # Force garbage collection
            import gc
            gc.collect()
            
            # Update status
            self.status_bar.force_update()
            
            self.log_widget.append_log("Performance optimization completed", "success")
            
        except Exception as e:
            self.log_widget.append_log(f"Performance optimization failed: {str(e)}", "warning")
    
    def debug_cpu_monitoring(self):
        """Debug CPU monitoring functionality"""
        try:
            debug_info = self.status_bar.debug_cpu_monitoring()
            QMessageBox.information(self, "CPU Monitoring Debug", debug_info)
        except Exception as e:
            QMessageBox.critical(self, "Debug Error", f"Failed to debug CPU monitoring: {str(e)}")
    
    def show_sqlmap_help(self):
        """Show SQLmap help information"""
        help_text = """
        <h2>SQLmap Help</h2>
        
        <p><b>SQLmap</b> is an open-source penetration testing tool that automates the process of detecting and exploiting SQL injection flaws.</p>
        
        <p><b>Basic Usage:</b></p>
        <pre>sqlmap -u "http://example.com/page.php?id=1"</pre>
        
        <p><b>Common Options:</b></p>
        <ul>
        <li><code>-u URL</code> - Target URL</li>
        <li><code>--dbs</code> - Enumerate databases</li>
        <li><code>--tables</code> - Enumerate tables</li>
        <li><code>--columns</code> - Enumerate columns</li>
        <li><code>--dump</code> - Dump table contents</li>
        <li><code>--batch</code> - Never ask for user input</li>
        </ul>
        
        <p><b>Advanced Options:</b></p>
        <ul>
        <li><code>--level=LEVEL</code> - Level of tests to perform (1-5)</li>
        <li><code>--risk=RISK</code> - Risk of tests to perform (1-3)</li>
        <li><code>--technique=TECH</code> - SQL injection techniques to use</li>
        <li><code>--dbms=DBMS</code> - Force back-end DBMS</li>
        </ul>
        
        <p><b>Documentation:</b> <a href="https://sqlmap.org">https://sqlmap.org</a></p>
        """
        
        QMessageBox.information(self, "SQLmap Help", help_text)
    
    def load_settings(self):
        """Load application settings"""
        try:
            settings = self.config_manager.load_config()
            # TODO: Apply settings to UI
        except Exception as e:
            self.log_widget.append_log(f"Failed to load settings: {str(e)}", "warning")
    
    def save_settings(self):
        """Save application settings"""
        try:
            # TODO: Collect settings from UI and save
            pass
        except Exception as e:
            self.log_widget.append_log(f"Failed to save settings: {str(e)}", "warning")
    
    def closeEvent(self, event):
        """Handle application close"""
        # Stop any running scan
        if self.current_scan_thread and self.current_scan_thread.isRunning():
            reply = QMessageBox.question(self, "Scan Running", 
                                       "A scan is currently running. Do you want to stop it and exit?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            
            if reply == QMessageBox.StandardButton.Yes:
                self.current_scan_thread.stop()
                self.current_scan_thread.wait(5000)  # Wait up to 5 seconds
            else:
                event.ignore()
                return
        
        # Stop all timers to prevent resource leaks
        try:
            if hasattr(self, 'command_timer') and self.command_timer:
                self.command_timer.stop()
            if hasattr(self, 'delayed_update_timer') and self.delayed_update_timer:
                self.delayed_update_timer.stop()
            if hasattr(self, 'status_bar') and self.status_bar:
                # Stop the status bar timer
                if hasattr(self.status_bar, 'timer'):
                    self.status_bar.timer.stop()
        except Exception as e:
            print(f"Error stopping timers: {e}")
        
        # Save settings
        self.save_settings()
        
        event.accept()

    def start_async_initialization(self):
        """Start async initialization of SQLmap and Python"""
        self.init_thread = SqlmapInitializationThread(self.sqlmap_wrapper)
        self.init_thread.initialization_complete.connect(self.on_initialization_complete)
        self.init_thread.initialization_failed.connect(self.on_initialization_failed)
        self.init_thread.start()

    def on_initialization_complete(self, sqlmap_available, python_available):
        """Handle successful initialization"""
        if sqlmap_available and python_available:
            self.log_widget.append_log("✅ SQLmap and Python are available and ready", "success")
            self.log_widget.append_log("Ready to start SQL injection testing", "info")
        elif sqlmap_available:
            self.log_widget.append_log("✅ SQLmap is available", "success")
            self.log_widget.append_log("⚠️ Python interpreter not found - some features may be limited", "warning")
        elif python_available:
            self.log_widget.append_log("✅ Python interpreter is available", "success")
            self.log_widget.append_log("❌ SQLmap not found - please install SQLmap and ensure it's in your PATH", "error")
        else:
            self.log_widget.append_log("❌ Neither SQLmap nor Python interpreter found", "error")
            self.log_widget.append_log("Please install SQLmap and Python to use this tool", "error")

    def on_initialization_failed(self, error_message):
        """Handle initialization failure"""
        self.log_widget.append_log(f"❌ Initialization failed: {error_message}", "error")
        self.log_widget.append_log("Some features may not work correctly", "warning")


class SqlmapInitializationThread(QThread):
    """Thread for async initialization of SQLmap wrapper"""
    
    initialization_complete = pyqtSignal(bool, bool)  # sqlmap_available, python_available
    initialization_failed = pyqtSignal(str)  # error_message
    
    def __init__(self, sqlmap_wrapper):
        super().__init__()
        self.sqlmap_wrapper = sqlmap_wrapper
    
    def run(self):
        """Run the initialization in background"""
        try:
            self.sqlmap_wrapper.initialize_async()
            self.initialization_complete.emit(
                self.sqlmap_wrapper.sqlmap_available,
                self.sqlmap_wrapper.python_available
            )
        except Exception as e:
            self.initialization_failed.emit(str(e))


class SqlmapScanThread(QThread):
    """Thread for running SQLmap scans"""
    
    log_message = pyqtSignal(str, str)  # message, type
    scan_finished = pyqtSignal(bool)    # success
    progress_updated = pyqtSignal(int)  # progress value
    
    def __init__(self, sqlmap_wrapper: SqlmapWrapper, options: Dict[str, Any], use_sudo: bool = False, sudo_password: str = None):
        super().__init__()
        self.sqlmap_wrapper = sqlmap_wrapper
        self.options = options
        self.use_sudo = use_sudo
        self.sudo_password = sudo_password
        self.should_stop = False
    
    def clean_ansi_escape_sequences(self, text: str) -> str:
        """Remove ANSI escape sequences from text - comprehensive pattern"""
        # More comprehensive ANSI escape sequence regex
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])|\x1B\[[0-9;]*[mG]|\x1B\([AB0-9]|\x1B\)[AB0-9]|\x1B[=>]')
        cleaned = ansi_escape.sub('', text)
        # Also remove any remaining control characters
        cleaned = re.sub(r'[\x00-\x1F\x7F]', '', cleaned)
        return cleaned
    
    def run(self):
        """Run the scan"""
        try:
            # Create scan process
            process = self.sqlmap_wrapper.create_process(self.options, self.use_sudo, self.sudo_password)
            
            if not process:
                self.log_message.emit("Failed to create SQLmap process - check SQLmap installation and PATH", "error")
                self.scan_finished.emit(False)
                return
            
            # Start process
            if not process.start():
                self.log_message.emit("Failed to start SQLmap process - check command syntax and permissions", "error")
                self.scan_finished.emit(False)
                return
            
            sudo_text = " with sudo" if self.use_sudo else ""
            self.log_message.emit(f"SQLmap process started successfully{sudo_text}", "info")
            
            # Wait a moment to see if the process produces any immediate output
            time.sleep(1)
            
            # Check if process is still running and get initial output
            initial_output = process.get_output()
            if initial_output:
                for line in initial_output:
                    cleaned_line = self.clean_ansi_escape_sequences(line)
                    if cleaned_line.strip():  # Only emit non-empty lines
                        self.log_message.emit(cleaned_line, "info")
            
            initial_errors = process.get_errors()
            if initial_errors:
                for line in initial_errors:
                    cleaned_line = self.clean_ansi_escape_sequences(line)
                    if cleaned_line.strip():
                        self.log_message.emit(f"Error: {cleaned_line}", "error")
            
            # Monitor process output
            while process.is_running and not self.should_stop:
                output = process.read_output()
                if output:
                    cleaned_output = self.clean_ansi_escape_sequences(output.strip())
                    if cleaned_output:  # Only emit non-empty cleaned output
                        self.log_message.emit(cleaned_output, "info")
                
                error = process.read_error()
                if error:
                    cleaned_error = self.clean_ansi_escape_sequences(error.strip())
                    if cleaned_error:
                        self.log_message.emit(f"Error: {cleaned_error}", "error")
                
                self.msleep(100)  # Small delay to prevent excessive CPU usage
            
            # Stop process if requested
            if self.should_stop:
                process.stop()
                self.log_message.emit("Scan stopped by user", "warning")
                self.scan_finished.emit(False)
            else:
                # Process completed naturally
                exit_code = process.get_exit_code()
                if exit_code == 0:
                    self.log_message.emit("Scan completed successfully", "success")
                    self.scan_finished.emit(True)
                else:
                    self.log_message.emit(f"Scan failed with exit code {exit_code}", "error")
                    # Try to get any remaining output
                    final_output = process.get_output()
                    if final_output:
                        for line in final_output:
                            cleaned_line = self.clean_ansi_escape_sequences(line)
                            if cleaned_line.strip():
                                self.log_message.emit(f"Final output: {cleaned_line}", "info")
                    
                    final_errors = process.get_errors()
                    if final_errors:
                        for line in final_errors:
                            cleaned_line = self.clean_ansi_escape_sequences(line)
                            if cleaned_line.strip():
                                self.log_message.emit(f"Final error: {cleaned_line}", "error")
                    
                    self.scan_finished.emit(False)
                
        except Exception as e:
            self.log_message.emit(f"Scan error: {str(e)}", "error")
            self.scan_finished.emit(False)
    
    def stop(self):
        """Request scan stop"""
        self.should_stop = True
