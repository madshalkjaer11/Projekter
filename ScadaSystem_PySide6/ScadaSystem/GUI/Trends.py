from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox
)

from PySide6.QtCore import QSignalBlocker

from pyqtgraph.graphicsItems.DateAxisItem import DateAxisItem

import pyqtgraph as pg


class Trends(QWidget):

    def __init__(
        self,
        config,
        data_model
    ):
        super().__init__()

        self.config = config
        self.data_model = data_model

        # ==========================================
        # SETTINGS
        # ==========================================

        self.time_options = {
            "1 min": 60,
            "5 min": 300,
            "15 min": 900,
            "30 min": 1800
        }

        self.visible_points = 60

        # ==========================================
        # COLORS
        # ==========================================

        self.colors = [
            "#4aaeff",
            "#45dc7a",
            "#ffcc66",
            "#ff6b6b",
            "#b084ff",
            "#00d4aa",
            "#ff8c42",
            "#7bdff2",
            "#f15bb5",
            "#9bde7e"
        ]

        # ==========================================
        # NAMES
        # ==========================================

        self.names = []

        # ==========================================
        # HISTORY
        # ==========================================

        self.history = {}

        # ==========================================
        # CURVES
        # ==========================================

        self.curves = {}

        # ==========================================
        # UI
        # ==========================================

        self.setup_ui()

        # ==========================================
        # LOAD SETTINGS
        # ==========================================

        self.refresh()

        # ==========================================
        # DATA MODEL SIGNAL
        # ==========================================

        self.data_model.data_updated.connect(
            self.update_data
        )

    # ==========================================
    # UI
    # ==========================================

    def setup_ui(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(
            15,
            15,
            15,
            15
        )

        layout.setSpacing(
            10
        )

        self.setLayout(
            layout
        )

        # ==========================================
        # TITLE
        # ==========================================

        title = QLabel(
            "TRENDS"
        )

        title.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
        """)

        layout.addWidget(
            title
        )

        # ==========================================
        # CONTROLS
        # ==========================================

        controls = QHBoxLayout()

        # ------------------------------------------
        # TREND
        # ------------------------------------------

        trend_label = QLabel(
            "Trend:"
        )

        self.trend_combo = QComboBox()

        self.trend_combo.setFixedWidth(
            150
        )

        self.trend_combo.currentTextChanged.connect(
            self.change_trend
        )

        controls.addWidget(
            trend_label
        )

        controls.addWidget(
            self.trend_combo
        )

        controls.addSpacing(
            20
        )

        # ------------------------------------------
        # METRIC
        # ------------------------------------------

        metric_label = QLabel(
            "Metric:"
        )

        self.metric_combo = QComboBox()

        self.metric_combo.addItems([
            "OEE",
            "Availability",
            "Performance",
            "Quality"
        ])

        self.metric_combo.setFixedWidth(
            150
        )

        self.metric_combo.currentTextChanged.connect(
            self.change_metric
        )

        controls.addWidget(
            metric_label
        )

        controls.addWidget(
            self.metric_combo
        )

        controls.addSpacing(
            20
        )

        # ------------------------------------------
        # TIME
        # ------------------------------------------

        time_label = QLabel(
            "Time:"
        )

        self.time_combo = QComboBox()

        self.time_combo.addItems(
            self.time_options.keys()
        )

        self.time_combo.setFixedWidth(
            150
        )

        self.time_combo.currentTextChanged.connect(
            self.change_time
        )

        controls.addWidget(
            time_label
        )

        controls.addWidget(
            self.time_combo
        )

        controls.addStretch()

        layout.addLayout(
            controls
        )

        # ==========================================
        # GRAPH
        # ==========================================

        axis = DateAxisItem(
            orientation="bottom"
        )

        self.graph = pg.PlotWidget(
            axisItems={
                "bottom": axis
            }
        )

        self.graph.setBackground(
            "#141c24"
        )

        self.graph.setLabel(
            "left",
            "OEE",
            units="%"
        )

        self.graph.setLabel(
            "bottom",
            "Time"
        )

        # ==========================================
        # Y = 0-100
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
        # NO ZOOM / PAN
        # ==========================================

        self.graph.setMouseEnabled(
            x=False,
            y=False
        )

        # ==========================================
        # GRID
        # ==========================================

        self.graph.showGrid(
            x=True,
            y=True,
            alpha=0.2
        )

        layout.addWidget(
            self.graph
        )

    # ==========================================
    # GET NAMES FROM CONFIG
    # ==========================================

    def get_names(self):

        names = []

        # ==========================================
        # UNITS
        # ==========================================

        for unit in self.config.config.get(
            "units",
            []
        ):

            names.append(
                unit["name"]
            )

        # ==========================================
        # EMS
        # ==========================================

        for em in self.config.config.get(
            "ems",
            []
        ):

            names.append(
                em["name"]
            )

        return names

    # ==========================================
    # REFRESH
    # ==========================================

    def refresh(self):

        old_names = self.names

        self.names = self.get_names()

        # ==========================================
        # CREATE NEW HISTORY
        # ==========================================

        new_history = {}

        for name in self.names:

            if name in self.history:

                new_history[name] = (
                    self.history[name]
                )

            else:

                new_history[name] = {
                    "time": [],
                    "OEE": [],
                    "Availability": [],
                    "Performance": [],
                    "Quality": []
                }

        self.history = new_history

        # ==========================================
        # UPDATE COMBO
        # ==========================================

        self.update_trend_combo()

        # ==========================================
        # UPDATE CURVES
        # ==========================================

        self.update_curves()

        # ==========================================
        # UPDATE GRAPH
        # ==========================================

        self.update_graph()

    # ==========================================
    # UPDATE TREND COMBO
    # ==========================================

    def update_trend_combo(self):

        current = (
            self.trend_combo.currentText()
        )

        blocker = QSignalBlocker(
            self.trend_combo
        )

        self.trend_combo.clear()

        self.trend_combo.addItem(
            "ALL"
        )

        self.trend_combo.addItems(
            self.names
        )

        # ==========================================
        # KEEP PREVIOUS SELECTION
        # ==========================================

        if current in self.names:

            index = (
                self.trend_combo.findText(
                    current
                )
            )

            self.trend_combo.setCurrentIndex(
                index
            )

        else:

            self.trend_combo.setCurrentIndex(
                0
            )

        del blocker

    # ==========================================
    # UPDATE CURVES
    # ==========================================

    def update_curves(self):

        # ==========================================
        # REMOVE OLD CURVES
        # ==========================================

        for curve in self.curves.values():

            self.graph.removeItem(
                curve
            )

        self.curves = {}

        # ==========================================
        # CREATE NEW CURVES
        # ==========================================

        for index, name in enumerate(
            self.names
        ):

            color = self.colors[
                index % len(
                    self.colors
                )
            ]

            curve = self.graph.plot(
                [],
                [],
                pen=pg.mkPen(
                    color=color,
                    width=3
                )
            )

            self.curves[name] = curve

    # ==========================================
    # UPDATE DATA
    # ==========================================

    def update_data(self):

        # ==========================================
        # GET CURRENT TIME
        # ==========================================

        from PySide6.QtCore import QDateTime

        timestamp = (
            QDateTime.currentDateTime()
            .toSecsSinceEpoch()
        )

        # ==========================================
        # READ DATA FROM DATA MODEL
        # ==========================================

        for name in self.names:

            data = None

            # --------------------------------------
            # UNIT
            # --------------------------------------

            if name in self.data_model.get_units():

                data = (
                    self.data_model.get_unit(
                        name
                    )
                )

            # --------------------------------------
            # EM
            # --------------------------------------

            elif name in self.data_model.get_ems():

                data = (
                    self.data_model.get_em(
                        name
                    )
                )

            if data is None:

                continue

            # ======================================
            # SAVE CURRENT VALUES
            # ======================================

            for metric in [
                "OEE",
                "Availability",
                "Performance",
                "Quality"
            ]:

                value = data.get(
                    metric,
                    0
                )

                try:

                    value = float(
                        value
                    )

                except (
                    TypeError,
                    ValueError
                ):

                    value = 0

                value = max(
                    0,
                    min(
                        100,
                        value
                    )
                )

                self.history[
                    name
                ][metric].append(
                    value
                )

            # ======================================
            # SAVE TIMESTAMP
            # ======================================

            self.history[
                name
            ]["time"].append(
                timestamp
            )

            # ======================================
            # LIMIT HISTORY
            # ======================================

            if len(
                self.history[name]["time"]
            ) > 1800:

                self.history[
                    name
                ]["time"].pop(
                    0
                )

                for metric in [
                    "OEE",
                    "Availability",
                    "Performance",
                    "Quality"
                ]:

                    self.history[
                        name
                    ][metric].pop(
                        0
                    )

        # ==========================================
        # UPDATE GRAPH
        # ==========================================

        self.update_graph()

    # ==========================================
    # UPDATE GRAPH
    # ==========================================

    def update_graph(self):

        metric = (
            self.metric_combo.currentText()
        )

        selected = (
            self.trend_combo.currentText()
        )

        # ==========================================
        # WHICH CURVES?
        # ==========================================

        if selected == "ALL":

            visible_names = self.names

        else:

            visible_names = [
                selected
            ]

        # ==========================================
        # UPDATE CURVES
        # ==========================================

        for name in self.names:

            curve = self.curves.get(
                name
            )

            if curve is None:

                continue

            if name in visible_names:

                times = (
                    self.history[name]["time"]
                )

                values = (
                    self.history[name][metric]
                )

                times = times[
                    -self.visible_points:
                ]

                values = values[
                    -self.visible_points:
                ]

                curve.setData(
                    times,
                    values
                )

                curve.setVisible(
                    True
                )

            else:

                curve.clear()

                curve.setVisible(
                    False
                )

        # ==========================================
        # UPDATE TIME RANGE
        # ==========================================

        self.update_time_range()

    # ==========================================
    # CHANGE TREND
    # ==========================================

    def change_trend(
        self,
        trend
    ):

        self.update_graph()

    # ==========================================
    # CHANGE METRIC
    # ==========================================

    def change_metric(
        self,
        metric
    ):

        self.graph.setLabel(
            "left",
            metric,
            units="%"
        )

        self.update_graph()

    # ==========================================
    # CHANGE TIME
    # ==========================================

    def change_time(
        self,
        time_text
    ):

        if time_text not in self.time_options:

            return

        self.visible_points = (
            self.time_options[
                time_text
            ]
        )

        self.update_graph()

    # ==========================================
    # TIME RANGE
    # ==========================================

    def update_time_range(self):

        selected = (
            self.trend_combo.currentText()
        )

        # ==========================================
        # WHICH NAMES?
        # ==========================================

        if selected == "ALL":

            names = self.names

        else:

            names = [
                selected
            ]

        # ==========================================
        # FIND TIMES
        # ==========================================

        all_times = []

        for name in names:

            if name not in self.history:

                continue

            all_times.extend(
                self.history[
                    name
                ]["time"]
            )

        # ==========================================
        # NO DATA
        # ==========================================

        if not all_times:

            return

        visible_times = (
            all_times[
                -self.visible_points:
            ]
        )

        if not visible_times:

            return

        # ==========================================
        # START / END
        # ==========================================

        start_time = min(
            visible_times
        )

        end_time = max(
            visible_times
        )

        # ==========================================
        # ONLY ONE DATA POINT
        # ==========================================

        if start_time == end_time:

            start_time -= 5
            end_time += 5

        # ==========================================
        # X RANGE
        # ==========================================

        self.graph.setXRange(
            start_time,
            end_time,
            padding=0.02
        )