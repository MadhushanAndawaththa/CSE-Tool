"""
Main window for CSE Stock Analyzer GUI application.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QToolBar, QStatusBar, QMessageBox, QLabel, QApplication
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction

import qtawesome as qta

try:
    import qdarktheme
except Exception:
    qdarktheme = None

from gui.tabs.breakeven_tab import BreakEvenTab
from gui.tabs.fees_tab import FeesTab
from gui.tabs.fundamental_tab import FundamentalTab
from gui.tabs.technical_tab import TechnicalTab
from gui.tabs.complete_analysis_tab import CompleteAnalysisTab
from gui.styles import GLOBAL_STYLESHEET, GLOBAL_STYLESHEET_DARK


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

        if qdarktheme is None:
            self.dark_mode_action.setEnabled(False)
            self.theme_toolbar_action.setEnabled(False)

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
        self.complete_tab = CompleteAnalysisTab()

        self.tabs.addTab(self.breakeven_tab, "Break-Even")
        self.tabs.addTab(self.fees_tab, "Fees")
        self.tabs.addTab(self.fundamental_tab, "Fundamental")
        self.tabs.addTab(self.technical_tab, "Technical")
        self.tabs.addTab(self.complete_tab, "Complete Analysis")

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
        if self.dark_mode_action.isChecked() != checked:
            self.dark_mode_action.setChecked(checked)
        if self.theme_toolbar_action.isChecked() != checked:
            self.theme_toolbar_action.setChecked(checked)

    def apply_theme(self, dark_mode: bool):
        app = QApplication.instance()
        if app is None:
            return
        if dark_mode:
            if qdarktheme is not None:
                app.setStyleSheet(qdarktheme.load_stylesheet() + GLOBAL_STYLESHEET_DARK)  # type: ignore
            else:
                app.setStyleSheet(GLOBAL_STYLESHEET_DARK)  # type: ignore
        else:
            app.setStyleSheet(GLOBAL_STYLESHEET)  # type: ignore
        self.dark_mode = dark_mode
        for tab in [self.breakeven_tab, self.fees_tab, self.fundamental_tab,
                     self.technical_tab, self.complete_tab]:
            if hasattr(tab, "apply_theme"):
                tab.apply_theme(dark_mode)

    def update_status(self, message, timeout=0):
        self.status_bar.showMessage(message, timeout)
