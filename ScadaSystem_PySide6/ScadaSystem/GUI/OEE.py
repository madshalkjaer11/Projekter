from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QFrame,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QScrollArea
)

from PySide6.QtCore import Qt

import pyqtgraph as pg


class OEE(QWidget):

    def __init__(
        self,
        config,
        data_model
    ):
        super().__init__()

        self.config = config
        self.data_model = data_model

        # ==========================================
        # DATA
        # ==========================================

        self.data = []

        # ==========================================
        # GRAPH ELEMENTS
        # ==========================================

        self.bars = None
        self.value_labels = []

        # ==========================================
        # UI
        # ==========================================

        self.setup_ui()

        # ==========================================
        # INITIAL DATA
        # ==========================================

        self.refresh()

        # ==========================================
        # DATA MODEL SIGNAL
        # ==========================================

        self.data_model.data_updated.connect(
            self.update_data
        )

    # ==========================================
    # MAIN UI
    # ==========================================

    def setup_ui(self):

        # ==========================================
        # SCROLL AREA
        # ==========================================

        scroll = QScrollArea()

        scroll.setWidgetResizable(
            True
        )

        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
            }

            QScrollBar:vertical {
                width: 10px;
                margin: 2px;
            }
        """)

        # ==========================================
        # CONTENT
        # ==========================================

        content = QWidget()

        layout = QVBoxLayout()

        layout.setContentsMargins(
            15,
            15,
            15,
            20
        )

        layout.setSpacing(
            15
        )

        content.setLayout(
            layout
        )

        scroll.setWidget(
            content
        )

        # ==========================================
        # MAIN LAYOUT
        # ==========================================

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        main_layout.addWidget(
            scroll
        )

        self.setLayout(
            main_layout
        )

        # ==========================================
        # TITLE
        # ==========================================

        title = QLabel(
            "OEE OVERVIEW"
        )

        title.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: bold;
            }
        """)

        layout.addWidget(
            title
        )

        # ==========================================
        # KPI CARDS
        # ==========================================

        kpi_layout = QGridLayout()

        kpi_layout.setSpacing(
            10
        )

        self.total_oee_card, self.total_oee_value = (
            self.create_kpi_card(
                "TOTAL OEE",
                0
            )
        )

        self.availability_card, self.availability_value = (
            self.create_kpi_card(
                "AVAILABILITY",
                0
            )
        )

        self.performance_card, self.performance_value = (
            self.create_kpi_card(
                "PERFORMANCE",
                0
            )
        )

        self.quality_card, self.quality_value = (
            self.create_kpi_card(
                "QUALITY",
                0
            )
        )

        kpi_layout.addWidget(
            self.total_oee_card,
            0,
            0
        )

        kpi_layout.addWidget(
            self.availability_card,
            0,
            1
        )

        kpi_layout.addWidget(
            self.performance_card,
            0,
            2
        )

        kpi_layout.addWidget(
            self.quality_card,
            0,
            3
        )

        layout.addLayout(
            kpi_layout
        )

        # ==========================================
        # OEE BAR CHART FRAME
        # ==========================================

        graph_frame = QFrame()

        graph_frame.setStyleSheet("""
            QFrame {
                border: 1px solid #bfc5ca;
                border-radius: 2px;
                background: #f4f4f4;
            }
        """)

        graph_layout = QVBoxLayout()

        graph_layout.setContentsMargins(
            10,
            8,
            10,
            8
        )

        graph_frame.setLayout(
            graph_layout
        )

        # ==========================================
        # GRAPH TITLE
        # ==========================================

        graph_title = QLabel(
            "OEE BY UNIT / EM"
        )

        graph_title.setStyleSheet("""
            QLabel {
                font-size: 15px;
                font-weight: bold;
                border: none;
                background: transparent;
            }
        """)

        graph_layout.addWidget(
            graph_title
        )

        # ==========================================
        # GRAPH
        # ==========================================

        self.graph = pg.PlotWidget()

        self.graph.setBackground(
            "#f4f4f4"
        )

        self.graph.setMinimumHeight(
            260
        )

        self.graph.setMaximumHeight(
            300
        )

        # ==========================================
        # NO ZOOM / PAN
        # ==========================================

        self.graph.setMouseEnabled(
            x=False,
            y=False
        )

        # ==========================================
        # Y-AXIS
        # ==========================================

        self.graph.setYRange(
            0,
            100
        )

        self.graph.setLimits(
            yMin=0,
            yMax=100
        )

        # ==========================================
        # AXES
        # ==========================================

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

        # ==========================================
        # GRID
        # ==========================================

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

        graph_layout.addWidget(
            self.graph
        )

        layout.addWidget(
            graph_frame
        )

        # ==========================================
        # TABLE TITLE
        # ==========================================

        table_title = QLabel(
            "OEE DETAILS"
        )

        table_title.setStyleSheet("""
            QLabel {
                font-size: 15px;
                font-weight: bold;
            }
        """)

        layout.addWidget(
            table_title
        )

        # ==========================================
        # TABLE
        # ==========================================

        self.table = QTableWidget()

        self.table.setRowCount(
            0
        )

        self.table.setColumnCount(
            5
        )

        self.table.setHorizontalHeaderLabels([
            "NAME",
            "OEE",
            "AVAILABILITY",
            "PERFORMANCE",
            "QUALITY"
        ])

        # ==========================================
        # TABLE STYLE
        # ==========================================

        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #f8f8f8;
                border: 1px solid #c5c5c5;
                gridline-color: #d8d8d8;
                font-size: 13px;
            }

            QTableWidget::item {
                padding: 8px;
            }

            QTableWidget::item:selected {
                background-color: #e4e4e4;
                color: #111111;
            }

            QHeaderView::section {
                background-color: #e9e9e9;
                color: #222222;
                border: none;
                border-right: 1px solid #d0d0d0;
                border-bottom: 1px solid #c5c5c5;
                padding: 8px;
                font-weight: bold;
            }
        """)

        # ==========================================
        # TABLE SETTINGS
        # ==========================================

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.verticalHeader().setVisible(
            False
        )

        self.table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.table.setSelectionMode(
            QTableWidget.NoSelection
        )

        self.table.setFocusPolicy(
            Qt.NoFocus
        )

        self.table.verticalHeader().setDefaultSectionSize(
            40
        )

        self.table.setFixedHeight(
            290
        )

        layout.addWidget(
            self.table
        )

        # ==========================================
        # BOTTOM SPACE
        # ==========================================

        layout.addSpacing(
            10
        )

    # ==========================================
    # KPI CARD
    # ==========================================

    def create_kpi_card(
        self,
        title,
        value
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

        frame.setLayout(
            layout
        )

        # ==========================================
        # TITLE
        # ==========================================

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

        # ==========================================
        # VALUE
        # ==========================================

        value_label = QLabel(
            f"{value:.1f}%"
        )

        value_label.setStyleSheet("""
            QLabel {
                font-size: 27px;
                font-weight: bold;
                color: #111111;
                border: none;
                background: transparent;
            }
        """)

        layout.addWidget(
            title_label
        )

        layout.addWidget(
            value_label
        )

        return frame, value_label

    # ==========================================
    # REFRESH
    # ==========================================

    def refresh(self):

        self.update_data()

    # ==========================================
    # UPDATE DATA FROM DATA MODEL
    # ==========================================

    def update_data(self):

        self.data = []

        # ==========================================
        # UNITS
        # ==========================================

        for name, data in (
            self.data_model.get_units().items()
        ):

            self.data.append({
                "name": name,
                "oee": self.safe_number(
                    data.get(
                        "OEE",
                        0
                    )
                ),
                "availability": self.safe_number(
                    data.get(
                        "Availability",
                        0
                    )
                ),
                "performance": self.safe_number(
                    data.get(
                        "Performance",
                        0
                    )
                ),
                "quality": self.safe_number(
                    data.get(
                        "Quality",
                        0
                    )
                )
            })

        # ==========================================
        # EMS
        # ==========================================

        for name, data in (
            self.data_model.get_ems().items()
        ):

            self.data.append({
                "name": name,
                "oee": self.safe_number(
                    data.get(
                        "OEE",
                        0
                    )
                ),
                "availability": self.safe_number(
                    data.get(
                        "Availability",
                        0
                    )
                ),
                "performance": self.safe_number(
                    data.get(
                        "Performance",
                        0
                    )
                ),
                "quality": self.safe_number(
                    data.get(
                        "Quality",
                        0
                    )
                )
            })

        # ==========================================
        # UPDATE UI
        # ==========================================

        self.update_kpis()

        self.update_graph()

        self.update_table()

    # ==========================================
    # UPDATE KPI
    # ==========================================

    def update_kpis(self):

        total_oee = self.calculate_average(
            "oee"
        )

        availability = self.calculate_average(
            "availability"
        )

        performance = self.calculate_average(
            "performance"
        )

        quality = self.calculate_average(
            "quality"
        )

        # ==========================================
        # UPDATE LABELS
        # ==========================================

        self.total_oee_value.setText(
            f"{total_oee:.1f}%"
        )

        self.availability_value.setText(
            f"{availability:.1f}%"
        )

        self.performance_value.setText(
            f"{performance:.1f}%"
        )

        self.quality_value.setText(
            f"{quality:.1f}%"
        )

    # ==========================================
    # UPDATE GRAPH
    # ==========================================

    def update_graph(self):

        # ==========================================
        # REMOVE OLD BAR CHART
        # ==========================================

        if self.bars is not None:

            self.graph.removeItem(
                self.bars
            )

        # ==========================================
        # REMOVE OLD VALUE LABELS
        # ==========================================

        for label in self.value_labels:

            self.graph.removeItem(
                label
            )

        self.value_labels = []

        # ==========================================
        # DATA
        # ==========================================

        names = [
            item["name"]
            for item in self.data
        ]

        values = [
            item["oee"]
            for item in self.data
        ]

        # ==========================================
        # EMPTY DATA
        # ==========================================

        if not values:

            self.bars = None

            self.graph.setXRange(
                -1,
                1
            )

            self.graph.getAxis(
                "bottom"
            ).setTicks([
                []
            ])

            return

        # ==========================================
        # BAR CHART
        # ==========================================

        self.bars = pg.BarGraphItem(
            x=list(
                range(
                    len(values)
                )
            ),
            height=values,
            width=0.55,
            brush="#4aaeff",
            pen=None
        )

        self.graph.addItem(
            self.bars
        )

        # ==========================================
        # VALUES INSIDE BARS
        # ==========================================

        for index, value in enumerate(
            values
        ):

            text = pg.TextItem(
                text=f"{value:.1f}%",
                color="white",
                anchor=(
                    0.5,
                    0.5
                )
            )

            text.setPos(
                index,
                max(
                    value - 5,
                    2
                )
            )

            self.graph.addItem(
                text
            )

            self.value_labels.append(
                text
            )

        # ==========================================
        # X AXIS
        # ==========================================

        bottom_axis = self.graph.getAxis(
            "bottom"
        )

        bottom_axis.setTicks([
            list(
                enumerate(
                    names
                )
            )
        ])

        # ==========================================
        # X RANGE
        # ==========================================

        self.graph.setXRange(
            -0.75,
            max(
                len(values) - 0.25,
                0.25
            ),
            padding=0
        )

    # ==========================================
    # UPDATE TABLE
    # ==========================================

    def update_table(self):

        self.table.setRowCount(
            len(self.data)
        )

        self.table.clearContents()

        self.populate_table()

    # ==========================================
    # POPULATE TABLE
    # ==========================================

    def populate_table(self):

        for row, item in enumerate(
            self.data
        ):

            values = [
                item["name"],
                f'{item["oee"]:.1f}%',
                f'{item["availability"]:.1f}%',
                f'{item["performance"]:.1f}%',
                f'{item["quality"]:.1f}%'
            ]

            for column, value in enumerate(
                values
            ):

                cell = QTableWidgetItem(
                    value
                )

                cell.setTextAlignment(
                    Qt.AlignCenter
                )

                self.table.setItem(
                    row,
                    column,
                    cell
                )

    # ==========================================
    # CALCULATE AVERAGE
    # ==========================================

    def calculate_average(
        self,
        key
    ):

        values = [
            item[key]
            for item in self.data
            if key in item
        ]

        if not values:

            return 0

        return sum(values) / len(values)

    # ==========================================
    # SAFE NUMBER
    # ==========================================

    def safe_number(
        self,
        value
    ):

        try:

            value = float(
                value
            )

            return max(
                0,
                min(
                    100,
                    value
                )
            )

        except (
            TypeError,
            ValueError
        ):

            return 0