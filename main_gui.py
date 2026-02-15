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
from src.utils.logger import setup_logging, get_logger

# Initialize logger
logger = get_logger(__name__)


def main():
    """Main entry point for the GUI application."""
    # Setup logging
    setup_logging(log_file_prefix="cse_gui")
    logger.info("Starting CSE Stock Analyzer GUI")
    
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
    try:
        sys.exit(app.exec())
    except Exception as e:
        logger.exception("GUI Application crashed")
        sys.exit(1)


if __name__ == "__main__":
    main()
