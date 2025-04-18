import sys
import json
import os
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QInputDialog, QDialog, QMessageBox,
    QLabel, QGraphicsDropShadowEffect, QScrollArea, QApplication
)
from PySide6.QtCore import Qt, QTimer, QPoint, QSize, QDateTime
from PySide6.QtGui import QPixmap, QIcon, QFont, QColor
import subprocess
from ui.patent_calculator import PatentCalculator
from ui.time_tracker import TimeTracker
from ui.task_planner import TaskPlanner
from ui.animated_label import AnimatedLabel
from ui.effects_overlay import EffectsOverlay
from ui.draggable_label import DraggableLabel
from ui.draggable_button_label import DraggableButtonLabel
from ui.switch import QSwitch
from utils.autoclicker import AutoClicker
from utils.key_press_thread import KeyPressThread
from utils.styles import MAIN_STYLE, BUTTON_STYLE, COUNTER_LABEL_STYLE, DATE_LABEL_STYLE, NOTE_PANEL_STYLE, CLOSE_BUTTON_STYLE

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
        # В скомпилированном виде сохраняем в папку с .exe
        base_path = os.path.dirname(sys.executable)
    else:
        # В PyCharm сохраняем в корне проекта
        base_path = os.path.abspath('.')
    data_dir = os.path.join(base_path, 'data')
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, filename)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('NPH')
        self.button_size = 40
        self.buttons_spacing = 1
        self.counter_size = 82
        self.notes_panel_width = 100
        self.setFixedSize(self.counter_size + (self.button_size + 2) * 3 + 37, 90)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.counter_file = data_path('counter.txt')
        self.notes_file = data_path('notes.json')
        self.notes_positions_file = data_path('notes_positions.json')
        self.task_history_file = data_path('task_history.json')
        self.counter = self._load_counter()
        self.daily_goal = 250
        self.notes = self._load_notes()
        self.notes_positions = self._load_positions()
        self.hotkeys = {
            'show_notes_1': 'space+1',
            'show_notes_2': 'space+2',
            'increment_counter': 'tab',
            'toggle_autoclicker': 'f10',
            'load_template': 'f9'
        }
        self.is_snipping = False
        self.notes_panel = None
        self.notes_layout = None
        self.notes_panel_position = None
        self.time_tracker_window = None
        self.patent_calculator_window = None
        self.task_planner_window = None
        self.autoclicker = AutoClicker()
        self._init_ui()
        self._init_key_thread()
        self._update_window_size()
        self.color_timer = QTimer(self)
        self.color_timer.timeout.connect(self._update_counter_color)
        self.color_timer.start(60000)

    def _load_counter(self):
        try:
            return int(open(self.counter_file, 'r', encoding='utf-8').read().strip())
        except (FileNotFoundError, ValueError):
            return 0

    def _save_counter(self):
        try:
            with open(self.counter_file, 'w', encoding='utf-8') as f:
                f.write(str(self.counter))
        except Exception as e:
            print(f'Ошибка сохранения counter.txt: {e}')

    def _load_notes(self):
        try:
            return json.load(open(self.notes_file, 'r', encoding='utf-8')) if os.path.exists(self.notes_file) else {}
        except Exception as e:
            print(f'Ошибка загрузки notes.json: {e}')
            return {}

    def _load_positions(self):
        try:
            if os.path.exists(self.notes_positions_file):
                with open(self.notes_positions_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f'Ошибка загрузки notes_positions.json: {e}')
        return {}

    def _save_positions(self):
        positions = {}
        for k, p in self.notes_positions.items():
            if k != 'notes_panel':
                if isinstance(p, list) and len(p) >= 2:
                    positions[k] = [p[0], p[1]]
                elif hasattr(p, 'x') and hasattr(p, 'y'):
                    positions[k] = [p.x(), p.y()]
        if self.notes_panel and self.notes_panel_position:
            positions['notes_panel'] = [
                self.notes_panel_position.x(),
                self.notes_panel_position.y(),
                self.notes_panel.width(),
                self.notes_panel.height()
            ]
        try:
            with open(self.notes_positions_file, 'w', encoding='utf-8') as f:
                json.dump(positions, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f'Ошибка сохранения notes_positions.json: {e}')

    def _save_task_history(self):
        """Сохраняет таски за текущий день в task_history.json"""
        today = datetime.now().strftime('%Y-%m-%d')
        task_data = {'date': today, 'tasks': self.counter}
        history = []
        if os.path.exists(self.task_history_file):
            try:
                with open(self.task_history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            except json.JSONDecodeError as e:
                print(f'Ошибка: файл {self.task_history_file} поврежден: {e}')
                history = []
        history = [entry for entry in history if entry['date'] != today]  # Удаляем старые данные за сегодня
        history.append(task_data)
        try:
            with open(self.task_history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=4)
            print(f'Сохранено в {self.task_history_file}: {task_data}')
        except Exception as e:
            print(f'Ошибка сохранения task_history.json: {e}')

    def _init_ui(self):
        self.setStyleSheet(MAIN_STYLE)
        self.main_layout = QHBoxLayout()
        self.main_layout.setSpacing(2)
        self.main_layout.setContentsMargins(2, 2, 2, 2)
        widget = QWidget()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)

        self.effects_overlay = EffectsOverlay(widget)
        self.effects_overlay.setGeometry(widget.rect())

        counter_container = QVBoxLayout()
        counter_container.setSpacing(0)
        counter_container.setContentsMargins(0, 0, 0, 0)
        counter_container.setAlignment(Qt.AlignCenter)

        self.counter_label = AnimatedLabel(str(self.counter), self, self.effects_overlay)
        self.counter_label.setFixedSize(self.counter_size, self.counter_size)
        self.counter_label.setAlignment(Qt.AlignCenter)
        self.counter_label.setStyleSheet(COUNTER_LABEL_STYLE)
        self.counter_label.mousePressEvent = self._handle_counter_click
        counter_container.addWidget(self.counter_label)

        self.effects_overlay.set_label(self.counter_label)

        counter_widget = QWidget()
        counter_widget.setLayout(counter_container)
        counter_widget.setFixedWidth(self.counter_size)

        self.main_layout.addSpacing(2)
        self.main_layout.addWidget(counter_widget, alignment=Qt.AlignCenter)

        self._update_glow_effect()

        buttons_container = QVBoxLayout()
        buttons_container.setSpacing(0)

        top_row = QHBoxLayout()
        top_row.setSpacing(0)
        self.buttons = {
            'T': QPushButton(),
            'Patent': QPushButton(),
            'Snip': QPushButton('✂️')
        }
        actions = {
            'T': self._handle_time_tracker_click,
            'Patent': self._launch_patent,
            'Snip': self._launch_snip
        }

        t_path = resource_path('resources/t.png')
        t_pixmap = QPixmap(t_path)
        if t_pixmap.isNull():
            print(f'Failed to load {t_path}. Make sure the file exists in the correct directory.')
            self.buttons['T'].setText('T')
        else:
            t_icon = QIcon(t_pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.buttons['T'].setIcon(t_icon)
            self.buttons['T'].setIconSize(QSize(24, 24))

        patent_path = resource_path('resources/patent.png')
        patent_pixmap = QPixmap(patent_path)
        if patent_pixmap.isNull():
            print(f'Failed to load {patent_path}. Make sure the file exists in the correct directory.')
            self.buttons['Patent'].setText('P')
        else:
            patent_icon = QIcon(patent_pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.buttons['Patent'].setIcon(patent_icon)
            self.buttons['Patent'].setIconSize(QSize(24, 24))

        for key in ['T', 'Patent', 'Snip']:
            btn = self.buttons[key]
            btn.setFixedSize(self.button_size, self.button_size)
            btn.setStyleSheet(BUTTON_STYLE)
            btn.clicked.connect(actions[key])
            top_row.addWidget(btn)
        buttons_container.addLayout(top_row)

        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(2)
        self.buttons.update({
            '1': QPushButton('1'),
            '2': QPushButton('2')
        })
        actions.update({
            '1': lambda: self._show_notes('1'),
            '2': lambda: self._show_notes('2')
        })
        for key in ['1', '2']:
            btn = self.buttons[key]
            btn.setFixedSize(self.button_size, self.button_size)
            btn.setStyleSheet(BUTTON_STYLE)
            btn.clicked.connect(actions[key])
            bottom_row.addWidget(btn)

        self.switch = QSwitch(self, self.autoclicker.toggle, self._update_switch_style)
        bottom_row.addWidget(self.switch)

        buttons_container.addLayout(bottom_row)

        self.main_layout.addLayout(buttons_container)

        self.autoclicker.set_switch(self.switch)

        self.current_date_label = QLabel(self._get_current_date())
        self.current_date_label.setAlignment(Qt.AlignCenter)
        self.current_date_label.setStyleSheet(DATE_LABEL_STYLE)
        self.current_date_label.setFixedWidth(self.counter_size)
        self.current_date_label.setFixedHeight(15)
        self.current_date_label.move(self.counter_label.x(), self.counter_label.y() - 0)
        self.current_date_label.setParent(self.counter_label)
        self.current_date_label.raise_()

        self.past_date_label = QLabel(self._get_past_date())
        self.past_date_label.setAlignment(Qt.AlignCenter)
        self.past_date_label.setStyleSheet(DATE_LABEL_STYLE)
        self.past_date_label.setFixedWidth(self.counter_size)
        self.past_date_label.setFixedHeight(15)
        self.past_date_label.move(self.counter_label.x(), self.counter_label.y() + self.counter_size - 15)
        self.past_date_label.setParent(self.counter_label)
        self.past_date_label.raise_()

        widget.resizeEvent = lambda event: self.effects_overlay.setGeometry(widget.rect())

    def closeEvent(self, event):
        """Обрабатывает закрытие окна, предлагая сохранить таски."""
        if self.counter > 0:
            reply = QMessageBox.question(
                self, 'Сохранить таски?',
                f'Вы выполнили {self.counter} тасков сегодня. Сохранить в историю?',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes
            )
            if reply == QMessageBox.Yes:
                self._save_task_history()
        super().closeEvent(event)

    def _get_current_date(self):
        return datetime.now().strftime('%d.%m.%Y')

    def _get_past_date(self):
        past_date = datetime.now() - relativedelta(days=90)
        return past_date.strftime('%d.%m.%Y')

    def _update_glow_effect(self):
        glow = QGraphicsDropShadowEffect()
        progress = min(self.counter / self.daily_goal, 1.0)
        if progress < 0.5:
            r = int(255 * (progress * 2))
            g = 255
            b = int(255 * (1 - progress * 2))
        else:
            r = 255
            g = int(255 * (1 - (progress - 0.5) * 2))
            b = 0
        glow.setColor(QColor(r, g, b))
        glow.setBlurRadius(10 + progress * 20)
        glow.setOffset(0, 0)
        if self.counter > 200:
            glow.setBlurRadius(glow.blurRadius() + 5)
            glow.setOffset(0, 2)
        self.counter_label.setGraphicsEffect(glow)

    def _update_switch_style(self):
        self.switch.update_style(self.autoclicker.button_template is not None)

    def _init_notes_panel(self):
        if self.notes_panel and self.notes_panel.isVisible():
            return
        self.notes_panel = QWidget(self)
        self.notes_panel.setStyleSheet(NOTE_PANEL_STYLE)
        main_window_width = self.width()
        self.notes_panel_width = main_window_width
        self.notes_panel.setMinimumSize(self.notes_panel_width, 200)
        screen = QApplication.primaryScreen().geometry()
        default_pos = QPoint(
            (screen.width() - self.notes_panel_width) // 2,
            (screen.height() - 200) // 2
        )
        saved_data = self.notes_positions.get('notes_panel',
                                              [default_pos.x(), default_pos.y(), self.notes_panel_width, 200])
        if len(saved_data) == 4 and (0 <= saved_data[0] <= screen.width() - saved_data[2] and
                                     0 <= saved_data[1] <= screen.height() - saved_data[3]):
            self.notes_panel_position = QPoint(saved_data[0], saved_data[1])
            self.notes_panel.resize(self.notes_panel_width, saved_data[3])
        else:
            self.notes_panel_position = default_pos
            self.notes_panel.resize(self.notes_panel_width, 200)
        self.notes_panel.move(self.notes_panel_position)
        self.notes_panel.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        layout = QVBoxLayout(self.notes_panel)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        clear_btn = QPushButton('Очистить все')
        clear_btn.setStyleSheet(BUTTON_STYLE)
        clear_btn.clicked.connect(self._clear_notes)
        layout.addWidget(clear_btn)
        scroll = QScrollArea()
        scroll.setStyleSheet('QScrollArea { border: none; }')
        scroll_widget = QWidget()
        self.notes_layout = QVBoxLayout(scroll_widget)
        self.notes_layout.setAlignment(Qt.AlignTop)
        self.notes_layout.setContentsMargins(0, 0, 0, 0)
        self.notes_layout.setSpacing(5)
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        self.notes_panel.closeEvent = self._on_notes_panel_close
        self.notes_panel.show()

    def _on_notes_panel_close(self, event):
        self.notes_panel_position = self.notes_panel.pos()
        self._save_positions()
        self.is_snipping = False
        event.accept()

    def _init_key_thread(self):
        self.key_thread = KeyPressThread(self.hotkeys, self)
        self.key_thread.show_notes.connect(self._show_notes)
        self.key_thread.increment_counter.connect(self._increment_counter)
        self.key_thread.toggle_autoclicker.connect(self._toggle_autoclicker)
        self.key_thread.load_template.connect(self.autoclicker.load_template)
        self.key_thread.start()

    def _toggle_autoclicker(self):
        self.switch.setChecked(not self.switch.isChecked())
        self.autoclicker.toggle(self.switch.isChecked())

    def _update_window_size(self):
        buttons_width = (self.button_size + 2) * 3 + 20
        new_width = self.counter_size + buttons_width
        self.setFixedSize(new_width, 90)
        if self.notes_panel and self.notes_panel.isVisible():
            self.notes_panel.move(self.notes_panel.pos())

    def _handle_time_tracker_click(self):
        """Обрабатывает клик на кнопку 'T', с Ctrl открывает TaskPlanner."""
        if QApplication.keyboardModifiers() & Qt.ControlModifier:
            self._launch_task_planner()
        else:
            self._launch_time_tracker()

    def _launch_time_tracker(self):
        if not self.time_tracker_window or not self.time_tracker_window.isVisible():
            self.time_tracker_window = TimeTracker()
            self.time_tracker_window.setWindowFlags(self.time_tracker_window.windowFlags() | Qt.WindowStaysOnTopHint)
            self.time_tracker_window.show()
        else:
            self.time_tracker_window.raise_()
            self.time_tracker_window.activateWindow()

    def _launch_snip(self):
        subprocess.Popen(['explorer.exe', 'ms-screenclip:'])
        self.is_snipping = True
        if not hasattr(self, '_clipboard_connected'):
            QApplication.clipboard().dataChanged.connect(self._update_from_clipboard)
            self._clipboard_connected = True

    def _launch_patent(self):
        if not self.patent_calculator_window or not self.patent_calculator_window.isVisible():
            self.patent_calculator_window = PatentCalculator()
            self.patent_calculator_window.setWindowFlags(
                self.patent_calculator_window.windowFlags() | Qt.WindowStaysOnTopHint)
            self.patent_calculator_window.show()
        else:
            self.patent_calculator_window.raise_()
            self.patent_calculator_window.activateWindow()

    def _launch_task_planner(self):
        if not self.task_planner_window or not self.task_planner_window.isVisible():
            self.task_planner_window = TaskPlanner()
            self.task_planner_window.setWindowFlags(
                self.task_planner_window.windowFlags() | Qt.WindowStaysOnTopHint)
            self.task_planner_window.show()
        else:
            self.task_planner_window.raise_()
            self.task_planner_window.activateWindow()

    def _update_from_clipboard(self):
        if not self.is_snipping:
            return
        text = QApplication.clipboard().text().strip()
        if text:
            self._add_note(self._process_text(text))

    def _add_note(self, text):
        if not self.notes_panel or not self.notes_panel.isVisible():
            self._init_notes_panel()
        note_widget = QWidget()
        note_layout = QHBoxLayout(note_widget)
        note_layout.setContentsMargins(0, 0, 0, 0)
        note_layout.setSpacing(5)
        label = DraggableLabel(text)
        label.setFixedWidth(self.notes_panel.width() - 40)
        close_btn = QPushButton('×')
        close_btn.setStyleSheet(CLOSE_BUTTON_STYLE)
        close_btn.clicked.connect(lambda: self._remove_note(note_widget))
        note_layout.addWidget(label)
        note_layout.addWidget(close_btn)
        self.notes_layout.addWidget(note_widget)

    def _remove_note(self, note_widget):
        self.notes_layout.removeWidget(note_widget)
        note_widget.deleteLater()

    def _clear_notes(self):
        while self.notes_layout.count():
            item = self.notes_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def _process_text(self, text):
        text = text.replace('№', '')
        text = re.sub(r'[.,]\s*', ' ', text)
        parts = text.split()
        result = []
        i = 0
        while i < len(parts):
            part = parts[i]
            part = part.replace('.', '').replace(',', '')
            if part.isdigit():
                number = part
                i += 1
                while i < len(parts) and parts[i].isdigit():
                    number += parts[i]
                    i += 1
                result.append(number)
            else:
                result.append(part)
                i += 1
        processed = ' '.join(result).upper()
        return processed

    def _show_notes(self, category):
        if category not in self.notes:
            QMessageBox.warning(self, 'Ошибка', 'Категория заметок не найдена.')
            return
        dialog = QDialog(self)
        dialog.setWindowTitle(f'Заметки: {category}')
        dialog.setStyleSheet('background-color: #2C2C2E; border: none;')
        position = self.notes_positions.get(category, [100, 100])
        if isinstance(position, list) and len(position) >= 2:
            dialog.move(QPoint(position[0], position[1]))
        else:
            dialog.move(QPoint(100, 100))
        dialog.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        notes_widget = QWidget()
        notes_layout = QVBoxLayout(notes_widget)
        notes_layout.setContentsMargins(0, 0, 0, 0)
        notes_layout.setSpacing(5)
        for note_title, note_value in self.notes[category].items():
            label = DraggableButtonLabel(note_title, note_value)
            label.setFixedWidth(390)
            label.dragFinished.connect(dialog.accept)
            notes_layout.addWidget(label)
        layout.addWidget(notes_widget)
        note_count = len(self.notes[category])
        dialog.setFixedSize(405, note_count * 38)
        dialog.exec()
        self.notes_positions[category] = [dialog.pos().x(), dialog.pos().y()]
        self._save_positions()

    def _handle_counter_click(self, event):
        if event.modifiers() & Qt.ControlModifier:
            self._manual_input()
        elif event.button() == Qt.LeftButton:
            self._increment_counter()
        elif event.button() == Qt.RightButton:
            self._decrement_counter()

    def _increment_counter(self):
        self.counter += 1
        self.counter_label.set_value(self.counter)
        self._save_counter()
        self._update_glow_effect()
        self.counter_label.animate()
        self._update_window_size()

    def _decrement_counter(self):
        if self.counter > 0:
            self.counter -= 1
        self.counter_label.set_value(self.counter)
        self._save_counter()
        self._update_glow_effect()
        self._update_window_size()

    def _manual_input(self):
        dialog = QInputDialog(self)
        dialog.setWindowTitle('Ввод значения')
        dialog.setLabelText('Новое значение:')
        dialog.setInputMode(QInputDialog.IntInput)
        dialog.setIntMinimum(0)
        dialog.setIntMaximum(99999)
        dialog.setIntValue(self.counter)
        if dialog.exec() == QDialog.Accepted:
            self.counter = dialog.intValue()
            self.counter_label.set_value(self.counter)
            self._save_counter()
            self._update_glow_effect()
            self._update_window_size()

    def _update_counter_color(self):
        self.counter_label.update_color()
        self.counter_label.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())