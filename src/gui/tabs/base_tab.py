"""
Base Tab Class - Common functionality for all tabs
"""

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal
from typing import Dict, Any

from ..widgets.custom_widgets import OptionGroup


class BaseTab(QWidget):
    """Base class for all tab widgets"""
    
    options_changed = pyqtSignal()
    
    def __init__(self, parent=None, mutual_exclusion_manager=None):
        super().__init__(parent)
        self.mutual_exclusion_manager = mutual_exclusion_manager

    def get_options(self) -> Dict[str, Any]:
        """Get all options from this tab"""
        options = {}
        
        try:
            # Navigate through scroll area to get option groups
            if self.layout() and self.layout().count() > 0:
                scroll_area = self.layout().itemAt(0).widget()
                if scroll_area and hasattr(scroll_area, 'widget'):
                    scroll_content = scroll_area.widget()
                    if scroll_content and hasattr(scroll_content, 'layout'):
                        content_layout = scroll_content.layout()
                        if content_layout:
                            for i in range(content_layout.count()):
                                item = content_layout.itemAt(i)
                                if item and item.widget() and isinstance(item.widget(), OptionGroup):
                                    group_options = item.widget().get_values()
                                    options.update(group_options)
        except Exception as e:
            print(f"Error getting options from tab: {e}")
        
        # Filter out empty values
        return {k: v for k, v in options.items() if v is not None and v != ''}
    
    def set_options(self, options: Dict[str, Any]):
        """Set options in this tab"""
        try:
            if self.layout() and self.layout().count() > 0:
                scroll_area = self.layout().itemAt(0).widget()
                if scroll_area and hasattr(scroll_area, 'widget'):
                    scroll_content = scroll_area.widget()
                    if scroll_content and hasattr(scroll_content, 'layout'):
                        content_layout = scroll_content.layout()
                        if content_layout:
                            for i in range(content_layout.count()):
                                item = content_layout.itemAt(i)
                                if item and item.widget() and isinstance(item.widget(), OptionGroup):
                                    item.widget().set_values(options)
        except Exception as e:
            print(f"Error setting options in tab: {e}")
    
    def reset_options(self):
        """Reset all options to defaults"""
        try:
            if self.layout() and self.layout().count() > 0:
                scroll_area = self.layout().itemAt(0).widget()
                if scroll_area and hasattr(scroll_area, 'widget'):
                    scroll_content = scroll_area.widget()
                    if scroll_content and hasattr(scroll_content, 'layout'):
                        content_layout = scroll_content.layout()
                        if content_layout:
                            for i in range(content_layout.count()):
                                item = content_layout.itemAt(i)
                                if item and item.widget() and isinstance(item.widget(), OptionGroup):
                                    item.widget().set_values({})
        except Exception as e:
            print(f"Error resetting options in tab: {e}")
