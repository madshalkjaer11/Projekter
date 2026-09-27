import pyqtgraph as pg
import random

from PySide6.QtCore import QTimer

from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QVBoxLayout,
    QLabel,
    QFrame
)


class Overview(QWidget):

    def __init__(self):
        super().__init__()

        self.setup_ui()

    # ==========================================
    # UI
    # ==========================================

    def setup_ui(self):

        # ==========================================
        # MAIN LAYOUT
        # ==========================================

        layout = QGridLayout()

        layout.setSpacing(10)

        layout.setContentsMargins(
            15,
            15,
            15,
            15
        )

        self.setLayout(
            layout
        )

        # ==========================================
        # PLC STATUS
        # ==========================================

        plc_status = self.create_info_card(
            "PLC STATUS",
            "● Connected",
            "#45dc7a"
        )

        # ==========================================
        # MACHINE STATE
        # ==========================================

        machine_state = self.create_info_card(
            "MACHINE STATE",
            "RUNNING",
            "#45dc7a"
        )

        # ==========================================
        # OEE
        # ==========================================

        oee = self.create_info_card(
            "OEE",
            "84.2 %",
            "#4aaeff"
        )

        # ==========================================
        # TREND FRAME
        # ==========================================

        trend_frame = QFrame()

        trend_frame.setStyleSheet("""
            QFrame {
                background-color: #f4f4f4;
                border: 1px solid #bfc5ca;
                border-radius: 2px;
            }
        """)

        trend_layout = QVBoxLayout()

        trend_layout.setContentsMargins(
            12,
            10,
            12,
            10
        )

        trend_layout.setSpacing(
            5
        )

        trend_frame.setLayout(
            trend_layout
        )

        # ------------------------------------------
        # TREND TITLE
        # ------------------------------------------

        trend_title = QLabel(
            "OEE TREND"
        )

        trend_title.setStyleSheet("""
            QLabel {
                font-size: 15px;
                font-weight: bold;
                color: #222222;
                border: none;
                background: transparent;
            }
        """)

        trend_layout.addWidget(
            trend_title
        )

        # ------------------------------------------
        # GRAPH
        # ------------------------------------------

        self.graph = pg.PlotWidget()

        self.graph.setBackground(
            "#f4f4f4"
        )

        # Ingen zoom / pan
        self.graph.setMouseEnabled(
            x=False,
            y=False
        )

        # Y-akse 0-100
        self.graph.setYRange(
            0,
            100
        )

        self.graph.setLimits(
            yMin=0,
            yMax=100
        )

        # ------------------------------------------
        # AXES
        # ------------------------------------------

        left_axis = self.graph.getAxis(
            "left"
        )

        left_axis.setPen(
            pg.mkPen("#7a7a7a")
        )

        left_axis.setTextPen(
            pg.mkPen("#555555")
        )

        bottom_axis = self.graph.getAxis(
            "bottom"
        )

        bottom_axis.setPen(
            pg.mkPen("#7a7a7a")
        )

        bottom_axis.setTextPen(
            pg.mkPen("#555555")
        )

        # ------------------------------------------
        # GRID
        # ------------------------------------------

        self.graph.showGrid(
            x=False,
            y=True,
            alpha=0.15
        )

        self.graph.setLabel(
            "left",
            "OEE",
            units="%"
        )

        # ------------------------------------------
        # LIVE DATA
        # ------------------------------------------

        self.data = []

        self.time = []

        self.counter = 0

        self.max_points = 300

        self.curve = self.graph.plot(
            [],
            [],
            pen=pg.mkPen(
                "#4aaeff",
                width=3
            )
        )

        trend_layout.addWidget(
            self.graph
        )

        # ==========================================
        # MACHINE DATA
        # ==========================================

        machine_data = self.create_data_card(
            "MACHINE DATA",
            [
                "Speed: 72 %",
                "Temperature: 43 °C",
                "Pressure: 4.2 bar"
            ]
        )

        # ==========================================
        # ACTIVE ALARMS
        # ==========================================

        alarms = self.create_data_card(
            "ACTIVE ALARMS",
            [
                "● No active alarms"
            ]
        )

        # ==========================================
        # PLACEMENT
        # ==========================================

        layout.addWidget(
            plc_status,
            0,
            0
        )

        layout.addWidget(
            machine_state,
            0,
            1
        )

        layout.addWidget(
            oee,
            0,
            2
        )

        layout.addWidget(
            trend_frame,
            1,
            0,
            1,
            3
        )

        layout.addWidget(
            machine_data,
            2,
            0,
            1,
            2
        )

        layout.addWidget(
            alarms,
            2,
            2
        )

        # ==========================================
        # SIZE RATIOS
        # ==========================================

        layout.setColumnStretch(
            0,
            1
        )

        layout.setColumnStretch(
            1,
            1
        )

        layout.setColumnStretch(
            2,
            1
        )

        layout.setRowStretch(
            0,
            1
        )

        layout.setRowStretch(
            1,
            3
        )

        layout.setRowStretch(
            2,
            1
        )

        # ==========================================
        # TIMER
        # ==========================================

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.update_graph
        )

        self.timer.start(
            1000
        )

    # ==========================================
    # INFO CARD
    # ==========================================

    def create_info_card(
        self,
        title,
        value,
        value_color="#222222"
    ):

        frame = QFrame()

        frame.setStyleSheet("""
            QFrame {
                background-color: #f4f4f4;
                border: 1px solid #bfc5ca;
                border-radius: 2px;
            }
        """)

        layout = QVBoxLayout()

        layout.setContentsMargins(
            15,
            12,
            15,
            12
        )

        layout.setSpacing(
            4
        )

        frame.setLayout(
            layout
        )

        # ------------------------------------------
        # TITLE
        # ------------------------------------------

        title_label = QLabel(
            title
        )

        title_label.setStyleSheet("""
            QLabel {
                font-size: 11px;
                font-weight: bold;
                color: #555555;
                border: none;
                background: transparent;
            }
        """)

        # ------------------------------------------
        # VALUE
        # ------------------------------------------

        value_label = QLabel(
            value
        )

        value_label.setStyleSheet(f"""
            QLabel {{
                font-size: 24px;
                font-weight: bold;
                color: {value_color};
                border: none;
                background: transparent;
            }}
        """)

        layout.addWidget(
            title_label
        )

        layout.addWidget(
            value_label
        )

        return frame

    # ==========================================
    # DATA CARD
    # ==========================================

    def create_data_card(
        self,
        title,
        values
    ):

        frame = QFrame()

        frame.setStyleSheet("""
            QFrame {
                background-color: #f4f4f4;
                border: 1px solid #bfc5ca;
                border-radius: 2px;
            }
        """)

        layout = QVBoxLayout()

        layout.setContentsMargins(
            15,
            12,
            15,
            12
        )

        layout.setSpacing(
            7
        )

        frame.setLayout(
            layout
        )

        # ------------------------------------------
        # TITLE
        # ------------------------------------------

        title_label = QLabel(
            title
        )

        title_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                font-weight: bold;
                color: #555555;
                border: none;
                background: transparent;
            }
        """)

        layout.addWidget(
            title_label
        )

        # ------------------------------------------
        # VALUES
        # ------------------------------------------

        for value in values:

            label = QLabel(
                value
            )

            label.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #222222;
                    border: none;
                    background: transparent;
                }
            """)

            layout.addWidget(
                label
            )

        layout.addStretch()

        return frame

    # ==========================================
    # UPDATE GRAPH
    # ==========================================

    def update_graph(self):

        # Fiktiv OEE-værdi
        value = random.randint(
            75,
            95
        )

        self.data.append(
            value
        )

        self.time.append(
            self.counter
        )

        self.counter += 1

        # ==========================================
        # BEHOLD SENESTE 300
        # ==========================================

        if len(self.data) > self.max_points:

            self.data.pop(0)

            self.time.pop(0)

        # ==========================================
        # UPDATE CURVE
        # ==========================================

        self.curve.setData(
            self.time,
            self.data
        )

        # ==========================================
        # MOVE X AXIS
        # ==========================================

        if self.time:

            self.graph.setXRange(
                self.time[0],
                self.time[-1],
                padding=0.02
            )