from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QFont, QColor
from PySide6.QtCore import Qt, QRectF
import math


class OEEGauge(QWidget):

    def __init__(
        self,
        oee=84.2,
        availability=92.1,
        performance=89.3,
        quality=96.8
    ):
        super().__init__()

        self.oee = oee
        self.availability = availability
        self.performance = performance
        self.quality = quality

        self.setMinimumSize(300, 270)

    def update_values(
        self,
        oee,
        availability,
        performance,
        quality
    ):
        self.oee = max(0, min(100, oee))
        self.availability = max(0, min(100, availability))
        self.performance = max(0, min(100, performance))
        self.quality = max(0, min(100, quality))

        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()

        # ==========================================
        # GAUGE
        # ==========================================

        gauge_size = min(width - 60, 230)

        gauge_x = (width - gauge_size) / 2
        gauge_y = 30

        rect = QRectF(
            gauge_x,
            gauge_y,
            gauge_size,
            gauge_size
        )

        # ==========================================
        # FARVEZONER
        # ==========================================

        pen = QPen()
        pen.setWidth(24)
        pen.setCapStyle(Qt.FlatCap)

        # Rød: 0-50
        pen.setColor(QColor("#ff4148"))
        painter.setPen(pen)

        painter.drawArc(
            rect,
            180 * 16,
            -90 * 16
        )

        # Orange: 50-65
        pen.setColor(QColor("#ff9814"))
        painter.setPen(pen)

        painter.drawArc(
            rect,
            90 * 16,
            -27 * 16
        )

        # Gul: 65-75
        pen.setColor(QColor("#ffd21c"))
        painter.setPen(pen)

        painter.drawArc(
            rect,
            63 * 16,
            -18 * 16
        )

        # Grøn: 75-100
        pen.setColor(QColor("#45dc7a"))
        painter.setPen(pen)

        painter.drawArc(
            rect,
            45 * 16,
            -45 * 16
        )

        # ==========================================
        # MIDTPUNKT
        # ==========================================

        center_x = gauge_x + gauge_size / 2
        center_y = gauge_y + gauge_size / 2

        # ==========================================
        # NÅL
        # ==========================================

        angle = 180 - (self.oee * 1.8)
        angle_rad = math.radians(angle)

        needle_length = gauge_size * 0.38

        end_x = center_x + math.cos(angle_rad) * needle_length
        end_y = center_y - math.sin(angle_rad) * needle_length

        needle_pen = QPen(Qt.black)
        needle_pen.setWidth(4)

        painter.setPen(needle_pen)

        painter.drawLine(
            int(center_x),
            int(center_y),
            int(end_x),
            int(end_y)
        )

        # Midterpunkt
        painter.setBrush(QColor("#bfcbd8"))
        painter.setPen(Qt.NoPen)

        painter.drawEllipse(
            int(center_x - 6),
            int(center_y - 6),
            12,
            12
        )

        # ==========================================
        # OEE PROCENT
        # ==========================================

        oee_font = QFont()
        oee_font.setPointSize(28)
        oee_font.setBold(True)

        painter.setFont(oee_font)
        painter.setPen(QColor("white"))

        painter.drawText(
            QRectF(
                0,
                center_y - 85,
                width,
                45
            ),
            Qt.AlignCenter,
            f"{self.oee:.1f}%"
        )


        # ==========================================
        # 0 OG 100
        # ==========================================

        number_font = QFont()
        number_font.setPointSize(9)

        painter.setFont(number_font)
        painter.setPen(QColor("#b8c4d1"))

        painter.drawText(
            QRectF(
                gauge_x - 15,
                center_y - 2,
                30,
                20
            ),
            Qt.AlignCenter,
            "0"
        )

        painter.drawText(
            QRectF(
                gauge_x + gauge_size - 15,
                center_y - 2,
                30,
                20
            ),
            Qt.AlignCenter,
            "100"
        )

        # ==========================================
        # SEPARATOR
        # ==========================================

        separator_y = 190

        separator_pen = QPen(QColor("#34495e"))
        separator_pen.setWidth(1)

        painter.setPen(separator_pen)

        painter.drawLine(
            20,
            separator_y,
            width - 20,
            separator_y
        )

        # ==========================================
        # KPI'er
        # ==========================================

        values = [
            (self.availability, "Availability"),
            (self.performance, "Performance"),
            (self.quality, "Quality")
        ]

        column_width = width / 3

        value_font = QFont()
        value_font.setPointSize(16)
        value_font.setBold(True)

        label_font = QFont()
        label_font.setPointSize(9)

        for i, (value, label) in enumerate(values):

            x = i * column_width

            # Værdi
            painter.setFont(value_font)
            painter.setPen(QColor("#4aaeff"))

            painter.drawText(
                QRectF(
                    x,
                    200,
                    column_width,
                    30
                ),
                Qt.AlignCenter,
                f"{value:.1f}%"
            )

            # Label
            painter.setFont(label_font)
            painter.setPen(QColor("#b8c4d1"))

            painter.drawText(
                QRectF(
                    x,
                    230,
                    column_width,
                    25
                ),
                Qt.AlignCenter,
                label
            )

            # Lodret separator
            if i < 2:

                painter.setPen(
                    QPen(QColor("#34495e"))
                )

                painter.drawLine(
                    int(x + column_width),
                    200,
                    int(x + column_width),
                    255
                )

        # ==========================================
        # OEE TITEL
        # ==========================================

        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)

        painter.setFont(title_font)
        painter.setPen(QColor("#d5dee8"))

        painter.drawText(
            QRectF(0, 0, width, 335),
            Qt.AlignCenter,
            "OEE"
        )