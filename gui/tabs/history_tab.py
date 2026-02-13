"""
History Tab for CSE Stock Analyzer.

Displays past analysis results from the database.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox, QAbstractItemView, QFrame
)
from PyQt6.QtCore import Qt
from datetime import datetime

from src.storage.database import AnalysisDatabase
from gui.styles import (
    CARD_STYLE, CARD_STYLE_DARK, TEXT, TEXT_SECONDARY,
    TEXT_SECONDARY_DARK, SUCCESS, WARNING, DANGER,
    _D_TEXT, _D_SURFACE, _D_BORDER
)
from src.utils.logger import get_logger

logger = get_logger(__name__)


class HistoryTab(QWidget):
    """Tab to view and manage analysis history."""
    
    def __init__(self):
        super().__init__()
        self.db = AnalysisDatabase()
        self.is_dark = False
        self.init_ui()
        self.refresh_history()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)
        
        # Header
        header = QLabel("Analysis History")
        header.setProperty("heading", True)
        layout.addWidget(header)
        
        # Toolbar
        toolbar = QHBoxLayout()
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setProperty("buttonStyle", "secondary")
        refresh_btn.clicked.connect(self.refresh_history)
        toolbar.addWidget(refresh_btn)
        
        self.delete_btn = QPushButton("Delete Selected")
        self.delete_btn.setProperty("buttonStyle", "danger")
        self.delete_btn.clicked.connect(self.delete_selected)
        self.delete_btn.setEnabled(False)
        toolbar.addWidget(self.delete_btn)
        
        toolbar.addStretch()
        layout.addLayout(toolbar)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Date", "Ticker", "Price", "Score", "Recommendation"
        ])
        
        # Table setup
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        
        # Column styling
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents) # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents) # Date
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents) # Ticker
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents) # Price
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents) # Score
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)          # Recommendation
        
        self.table.itemSelectionChanged.connect(self._on_selection_changed)
        self.table.doubleClicked.connect(self.view_details)
        
        layout.addWidget(self.table)
        
        # Details placeholder (could be expanded later)
        self.info_lbl = QLabel("Double-click a row to view details (feature coming soon)")
        self.info_lbl.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 11px;")
        layout.addWidget(self.info_lbl)
        
        self.setLayout(layout)
        
    def refresh_history(self):
        """Reload history from database."""
        logger.info("Refreshing history tab")
        self.table.setRowCount(0)
        
        history = self.db.get_history(limit=50)
        self.table.setRowCount(len(history))
        
        for i, row in enumerate(history):
            # ID (hidden data, shown for debug/ref)
            id_item = QTableWidgetItem(str(row['id']))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i, 0, id_item)
            
            # Date
            try:
                dt = datetime.fromisoformat(row['timestamp'])
                date_str = dt.strftime("%Y-%m-%d %H:%M")
            except:
                date_str = row['timestamp']
            self.table.setItem(i, 1, QTableWidgetItem(date_str))
            
            # Ticker
            ticker = row['ticker'] or "N/A"
            self.table.setItem(i, 2, QTableWidgetItem(ticker))
            
            # Price
            price = f"{row['current_price']:,.2f}" if row['current_price'] else "N/A"
            price_item = QTableWidgetItem(price)
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(i, 3, price_item)
            
            # Score
            score = row['overall_score']
            score_item = QTableWidgetItem(f"{score:.0f}")
            score_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Color code score
            if score >= 75:
                score_item.setForeground(Qt.GlobalColor.darkGreen)
            elif score <= 40:
                score_item.setForeground(Qt.GlobalColor.red)
            
            self.table.setItem(i, 4, score_item)
            
            # Recommendation
            rec = row['recommendation']
            self.table.setItem(i, 5, QTableWidgetItem(rec))

    def _on_selection_changed(self):
        """Enable delete button if row selected."""
        selected = len(self.table.selectedItems()) > 0
        self.delete_btn.setEnabled(selected)

    def delete_selected(self):
        """Delete selected analysis."""
        # Not implemented in DB yet, would require add'l method
        QMessageBox.information(self, "Not Implemented", "Delete functionality coming soon.")
        
    def view_details(self):
        """View full details of selected analysis."""
        row = self.table.currentRow()
        if row < 0:
            return
            
        id_item = self.table.item(row, 0)
        if not id_item:
            return
            
        analysis_id = int(id_item.text())
        data = self.db.get_analysis_by_id(analysis_id)
        
        if data:
            # For now, just show a summary in a message box
            # Ideally this would open results in the CompleteAnalysisTab or a dialog
            info = f"Ticker: {data.get('stock_info', {}).get('ticker')}\n"
            info += f"Date: {datetime.now().strftime('%Y-%m-%d')}\n" # Timestamp lost in flat dict, stored in DB col
            info += f"Score: {data.get('overall_score')}\n"
            info += f"Rec: {data.get('recommendation')}\n\n"
            
            strengths = data.get('key_strengths', [])
            if strengths:
                info += "Strengths:\n" + "\n".join(f"- {s}" for s in strengths[:3]) + "\n\n"
                
            QMessageBox.information(self, "Analysis Details", info)
        
    def apply_theme(self, dark_mode: bool):
        """Apply light/dark theme."""
        self.is_dark = dark_mode
        self.info_lbl.setStyleSheet(
            f"color: {TEXT_SECONDARY_DARK if dark_mode else TEXT_SECONDARY}; font-size: 11px;"
        )
