"""
Complete Analysis tab for CSE Stock Analyzer GUI.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt

from gui.styles import INFO_CARD_WARNING, TEXT_SECONDARY


class CompleteAnalysisTab(QWidget):
    """Complete stock analysis tab with recommendations."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface."""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = QLabel("Complete Stock Analysis")
        header.setProperty("heading", True)
        main_layout.addWidget(header)
        
        # Coming soon message
        message_container = QWidget()
        message_layout = QVBoxLayout()
        message_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        icon_label = QLabel("🎯")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("font-size: 72px;")
        message_layout.addWidget(icon_label)
        
        title_label = QLabel("Complete Analysis with Recommendations")
        title_label.setProperty("heading", True)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message_layout.addWidget(title_label)
        
        desc_label = QLabel(
            "This feature combines fundamental and technical analysis to provide "
            "comprehensive buy/sell recommendations with risk scoring."
        )
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 14px; padding: 20px; max-width: 600px;")
        message_layout.addWidget(desc_label)
        
        # Features list
        features_html = """
        <div style='background-color: #f9fafb; border: 2px solid #e5e7eb; border-radius: 8px; padding: 20px; margin: 20px;'>
            <h3 style='color: #111827; margin-top: 0;'>Planned Features:</h3>
            <ul style='color: #4b5563; font-size: 14px; line-height: 1.8;'>
                <li><b>Combined Analysis:</b> Merge fundamental and technical indicators</li>
                <li><b>Risk Assessment:</b> Calculate risk scores based on volatility and fundamentals</li>
                <li><b>Recommendation Engine:</b> Strong Buy, Buy, Hold, Sell, Strong Sell</li>
                <li><b>Target Prices:</b> Calculate optimal entry and exit points</li>
                <li><b>Confidence Levels:</b> High, Medium, Low confidence ratings</li>
                <li><b>PDF Reports:</b> Export comprehensive analysis reports</li>
            </ul>
        </div>
        """
        features_label = QLabel(features_html)
        features_label.setWordWrap(True)
        message_layout.addWidget(features_label)
        
        # Workaround info
        workaround_html = f"""
        <div style='{INFO_CARD_WARNING}'>
            <h3 style='margin-top:0; color: inherit;'>⚡ Current Workaround</h3>
            <p style='color: inherit;'>Use the <b>Fundamental Analysis</b> and <b>Technical Analysis</b> tabs separately, 
            then combine the insights manually. The Break-Even Calculator helps determine optimal sell prices.</p>
        </div>
        """
        workaround_label = QLabel(workaround_html)
        workaround_label.setWordWrap(True)
        message_layout.addWidget(workaround_label)
        
        # Action button
        action_btn = QPushButton("Use CLI Version for Complete Analysis")
        action_btn.clicked.connect(self.show_cli_instructions)
        action_btn.setMaximumWidth(400)
        message_layout.addWidget(action_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        message_layout.addStretch()
        message_container.setLayout(message_layout)
        main_layout.addWidget(message_container)
        
        self.setLayout(main_layout)
        
    def show_cli_instructions(self):
        """Show instructions for using CLI version."""
        QMessageBox.information(
            self,
            "CLI Complete Analysis",
            """<h3>Using the Command Line Interface</h3>
            <p>The CLI version has full complete analysis functionality:</p>
            <ol>
                <li>Open a terminal in the CSE directory</li>
                <li>Run: <code>python main.py</code></li>
                <li>Select option 3: "Complete Stock Analysis (with Recommendations)"</li>
                <li>Enter all required data (fundamental + technical)</li>
                <li>Get comprehensive buy/sell recommendations with scoring</li>
            </ol>
            <p><b>Note:</b> The GUI version of this feature is under development.</p>
            """
        )
