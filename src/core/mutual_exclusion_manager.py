"""
Mutual Exclusion Manager - Handles GUI-level mutual exclusion for SQLmap options
"""

from typing import Dict, List, Set, Any, Optional
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal, QObject


class MutualExclusionManager(QObject):
    """Manages mutual exclusion groups across the GUI"""

    option_state_changed = pyqtSignal(str, bool)  # option_name, enabled

    def __init__(self):
        super().__init__()
        # Define mutual exclusion groups
        self.mutual_exclusions = {
            'target_input': ['url', 'direct', 'log_file', 'bulk_file', 'request_file', 'google_dork'],
            'user_agent_type': ['user_agent', 'random_agent', 'mobile'],
            'proxy_type': ['proxy', 'tor'],
            'shell_access': ['sql_shell', 'os_shell', 'os_cmd'],
            'data_output': ['dump_all', 'sql_query', 'dump'],
            'crawl_vs_threads': ['crawl', 'threads'],
            'batch_vs_wizard': ['batch', 'wizard']
        }

        # Track current state of options
        self.option_states = {}  # option_name -> current_value
        self.option_widgets = {}  # option_name -> widget

        # Build reverse mapping for quick lookup
        self.option_to_groups = {}
        for group_name, options in self.mutual_exclusions.items():
            for option in options:
                if option not in self.option_to_groups:
                    self.option_to_groups[option] = []
                self.option_to_groups[option].append(group_name)

    def register_option(self, option_name: str, widget: QWidget):
        """Register an option widget for mutual exclusion management"""
        self.option_widgets[option_name] = widget
        self.option_states[option_name] = self._get_widget_value(widget)

    def update_option_state(self, option_name: str, value: Any):
        """Update the state of an option and handle mutual exclusions"""
        old_value = self.option_states.get(option_name)
        self.option_states[option_name] = value

        # Only process mutual exclusions if the value actually changed
        if old_value != value:
            self._handle_mutual_exclusions(option_name, value)

    def _handle_mutual_exclusions(self, changed_option: str, new_value: Any):
        """Handle mutual exclusion logic when an option changes"""
        if changed_option not in self.option_to_groups:
            return

        # Get all groups this option belongs to
        groups = self.option_to_groups[changed_option]

        for group_name in groups:
            group_options = self.mutual_exclusions[group_name]

            # If this option is now set (has a value), disable all other options in the group
            if self._has_value(new_value):
                for option in group_options:
                    if option != changed_option:
                        self._disable_option(option, f"Disabled: conflicts with '{changed_option}' in {group_name} group")
            else:
                # If this option is now unset, check if we need to re-enable other options
                self._reevaluate_group(group_name)

    def _reevaluate_group(self, group_name: str):
        """Re-evaluate the state of a mutual exclusion group"""
        group_options = self.mutual_exclusions[group_name]

        # Find which options in this group currently have values
        active_options = []
        for option in group_options:
            if option in self.option_states and self._has_value(self.option_states[option]):
                active_options.append(option)

        if len(active_options) <= 1:
            # Either no options or only one option is active, so all others can be enabled
            for option in group_options:
                if option not in active_options:
                    self._enable_option(option)
        else:
            # Multiple options are active (shouldn't happen, but handle gracefully)
            # Keep the first one active and disable the rest
            for i, option in enumerate(active_options):
                if i > 0:
                    self._disable_option(option, f"Disabled: conflicts with active options in {group_name} group")

    def _disable_option(self, option_name: str, reason: str):
        """Disable an option widget"""
        if option_name in self.option_widgets:
            widget = self.option_widgets[option_name]
            # For file inputs, we need to disable the container if it exists
            container = self._find_container_for_option(option_name, widget)
            if container:
                container.setEnabled(False)
                container.setToolTip(reason)
            else:
                widget.setEnabled(False)
                widget.setToolTip(reason)
            # Emit signal for additional handling
            self.option_state_changed.emit(option_name, False)

    def _enable_option(self, option_name: str):
        """Enable an option widget"""
        if option_name in self.option_widgets:
            widget = self.option_widgets[option_name]
            # For file inputs, we need to enable the container if it exists
            container = self._find_container_for_option(option_name, widget)
            if container:
                container.setEnabled(True)
                container.setToolTip("")
            else:
                widget.setEnabled(True)
                widget.setToolTip("")
            # Emit signal for additional handling
            self.option_state_changed.emit(option_name, True)

    def _find_container_for_option(self, option_name: str, widget) -> Optional[QWidget]:
        """Find the container widget for a file input option"""
        # Walk up the parent hierarchy to find an OptionGroup with _containers
        current = widget.parent()
        while current:
            if hasattr(current, '_containers') and option_name in current._containers:
                return current._containers[option_name]
            current = current.parent()
        return None

    def _has_value(self, value: Any) -> bool:
        """Check if a value represents an active/selected option"""
        if value is None or value == '':
            return False
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return len(value.strip()) > 0
        return True

    def _get_widget_value(self, widget: QWidget) -> Any:
        """Get the current value from a widget"""
        # This is a simplified version - in practice, we'd need to handle different widget types
        # The actual implementation would be in the OptionGroup class
        return None

    def get_disabled_options(self) -> Set[str]:
        """Get set of currently disabled option names"""
        disabled = set()
        for option_name, widget in self.option_widgets.items():
            if not widget.isEnabled():
                disabled.add(option_name)
        return disabled

    def reset_all(self):
        """Reset all mutual exclusion states"""
        for option_name in self.option_widgets.keys():
            self._enable_option(option_name)
        self.option_states.clear()