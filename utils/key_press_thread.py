from PySide6.QtCore import QThread, Signal, QDateTime
import keyboard

class KeyPressThread(QThread):
    show_notes = Signal(str)
    increment_counter = Signal()
    toggle_autoclicker = Signal()
    load_template = Signal()

    def __init__(self, hotkeys, parent_window):
        super().__init__()
        self.hotkeys = hotkeys
        self.running = True
        self.last_tab_press = 0
        self.tab_cooldown = 500
        self.parent_window = parent_window

    def run(self):
        try:
            self._register_hotkeys()
            while self.running:
                self.sleep(1)
        except Exception as e:
            print(f"Ошибка в потоке горячих клавиш: {e}")

    def _register_hotkeys(self):
        keyboard.unhook_all()
        for action, hotkey in self.hotkeys.items():
            if action.startswith("show_notes_"):
                keyboard.add_hotkey(hotkey, lambda cat=action[-1]: self.show_notes.emit(cat))
            elif action == "increment_counter":
                keyboard.add_hotkey(hotkey, self._handle_tab_press)
            elif action == "toggle_autoclicker":
                keyboard.add_hotkey(hotkey, self.toggle_autoclicker.emit)
            elif action == "load_template":
                keyboard.add_hotkey(hotkey, self.load_template.emit)

    def _handle_tab_press(self):
        current_time = QDateTime.currentMSecsSinceEpoch()
        if current_time - self.last_tab_press > self.tab_cooldown:
            self.increment_counter.emit()
            self.last_tab_press = current_time

    def stop(self):
        self.running = False
        keyboard.unhook_all()
        self.quit()