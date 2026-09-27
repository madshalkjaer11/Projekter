from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QGridLayout
)

from PySide6.QtCore import Qt

from LOGIC.packml import get_state_name

from GUI.OEEGauge import OEEGauge
from GUI.PackMLStateChart import PackMLStateChart


class UnitCard(QFrame):

    def __init__(
        self,
        name,
        oee=84.2,
        availability=92.1,
        performance=89.3,
        quality=96.8
    ):
        super().__init__()

        self.name = name

        self.oee = oee
        self.availability = availability
        self.performance = performance
        self.quality = quality

        self.setup_ui()

    def setup_ui(self):

        self.setFrameShape(QFrame.Box)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # ==========================================
        # HEADER
        # ==========================================

        header = QHBoxLayout()

        title = QLabel(self.name)

        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
        """)

        self.state = QLabel("● UNKNOWN")

        self.state.setStyleSheet("""
            font-size: 15px;
            font-weight: bold;
            color: #45dc7a;
        """)

        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.state)

        layout.addLayout(header)

        # ==========================================
        # CONTENT
        # ==========================================

        content_layout = QGridLayout()

        content_layout.setColumnStretch(0, 1)
        content_layout.setColumnStretch(1, 1)

        # ==========================================
        # OEE
        # ==========================================

        oee_frame = QFrame()
        oee_frame.setFrameShape(QFrame.Box)

        oee_layout = QVBoxLayout()
        oee_layout.setContentsMargins(
            10,
            10,
            10,
            10
        )

        oee_layout.setAlignment(
            Qt.AlignTop
        )

        oee_frame.setLayout(
            oee_layout
        )

        self.oee_gauge = OEEGauge(
            self.oee,
            self.availability,
            self.performance,
            self.quality
        )

        oee_layout.addWidget(
            self.oee_gauge
        )

        content_layout.addWidget(
            oee_frame,
            0,
            0
        )

        # ==========================================
        # PACKML
        # ==========================================

        packml_frame = QFrame()
        packml_frame.setFrameShape(QFrame.Box)

        packml_layout = QVBoxLayout()

        packml_layout.setContentsMargins(
            10,
            10,
            10,
            10
        )

        packml_frame.setLayout(
            packml_layout
        )

        self.packml_chart = PackMLStateChart()

        self.packml_chart.setMaximumHeight(
            330
        )

        packml_layout.addWidget(
            self.packml_chart
        )

        content_layout.addWidget(
            packml_frame,
            0,
            1
        )

        layout.addLayout(
            content_layout
        )

    # ==========================================
    # UPDATE DATA
    # ==========================================

    def update_data(
        self,
        oee,
        availability,
        performance,
        quality,
        packml,
        packml_times
    ):

        self.oee = oee
        self.availability = availability
        self.performance = performance
        self.quality = quality

        # ======================================
        # CURRENT PACKML STATE
        # ======================================

        state_name = get_state_name(
            packml
        )

        self.state.setText(
            f"● {state_name}"
        )

        # ======================================
        # OEE GAUGE
        # ======================================

        self.oee_gauge.update_values(
            oee,
            availability,
            performance,
            quality
        )

        # ======================================
        # PACKML STATE TIME
        # ======================================

        self.packml_chart.update_data(
            packml_times,
            state_name
        )