"""
Complete Analysis tab for CSE Stock Analyzer GUI.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt

from gui.styles import INFO_CARD_WARNING, INFO_CARD_WARNING_DARK, TEXT_SECONDARY, TEXT_SECONDARY_DARK


class CompleteAnalysisTab(QWidget):
    """Complete stock analysis tab - coming soon placeholder."""

    def __init__(self):
        super().__init__()
        self.is_dark = False
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(14, 14, 14, 14)

        header = QLabel("Complete Stock Analysis")
        header.setProperty("heading", True)
        main_layout.addWidget(header)

        # centered coming-soon card
        center = QVBoxLayout()
        center.setAlignment(Qt.AlignmentFlag.AlignCenter)
        center.setSpacing(12)

        self.title_label = QLabel("Complete Analysis with Recommendations")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 15px; font-weight: 600; color: #1e293b;")
        center.addWidget(self.title_label)

        self.desc_label = QLabel(
            "Combines fundamental and technical analysis to provide "
            "comprehensive buy/sell recommendations with risk scoring."
        )
        self.desc_label.setWordWrap(True)
        self.desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.desc_label.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 12px; padding: 4px 40px;")
        center.addWidget(self.desc_label)

        self.features_label = QLabel()
        self.features_label.setWordWrap(True)
        self.features_label.setMaximumWidth(460)
        self.features_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        center.addWidget(self.features_label, 0, Qt.AlignmentFlag.AlignCenter)

        self.hint_label = QLabel()
        self.hint_label.setWordWrap(True)
        self.hint_label.setMaximumWidth(460)
        center.addWidget(self.hint_label, 0, Qt.AlignmentFlag.AlignCenter)

        # Set initial content
        self._update_features_label()
        self._update_hint_label()

        cli_btn = QPushButton("CLI Instructions")
        cli_btn.setProperty("buttonStyle", "secondary")
        cli_btn.setMaximumWidth(200)
        cli_btn.clicked.connect(self.show_cli_instructions)
        center.addWidget(cli_btn, 0, Qt.AlignmentFlag.AlignCenter)

        main_layout.addLayout(center, 1)
        self.setLayout(main_layout)

    def apply_theme(self, dark_mode: bool):
        self.is_dark = dark_mode
        c = TEXT_SECONDARY_DARK if dark_mode else TEXT_SECONDARY
        tc = "#e2e4e7" if dark_mode else "#1e293b"
        self.desc_label.setStyleSheet(f"color: {c}; font-size: 12px; padding: 4px 40px;")
        self.title_label.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {tc};")
        self._update_features_label()
        self._update_hint_label()

    def _update_features_label(self):
        bg = "#1e293b" if self.is_dark else "#f8fafc"
        border = "#334155" if self.is_dark else "#e2e8f0"
        tc = "#e2e4e7" if self.is_dark else "#1e293b"
        self.features_label.setText(
            f"<div style='padding:12px; background:{bg}; border:1px solid {border}; border-radius:6px; color:{tc};'>"
            "<b>Planned Features</b><br><br>"
            "\u2022 Combined fundamental + technical indicators<br>"
            "\u2022 Risk assessment &amp; confidence levels<br>"
            "\u2022 Strong Buy / Buy / Hold / Sell recommendations<br>"
            "\u2022 Target entry &amp; exit prices<br>"
            "\u2022 PDF report export"
            "</div>"
        )

    def _update_hint_label(self):
        style = INFO_CARD_WARNING_DARK if self.is_dark else INFO_CARD_WARNING
        self.hint_label.setText(
            f"<div style='{style}'>"
            "Use the <b>Fundamental</b> and <b>Technical</b> tabs separately for now, "
            "or run the CLI for a combined analysis.</div>"
        )

    def clear_inputs(self):
        """Reset tab to default state."""
        pass  # placeholder tab has no inputs to clear

    def show_cli_instructions(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("CLI Complete Analysis")
        msg.setTextFormat(Qt.TextFormat.RichText)
        tc = "#e2e4e7" if self.is_dark else "#1e293b"
        bc = "#0f172a" if self.is_dark else "#f8fafc"
        msg.setText(
            f"<h3 style='color:{tc}'>Using the CLI</h3>"
            f"<ol style='color:{tc}'><li>Open a terminal in the CSE directory</li>"
            f"<li>Run: <code style='background:{bc}; padding:2px 6px; border-radius:3px;'>python main.py</code></li>"
            f"<li>Select option 3: Complete Stock Analysis</li></ol>"
            f"<p style='color:{tc}'>The CLI version provides full combined analysis.</p>"
        )
        if self.is_dark:
            msg.setStyleSheet("QLabel { color: #e2e4e7; } QMessageBox { background: #1e293b; }")
        msg.exec()
