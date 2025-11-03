from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QApplication, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QSize
from PySide6.QtGui import QIcon, QPixmap, QFont
from utils.helpers import resource_path
from utils.styles import BUTTON_STYLE

class TaskChoiceWidget(QWidget):
    def __init__(self, parent, on_complete, on_defer):
        super().__init__(parent)
        self.on_complete = on_complete
        self.on_defer = on_defer
        self.selected_index = 0  # 0: Завершить, 1: Отложить
        self.buttons = []
        self.init_ui()
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")  # Полностью прозрачный фон
        self.start_animation()
        QTimer.singleShot(10000, self.close)  # Закрытие через 10 секунд

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        # Кнопка "Завершить"
        complete_button = QPushButton()
        complete_icon = QIcon(QPixmap(resource_path("resources/check.png")))
        complete_button.setIcon(complete_icon)
        complete_button.setIconSize(QSize(60, 60))  # Увеличенный размер иконки
        complete_button.setFixedSize(80, 80)  # Увеличенный размер кнопки
        complete_button.setStyleSheet("""
            QPushButton {
                background: transparent;  # Прозрачный фон
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.1);
            }
        """)
        complete_button.clicked.connect(self.complete_task)
        layout.addWidget(complete_button)
        self.buttons.append(complete_button)

        # Кнопка "Отложить"
        defer_button = QPushButton()
        defer_icon = QIcon(QPixmap(resource_path("resources/clock.png")))
        defer_button.setIcon(defer_icon)
        defer_button.setIconSize(QSize(60, 60))  # Увеличенный размер иконки
        defer_button.setFixedSize(80, 80)  # Увеличенный размер кнопки
        defer_button.setStyleSheet("""
            QPushButton {
                background: transparent;  # Прозрачный фон
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.1);
            }
        """)
        defer_button.clicked.connect(self.defer_task)
        layout.addWidget(defer_button)
        self.buttons.append(defer_button)

        self.setLayout(layout)
        self.update_selection()

    def start_animation(self):
        """Запускает анимацию появления виджета."""
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(300)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.start()

    def show_at(self, position):
        """Показывает виджет рядом с курсором."""
        screen = self.screen().availableGeometry()
        widget_size = self.sizeHint()
        x = position.x() - widget_size.width() // 2
        y = position.y() - widget_size.height() - 20
        x = max(0, min(x, screen.width() - widget_size.width()))
        y = max(0, min(y, screen.height() - widget_size.height()))
        self.move(x, y)
        self.show()
        self.setFocus()  # Устанавливаем фокус для обработки клавиш

    def update_selection(self):
        """Обновляет визуальное выделение кнопок."""
        for i, button in enumerate(self.buttons):
            if i == self.selected_index:
                button.setStyleSheet(button.styleSheet() + "border: 2px solid #FFFFFF;")
            else:
                button.setStyleSheet(button.styleSheet().replace("border: 2px solid #FFFFFF;", ""))

    def keyPressEvent(self, event):
        """Обрабатывает нажатия клавиш для выбора и подтверждения."""
        if event.key() == Qt.Key_1:  # Клавиша "1" для "Завершить"
            self.complete_task()
        elif event.key() == Qt.Key_2:  # Клавиша "2" для "Отложить"
            self.defer_task()
        elif event.key() == Qt.Key_Left:
            self.selected_index = 1  # Отложить
            self.update_selection()
        elif event.key() == Qt.Key_Right:
            self.selected_index = 0  # Завершить
            self.update_selection()
        elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            if self.selected_index == 0:
                self.complete_task()
            else:
                self.defer_task()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def complete_task(self):
        """Обрабатывает выбор 'Завершить'."""
        self.on_complete()
        self.close()

    def defer_task(self):
        """Обрабатывает выбор 'Отложить'."""
        self.on_defer()
        self.close()

    def closeEvent(self, event):
        """Восстанавливает курсор и завершает анимацию при закрытии."""
        QApplication.restoreOverrideCursor()
        event.accept()