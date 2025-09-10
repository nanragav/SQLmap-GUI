"""
Custom GUI Widgets for SQLmap GUI
Reusable components with built-in validation and styling
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                            QCheckBox, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit,
                            QGroupBox, QScrollArea, QPushButton, QFileDialog, QFrame,
                            QSlider, QProgressBar, QTabWidget, QSplitter)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QRegularExpression
from PyQt6.QtGui import QFont, QPalette, QValidator, QRegularExpressionValidator
import re
from typing import Any, Dict, List, Optional, Callable

class ValidatedLineEdit(QLineEdit):
    """Line edit with built-in validation and error styling"""
    
    validationChanged = pyqtSignal(bool)  # Emits validation state
    
    def __init__(self, validator_type: str = "text", placeholder: str = "", parent=None):
        super().__init__(parent)
        self.validator_type = validator_type
        self.is_valid = True
        self.error_style = "QLineEdit { border: 2px solid red; background-color: #ffe6e6; }"
        self.normal_style = ""
        
        if placeholder:
            self.setPlaceholderText(placeholder)
        
        self.setup_validator()
        self.textChanged.connect(self.validate_input)
    
    def setup_validator(self):
        """Setup validator based on type"""
        if self.validator_type == "url":
            regex = QRegularExpression(r"^https?://[^\s/$.?#].[^\s]*$")
            validator = QRegularExpressionValidator(regex)
            self.setValidator(validator)
        elif self.validator_type == "ip":
            regex = QRegularExpression(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
            validator = QRegularExpressionValidator(regex)
            self.setValidator(validator)
        elif self.validator_type == "port":
            regex = QRegularExpression(r"^([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$")
            validator = QRegularExpressionValidator(regex)
            self.setValidator(validator)
        elif self.validator_type == "email":
            regex = QRegularExpression(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
            validator = QRegularExpressionValidator(regex)
            self.setValidator(validator)
    
    def validate_input(self):
        """Validate current input and update styling"""
        text = self.text()
        
        if not text:  # Empty is usually valid
            self.is_valid = True
            self.setStyleSheet(self.normal_style)
        else:
            if self.validator():
                pos = 0
                state, _, _ = self.validator().validate(text, pos)
                self.is_valid = state == QValidator.State.Acceptable
            else:
                self.is_valid = True
        
        # Update styling
        if self.is_valid:
            self.setStyleSheet(self.normal_style)
        else:
            self.setStyleSheet(self.error_style)
        
        self.validationChanged.emit(self.is_valid)
    
    def get_value(self) -> str:
        """Get current value"""
        return self.text()
    
    def set_value(self, value: str):
        """Set value and validate"""
        self.setText(str(value))
        self.validate_input()


class OptionGroup(QGroupBox):
    """Grouped options with enable/disable functionality and mutual exclusion support"""
    
    def __init__(self, title: str, options: List[Dict], mutual_exclusion_manager=None, parent=None):
        super().__init__(title, parent)
        self.options = options
        self.widgets = {}
        self.enabled_changed = {}
        self.mutual_exclusion_manager = mutual_exclusion_manager
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the UI for this option group"""
        layout = QVBoxLayout()
        
        for option in self.options:
            widget = self.create_option_widget(option)
            if widget:
                layout.addWidget(widget)
                
        self.setLayout(layout)
        
        # Register widgets with mutual exclusion manager
        if self.mutual_exclusion_manager:
            for name, widget in self.widgets.items():
                self.mutual_exclusion_manager.register_option(name, widget)
    
    def create_option_widget(self, option: Dict) -> Optional[QWidget]:
        """Create widget for a single option"""
        option_type = option.get('type', 'checkbox')
        name = option['name']
        label = option.get('label', name.replace('_', ' ').title())
        
        if option_type == 'checkbox':
            widget = QCheckBox(label)
            widget.stateChanged.connect(lambda state, n=name: self.option_changed(n, state == Qt.CheckState.Checked.value))
            self.widgets[name] = widget
            return widget
            
        elif option_type == 'text':
            container = QWidget()
            layout = QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            
            label_widget = QLabel(label + ":")
            line_edit = ValidatedLineEdit(
                validator_type=option.get('validator', 'text'),
                placeholder=option.get('placeholder', '')
            )
            
            layout.addWidget(label_widget)
            layout.addWidget(line_edit)
            
            container.setLayout(layout)
            self.widgets[name] = line_edit
            
            line_edit.textChanged.connect(lambda text, n=name: self.option_changed(n, text))
            return container
            
        elif option_type == 'number':
            container = QWidget()
            layout = QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            
            label_widget = QLabel(label + ":")
            
            if option.get('decimal', False):
                spin_box = QDoubleSpinBox()
                spin_box.setDecimals(option.get('decimals', 2))
            else:
                spin_box = QSpinBox()
            
            spin_box.setMinimum(option.get('min', 0))
            spin_box.setMaximum(option.get('max', 999999))
            spin_box.setValue(option.get('default', 0))
            
            # Add placeholder as tooltip if no default but placeholder exists
            if 'placeholder' in option and 'default' not in option:
                spin_box.setToolTip(f"{option.get('tooltip', '')} {option['placeholder']}".strip())
            
            layout.addWidget(label_widget)
            layout.addWidget(spin_box)
            
            container.setLayout(layout)
            self.widgets[name] = spin_box
            
            spin_box.valueChanged.connect(lambda value, n=name: self.option_changed(n, value))
            return container
            
        elif option_type == 'combo':
            container = QWidget()
            layout = QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            
            label_widget = QLabel(label + ":")
            combo_box = QComboBox()
            
            items = option.get('items', [])
            for item in items:
                if isinstance(item, dict):
                    combo_box.addItem(item['label'], item['value'])
                else:
                    combo_box.addItem(str(item), item)
            
            layout.addWidget(label_widget)
            layout.addWidget(combo_box)
            
            container.setLayout(layout)
            self.widgets[name] = combo_box
            
            combo_box.currentTextChanged.connect(lambda text, n=name: self.option_changed(n, combo_box.currentData()))
            return container
            
        elif option_type == 'file':
            container = QWidget()
            layout = QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            
            label_widget = QLabel(label + ":")
            line_edit = QLineEdit()
            line_edit.setPlaceholderText(option.get('placeholder', 'Select file...'))
            browse_button = QPushButton("Browse")
            
            def browse_file():
                file_path, _ = QFileDialog.getOpenFileName(
                    self, 
                    f"Select {label}",
                    "",
                    option.get('filter', "All Files (*)")
                )
                if file_path:
                    line_edit.setText(file_path)
            
            browse_button.clicked.connect(browse_file)
            line_edit.textChanged.connect(lambda text, n=name: self.option_changed(n, text))
            
            layout.addWidget(label_widget)
            layout.addWidget(line_edit)
            layout.addWidget(browse_button)
            
            container.setLayout(layout)
            # Store both the line_edit and container for proper disabling
            self.widgets[name] = line_edit
            # Also store a reference to disable the entire container
            if not hasattr(self, '_containers'):
                self._containers = {}
            self._containers[name] = container
            return container
        
        return None
    
    def option_changed(self, name: str, value: Any):
        """Handle option value change"""
        if name in self.enabled_changed:
            self.enabled_changed[name](value)
        
        # Notify mutual exclusion manager
        if self.mutual_exclusion_manager:
            self.mutual_exclusion_manager.update_option_state(name, value)
        
        # Emit signal to parent for real-time updates
        parent = self.parent()
        while parent:
            if hasattr(parent, 'options_changed'):
                parent.options_changed.emit()
                break
            parent = parent.parent()
    
    def get_values(self) -> Dict[str, Any]:
        """Get all option values"""
        values = {}
        try:
            for name, widget in self.widgets.items():
                if isinstance(widget, QCheckBox):
                    values[name] = widget.isChecked()
                elif isinstance(widget, (QLineEdit, ValidatedLineEdit)):
                    text = widget.text()
                    values[name] = text if text else None
                elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                    value = widget.value()
                    # For spinboxes, check if value differs from minimum (indicating user input)
                    # But include if there's an explicit default that was set
                    minimum = widget.minimum()
                    # Special handling for common parameters that shouldn't default to minimum
                    if name in ['start', 'stop', 'first', 'last', 'safe_freq', 'proxy_freq'] and value == minimum:
                        values[name] = None  # Don't include these unless explicitly set above minimum
                    else:
                        values[name] = value if value != 0 else None
                elif isinstance(widget, QComboBox):
                    data = widget.currentData()
                    values[name] = data if data is not None else widget.currentText()
        except Exception as e:
            print(f"Error getting values from OptionGroup: {e}")
        return values
    
    def set_values(self, values: Dict[str, Any]):
        """Set option values"""
        try:
            for name, value in values.items():
                if name in self.widgets:
                    widget = self.widgets[name]
                    try:
                        if isinstance(widget, QCheckBox):
                            widget.setChecked(bool(value))
                        elif isinstance(widget, (QLineEdit, ValidatedLineEdit)):
                            widget.setText(str(value) if value is not None else "")
                        elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                            if isinstance(value, (int, float)):
                                widget.setValue(value)
                        elif isinstance(widget, QComboBox):
                            if value is not None:
                                index = widget.findData(value)
                                if index >= 0:
                                    widget.setCurrentIndex(index)
                                else:
                                    # Try to find by text if data doesn't match
                                    index = widget.findText(str(value))
                                    if index >= 0:
                                        widget.setCurrentIndex(index)
                    except Exception as e:
                        print(f"Error setting value for {name}: {e}")
        except Exception as e:
            print(f"Error setting values in OptionGroup: {e}")
    
    def set_enabled(self, enabled: bool):
        """Enable/disable all widgets in group"""
        for widget in self.widgets.values():
            widget.setEnabled(enabled)


class StatusBar(QWidget):
    """Custom status bar with progress and resource monitoring"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
        # Timer for updating resource info
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_resources)
        self.timer.start(2000)  # Update every 2 seconds
    
    def setup_ui(self):
        """Setup status bar UI"""
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 2, 5, 2)
        
        # Status label
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMaximumWidth(200)
        layout.addWidget(self.progress_bar)
        
        # Spacer
        layout.addStretch()
        
        # Resource info
        self.memory_label = QLabel("Memory: 0 MB")
        self.cpu_label = QLabel("CPU: 0%")
        
        layout.addWidget(self.memory_label)
        layout.addWidget(QLabel("|"))
        layout.addWidget(self.cpu_label)
        
        self.setLayout(layout)
    
    def set_status(self, status: str):
        """Set status message"""
        self.status_label.setText(status)
    
    def show_progress(self, show: bool = True):
        """Show/hide progress bar"""
        self.progress_bar.setVisible(show)
    
    def set_progress(self, value: int, maximum: int = 100):
        """Set progress value"""
        self.progress_bar.setMaximum(maximum)
        self.progress_bar.setValue(value)
    
    def update_resources(self):
        """Update resource usage display"""
        try:
            import psutil
            process = psutil.Process()
            
            # Memory usage
            memory_mb = process.memory_info().rss / 1024 / 1024
            self.memory_label.setText(f"Memory: {memory_mb:.1f} MB")
            
            # CPU usage
            cpu_percent = process.cpu_percent()
            self.cpu_label.setText(f"CPU: {cpu_percent:.1f}%")
            
        except ImportError:
            # psutil not available
            pass
        except Exception:
            # Error getting process info
            pass


class LogWidget(QTextEdit):
    """Enhanced text widget for displaying logs with syntax highlighting"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        # Note: setMaximumBlockCount is not available in PyQt6, we'll handle log size manually
        
        # Setup font
        font = QFont("Consolas", 9)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.setFont(font)
        
        self.auto_scroll = True
    
    def append_log(self, text: str, log_type: str = "info"):
        """Append log entry with styling"""
        color_map = {
            "info": "black",
            "warning": "#ff8c00",
            "error": "red",
            "success": "green",
            "debug": "gray"
        }
        
        color = color_map.get(log_type, "black")
        
        # Format with timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        formatted_text = f"<span style='color: {color};'>[{timestamp}] {text}</span>"
        
        # Append and scroll if auto-scroll is enabled
        cursor = self.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.setTextCursor(cursor)
        self.insertHtml(formatted_text + "<br>")
        
        if self.auto_scroll:
            self.scroll_to_bottom()
    
    def scroll_to_bottom(self):
        """Scroll to bottom of log"""
        scrollbar = self.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def clear_log(self):
        """Clear all log content"""
        self.clear()
    
    def set_auto_scroll(self, enabled: bool):
        """Enable/disable auto-scrolling"""
        self.auto_scroll = enabled


class CollapsibleWidget(QWidget):
    """Widget that can be collapsed/expanded"""
    
    def __init__(self, title: str, content_widget: QWidget, parent=None):
        super().__init__(parent)
        self.title = title
        self.content_widget = content_widget
        self.is_expanded = True
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup collapsible UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header with toggle button
        header = QWidget()
        header.setStyleSheet("""
            QWidget { 
                background-color: #f0f0f0; 
                border: 1px solid #ccc; 
                color: #333;
            }
        """)
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(5, 5, 5, 5)
        
        self.toggle_button = QPushButton("▼")
        self.toggle_button.setMaximumSize(20, 20)
        self.toggle_button.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                border: 1px solid #aaa;
                border-radius: 3px;
                color: #333;
                font-weight: bold;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
            QPushButton:pressed {
                background-color: #c0c0c0;
            }
        """)
        self.toggle_button.clicked.connect(self.toggle)
        
        title_label = QLabel(self.title)
        title_label.setStyleSheet("""
            font-weight: bold;
            color: #333;
            font-size: 11pt;
        """)
        
        header_layout.addWidget(self.toggle_button)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        header.setLayout(header_layout)
        
        # Content area
        self.content_area = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(10, 5, 10, 5)
        content_layout.addWidget(self.content_widget)
        self.content_area.setLayout(content_layout)
        
        layout.addWidget(header)
        layout.addWidget(self.content_area)
        
        self.setLayout(layout)
    
    def toggle(self):
        """Toggle expanded/collapsed state"""
        self.is_expanded = not self.is_expanded
        self.content_area.setVisible(self.is_expanded)
        self.toggle_button.setText("▼" if self.is_expanded else "▶")
    
    def set_expanded(self, expanded: bool):
        """Set expanded state"""
        self.is_expanded = expanded
        self.content_area.setVisible(expanded)
        self.toggle_button.setText("▼" if expanded else "▶")
