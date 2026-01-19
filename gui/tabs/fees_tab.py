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
        """Initialize the user interface."""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = QLabel("CSE Fee Structure & Calculator")
        header.setProperty("heading", True)
        main_layout.addWidget(header)
        
        # Content layout
        content_layout = QHBoxLayout()
        
        # Left side - Fee calculator
        calculator_panel = self.create_calculator_panel()
        content_layout.addWidget(calculator_panel, 1)
        
        # Right side - Fee structure info
        info_panel = self.create_info_panel()
        content_layout.addWidget(info_panel, 1)
        
        main_layout.addLayout(content_layout)
        
        # Set main layout
        self.setLayout(main_layout)
        
    def create_calculator_panel(self):
        """Create the fee calculator panel."""
        group = QGroupBox("Interactive Fee Calculator")
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(12, 20, 12, 12)
        
        # Input section
        input_layout = QGridLayout()
        
        input_layout.addWidget(QLabel("Transaction Value (LKR):"), 0, 0)
        self.transaction_value_input = QLineEdit()
        self.transaction_value_input.setPlaceholderText("e.g., 80625")
        self.transaction_value_input.setValidator(QDoubleValidator(0.01, 999999999.99, 2))
        input_layout.addWidget(self.transaction_value_input, 0, 1)
        
        input_layout.addWidget(QLabel("Number of Shares:"), 1, 0)
        self.shares_input = QLineEdit()
        self.shares_input.setPlaceholderText("e.g., 500")
        self.shares_input.setValidator(QIntValidator(1, 99999999))
        input_layout.addWidget(self.shares_input, 1, 1)
        
        layout.addLayout(input_layout)
        
        # Calculate buttons
        btn_layout = QHBoxLayout()
        
        self.calc_buy_btn = QPushButton("Calculate Buy Fees")
        self.calc_buy_btn.clicked.connect(lambda: self.calculate_fees('buy'))
        btn_layout.addWidget(self.calc_buy_btn)
        
        self.calc_sell_btn = QPushButton("Calculate Sell Fees")
        self.calc_sell_btn.setProperty("buttonStyle", "success")
        self.calc_sell_btn.clicked.connect(lambda: self.calculate_fees('sell'))
        btn_layout.addWidget(self.calc_sell_btn)
        
        layout.addLayout(btn_layout)
        
        # Results table
        self.fee_table = QTableWidget()
        self.fee_table.setColumnCount(3)
        self.fee_table.setHorizontalHeaderLabels(["Fee Type", "Rate", "Amount (LKR)"])
        self.fee_table.horizontalHeader().setStretchLastSection(True)
        self.fee_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.fee_table.setAlternatingRowColors(True)
        self.fee_table.verticalHeader().setVisible(False)
        self.fee_table.verticalHeader().setDefaultSectionSize(36)
        self.fee_table.setShowGrid(False)
        layout.addWidget(self.fee_table)
        
        # Clear button
        clear_btn = QPushButton("Clear")
        clear_btn.setProperty("buttonStyle", "secondary")
        clear_btn.clicked.connect(self.clear_inputs)
        layout.addWidget(clear_btn)
        
        group.setLayout(layout)
        return group
        
    def create_info_panel(self):
        """Create the fee structure information panel."""
        group = QGroupBox("CSE Fee Structure Reference")
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Tier information
        tier_info = QLabel("""
        <h3>Fee Tiers</h3>
        <p><b>Tier 1:</b> Transactions ≤ Rs. 100,000,000<br/>
        <b>Tier 2:</b> Transactions > Rs. 100,000,000</p>
        """)
        tier_info.setWordWrap(True)
        layout.addWidget(tier_info)
        
        # Tier 1 fees
        tier1_table = QTableWidget()
        tier1_table.setColumnCount(2)
        tier1_table.setHorizontalHeaderLabels(["Fee Component", "Rate"])
        tier1_table.setRowCount(5)
        tier1_table.setAlternatingRowColors(True)
        tier1_table.verticalHeader().setVisible(False)
        tier1_table.verticalHeader().setDefaultSectionSize(32)
        tier1_table.setShowGrid(False)
        
        tier1_data = [
            ("Broker Commission", "0.64%"),
            ("SEC Fee", "0.072%"),
            ("CSE Fee", "0.084%"),
            ("CDS Fee", "0.024%"),
            ("STL Tax (Sell only)", "0.30%")
        ]
        
        for row, (component, rate) in enumerate(tier1_data):
            tier1_table.setItem(row, 0, QTableWidgetItem(component))
            tier1_table.setItem(row, 1, QTableWidgetItem(rate))
            
        tier1_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        tier1_table.resizeColumnsToContents()
        layout.addWidget(QLabel("<b>Tier 1 Fees:</b>"))
        layout.addWidget(tier1_table)
        
        # Tier 2 fees
        tier2_table = QTableWidget()
        tier2_table.setColumnCount(2)
        tier2_table.setHorizontalHeaderLabels(["Fee Component", "Rate"])
        tier2_table.setRowCount(5)
        tier2_table.setAlternatingRowColors(True)
        tier2_table.verticalHeader().setVisible(False)
        tier2_table.verticalHeader().setDefaultSectionSize(32)
        tier2_table.setShowGrid(False)
        
        tier2_data = [
            ("Broker Commission", "Min 0.20%"),
            ("SEC Fee", "0.042%"),
            ("CSE Fee", "0.054%"),
            ("CDS Fee", "0.024%"),
            ("STL Tax (Sell only)", "0.30%")
        ]
        
        for row, (component, rate) in enumerate(tier2_data):
            tier2_table.setItem(row, 0, QTableWidgetItem(component))
            tier2_table.setItem(row, 1, QTableWidgetItem(rate))
            
        tier2_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        tier2_table.resizeColumnsToContents()
        layout.addWidget(QLabel("<b>Tier 2 Fees:</b>"))
        layout.addWidget(tier2_table)
        
        # Capital gains tax
        tax_info = QLabel("""
        <h3>Capital Gains Tax</h3>
        <p><b>Rate:</b> 30% on net profit<br/>
        <i>Applied to: Gross Profit - Total Fees</i></p>
        """)
        tax_info.setWordWrap(True)
        layout.addWidget(tax_info)
        
        layout.addStretch()
        
        group.setLayout(layout)
        return group
        
    def calculate_fees(self, fee_type):
        """Calculate and display fees."""
        try:
            if not self.transaction_value_input.text() or not self.shares_input.text():
                QMessageBox.warning(self, "Input Error", "Please enter transaction value and number of shares.")
                return
                
            transaction_value = float(self.transaction_value_input.text())
            shares = int(float(self.shares_input.text()))
            
            if fee_type == 'buy':
                result = self.fee_calculator.calculate_buy_fees(transaction_value, shares)
                title = "Buy Fees"
            else:
                result = self.fee_calculator.calculate_sell_fees(transaction_value, shares)
                title = "Sell Fees"
                
            self.display_fee_results(result, title)
            
        except ValueError:
            QMessageBox.critical(self, "Input Error", "Please enter valid numbers.")
        except Exception as e:
            QMessageBox.critical(self, "Calculation Error", f"An error occurred: {str(e)}")
            
    def display_fee_results(self, result, title):
        """Display fee calculation results."""
        self.fee_table.setRowCount(0)
        
        # Prepare data
        data = [
            ("Transaction Value", "", f"{result['transaction_value']:,.2f}"),
            ("", "", ""),
            ("Broker Commission", f"{result['broker_commission_rate'] * 100:.3f}%", f"{result['broker_commission']:,.2f}"),
            ("SEC Fee", f"{result['sec_fee_rate'] * 100:.3f}%", f"{result['sec_fee']:,.2f}"),
            ("CSE Fee", f"{result['cse_fee_rate'] * 100:.3f}%", f"{result['cse_fee']:,.2f}"),
            ("CDS Fee", f"{result['cds_fee_rate'] * 100:.3f}%", f"{result['cds_fee']:,.2f}"),
        ]
        
        # Add STL tax for sell fees
        if 'stl_tax' in result:
            data.append(("STL Tax", f"{result['stl_tax_rate'] * 100:.2f}%", f"{result['stl_tax']:,.2f}"))
            
        data.extend([
            ("", "", ""),
            ("TOTAL FEES", f"{result['total_fee_percentage'] * 100:.3f}%", f"{result['total_fees']:,.2f}"),
        ])
        
        if 'net_proceeds' in result:
            data.append(("Net Proceeds", "", f"{result['net_proceeds']:,.2f}"))
        else:
            data.append(("Total Cost", "", f"{result['total_cost']:,.2f}"))
        
        # Populate table
        for row_data in data:
            row = self.fee_table.rowCount()
            self.fee_table.insertRow(row)
            
            item1 = QTableWidgetItem(row_data[0])
            item2 = QTableWidgetItem(row_data[1])
            item3 = QTableWidgetItem(row_data[2])
            
            # Set text color explicitly for all items
            item1.setForeground(Qt.GlobalColor.black)
            item2.setForeground(Qt.GlobalColor.black)
            item3.setForeground(Qt.GlobalColor.black)
            
            # Bold totals
            if row_data[0] in ["TOTAL FEES", "Net Proceeds", "Total Cost"]:
                font = item1.font()
                font.setBold(True)
                item1.setFont(font)
                item2.setFont(font)
                item3.setFont(font)
                
            self.fee_table.setItem(row, 0, item1)
            self.fee_table.setItem(row, 1, item2)
            self.fee_table.setItem(row, 2, item3)
        
        self.fee_table.resizeColumnsToContents()
        
    def clear_inputs(self):
        """Clear all input fields and results."""
        self.transaction_value_input.clear()
        self.shares_input.clear()
        self.fee_table.setRowCount(0)
