"""UI styling and themes for WBAN Node Research application."""
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt

# Color scheme
COLORS = {
    "bg_dark": "#1e1e1e",
    "bg_lighter": "#2d2d2d",
    "bg_panel": "#3d3d3d",
    "text_primary": "#e0e0e0",
    "text_secondary": "#999999",
    "accent": "#0d47a1",
    "success": "#4caf50",
    "warning": "#ff9800",
    "error": "#f44336",
    "border": "#555555",
}

# Stylesheet for dark theme
DARK_STYLESHEET = f"""
QMainWindow {{
    background-color: {COLORS["bg_dark"]};
    color: {COLORS["text_primary"]};
}}

QWidget {{
    background-color: {COLORS["bg_dark"]};
    color: {COLORS["text_primary"]};
}}

QTabWidget::pane {{
    border: 1px solid {COLORS["border"]};
}}

QTabBar::tab {{
    background-color: {COLORS["bg_lighter"]};
    color: {COLORS["text_primary"]};
    padding: 5px 15px;
    margin: 2px;
    border: 1px solid {COLORS["border"]};
    border-bottom: none;
}}

QTabBar::tab:selected {{
    background-color: {COLORS["accent"]};
    color: white;
}}

QTabBar::tab:hover {{
    background-color: {COLORS["bg_panel"]};
}}

QMenuBar {{
    background-color: {COLORS["bg_lighter"]};
    color: {COLORS["text_primary"]};
    border-bottom: 1px solid {COLORS["border"]};
}}

QMenuBar::item:selected {{
    background-color: {COLORS["accent"]};
}}

QMenu {{
    background-color: {COLORS["bg_lighter"]};
    color: {COLORS["text_primary"]};
    border: 1px solid {COLORS["border"]};
}}

QMenu::item:selected {{
    background-color: {COLORS["accent"]};
}}

QPushButton {{
    background-color: {COLORS["accent"]};
    color: white;
    border: none;
    border-radius: 3px;
    padding: 5px 15px;
    font-weight: bold;
}}

QPushButton:hover {{
    background-color: #1565c0;
}}

QPushButton:pressed {{
    background-color: #0d3d8f;
}}

QPushButton:disabled {{
    background-color: {COLORS["bg_panel"]};
    color: {COLORS["text_secondary"]};
}}

QLineEdit {{
    background-color: {COLORS["bg_panel"]};
    color: {COLORS["text_primary"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 3px;
    padding: 5px;
}}

QLineEdit:focus {{
    border: 2px solid {COLORS["accent"]};
}}

QTextEdit {{
    background-color: {COLORS["bg_panel"]};
    color: {COLORS["text_primary"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 3px;
}}

QTreeWidget {{
    background-color: {COLORS["bg_panel"]};
    color: {COLORS["text_primary"]};
    border: 1px solid {COLORS["border"]};
    alternate-background-color: {COLORS["bg_lighter"]};
}}

QTreeWidget::item:selected {{
    background-color: {COLORS["accent"]};
}}

QTableWidget {{
    background-color: {COLORS["bg_panel"]};
    color: {COLORS["text_primary"]};
    border: 1px solid {COLORS["border"]};
    gridline-color: {COLORS["border"]};
    alternate-background-color: {COLORS["bg_lighter"]};
}}

QTableWidget::item:selected {{
    background-color: {COLORS["accent"]};
}}

QHeaderView::section {{
    background-color: {COLORS["bg_lighter"]};
    color: {COLORS["text_primary"]};
    padding: 5px;
    border: 1px solid {COLORS["border"]};
}}

QComboBox {{
    background-color: {COLORS["bg_panel"]};
    color: {COLORS["text_primary"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 3px;
    padding: 5px;
}}

QComboBox::drop-down {{
    border: none;
}}

QComboBox::down-arrow {{
    image: none;
}}

QSpinBox, QDoubleSpinBox {{
    background-color: {COLORS["bg_panel"]};
    color: {COLORS["text_primary"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 3px;
}}

QLabel {{
    color: {COLORS["text_primary"]};
}}

QStatusBar {{
    background-color: {COLORS["bg_lighter"]};
    color: {COLORS["text_primary"]};
    border-top: 1px solid {COLORS["border"]};
}}

QProgressBar {{
    background-color: {COLORS["bg_panel"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 3px;
}}

QProgressBar::chunk {{
    background-color: {COLORS["accent"]};
}}

QScrollBar:vertical {{
    background-color: {COLORS["bg_panel"]};
    width: 12px;
}}

QScrollBar::handle:vertical {{
    background-color: {COLORS["border"]};
    border-radius: 6px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {COLORS["text_secondary"]};
}}

QScrollBar:horizontal {{
    background-color: {COLORS["bg_panel"]};
    height: 12px;
}}

QScrollBar::handle:horizontal {{
    background-color: {COLORS["border"]};
    border-radius: 6px;
}}

QScrollBar::handle:horizontal:hover {{
    background-color: {COLORS["text_secondary"]};
}}

QCheckBox {{
    color: {COLORS["text_primary"]};
    spacing: 5px;
}}

QCheckBox::indicator {{
    width: 18px;
    height: 18px;
}}

QCheckBox::indicator:unchecked {{
    background-color: {COLORS["bg_panel"]};
    border: 1px solid {COLORS["border"]};
}}

QCheckBox::indicator:checked {{
    background-color: {COLORS["accent"]};
    border: 1px solid {COLORS["accent"]};
}}

QGroupBox {{
    color: {COLORS["text_primary"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 3px;
    margin-top: 10px;
    padding-top: 10px;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    margin-left: 5px;
    padding: 0 5px;
}}
"""

def get_status_color(status: str) -> str:
    """Get color for device status."""
    status_colors = {
        "discovered": COLORS["warning"],
        "connecting": COLORS["warning"],
        "connected": COLORS["success"],
        "disconnected": COLORS["error"],
        "error": COLORS["error"],
        "terminated": COLORS["error"],
    }
    return status_colors.get(status.lower(), COLORS["text_secondary"])

def format_rssi(rssi: int) -> tuple:
    """Format RSSI value with color.
    
    Returns:
        Tuple of (formatted_text, color)
    """
    if rssi >= -30:
        return f"{rssi} dBm (Excellent)", COLORS["success"]
    elif rssi >= -60:
        return f"{rssi} dBm (Good)", "#90ee90"
    elif rssi >= -80:
        return f"{rssi} dBm (Fair)", COLORS["warning"]
    else:
        return f"{rssi} dBm (Poor)", COLORS["error"]
