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
from gui.styles import INFO_CARD_SUCCESS, INFO_CARD_WARNING, INFO_CARD_DANGER, TEXT_SECONDARY


class FundamentalTab(QWidget):
    """Fundamental analysis tab."""
    
    def __init__(self):
        super().__init__()
        self.analyzer = FundamentalAnalyzer()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface."""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = QLabel("Fundamental Analysis")
        header.setProperty("heading", True)
        main_layout.addWidget(header)
        
        # Content layout
        content_layout = QHBoxLayout()
        
        # Left side - Input panel
        input_panel = self.create_input_panel()
        content_layout.addWidget(input_panel, 1)
        
        # Right side - Results panel
        self.results_panel = self.create_results_panel()
        content_layout.addWidget(self.results_panel, 1)
        
        main_layout.addLayout(content_layout)
        
        self.setLayout(main_layout)
        
    def create_input_panel(self):
        """Create the input panel."""
        group = QGroupBox("Financial Data Input")
        layout = QGridLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(12, 20, 12, 12)
        
        row = 0
        
        # Stock info
        layout.addWidget(QLabel("Stock Symbol:"), row, 0)
        self.symbol_input = QLineEdit()
        self.symbol_input.setPlaceholderText("e.g., JKH.N0000")
        self.symbol_input.setToolTip("Enter the stock symbol (e.g., JKH.N0000 for John Keells Holdings)")
        layout.addWidget(self.symbol_input, row, 1)
        
        row += 1
        layout.addWidget(QLabel("Current Price (LKR):"), row, 0)
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("e.g., 161.25")
        self.price_input.setValidator(QDoubleValidator(0.01, 999999.99, 2))
        self.price_input.setToolTip("Current market price per share in LKR")
        self.price_input.returnPressed.connect(self.analyze)
        layout.addWidget(self.price_input, row, 1)
        
        row += 1
        layout.addWidget(QLabel("EPS (Earnings Per Share):"), row, 0)
        self.eps_input = QLineEdit()
        self.eps_input.setPlaceholderText("e.g., 12.50")
        self.eps_input.setValidator(QDoubleValidator(-999999.99, 999999.99, 2))
        self.eps_input.setToolTip("Annual earnings per share (can be negative for loss-making companies)")
        self.eps_input.returnPressed.connect(self.analyze)
        layout.addWidget(self.eps_input, row, 1)
        
        row += 1
        layout.addWidget(QLabel("Book Value Per Share:"), row, 0)
        self.book_value_input = QLineEdit()
        self.book_value_input.setPlaceholderText("e.g., 85.00")
        self.book_value_input.setValidator(QDoubleValidator(0.01, 999999.99, 2))
        layout.addWidget(self.book_value_input, row, 1)
        
        row += 1
        layout.addWidget(QLabel("Net Income (Million):"), row, 0)
        self.net_income_input = QLineEdit()
        self.net_income_input.setPlaceholderText("e.g., 5000")
        self.net_income_input.setValidator(QDoubleValidator(-999999.99, 999999999.99, 2))
        layout.addWidget(self.net_income_input, row, 1)
        
        row += 1
        layout.addWidget(QLabel("Shareholders Equity (Million):"), row, 0)
        self.equity_input = QLineEdit()
        self.equity_input.setPlaceholderText("e.g., 25000")
        self.equity_input.setValidator(QDoubleValidator(0.01, 999999999.99, 2))
        layout.addWidget(self.equity_input, row, 1)
        
        row += 1
        layout.addWidget(QLabel("Total Debt (Million):"), row, 0)
        self.debt_input = QLineEdit()
        self.debt_input.setPlaceholderText("e.g., 10000")
        self.debt_input.setValidator(QDoubleValidator(0, 999999999.99, 2))
        layout.addWidget(self.debt_input, row, 1)
        
        row += 1
        layout.addWidget(QLabel("Current Assets (Million):"), row, 0)
        self.current_assets_input = QLineEdit()
        self.current_assets_input.setPlaceholderText("e.g., 15000")
        self.current_assets_input.setValidator(QDoubleValidator(0.01, 999999999.99, 2))
        layout.addWidget(self.current_assets_input, row, 1)
        
        row += 1
        layout.addWidget(QLabel("Current Liabilities (Million):"), row, 0)
        self.current_liabilities_input = QLineEdit()
        self.current_liabilities_input.setPlaceholderText("e.g., 8000")
        self.current_liabilities_input.setValidator(QDoubleValidator(0.01, 999999999.99, 2))
        layout.addWidget(self.current_liabilities_input, row, 1)
        
        # Analyze button
        row += 1
        self.analyze_btn = QPushButton("Analyze")
        self.analyze_btn.setToolTip("Perform fundamental analysis (Press Enter in any field)")
        self.analyze_btn.clicked.connect(self.analyze)
        layout.addWidget(self.analyze_btn, row, 0, 1, 2)
        
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
        group = QGroupBox("Analysis Results")
        layout = QVBoxLayout()
        
        # Results label
        self.results_label = QLabel("Enter financial data and click Analyze to see results")
        self.results_label.setWordWrap(True)
        self.results_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.results_label.setMinimumHeight(100)
        self.results_label.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 14px; padding: 20px;")
        layout.addWidget(self.results_label)
        
        # Results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["Metric", "Value", "Rating"])
        self.results_table.horizontalHeader().setStretchLastSection(True)
        self.results_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.results_table.setAlternatingRowColors(True)
        self.results_table.verticalHeader().setVisible(False)
        self.results_table.verticalHeader().setDefaultSectionSize(36)
        self.results_table.setShowGrid(False)
        self.results_table.setAccessibleName("Fundamental analysis results table")
        self.results_table.setAccessibleDescription("Displays calculated ratios like P/E, P/B, ROE with ratings")
        self.results_table.hide()
        layout.addWidget(self.results_table)
        
        group.setLayout(layout)
        return group
        
    def analyze(self):
        """Perform fundamental analysis."""
        try:
            # Validate required inputs
            if not all([self.price_input.text(), self.eps_input.text()]):
                QMessageBox.warning(self, "Input Required", 
                    "Please enter at least Current Price and EPS to perform analysis.\n\n"
                    "Additional fields are optional but provide more comprehensive analysis.")
                return
                
            price = float(self.price_input.text())
            eps = float(self.eps_input.text())
            
            results = []
            
            # P/E Ratio
            pe_result = self.analyzer.calculate_pe_ratio(price, eps)
            results.append(("P/E Ratio", f"{pe_result['pe_ratio']:.2f}", pe_result['rating']))
            
            # P/B Ratio (if book value provided)
            if self.book_value_input.text():
                book_value = float(self.book_value_input.text())
                pb_result = self.analyzer.calculate_pb_ratio(price, book_value)
                results.append(("P/B Ratio", f"{pb_result['pb_ratio']:.2f}", pb_result['rating']))
            
            # ROE (if net income and equity provided)
            if self.net_income_input.text() and self.equity_input.text():
                net_income = float(self.net_income_input.text()) * 1_000_000
                equity = float(self.equity_input.text()) * 1_000_000
                roe_result = self.analyzer.calculate_roe(net_income, equity)
                results.append(("ROE", f"{roe_result['roe'] * 100:.2f}%", roe_result['rating']))
            
            # Debt to Equity
            if self.debt_input.text() and self.equity_input.text():
                debt = float(self.debt_input.text()) * 1_000_000
                equity = float(self.equity_input.text()) * 1_000_000
                de_result = self.analyzer.calculate_debt_to_equity(debt, equity)
                results.append(("Debt/Equity", f"{de_result['debt_to_equity']:.2f}", de_result['rating']))
            
            # Current Ratio
            if self.current_assets_input.text() and self.current_liabilities_input.text():
                assets = float(self.current_assets_input.text()) * 1_000_000
                liabilities = float(self.current_liabilities_input.text()) * 1_000_000
                cr_result = self.analyzer.calculate_current_ratio(assets, liabilities)
                results.append(("Current Ratio", f"{cr_result['current_ratio']:.2f}", cr_result['rating']))
            
            self.display_results(results)
            
        except ValueError as e:
            QMessageBox.critical(self, "Input Error", f"Invalid input: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            
    def display_results(self, results):
        """Display analysis results."""
        self.results_table.setRowCount(0)
        self.results_table.show()
        
        # Count ratings
        excellent = sum(1 for _, _, rating in results if rating == "Excellent")
        good = sum(1 for _, _, rating in results if rating == "Good")
        fair = sum(1 for _, _, rating in results if rating == "Fair")
        poor = sum(1 for _, _, rating in results if rating == "Poor")
        
        # Populate table
        for metric, value, rating in results:
            row = self.results_table.rowCount()
            self.results_table.insertRow(row)
            
            self.results_table.setItem(row, 0, QTableWidgetItem(metric))
            self.results_table.setItem(row, 1, QTableWidgetItem(value))
            self.results_table.setItem(row, 2, QTableWidgetItem(rating))
        
        self.results_table.resizeColumnsToContents()
        
        # Overall summary
        if excellent + good >= len(results) * 0.6:
            style = INFO_CARD_SUCCESS
            summary = "Strong Fundamentals"
        elif poor >= len(results) * 0.5:
            style = INFO_CARD_DANGER
            summary = "Weak Fundamentals"
        else:
            style = INFO_CARD_WARNING
            summary = "Mixed Fundamentals"
        
        summary_html = f"""
        <div style='{style}'>
            <h3 style='margin-top:0; color: inherit;'>{summary}</h3>
            <p style='color: inherit;'><b>Excellent:</b> {excellent} | <b>Good:</b> {good} | <b>Fair:</b> {fair} | <b>Poor:</b> {poor}</p>
        </div>
        """
        self.results_label.setText(summary_html)
        
    def clear_inputs(self):
        """Clear all input fields and results."""
        self.symbol_input.clear()
        self.price_input.clear()
        self.eps_input.clear()
        self.book_value_input.clear()
        self.net_income_input.clear()
        self.equity_input.clear()
        self.debt_input.clear()
        self.current_assets_input.clear()
        self.current_liabilities_input.clear()
        self.results_table.hide()
        self.results_label.setText("Enter financial data and click Analyze to see results")
        self.results_label.setStyleSheet(f"color: #6b7280; font-size: 14px; padding: 20px;")
