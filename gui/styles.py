"""
Modern styling and color scheme for CSE Stock Analyzer GUI.
Inspired by Material Design principles.
"""

# Color Palette (Material Design inspired)
PRIMARY_COLOR = "#1a73e8"       # Google Blue
PRIMARY_HOVER = "#1557b0"
PRIMARY_PRESSED = "#0e438a"

SUCCESS_COLOR = "#1e8e3e"       # Google Green
SUCCESS_HOVER = "#137333"

WARNING_COLOR = "#f9ab00"       # Google Yellow/Orange
DANGER_COLOR = "#d93025"        # Google Red
DANGER_HOVER = "#a50e0e"

INFO_COLOR = "#129eaf"          # Cyan
BACKGROUND = "#f8f9fa"          # Very light gray (Material Surface)
CARD_BG = "#ffffff"             # White
TEXT_PRIMARY = "#202124"        # Nearly Black
TEXT_SECONDARY = "#5f6368"      # Gray
BORDER_COLOR = "#dadce0"        # Light border
HOVER_BG = "#f1f3f4"            # Hover background

# Global Application Stylesheet (QSS)
GLOBAL_STYLESHEET = f"""
/* Main Window */
QMainWindow {{
    background-color: {BACKGROUND};
}}

/* Tab Widget */
QTabWidget::pane {{
    border: none;
    background: {CARD_BG};
    border-radius: 8px;
    padding: 16px;
    /* Use a subtle layout separation instead of a hard border for the pane */
}}

QTabWidget::tab-bar {{
    alignment: left;
    left: 16px;
}}

QTabBar::tab {{
    background: transparent;
    color: {TEXT_SECONDARY};
    padding: 12px 24px;
    font-size: 14px;
    font-weight: 500;
    border-bottom: 2px solid transparent;
    margin-right: 4px;
}}

QTabBar::tab:selected {{
    color: {PRIMARY_COLOR};
    border-bottom: 3px solid {PRIMARY_COLOR};
}}

QTabBar::tab:hover {{
    background: {HOVER_BG};
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}}

/* Labels */
QLabel {{
    color: {TEXT_PRIMARY};
    font-family: 'Segoe UI', 'Roboto', sans-serif;
    font-size: 14px;
}}

QLabel[heading="true"] {{
    font-size: 22px;
    font-weight: 400; /* Material headings are often lighter weight but larger */
    color: {TEXT_PRIMARY};
    padding: 16px 0 8px 0;
}}

QLabel[subheading="true"] {{
    font-size: 16px;
    font-weight: 500;
    color: {TEXT_PRIMARY};
    padding-bottom: 8px;
}}

/* Line Edits (Input Fields) */
QLineEdit {{
    background-color: {CARD_BG};
    border: 1px solid {BORDER_COLOR};
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 14px;
    color: {TEXT_PRIMARY};
    selection-background-color: {PRIMARY_COLOR};
}}

QTextEdit {{
    background-color: {CARD_BG};
    border: 1px solid {BORDER_COLOR};
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 14px;
    color: {TEXT_PRIMARY};
}}

QLineEdit:focus {{
    border: 2px solid {PRIMARY_COLOR};
    padding: 7px 11px;
    background-color: #ffffff;
}}

QTextEdit:focus {{
    border: 2px solid {PRIMARY_COLOR};
    padding: 7px 11px;
    background-color: #ffffff;
}}

QLineEdit:disabled {{
    background-color: {BACKGROUND};
    color: {TEXT_SECONDARY};
    border: 1px dashed {BORDER_COLOR};
}}

/* Spin Boxes */
QSpinBox, QDoubleSpinBox {{
    background-color: {CARD_BG};
    border: 1px solid {BORDER_COLOR};
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 14px;
    color: {TEXT_PRIMARY};
}}

QSpinBox:focus, QDoubleSpinBox:focus {{
    border: 2px solid {PRIMARY_COLOR};
    padding: 7px 11px;
    background-color: #ffffff;
}}

/* Buttons - Material Design Filled and Outlined */
QPushButton {{
    background-color: {PRIMARY_COLOR};
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-size: 13px;
    font-weight: 600;
    min-height: 32px;
    outline: none;
}}

QPushButton:hover {{
    background-color: {PRIMARY_HOVER};
}}

QPushButton:pressed {{
    background-color: {PRIMARY_PRESSED};
}}

QPushButton:disabled {{
    background-color: #e0e0e0;
    color: #9e9e9e;
}}

QPushButton[buttonStyle="success"] {{
    background-color: {SUCCESS_COLOR};
}}

QPushButton[buttonStyle="success"]:hover {{
    background-color: {SUCCESS_HOVER};
}}

QPushButton[buttonStyle="danger"] {{
    background-color: {DANGER_COLOR};
}}

QPushButton[buttonStyle="danger"]:hover {{
    background-color: {DANGER_HOVER};
}}

QPushButton[buttonStyle="secondary"] {{
    background-color: transparent;
    color: {PRIMARY_COLOR};
    border: 1px solid {BORDER_COLOR};
}}

QPushButton[buttonStyle="secondary"]:hover {{
    background-color: {HOVER_BG};
    border: 1px solid {PRIMARY_COLOR};
    color: {PRIMARY_COLOR};
}}

QPushButton[buttonStyle="secondary"]:pressed {{
    background-color: #e8f0fe;
    border: 1px solid {PRIMARY_COLOR};
}}


/* Check Boxes */
QCheckBox {{
    color: {TEXT_PRIMARY};
    font-size: 14px;
    spacing: 8px;
    padding: 4px;
}}

QCheckBox::indicator {{
    width: 20px;
    height: 20px;
    border: 1px solid {BORDER_COLOR};
    border-radius: 4px;
    background-color: #ffffff;
}}

QCheckBox::indicator:checked {{
    background-color: {PRIMARY_COLOR};
    border-color: {PRIMARY_COLOR};
    image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>');
}}

/* Radio Buttons */
QRadioButton {{
    color: {TEXT_PRIMARY};
    font-size: 14px;
    spacing: 8px;
    padding: 4px;
}}

QRadioButton::indicator {{
    width: 20px;
    height: 20px;
    border: 1px solid {BORDER_COLOR};
    border-radius: 10px;
    background-color: #ffffff;
}}

QRadioButton::indicator:checked {{
    background-color: {PRIMARY_COLOR};
    border-color: {PRIMARY_COLOR};
    image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="white"><circle cx="12" cy="12" r="6"/></svg>');
}}

/* Tables */
QTableWidget {{
    background-color: {CARD_BG};
    border: 1px solid {BORDER_COLOR};
    border-radius: 6px;
    gridline-color: transparent;
    font-size: 13px;
    color: {TEXT_PRIMARY};
    outline: none;
}}

QTableWidget::item {{
    padding: 8px 12px;
    color: {TEXT_PRIMARY};
    border-bottom: 1px solid #f0f0f0;
}}

QTableWidget::item:selected {{
    background-color: #e8f0fe;
    color: {PRIMARY_COLOR};
}}

QTableWidget::item:alternate {{
    background-color: {BACKGROUND};
}}

QHeaderView {{
    background-color: {CARD_BG};
}}

QHeaderView::section {{
    background-color: {BACKGROUND};
    color: {TEXT_SECONDARY};
    padding: 10px 12px;
    border: none;
    border-bottom: 2px solid {BORDER_COLOR};
    font-weight: 600;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

/* Scroll Bars */
QScrollBar:vertical {{
    border: none;
    background: {BACKGROUND};
    width: 10px;
    margin: 0;
}}

QScrollBar::handle:vertical {{
    background: {BORDER_COLOR};
    min-height: 20px;
    border-radius: 5px;
}}

QScrollBar::handle:vertical:hover {{
    background: {TEXT_SECONDARY};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

/* Group Box */
QGroupBox {{
    border: 1px solid {BORDER_COLOR};
    border-radius: 8px;
    margin-top: 16px;
    padding: 16px 12px 12px 12px;
    font-weight: 600;
    color: {TEXT_PRIMARY};
    background-color: {CARD_BG};
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    padding: 2px 8px;
    background-color: {CARD_BG};
    color: {TEXT_PRIMARY};
    font-size: 13px;
    font-weight: 600;
}}

/* Combo Box */
QComboBox {{
    background-color: {CARD_BG};
    border: 1px solid {BORDER_COLOR};
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 14px;
    color: {TEXT_PRIMARY};
}}

QComboBox:focus {{
    border: 2px solid {PRIMARY_COLOR};
    padding: 7px 11px;
    background-color: #ffffff;
}}

QComboBox::drop-down {{
    border: none;
    width: 32px;
    subcontrol-origin: padding;
    subcontrol-position: center right;
}}

QComboBox::down-arrow {{
    width: 12px;
    height: 12px;
}}

QComboBox QAbstractItemView {{
    background-color: {CARD_BG};
    border: 1px solid {BORDER_COLOR};
    border-radius: 8px;
    selection-background-color: #e8f0fe;
    padding: 4px;
}}

QComboBox QAbstractItemView::item {{
    padding: 10px 16px;
    border-radius: 4px;
}}

QComboBox QAbstractItemView::item:selected {{
    background-color: #e8f0fe;
    color: {PRIMARY_COLOR};
}}

/* Status Bar */
QStatusBar {{
    background-color: {CARD_BG};
    color: {TEXT_SECONDARY};
    border-top: 1px solid {BORDER_COLOR};
}}

/* Menu Bar */
QMenuBar {{
    background-color: {CARD_BG};
    color: {TEXT_PRIMARY};
    border-bottom: 1px solid {BORDER_COLOR};
}}

QMenuBar::item {{
    padding: 8px 12px;
}}

QMenuBar::item:selected {{
    background-color: {BACKGROUND};
}}

QMenu {{
    background-color: {CARD_BG};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_COLOR};
    padding: 4px;
}}

QMenu::item {{
    color: {TEXT_PRIMARY};
    padding: 8px 24px;
    border-radius: 4px;
}}

QMenu::item:selected {{
    background-color: {PRIMARY_COLOR};
    color: #ffffff;
}}

/* Tool Bar */
QToolBar {{
    background-color: {CARD_BG};
    border-bottom: 1px solid {BORDER_COLOR};
    spacing: 8px;
    padding: 8px;
}}

QToolButton {{
    background-color: {PRIMARY_COLOR};
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 10px 16px;
    font-weight: 600;
    min-height: 32px;
    min-width: 70px;
}}

QToolButton:hover {{
    background-color: #1d4ed8;
}}

QToolButton:pressed {{
    background-color: #1e40af;
}}
"""

# Card widget styling
CARD_STYLE = f"""
    background-color: {CARD_BG};
    border: 1px solid {BORDER_COLOR};
    border-radius: 8px;
    padding: 16px;
"""

INFO_CARD_SUCCESS = f"""
    background-color: #d1fae5;
    border: 2px solid {SUCCESS_COLOR};
    border-radius: 8px;
    padding: 16px;
    color: #065f46;
    font-weight: 600;
"""

INFO_CARD_DANGER = f"""
    background-color: #fee2e2;
    border: 2px solid {DANGER_COLOR};
    border-radius: 8px;
    padding: 16px;
    color: #991b1b;
    font-weight: 600;
"""

INFO_CARD_WARNING = f"""
    background-color: #fef3c7;
    border: 2px solid {WARNING_COLOR};
    border-radius: 8px;
    padding: 16px;
    color: #92400e;
    font-weight: 600;
"""
