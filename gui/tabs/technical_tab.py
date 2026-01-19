"""
Technical Analysis tab for CSE Stock Analyzer GUI.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QTextEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator

from src.calculations.technical import TechnicalAnalyzer
from gui.styles import INFO_CARD_SUCCESS, INFO_CARD_WARNING, INFO_CARD_DANGER, TEXT_SECONDARY


class TechnicalTab(QWidget):
    """Technical analysis tab."""
    
    def __init__(self):
        super().__init__()
        self.analyzer = TechnicalAnalyzer()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface."""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = QLabel("Technical Analysis")
        header.setProperty("heading", True)
        main_layout.addWidget(header)
        
        # Instructions
        instructions = QLabel(
            "Enter historical price data (one price per line, most recent last). "
            "Minimum 14 prices for RSI, 26 for MACD, 50 for moving averages."
        )
        instructions.setWordWrap(True)
        instructions.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 13px; padding: 10px; background-color: #f3f4f6; border-radius: 6px;")
        main_layout.addWidget(instructions)
        
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
        group = QGroupBox("Price Data Input")
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(12, 20, 12, 12)
        
        # Stock symbol
        symbol_layout = QHBoxLayout()
        symbol_layout.addWidget(QLabel("Stock Symbol:"))
        self.symbol_input = QLineEdit()
        self.symbol_input.setPlaceholderText("e.g., JKH.N0000")
        self.symbol_input.setToolTip("Enter the stock symbol for reference")
        symbol_layout.addWidget(self.symbol_input)
        layout.addLayout(symbol_layout)
        
        # Price data text area
        layout.addWidget(QLabel("Historical Prices (one per line):"))
        self.price_data_input = QTextEdit()
        self.price_data_input.setPlaceholderText(
            "Example:\n150.00\n152.50\n151.75\n155.00\n157.25\n..."
        )
        self.price_data_input.setMinimumHeight(300)
        layout.addWidget(self.price_data_input)
        
        # Sample data button
        sample_btn = QPushButton("Load Sample Data")
        sample_btn.setProperty("buttonStyle", "secondary")
        sample_btn.setToolTip("Load example price data for testing")
        sample_btn.clicked.connect(self.load_sample_data)
        layout.addWidget(sample_btn)
        
        # Analyze button
        self.analyze_btn = QPushButton("Analyze")
        self.analyze_btn.setToolTip("Calculate technical indicators (RSI, MACD, Moving Averages)")
        self.analyze_btn.clicked.connect(self.analyze)
        layout.addWidget(self.analyze_btn)
        
        # Clear button
        clear_btn = QPushButton("Clear")
        clear_btn.setProperty("buttonStyle", "secondary")
        clear_btn.setToolTip("Clear all inputs and results")
        clear_btn.clicked.connect(self.clear_inputs)
        layout.addWidget(clear_btn)
        
        group.setLayout(layout)
        return group
        
    def create_results_panel(self):
        """Create the results display panel."""
        group = QGroupBox("Technical Indicators")
        layout = QVBoxLayout()
        
        # Results label
        self.results_label = QLabel("Enter price data and click Analyze to see technical indicators")
        self.results_label.setWordWrap(True)
        self.results_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.results_label.setMinimumHeight(100)
        self.results_label.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 14px; padding: 20px;")
        layout.addWidget(self.results_label)
        
        # Results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["Indicator", "Value", "Signal"])
        self.results_table.horizontalHeader().setStretchLastSection(True)
        self.results_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.results_table.setAlternatingRowColors(True)
        self.results_table.verticalHeader().setVisible(False)
        self.results_table.verticalHeader().setDefaultSectionSize(36)
        self.results_table.setShowGrid(False)
        self.results_table.setAccessibleName("Technical analysis results table")
        self.results_table.setAccessibleDescription("Displays technical indicators like RSI, MACD with buy/sell signals")
        self.results_table.hide()
        layout.addWidget(self.results_table)
        
        group.setLayout(layout)
        return group
        
    def load_sample_data(self):
        """Load sample price data."""
        sample_data = """150.00
152.50
151.75
155.00
157.25
156.50
158.75
160.00
159.25
161.50
163.00
162.25
165.00
167.50
166.75
169.00
171.25
170.50
172.75
175.00
174.25
176.50
178.75
177.50
180.00
182.25
181.50
183.75
186.00
185.25
187.50
190.00
189.25
191.50
193.75
192.50
195.00
197.25
196.50
199.00
201.25
200.50
202.75
205.00
204.25
206.50
208.75
207.50
210.00
212.25"""
        self.price_data_input.setPlainText(sample_data)
        
    def analyze(self):
        """Perform technical analysis."""
        try:
            # Parse price data
            price_text = self.price_data_input.toPlainText().strip()
            if not price_text:
                QMessageBox.warning(self, "Input Error", "Please enter price data.")
                return
                
            prices = []
            for line in price_text.split('\n'):
                line = line.strip()
                if line:
                    try:
                        prices.append(float(line))
                    except ValueError:
                        QMessageBox.warning(self, "Input Error", f"Invalid price value: {line}")
                        return
            
            if len(prices) < 14:
                QMessageBox.warning(
                    self, "Insufficient Data", 
                    "Please provide at least 14 price values for technical analysis."
                )
                return
            
            results = []
            
            # RSI
            if len(prices) >= 14:
                rsi_result = self.analyzer.calculate_rsi(prices, period=14)
                if rsi_result['rsi'] is not None:
                    results.append(("RSI (14)", f"{rsi_result['rsi']:.2f}", rsi_result['signal']))
            
            # MACD
            if len(prices) >= 26:
                macd_result = self.analyzer.calculate_macd(prices)
                if macd_result['macd'] is not None:
                    results.append(("MACD", f"{macd_result['macd']:.2f}", macd_result['signal']))
                    if macd_result['signal_line'] is not None:
                        results.append(("MACD Signal", f"{macd_result['signal_line']:.2f}", ""))
            
            # Moving Averages
            if len(prices) >= 50:
                ma_result = self.analyzer.calculate_moving_averages(prices, short_period=20, long_period=50)
                current_price = prices[-1]
                results.append(("Current Price", f"{current_price:.2f}", ""))
                results.append(("MA 20", f"{ma_result['short_ma']:.2f}", ""))
                results.append(("MA 50", f"{ma_result['long_ma']:.2f}", ma_result['signal']))
            
            if not results:
                QMessageBox.warning(
                    self, "Analysis Error", 
                    "Could not calculate indicators. Please check your data."
                )
                return
            
            self.display_results(results, prices)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            
    def display_results(self, results, prices):
        """Display analysis results."""
        self.results_table.setRowCount(0)
        self.results_table.show()
        
        # Count signals - match actual technical analyzer output
        buy_signals = sum(1 for _, _, signal in results if signal in ['BUY', 'STRONG BUY'])
        sell_signals = sum(1 for _, _, signal in results if signal in ['SELL', 'STRONG SELL'])
        neutral_signals = sum(1 for _, _, signal in results if signal == 'NEUTRAL')
        
        # Populate table
        for indicator, value, signal in results:
            row = self.results_table.rowCount()
            self.results_table.insertRow(row)
            
            item1 = QTableWidgetItem(indicator)
            item2 = QTableWidgetItem(value)
            item3 = QTableWidgetItem(signal)
            
            # Bold current price
            if indicator == "Current Price":
                font = item1.font()
                font.setBold(True)
                item1.setFont(font)
                item2.setFont(font)
            
            self.results_table.setItem(row, 0, item1)
            self.results_table.setItem(row, 1, item2)
            self.results_table.setItem(row, 2, item3)
        
        self.results_table.resizeColumnsToContents()
        
        # Overall summary
        if buy_signals > sell_signals:
            style = INFO_CARD_SUCCESS
            summary = "Bullish Technical Signals"
            message = f"Buy signals: {buy_signals}, Sell signals: {sell_signals}"
        elif sell_signals > buy_signals:
            style = INFO_CARD_DANGER
            summary = "Bearish Technical Signals"
            message = f"Sell signals: {sell_signals}, Buy signals: {buy_signals}"
        else:
            style = INFO_CARD_WARNING
            summary = "Neutral Technical Signals"
            message = f"Mixed signals detected"
        
        summary_html = f"""
        <div style='{style}'>
            <h3 style='margin-top:0; color: inherit;'>{summary}</h3>
            <p style='color: inherit;'><b>{message}</b></p>
            <p style='color: inherit;'>Analyzed {len(prices)} price points</p>
        </div>
        """
        self.results_label.setText(summary_html)
        
    def clear_inputs(self):
        """Clear all input fields and results."""
        self.symbol_input.clear()
        self.price_data_input.clear()
        self.results_table.hide()
        self.results_label.setText("Enter price data and click Analyze to see technical indicators")
        self.results_label.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 14px; padding: 20px;")
