from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor
from utils.styles import SWITCH_STYLE_OFF, SWITCH_STYLE_GREEN, SWITCH_STYLE_RED

class QSwitch(QWidget):
    def __init__(self, parent=None, toggle_callback=None, template_status_callback=None):
        super().__init__(parent)
        self.setFixedSize(40, 20)
        self._checked = False
        self.setStyleSheet(SWITCH_STYLE_OFF)
        self.toggle_callback = toggle_callback
        self.template_status_callback = template_status_callback

    def mousePressEvent(self, event):
        self._checked = not self._checked
        self.update()
        if self.toggle_callback:
            self.toggle_callback(self._checked)
        if self.template_status_callback:
            self.template_status_callback()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect().adjusted(2, 2, -2, -2)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#34C759" if self._checked else "#3A3A3C"))
        painter.drawRoundedRect(rect, 10, 10)
        handle_x = 20 if self._checked else 0
        painter.setBrush(QColor("#FFFFFF"))
        painter.drawEllipse(handle_x, 2, 16, 16)

    def isChecked(self):
        return self._checked

    def setChecked(self, checked):
        self._checked = checked
        self.update()
        if self.template_status_callback:
            self.template_status_callback()

    def update_style(self, has_template):
        if has_template:
            self.setStyleSheet(SWITCH_STYLE_GREEN)
        else:
            self.setStyleSheet(SWITCH_STYLE_RED if self._checked else SWITCH_STYLE_OFF)