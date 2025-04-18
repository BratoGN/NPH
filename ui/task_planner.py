from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QScrollArea, QGraphicsDropShadowEffect,
    QGraphicsOpacityEffect, QProgressBar, QApplication
)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QSize
from PySide6.QtGui import QColor, QPixmap
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtCore import QUrl
from datetime import datetime
import os
import sys
import json

def resource_path(relative_path):
    """Возвращает путь к ресурсам для PyCharm и скомпилированного приложения."""
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)

def data_path(filename):
    """Возвращает путь для данных в папке data."""
    if hasattr(sys, '_MEIPASS'):
        # В скомпилированном виде читаем из папки с .exe
        base_path = os.path.dirname(sys.executable)
    else:
        # В PyCharm читаем из корня проекта
        base_path = os.path.abspath('.')
    data_dir = os.path.join(base_path, 'data')
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, filename)

class CongratulationOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(parent.rect())

        # Картинка
        self.card = QLabel(self)
        image_path = resource_path('resources/full.png')
        if not os.path.exists(image_path):
            print(f'Ошибка: файл {image_path} не найден')
        pixmap = QPixmap(image_path)
        max_size = QSize(380, 500)
        scaled_pixmap = pixmap.scaled(max_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.card.setPixmap(scaled_pixmap)
        self.card.setScaledContents(False)
        self.card.setAlignment(Qt.AlignCenter)
        self.card.resize(scaled_pixmap.size())
        self.card.move(
            (self.width() - self.card.width()) // 2,
            (self.height() - self.card.height()) // 2
        )

        # Тень
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(0, 5)
        self.card.setGraphicsEffect(shadow)

        # Прозрачность
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.card.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0)

        # Звук
        self.sound = QSoundEffect(self)
        sound_path = resource_path('resources/full.wav')
        if not os.path.exists(sound_path):
            print(f'Ошибка: файл {sound_path} не найден')
        self.sound.setSource(QUrl.fromLocalFile(sound_path))
        self.sound.setVolume(0.7)

        # Анимации
        self.fade_in = QPropertyAnimation(self.opacity_effect, b'opacity')
        self.fade_in.setDuration(600)
        self.fade_in.setStartValue(0)
        self.fade_in.setEndValue(1)
        self.fade_in.setEasingCurve(QEasingCurve.InOutQuad)

        self.scale_anim = QPropertyAnimation(self.card, b'size')
        self.scale_anim.setDuration(600)
        self.scale_anim.setStartValue(QSize(int(self.card.width() * 0.8), int(self.card.height() * 0.8)))
        self.scale_anim.setEndValue(QSize(self.card.width(), self.card.height()))
        self.scale_anim.setEasingCurve(QEasingCurve.OutBack)

        self.fade_out = QPropertyAnimation(self.opacity_effect, b'opacity')
        self.fade_out.setDuration(600)
        self.fade_out.setStartValue(1)
        self.fade_out.setEndValue(0)
        self.fade_out.setEasingCurve(QEasingCurve.InOutQuad)
        self.fade_out.finished.connect(self.hide)

        # Таймер закрытия
        self.close_timer = QTimer(self)
        self.close_timer.setSingleShot(True)
        self.close_timer.timeout.connect(self.start_fade_out)

    def show_animation(self):
        self.show()
        self.raise_()
        self.sound.play()
        self.fade_in.start()
        self.scale_anim.start()
        self.close_timer.start(3000)

    def start_fade_out(self):
        self.fade_in.stop()
        self.scale_anim.stop()
        self.fade_out.start()

    def mousePressEvent(self, event):
        self.start_fade_out()

class TaskPlanner(QWidget):
    def __init__(self):
        super().__init__()
        self.task_history_file = data_path('task_history.json')
        self.monthly_goal = 5000
        self.last_progress_percent = 0
        self.overlay = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Task Planner')
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: #E0E0E0;
                font-family: 'SF Pro Display', 'Helvetica Neue', sans-serif;
            }
        """)
        self.setFixedSize(400, 550)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        header = QLabel('Планировщик задач')
        header.setStyleSheet("""
            font-size: 20px;
            font-weight: 600;
            color: #FFFFFF;
            padding: 8px;
            background: rgba(28, 28, 30, 0.8);
            border-radius: 10px;
        """)
        header.setAlignment(Qt.AlignCenter)
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(10)
        glow.setColor(QColor(0, 0, 0, 80))
        glow.setOffset(0, 1)
        header.setGraphicsEffect(glow)
        main_layout.addWidget(header)

        scroll = QScrollArea()
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: rgba(28, 28, 30, 0.7);
                width: 6px;
                margin: 0;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical {
                background: rgba(80, 80, 82, 0.9);
                border-radius: 3px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
            }
        """)
        scroll_widget = QWidget()
        self.history_layout = QVBoxLayout(scroll_widget)
        self.history_layout.setAlignment(Qt.AlignTop)
        self.history_layout.setContentsMargins(0, 0, 0, 0)
        self.history_layout.setSpacing(6)
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        main_layout.addWidget(scroll)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(30)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background: rgba(28, 28, 30, 0.8);
                border-radius: 8px;
                border: none;
                text-align: center;
                color: #FFFFFF;
                font-size: 13px;
                font-weight: 500;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #34C759, stop:1 #28A745);
                border-radius: 8px;
            }
        """)
        progress_glow = QGraphicsDropShadowEffect()
        progress_glow.setBlurRadius(15)
        progress_glow.setColor(QColor(34, 197, 94, 100))
        progress_glow.setOffset(0, 2)
        self.progress_bar.setGraphicsEffect(progress_glow)
        main_layout.addWidget(self.progress_bar)

        self.progress_animation = QPropertyAnimation(self.progress_bar, b'value')
        self.progress_animation.setDuration(1000)
        self.progress_animation.setEasingCurve(QEasingCurve.InOutCubic)

        self.setLayout(main_layout)
        self.load_task_history()

    def load_task_history(self):
        self.clear_history_layout()
        history = []
        if os.path.exists(self.task_history_file):
            try:
                with open(self.task_history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
                print(f'Загружено из {self.task_history_file}: {history}')
            except json.JSONDecodeError as e:
                print(f'Ошибка: файл {self.task_history_file} поврежден: {e}')
                history = []
            except Exception as e:
                print(f'Ошибка чтения task_history.json: {e}')
                history = []

        current_month = datetime.now().strftime('%Y-%m')
        for entry in sorted(history, key=lambda x: x['date'], reverse=True):
            if entry['date'].startswith(current_month):
                date_obj = datetime.strptime(entry['date'], '%Y-%m-%d')
                formatted_date = date_obj.strftime('%d.%m.%Y')
                date_label = QLabel(f'{formatted_date}: {entry["tasks"]} тасков')
                date_label.setStyleSheet("""
                    font-size: 12px;
                    font-weight: 400;
                    color: #E0E0E0;
                    padding: 8px;
                    background: rgba(28, 28, 30, 0.8);
                    border-radius: 6px;
                """)
                date_label.setFixedHeight(35)
                glow = QGraphicsDropShadowEffect()
                glow.setBlurRadius(8)
                glow.setColor(QColor(0, 0, 0, 50))
                glow.setOffset(0, 1)
                date_label.setGraphicsEffect(glow)
                self.history_layout.addWidget(date_label)

        self.calculate_progress()

    def clear_history_layout(self):
        while self.history_layout.count():
            item = self.history_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def calculate_progress(self):
        history = []
        if os.path.exists(self.task_history_file):
            try:
                with open(self.task_history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            except json.JSONDecodeError as e:
                print(f'Ошибка: файл {self.task_history_file} поврежден: {e}')
                history = []
            except Exception as e:
                print(f'Ошибка чтения task_history.json: {e}')
                history = []

        current_month = datetime.now().strftime('%Y-%m')
        total_tasks = sum(entry['tasks'] for entry in history if entry['date'].startswith(current_month))
        progress_percent = (total_tasks / self.monthly_goal) * 100 if self.monthly_goal > 0 else 0
        remaining_tasks = max(0, self.monthly_goal - total_tasks)

        if progress_percent >= 100 and self.last_progress_percent < 100:
            if self.overlay is None or not self.overlay.isVisible():
                self.show_congratulation()

        self.last_progress_percent = progress_percent

        self.progress_animation.setStartValue(self.progress_bar.value())
        self.progress_animation.setEndValue(int(progress_percent))
        self.progress_animation.start()

        self.progress_bar.setFormat(
            f'{total_tasks} / {self.monthly_goal} ({progress_percent:.1f}%) • Осталось: {remaining_tasks}'
        )

    def show_congratulation(self):
        self.overlay = CongratulationOverlay(self)
        self.overlay.show_animation()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TaskPlanner()
    window.show()
    sys.exit(app.exec())