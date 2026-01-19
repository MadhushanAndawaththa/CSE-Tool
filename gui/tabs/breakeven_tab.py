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
from gui.styles import INFO_CARD_SUCCESS, INFO_CARD_DANGER, INFO_CARD_WARNING, TEXT_SECONDARY


class BreakEvenTab(QWidget):
    """Break-even calculator tab with profit/loss analysis."""
    
    def __init__(self):
        super().__init__()
        self.calculator = BreakEvenCalculator()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface."""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = QLabel("Break-Even Price Calculator")
        header.setProperty("heading", True)
        main_layout.addWidget(header)
        
        # Mode selection
        mode_group = QGroupBox("Calculation Mode")
        mode_layout = QVBoxLayout()
        
        self.mode_breakeven = QRadioButton("Calculate break-even price (minimum sell price to break even)")
        self.mode_profit = QRadioButton("Calculate profit/loss at a specific selling price")
        self.mode_breakeven.setChecked(True)
        self.mode_breakeven.toggled.connect(self.on_mode_changed)
        
        mode_layout.addWidget(self.mode_breakeven)
        mode_layout.addWidget(self.mode_profit)
        mode_group.setLayout(mode_layout)
        main_layout.addWidget(mode_group)
        
        # Input/Output section
        content_layout = QHBoxLayout()
        
        # Left side - Input panel
        input_panel = self.create_input_panel()
        content_layout.addWidget(input_panel, 1)
        
        # Right side - Results panel
        self.results_panel = self.create_results_panel()
        content_layout.addWidget(self.results_panel, 1)
        
        main_layout.addLayout(content_layout)
        
        # Set main layout
        self.setLayout(main_layout)
        
    def create_input_panel(self):
        """Create the input panel."""
        group = QGroupBox("Input Parameters")
        layout = QGridLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(12, 20, 12, 12)
        
        # Buy price
        row = 0
        layout.addWidget(QLabel("Purchase Price (LKR):"), row, 0)
        self.buy_price_input = QLineEdit()
        self.buy_price_input.setPlaceholderText("e.g., 161.25")
        self.buy_price_input.setValidator(QDoubleValidator(0.01, 999999.99, 2))
        self.buy_price_input.setToolTip("Enter the price you paid per share (0.01 - 999,999.99)")
        self.buy_price_input.returnPressed.connect(self.calculate)
        layout.addWidget(self.buy_price_input, row, 1)
        
        # Quantity
        row += 1
        layout.addWidget(QLabel("Quantity (shares):"), row, 0)
        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("e.g., 500")
        self.quantity_input.setValidator(QIntValidator(1, 99999999))
        self.quantity_input.setToolTip("Enter the number of shares purchased (1 - 99,999,999)")
        self.quantity_input.returnPressed.connect(self.calculate)
        layout.addWidget(self.quantity_input, row, 1)
        
        # Sell price (only for profit mode)
        row += 1
        self.sell_price_label = QLabel("Selling Price (LKR):")
        self.sell_price_input = QLineEdit()
        self.sell_price_input.setPlaceholderText("e.g., 170.00")
        self.sell_price_input.setValidator(QDoubleValidator(0.01, 999999.99, 2))
        self.sell_price_input.setToolTip("Enter your intended selling price per share")
        self.sell_price_input.returnPressed.connect(self.calculate)
        layout.addWidget(self.sell_price_label, row, 0)
        layout.addWidget(self.sell_price_input, row, 1)
        
        # Initially hide sell price (break-even mode is default)
        self.sell_price_label.hide()
        self.sell_price_input.hide()
        
        # Tax checkbox
        row += 1
        self.include_tax_checkbox = QCheckBox("Include Capital Gains Tax (30%)")
        self.include_tax_checkbox.setChecked(True)
        layout.addWidget(self.include_tax_checkbox, row, 0, 1, 2)
        
        # Calculate button
        row += 1
        self.calculate_btn = QPushButton("Calculate")
        self.calculate_btn.setToolTip("Calculate break-even price or profit/loss (Press Enter in any field)")
        self.calculate_btn.clicked.connect(self.calculate)
        layout.addWidget(self.calculate_btn, row, 0, 1, 2)
        
        # Clear button
        row += 1
        clear_btn = QPushButton("Clear")
        clear_btn.setProperty("buttonStyle", "secondary")
        clear_btn.setToolTip("Clear all inputs and results")
        clear_btn.clicked.connect(self.clear_inputs)
        layout.addWidget(clear_btn, row, 0, 1, 2)
        
        layout.setRowStretch(row + 1, 1)
        group.setLayout(layout)
        return group
        
    def create_results_panel(self):
        """Create the results display panel."""
        group = QGroupBox("Results")
        layout = QVBoxLayout()
        
        # Results label
        self.results_label = QLabel("Enter values and click Calculate to see results")
        self.results_label.setWordWrap(True)
        self.results_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.results_label.setMinimumHeight(100)
        self.results_label.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 14px; padding: 20px;")
        layout.addWidget(self.results_label)
        
        # Results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(2)
        self.results_table.setHorizontalHeaderLabels(["Metric", "Value"])
        self.results_table.horizontalHeader().setStretchLastSection(True)
        self.results_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.results_table.setAlternatingRowColors(True)
        self.results_table.verticalHeader().setVisible(False)
        self.results_table.verticalHeader().setDefaultSectionSize(36)
        self.results_table.setShowGrid(False)
        self.results_table.setAccessibleName("Break-even calculation results table")
        self.results_table.setAccessibleDescription("Displays detailed break-even analysis including fees, prices, and profit calculations")
        self.results_table.hide()
        layout.addWidget(self.results_table)
        
        group.setLayout(layout)
        return group
        
    def on_mode_changed(self):
        """Handle mode change between break-even and profit calculation."""
        if self.mode_profit.isChecked():
            self.sell_price_label.show()
            self.sell_price_input.show()
        else:
            self.sell_price_label.hide()
            self.sell_price_input.hide()
            
    def calculate(self):
        """Perform calculation based on selected mode."""
        try:
            # Validate inputs
            if not self.buy_price_input.text() or not self.quantity_input.text():
                QMessageBox.warning(self, "Input Required", 
                    "Please enter both purchase price and quantity.\n\n"
                    "Purchase price must be between 0.01 and 999,999.99 LKR.\n"
                    "Quantity must be between 1 and 99,999,999 shares.")
                return
                
            buy_price = float(self.buy_price_input.text())
            quantity = int(self.quantity_input.text())
            include_tax = self.include_tax_checkbox.isChecked()
            
            if self.mode_profit.isChecked():
                # Profit/Loss mode
                if not self.sell_price_input.text():
                    QMessageBox.warning(self, "Input Required", 
                        "Please enter selling price to calculate profit/loss.\n\n"
                        "Selling price must be between 0.01 and 999,999.99 LKR.")
                    return
                    
                sell_price = float(self.sell_price_input.text())
                result = self.calculator.calculate_profit_at_price(
                    buy_price, sell_price, quantity, include_tax
                )
                self.display_profit_results(result)
            else:
                # Break-even mode
                result = self.calculator.calculate_breakeven_price(
                    buy_price, quantity, include_tax
                )
                self.display_breakeven_results(result)
                
        except ValueError as e:
            QMessageBox.critical(self, "Calculation Error", f"Invalid input: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            
    def display_breakeven_results(self, result):
        """Display break-even calculation results."""
        self.results_table.setRowCount(0)
        self.results_table.show()
        
        # Prepare data
        data = [
            ("Purchase Price", f"LKR {result['buy_price']:.2f}"),
            ("Quantity", f"{result['quantity']:,} shares"),
            ("", ""),
            ("Total Investment", f"LKR {result['total_investment']:,.2f}"),
            ("Buy Fees Paid", f"LKR {result['buy_fees_paid']:,.2f}"),
            ("", ""),
            ("BREAK-EVEN PRICE", f"LKR {result['breakeven_price']:.2f}"),
            ("Price Increase Required", f"LKR {result['price_increase_required']:.2f}"),
            ("Percentage Increase", f"{result['price_increase_percentage'] * 100:.2f}%"),
            ("", ""),
            ("Sell Value at Break-Even", f"LKR {result['sell_value_at_breakeven']:,.2f}"),
            ("Sell Fees at Break-Even", f"LKR {result['sell_fees_at_breakeven']:,.2f}"),
        ]
        
        if result['includes_capital_gains_tax']:
            data.append(("Capital Gains Tax Included", "Yes (30%)"))
        
        # Populate table
        for row_data in data:
            row = self.results_table.rowCount()
            self.results_table.insertRow(row)
            
            item1 = QTableWidgetItem(row_data[0])
            item2 = QTableWidgetItem(row_data[1])
            
            # Set text color explicitly
            item1.setForeground(Qt.GlobalColor.black)
            item2.setForeground(Qt.GlobalColor.black)
            
            # Bold key metrics
            if row_data[0] == "BREAK-EVEN PRICE":
                font = item1.font()
                font.setBold(True)
                item1.setFont(font)
                item2.setFont(font)
                
            self.results_table.setItem(row, 0, item1)
            self.results_table.setItem(row, 1, item2)
        
        self.results_table.resizeColumnsToContents()
        
        # Update results label with summary
        summary = f"""
        <div style='{INFO_CARD_SUCCESS}'>
            <h3 style='margin-top:0;'>✓ Break-Even Price Calculated</h3>
            <p><b>Sell at LKR {result['breakeven_price']:.2f}</b> to break even</p>
            <p>Price increase required: LKR {result['price_increase_required']:.2f} 
            ({result['price_increase_percentage'] * 100:.2f}%)</p>
        </div>
        """
        self.results_label.setText(summary)
        
    def display_profit_results(self, result):
        """Display profit/loss calculation results."""
        self.results_table.setRowCount(0)
        self.results_table.show()
        
        is_profit = result['net_profit'] > 0
        
        # Prepare data
        data = [
            ("Purchase Price", f"LKR {result['buy_price']:.2f}"),
            ("Selling Price", f"LKR {result['sell_price']:.2f}"),
            ("Quantity", f"{result['quantity']:,} shares"),
            ("Price Change", f"LKR {result['sell_price'] - result['buy_price']:.2f}"),
            ("", ""),
            ("Total Investment", f"LKR {result['total_investment']:,.2f}"),
            ("Total Fees Paid", f"LKR {result['total_fees']:,.2f}"),
            ("Gross Profit/Loss", f"LKR {result['gross_profit']:,.2f}"),
            ("Capital Gains Tax", f"LKR {result['capital_gains_tax']:,.2f}"),
            ("", ""),
            ("NET PROFIT/LOSS", f"LKR {result['net_profit']:,.2f}"),
            ("Return Percentage", f"{result['profit_percentage'] * 100:.2f}%"),
            ("", ""),
            ("Break-Even Price", f"LKR {result['breakeven_price']:.2f}"),
            ("Above/Below Break-Even", f"LKR {result['price_vs_breakeven']:.2f}"),
        ]
        
        # Populate table
        for row_data in data:
            row = self.results_table.rowCount()
            self.results_table.insertRow(row)
            
            item1 = QTableWidgetItem(row_data[0])
            item2 = QTableWidgetItem(row_data[1])
            
            # Set text color explicitly
            item1.setForeground(Qt.GlobalColor.black)
            item2.setForeground(Qt.GlobalColor.black)
            
            # Bold and color net profit
            if row_data[0] == "NET PROFIT/LOSS":
                font = item1.font()
                font.setBold(True)
                item1.setFont(font)
                item2.setFont(font)
                
            self.results_table.setItem(row, 0, item1)
            self.results_table.setItem(row, 1, item2)
        
        self.results_table.resizeColumnsToContents()
        
        # Update results label with summary
        if is_profit:
            style = INFO_CARD_SUCCESS
            icon = "✓"
            status = "PROFIT"
        else:
            style = INFO_CARD_DANGER
            icon = "✗"
            status = "LOSS"
            
        summary = f"""
        <div style='{style}'>
            <h3 style='margin-top:0;'>{icon} {status}</h3>
            <p><b>Net Profit/Loss: LKR {result['net_profit']:,.2f}</b></p>
            <p>Return: {result['profit_percentage'] * 100:.2f}%</p>
            <p>Break-even price: LKR {result['breakeven_price']:.2f}</p>
        </div>
        """
        self.results_label.setText(summary)
        
    def clear_inputs(self):
        """Clear all input fields and results."""
        self.buy_price_input.clear()
        self.quantity_input.clear()
        self.sell_price_input.clear()
        self.include_tax_checkbox.setChecked(True)
        self.mode_breakeven.setChecked(True)
        self.results_table.hide()
        self.results_label.setText("Enter values and click Calculate to see results")
        self.results_label.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 14px; padding: 20px;")
