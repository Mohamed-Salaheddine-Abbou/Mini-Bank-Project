# utils/styles.py

DARK_STYLE = """
QWidget {
    background-color: #1e1e1e;
    color: #e0e0e0;
    font-family: 'Arial', sans-serif;
    font-size: 14px;
}
QLineEdit {
    background-color: #2d2d2d;
    border: 1px solid #3e3e3e;
    color: #ffffff;
    padding: 8px;
    border-radius: 6px;
}
QPushButton {
    background-color: #333333;
    border: 1px solid #444444;
    color: #cccccc;
    padding: 8px 16px;
    border-radius: 6px;
    font-weight: 600;
}
QPushButton:hover {
    background-color: #444444;
    border-color: #555555;
}
QPushButton:pressed {
    background-color: #222222;
}
QHeaderView::section {
    background-color: #2d2d2d;
    color: #cccccc;
    padding: 6px;
    border: 1px solid #3e3e3e;
}
QTableWidget {
    gridline-color: #3e3e3e;
    background-color: #1e1e1e;
    color: #cccccc;
    selection-background-color: #3a3a3a;
}
QTabWidget::pane {
    border: 1px solid #3e3e3e;
}
QTabBar::tab {
    background-color: #2d2d2d;
    color: #cccccc;
    padding: 8px 16px;
    border: 1px solid #3e3e3e;
    margin-right: 2px;
}
QTabBar::tab:selected {
    background-color: #444444;
}
QTextEdit {
    background-color: #1e1e1e;
    color: #cccccc;
    border: 1px solid #3e3e3e;
}
QDialog {
    background-color: #1e1e1e;
}
QMessageBox {
    background-color: #1e1e1e;
    color: #cccccc;
}
"""

LIGHT_STYLE = """
QWidget {
    background-color: #D9D9D9;
    color: #1e1e1e;
    font-family: 'Arial', sans-serif;
    font-size: 14px;
}
QLineEdit {
    background-color: #ffffff;
    border: 1px solid #cccccc;
    color: #000000;
    padding: 8px;
    border-radius: 8px;
}
QPushButton {
    background-color: #e0e0e0;
    border: 1px solid #cccccc;
    color: #333333;
    padding: 8px 16px;
    border-radius: 8px;
    font-weight: 600;
}
QPushButton:hover {
    background-color: #d0d0d0;
    border-color: #bbbbbb;
}
QPushButton:pressed {
    background-color: #c0c0c0;
}
QPushButton#DangerButton {
    background-color: #e74c3c;
    color: white;
    border: none;
}
QPushButton#DangerButton:hover {
    background-color: #c0392b;
}
QHeaderView::section {
    background-color: #e0e0e0;
    color: #333333;
    padding: 6px;
    border: none;
    border-bottom: 1px solid #cccccc;
}
QTableWidget {
    gridline-color: transparent;
    background-color: #ffffff;
    color: #333333;
    selection-background-color: #a0a0a0;
    border: 1px solid #cccccc;
    border-radius: 8px;
}
QTableWidget::item {
    padding: 10px;
}
QTableWidget QLineEdit { /* Style for editors in QTableWidget */
    background-color: #ffffff; /* Explicitly white to match non-alternating rows */
    border: none; /* Remove border */
    padding: 0px; /* Remove padding, controlled by item delegate */
    color: #333333; /* Match cell text color */
}
QTableWidget QTableCornerButton::section {
    background-color: #e0e0e0;
    border: none;
    border-bottom: 1px solid #cccccc;
}
QTabWidget::pane {
    border: none;
}
QTabBar::tab {
    background-color: #e0e0e0;
    color: #333333;
    padding: 8px 16px;
    border: 1px solid #cccccc;
    margin-right: 2px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
}
QTabBar::tab:selected {
    background-color: #ffffff;
    border-bottom-color: #ffffff;
}
QTabBar::tab:!selected {
    background-color: #e0e0e0;
}
QTextEdit {
    background-color: #ffffff;
    color: #000000;
    border: 1px solid #cccccc;
    border-radius: 8px;
}
QDialog {
    background-color: #D9D9D9;
}
QMessageBox {
    background-color: #D9D9D9;
    color: #1e1e1e;
}
"""
