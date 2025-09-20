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
            # If empty dictionary is passed, reset all widgets to defaults
            if not values:
                self.reset_values()
                return
                
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
    
    def reset_values(self):
        """Reset all widgets to their default values"""
        try:
            for name, widget in self.widgets.items():
                try:
                    if isinstance(widget, QCheckBox):
                        widget.setChecked(False)
                    elif isinstance(widget, (QLineEdit, ValidatedLineEdit)):
                        widget.clear()
                    elif isinstance(widget, QSpinBox):
                        widget.setValue(widget.minimum())
                    elif isinstance(widget, QDoubleSpinBox):
                        widget.setValue(widget.minimum())
                    elif isinstance(widget, QComboBox):
                        widget.setCurrentIndex(0)  # Reset to first item
                except Exception as e:
                    print(f"Error resetting widget {name}: {e}")
        except Exception as e:
            print(f"Error resetting values in OptionGroup: {e}")
    
    def set_enabled(self, enabled: bool):
        """Enable/disable all widgets in group"""
        for widget in self.widgets.values():
            widget.setEnabled(enabled)


class StatusBar(QWidget):
    """Custom status bar with progress and resource monitoring"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
        # Timer for updating resource info - less frequent and more efficient
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_resources)
        self.timer.start(10000)  # Update every 10 seconds to reduce CPU overhead
        
        # Cache for resource values to avoid unnecessary updates
        self.last_memory_mb = 0
        self.last_cpu_percent = 0.0
        self.cpu_measurement_count = 0  # Track CPU measurements for non-blocking approach
        
        # Flag to control monitoring
        self.monitoring_enabled = True
    
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
        """Update resource usage display - optimized version"""
        if not self.monitoring_enabled:
            return
            
        try:
            import psutil
            import os
            
            # Get current process
            current_pid = os.getpid()
            process = psutil.Process(current_pid)
            
            # Memory usage
            memory_info = process.memory_info()
            memory_mb = memory_info.rss / 1024 / 1024
            
            # Only update if memory changed significantly (>1MB difference)
            if abs(memory_mb - self.last_memory_mb) > 1.0:
                self.memory_label.setText(f"Memory: {memory_mb:.1f} MB")
                self.last_memory_mb = memory_mb
            
            # CPU usage - use non-blocking approach
            try:
                # First call to cpu_percent() needs to establish baseline (non-blocking)
                if self.cpu_measurement_count == 0:
                    # Initial call to establish baseline
                    process.cpu_percent()
                    self.cpu_measurement_count = 1
                    cpu_percent = 0.0  # Show 0% on first measurement
                else:
                    # Subsequent calls will return actual CPU usage (non-blocking)
                    cpu_percent = process.cpu_percent()
                
                # Only update if CPU changed significantly (>2% difference) to reduce flicker
                if abs(cpu_percent - self.last_cpu_percent) > 2.0:
                    if cpu_percent >= 0:  # Valid CPU percentage
                        self.cpu_label.setText(f"CPU: {cpu_percent:.1f}%")
                        self.last_cpu_percent = cpu_percent
                    else:
                        self.cpu_label.setText("CPU: 0.0%")
                        self.last_cpu_percent = 0.0

            except KeyboardInterrupt as ke:
                # Allow graceful exit on keyboard interrupt
                print("Resource monitoring interrupted by user.")
                pass
                        
            except Exception as cpu_error:
                # Fallback: show last known value or error
                if self.last_cpu_percent != -1:  # Only update once
                    self.cpu_label.setText("CPU: N/A")
                    self.last_cpu_percent = -1
            
        except ImportError:
            # psutil not available - only update once
            if self.last_memory_mb == 0:
                self.memory_label.setText("Memory: N/A")
                self.cpu_label.setText("CPU: N/A")
                self.last_memory_mb = -1
                self.last_cpu_percent = -1

        except KeyboardInterrupt as ke:
            # Allow graceful exit on keyboard interrupt
            print("Resource monitoring interrupted by user.")
            pass
        except Exception as e:
            # Error getting process info - only update once
            if self.last_memory_mb == 0:
                self.memory_label.setText("Memory: Error")
                self.cpu_label.setText("CPU: Error")
                self.last_memory_mb = -1
                self.last_cpu_percent = -1
    
    def set_monitoring_enabled(self, enabled: bool):
        """Enable or disable resource monitoring"""
        self.monitoring_enabled = enabled
        if enabled:
            # Reset cache when re-enabling
            self.last_memory_mb = 0
            self.last_cpu_percent = 0.0
            self.cpu_measurement_count = 0  # Reset CPU measurement counter
            # Update immediately
            self.update_resources()
        else:
            self.memory_label.setText("Memory: Paused")
            self.cpu_label.setText("CPU: Paused")
    
    def force_update(self):
        """Force an immediate resource update"""
        self.last_memory_mb = 0  # Reset cache to force update
        self.last_cpu_percent = 0.0
        self.cpu_measurement_count = 0  # Reset CPU measurement counter
        self.update_resources()
    
    def debug_cpu_monitoring(self):
        """Debug method to check CPU monitoring status"""
        try:
            import psutil
            import os
            
            debug_info = "CPU Monitoring Debug Info:\n"
            
            # Check psutil version
            debug_info += f"psutil version: {psutil.__version__}\n"
            
            # Get current process
            current_pid = os.getpid()
            process = psutil.Process(current_pid)
            debug_info += f"Current PID: {current_pid}\n"
            
            # Check if process exists
            debug_info += f"Process exists: {process.is_running()}\n"
            
            # Try CPU measurement
            try:
                cpu_percent = process.cpu_percent(interval=0.1)
                debug_info += f"CPU percent (0.1s interval): {cpu_percent}%\n"
            except Exception as e:
                debug_info += f"CPU percent error: {e}\n"
            
            # Try without interval
            try:
                cpu_percent_no_interval = process.cpu_percent()
                debug_info += f"CPU percent (no interval): {cpu_percent_no_interval}%\n"
            except Exception as e:
                debug_info += f"CPU percent (no interval) error: {e}\n"
            
            # System CPU info
            debug_info += f"System CPU count: {psutil.cpu_count()}\n"
            debug_info += f"System CPU percent: {psutil.cpu_percent()}%\n"
            
            return debug_info
            
        except Exception as e:
            return f"Debug error: {e}"


class LogWidget(QTextEdit):
    """Enhanced text widget for displaying logs with syntax highlighting"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        
        # Setup font
        font = QFont("Consolas", 9)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.setFont(font)
        
        # Set dark theme compatible styling
        self.setStyleSheet("""
            QTextEdit {
                background-color: #2B2B2B;
                color: #E0E0E0;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 4px;
            }
            QTextEdit:focus {
                border: 1px solid #0078D4;
            }
        """)
        
        self.auto_scroll = True
    
    def append_log(self, text: str, log_type: str = "info"):
        """Append log entry with styling - optimized version"""
        # Limit log size to prevent memory issues
        if self.document().blockCount() >= 1000:
            # Remove oldest entries (keep last 800 lines)
            cursor = self.textCursor()
            cursor.movePosition(cursor.MoveOperation.Start)
            cursor.movePosition(cursor.MoveOperation.Down, cursor.MoveOperation.MoveAnchor, 200)
            cursor.movePosition(cursor.MoveOperation.End, cursor.MoveOperation.KeepAnchor)
            cursor.removeSelectedText()
            
            # Disable auto-scroll for large logs to improve performance
            if self.document().blockCount() > 500:
                self.auto_scroll = False
        
        color_map = {
            "info": "#E0E0E0",      # Light gray - visible on dark backgrounds
            "warning": "#FFA500",   # Orange - good contrast on both light/dark
            "error": "#FF6B6B",     # Light red - visible on dark backgrounds
            "success": "#4CAF50",   # Green - good contrast on both themes
            "debug": "#9E9E9E"      # Medium gray - visible on dark backgrounds
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
    
    def optimize_log_size(self):
        """Optimize log size by removing old entries"""
        if self.document().blockCount() > 500:
            # Keep only the last 500 lines
            cursor = self.textCursor()
            cursor.movePosition(cursor.MoveOperation.Start)
            cursor.movePosition(cursor.MoveOperation.Down, cursor.MoveOperation.MoveAnchor, self.document().blockCount() - 500)
            cursor.movePosition(cursor.MoveOperation.End, cursor.MoveOperation.KeepAnchor)
            cursor.removeSelectedText()


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
