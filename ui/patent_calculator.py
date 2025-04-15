from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QComboBox, QPushButton,
    QCalendarWidget, QHBoxLayout, QMessageBox
)
from PySide6.QtCore import Qt, QRect
from datetime import datetime
from dateutil.relativedelta import relativedelta
from utils.styles import PATENT_CALCULATOR_STYLE, CALENDAR_STYLE
from utils.helpers import load_region_tax_data

class PatentCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.region_tax_data = load_region_tax_data()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Patent Calculator")
        self.setFixedSize(410, 400)
        self.setStyleSheet(PATENT_CALCULATOR_STYLE)

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        header_label = QLabel("ФЕДЕРАЛЬНАЯ МИГРАЦИОННАЯ СЛУЖБА")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #5a2e3c; margin-bottom: 10px;")
        layout.insertWidget(0, header_label)

        form_layout = QFormLayout()
        form_layout.setSpacing(6)
        form_layout.setVerticalSpacing(10)

        self.issue_date_label = QLabel("Дата выдачи")
        self.issue_date_input = QLineEdit()
        self.issue_date_input.setPlaceholderText("дд.мм.гггг")
        self.issue_date_input.textChanged.connect(self.format_date_input)
        issue_date_button = QPushButton("📅")
        issue_date_button.setProperty("calendar", True)
        issue_date_button.setFixedSize(36, 36)
        issue_date_button.clicked.connect(lambda: self.show_calendar(self.issue_date_input))
        issue_date_layout = QHBoxLayout()
        issue_date_layout.addWidget(self.issue_date_input)
        issue_date_layout.addWidget(issue_date_button)
        form_layout.addRow(self.issue_date_label, issue_date_layout)

        self.region_category_label = QLabel("Категория региона")
        self.region_category_input = QComboBox()
        self.region_category_input.addItems(["Город", "Республика", "Край", "Область", "Автономный округ"])
        self.region_category_input.currentTextChanged.connect(self.update_region_input)
        form_layout.addRow(self.region_category_label, self.region_category_input)

        self.region_label = QLabel("Регион")
        self.region_input = QComboBox()
        form_layout.addRow(self.region_label, self.region_input)

        self.payment_date_label = QLabel("Дата оплаты")
        self.payment_date_input = QLineEdit()
        self.payment_date_input.setPlaceholderText("дд.мм.гггг")
        self.payment_date_input.textChanged.connect(self.format_date_input)
        self.payment_date_input.textChanged.connect(self.on_payment_date_change)
        payment_date_button = QPushButton("📅")
        payment_date_button.setProperty("calendar", True)
        payment_date_button.setFixedSize(36, 36)
        payment_date_button.clicked.connect(lambda: self.show_calendar(self.payment_date_input))
        payment_date_layout = QHBoxLayout()
        payment_date_layout.addWidget(self.payment_date_input)
        payment_date_layout.addWidget(payment_date_button)
        form_layout.addRow(self.payment_date_label, payment_date_layout)

        self.payment_amount_label = QLabel("Сумма платежа")
        self.payment_amount_input = QLineEdit()
        self.payment_amount_input.setPlaceholderText("Введите сумму в рублях")
        form_layout.addRow(self.payment_amount_label, self.payment_amount_input)

        layout.addLayout(form_layout)

        self.cost_label = QLabel("")
        self.cost_label.setStyleSheet(
            "color: #8E8E93; font-size: 12px; font-family: 'SF Pro Text', 'Helvetica Neue', sans-serif;")
        layout.addWidget(self.cost_label)

        layout.addStretch()

        self.calculate_button = QPushButton("Рассчитать")
        self.calculate_button.clicked.connect(self.calculate_patent_end_date)
        layout.addWidget(self.calculate_button)

        self.result_label = QLabel("")
        self.result_label.setStyleSheet(
            "font-size: 15px; font-weight: 600; color: #FFFFFF; font-family: 'SF Pro Display', 'Helvetica Neue', sans-serif;")
        self.result_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.result_label)

        self.setLayout(layout)
        self.update_region_input()

    def format_date_input(self):
        sender = self.sender()
        text = sender.text().replace('.', '')
        if len(text) > 8:
            text = text[:8]
        formatted_text = ""
        for i, char in enumerate(text):
            if i == 2 or i == 4:
                formatted_text += '.'
            formatted_text += char
        sender.setText(formatted_text)
        sender.setCursorPosition(len(formatted_text))

    def show_calendar(self, date_input):
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendar.setStyleSheet(CALENDAR_STYLE)
        self.calendar.setFixedSize(280, 220)
        self.calendar.clicked.connect(lambda date: self.set_date_from_calendar(date, date_input))
        self.calendar_window = QWidget()
        self.calendar_window.setWindowModality(Qt.ApplicationModal)
        self.calendar_window.setWindowFlags(self.calendar_window.windowFlags() | Qt.WindowStaysOnTopHint)
        calendar_layout = QVBoxLayout()
        calendar_layout.addWidget(self.calendar)
        self.calendar_window.setLayout(calendar_layout)
        self.calendar_window.setWindowTitle("Выберите дату")
        self.calendar_window.setStyleSheet("background-color: #2C2C2E; border-radius: 10px;")
        self.calendar_window.setGeometry(
            QRect(self.geometry().center().x() - 140, self.geometry().center().y() - 110, 280, 220))
        self.calendar_window.show()

    def set_date_from_calendar(self, date, date_input):
        formatted_date = date.toString("dd.MM.yyyy")
        date_input.setText(formatted_date)
        self.calendar_window.close()
        self.update_cost_label()

    def on_payment_date_change(self):
        if self.payment_date_input.text() and self.region_input.currentText():
            self.update_cost_label()

    def update_cost_label(self):
        payment_year = self.get_year_from_date(self.payment_date_input.text())
        category = self.region_category_input.currentText()
        region = self.region_input.currentText()
        if payment_year in self.region_tax_data and category in self.region_tax_data[payment_year] and region in \
                self.region_tax_data[payment_year][category]:
            self.cost_label.setText(f"Стоимость патента: {self.region_tax_data[payment_year][category][region]} ₽")
        else:
            self.cost_label.setText("Выберите регион и дату оплаты")
        self.cost_label.setVisible(True)

    def get_year_from_date(self, date_str):
        try:
            date_obj = datetime.strptime(date_str, "%d.%m.%Y")
            return str(date_obj.year)
        except ValueError:
            return "2023"

    def calculate_patent_end_date(self):
        try:
            issue_date = self.issue_date_input.text()
            payment_date = self.payment_date_input.text()
            payment_amount = self.payment_amount_input.text()
            if not issue_date or not payment_date or not payment_amount:
                raise ValueError("Заполните все поля")
            payment_amount = int(payment_amount)
            if payment_amount <= 0:
                raise ValueError("Сумма платежа должна быть больше 0")
            end_date = self.calculate_end_date(issue_date, payment_date, payment_amount)
            self.result_label.setText(f"Действует до {end_date}")
        except ValueError as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def calculate_end_date(self, issue_date_str, payment_date_str, payment_amount):
        issue_date = datetime.strptime(issue_date_str, "%d.%m.%Y")
        payment_date = datetime.strptime(payment_date_str, "%d.%m.%Y")
        year = self.get_year_from_date(payment_date_str)
        category = self.region_category_input.currentText()
        region = self.region_input.currentText()
        monthly_cost = self.region_tax_data.get(year, {}).get(category, {}).get(region, 3000)
        if payment_amount % monthly_cost != 0:
            raise ValueError("Сумма должна быть кратна стоимости патента")
        months_paid = payment_amount // monthly_cost
        start_date = issue_date if payment_date <= issue_date else payment_date.replace(day=issue_date.day)
        if start_date < payment_date:
            start_date += relativedelta(months=1)
        end_date = start_date + relativedelta(months=months_paid)
        self.result_label.setStyleSheet("font-size: 15px; font-weight: 600; color: " + (
            "#FF3B30" if end_date > issue_date + relativedelta(
                years=1) else "#FFFFFF") + "; font-family: 'SF Pro Display', 'Helvetica Neue', sans-serif;")
        return end_date.strftime("%d.%m.%Y")

    def update_region_input(self):
        self.region_input.clear()
        category = self.region_category_input.currentText()
        payment_year = self.get_year_from_date(self.payment_date_input.text())
        if payment_year in self.region_tax_data and category in self.region_tax_data[payment_year]:
            self.region_input.addItems(sorted(self.region_tax_data[payment_year][category].keys()))