"""
Fundamental Analysis tab for CSE Stock Analyzer GUI.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator

from src.calculations.fundamental import FundamentalAnalyzer
from gui.styles import (
    INFO_CARD_SUCCESS, INFO_CARD_WARNING, INFO_CARD_DANGER,
    TEXT_SECONDARY, TEXT_SECONDARY_DARK,
    get_info_card_style
)


class FundamentalTab(QWidget):
    """Fundamental analysis tab."""

    def __init__(self):
        super().__init__()
        self.analyzer = FundamentalAnalyzer()
        self.is_dark = False
        # declare input attributes (set in _build_input_panel)
        self.symbol_input: QLineEdit = None  # type: ignore
        self.price_input: QLineEdit = None  # type: ignore
        self.eps_input: QLineEdit = None  # type: ignore
        self.book_value_input: QLineEdit = None  # type: ignore
        self.net_income_input: QLineEdit = None  # type: ignore
        self.equity_input: QLineEdit = None  # type: ignore
        self.debt_input: QLineEdit = None  # type: ignore
        self.current_assets_input: QLineEdit = None  # type: ignore
        self.current_liabilities_input: QLineEdit = None  # type: ignore
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(14, 14, 14, 14)

        header = QLabel("Fundamental Analysis")
        header.setProperty("heading", True)
        main_layout.addWidget(header)

        content = QHBoxLayout()
        content.setSpacing(12)
        content.setContentsMargins(0, 0, 0, 0)
        input_panel = self._build_input_panel()
        input_panel.setMinimumWidth(320)  # Ensure input panel doesn't get too narrow
        content.addWidget(input_panel, 1)
        self.results_panel = self._build_results_panel()
        content.addWidget(self.results_panel, 1)
        main_layout.addLayout(content, 1)
        self.setLayout(main_layout)

    # ── input panel ───────────────────────────────────────────────────

    def _build_input_panel(self):
        group = QGroupBox("Financial Data Input")
        grid = QGridLayout()
        grid.setSpacing(7)
        grid.setContentsMargins(10, 14, 10, 10)

        fields = [
            ("Stock Symbol:", "symbol_input", "e.g., JKH.N0000", None),
            ("Current Price (LKR):", "price_input", "e.g., 161.25", (0.01, 999999.99)),
            ("EPS:", "eps_input", "e.g., 12.50", (-999999.99, 999999.99)),
            ("Book Value / Share:", "book_value_input", "e.g., 85.00", (0.01, 999999.99)),
            ("Net Income (Mn):", "net_income_input", "e.g., 5000", (-999999.99, 999999999.99)),
            ("Shareholders Equity (Mn):", "equity_input", "e.g., 25000", (0.01, 999999999.99)),
            ("Total Debt (Mn):", "debt_input", "e.g., 10000", (0, 999999999.99)),
            ("Current Assets (Mn):", "current_assets_input", "e.g., 15000", (0.01, 999999999.99)),
            ("Current Liabilities (Mn):", "current_liabilities_input", "e.g., 8000", (0.01, 999999999.99)),
        ]

        for r, (label, attr, placeholder, validator_range) in enumerate(fields):
            grid.addWidget(QLabel(label), r, 0)
            inp = QLineEdit()
            inp.setPlaceholderText(placeholder)
            if validator_range:
                inp.setValidator(QDoubleValidator(validator_range[0], validator_range[1], 2))
            inp.returnPressed.connect(self.analyze)
            setattr(self, attr, inp)
            grid.addWidget(inp, r, 1)

        r = len(fields)
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        btn_row.setContentsMargins(0, 4, 0, 0)

        self.analyze_btn = QPushButton("Analyze")
        self.analyze_btn.clicked.connect(self.analyze)
        self.analyze_btn.setMinimumHeight(32)

        clear_btn = QPushButton("Clear")
        clear_btn.setProperty("buttonStyle", "secondary")
        clear_btn.clicked.connect(self.clear_inputs)
        clear_btn.setMinimumHeight(32)

        btn_row.addWidget(self.analyze_btn)
        btn_row.addWidget(clear_btn)

        btn_widget = QWidget()
        btn_widget.setLayout(btn_row)
        grid.addWidget(btn_widget, r, 0, 1, 2)

        group.setLayout(grid)
        group.setMinimumHeight(420)
        return group

    # ── results panel ─────────────────────────────────────────────────

    def _build_results_panel(self):
        group = QGroupBox("Analysis Results")
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(10, 14, 10, 10)

        self.results_label = QLabel("Enter financial data and click Analyze to see results")
        self.results_label.setWordWrap(True)
        self.results_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.results_label.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 12px; padding: 12px;")
        layout.addWidget(self.results_label)

        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["Metric", "Value", "Rating"])
        self.results_table.horizontalHeader().setStretchLastSection(True)
        self.results_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.results_table.setAlternatingRowColors(True)
        self.results_table.verticalHeader().setVisible(False)
        self.results_table.verticalHeader().setDefaultSectionSize(28)
        self.results_table.setShowGrid(False)
        self.results_table.hide()
        layout.addWidget(self.results_table)

        group.setLayout(layout)
        return group

    # ── logic ─────────────────────────────────────────────────────────

    def analyze(self):
        try:
            if not all([self.price_input.text(), self.eps_input.text()]):
                self._show_msg(QMessageBox.Icon.Warning, "Input Required",
                    "Please enter at least Current Price and EPS.")
                return

            price = float(self.price_input.text())
            eps = float(self.eps_input.text())
            results = []

            pe = self.analyzer.calculate_pe_ratio(price, eps)
            results.append(("P/E Ratio", f"{pe['pe_ratio']:.2f}", pe['rating']))

            if self.book_value_input.text():
                bv = float(self.book_value_input.text())
                pb = self.analyzer.calculate_pb_ratio(price, bv)
                results.append(("P/B Ratio", f"{pb['pb_ratio']:.2f}", pb['rating']))

            if self.net_income_input.text() and self.equity_input.text():
                ni = float(self.net_income_input.text()) * 1e6
                eq = float(self.equity_input.text()) * 1e6
                roe = self.analyzer.calculate_roe(ni, eq)
                results.append(("ROE", f"{roe['roe']*100:.2f}%", roe['rating']))

            if self.debt_input.text() and self.equity_input.text():
                debt = float(self.debt_input.text()) * 1e6
                eq = float(self.equity_input.text()) * 1e6
                de = self.analyzer.calculate_debt_to_equity(debt, eq)
                results.append(("Debt/Equity", f"{de['debt_to_equity']:.2f}", de['rating']))

            if self.current_assets_input.text() and self.current_liabilities_input.text():
                ca = float(self.current_assets_input.text()) * 1e6
                cl = float(self.current_liabilities_input.text()) * 1e6
                cr = self.analyzer.calculate_current_ratio(ca, cl)
                results.append(("Current Ratio", f"{cr['current_ratio']:.2f}", cr['rating']))

            self._show_results(results)
        except ValueError as e:
            self._show_msg(QMessageBox.Icon.Critical, "Input Error", f"Invalid input: {e}")
        except Exception as e:
            self._show_msg(QMessageBox.Icon.Critical, "Error", str(e))

    def _show_results(self, results):
        self.results_table.setRowCount(0)
        self.results_table.show()

        for metric, value, rating in results:
            row = self.results_table.rowCount()
            self.results_table.insertRow(row)
            self.results_table.setItem(row, 0, QTableWidgetItem(metric))
            self.results_table.setItem(row, 1, QTableWidgetItem(value))
            self.results_table.setItem(row, 2, QTableWidgetItem(rating))
        self.results_table.resizeColumnsToContents()

        exc = sum(1 for _, _, r in results if r == "Excellent")
        good = sum(1 for _, _, r in results if r == "Good")
        fair = sum(1 for _, _, r in results if r == "Fair")
        poor = sum(1 for _, _, r in results if r == "Poor")

        if exc + good >= len(results) * 0.6:
            style, summary = get_info_card_style('success', self.is_dark), "Strong Fundamentals"
        elif poor >= len(results) * 0.5:
            style, summary = get_info_card_style('danger', self.is_dark), "Weak Fundamentals"
        else:
            style, summary = get_info_card_style('warning', self.is_dark), "Mixed Fundamentals"

        self.results_label.setText(
            f"<div style='{style}'>"
            f"<b>{summary}</b><br>"
            f"Excellent: {exc} | Good: {good} | Fair: {fair} | Poor: {poor}</div>"
        )

    def clear_inputs(self):
        for attr in ("symbol_input", "price_input", "eps_input", "book_value_input",
                      "net_income_input", "equity_input", "debt_input",
                      "current_assets_input", "current_liabilities_input"):
            getattr(self, attr).clear()
        self.results_table.hide()
        self.results_label.setText("Enter financial data and click Analyze to see results")
        self._update_results_label_style()

    def _update_results_label_style(self):
        c = TEXT_SECONDARY_DARK if self.is_dark else TEXT_SECONDARY
        self.results_label.setStyleSheet(f"color: {c}; font-size: 12px; padding: 12px;")

    def apply_theme(self, dark_mode: bool):
        self.is_dark = dark_mode
        self._update_results_label_style()

    def _show_msg(self, icon, title, text):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(icon)
        if self.is_dark:
            msg.setStyleSheet("QLabel { color: #e2e4e7; } QMessageBox { background: #1e293b; }")
        msg.exec()
