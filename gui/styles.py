"""
Clean, modern styling for CSE Stock Analyzer GUI.
Flat design with subtle accents - no heavy gradients or oversized elements.
"""

# --- Color Palette ---
PRIMARY = "#2563eb"
PRIMARY_LIGHT = "#dbeafe"
PRIMARY_HOVER = "#1d4ed8"
PRIMARY_DARK = "#1e40af"

SUCCESS = "#059669"
SUCCESS_LIGHT = "#d1fae5"

WARNING = "#d97706"
WARNING_LIGHT = "#fef3c7"

DANGER = "#dc2626"
DANGER_LIGHT = "#fee2e2"

INFO = "#0891b2"
INFO_LIGHT = "#cffafe"

BG = "#f1f5f9"
SURFACE = "#ffffff"
TEXT = "#1e293b"
TEXT_DIM = "#64748b"
TEXT_MUTED = "#94a3b8"
BORDER = "#e2e8f0"
HOVER = "#f8fafc"

_D_BG = "#0f172a"
_D_SURFACE = "#1e293b"
_D_TEXT = "#e2e4e7"
_D_TEXT_DIM = "#94a3b8"
_D_BORDER = "#334155"

# aliases kept for imports in tabs
TEXT_SECONDARY = TEXT_DIM
TEXT_SECONDARY_DARK = _D_TEXT_DIM
# legacy aliases
PRIMARY_COLOR = PRIMARY
PRIMARY_LIGHT_COLOR = PRIMARY_LIGHT
SUCCESS_COLOR = SUCCESS
WARNING_COLOR = WARNING
DANGER_COLOR = DANGER
CARD_BG = SURFACE
TEXT_PRIMARY = TEXT
BORDER_COLOR = BORDER
BACKGROUND = BG

FONT = "'Segoe UI', 'Roboto', 'Helvetica Neue', sans-serif"

GLOBAL_STYLESHEET = f"""
QMainWindow {{
    background: {BG};
    font-family: {FONT};
}}

#HeaderBar {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 {PRIMARY}, stop:1 {PRIMARY_HOVER});
    border: none;
    border-radius: 10px;
}}
#HeaderTitle {{
    color: #fff;
    font-size: 17px;
    font-weight: 700;
    letter-spacing: 0.3px;
}}
#HeaderSubtitle {{
    color: rgba(255,255,255,0.78);
    font-size: 12px;
    font-weight: 400;
}}
#HeaderBadge {{
    color: rgba(255,255,255,0.9);
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.3);
    border-radius: 10px;
    padding: 2px 8px;
    font-size: 10px;
    font-weight: 600;
}}

QTabWidget::pane {{
    border: 1px solid {BORDER};
    background: {SURFACE};
    border-radius: 10px;
    padding: 6px;
}}
QTabWidget::tab-bar {{
    alignment: left;
    left: 8px;
}}
QTabBar::tab {{
    background: transparent;
    color: {TEXT_DIM};
    padding: 8px 16px;
    margin-right: 2px;
    font-size: 13px;
    font-weight: 600;
    border-bottom: 2px solid transparent;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
}}
QTabBar::tab:selected {{
    color: {PRIMARY};
    border-bottom: 2px solid {PRIMARY};
    background: {HOVER};
}}
QTabBar::tab:hover:!selected {{
    background: {HOVER};
    color: {TEXT};
}}

QLabel {{
    color: {TEXT};
    font-family: {FONT};
    font-size: 13px;
}}
QLabel[heading="true"] {{
    font-size: 18px;
    font-weight: 700;
    color: {TEXT};
    padding: 2px 0;
}}
QLabel[subheading="true"] {{
    font-size: 14px;
    font-weight: 600;
    color: {TEXT};
    padding-bottom: 2px;
}}

QLineEdit, QTextEdit {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 13px;
    color: {TEXT};
    selection-background-color: {PRIMARY_LIGHT};
}}
QLineEdit:focus, QTextEdit:focus {{
    border: 1.5px solid {PRIMARY};
    background: #fafbff;
}}
QLineEdit:disabled {{
    background: {BG};
    color: {TEXT_MUTED};
    border: 1px dashed {BORDER};
}}

QSpinBox, QDoubleSpinBox {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 13px;
    color: {TEXT};
}}
QSpinBox:focus, QDoubleSpinBox:focus {{
    border: 1.5px solid {PRIMARY};
}}

QPushButton {{
    background: {PRIMARY};
    color: #fff;
    border: none;
    border-radius: 6px;
    padding: 6px 14px;
    font-size: 13px;
    font-weight: 600;
    min-height: 30px;
}}
QPushButton:hover {{
    background: {PRIMARY_HOVER};
}}
QPushButton:pressed {{
    background: {PRIMARY_DARK};
}}
QPushButton:disabled {{
    background: #cbd5e1;
    color: #94a3b8;
}}
QPushButton[buttonStyle="success"] {{
    background: {SUCCESS};
}}
QPushButton[buttonStyle="success"]:hover {{
    background: #047857;
}}
QPushButton[buttonStyle="danger"] {{
    background: {DANGER};
}}
QPushButton[buttonStyle="danger"]:hover {{
    background: #b91c1c;
}}
QPushButton[buttonStyle="secondary"] {{
    background: transparent;
    color: {PRIMARY};
    border: 1px solid {BORDER};
}}
QPushButton[buttonStyle="secondary"]:hover {{
    background: {PRIMARY_LIGHT};
    border-color: {PRIMARY};
}}

QCheckBox, QRadioButton {{
    color: {TEXT};
    font-size: 13px;
    spacing: 6px;
    padding: 2px;
}}
QCheckBox::indicator {{
    width: 16px; height: 16px;
    border: 1.5px solid {BORDER};
    border-radius: 3px;
    background: #fff;
}}
QCheckBox::indicator:checked {{
    background: {PRIMARY};
    border-color: {PRIMARY};
}}
QRadioButton::indicator {{
    width: 16px; height: 16px;
    border: 1.5px solid {BORDER};
    border-radius: 8px;
    background: #fff;
}}
QRadioButton::indicator:checked {{
    background: {PRIMARY};
    border-color: {PRIMARY};
}}

QTableWidget {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 6px;
    gridline-color: transparent;
    font-size: 12px;
    color: {TEXT};
    outline: none;
}}
QTableWidget::item {{
    padding: 5px 8px;
    border-bottom: 1px solid #f1f5f9;
}}
QTableWidget::item:selected {{
    background: {PRIMARY_LIGHT};
    color: {PRIMARY};
}}
QTableWidget::item:alternate {{
    background: {BG};
}}
QHeaderView {{
    background: {SURFACE};
}}
QHeaderView::section {{
    background: {BG};
    color: {TEXT_DIM};
    padding: 5px 8px;
    border: none;
    border-bottom: 1.5px solid {BORDER};
    font-weight: 700;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

QScrollBar:vertical {{
    border: none;
    background: transparent;
    width: 7px;
}}
QScrollBar::handle:vertical {{
    background: {BORDER};
    min-height: 24px;
    border-radius: 3px;
}}
QScrollBar::handle:vertical:hover {{
    background: {TEXT_MUTED};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}

QGroupBox {{
    border: 1px solid {BORDER};
    border-radius: 8px;
    margin-top: 12px;
    padding: 12px 10px 10px 10px;
    font-weight: 600;
    color: {TEXT};
    background: {SURFACE};
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 10px;
    padding: 2px 8px;
    background: {PRIMARY};
    color: #fff;
    font-size: 11px;
    font-weight: 700;
    border-radius: 6px;
}}

QComboBox {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 13px;
    color: {TEXT};
}}
QComboBox:focus {{
    border: 1.5px solid {PRIMARY};
}}
QComboBox::drop-down {{
    border: none;
    width: 24px;
}}
QComboBox QAbstractItemView {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    selection-background-color: {PRIMARY_LIGHT};
    padding: 2px;
}}

QStatusBar {{
    background: {SURFACE};
    color: {TEXT_DIM};
    font-size: 12px;
    border-top: 1px solid {BORDER};
    padding: 2px 8px;
}}

QMenuBar {{
    background: {SURFACE};
    color: {TEXT};
    border-bottom: 1px solid {BORDER};
    font-size: 13px;
}}
QMenuBar::item {{
    padding: 5px 10px;
}}
QMenuBar::item:selected {{
    background: {BG};
    border-radius: 4px;
}}
QMenu {{
    background: {SURFACE};
    color: {TEXT};
    border: 1px solid {BORDER};
    padding: 4px;
    border-radius: 6px;
}}
QMenu::item {{
    padding: 5px 18px;
    border-radius: 4px;
}}
QMenu::item:selected {{
    background: {PRIMARY};
    color: #fff;
}}

QToolBar {{
    background: {SURFACE};
    border-bottom: 1px solid {BORDER};
    spacing: 4px;
    padding: 3px 6px;
}}
QToolButton {{
    background: transparent;
    color: {TEXT};
    border: 1px solid {BORDER};
    border-radius: 5px;
    padding: 4px 10px;
    font-weight: 600;
    font-size: 12px;
    min-height: 24px;
    min-width: 44px;
}}
QToolButton:hover {{
    background: {PRIMARY_LIGHT};
    border-color: {PRIMARY};
    color: {PRIMARY};
}}
QToolButton:pressed, QToolButton:checked {{
    background: {PRIMARY};
    color: #fff;
    border-color: {PRIMARY};
}}
"""

GLOBAL_STYLESHEET_DARK = f"""
QMainWindow {{ background: {_D_BG}; }}

#HeaderBar {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 {PRIMARY_DARK}, stop:1 {PRIMARY});
    border: none; border-radius: 10px;
}}
#HeaderTitle {{ color:#fff; font-size:17px; font-weight:700; }}
#HeaderSubtitle {{ color:rgba(255,255,255,0.72); font-size:12px; }}
#HeaderBadge {{
    color:rgba(255,255,255,0.85);
    background:rgba(255,255,255,0.1);
    border:1px solid rgba(255,255,255,0.22);
    border-radius:10px; padding:2px 8px;
    font-size:10px; font-weight:600;
}}

QTabWidget::pane {{
    border:1px solid {_D_BORDER};
    background:{_D_SURFACE};
    border-radius:10px; padding:6px;
}}
QTabBar::tab {{
    background:transparent; color:{_D_TEXT_DIM};
    padding:8px 16px; font-size:13px; font-weight:600;
    border-bottom:2px solid transparent;
    border-top-left-radius:6px; border-top-right-radius:6px;
    margin-right:2px;
}}
QTabBar::tab:selected {{
    color:#93c5fd;
    border-bottom:2px solid #93c5fd;
    background:rgba(255,255,255,0.04);
}}
QTabBar::tab:hover:!selected {{
    background:rgba(255,255,255,0.03);
    color:{_D_TEXT};
}}

QLabel {{ color:{_D_TEXT}; }}
QLabel[heading="true"] {{ color:{_D_TEXT}; }}
QLabel[subheading="true"] {{ color:{_D_TEXT}; }}

QGroupBox {{
    border:1px solid {_D_BORDER}; border-radius:8px;
    margin-top:12px; padding:12px 10px 10px 10px;
    color:{_D_TEXT}; background:{_D_SURFACE};
}}
QGroupBox::title {{
    subcontrol-origin:margin; subcontrol-position:top left;
    left:10px; padding:2px 8px;
    background:{PRIMARY_DARK}; color:#fff;
    font-size:11px; font-weight:700; border-radius:6px;
}}

QLineEdit, QTextEdit {{
    background: #0f172a;
    border: 1px solid {_D_BORDER};
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 13px;
    color: {_D_TEXT};
    selection-background-color: #1e3a5f;
}}
QLineEdit:focus, QTextEdit:focus {{
    border: 1.5px solid #60a5fa;
    background: #131c2e;
}}
QLineEdit:disabled {{
    background: #0c1322;
    color: #475569;
    border: 1px dashed {_D_BORDER};
}}

QPushButton {{
    background: {PRIMARY};
    color: #fff;
    border: none;
    border-radius: 6px;
    padding: 6px 14px;
    font-size: 13px;
    font-weight: 600;
    min-height: 30px;
}}
QPushButton:hover {{ background: #3b82f6; }}
QPushButton:pressed {{ background: {PRIMARY_DARK}; }}
QPushButton:disabled {{ background: #334155; color: #64748b; }}
QPushButton[buttonStyle="success"] {{ background: {SUCCESS}; }}
QPushButton[buttonStyle="success"]:hover {{ background: #10b981; }}
QPushButton[buttonStyle="danger"] {{ background: {DANGER}; }}
QPushButton[buttonStyle="danger"]:hover {{ background: #ef4444; }}
QPushButton[buttonStyle="secondary"] {{
    background: transparent;
    color: #93c5fd;
    border: 1px solid {_D_BORDER};
}}
QPushButton[buttonStyle="secondary"]:hover {{
    background: rgba(59,130,246,0.15);
    border-color: #60a5fa;
}}

QCheckBox, QRadioButton {{ color:{_D_TEXT}; font-size:13px; }}
QCheckBox::indicator {{
    width:16px; height:16px;
    border:1.5px solid {_D_BORDER};
    border-radius:3px; background:#0f172a;
}}
QCheckBox::indicator:checked {{ background:{PRIMARY}; border-color:{PRIMARY}; }}
QRadioButton::indicator {{
    width:16px; height:16px;
    border:1.5px solid {_D_BORDER};
    border-radius:8px; background:#0f172a;
}}
QRadioButton::indicator:checked {{ background:{PRIMARY}; border-color:{PRIMARY}; }}

QTableWidget {{
    background: {_D_SURFACE};
    border: 1px solid {_D_BORDER};
    border-radius: 6px;
    gridline-color: transparent;
    font-size: 12px;
    color: {_D_TEXT};
    outline: none;
}}
QTableWidget::item {{
    padding: 5px 8px;
    border-bottom: 1px solid #1e293b;
    color: {_D_TEXT};
}}
QTableWidget::item:selected {{
    background: rgba(59,130,246,0.25);
    color: #93c5fd;
}}
QTableWidget::item:alternate {{ background: #0f172a; }}
QHeaderView {{ background: {_D_SURFACE}; }}
QHeaderView::section {{
    background: #0f172a;
    color: {_D_TEXT_DIM};
    padding: 5px 8px;
    border: none;
    border-bottom: 1.5px solid {_D_BORDER};
    font-weight: 700;
    font-size: 11px;
}}

QScrollBar:vertical {{
    border:none; background:transparent; width:7px;
}}
QScrollBar::handle:vertical {{
    background:{_D_BORDER}; min-height:24px; border-radius:3px;
}}
QScrollBar::handle:vertical:hover {{ background:#475569; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height:0; }}

QSpinBox, QDoubleSpinBox {{
    background:#0f172a; border:1px solid {_D_BORDER};
    border-radius:6px; padding:6px 10px;
    font-size:13px; color:{_D_TEXT};
}}
QSpinBox:focus, QDoubleSpinBox:focus {{ border:1.5px solid #60a5fa; }}

QComboBox {{
    background:#0f172a; border:1px solid {_D_BORDER};
    border-radius:6px; padding:6px 10px;
    font-size:13px; color:{_D_TEXT};
}}
QComboBox:focus {{ border:1.5px solid #60a5fa; }}
QComboBox::drop-down {{ border:none; width:24px; }}
QComboBox QAbstractItemView {{
    background:{_D_SURFACE}; border:1px solid {_D_BORDER};
    selection-background-color:rgba(59,130,246,0.3);
    color:{_D_TEXT}; padding:2px;
}}

QMenuBar {{
    background: {_D_SURFACE};
    color: {_D_TEXT};
    border-bottom: 1px solid {_D_BORDER};
    font-size: 13px;
}}
QMenuBar::item {{ padding:5px 10px; }}
QMenuBar::item:selected {{ background:rgba(255,255,255,0.08); border-radius:4px; }}
QMenu {{
    background: {_D_SURFACE};
    color: {_D_TEXT};
    border: 1px solid {_D_BORDER};
    padding: 4px;
    border-radius: 6px;
}}
QMenu::item {{ padding:5px 18px; border-radius:4px; }}
QMenu::item:selected {{ background:{PRIMARY}; color:#fff; }}
QMenu::separator {{ height:1px; background:{_D_BORDER}; margin:4px 8px; }}

QToolBar {{
    background: {_D_SURFACE};
    border-bottom: 1px solid {_D_BORDER};
    spacing: 4px;
    padding: 3px 6px;
}}
QToolButton {{
    background: transparent;
    color: {_D_TEXT};
    border: 1px solid {_D_BORDER};
    border-radius: 5px;
    padding: 4px 10px;
    font-weight: 600;
    font-size: 12px;
    min-height: 24px;
    min-width: 44px;
}}
QToolButton:hover {{
    background: rgba(59,130,246,0.15);
    border-color: #60a5fa;
    color: #93c5fd;
}}
QToolButton:pressed, QToolButton:checked {{
    background: {PRIMARY};
    color: #fff;
    border-color: {PRIMARY};
}}

QStatusBar {{
    background: {_D_SURFACE};
    color: {_D_TEXT_DIM};
    font-size: 12px;
    border-top: 1px solid {_D_BORDER};
    padding: 2px 8px;
}}

QMessageBox {{
    background: {_D_SURFACE};
    color: {_D_TEXT};
}}
QMessageBox QLabel {{
    color: {_D_TEXT};
    font-size: 13px;
}}
QMessageBox QPushButton {{
    min-width: 80px;
}}

QDialog {{
    background: {_D_SURFACE};
    color: {_D_TEXT};
}}

QToolTip {{
    background: {_D_SURFACE};
    color: {_D_TEXT};
    border: 1px solid {_D_BORDER};
    padding: 4px 8px;
    font-size: 12px;
    border-radius: 4px;
}}
"""

CARD_STYLE = f"""
    background-color: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 12px;
"""

INFO_CARD_SUCCESS = f"""
    background-color: {SUCCESS_LIGHT};
    border-left: 4px solid {SUCCESS};
    border-radius: 6px;
    padding: 12px 14px;
    color: #065f46;
"""

INFO_CARD_DANGER = f"""
    background-color: {DANGER_LIGHT};
    border-left: 4px solid {DANGER};
    border-radius: 6px;
    padding: 12px 14px;
    color: #991b1b;
"""

INFO_CARD_WARNING = f"""
    background-color: {WARNING_LIGHT};
    border-left: 4px solid {WARNING};
    border-radius: 6px;
    padding: 12px 14px;
    color: #92400e;
"""
