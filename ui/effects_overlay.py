from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, QPointF, QRectF
from PySide6.QtGui import QPainter, QPen, QPainterPath, QRadialGradient, QColor
import random
import math

class Spark:
    def __init__(self, center, value, label_color):
        self.x = center.x()
        self.y = center.y()
        self.value = value
        angle = random.uniform(0, 360)
        speed = self.get_speed()
        self.vx = speed * math.cos(math.radians(angle))
        self.vy = speed * math.sin(math.radians(angle))
        self.life = random.uniform(0.5, 1.0)
        self.max_life = self.life
        self.size = self.get_size()
        self.color = label_color  # Используем цвет из AnimatedLabel
        self.spin = random.uniform(-0.6, 0.6)
        self.smoke = value >= 50
        self.smoke_alpha = random.uniform(0.15, 0.3)
        self.phase = random.uniform(0, 2 * math.pi)

    def get_speed(self):
        t = min(self.value / 1000, 1.0)
        return random.uniform(2, 6 + 10 * t)

    def get_size(self):
        t = min(self.value / 1000, 1.0)
        return random.uniform(0.5, 2 + 8 * t)

    def update(self):
        self.vy += 0.15
        self.vx += self.spin
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.93
        self.vy *= 0.93
        self.life -= 0.025
        self.phase += 0.2
        return self.life > 0

class Flame:
    def __init__(self, center):
        self.x = center.x() + random.uniform(-30, 30)
        self.y = center.y() + random.uniform(-30, 30)
        self.size = random.uniform(8, 14)
        self.life = 1.0
        self.phase = random.uniform(0, 2 * math.pi)

    def update(self):
        self.life -= 0.015
        self.size += 0.4 * math.sin(self.phase)
        self.phase += 0.2
        return self.life > 0

class EffectsOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.sparks = []
        self.flames = []
        self._value = 0
        self.center = QPointF(0, 0)
        self.counter_rect = QRectF(0, 0, 0, 0)
        self.spark_timer = QTimer(self)
        self.spark_timer.timeout.connect(self.update_sparks)
        self.spark_timer.start(16)
        self.label = None  # Ссылка на AnimatedLabel

    def set_label(self, label):
        self.label = label

    def set_value(self, value):
        self._value = value
        self.update()

    def set_center(self, center):
        self.center = center
        self.update()

    def set_counter_rect(self, rect):
        self.counter_rect = rect
        self.update()

    def update_sparks(self):
        self.sparks = [s for s in self.sparks if s.update()]
        self.flames = [f for f in self.flames if f.update()]
        self.update()

    def emit_sparks(self):
        count = 20 + int(self._value / 10) * 3
        label_color = self.label.current_color if self.label else QColor(255, 255, 255)
        for _ in range(count):
            self.sparks.append(Spark(self.center, self._value, label_color))

    def emit_flames(self):
        if self._value >= 50:
            count = 4 + int(self._value / 100)
            for _ in range(count):
                self.flames.append(Flame(self.center))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        for spark in self.sparks:
            if not self.counter_rect.contains(QPointF(spark.x, spark.y)):
                c = QColor(spark.color)
                alpha = (spark.life / spark.max_life) * (0.8 + 0.2 * math.sin(spark.phase))
                c.setAlphaF(alpha)

                if spark.smoke and self._value >= 50:
                    smoke_color = QColor(80, 80, 80, int(spark.smoke_alpha * spark.life * 255))
                    gradient = QRadialGradient(spark.x, spark.y, spark.size * 3)
                    gradient.setColorAt(0, smoke_color)
                    gradient.setColorAt(1, QColor(0, 0, 0, 0))
                    painter.setPen(Qt.NoPen)
                    painter.setBrush(gradient)
                    painter.drawEllipse(QPointF(spark.x, spark.y), spark.size * 3, spark.size * 3)

                painter.setPen(QPen(c, spark.size / 2))
                path = QPainterPath()
                rays = 6 if spark.value >= 50 else 4
                for i in range(rays):
                    angle = i * (360 / rays)
                    length = spark.size * (1.5 if i % 2 == 0 else 0.8)
                    path.moveTo(spark.x, spark.y)
                    path.lineTo(spark.x + length * math.cos(math.radians(angle)),
                                spark.y + length * math.sin(math.radians(angle)))
                painter.drawPath(path)

        for flame in self.flames:
            c = QColor(255, random.randint(120, 220), 20)
            c.setAlphaF(flame.life * 0.9)
            gradient = QRadialGradient(flame.x, flame.y, flame.size)
            gradient.setColorAt(0, c)
            gradient.setColorAt(1, QColor(255, 50, 0, 0))
            painter.setBrush(gradient)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QPointF(flame.x, flame.y), flame.size, flame.size)