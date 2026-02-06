"""
Fee Information tab for CSE Stock Analyzer GUI.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator, QIntValidator

from src.fees.cse_fees import CSEFeeCalculator
from gui.styles import CARD_STYLE


class FeesTab(QWidget):
    """Fee information and calculator tab."""

    def __init__(self):
        super().__init__()
        self.fee_calculator = CSEFeeCalculator()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(14, 14, 14, 14)

        header = QLabel("CSE Fee Structure & Calculator")
        header.setProperty("heading", True)
        main_layout.addWidget(header)

        content = QHBoxLayout()
        content.setSpacing(12)
        content.addWidget(self._build_calculator(), 1)
        content.addWidget(self._build_info_panel(), 1)
        main_layout.addLayout(content, 1)
        self.setLayout(main_layout)

    # ── calculator ────────────────────────────────────────────────────

    def _build_calculator(self):
        group = QGroupBox("Interactive Fee Calculator")
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(10, 14, 10, 10)

        grid = QGridLayout()
        grid.setSpacing(8)
        grid.addWidget(QLabel("Transaction Value (LKR):"), 0, 0)
        self.transaction_value_input = QLineEdit()
        self.transaction_value_input.setPlaceholderText("e.g., 80625")
        self.transaction_value_input.setValidator(QDoubleValidator(0.01, 999999999.99, 2))
        grid.addWidget(self.transaction_value_input, 0, 1)

        grid.addWidget(QLabel("Number of Shares:"), 1, 0)
        self.shares_input = QLineEdit()
        self.shares_input.setPlaceholderText("e.g., 500")
        self.shares_input.setValidator(QIntValidator(1, 99999999))
        grid.addWidget(self.shares_input, 1, 1)
        layout.addLayout(grid)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        self.calc_buy_btn = QPushButton("Calculate Buy Fees")
        self.calc_buy_btn.clicked.connect(lambda: self.calculate_fees("buy"))
        btn_row.addWidget(self.calc_buy_btn)
        self.calc_sell_btn = QPushButton("Calculate Sell Fees")
        self.calc_sell_btn.setProperty("buttonStyle", "success")
        self.calc_sell_btn.clicked.connect(lambda: self.calculate_fees("sell"))
        btn_row.addWidget(self.calc_sell_btn)
        layout.addLayout(btn_row)

        self.fee_table = QTableWidget()
        self.fee_table.setColumnCount(3)
        self.fee_table.setHorizontalHeaderLabels(["Fee Type", "Rate", "Amount (LKR)"])
        self.fee_table.horizontalHeader().setStretchLastSection(True)
        self.fee_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.fee_table.setAlternatingRowColors(True)
        self.fee_table.verticalHeader().setVisible(False)
        self.fee_table.verticalHeader().setDefaultSectionSize(28)
        self.fee_table.setShowGrid(False)
        layout.addWidget(self.fee_table)

        clear_btn = QPushButton("Clear")
        clear_btn.setProperty("buttonStyle", "secondary")
        clear_btn.clicked.connect(self.clear_inputs)
        layout.addWidget(clear_btn)

        group.setLayout(layout)
        return group

    # ── info panel ────────────────────────────────────────────────────

    def _build_info_panel(self):
        group = QGroupBox("CSE Fee Structure Reference")
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(10, 14, 10, 10)

        tier_info = QLabel(
            "<b>Tier 1:</b> Transactions <= Rs. 100,000,000  &nbsp;|&nbsp;  "
            "<b>Tier 2:</b> Transactions > Rs. 100,000,000"
        )
        tier_info.setWordWrap(True)
        layout.addWidget(tier_info)

        # Tier 1
        layout.addWidget(QLabel("<b>Tier 1 Fees:</b>"))
        t1 = self._make_tier_table([
            ("Broker Commission", "0.64%"),
            ("SEC Fee", "0.072%"),
            ("CSE Fee", "0.084%"),
            ("CDS Fee", "0.024%"),
            ("STL Tax (Sell only)", "0.30%"),
        ])
        layout.addWidget(t1)

        # Tier 2
        layout.addWidget(QLabel("<b>Tier 2 Fees:</b>"))
        t2 = self._make_tier_table([
            ("Broker Commission", "Min 0.20%"),
            ("SEC Fee", "0.042%"),
            ("CSE Fee", "0.054%"),
            ("CDS Fee", "0.024%"),
            ("STL Tax (Sell only)", "0.30%"),
        ])
        layout.addWidget(t2)

        tax_lbl = QLabel(
            "<b>Capital Gains Tax:</b> 30% on net profit "
            "<span style='color:#64748b;'>(Gross Profit - Total Fees)</span>"
        )
        tax_lbl.setWordWrap(True)
        layout.addWidget(tax_lbl)

        layout.addStretch()
        group.setLayout(layout)
        return group

    @staticmethod
    def _make_tier_table(rows):
        t = QTableWidget()
        t.setColumnCount(2)
        t.setHorizontalHeaderLabels(["Fee Component", "Rate"])
        t.setRowCount(len(rows))
        t.setAlternatingRowColors(True)
        t.verticalHeader().setVisible(False)
        t.verticalHeader().setDefaultSectionSize(26)
        t.setShowGrid(False)
        t.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        t.setMaximumHeight(26 * len(rows) + 30)
        for i, (comp, rate) in enumerate(rows):
            t.setItem(i, 0, QTableWidgetItem(comp))
            t.setItem(i, 1, QTableWidgetItem(rate))
        t.resizeColumnsToContents()
        t.horizontalHeader().setStretchLastSection(True)
        return t

    # ── logic ─────────────────────────────────────────────────────────

    def calculate_fees(self, fee_type):
        try:
            if not self.transaction_value_input.text() or not self.shares_input.text():
                QMessageBox.warning(self, "Input Error", "Please enter transaction value and number of shares.")
                return
            tv = float(self.transaction_value_input.text())
            shares = int(float(self.shares_input.text()))
            if fee_type == "buy":
                result = self.fee_calculator.calculate_buy_fees(tv, shares)
            else:
                result = self.fee_calculator.calculate_sell_fees(tv, shares)
            self._show_fee_results(result)
        except ValueError:
            QMessageBox.critical(self, "Input Error", "Please enter valid numbers.")
        except Exception as e:
            QMessageBox.critical(self, "Calculation Error", str(e))

    def _show_fee_results(self, r):
        self.fee_table.setRowCount(0)
        data = [
            ("Transaction Value", "", f"{r['transaction_value']:,.2f}"),
            ("", "", ""),
            ("Broker Commission", f"{r['broker_commission_rate']*100:.3f}%", f"{r['broker_commission']:,.2f}"),
            ("SEC Fee", f"{r['sec_fee_rate']*100:.3f}%", f"{r['sec_fee']:,.2f}"),
            ("CSE Fee", f"{r['cse_fee_rate']*100:.3f}%", f"{r['cse_fee']:,.2f}"),
            ("CDS Fee", f"{r['cds_fee_rate']*100:.3f}%", f"{r['cds_fee']:,.2f}"),
        ]
        if "stl_tax" in r:
            data.append(("STL Tax", f"{r['stl_tax_rate']*100:.2f}%", f"{r['stl_tax']:,.2f}"))
        data.append(("", "", ""))
        data.append(("TOTAL FEES", f"{r['total_fee_percentage']*100:.3f}%", f"{r['total_fees']:,.2f}"))
        if "net_proceeds" in r:
            data.append(("Net Proceeds", "", f"{r['net_proceeds']:,.2f}"))
        else:
            data.append(("Total Cost", "", f"{r['total_cost']:,.2f}"))

        for row_data in data:
            row = self.fee_table.rowCount()
            self.fee_table.insertRow(row)
            items = [QTableWidgetItem(v) for v in row_data]
            if row_data[0] in ("TOTAL FEES", "Net Proceeds", "Total Cost"):
                f = items[0].font(); f.setBold(True)
                for it in items:
                    it.setFont(f)
            for c, it in enumerate(items):
                self.fee_table.setItem(row, c, it)
        self.fee_table.resizeColumnsToContents()

    def clear_inputs(self):
        self.transaction_value_input.clear()
        self.shares_input.clear()
        self.fee_table.setRowCount(0)

    def apply_theme(self, dark_mode: bool):
        pass  # handled by global stylesheet
