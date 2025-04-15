import sys
import os
import json
from PySide6.QtWidgets import QMessageBox

def resource_path(relative_path):
    """Получить абсолютный путь к ресурсу, работает для dev и для PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def load_region_tax_data():
    try:
        with open("data/region_tax_data.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        QMessageBox.critical(None, "Ошибка", "Файл region_tax_data.json не найден.")
        sys.exit()
    except json.JSONDecodeError:
        QMessageBox.critical(None, "Ошибка", "Ошибка в формате JSON-файла.")
        sys.exit()