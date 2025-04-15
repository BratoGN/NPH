from PySide6.QtWidgets import QLabel, QApplication
from PySide6.QtCore import Qt, Signal, QPoint, QMimeData  # Переносим QMimeData сюда
from PySide6.QtGui import QDrag, QPixmap, QPainter, QFont


class DraggableButtonLabel(QLabel):
    dragFinished = Signal()

    def __init__(self, display_text, drag_text=None, parent=None):
        super().__init__(display_text, parent)
        self.display_text = display_text
        self.drag_text = drag_text if drag_text is not None else display_text
        self.setStyleSheet("color: white; background-color: #3C3C3E; padding: 5px; border-radius: 5px;")
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # Устанавливаем шрифт и его размер
        font = QFont()
        font.setPointSize(10)  # Увеличиваем размер шрифта (можно изменить на нужный, например, 14)
        self.setFont(font)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < 10:
            return

        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(self.drag_text)
        drag.setMimeData(mime_data)

        pixmap = QPixmap(self.size())
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setOpacity(0.8)
        self.render(painter, QPoint(0, 0))
        painter.end()
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos() - self.drag_start_position)

        drag.exec(Qt.CopyAction)
        self.dragFinished.emit()