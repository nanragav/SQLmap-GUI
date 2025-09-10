"""
Command Validation Dialog - Display comprehensive SQLmap command validation results
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTextEdit, 
                            QPushButton, QLabel, QScrollArea, QWidget,
                            QTabWidget, QGroupBox, QListWidget, QListWidgetItem,
                            QSplitter, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QPixmap, QPalette
import sys
import os

# Add the parent directory to the path to import from core
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.core.sqlmap_wrapper import CommandValidation, ValidationLevel, ValidationResult


class ValidationResultWidget(QWidget):
    """Widget to display individual validation result"""
    
    def __init__(self, result: ValidationResult, parent=None):
        super().__init__(parent)
        self.result = result
        self.init_ui()
    
    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Icon based on validation level
        icon_label = QLabel()
        if self.result.level == ValidationLevel.ERROR:
            icon_label.setText("🚨")
            icon_label.setStyleSheet("color: #e74c3c; font-size: 16px;")
        elif self.result.level == ValidationLevel.WARNING:
            icon_label.setText("⚠️")
            icon_label.setStyleSheet("color: #f39c12; font-size: 16px;")
        elif self.result.level == ValidationLevel.INFO:
            icon_label.setText("💡")
            icon_label.setStyleSheet("color: #3498db; font-size: 16px;")
        else:
            icon_label.setText("✅")
            icon_label.setStyleSheet("color: #27ae60; font-size: 16px;")
        
        icon_label.setFixedWidth(30)
        layout.addWidget(icon_label)
        
        # Message content
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Main message
        message_label = QLabel(self.result.message)
        message_label.setWordWrap(True)
        
        # Style based on level with better contrast
        if self.result.level == ValidationLevel.ERROR:
            message_label.setStyleSheet("color: #d32f2f; font-weight: bold; font-size: 12px; background-color: rgba(244, 67, 54, 0.1); padding: 4px; border-radius: 3px;")
        elif self.result.level == ValidationLevel.WARNING:
            message_label.setStyleSheet("color: #f57c00; font-weight: bold; font-size: 12px; background-color: rgba(255, 152, 0, 0.1); padding: 4px; border-radius: 3px;")
        elif self.result.level == ValidationLevel.INFO:
            message_label.setStyleSheet("color: #1976d2; font-size: 12px; background-color: rgba(33, 150, 243, 0.1); padding: 4px; border-radius: 3px;")
        
        content_layout.addWidget(message_label)
        
        # Flag info
        if self.result.flag:
            flag_label = QLabel(f"Flag: {self.result.flag}")
            flag_label.setStyleSheet("color: #424242; font-style: italic; font-size: 11px; font-family: 'Courier New', monospace; background-color: #f5f5f5; padding: 2px 4px; border-radius: 2px;")
            content_layout.addWidget(flag_label)
        
        # Suggestion
        if self.result.suggestion:
            suggestion_label = QLabel(f"💡 {self.result.suggestion}")
            suggestion_label.setWordWrap(True)
            suggestion_label.setStyleSheet("color: #2e7d32; font-size: 11px; margin-top: 3px; padding: 6px; background-color: #e8f5e8; border-left: 4px solid #4caf50; border-radius: 3px;")
            content_layout.addWidget(suggestion_label)
        
        layout.addLayout(content_layout, 1)
        self.setLayout(layout)


class CommandValidationDialog(QDialog):
    """Dialog for displaying comprehensive command validation results"""
    
    command_fixed = pyqtSignal(str)  # Emitted when user wants to apply fixes
    
    def __init__(self, validation: CommandValidation, original_command: str = "", parent=None):
        super().__init__(parent)
        self.validation = validation
        self.original_command = original_command
        self.setWindowTitle("SQLmap Command Validation")
        self.setModal(True)
        self.resize(800, 600)
        self.init_ui()
    
    def init_ui(self):
        # Set dialog background
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                color: #333333;
            }
            QTextEdit {
                background-color: #fafafa;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 8px;
                color: #333333;
            }
            QScrollArea {
                background-color: #ffffff;
                border: none;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Header with overall status
        header = self.create_header()
        layout.addWidget(header)
        
        # Main content area with tabs
        tabs = QTabWidget()
        
        # Overview tab
        overview_tab = self.create_overview_tab()
        tabs.addTab(overview_tab, "Overview")
        
        # Errors tab
        if self.validation.errors:
            errors_tab = self.create_results_tab(self.validation.errors, "Errors")
            tabs.addTab(errors_tab, f"Errors ({len(self.validation.errors)})")
        
        # Warnings tab
        if self.validation.warnings:
            warnings_tab = self.create_results_tab(self.validation.warnings, "Warnings")
            tabs.addTab(warnings_tab, f"Warnings ({len(self.validation.warnings)})")
        
        # Suggestions tab
        if self.validation.infos:
            infos_tab = self.create_results_tab(self.validation.infos, "Suggestions")
            tabs.addTab(infos_tab, f"Suggestions ({len(self.validation.infos)})")
        
        # Command details tab
        command_tab = self.create_command_tab()
        tabs.addTab(command_tab, "Command Details")
        
        layout.addWidget(tabs)
        
        # Buttons
        button_layout = self.create_button_layout()
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def create_header(self):
        """Create header with overall validation status"""
        header = QFrame()
        header.setFrameStyle(QFrame.Shape.StyledPanel)
        
        if self.validation.is_valid:
            header.setStyleSheet("background-color: #d4edda; border: 1px solid #c3e6cb; border-radius: 5px; padding: 10px;")
        else:
            header.setStyleSheet("background-color: #f8d7da; border: 1px solid #f5c6cb; border-radius: 5px; padding: 10px;")
        
        layout = QHBoxLayout()
        
        # Status icon and text
        status_layout = QVBoxLayout()
        
        if self.validation.is_valid:
            status_icon = QLabel("✅")
            status_text = QLabel("Command is valid and ready to execute!")
            status_text.setStyleSheet("color: #155724; font-weight: bold; font-size: 14px;")
        else:
            status_icon = QLabel("❌")
            status_text = QLabel("Command has errors and cannot be executed")
            status_text.setStyleSheet("color: #721c24; font-weight: bold; font-size: 14px;")
        
        status_icon.setStyleSheet("font-size: 24px;")
        status_layout.addWidget(status_icon)
        status_layout.addWidget(status_text)
        
        layout.addLayout(status_layout)
        
        # Statistics
        stats_layout = QVBoxLayout()
        stats_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        if self.validation.errors:
            error_label = QLabel(f"🚨 {len(self.validation.errors)} Errors")
            error_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
            stats_layout.addWidget(error_label)
        
        if self.validation.warnings:
            warning_label = QLabel(f"⚠️ {len(self.validation.warnings)} Warnings")
            warning_label.setStyleSheet("color: #f39c12; font-weight: bold;")
            stats_layout.addWidget(warning_label)
        
        if self.validation.infos:
            info_label = QLabel(f"💡 {len(self.validation.infos)} Suggestions")
            info_label.setStyleSheet("color: #3498db;")
            stats_layout.addWidget(info_label)
        
        layout.addLayout(stats_layout)
        header.setLayout(layout)
        
        return header
    
    def create_overview_tab(self):
        """Create overview tab with summary"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Summary text
        summary = QTextEdit()
        summary.setReadOnly(True)
        summary.setMaximumHeight(200)
        
        summary_text = "VALIDATION SUMMARY\n" + "="*50 + "\n\n"
        
        if self.validation.is_valid:
            summary_text += "✅ Your SQLmap command passed all validation checks and is ready to execute.\n\n"
        else:
            summary_text += "❌ Your SQLmap command has issues that need to be addressed before execution.\n\n"
        
        summary_text += f"Total Issues Found: {len(self.validation.results)}\n"
        summary_text += f"  • Errors: {len(self.validation.errors)}\n"
        summary_text += f"  • Warnings: {len(self.validation.warnings)}\n"
        summary_text += f"  • Suggestions: {len(self.validation.infos)}\n\n"
        
        if self.validation.errors:
            summary_text += "CRITICAL ISSUES:\n"
            for error in self.validation.errors[:3]:  # Show first 3 errors
                summary_text += f"  • {error.message}\n"
            if len(self.validation.errors) > 3:
                summary_text += f"  ... and {len(self.validation.errors) - 3} more errors\n"
            summary_text += "\n"
        
        summary.setPlainText(summary_text)
        layout.addWidget(summary)
        
        # Quick fixes section
        if self.validation.results:
            quick_fixes = QGroupBox("Quick Action Items")
            quick_layout = QVBoxLayout()
            
            for result in self.validation.results[:5]:  # Show first 5 results
                item = ValidationResultWidget(result)
                quick_layout.addWidget(item)
            
            quick_fixes.setLayout(quick_layout)
            
            scroll = QScrollArea()
            scroll.setWidget(quick_fixes)
            scroll.setWidgetResizable(True)
            layout.addWidget(scroll)
        
        widget.setLayout(layout)
        return widget
    
    def create_results_tab(self, results: list, title: str):
        """Create tab for displaying specific type of results"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Results list
        scroll = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_layout.setContentsMargins(5, 5, 5, 5)
        
        for result in results:
            item_widget = ValidationResultWidget(result)
            item_widget.setStyleSheet("border-bottom: 1px solid #ecf0f1; padding: 5px; margin: 2px;")
            scroll_layout.addWidget(item_widget)
        
        scroll_layout.addStretch()
        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        
        layout.addWidget(scroll)
        widget.setLayout(layout)
        
        return widget
    
    def create_command_tab(self):
        """Create tab showing command details"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Original command
        if self.original_command:
            original_group = QGroupBox("Original Command")
            original_layout = QVBoxLayout()
            
            original_text = QTextEdit()
            original_text.setPlainText(self.original_command)
            original_text.setMaximumHeight(100)
            original_text.setReadOnly(True)
            original_text.setStyleSheet("font-family: 'Courier New', monospace; background-color: #f8f9fa;")
            
            original_layout.addWidget(original_text)
            original_group.setLayout(original_layout)
            layout.addWidget(original_group)
        
        # Suggested command
        if self.validation.suggested_command:
            suggested_group = QGroupBox("Suggested Command")
            suggested_layout = QVBoxLayout()
            
            suggested_text = QTextEdit()
            suggested_text.setPlainText(self.validation.suggested_command)
            suggested_text.setMaximumHeight(100)
            suggested_text.setReadOnly(True)
            suggested_text.setStyleSheet("font-family: 'Courier New', monospace; background-color: #e8f5e8;")
            
            suggested_layout.addWidget(suggested_text)
            suggested_group.setLayout(suggested_layout)
            layout.addWidget(suggested_group)
        
        # Analysis details
        analysis_group = QGroupBox("Technical Analysis")
        analysis_layout = QVBoxLayout()
        
        analysis_text = QTextEdit()
        analysis_text.setReadOnly(True)
        
        analysis_content = "TECHNICAL VALIDATION DETAILS\n" + "="*40 + "\n\n"
        
        # Group results by category
        analysis_content += "Flag Analysis:\n"
        flag_results = [r for r in self.validation.results if r.flag]
        if flag_results:
            for result in flag_results:
                analysis_content += f"  {result.flag}: {result.message}\n"
        else:
            analysis_content += "  No flag-specific issues found.\n"
        
        analysis_content += "\nGeneral Issues:\n"
        general_results = [r for r in self.validation.results if not r.flag]
        if general_results:
            for result in general_results:
                analysis_content += f"  • {result.message}\n"
        else:
            analysis_content += "  No general issues found.\n"
        
        analysis_text.setPlainText(analysis_content)
        analysis_text.setStyleSheet("font-family: 'Courier New', monospace; font-size: 11px;")
        
        analysis_layout.addWidget(analysis_text)
        analysis_group.setLayout(analysis_layout)
        layout.addWidget(analysis_group)
        
        widget.setLayout(layout)
        return widget
    
    def create_button_layout(self):
        """Create button layout"""
        layout = QHBoxLayout()
        
        # Apply fixes button (if suggestions available)
        if self.validation.suggested_command:
            apply_button = QPushButton("Apply Suggested Fixes")
            apply_button.setStyleSheet("QPushButton { background-color: #2ecc71; color: white; font-weight: bold; padding: 8px 16px; border: none; border-radius: 4px; } QPushButton:hover { background-color: #27ae60; }")
            apply_button.clicked.connect(self.apply_fixes)
            layout.addWidget(apply_button)
        
        layout.addStretch()
        
        # Close button
        close_button = QPushButton("Close")
        close_button.setDefault(True)
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)
        
        return layout
    
    def apply_fixes(self):
        """Apply suggested fixes"""
        if self.validation.suggested_command:
            self.command_fixed.emit(self.validation.suggested_command)
            self.accept()


# Test the dialog if run directly
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    # Create sample validation results for testing
    from src.core.sqlmap_validator import ValidationResult, ValidationLevel, CommandValidation
    
    results = [
        ValidationResult(ValidationLevel.ERROR, "Missing target specification", suggestion="Add -u, -r, or other target flag"),
        ValidationResult(ValidationLevel.WARNING, "High risk flag detected", flag="--os-shell", suggestion="Ensure proper authorization"),
        ValidationResult(ValidationLevel.INFO, "Consider adding --batch for automation", suggestion="Add --batch flag")
    ]
    
    validation = CommandValidation(
        is_valid=False,
        results=results,
        errors=[results[0]],
        warnings=[results[1]],
        infos=[results[2]]
    )
    
    dialog = CommandValidationDialog(validation, "sqlmap --os-shell")
    dialog.show()
    
    sys.exit(app.exec())
