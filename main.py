import sys
import os
from PySide6.QtWidgets import QApplication, QSplashScreen
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QTimer

from ui.main_window import MainWindow

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def main():
    app = QApplication(sys.argv)


    splash_path = resource_path("resources/splash.png")
    splash_pix = QPixmap(splash_path)

    if splash_pix.isNull():
        with open("error.log", "w") as f:
            f.write(f"Ошибка: не удалось загрузить splash.png по пути {splash_path}")
        sys.exit(1)

    splash_pix = splash_pix.scaled(500, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setWindowFlag(Qt.FramelessWindowHint)
    splash.show()
    app.processEvents()

    window = MainWindow()
    window.show()
    QTimer.singleShot(1000, splash.close)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()