"""
PyQt6 GUI Application Entry Point for CSE Stock Analyzer.

This is the main entry point for the desktop GUI version of the 
CSE Stock Analyzer. Run this file to launch the GUI application.

Usage:
    python main_gui.py
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from gui.main_window import MainWindow
from gui.styles import GLOBAL_STYLESHEET


def main():
    """Main entry point for the GUI application."""
    # Enable High DPI scaling for better display on 4K monitors
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    # Create application instance
    app = QApplication(sys.argv)
    
    # Set application metadata
    app.setApplicationName("CSE Stock Analyzer")
    app.setOrganizationName("CSE Tools")
    app.setApplicationVersion("1.0.0")
    
    # Set modern Fusion style (cross-platform)
    app.setStyle('Fusion')
    
    # Apply global stylesheet
    app.setStyleSheet(GLOBAL_STYLESHEET)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
