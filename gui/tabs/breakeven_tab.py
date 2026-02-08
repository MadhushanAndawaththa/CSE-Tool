"""
Break-Even Calculator tab for CSE Stock Analyzer GUI.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox,
    QLabel, QLineEdit, QRadioButton, QCheckBox, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator, QIntValidator

from src.calculations.breakeven import BreakEvenCalculator
from gui.styles import (
    INFO_CARD_SUCCESS, INFO_CARD_DANGER, INFO_CARD_WARNING,
    TEXT_SECONDARY, TEXT_SECONDARY_DARK,
    get_info_card_style
)


class BreakEvenTab(QWidget):
    """Break-even calculator tab with profit/loss analysis."""

    def __init__(self):
        super().__init__()
        self.calculator = BreakEvenCalculator()
        self.is_dark = False
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(14, 14, 14, 14)

        header = QLabel("Break-Even Price Calculator")
        header.setProperty("heading", True)
        main_layout.addWidget(header)

        # Mode selection
        mode_group = QGroupBox("Calculation Mode")
        mode_layout = QVBoxLayout()
        mode_layout.setSpacing(4)
        mode_layout.setContentsMargins(10, 8, 10, 8)

        self.mode_breakeven = QRadioButton("Calculate break-even price (minimum sell price to break even)")
        self.mode_profit = QRadioButton("Calculate profit/loss at a specific selling price")
        self.mode_breakeven.setChecked(True)
        self.mode_breakeven.toggled.connect(self.on_mode_changed)

        mode_layout.addWidget(self.mode_breakeven)
        mode_layout.addWidget(self.mode_profit)
        mode_group.setLayout(mode_layout)
        main_layout.addWidget(mode_group)

        # Input / Output
        content_layout = QHBoxLayout()
        content_layout.setSpacing(12)
        content_layout.addWidget(self._build_input_panel(), 1)
        self.results_panel = self._build_results_panel()
        content_layout.addWidget(self.results_panel, 1)
        main_layout.addLayout(content_layout, 1)

        self.setLayout(main_layout)

    # ── panels ────────────────────────────────────────────────────────

    def _build_input_panel(self):
        group = QGroupBox("Input Parameters")
        grid = QGridLayout()
        grid.setSpacing(8)
        grid.setContentsMargins(10, 14, 10, 10)

        r = 0
        grid.addWidget(QLabel("Purchase Price (LKR):"), r, 0)
        self.buy_price_input = QLineEdit()
        self.buy_price_input.setPlaceholderText("e.g., 161.25")
        self.buy_price_input.setValidator(QDoubleValidator(0.01, 999999.99, 2))
        self.buy_price_input.returnPressed.connect(self.calculate)
        grid.addWidget(self.buy_price_input, r, 1)

        r += 1
        grid.addWidget(QLabel("Quantity (shares):"), r, 0)
        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("e.g., 500")
        self.quantity_input.setValidator(QIntValidator(1, 99999999))
        self.quantity_input.returnPressed.connect(self.calculate)
        grid.addWidget(self.quantity_input, r, 1)

        r += 1
        self.sell_price_label = QLabel("Selling Price (LKR):")
        self.sell_price_input = QLineEdit()
        self.sell_price_input.setPlaceholderText("e.g., 170.00")
        self.sell_price_input.setValidator(QDoubleValidator(0.01, 999999.99, 2))
        self.sell_price_input.returnPressed.connect(self.calculate)
        grid.addWidget(self.sell_price_label, r, 0)
        grid.addWidget(self.sell_price_input, r, 1)
        self.sell_price_label.hide()
        self.sell_price_input.hide()

        r += 1
        self.include_tax_checkbox = QCheckBox("Include Capital Gains Tax (30%)")
        self.include_tax_checkbox.setChecked(True)
        grid.addWidget(self.include_tax_checkbox, r, 0, 1, 2)

        r += 1
        self.calculate_btn = QPushButton("Calculate")
        self.calculate_btn.clicked.connect(self.calculate)
        grid.addWidget(self.calculate_btn, r, 0, 1, 2)

        r += 1
        clear_btn = QPushButton("Clear")
        clear_btn.setProperty("buttonStyle", "secondary")
        clear_btn.clicked.connect(self.clear_inputs)
        grid.addWidget(clear_btn, r, 0, 1, 2)

        grid.setRowStretch(r + 1, 1)
        group.setLayout(grid)
        return group

    def _build_results_panel(self):
        group = QGroupBox("Results")
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(10, 14, 10, 10)

        self.results_label = QLabel("Enter values and click Calculate to see results")
        self.results_label.setWordWrap(True)
        self.results_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.results_label.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 12px; padding: 12px;")
        layout.addWidget(self.results_label)

        self.results_table = QTableWidget()
        self.results_table.setColumnCount(2)
        self.results_table.setHorizontalHeaderLabels(["Metric", "Value"])
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

    def on_mode_changed(self):
        if self.mode_profit.isChecked():
            self.sell_price_label.show(); self.sell_price_input.show()
        else:
            self.sell_price_label.hide(); self.sell_price_input.hide()

    def calculate(self):
        try:
            if not self.buy_price_input.text() or not self.quantity_input.text():
                self._show_msg(QMessageBox.Icon.Warning, "Input Required",
                    "Please enter both purchase price and quantity.")
                return
            buy_price = float(self.buy_price_input.text())
            quantity = int(self.quantity_input.text())
            include_tax = self.include_tax_checkbox.isChecked()

            if self.mode_profit.isChecked():
                if not self.sell_price_input.text():
                    self._show_msg(QMessageBox.Icon.Warning, "Input Required", "Please enter selling price.")
                    return
                sell_price = float(self.sell_price_input.text())
                result = self.calculator.calculate_profit_at_price(buy_price, sell_price, quantity, include_tax)
                self._show_profit_results(result)
            else:
                result = self.calculator.calculate_breakeven_price(buy_price, quantity, include_tax)
                self._show_breakeven_results(result)
        except ValueError as e:
            self._show_msg(QMessageBox.Icon.Critical, "Calculation Error", f"Invalid input: {e}")
        except Exception as e:
            self._show_msg(QMessageBox.Icon.Critical, "Error", str(e))

    # ── display helpers ───────────────────────────────────────────────

    def _populate_table(self, data):
        self.results_table.setRowCount(0)
        self.results_table.show()
        for label, value in data:
            row = self.results_table.rowCount()
            self.results_table.insertRow(row)
            i1, i2 = QTableWidgetItem(label), QTableWidgetItem(value)
            if label in ("BREAK-EVEN PRICE", "NET PROFIT/LOSS"):
                f = i1.font(); f.setBold(True); i1.setFont(f); i2.setFont(f)
            self.results_table.setItem(row, 0, i1)
            self.results_table.setItem(row, 1, i2)
        self.results_table.resizeColumnsToContents()

    def _show_breakeven_results(self, r):
        data = [
            ("Purchase Price", f"LKR {r['buy_price']:.2f}"),
            ("Quantity", f"{r['quantity']:,} shares"),
            ("", ""),
            ("Total Investment", f"LKR {r['total_investment']:,.2f}"),
            ("Buy Fees Paid", f"LKR {r['buy_fees_paid']:,.2f}"),
            ("", ""),
            ("BREAK-EVEN PRICE", f"LKR {r['breakeven_price']:.2f}"),
            ("Price Increase Required", f"LKR {r['price_increase_required']:.2f}"),
            ("Percentage Increase", f"{r['price_increase_percentage'] * 100:.2f}%"),
            ("", ""),
            ("Sell Value at Break-Even", f"LKR {r['sell_value_at_breakeven']:,.2f}"),
            ("Sell Fees at Break-Even", f"LKR {r['sell_fees_at_breakeven']:,.2f}"),
        ]
        if r['includes_capital_gains_tax']:
            data.append(("Capital Gains Tax", "Yes (30%)"))
        self._populate_table(data)
        self.results_label.setText(
            f"<div style='{get_info_card_style('success', self.is_dark)}'>"
            f"<b>Break-Even: LKR {r['breakeven_price']:.2f}</b><br>"
            f"Price increase: LKR {r['price_increase_required']:.2f} "
            f"({r['price_increase_percentage'] * 100:.2f}%)</div>"
        )

    def _show_profit_results(self, r):
        is_profit = r['net_profit'] > 0
        data = [
            ("Purchase Price", f"LKR {r['buy_price']:.2f}"),
            ("Selling Price", f"LKR {r['sell_price']:.2f}"),
            ("Quantity", f"{r['quantity']:,} shares"),
            ("Price Change", f"LKR {r['sell_price'] - r['buy_price']:.2f}"),
            ("", ""),
            ("Total Investment", f"LKR {r['total_investment']:,.2f}"),
            ("Total Fees Paid", f"LKR {r['total_fees']:,.2f}"),
            ("Gross Profit/Loss", f"LKR {r['gross_profit']:,.2f}"),
            ("Capital Gains Tax", f"LKR {r['capital_gains_tax']:,.2f}"),
            ("", ""),
            ("NET PROFIT/LOSS", f"LKR {r['net_profit']:,.2f}"),
            ("Return Percentage", f"{r['profit_percentage'] * 100:.2f}%"),
            ("", ""),
            ("Break-Even Price", f"LKR {r['breakeven_price']:.2f}"),
            ("Above/Below BE", f"LKR {r['price_vs_breakeven']:.2f}"),
        ]
        self._populate_table(data)
        style = get_info_card_style('success', self.is_dark) if is_profit else get_info_card_style('danger', self.is_dark)
        tag = "PROFIT" if is_profit else "LOSS"
        self.results_label.setText(
            f"<div style='{style}'>"
            f"<b>{tag}: LKR {r['net_profit']:,.2f}</b><br>"
            f"Return: {r['profit_percentage'] * 100:.2f}% | "
            f"BE: LKR {r['breakeven_price']:.2f}</div>"
        )

    def clear_inputs(self):
        self.buy_price_input.clear()
        self.quantity_input.clear()
        self.sell_price_input.clear()
        self.include_tax_checkbox.setChecked(True)
        self.mode_breakeven.setChecked(True)
        self.results_table.hide()
        self.results_label.setText("Enter values and click Calculate to see results")
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
