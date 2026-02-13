"""
Complete Analysis tab for CSE Stock Analyzer GUI.
Combines fundamental + technical + risk analysis into a single dashboard.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox,
    QFrame, QGridLayout, QScrollArea, QGroupBox, QLineEdit, QTextEdit,
    QTableWidget, QTableWidgetItem, QSplitter, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator

from gui.styles import (
    CARD_STYLE, CARD_STYLE_DARK, TEXT_SECONDARY, TEXT_SECONDARY_DARK,
    SUCCESS, WARNING, DANGER, TEXT, _D_TEXT, _D_SURFACE, _D_BORDER, _D_BG,
    get_info_card_style
)

from src.analysis.recommendations import RecommendationEngine
from src.storage.database import AnalysisDatabase
from src.utils.logger import get_logger

logger = get_logger(__name__)


class CompleteAnalysisTab(QWidget):
    """Complete stock analysis dashboard with user input."""

    def __init__(self):
        super().__init__()
        self.is_dark = False
        self.engine = RecommendationEngine()
        self.db = AnalysisDatabase()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(14, 14, 14, 14)

        header = QLabel("Complete Stock Analysis")
        header.setProperty("heading", True)
        main_layout.addWidget(header)

        # Use a splitter: Left = inputs, Right = results
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # ── Left: Input Panel ──────────────────────────────
        input_scroll = QScrollArea()
        input_scroll.setWidgetResizable(True)
        input_scroll.setFrameShape(QFrame.Shape.NoFrame)
        input_widget = QWidget()
        input_layout = QVBoxLayout(input_widget)
        input_layout.setSpacing(10)
        input_layout.setContentsMargins(0, 0, 6, 0)

        # Fundamental inputs
        fund_group = QGroupBox("Fundamental Data")
        fund_grid = QGridLayout()
        fund_grid.setSpacing(6)
        fund_grid.setContentsMargins(10, 14, 10, 10)

        fund_fields = [
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

        for r, (label, attr, placeholder, validator_range) in enumerate(fund_fields):
            fund_grid.addWidget(QLabel(label), r, 0)
            inp = QLineEdit()
            inp.setPlaceholderText(placeholder)
            if validator_range:
                inp.setValidator(QDoubleValidator(validator_range[0], validator_range[1], 2))
            setattr(self, attr, inp)
            fund_grid.addWidget(inp, r, 1)

        fund_group.setLayout(fund_grid)
        input_layout.addWidget(fund_group)

        # Technical inputs (price history)
        tech_group = QGroupBox("Price History (for Technical Analysis)")
        tech_layout = QVBoxLayout()
        tech_layout.setSpacing(6)
        tech_layout.setContentsMargins(10, 14, 10, 10)

        self.price_hint = QLabel("Enter historical closing prices, one per line (oldest first).\n"
                            "Need at least 35 prices for full analysis.")
        self.price_hint.setWordWrap(True)
        self.price_hint.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 11px;")
        tech_layout.addWidget(self.price_hint)

        self.prices_input = QTextEdit()
        self.prices_input.setPlaceholderText(
            "100.00\n101.50\n103.25\n102.00\n..."
        )
        self.prices_input.setMaximumHeight(160)
        self.prices_input.setStyleSheet("font-family: 'Consolas', 'Courier New', monospace; font-size: 12px;")
        tech_layout.addWidget(self.prices_input)

        sample_btn = QPushButton("Load Sample Prices")
        sample_btn.setProperty("buttonStyle", "secondary")
        sample_btn.clicked.connect(self._load_sample_prices)
        tech_layout.addWidget(sample_btn)

        tech_group.setLayout(tech_layout)
        input_layout.addWidget(tech_group)

        # Action buttons
        btn_layout = QHBoxLayout()
        self.analyze_btn = QPushButton("Run Complete Analysis")
        self.analyze_btn.setProperty("buttonStyle", "success")
        self.analyze_btn.clicked.connect(self.run_analysis)
        btn_layout.addWidget(self.analyze_btn)

        clear_btn = QPushButton("Clear All")
        clear_btn.setProperty("buttonStyle", "secondary")
        clear_btn.clicked.connect(self.clear_inputs)
        btn_layout.addWidget(clear_btn)

        input_layout.addLayout(btn_layout)
        input_layout.addStretch()

        input_scroll.setWidget(input_widget)
        splitter.addWidget(input_scroll)

        # ── Right: Results Dashboard ──────────────────────
        results_scroll = QScrollArea()
        results_scroll.setWidgetResizable(True)
        results_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.results_widget = QWidget()
        self.results_layout = QVBoxLayout(self.results_widget)
        self.results_layout.setSpacing(14)
        self.results_layout.setContentsMargins(6, 0, 0, 0)

        # Placeholder before analysis
        self.placeholder_label = QLabel(
            "Enter stock data on the left and click\n"
            "\"Run Complete Analysis\" to see results."
        )
        self.placeholder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.placeholder_label.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 13px; padding: 40px;")
        self.results_layout.addWidget(self.placeholder_label)

        # Score + Recommendation (hidden initially)
        self.top_frame = QFrame()
        self.top_frame.setStyleSheet(CARD_STYLE)
        top_layout = QHBoxLayout(self.top_frame)

        score_col = QVBoxLayout()
        self.score_value = QLabel("--")
        self.score_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.score_value.setStyleSheet(f"font-size: 42px; font-weight: bold; color: {TEXT};")
        self.score_title = QLabel("OVERALL SCORE")
        self.score_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.score_title.setStyleSheet(f"font-size: 10px; font-weight: bold; color: {TEXT_SECONDARY}; letter-spacing: 1px;")
        score_col.addWidget(self.score_value)
        score_col.addWidget(self.score_title)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.VLine)
        sep.setFrameShadow(QFrame.Shadow.Sunken)

        rec_col = QVBoxLayout()
        self.rec_value = QLabel("--")
        self.rec_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rec_value.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {TEXT};")
        self.conf_value = QLabel("")
        self.conf_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.conf_value.setStyleSheet(f"font-size: 12px; color: {TEXT_SECONDARY}; background: #e0f2fe; padding: 3px 10px; border-radius: 10px;")
        rec_col.addWidget(self.rec_value)
        rec_col.addWidget(self.conf_value, 0, Qt.AlignmentFlag.AlignCenter)

        top_layout.addLayout(score_col, 1)
        top_layout.addWidget(sep)
        top_layout.addLayout(rec_col, 2)
        self.top_frame.hide()
        self.results_layout.addWidget(self.top_frame)

        # Breakdown cards row
        self.cards_widget = QWidget()
        cards_layout = QHBoxLayout(self.cards_widget)
        cards_layout.setContentsMargins(0, 0, 0, 0)
        cards_layout.setSpacing(10)

        self.fund_card = self._make_card("FUNDAMENTAL")
        self.tech_card = self._make_card("TECHNICAL")
        self.risk_card = self._make_card("RISK")
        cards_layout.addWidget(self.fund_card)
        cards_layout.addWidget(self.tech_card)
        cards_layout.addWidget(self.risk_card)
        self.cards_widget.hide()
        self.results_layout.addWidget(self.cards_widget)

        # Strengths & Concerns
        self.insights_widget = QWidget()
        insights_layout = QHBoxLayout(self.insights_widget)
        insights_layout.setContentsMargins(0, 0, 0, 0)
        insights_layout.setSpacing(10)

        self.strengths_frame = QFrame()
        self.strengths_frame.setStyleSheet(CARD_STYLE)
        s_layout = QVBoxLayout(self.strengths_frame)
        self.strengths_title = QLabel("✅ Key Strengths")
        self.strengths_title.setStyleSheet(f"color: {SUCCESS}; font-weight: bold; font-size: 13px;")
        self.strengths_label = QLabel("—")
        self.strengths_label.setWordWrap(True)
        self.strengths_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        s_layout.addWidget(self.strengths_title)
        s_layout.addWidget(self.strengths_label)
        s_layout.addStretch()

        self.concerns_frame = QFrame()
        self.concerns_frame.setStyleSheet(CARD_STYLE)
        c_layout = QVBoxLayout(self.concerns_frame)
        self.concerns_title = QLabel("⚠ Key Concerns")
        self.concerns_title.setStyleSheet(f"color: {DANGER}; font-weight: bold; font-size: 13px;")
        self.concerns_label = QLabel("—")
        self.concerns_label.setWordWrap(True)
        self.concerns_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        c_layout.addWidget(self.concerns_title)
        c_layout.addWidget(self.concerns_label)
        c_layout.addStretch()

        insights_layout.addWidget(self.strengths_frame)
        insights_layout.addWidget(self.concerns_frame)
        self.insights_widget.hide()
        self.results_layout.addWidget(self.insights_widget)

        # Action Items
        self.actions_frame = QFrame()
        self.actions_frame.setStyleSheet(CARD_STYLE)
        act_layout = QVBoxLayout(self.actions_frame)
        self.act_title = QLabel("📋 Action Items")
        self.act_title.setStyleSheet(f"font-weight: bold; font-size: 13px;")
        self.actions_label = QLabel("—")
        self.actions_label.setWordWrap(True)
        act_layout.addWidget(self.act_title)
        act_layout.addWidget(self.actions_label)
        self.actions_frame.hide()
        self.results_layout.addWidget(self.actions_frame)

        self.results_layout.addStretch()
        results_scroll.setWidget(self.results_widget)
        splitter.addWidget(results_scroll)

        splitter.setSizes([400, 600])
        main_layout.addWidget(splitter, 1)
        self.setLayout(main_layout)

    # ── Helper: Create a mini score card ───────────────────
    def _make_card(self, title):
        frame = QFrame()
        frame.setStyleSheet(CARD_STYLE)
        layout = QVBoxLayout(frame)
        layout.setSpacing(4)

        t = QLabel(title)
        t.setAlignment(Qt.AlignmentFlag.AlignCenter)
        t.setStyleSheet(f"font-size: 10px; font-weight: bold; color: {TEXT_SECONDARY}; letter-spacing: 1px;")
        t.setObjectName(f"{title.lower()}_card_title")

        v = QLabel("--")
        v.setObjectName(f"{title.lower()}_score_val")
        v.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {TEXT};")

        lbl = QLabel("")
        lbl.setObjectName(f"{title.lower()}_score_lbl")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet(f"font-size: 11px; color: {TEXT_SECONDARY};")

        layout.addWidget(t)
        layout.addWidget(v)
        layout.addWidget(lbl)
        return frame

    # ── Load sample prices ─────────────────────────────────
    def _load_sample_prices(self):
        sample = [
            150.00, 152.50, 151.00, 153.75, 155.00, 154.25, 156.50, 158.00,
            157.00, 159.25, 160.50, 161.00, 160.25, 162.00, 163.50, 162.75,
            164.00, 165.50, 164.25, 166.00, 167.50, 168.00, 167.25, 169.00,
            170.50, 169.75, 171.00, 172.50, 171.25, 173.00, 174.50, 173.75,
            175.00, 176.50, 175.25, 177.00, 178.50, 177.75, 179.00, 180.50
        ]
        self.prices_input.setPlainText("\n".join(f"{p:.2f}" for p in sample))

    # ── Parse prices from text ─────────────────────────────
    def _parse_prices(self):
        text = self.prices_input.toPlainText().strip()
        if not text:
            return []
        prices = []
        for line in text.split("\n"):
            line = line.strip()
            if line:
                try:
                    prices.append(float(line))
                except ValueError:
                    pass  # skip non-numeric lines
        return prices

    # ── Run the analysis ───────────────────────────────────
    def run_analysis(self):
        # Validate minimum required inputs
        if not self.price_input.text() or not self.eps_input.text():
            self._show_msg("Input Required",
                           "Please enter at least Current Price and EPS to run analysis.")
            return

        try:
            price = float(self.price_input.text())
            eps = float(self.eps_input.text())
        except ValueError:
            self._show_msg("Invalid Input", "Price and EPS must be valid numbers.")
            return

        # Build stock_data dict from inputs
        stock_data = {
            'price': price,
            'eps': eps,
        }

        if self.symbol_input.text().strip():
            stock_data['ticker'] = self.symbol_input.text().strip()

        if self.book_value_input.text():
            try:
                stock_data['book_value_per_share'] = float(self.book_value_input.text())
            except ValueError:
                pass

        if self.net_income_input.text():
            try:
                stock_data['net_income'] = float(self.net_income_input.text()) * 1e6
            except ValueError:
                pass

        if self.equity_input.text():
            try:
                stock_data['shareholders_equity'] = float(self.equity_input.text()) * 1e6
            except ValueError:
                pass

        if self.debt_input.text():
            try:
                stock_data['total_debt'] = float(self.debt_input.text()) * 1e6
            except ValueError:
                pass

        if self.current_assets_input.text():
            try:
                stock_data['current_assets'] = float(self.current_assets_input.text()) * 1e6
            except ValueError:
                pass

        if self.current_liabilities_input.text():
            try:
                stock_data['current_liabilities'] = float(self.current_liabilities_input.text()) * 1e6
            except ValueError:
                pass

        # Derived values the engine may need
        if 'total_debt' in stock_data and 'shareholders_equity' in stock_data:
            stock_data['debt_to_equity_ratio'] = stock_data['total_debt'] / stock_data['shareholders_equity']

        if 'current_assets' in stock_data and 'current_liabilities' in stock_data:
            stock_data['current_ratio'] = stock_data['current_assets'] / stock_data['current_liabilities']

        # Parse historical prices
        prices = self._parse_prices()

        # Run the engine
        try:
            result = self.engine.generate_recommendation(stock_data, prices=prices if prices else None)
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            self._show_msg("Analysis Error", f"An error occurred during analysis:\n{e}")
            return
            
        # Save result to database
        try:
            self.db.save_analysis(result)
            logger.info("Analysis result autosaved to database")
        except Exception as e:
            logger.error(f"Failed to autosave analysis: {e}")

        # Update the dashboard with real results
        self._display_results(result)

    # ── Display results on dashboard ───────────────────────
    def _display_results(self, result):
        self.last_result = result
        self.placeholder_label.hide()
        self.top_frame.show()
        self.cards_widget.show()
        self.insights_widget.show()
        self.actions_frame.show()

        # Overall score & recommendation
        score = result.get('overall_score', 0)
        rec = result.get('recommendation', 'N/A')
        conf = result.get('confidence', 'N/A')

        self.score_value.setText(f"{score:.0f}")
        self.score_value.setStyleSheet(f"font-size: 42px; font-weight: bold; color: {self._score_color(score)};")
        self.rec_value.setText(rec)
        self.conf_value.setText(f"{conf} Confidence")

        # Fundamental score
        fund = result.get('fundamental_analysis', {})
        fund_score = fund.get('overall_score', 0) if fund else 0
        self._update_card(self.fund_card, "fundamental", fund_score,
                          fund.get('overall_rating', '') if fund else '')

        # Technical score
        tech = result.get('technical_analysis', {})
        tech_score = tech.get('overall_score', 0) if tech else 0
        self._update_card(self.tech_card, "technical", tech_score,
                          tech.get('overall_signal', '') if tech else '')

        # Risk score
        risk = result.get('risk_assessment', {})
        risk_score = risk.get('risk_score', 0) if risk else 0
        self._update_card(self.risk_card, "risk", risk_score,
                          risk.get('risk_level', '') if risk else '')

        # Strengths
        strengths = result.get('key_strengths', [])
        if strengths:
            self.strengths_label.setText("\n".join(f"• {s}" for s in strengths))
        else:
            self.strengths_label.setText("No specific strengths identified")

        # Concerns
        concerns = result.get('key_concerns', [])
        if concerns:
            self.concerns_label.setText("\n".join(f"• {c}" for c in concerns))
        else:
            self.concerns_label.setText("No specific concerns identified")

        # Action items
        actions = result.get('action_items', [])
        if actions:
            self.actions_label.setText("\n".join(f"→ {a}" for a in actions))
        else:
            self.actions_label.setText("No specific actions recommended")

    def _update_card(self, card, prefix, score, label):
        val_widget = card.findChild(QLabel, f"{prefix}_score_val")
        lbl_widget = card.findChild(QLabel, f"{prefix}_score_lbl")
        if val_widget:
            val_widget.setText(f"{score:.0f}")
            val_widget.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {self._score_color(score)};")
        if lbl_widget:
            lbl_widget.setText(str(label))

    def _score_color(self, score):
        if score >= 70:
            return SUCCESS
        if score >= 50:
            return WARNING
        return DANGER

    # ── Clear / Reset ──────────────────────────────────────
    def clear_inputs(self):
        for attr in ("symbol_input", "price_input", "eps_input", "book_value_input",
                      "net_income_input", "equity_input", "debt_input",
                      "current_assets_input", "current_liabilities_input"):
            getattr(self, attr).clear()
        self.prices_input.clear()

        # Hide results, show placeholder
        self.top_frame.hide()
        self.cards_widget.hide()
        self.insights_widget.hide()
        self.actions_frame.hide()
        self.placeholder_label.show()

    # ── Theme ──────────────────────────────────────────────
    def apply_theme(self, dark_mode: bool):
        self.is_dark = dark_mode
        tc = _D_TEXT if dark_mode else TEXT
        sc = TEXT_SECONDARY_DARK if dark_mode else TEXT_SECONDARY
        card = CARD_STYLE_DARK if dark_mode else CARD_STYLE
        bg_color = _D_BG if dark_mode else '#f1f5f9'
        
        # Placeholder
        self.placeholder_label.setStyleSheet(f"color: {sc}; font-size: 13px; padding: 40px;")
        
        # Price hint
        self.price_hint.setStyleSheet(f"color: {sc}; font-size: 11px;")
        
        # Top score/recommendation frame
        self.top_frame.setStyleSheet(card)
        self.score_value.setStyleSheet(f"font-size: 42px; font-weight: bold; color: {tc};")
        self.score_title.setStyleSheet(f"font-size: 10px; font-weight: bold; color: {sc}; letter-spacing: 1px;")
        self.rec_value.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {tc};")
        conf_bg = 'rgba(59,130,246,0.15)' if dark_mode else '#e0f2fe'
        conf_fg = '#93c5fd' if dark_mode else TEXT
        self.conf_value.setStyleSheet(
            f"font-size: 12px; color: {conf_fg}; background: {conf_bg}; padding: 3px 10px; border-radius: 10px;"
        )
        
        # Breakdown cards
        for card_frame in (self.fund_card, self.tech_card, self.risk_card):
            card_frame.setStyleSheet(card)
            # Update card child label colors
            for child in card_frame.findChildren(QLabel):
                name = child.objectName()
                if name.endswith('_card_title'):
                    child.setStyleSheet(f"font-size: 10px; font-weight: bold; color: {sc}; letter-spacing: 1px;")
                elif name.endswith('_score_lbl'):
                    child.setStyleSheet(f"font-size: 11px; color: {sc};")
                # _score_val keeps its color based on score value, leave it
        
        # Strengths & Concerns frames
        self.strengths_frame.setStyleSheet(card)
        self.concerns_frame.setStyleSheet(card)
        self.strengths_label.setStyleSheet(f"color: {tc}; font-size: 12px; padding: 4px;")
        self.concerns_label.setStyleSheet(f"color: {tc}; font-size: 12px; padding: 4px;")
        
        # Action Items frame
        self.actions_frame.setStyleSheet(card)
        self.act_title.setStyleSheet(f"font-weight: bold; font-size: 13px; color: {tc};")
        self.actions_label.setStyleSheet(f"color: {tc}; font-size: 12px;")

    # ── Message box ────────────────────────────────────────
    def _show_msg(self, title, text):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(QMessageBox.Icon.Warning)
        if self.is_dark:
            msg.setStyleSheet("QLabel { color: #e2e4e7; } QMessageBox { background: #1e293b; }")
        msg.exec()
