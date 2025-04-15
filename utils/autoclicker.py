import cv2
import pyautogui
import numpy as np
import time
import threading
from PySide6.QtWidgets import QFileDialog

class AutoClicker:
    def __init__(self):
        self.running = False
        self.button_template = None
        self.switch = None

    def set_switch(self, switch):
        self.switch = switch

    def load_template(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "Выберите изображение кнопки", "",
                                                   "Image files (*.png *.jpg *.jpeg)")
        if file_path:
            self.button_template = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            if self.button_template is not None:
                if self.switch:
                    self.switch.update_style(True)
            else:
                self.button_template = None
                if self.switch:
                    self.switch.update_style(False)

    def click_button(self):
        while self.running:
            if self.button_template is None:
                if self.switch:
                    self.switch.update_style(False)
                self.running = False
                return
            screenshot = pyautogui.screenshot()
            screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
            if screenshot.shape[0] < self.button_template.shape[0] or screenshot.shape[1] < self.button_template.shape[
                1]:
                if self.switch:
                    self.switch.update_style(False)
                self.running = False
                return
            result = cv2.matchTemplate(screenshot, self.button_template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            if max_val > 0.8:
                x, y = max_loc
                pyautogui.click(x + self.button_template.shape[1] // 2, y + self.button_template.shape[0] // 2)
            time.sleep(1)

    def toggle(self, checked):
        self.running = checked
        if self.running:
            if self.button_template is None:
                self.switch.update_style(False)
                self.running = False
            else:
                self.switch.update_style(True)
                threading.Thread(target=self.click_button, daemon=True).start()
        else:
            self.switch.update_style(self.button_template is not None)