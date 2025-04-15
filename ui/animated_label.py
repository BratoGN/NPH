from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, QPropertyAnimation, QSequentialAnimationGroup, QEasingCurve, QParallelAnimationGroup, Property, QUrl, QRectF, QPointF, QAbstractAnimation
from PySide6.QtGui import QPainter, QTransform, QFont, QPen, QColor, QPainterPath, QRadialGradient
from PySide6.QtMultimedia import QSoundEffect
from datetime import datetime
from dateutil.relativedelta import relativedelta
import math
from utils.helpers import resource_path

class AnimatedLabel(QLabel):
    def __init__(self, text, parent=None, effects_overlay=None):
        super().__init__(text, parent)
        self._rotation = 0
        self._scale = 1.0
        self._glow = 0.0
        self._offset_x = 0.0
        self._offset_y = 0.0
        self._heat = 0.0
        self._darken = 0.0
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAlignment(Qt.AlignCenter)
        self._value = 0
        self.effects_overlay = effects_overlay
        self.sound = QSoundEffect()
        self.sound.setSource(QUrl.fromLocalFile(resource_path("resources/sound.wav")))
        self.sound.setVolume(0.5)
        # Параметры смены
        self.shift_start = datetime.strptime("09:00", "%H:%M")
        self.shift_end = datetime.strptime("21:00", "%H:%M")
        self.break_duration = 2 * 60  # 2 часа в минутах
        self.daily_goal = 250
        self.work_hours = (self.shift_end - self.shift_start).seconds / 3600 - self.break_duration / 60
        self.tasks_per_hour = self.daily_goal / self.work_hours
        self.current_color = QColor(120, 120, 255)  # Начальный холодный цвет (заметный синий)

    def set_value(self, value):
        self._value = value
        self.setText(str(value))
        if self.effects_overlay:
            self.effects_overlay.set_value(value)
        self.update_color()
        self.update()

    def update_color(self):
        """Рассчитываем цвет на основе времени и количества тасков."""
        now = datetime.now()
        shift_start_today = now.replace(
            hour=self.shift_start.hour, minute=self.shift_start.minute, second=0, microsecond=0
        )
        shift_end_today = now.replace(
            hour=self.shift_end.hour, minute=self.shift_end.minute, second=0, microsecond=0
        )

        # Проверяем, идет ли смена
        if not (shift_start_today <= now <= shift_end_today):
            self.current_color = QColor(120, 120, 255)  # Холодный цвет вне смены
            return

        # Время с начала смены в часах
        elapsed_hours = (now - shift_start_today).total_seconds() / 3600
        # Пропорционально учитываем перерывы (2 часа за 12 часов смены)
        total_shift_hours = (self.shift_end - self.shift_start).seconds / 3600  # 12 часов
        break_proportion = elapsed_hours / total_shift_hours
        effective_break_hours = self.break_duration / 60 * break_proportion
        effective_elapsed_hours = max(0, elapsed_hours - effective_break_hours)

        # Ожидаемое количество тасков
        expected_tasks = effective_elapsed_hours * self.tasks_per_hour

        # Прогресс относительно нормы
        if expected_tasks > 0:
            progress = self._value / expected_tasks
        else:
            progress = 1.0 if self._value > 0 else 0.0

        # Плавное изменение цвета
        if progress < 0.8:
            # Холодный цвет: яркий синий с фиолетовым оттенком
            r = int(120 + (120 - 120) * (progress / 0.8))
            g = int(120 + (140 - 120) * (progress / 0.8))
            b = int(255 - (255 - 200) * (progress / 0.8))
        elif progress < 1.0:
            # Переход к огненному: от синего к желтому
            t = (progress - 0.8) / 0.2
            r = int(120 + (255 - 120) * t)
            g = int(140 + (255 - 140) * t)
            b = int(200 - (200 - 0) * t)
        elif progress < 1.5:
            # Огонь поддержки: от желтого к оранжево-красному
            t = (progress - 1.0) / 0.5
            r = 255
            g = int(255 - (255 - 165) * t)
            b = 0
        else:
            # Супер-прогресс: от оранжево-красного к ярко-красному (огнище)
            t = min((progress - 1.5) / 0.5, 1.0)
            r = 255
            g = int(165 - (165 - 69) * t)
            b = int(58 * t)  # Исправлено: от 0 до 58
            print(f"Progress: {progress}, t: {t}, Color: ({r}, {g}, {b})")  # Для отладки

        self.current_color = QColor(r, g, b)
        self.current_color.setAlpha(255)  # Гарантируем непрозрачность

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setOpacity(self.windowOpacity())

        # Трансформация для текста
        center = self.rect().center()
        transform = QTransform()
        transform.translate(center.x() + self._offset_x, center.y() + self._offset_y)
        transform.rotate(self._rotation)
        transform.scale(self._scale, self._scale)
        transform.translate(-center.x(), -center.y())
        painter.setTransform(transform)

        # Цвет текста
        painter.setFont(QFont("SF Pro Display", 25, QFont.Bold))

        # Свечение
        glow_color = QColor(self.current_color)
        glow_color.setAlphaF(self._glow)
        for radius in range(4, 20, 4):
            painter.setPen(QPen(glow_color, radius))
            painter.drawText(self.rect(), Qt.AlignCenter, self.text())

        # Убедимся, что текст непрозрачный
        text_color = QColor(self.current_color)
        text_color.setAlpha(255)  # Принудительная непрозрачность
        painter.setPen(QPen(text_color, 1.5))
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())

        # Сбрасываем трансформацию для искр
        painter.resetTransform()

        # Рисуем искры внутри области счетчика
        if self.effects_overlay:
            global_rect = self.mapTo(self.window().centralWidget(), self.rect().topLeft())
            counter_rect = QRectF(global_rect.x(), global_rect.y(), self.rect().width(), self.rect().height())
            self.effects_overlay.set_counter_rect(counter_rect)

            for spark in self.effects_overlay.sparks:
                if counter_rect.contains(QPointF(spark.x, spark.y)):
                    local_x = spark.x - global_rect.x()
                    local_y = spark.y - global_rect.y()
                    c = QColor(self.current_color)
                    alpha = (spark.life / spark.max_life) * (0.8 + 0.2 * math.sin(spark.phase))
                    c.setAlphaF(alpha)

                    if spark.smoke and self._value >= 50:
                        smoke_color = QColor(80, 80, 80, int(spark.smoke_alpha * spark.life * 255))
                        gradient = QRadialGradient(local_x, local_y, spark.size * 3)
                        gradient.setColorAt(0, smoke_color)
                        gradient.setColorAt(1, QColor(0, 0, 0, 0))
                        painter.setPen(Qt.NoPen)
                        painter.setBrush(gradient)
                        painter.drawEllipse(QPointF(local_x, local_y), spark.size * 3, spark.size * 3)

                    painter.setPen(QPen(c, spark.size / 2))
                    path = QPainterPath()
                    rays = 6 if spark.value >= 50 else 4
                    for i in range(rays):
                        angle = i * (360 / rays)
                        length = spark.size * (1.5 if i % 2 == 0 else 0.8)
                        path.moveTo(local_x, local_y)
                        path.lineTo(local_x + length * math.cos(math.radians(angle)),
                                    local_y + length * math.sin(math.radians(angle)))
                    painter.drawPath(path)

    def animate(self):
        if self.effects_overlay:
            center = self.mapTo(self.window().centralWidget(), self.rect().center())
            self.effects_overlay.set_center(QPointF(center.x(), center.y()))
            self.effects_overlay.emit_sparks()
            self.effects_overlay.emit_flames()

        if self.sound.isLoaded():
            self.sound.play()

        anim_group = QSequentialAnimationGroup(self)

        spin_anim = QPropertyAnimation(self, b"rotation")
        spin_anim.setDuration(600)
        spin_anim.setStartValue(0)
        spin_anim.setEndValue(720)
        spin_anim.setEasingCurve(QEasingCurve.OutInQuad)
        anim_group.addAnimation(spin_anim)

        explosion_group = QParallelAnimationGroup()
        scale_anim = QPropertyAnimation(self, b"scale")
        scale_anim.setDuration(300)
        scale_anim.setStartValue(1.0)
        scale_anim.setEndValue(1.5)
        scale_anim.setEasingCurve(QEasingCurve.OutQuad)
        explosion_group.addAnimation(scale_anim)

        fade_anim = QPropertyAnimation(self, b"windowOpacity")
        fade_anim.setDuration(300)
        fade_anim.setStartValue(1.0)
        fade_anim.setEndValue(0.0)
        fade_anim.setEasingCurve(QEasingCurve.OutQuad)
        explosion_group.addAnimation(fade_anim)

        anim_group.addAnimation(explosion_group)

        reset_group = QParallelAnimationGroup()
        reset_scale = QPropertyAnimation(self, b"scale")
        reset_scale.setDuration(300)
        reset_scale.setStartValue(1.5)
        reset_scale.setEndValue(1.0)
        reset_scale.setEasingCurve(QEasingCurve.InQuad)
        reset_group.addAnimation(reset_scale)

        reset_fade = QPropertyAnimation(self, b"windowOpacity")
        reset_fade.setDuration(300)
        reset_fade.setStartValue(0.0)
        reset_fade.setEndValue(1.0)
        reset_fade.setEasingCurve(QEasingCurve.InQuad)
        reset_group.addAnimation(reset_fade)

        reset_rotation = QPropertyAnimation(self, b"rotation")
        reset_rotation.setDuration(0)
        reset_rotation.setStartValue(0)
        reset_rotation.setEndValue(0)
        reset_group.addAnimation(reset_rotation)

        anim_group.addAnimation(reset_group)
        anim_group.start(QAbstractAnimation.DeleteWhenStopped)

    def get_rotation(self): return self._rotation
    def set_rotation(self, value): self._rotation = value; self.update()

    def get_scale(self): return self._scale
    def set_scale(self, value): self._scale = value; self.update()

    def get_glow(self): return self._glow
    def set_glow(self, value): self._glow = value; self.update()

    def get_offset_x(self): return self._offset_x
    def set_offset_x(self, value): self._offset_x = value; self.update()

    def get_offset_y(self): return self._offset_y
    def set_offset_y(self, value): self._offset_y = value; self.update()

    def get_heat(self): return self._heat
    def set_heat(self, value): self._heat = value; self.update()

    def get_darken(self): return self._darken
    def set_darken(self, value): self._darken = value; self.update()

    rotation = Property(float, get_rotation, set_rotation)
    scale = Property(float, get_scale, set_scale)
    glow = Property(float, get_glow, set_glow)
    offset_x = Property(float, get_offset_x, set_offset_x)
    offset_y = Property(float, get_offset_y, set_offset_y)
    heat = Property(float, get_heat, set_heat)
    darken = Property(float, get_darken, set_darken)