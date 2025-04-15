import sys
from PySide6.QtWidgets import QApplication, QSplashScreen
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QTimer

from ui.main_window import MainWindow  # Подстрой под свою структуру

def main():
    app = QApplication(sys.argv)

    # Загрузка и показ заставки
    splash_pix = QPixmap("resources/splash.png").scaled(500, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setWindowFlag(Qt.FramelessWindowHint)  # без рамки
    splash.show()
    app.processEvents()

    # Загружаем основное окно
    window = MainWindow()

    # Показываем окно и убираем заставку через 1 секунду
    window.show()
    QTimer.singleShot(10, splash.close)  # или больше времени, если нужно

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
