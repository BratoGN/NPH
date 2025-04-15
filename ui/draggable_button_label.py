from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QDrag
from PySide6.QtCore import Qt, QMimeData, Signal
from PySide6.QtGui import QPixmap, QPainter, QFont
from utils.styles import NOTE_BUTTON_STYLE

class DraggableButtonLabel(QLabel):
    dragFinished = Signal()

    def __init__(self, text):
        super().__init__(text)
        self.setWordWrap(False)
        self.setStyleSheet(NOTE_BUTTON_STYLE)
        self.setFont(QFont("SF Pro Text", 10))
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.setFixedHeight(30)
        self.adjustSize()

    def mouseMoveEvent(self, event):
        if event.buttons() != Qt.LeftButton:
            return
        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(self.text())
        drag.setMimeData(mime_data)
        pixmap = QPixmap(self.width(), self.height())
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.drawText(pixmap.rect(), Qt.AlignLeft | Qt.AlignVCenter, self.text())
        painter.end()
        drag.setPixmap(pixmap)
        result = drag.exec(Qt.CopyAction)
        if result == Qt.CopyAction:
            self.dragFinished.emit()