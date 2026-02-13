"""
Main window for CSE Stock Analyzer GUI application.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QToolBar, QStatusBar, QMessageBox, QLabel, QApplication, QFileDialog
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QColor, QPalette

import qtawesome as qta

try:
    import qdarktheme
except Exception:
    qdarktheme = None

from gui.tabs.breakeven_tab import BreakEvenTab
from gui.tabs.fees_tab import FeesTab
from gui.tabs.fundamental_tab import FundamentalTab
from gui.tabs.technical_tab import TechnicalTab
from gui.tabs.technical_tab import TechnicalTab
from gui.tabs.complete_analysis_tab import CompleteAnalysisTab
from gui.tabs.history_tab import HistoryTab
from gui.styles import GLOBAL_STYLESHEET, GLOBAL_STYLESHEET_DARK

from src.export.pdf_report import generate_pdf_report
from src.export.pdf_report import generate_pdf_report
from src.export.csv_export import export_to_csv, export_to_excel
from src.utils.logger import get_logger

logger = get_logger(__name__)


class MainWindow(QMainWindow):
    """Main application window with tab-based interface."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CSE Stock Analyzer")
        self.setMinimumSize(1100, 720)
        self.dark_mode = False

        self.init_ui()
        self.create_menus()
        self.create_toolbar()
        self.create_status_bar()
        self.apply_theme(False)

        # Dark mode works with or without qdarktheme

    # ── UI setup ──────────────────────────────────────────────────────

    def init_ui(self):
        central = QWidget()
        root = QVBoxLayout()
        root.setContentsMargins(10, 8, 10, 6)
        root.setSpacing(8)

        # compact header bar
        header = QWidget()
        header.setObjectName("HeaderBar")
        header.setFixedHeight(48)

        hl = QHBoxLayout()
        hl.setContentsMargins(14, 0, 14, 0)
        hl.setSpacing(8)

        title = QLabel("CSE Stock Analyzer")
        title.setObjectName("HeaderTitle")

        sep = QLabel("  |  ")
        sep.setStyleSheet("color: rgba(255,255,255,0.4); font-size: 14px;")

        subtitle = QLabel("Colombo Stock Exchange")
        subtitle.setObjectName("HeaderSubtitle")

        hl.addWidget(title)
        hl.addWidget(sep)
        hl.addWidget(subtitle)
        hl.addStretch()

        badge = QLabel("v1.0.0")
        badge.setObjectName("HeaderBadge")
        hl.addWidget(badge)
        header.setLayout(hl)
        root.addWidget(header)

        # tabs
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setMovable(False)
        self.tabs.setDocumentMode(False)

        self.breakeven_tab = BreakEvenTab()
        self.fees_tab = FeesTab()
        self.fundamental_tab = FundamentalTab()
        self.technical_tab = TechnicalTab()
        self.technical_tab = TechnicalTab()
        self.complete_tab = CompleteAnalysisTab()
        self.history_tab = HistoryTab()

        self.tabs.addTab(self.breakeven_tab, "Break-Even")
        self.tabs.addTab(self.fees_tab, "Fees")
        self.tabs.addTab(self.fundamental_tab, "Fundamental")
        self.tabs.addTab(self.technical_tab, "Technical")
        self.tabs.addTab(self.complete_tab, "Complete Analysis")
        self.tabs.addTab(self.history_tab, "History")
        
        # Connect tab change signal
        self.tabs.currentChanged.connect(self.on_tab_changed)

        root.addWidget(self.tabs, 1)
        central.setLayout(root)
        self.setCentralWidget(central)

    # ── Menus ─────────────────────────────────────────────────────────

    def create_menus(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("&File")

        new_action = QAction(qta.icon("fa5s.file", color="#64748b"), "&New Analysis", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_analysis)
        file_menu.addAction(new_action)

        file_menu.addSeparator()

        export_action = QAction(qta.icon("fa5s.file-export", color="#64748b"), "&Export Results", self)
        export_action.setShortcut("Ctrl+E")
        export_action.triggered.connect(self.export_results)
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        exit_action = QAction(qta.icon("fa5s.sign-out-alt", color="#64748b"), "E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        tools_menu = menubar.addMenu("&Tools")
        clear_action = QAction(qta.icon("fa5s.eraser", color="#64748b"), "&Clear Current Tab", self)
        clear_action.setShortcut("Ctrl+L")
        clear_action.triggered.connect(self.clear_current_tab)
        tools_menu.addAction(clear_action)

        view_menu = menubar.addMenu("&View")
        self.dark_mode_action = QAction(qta.icon("fa5s.moon", color="#64748b"), "&Dark Mode", self)
        self.dark_mode_action.setCheckable(True)
        self.dark_mode_action.setChecked(False)
        self.dark_mode_action.triggered.connect(self.toggle_theme)
        view_menu.addAction(self.dark_mode_action)

        help_menu = menubar.addMenu("&Help")
        about_action = QAction(qta.icon("fa5s.info-circle", color="#64748b"), "&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    # ── Toolbar ───────────────────────────────────────────────────────

    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        new_btn = QAction(qta.icon("fa5s.file", color="#64748b"), "New", self)
        new_btn.setStatusTip("Start a new analysis")
        new_btn.triggered.connect(self.new_analysis)
        toolbar.addAction(new_btn)

        export_btn = QAction(qta.icon("fa5s.file-export", color="#64748b"), "Export", self)
        export_btn.setStatusTip("Export current results")
        export_btn.triggered.connect(self.export_results)
        toolbar.addAction(export_btn)

        toolbar.addSeparator()

        theme_btn = QAction(qta.icon("fa5s.adjust", color="#64748b"), "Theme", self)
        theme_btn.setStatusTip("Toggle light / dark mode")
        theme_btn.setCheckable(True)
        theme_btn.setChecked(False)
        theme_btn.triggered.connect(self.toggle_theme)
        self.theme_toolbar_action = theme_btn
        toolbar.addAction(theme_btn)

        help_btn = QAction(qta.icon("fa5s.question-circle", color="#64748b"), "Help", self)
        help_btn.setStatusTip("About this application")
        help_btn.triggered.connect(self.show_about)
        toolbar.addAction(help_btn)

    # ── Status bar ────────────────────────────────────────────────────

    def create_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

    # ── Actions ───────────────────────────────────────────────────────

    def new_analysis(self):
        logger.info("User started new analysis")
        self.clear_current_tab()
        self.status_bar.showMessage("Started new analysis", 3000)

    def clear_current_tab(self):
        tab = self.tabs.currentWidget()
        if hasattr(tab, "clear_inputs"):
            tab.clear_inputs()
            self.status_bar.showMessage("Cleared inputs", 3000)

    def export_results(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Export")
        msg.setText("Export will be available in a future update.")
        msg.setIcon(QMessageBox.Icon.Information)
        if self.dark_mode:
            msg.setStyleSheet("QLabel { color: #e2e4e7; } QMessageBox { background: #1e293b; }")
        msg.exec()

    def show_about(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("About CSE Stock Analyzer")
        msg.setTextFormat(Qt.TextFormat.RichText)
        text_color = "#e2e4e7" if self.dark_mode else "#1e293b"
        msg.setText(
            f"<h3 style='color:{text_color}'>CSE Stock Analyzer v1.0.0</h3>"
            f"<p style='color:{text_color}'>Professional stock analysis for the Colombo Stock Exchange.</p>"
            f"<p style='color:{text_color}'>Break-even, fees, fundamental &amp; technical analysis.</p>"
            f"<p style='color:{text_color}'>&copy; 2026 CSE Tools</p>"
        )
        if self.dark_mode:
            msg.setStyleSheet("QLabel { color: #e2e4e7; } QMessageBox { background: #1e293b; }")
        msg.exec()

    # ── Theme toggle ──────────────────────────────────────────────────

    def toggle_theme(self, checked):
        self.apply_theme(checked)
        # Sync both toggle actions without re-firing signals
        self.dark_mode_action.blockSignals(True)
        self.dark_mode_action.setChecked(checked)
        self.dark_mode_action.blockSignals(False)
        self.theme_toolbar_action.blockSignals(True)
        self.theme_toolbar_action.setChecked(checked)
        self.theme_toolbar_action.blockSignals(False)

    def apply_theme(self, dark_mode: bool):
        app = QApplication.instance()
        if app is None:
            return
        if dark_mode:
            if qdarktheme is not None:
                app.setStyleSheet(qdarktheme.load_stylesheet() + GLOBAL_STYLESHEET_DARK)  # type: ignore
            else:
                # Build a dark palette so Fusion renders dark base colors
                palette = QPalette()
                palette.setColor(QPalette.ColorRole.Window, QColor("#0f172a"))
                palette.setColor(QPalette.ColorRole.WindowText, QColor("#e2e4e7"))
                palette.setColor(QPalette.ColorRole.Base, QColor("#1e293b"))
                palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#0f172a"))
                palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#1e293b"))
                palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#e2e4e7"))
                palette.setColor(QPalette.ColorRole.Text, QColor("#e2e4e7"))
                palette.setColor(QPalette.ColorRole.Button, QColor("#1e293b"))
                palette.setColor(QPalette.ColorRole.ButtonText, QColor("#e2e4e7"))
                palette.setColor(QPalette.ColorRole.BrightText, QColor("#ffffff"))
                palette.setColor(QPalette.ColorRole.Link, QColor("#93c5fd"))
                palette.setColor(QPalette.ColorRole.Highlight, QColor("#2563eb"))
                palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
                palette.setColor(QPalette.ColorRole.PlaceholderText, QColor("#64748b"))
                palette.setColor(QPalette.ColorRole.Light, QColor("#334155"))
                palette.setColor(QPalette.ColorRole.Midlight, QColor("#1e293b"))
                palette.setColor(QPalette.ColorRole.Dark, QColor("#0f172a"))
                palette.setColor(QPalette.ColorRole.Mid, QColor("#334155"))
                palette.setColor(QPalette.ColorRole.Shadow, QColor("#000000"))
                app.setPalette(palette)  # type: ignore
                app.setStyleSheet(GLOBAL_STYLESHEET_DARK)  # type: ignore
        else:
            app.setPalette(self.style().standardPalette())  # type: ignore
            app.setStyleSheet(GLOBAL_STYLESHEET)  # type: ignore
        self.dark_mode = dark_mode
        self.dark_mode = dark_mode
        for tab in [self.breakeven_tab, self.fees_tab, self.fundamental_tab,
                     self.technical_tab, self.complete_tab, self.history_tab]:
            if hasattr(tab, "apply_theme"):
                tab.apply_theme(dark_mode)

    def on_tab_changed(self, index):
        """Handle tab changes."""
        # Refresh history if history tab (index 5) is selected
        if self.tabs.widget(index) == self.history_tab:
            self.history_tab.refresh_history()

    def update_status(self, message, timeout=0):
        self.status_bar.showMessage(message, timeout)
    def export_results(self):
        """Export analysis results to PDF, CSV, or Excel."""
        logger.info("User requested export results")
        # Get result from the active tab (currently only Complete Analysis tab supports full export)
        # We check if CompleteAnalysisTab has 'last_result' attribute
        
        if not hasattr(self.complete_tab, 'last_result') or not self.complete_tab.last_result:
            logger.warning("Export failed: No analysis results available")
            QMessageBox.warning(self, "Export Error", "No analysis results available to export.\nPlease run an analysis first.")
            return
            
        result = self.complete_tab.last_result
        
        # Open file dialog
        filepath, filter_type = QFileDialog.getSaveFileName(
            self,
            "Export Results",
            "",
            "PDF Report (*.pdf);;CSV File (*.csv);;Excel File (*.xlsx)"
        )
        
        if not filepath:
            logger.info("Export cancelled by user")
            return
            
        try:
            logger.info(f"Exporting results to {filepath} with filter {filter_type}")
            if filter_type.startswith("PDF"):
                if not filepath.lower().endswith('.pdf'):
                    filepath += '.pdf'
                saved_path = generate_pdf_report(result, filepath)
                
            elif filter_type.startswith("CSV"):
                if not filepath.lower().endswith('.csv'):
                    filepath += '.csv'
                saved_path = export_to_csv(result, filepath)
                
            elif filter_type.startswith("Excel"):
                if not filepath.lower().endswith('.xlsx'):
                    filepath += '.xlsx'
                saved_path = export_to_excel(result, filepath)
                
            else:
                # Default to PDF if something weird happens (or infer from extension)
                if filepath.lower().endswith('.csv'):
                    saved_path = export_to_csv(result, filepath)
                elif filepath.lower().endswith('.xlsx'):
                    saved_path = export_to_excel(result, filepath)
                else:
                    if not filepath.lower().endswith('.pdf'):
                        filepath += '.pdf'
                    saved_path = generate_pdf_report(result, filepath)

            QMessageBox.information(self, "Export Successful", f"Report saved successfully to:\n{saved_path}")
            logger.info(f"Export successful to {saved_path}")
            
        except Exception as e:
            logger.exception(f"Export failed: {str(e)}")
            QMessageBox.critical(self, "Export Failed", f"Failed to export report:\n{str(e)}")
