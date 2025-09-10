#!/usr/bin/env python3
"""
SQLmap GUI Application
Main entry point for the SQLmap graphical user interface
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from src.gui.main_window import SqlmapMainWindow


def setup_application():
    """Setup the PyQt6 application"""
    # Create application
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("SQLmap GUI")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("SQLmap GUI")
    app.setOrganizationDomain("sqlmap-gui.local")
    
    # Set application style
    app.setStyle("Fusion")
    
    # Enable high DPI scaling (commented out as these attributes are deprecated in newer Qt versions)
    # app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    # app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    
    return app


def main():
    """Main application entry point"""
    try:
        # Create and setup application
        app = setup_application()
        
        # Create and show main window
        main_window = SqlmapMainWindow()
        main_window.show()
        
        # Center window on screen
        screen = app.primaryScreen().geometry()
        window_rect = main_window.geometry()
        x = (screen.width() - window_rect.width()) // 2
        y = (screen.height() - window_rect.height()) // 2
        main_window.move(x, y)
        
        # Start application event loop
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"Error starting SQLmap GUI: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
