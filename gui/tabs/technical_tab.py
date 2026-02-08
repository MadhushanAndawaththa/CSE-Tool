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

import pyqtgraph as pg

from src.calculations.technical import TechnicalAnalyzer
from gui.styles import (
    INFO_CARD_SUCCESS, INFO_CARD_WARNING, INFO_CARD_DANGER,
    INFO_CARD_SUCCESS_DARK, INFO_CARD_WARNING_DARK, INFO_CARD_DANGER_DARK,
    TEXT_SECONDARY, TEXT_SECONDARY_DARK,
    get_info_card_style
)


class TechnicalTab(QWidget):
    """Technical analysis tab."""

    def __init__(self):
        super().__init__()
        self.analyzer = TechnicalAnalyzer()
        self.is_dark = False
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(14, 14, 14, 14)

        header = QLabel("Technical Analysis")
        header.setProperty("heading", True)
        main_layout.addWidget(header)

        self.instructions_label = QLabel(
            "Enter historical prices (one per line, most recent last). "
            "Min 14 for RSI, 26 for MACD, 50 for moving averages."
        )
        self.instructions_label.setWordWrap(True)
        self.instructions_label.setStyleSheet(
            f"color: {TEXT_SECONDARY}; font-size: 11px; padding: 6px 8px; "
            "background-color: #f3f4f6; border-radius: 4px;"
        )
        main_layout.addWidget(self.instructions_label)

        content = QHBoxLayout()
        content.setSpacing(12)
        content.addWidget(self._build_input_panel(), 1)
        self.results_panel = self._build_results_panel()
        content.addWidget(self.results_panel, 1)
        main_layout.addLayout(content, 1)
        self.setLayout(main_layout)

    # ── panels ────────────────────────────────────────────────────────

    def _build_input_panel(self):
        group = QGroupBox("Price Data Input")
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(10, 14, 10, 10)

        sym_row = QHBoxLayout()
        sym_row.addWidget(QLabel("Symbol:"))
        self.symbol_input = QLineEdit()
        self.symbol_input.setPlaceholderText("e.g., JKH.N0000")
        sym_row.addWidget(self.symbol_input)
        layout.addLayout(sym_row)

        layout.addWidget(QLabel("Historical Prices (one per line):"))
        self.price_data_input = QTextEdit()
        self.price_data_input.setPlaceholderText("150.00\n152.50\n151.75\n...")
        self.price_data_input.setMinimumHeight(180)
        layout.addWidget(self.price_data_input, 1)

        sample_btn = QPushButton("Load Sample Data")
        sample_btn.setProperty("buttonStyle", "secondary")
        sample_btn.clicked.connect(self.load_sample_data)
        layout.addWidget(sample_btn)

        self.analyze_btn = QPushButton("Analyze")
        self.analyze_btn.clicked.connect(self.analyze)
        layout.addWidget(self.analyze_btn)

        clear_btn = QPushButton("Clear")
        clear_btn.setProperty("buttonStyle", "secondary")
        clear_btn.clicked.connect(self.clear_inputs)
        layout.addWidget(clear_btn)

        group.setLayout(layout)
        return group

    def _build_results_panel(self):
        group = QGroupBox("Technical Indicators")
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(10, 14, 10, 10)

        self.results_label = QLabel("Enter price data and click Analyze to see technical indicators")
        self.results_label.setWordWrap(True)
        self.results_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.results_label.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 12px; padding: 12px;")
        layout.addWidget(self.results_label)

        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["Indicator", "Value", "Signal"])
        self.results_table.horizontalHeader().setStretchLastSection(True)
        self.results_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.results_table.setAlternatingRowColors(True)
        self.results_table.verticalHeader().setVisible(False)
        self.results_table.verticalHeader().setDefaultSectionSize(28)
        self.results_table.setShowGrid(False)
        self.results_table.hide()
        layout.addWidget(self.results_table)

        self.price_plot = pg.PlotWidget()
        self.price_plot.setMinimumHeight(200)
        self.price_plot.showGrid(x=True, y=True, alpha=0.2)
        self.price_plot.addLegend(offset=(10, 10))
        self.price_plot.setBackground(None)
        layout.addWidget(self.price_plot)

        group.setLayout(layout)
        return group

    # ── sample data ───────────────────────────────────────────────────

    def load_sample_data(self):
        self.price_data_input.setPlainText(
            "150.00\n152.50\n151.75\n155.00\n157.25\n156.50\n158.75\n160.00\n"
            "159.25\n161.50\n163.00\n162.25\n165.00\n167.50\n166.75\n169.00\n"
            "171.25\n170.50\n172.75\n175.00\n174.25\n176.50\n178.75\n177.50\n"
            "180.00\n182.25\n181.50\n183.75\n186.00\n185.25\n187.50\n190.00\n"
            "189.25\n191.50\n193.75\n192.50\n195.00\n197.25\n196.50\n199.00\n"
            "201.25\n200.50\n202.75\n205.00\n204.25\n206.50\n208.75\n207.50\n"
            "210.00\n212.25"
        )

    # ── analysis ──────────────────────────────────────────────────────

    def analyze(self):
        try:
            price_text = self.price_data_input.toPlainText().strip()
            if not price_text:
                self._show_msg(QMessageBox.Icon.Warning, "Input Error", "Please enter price data.")
                return

            prices = []
            for line in price_text.split("\n"):
                line = line.strip()
                if line:
                    try:
                        prices.append(float(line))
                    except ValueError:
                        self._show_msg(QMessageBox.Icon.Warning, "Input Error", f"Invalid price: {line}")
                        return

            if len(prices) < 14:
                self._show_msg(QMessageBox.Icon.Warning, "Insufficient Data",
                    "Need at least 14 prices for technical analysis.")
                return

            results = []
            plot_data = {"prices": prices}

            if len(prices) >= 14:
                rsi = self.analyzer.calculate_rsi(prices, period=14)
                if rsi["rsi"] is not None:
                    results.append(("RSI (14)", f"{rsi['rsi']:.2f}", rsi["signal"]))

            if len(prices) >= 26:
                macd = self.analyzer.calculate_macd(prices)
                if macd["macd"] is not None:
                    results.append(("MACD", f"{macd['macd']:.2f}", macd["signal"]))
                    if macd["signal_line"] is not None:
                        results.append(("MACD Signal", f"{macd['signal_line']:.2f}", ""))

            if len(prices) >= 50:
                ma = self.analyzer.calculate_moving_averages(prices, short_period=20, long_period=50)
                results.append(("Current Price", f"{prices[-1]:.2f}", ""))
                results.append(("MA 20", f"{ma['short_ma']:.2f}", ""))
                results.append(("MA 50", f"{ma['long_ma']:.2f}", ma["signal"]))
                plot_data["ma20"] = self.calculate_sma(prices, 20)
                plot_data["ma50"] = self.calculate_sma(prices, 50)

            if not results:
                self._show_msg(QMessageBox.Icon.Warning, "Analysis Error", "Could not calculate indicators.")
                return

            self._show_results(results, prices, plot_data)
        except Exception as e:
            self._show_msg(QMessageBox.Icon.Critical, "Error", str(e))

    def _show_results(self, results, prices, plot_data):
        self.results_table.setRowCount(0)
        self.results_table.show()

        buy = sum(1 for _, _, s in results if s in ("BUY", "STRONG BUY"))
        sell = sum(1 for _, _, s in results if s in ("SELL", "STRONG SELL"))

        for ind, val, sig in results:
            row = self.results_table.rowCount()
            self.results_table.insertRow(row)
            i1, i2, i3 = QTableWidgetItem(ind), QTableWidgetItem(val), QTableWidgetItem(sig)
            if ind == "Current Price":
                f = i1.font(); f.setBold(True); i1.setFont(f); i2.setFont(f)
            self.results_table.setItem(row, 0, i1)
            self.results_table.setItem(row, 1, i2)
            self.results_table.setItem(row, 2, i3)
        self.results_table.resizeColumnsToContents()

        if buy > sell:
            style, summary, msg = get_info_card_style('success', self.is_dark), "Bullish Signals", f"Buy: {buy}, Sell: {sell}"
        elif sell > buy:
            style, summary, msg = get_info_card_style('danger', self.is_dark), "Bearish Signals", f"Sell: {sell}, Buy: {buy}"
        else:
            style, summary, msg = get_info_card_style('warning', self.is_dark), "Neutral Signals", "Mixed signals"

        self.results_label.setText(
            f"<div style='{style}'><b>{summary}</b><br>"
            f"{msg} &mdash; {len(prices)} data points</div>"
        )
        self.update_plot(plot_data)

    # ── clear ─────────────────────────────────────────────────────────

    def clear_inputs(self):
        self.symbol_input.clear()
        self.price_data_input.clear()
        self.results_table.hide()
        self.results_label.setText("Enter price data and click Analyze to see technical indicators")
        self._update_results_label_style()
        self.price_plot.clear()

    # ── theme ─────────────────────────────────────────────────────────

    def _update_results_label_style(self):
        c = TEXT_SECONDARY_DARK if self.is_dark else TEXT_SECONDARY
        self.results_label.setStyleSheet(f"color: {c}; font-size: 12px; padding: 12px;")

    def _update_instructions_style(self):
        c = TEXT_SECONDARY_DARK if self.is_dark else TEXT_SECONDARY
        bg = "#1f2937" if self.is_dark else "#f3f4f6"
        self.instructions_label.setStyleSheet(
            f"color: {c}; font-size: 11px; padding: 6px 8px; background-color: {bg}; border-radius: 4px;"
        )

    def apply_theme(self, dark_mode: bool):
        self.is_dark = dark_mode
        self._update_results_label_style()
        self._update_instructions_style()
        self._update_plot_theme()

    def _show_msg(self, icon, title, text):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(icon)
        if self.is_dark:
            msg.setStyleSheet("QLabel { color: #e2e4e7; } QMessageBox { background: #1e293b; }")
        msg.exec()

    def _update_plot_theme(self):
        ac = "#cbd5e1" if self.is_dark else "#475569"
        gc = "#334155" if self.is_dark else "#e2e8f0"
        for axis in ("left", "bottom"):
            ax = self.price_plot.getAxis(axis)
            ax.setPen(pg.mkPen(ac))
            ax.setTextPen(pg.mkPen(ac))
        self.price_plot.getPlotItem().getViewBox().setBackgroundColor(
            "#0b1220" if self.is_dark else "#ffffff"
        )
        self.price_plot.getPlotItem().setMenuEnabled(False)
        self.price_plot.showGrid(x=True, y=True, alpha=0.25)
        self.price_plot.getPlotItem().getViewBox().setBorder(pg.mkPen(gc))

    # ── chart ─────────────────────────────────────────────────────────

    def update_plot(self, plot_data):
        self.price_plot.clear()
        prices = plot_data.get("prices", [])
        if not prices:
            return
        x = list(range(1, len(prices) + 1))
        pc = "#60a5fa" if self.is_dark else "#2563eb"
        mc = "#22c55e" if self.is_dark else "#16a34a"
        fc = "#f59e0b" if self.is_dark else "#d97706"
        self.price_plot.plot(x, prices, pen=pg.mkPen(pc, width=2), name="Price")
        for series_key, color, label in [("ma20", mc, "MA 20"), ("ma50", fc, "MA 50")]:
            series = plot_data.get(series_key)
            if series:
                xs, ys = self._series_points(series)
                if xs:
                    self.price_plot.plot(xs, ys, pen=pg.mkPen(color, width=2), name=label)
        self.price_plot.setLabel("bottom", "Data Points")
        self.price_plot.setLabel("left", "Price (LKR)")

    @staticmethod
    def calculate_sma(prices, period):
        if len(prices) < period:
            return None
        sma = []
        for i in range(len(prices)):
            if i < period - 1:
                sma.append(None)
            else:
                sma.append(sum(prices[i - period + 1: i + 1]) / period)
        return sma

    @staticmethod
    def _series_points(series):
        xs, ys = [], []
        for i, v in enumerate(series):
            if v is not None:
                xs.append(i + 1)
                ys.append(v)
        return xs, ys
