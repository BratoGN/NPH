MAIN_STYLE = """
    background-color: #1C1C1E;
"""

BUTTON_STYLE = """
    QPushButton {
        background-color: #2C2C2E;
        color: #FFFFFF;
        border: none;
        border-radius: 5px;
        padding: 5px;
        font-size: 12pt;
        font-family: 'SF Pro Display', 'Helvetica Neue', sans-serif;
        font-weight: 500;
    }
    QPushButton:hover {
        background-color: #3A3A3C;
    }
    QPushButton:pressed {
        background-color: #1A1A1C;
    }
"""

NOTE_BUTTON_STYLE = """
    QLabel {
        background-color: rgba(44, 44, 46, 0.9);
        color: #FFFFFF;
        border: none;
        border-radius: 5px;
        padding: 5px;
        font-size: 10pt;
        font-family: 'SF Pro Text', 'Helvetica Neue', sans-serif;
        text-align: left;
    }
    QLabel:hover {
        background-color: rgba(58, 58, 60, 0.9);
    }
"""

NOTE_PANEL_STYLE = """
    QWidget {
        background-color: rgba(28, 28, 30, 0.85);
        border-radius: 10px;
        border: none;
    }
"""

NOTE_STYLE = """
    QLabel {
        background-color: transparent;
        color: #E0E0E0;
        padding: 5px;
        font-size: 10pt;
        font-family: 'SF Pro Text', 'Helvetica Neue', sans-serif;
    }
"""

CLOSE_BUTTON_STYLE = """
    QPushButton {
        background-color: rgba(255, 69, 58, 0.9);
        color: transparent;
        border: none;
        border-radius: 7px;
        font-size: 0pt;
        min-width: 14px;
        min-height: 14px;
    }
    QPushButton:hover {
        background-color: rgba(255, 69, 58, 1.0);
    }
    QPushButton:pressed {
        background-color: rgba(200, 40, 30, 1.0);
    }
"""

SWITCH_STYLE_OFF = """
    QWidget {
        background-color: #3A3A3C;
        border-radius: 10px;
        min-width: 40px;
        min-height: 20px;
    }
"""

SWITCH_STYLE_GREEN = """
    QWidget {
        background-color: #34C759;
        border-radius: 10px;
        min-width: 40px;
        min-height: 20px;
    }
"""

SWITCH_STYLE_RED = """
    QWidget {
        background-color: #FF3B30;
        border-radius: 10px;
        min-width: 40px;
        min-height: 20px;
    }
"""

PATENT_CALCULATOR_STYLE = """
    QWidget {
        background-color: #1C1C1E;
        font-family: 'SF Pro Display', 'Helvetica Neue', sans-serif;
    }
    QLabel {
        color: #E0E0E0;
        font-size: 14px;
        font-weight: 500;
    }
    QLineEdit, QComboBox {
        padding: 8px;
        border: none;
        border-radius: 10px;
        background-color: rgba(44, 44, 46, 0.9);
        color: #FFFFFF;
        font-size: 14px;
        font-family: 'SF Pro Text', 'Helvetica Neue', sans-serif;
    }
    QLineEdit:focus, QComboBox:focus {
        background-color: rgba(58, 58, 60, 0.9);
    }
    QComboBox::drop-down {
        border: none;
        width: 30px;
    }
    QComboBox::down-arrow {
        image: none;
        width: 0px;
    }
    QComboBox QAbstractItemView {
        background-color: #2C2C2E;
        color: #FFFFFF;
        border: none;
        selection-background-color: #007AFF;
        selection-color: #FFFFFF;
    }
    QPushButton {
        background-color: #007AFF;
        color: #FFFFFF;
        padding: 8px;
        border-radius: 10px;
        font-size: 15px;
        font-weight: 600;
        border: none;
    }
    QPushButton:hover {
        background-color: #005FD7;
    }
    QPushButton:disabled {
        background-color: rgba(44, 44, 46, 0.5);
        color: #6E6E73;
    }
    QPushButton[calendar="true"] {
        background-color: rgba(44, 44, 46, 0.9);
        border: none;
        padding: 4px;
        border-radius: 8px;
    }
    QPushButton[calendar="true"]:hover {
        background-color: rgba(58, 58, 60, 0.9);
    }
"""

CALENDAR_STYLE = """
    QCalendarWidget {
        background-color: #2C2C2E;
        border: none;
        border-radius: 10px;
        color: #E0E0E0;
    }
    QCalendarWidget QToolButton {
        color: #FFFFFF;
        background-color: transparent;
        border: none;
        font-size: 14px;
        font-family: 'SF Pro Display', 'Helvetica Neue', sans-serif;
    }
    QCalendarWidget QToolButton:hover {
        background-color: rgba(58, 58, 60, 0.9);
    }
    QCalendarWidget QMenu {
        background-color: #2C2C2E;
        color: #FFFFFF;
        border: none;
    }
    QCalendarWidget QWidget#qt_calendar_navigationbar {
        background-color: #1C1C1E;
        border-bottom: 1px solid #3A3A3C;
    }
    QCalendarWidget QAbstractItemView {
        background-color: #2C2C2E;
        color: #E0E0E0;
        selection-background-color: #007AFF;
        selection-color: #FFFFFF;
    }
"""

TIME_TRACKER_STYLE = """
    background-color: #1C1C1E;
    color: #E0E0E0;
    font-family: 'SF Pro Text', 'Helvetica Neue', sans-serif;
    font-size: 14px;
"""

TIME_TRACKER_INPUT_STYLE = """
    background-color: rgba(44, 44, 46, 0.9);
    border: none;
    padding: 5px;
    color: #FFFFFF;
    border-radius: 8px;
    font-family: 'SF Pro Text', 'Helvetica Neue', sans-serif;
"""

COUNTER_LABEL_STYLE = """
    QLabel {
        background-color: #2C2C2E;
        color: #FFFFFF;
        border: none;
        border-radius: 5px;
        font-size: 25pt;
        font-weight: 600;
        font-family: 'SF Pro Display', 'Helvetica Neue', sans-serif;
    }
    QLabel:hover {
        background-color: #3A3A3C;
    }
"""

DATE_LABEL_STYLE = """
    QLabel {
        background-color: transparent;
        color: #8E8E93;
        font-size: 10pt;
        font-family: 'SF Pro Text', 'Helvetica Neue', sans-serif;
    }
"""