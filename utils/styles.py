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
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                      stop:0 #f5c6c6, stop:1 #e6b8d4);
    font-family: 'Georgia', serif;
    color: #2c2c2c;
}

QLabel {
    font-size: 14px;
    font-weight: bold;
    color: #4b2e33;
}

QLineEdit, QComboBox {
    background-color: #fffafa;
    border: 1px solid #a36f86;
    border-radius: 6px;
    padding: 6px;
    font-size: 14px;
    color: #3a2b2b;
    selection-background-color: #dcaec0;
}

QLineEdit:focus, QComboBox:focus {
    border: 1px solid #c56f90;
    background-color: #fff0f5;
}

QPushButton {
    background-color: #a94468;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 15px;
    font-size: 14px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #c25680;
}

QPushButton[calendar="true"] {
    background-color: #d6a3b0;
    color: #fff;
    font-size: 16px;
    border-radius: 6px;
    padding: 0;
}

QPushButton[calendar="true"]:hover {
    background-color: #e1b4c1;
}
"""



CALENDAR_STYLE = """
QCalendarWidget QWidget {
    alternate-background-color: #fce4ec;
}

QCalendarWidget QToolButton {
    background-color: #a94468;
    color: white;
    font-weight: bold;
    border: none;
    border-radius: 4px;
    padding: 4px;
}

QCalendarWidget QToolButton:hover {
    background-color: #c25680;
}

QCalendarWidget QMenu {
    background-color: #fffafa;
    border: 1px solid #a36f86;
}

QCalendarWidget QSpinBox {
    margin: 2px;
    border: 1px solid #a36f86;
    border-radius: 4px;
}

QCalendarWidget QAbstractItemView:enabled {
    font-size: 13px;
    color: #2c2c2c;
    background-color: #fffafa;
    selection-background-color: #a94468;
    selection-color: white;
}

QCalendarWidget QAbstractItemView:disabled {
    color: #aaa;
}
"""


TIME_TRACKER_STYLE = """
    QWidget {
        background-color: #1C1C1E;
        color: #E0E0E0;
        font-family: 'SF Pro Text', 'Helvetica Neue', sans-serif;
        font-size: 13px;
    }

    QLabel {
        color: #E0E0E0;
    }

    QLineEdit {
        background-color: rgba(44, 44, 46, 0.9);
        border: none;
        border-radius: 6px;
        padding: 6px 8px;
        color: #FFFFFF;
        font-size: 13px;
    }

    QLineEdit:focus {
        background-color: rgba(58, 58, 60, 1.0);
        border: 1px solid #636366;
    }

    QPushButton {
        background-color: #2C2C2E;
        color: #FFFFFF;
        border-radius: 6px;
        padding: 6px 10px;
    }

    QPushButton:hover {
        background-color: #3A3A3C;
    }

    QPushButton:pressed {
        background-color: #1A1A1C;
    }
"""

TIME_TRACKER_INPUT_STYLE = """
    background-color: rgba(44, 44, 46, 0.9);
    border: none;
    border-radius: 6px;
    padding: 6px 8px;
    color: #FFFFFF;
    font-family: 'SF Pro Text', 'Helvetica Neue', sans-serif;
    font-size: 13px;
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