"""
Main window for CSE Stock Analyzer GUI application.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QMenuBar, QMenu, QToolBar, QStatusBar, QMessageBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon

from gui.tabs.breakeven_tab import BreakEvenTab
from gui.tabs.fees_tab import FeesTab
from gui.tabs.fundamental_tab import FundamentalTab
from gui.tabs.technical_tab import TechnicalTab
from gui.tabs.complete_analysis_tab import CompleteAnalysisTab


class MainWindow(QMainWindow):
    """Main application window with tab-based interface."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CSE Stock Analyzer")
        self.setMinimumSize(1200, 800)
        
        # Initialize UI components
        self.init_ui()
        self.create_menus()
        self.create_toolbar()
        self.create_status_bar()
        
    def init_ui(self):
        """Initialize the user interface."""
        # Create central widget with tab interface
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setMovable(False)
        self.tabs.setDocumentMode(False)
        
        # Add tabs
        self.breakeven_tab = BreakEvenTab()
        self.fees_tab = FeesTab()
        self.fundamental_tab = FundamentalTab()
        self.technical_tab = TechnicalTab()
        self.complete_tab = CompleteAnalysisTab()
        
        self.tabs.addTab(self.breakeven_tab, "💰 Break-Even Calculator")
        self.tabs.addTab(self.fees_tab, "📊 Fee Information")
        self.tabs.addTab(self.fundamental_tab, "📈 Fundamental Analysis")
        self.tabs.addTab(self.technical_tab, "📉 Technical Analysis")
        self.tabs.addTab(self.complete_tab, "🎯 Complete Analysis")
        
        # Set central widget
        self.setCentralWidget(self.tabs)
        
    def create_menus(self):
        """Create menu bar."""
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu("&File")
        
        new_action = QAction("&New Analysis", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_analysis)
        file_menu.addAction(new_action)
        
        file_menu.addSeparator()
        
        export_action = QAction("&Export Results", self)
        export_action.setShortcut("Ctrl+E")
        export_action.triggered.connect(self.export_results)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Tools Menu
        tools_menu = menubar.addMenu("&Tools")
        
        clear_action = QAction("&Clear Current Tab", self)
        clear_action.setShortcut("Ctrl+L")
        clear_action.triggered.connect(self.clear_current_tab)
        tools_menu.addAction(clear_action)
        
        # Help Menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def create_toolbar(self):
        """Create toolbar."""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(toolbar)
        
        # New button
        new_btn = QAction("New", self)
        new_btn.setStatusTip("Start a new analysis")
        new_btn.triggered.connect(self.new_analysis)
        toolbar.addAction(new_btn)
        
        toolbar.addSeparator()
        
        # Export button
        export_btn = QAction("Export", self)
        export_btn.setStatusTip("Export current results")
        export_btn.triggered.connect(self.export_results)
        toolbar.addAction(export_btn)
        
        toolbar.addSeparator()
        
        # Help button
        help_btn = QAction("Help", self)
        help_btn.setStatusTip("Show help information")
        help_btn.triggered.connect(self.show_about)
        toolbar.addAction(help_btn)
        
    def create_status_bar(self):
        """Create status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
    def new_analysis(self):
        """Start a new analysis by clearing current tab."""
        self.clear_current_tab()
        self.status_bar.showMessage("Started new analysis", 3000)
        
    def clear_current_tab(self):
        """Clear the current active tab."""
        current_tab = self.tabs.currentWidget()
        if hasattr(current_tab, 'clear_inputs'):
            current_tab.clear_inputs()
            self.status_bar.showMessage("Cleared inputs", 3000)
        
    def export_results(self):
        """Export current results (placeholder)."""
        QMessageBox.information(
            self,
            "Export Results",
            "Export functionality will be implemented in a future update."
        )
        
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About CSE Stock Analyzer",
            """<h2>CSE Stock Analyzer</h2>
            <p><b>Version:</b> 1.0.0</p>
            <p>Professional stock analysis tool for the Colombo Stock Exchange (CSE).</p>
            <p><b>Features:</b></p>
            <ul>
                <li>Break-even price calculation with CSE fees</li>
                <li>Profit/Loss analysis at specific prices</li>
                <li>Fundamental analysis metrics</li>
                <li>Technical analysis indicators</li>
                <li>Complete stock recommendations</li>
            </ul>
            <p><b>CSE Fee Structure:</b> Includes broker commissions, SEC fees, 
            CSE fees, CDS fees, STL tax, and 30% capital gains tax.</p>
            <p>© 2026 CSE Tools. All rights reserved.</p>
            """
        )
        
    def update_status(self, message, timeout=0):
        """Update status bar message."""
        self.status_bar.showMessage(message, timeout)
