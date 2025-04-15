from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QHBoxLayout, QApplication
from PySide6.QtCore import Qt
from datetime import datetime
from utils.styles import TIME_TRACKER_STYLE, TIME_TRACKER_INPUT_STYLE

class TimeTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("NitroTime")
        self.setStyleSheet(TIME_TRACKER_STYLE)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        time_layout = QFormLayout()
        time_layout.setSpacing(10)

        self.start_time_edit = self.create_time_edit("Начало с:", "09:00")
        self.end_time_edit = self.create_time_edit("Конец в:", "21:00")

        time_layout.addRow(self.start_time_edit[0], self.start_time_edit[1])
        time_layout.addRow(self.end_time_edit[0], self.end_time_edit[1])

        self.time_vars = []
        labels = [
            "Время перерывов", "Чтение инструкций", "Инф. встреча",
            "Прохождение тестирований и курсов", "Актуализация (Nitro)", "Ожидание", "Нет заданий"
        ]

        for label_text in labels:
            time_entry = self.create_time_entry(label_text)
            self.time_vars.append(time_entry)
            time_layout.addRow(time_entry[0])

        main_layout.addLayout(time_layout)

        self.total_time_label = QLabel("Общее Время: 0 часов и 0 минут (нажми, чтобы скопировать)")
        self.total_time_label.setStyleSheet("""
            margin-top: 20px;
            padding: 10px;
            background-color: rgba(44, 44, 46, 0.9);
            color: #FFFFFF;
            border-radius: 8px;
            font-family: 'SF Pro Text', 'Helvetica Neue', sans-serif;
        """)
        self.total_time_label.setAlignment(Qt.AlignCenter)
        self.total_time_label.mousePressEvent = self.copy_to_clipboard

        main_layout.addWidget(self.total_time_label)

        self.setLayout(main_layout)

        self.start_time_edit[1].textChanged.connect(self.calculate_total_time)
        self.end_time_edit[1].textChanged.connect(self.calculate_total_time)
        self.calculate_total_time()

    def create_time_edit(self, label_text, default_value):
        label = QLabel(label_text)
        label.setStyleSheet(
            "font-weight: 600; color: #E0E0E0; font-family: 'SF Pro Text', 'Helvetica Neue', sans-serif;")
        line_edit = QLineEdit(default_value)
        line_edit.setFixedWidth(80)
        line_edit.setStyleSheet(TIME_TRACKER_INPUT_STYLE)
        line_edit.textChanged.connect(lambda: self.on_time_entry(line_edit))
        return label, line_edit

    def create_time_entry(self, label_text):
        layout = QHBoxLayout()
        layout.setSpacing(10)

        label = QLabel(label_text)
        label.setFixedWidth(250)
        label.setStyleSheet("color: #E0E0E0; font-family: 'SF Pro Text', 'Helvetica Neue', sans-serif;")
        layout.addWidget(label)

        hour_var = QLineEdit()
        hour_var.setFixedWidth(40)
        hour_var.setStyleSheet(TIME_TRACKER_INPUT_STYLE)
        hour_var.textChanged.connect(self.calculate_total_time)
        layout.addWidget(hour_var)

        hour_label = QLabel("ч")
        hour_label.setStyleSheet("color: #8E8E93;")
        layout.addWidget(hour_label)

        minute_var = QLineEdit()
        minute_var.setFixedWidth(40)
        minute_var.setStyleSheet(TIME_TRACKER_INPUT_STYLE)
        minute_var.textChanged.connect(self.calculate_total_time)
        layout.addWidget(minute_var)

        minute_label = QLabel("мин")
        minute_label.setStyleSheet("color: #8E8E93;")
        layout.addWidget(minute_label)

        return layout, hour_var, minute_var

    def on_time_entry(self, line_edit):
        text = line_edit.text().replace(":", "")
        if len(text) == 4:
            line_edit.setText(text[:2] + ":" + text[2:])

    def calculate_total_time(self):
        start_time = self.start_time_edit[1].text()
        end_time = self.end_time_edit[1].text()
        try:
            start = datetime.strptime(start_time, "%H:%M")
            end = datetime.strptime(end_time, "%H:%M")
            total_minutes = int((end - start).total_seconds() // 60)
        except ValueError:
            total_minutes = 0

        entered_minutes = 0
        nitro_entry = None

        for layout, hours, minutes in self.time_vars:
            label = layout.itemAt(0).widget().text()
            if label == "Актуализация (Nitro)":
                nitro_entry = (hours, minutes)
            else:
                try:
                    hours_value = int(hours.text() or 0)
                    minutes_value = int(minutes.text() or 0)
                    if 0 <= minutes_value < 60:
                        entered_minutes += hours_value * 60 + minutes_value
                    else:
                        minutes.setText("0")
                except ValueError:
                    pass

        if nitro_entry:
            nitro_hours, nitro_minutes = nitro_entry
            remaining_minutes = total_minutes - entered_minutes
            nitro_hours.setText(str(remaining_minutes // 60))
            nitro_minutes.setText(str(remaining_minutes % 60))

        total_hours = total_minutes // 60
        remaining_minutes = total_minutes % 60
        self.total_time_label.setText(f"Общее Время: {total_hours} часов и {remaining_minutes} минут")

    def copy_to_clipboard(self, event):
        clipboard = QApplication.clipboard()
        time_info = f"Время начала: {self.start_time_edit[1].text()}\n"
        labels = [
            "Время перерывов", "Чтение инструкций", "Инф. встреча",
            "Прохождение тестирований и курсов", "Актуализация (Nitro)", "Ожидание", "Нет заданий"
        ]
        for (layout, hours, minutes), label in zip(self.time_vars, labels):
            hours_text = hours.text().strip() or "0"
            minutes_text = minutes.text().strip() or "0"
            if hours_text != "0" or minutes_text != "0":
                time_info += f"{label}: {hours_text} часов {minutes_text} минут\n"
        time_info += f"Время завершения: {self.end_time_edit[1].text()}"
        clipboard.setText(time_info)
        self.total_time_label.setText("Скопировано в буфер обмена!")