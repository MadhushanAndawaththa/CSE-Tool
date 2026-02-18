"""
Screenshot capture script — generates docs/screenshots/light_mode.png and dark_mode.png.
Run once with: python capture_screenshots.py
"""
import sys
import os

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(__file__))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QScreen

from gui.main_window import MainWindow
from gui.styles import GLOBAL_STYLESHEET

SAVE_DIR = os.path.join(os.path.dirname(__file__), "docs", "screenshots")
os.makedirs(SAVE_DIR, exist_ok=True)

app = QApplication(sys.argv)
app.setApplicationName("CSE Stock Analyzer")
app.setStyle("Fusion")
app.setStyleSheet(GLOBAL_STYLESHEET)

window = MainWindow()
window.resize(1280, 800)
window.show()

step = [0]  # mutable counter for closure


def capture():
    if step[0] == 0:
        # Light mode — already the default
        pixmap = window.grab()
        path = os.path.join(SAVE_DIR, "light_mode.png")
        pixmap.save(path)
        print(f"Saved: {path}")
        # Switch to dark mode
        window.apply_theme(True)
        step[0] = 1
        QTimer.singleShot(400, capture)

    elif step[0] == 1:
        pixmap = window.grab()
        path = os.path.join(SAVE_DIR, "dark_mode.png")
        pixmap.save(path)
        print(f"Saved: {path}")
        print("Done.")
        app.quit()


# Wait for the window to fully render before capturing
QTimer.singleShot(600, capture)
sys.exit(app.exec())
