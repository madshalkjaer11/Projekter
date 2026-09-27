import os
import csv

from datetime import datetime, timedelta

import pyqtgraph as pg

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QDateEdit,
    QFrame,
    QCheckBox,
    QGridLayout,
    QProgressBar,
    QScrollArea
)

from PySide6.QtCore import Qt, QDate

from pyqtgraph.graphicsItems.DateAxisItem import DateAxisItem


class History(QWidget):

    def __init__(self, config):
        super().__init__()

        self.config = config

        # ==========================================
        # LOG FOLDER
        # ==========================================

        self.log_folder = os.path.join(
            os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            ),
            "DATA",
            "LOGS"
        )

        # ==========================================
        # DATA
        # ==========================================

        self.data = []

        # ==========================================
        # METRIC COLORS
        # ==========================================

        self.metric_colors = {
            "OEE": "#4aaeff",
            "Availability": "#45dc7a",
            "Performance": "#ffcc66",
            "Quality": "#ff6b6b"
        }

        # ==========================================
        # GRAPH
        # ==========================================

        self.curves = {}

        # ==========================================
        # PACKML
        # ==========================================

        self.packml_display_states = [
            "IDLE",
            "EXECUTE",
            "SUSPENDED",
            "HELD",
            "COMPLETE",
            "ABORTED",
            "STOPPED"
        ]

        self.packml_times = {
            state: 0.0
            for state in self.packml_display_states
        }

        self.packml_cards = {}

        # ==========================================
        # UI
        # ==========================================

        self.setup_ui()

        self.update_names()

        self.change_period(
            self.period_combo.currentText()
        )

    # ==========================================
    # SETUP UI
    # ==========================================

    def setup_ui(self):

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
            15,
            15,
            15,
            15
        )

        main_layout.setSpacing(10)

        self.setLayout(
            main_layout
        )

        # ==========================================
        # TITLE
        # ==========================================

        title = QLabel(
            "HISTORY"
        )

        title.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: bold;
                color: #000000;
            }
        """)

        main_layout.addWidget(
            title
        )

        # ==========================================
        # CONTROL FRAME
        # ==========================================

        control_frame = QFrame()

        control_frame.setStyleSheet("""
            QFrame {
                background-color: #f4f4f4;
                border: 1px solid #2d4052;
                border-radius: 8px;
            }
        """)

        control_layout = QVBoxLayout()

        control_layout.setContentsMargins(
            12,
            10,
            12,
            10
        )

        control_layout.setSpacing(8)

        control_frame.setLayout(
            control_layout
        )

        # ==========================================
        # TOP CONTROLS
        # ==========================================

        controls = QHBoxLayout()

        controls.setSpacing(8)

        # Period
        controls.addWidget(
            self.create_control_label("Period:")
        )

        self.period_combo = QComboBox()

        self.period_combo.addItems([
            "Today",
            "Yesterday",
            "Last 7 days",
            "Last 30 days",
            "Custom"
        ])

        self.period_combo.setFixedWidth(150)

        self.period_combo.currentTextChanged.connect(
            self.change_period
        )

        controls.addWidget(
            self.period_combo
        )

        controls.addSpacing(10)

        # From
        self.from_label = self.create_control_label(
            "From:"
        )

        self.from_date = QDateEdit()

        self.from_date.setCalendarPopup(True)
        self.from_date.setDisplayFormat("dd-MM-yyyy")
        self.from_date.setFixedWidth(125)

        self.from_date.dateChanged.connect(
            self.custom_date_changed
        )

        controls.addWidget(
            self.from_label
        )

        controls.addWidget(
            self.from_date
        )

        # To
        self.to_label = self.create_control_label(
            "To:"
        )

        self.to_date = QDateEdit()

        self.to_date.setCalendarPopup(True)
        self.to_date.setDisplayFormat("dd-MM-yyyy")
        self.to_date.setFixedWidth(125)

        self.to_date.dateChanged.connect(
            self.custom_date_changed
        )

        controls.addWidget(
            self.to_label
        )

        controls.addWidget(
            self.to_date
        )

        controls.addSpacing(10)

        # Device
        controls.addWidget(
            self.create_control_label("Device:")
        )

        self.device_combo = QComboBox()

        self.device_combo.setFixedWidth(150)

        self.device_combo.currentTextChanged.connect(
            self.load_data
        )

        controls.addWidget(
            self.device_combo
        )

        controls.addStretch()

        control_layout.addLayout(
            controls
        )

        # ==========================================
        # METRIC CONTROLS
        # ==========================================

        metric_layout = QHBoxLayout()

        metric_layout.setSpacing(12)

        metric_label = QLabel(
            "Show:"
        )

        metric_label.setStyleSheet("""
            QLabel {
                font-size: 11px;
                font-weight: bold;
                color: #d5dee8;
                border: none;
            }
        """)

        metric_layout.addWidget(
            metric_label
        )

        self.oee_checkbox = self.create_metric_checkbox(
            "OEE",
            True
        )

        self.availability_checkbox = self.create_metric_checkbox(
            "Availability",
            False
        )

        self.performance_checkbox = self.create_metric_checkbox(
            "Performance",
            False
        )

        self.quality_checkbox = self.create_metric_checkbox(
            "Quality",
            False
        )

        metric_layout.addWidget(
            self.oee_checkbox
        )

        metric_layout.addWidget(
            self.availability_checkbox
        )

        metric_layout.addWidget(
            self.performance_checkbox
        )

        metric_layout.addWidget(
            self.quality_checkbox
        )

        metric_layout.addStretch()

        control_layout.addLayout(
            metric_layout
        )

        main_layout.addWidget(
            control_frame
        )

        # ==========================================
        # KPI CARDS
        # ==========================================

        kpi_layout = QHBoxLayout()

        kpi_layout.setSpacing(10)

        self.average_card = self.create_kpi_card(
            "AVERAGE"
        )

        self.minimum_card = self.create_kpi_card(
            "MINIMUM"
        )

        self.maximum_card = self.create_kpi_card(
            "MAXIMUM"
        )

        self.samples_card = self.create_kpi_card(
            "SAMPLES"
        )

        kpi_layout.addWidget(
            self.average_card[0]
        )

        kpi_layout.addWidget(
            self.minimum_card[0]
        )

        kpi_layout.addWidget(
            self.maximum_card[0]
        )

        kpi_layout.addWidget(
            self.samples_card[0]
        )

        main_layout.addLayout(
            kpi_layout
        )

        # ==========================================
        # PACKML TITLE
        # ==========================================

        packml_title = QLabel(
            "PACKML STATE TIME"
        )

        packml_title.setStyleSheet("""
            QLabel {
                font-size: 15px;
                font-weight: bold;
                color: #000000;
            }
        """)

        main_layout.addWidget(
            packml_title
        )

        self.packml_total_label = QLabel(
            "Total state time: 00:00:00"
        )

        self.packml_total_label.setStyleSheet("""
            QLabel {
                font-size: 11px;
                color: #000000;
            }
        """)

        main_layout.addWidget(
            self.packml_total_label
        )

        # ==========================================
        # PACKML CARDS
        # ==========================================

        packml_grid = QGridLayout()

        packml_grid.setSpacing(8)

        for index, state in enumerate(
            self.packml_display_states
        ):

            (
                card,
                value_label,
                percentage_label,
                progress
            ) = self.create_packml_card(
                state
            )

            row = index // 4
            column = index % 4

            packml_grid.addWidget(
                card,
                row,
                column
            )

            self.packml_cards[state] = {
                "card": card,
                "value": value_label,
                "percentage": percentage_label,
                "progress": progress
            }

        main_layout.addLayout(
            packml_grid
        )

        # ==========================================
        # GRAPH
        # ==========================================

        graph_frame = QFrame()

        graph_frame.setStyleSheet("""
            QFrame {
                background-color: #f4f4f4;
                border: 1px solid #2d4052;
                border-radius: 8px;
            }
        """)

        graph_layout = QVBoxLayout()

        graph_layout.setContentsMargins(
            10,
            8,
            10,
            10
        )

        graph_frame.setLayout(
            graph_layout
        )

        graph_title = QLabel(
            "TREND HISTORY"
        )

        graph_title.setStyleSheet("""
            QLabel {
                font-size: 15px;
                font-weight: bold;
                color: #d5dee8;
                border: none;
            }
        """)

        graph_layout.addWidget(
            graph_title
        )

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

        self.graph.setMinimumHeight(
            280
        )

        self.graph.setLabel(
            "left",
            "Value",
            units="%"
        )

        self.graph.setLabel(
            "bottom",
            "Time"
        )

        self.graph.setYRange(
            0,
            100
        )

        self.graph.setLimits(
            yMin=0,
            yMax=100
        )

        self.graph.setMouseEnabled(
            x=True,
            y=False
        )

        self.graph.showGrid(
            x=True,
            y=True,
            alpha=0.2
        )

        self.graph.setStyleSheet("""
            QWidget {
                border: none;
            }
        """)

        graph_layout.addWidget(
            self.graph
        )

        main_layout.addWidget(
            graph_frame,
            1
        )

        # ==========================================
        # CREATE CURVES
        # ==========================================

        for metric, color in self.metric_colors.items():

            self.curves[metric] = self.graph.plot(
                [],
                [],
                pen=pg.mkPen(
                    color=color,
                    width=3
                )
            )

        # ==========================================
        # INITIAL VISIBILITY
        # ==========================================

        self.update_curve_visibility()

    # ==========================================
    # CONTROL LABEL
    # ==========================================

    def create_control_label(
        self,
        text
    ):

        label = QLabel(
            text
        )

        label.setStyleSheet("""
            QLabel {
                font-size: 11px;
                font-weight: bold;
                color: #d5dee8;
                border: none;
            }
        """)

        return label

    # ==========================================
    # METRIC CHECKBOX
    # ==========================================

    def create_metric_checkbox(
        self,
        text,
        checked=False
    ):

        checkbox = QCheckBox(
            text
        )

        checkbox.setChecked(
            checked
        )

        checkbox.setStyleSheet("""
            QCheckBox {
                color: #444444;
                spacing: 5px;
            }

            QCheckBox::indicator {
                width: 14px;
                height: 14px;
            }
        """)

        checkbox.stateChanged.connect(
            self.update_graph
        )

        return checkbox

    # ==========================================
    # KPI CARD
    # ==========================================

    def create_kpi_card(
        self,
        title
    ):

        frame = QFrame()

        frame.setMinimumHeight(
            80
        )

        frame.setStyleSheet("""
            QFrame {
                background-color: #f4f4f4;
                border: 1px solid #2d4052;
                border-radius: 8px;
            }
        """)

        layout = QVBoxLayout()

        layout.setContentsMargins(
            12,
            8,
            12,
            8
        )

        layout.setSpacing(2)

        frame.setLayout(
            layout
        )

        title_label = QLabel(
            title
        )

        title_label.setStyleSheet("""
            QLabel {
                font-size: 10px;
                font-weight: bold;
                color: #8fa1b3;
                border: none;
            }
        """)

        value_label = QLabel(
            "0"
        )

        value_label.setStyleSheet("""
            QLabel {
                font-size: 23px;
                font-weight: bold;
                color: #d5dee8;
                border: none;
            }
        """)

        value_label.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            title_label
        )

        layout.addWidget(
            value_label
        )

        return frame, value_label

    # ==========================================
    # PACKML CARD
    # ==========================================

    def create_packml_card(
        self,
        state
    ):

        frame = QFrame()

        frame.setMinimumHeight(
            68
        )

        frame.setStyleSheet("""
            QFrame {
                background-color: #f4f4f4;
                border: 1px solid #2d4052;
                border-radius: 6px;
            }
        """)

        card_layout = QVBoxLayout()

        card_layout.setContentsMargins(
            9,
            6,
            9,
            6
        )

        card_layout.setSpacing(
            3
        )

        frame.setLayout(
            card_layout
        )

        title_row = QHBoxLayout()

        state_label = QLabel(
            state
        )

        state_label.setStyleSheet("""
            QLabel {
                font-size: 10px;
                font-weight: bold;
                color: #d5dee8;
                border: none;
            }
        """)

        value_label = QLabel(
            "00:00:00"
        )

        value_label.setAlignment(
            Qt.AlignRight |
            Qt.AlignVCenter
        )

        value_label.setStyleSheet("""
            QLabel {
                font-size: 10px;
                color: #d5dee8;
                border: none;
            }
        """)

        percentage_label = QLabel(
            "0.0%"
        )

        percentage_label.setFixedWidth(
            38
        )

        percentage_label.setAlignment(
            Qt.AlignRight |
            Qt.AlignVCenter
        )

        percentage_label.setStyleSheet("""
            QLabel {
                font-size: 9px;
                color: #8fa1b3;
                border: none;
            }
        """)

        title_row.addWidget(
            state_label
        )

        title_row.addStretch()

        title_row.addWidget(
            value_label
        )

        title_row.addWidget(
            percentage_label
        )

        card_layout.addLayout(
            title_row
        )

        progress = QProgressBar()

        progress.setRange(
            0,
            100
        )

        progress.setValue(
            0
        )

        progress.setTextVisible(
            False
        )

        progress.setFixedHeight(
            5
        )

        progress.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: #263646;
                border-radius: 2px;
            }

            QProgressBar::chunk {
                background-color: #4aaeff;
                border-radius: 2px;
            }
        """)

        card_layout.addWidget(
            progress
        )

        return (
            frame,
            value_label,
            percentage_label,
            progress
        )

    # ==========================================
    # FORMAT PACKML TIME
    # ==========================================

    def format_packml_time(
        self,
        seconds
    ):

        seconds = int(
            max(
                0,
                seconds
            )
        )

        hours = seconds // 3600

        minutes = (
            (seconds % 3600)
            // 60
        )

        seconds = seconds % 60

        return (
            f"{hours:02d}:"
            f"{minutes:02d}:"
            f"{seconds:02d}"
        )

    # ==========================================
    # CALCULATE PACKML HISTORY
    # ==========================================

    def calculate_packml_history(self):

        times = {
            state: 0.0
            for state in self.packml_display_states
        }

        if len(self.data) < 2:
            return times

        rows = []

        for row in self.data:

            try:

                timestamp = datetime.strptime(
                    row["Timestamp"],
                    "%Y-%m-%d %H:%M:%S"
                )

                state = row.get(
                    "PackML",
                    ""
                ).strip().upper()

                if not state:
                    continue

                rows.append(
                    (
                        timestamp,
                        state
                    )
                )

            except (
                ValueError,
                TypeError,
                KeyError
            ):
                continue

        rows.sort(
            key=lambda item: item[0]
        )

        for index in range(
            len(rows) - 1
        ):

            timestamp, state = rows[index]

            next_timestamp = rows[
                index + 1
            ][0]

            delta = (
                next_timestamp - timestamp
            ).total_seconds()

            # Ignore large logging gaps.
            if delta <= 0 or delta > 10:
                continue

            if state in times:
                times[state] += delta

        return times

    # ==========================================
    # UPDATE PACKML HISTORY
    # ==========================================

    def update_packml_history(self):

        self.packml_times = (
            self.calculate_packml_history()
        )

        total_time = sum(
            self.packml_times.values()
        )

        self.packml_total_label.setText(
            "Total state time: "
            + self.format_packml_time(
                total_time
            )
        )

        for state in self.packml_display_states:

            seconds = self.packml_times.get(
                state,
                0
            )

            if total_time > 0:

                percentage = (
                    seconds
                    / total_time
                    * 100
                )

            else:
                percentage = 0

            card = self.packml_cards[
                state
            ]

            card["value"].setText(
                self.format_packml_time(
                    seconds
                )
            )

            card["percentage"].setText(
                f"{percentage:.1f}%"
            )

            card["progress"].setValue(
                int(percentage)
            )

    # ==========================================
    # UPDATE DEVICES
    # ==========================================

    def update_names(self):

        current_device = (
            self.device_combo.currentText()
        )

        self.device_combo.blockSignals(
            True
        )

        self.device_combo.clear()

        names = []

        units = self.config.config.get(
            "units",
            []
        )

        for unit in units:

            name = unit.get(
                "name",
                ""
            )

            if name:
                names.append(
                    name
                )

        ems = self.config.config.get(
            "ems",
            []
        )

        for em in ems:

            name = em.get(
                "name",
                ""
            )

            if name:
                names.append(
                    name
                )

        self.device_combo.addItems(
            names
        )

        self.device_combo.blockSignals(
            False
        )

        if current_device in names:

            self.device_combo.setCurrentText(
                current_device
            )

        elif names:

            self.device_combo.setCurrentIndex(
                0
            )

    # ==========================================
    # CHANGE PERIOD
    # ==========================================

    def change_period(
        self,
        period
    ):

        today = datetime.now().date()

        if period == "Today":

            start_date = today
            end_date = today

        elif period == "Yesterday":

            yesterday = (
                today - timedelta(
                    days=1
                )
            )

            start_date = yesterday
            end_date = yesterday

        elif period == "Last 7 days":

            start_date = (
                today - timedelta(
                    days=6
                )
            )

            end_date = today

        elif period == "Last 30 days":

            start_date = (
                today - timedelta(
                    days=29
                )
            )

            end_date = today

        elif period == "Custom":

            self.from_label.setVisible(
                True
            )

            self.from_date.setVisible(
                True
            )

            self.to_label.setVisible(
                True
            )

            self.to_date.setVisible(
                True
            )

            self.load_data()

            return

        else:
            return

        self.from_label.setVisible(
            False
        )

        self.from_date.setVisible(
            False
        )

        self.to_label.setVisible(
            False
        )

        self.to_date.setVisible(
            False
        )

        self.from_date.blockSignals(
            True
        )

        self.to_date.blockSignals(
            True
        )

        self.from_date.setDate(
            QDate(
                start_date.year,
                start_date.month,
                start_date.day
            )
        )

        self.to_date.setDate(
            QDate(
                end_date.year,
                end_date.month,
                end_date.day
            )
        )

        self.from_date.blockSignals(
            False
        )

        self.to_date.blockSignals(
            False
        )

        self.load_data()

    # ==========================================
    # CUSTOM DATE CHANGED
    # ==========================================

    def custom_date_changed(self):

        if self.period_combo.currentText() != "Custom":
            return

        if self.from_date.date() > self.to_date.date():

            self.to_date.blockSignals(
                True
            )

            self.to_date.setDate(
                self.from_date.date()
            )

            self.to_date.blockSignals(
                False
            )

        self.load_data()

    # ==========================================
    # GET SELECTED DATES
    # ==========================================

    def get_selected_dates(self):

        start = self.from_date.date()
        end = self.to_date.date()

        start_date = datetime(
            start.year(),
            start.month(),
            start.day()
        ).date()

        end_date = datetime(
            end.year(),
            end.month(),
            end.day()
        ).date()

        return start_date, end_date

    # ==========================================
    # LOAD DATA
    # ==========================================

    def load_data(self):

        self.data = []

        device = (
            self.device_combo.currentText()
        )

        if not device:

            self.update_graph()

            return

        start_date, end_date = (
            self.get_selected_dates()
        )

        current_date = start_date

        while current_date <= end_date:

            filename = (
                current_date.strftime(
                    "%Y-%m-%d"
                )
                + ".csv"
            )

            file_path = os.path.join(
                self.log_folder,
                filename
            )

            if os.path.exists(
                file_path
            ):

                self.read_csv_file(
                    file_path,
                    device
                )

            current_date += timedelta(
                days=1
            )

        self.data.sort(
            key=lambda row: row.get(
                "Timestamp",
                ""
            )
        )

        self.update_graph()

    # ==========================================
    # READ CSV FILE
    # ==========================================

    def read_csv_file(
        self,
        file_path,
        device
    ):

        try:

            with open(
                file_path,
                "r",
                newline="",
                encoding="utf-8"
            ) as file:

                reader = csv.DictReader(
                    file
                )

                for row in reader:

                    unit = row.get(
                        "Unit",
                        ""
                    )

                    em = row.get(
                        "EM",
                        ""
                    )

                    if (
                        unit == device
                        or em == device
                    ):

                        self.data.append(
                            row
                        )

        except Exception as e:

            print(
                f"History read error: {e}"
            )

    # ==========================================
    # SELECTED METRICS
    # ==========================================

    def get_selected_metrics(self):

        selected = []

        if self.oee_checkbox.isChecked():
            selected.append("OEE")

        if self.availability_checkbox.isChecked():
            selected.append("Availability")

        if self.performance_checkbox.isChecked():
            selected.append("Performance")

        if self.quality_checkbox.isChecked():
            selected.append("Quality")

        return selected

    # ==========================================
    # PRIMARY METRIC
    # ==========================================

    def get_primary_metric(self):

        selected = self.get_selected_metrics()

        if not selected:
            return None

        return selected[0]

    # ==========================================
    # UPDATE CURVE VISIBILITY
    # ==========================================

    def update_curve_visibility(self):

        selected = self.get_selected_metrics()

        for metric, curve in self.curves.items():

            curve.setVisible(
                metric in selected
            )

    # ==========================================
    # UPDATE GRAPH
    # ==========================================

    def update_graph(self):

        selected_metrics = (
            self.get_selected_metrics()
        )

        self.update_curve_visibility()

        self.update_packml_history()

        for metric in self.curves:

            self.curves[metric].clear()

        if not selected_metrics:

            self.update_kpis([])

            return

        all_times = []

        metric_values = {}

        for metric in selected_metrics:

            times = []
            values = []

            for row in self.data:

                try:

                    timestamp = datetime.strptime(
                        row["Timestamp"],
                        "%Y-%m-%d %H:%M:%S"
                    ).timestamp()

                    value = float(
                        row[metric]
                    )

                    value = max(
                        0,
                        min(
                            100,
                            value
                        )
                    )

                    times.append(
                        timestamp
                    )

                    values.append(
                        value
                    )

                except (
                    ValueError,
                    TypeError,
                    KeyError
                ):
                    continue

            if times:

                combined = sorted(
                    zip(
                        times,
                        values
                    )
                )

                times = [
                    item[0]
                    for item in combined
                ]

                values = [
                    item[1]
                    for item in combined
                ]

                self.curves[
                    metric
                ].setData(
                    times,
                    values
                )

            metric_values[metric] = values

            all_times.extend(
                times
            )

        if all_times:

            self.graph.setXRange(
                min(all_times),
                max(all_times),
                padding=0.02
            )

        else:

            self.graph.enableAutoRange(
                axis="x"
            )

        # KPI follows the first selected metric.
        primary_metric = (
            selected_metrics[0]
        )

        self.update_kpis(
            metric_values.get(
                primary_metric,
                []
            )
        )

    # ==========================================
    # UPDATE KPIs
    # ==========================================

    def update_kpis(
        self,
        values
    ):

        if not values:

            self.average_card[1].setText(
                "0.0 %"
            )

            self.minimum_card[1].setText(
                "0.0 %"
            )

            self.maximum_card[1].setText(
                "0.0 %"
            )

            self.samples_card[1].setText(
                "0"
            )

            return

        average = (
            sum(values)
            / len(values)
        )

        minimum = min(
            values
        )

        maximum = max(
            values
        )

        samples = len(
            values
        )

        self.average_card[1].setText(
            f"{average:.1f} %"
        )

        self.minimum_card[1].setText(
            f"{minimum:.1f} %"
        )

        self.maximum_card[1].setText(
            f"{maximum:.1f} %"
        )

        self.samples_card[1].setText(
            str(samples)
        )

    # ==========================================
    # REFRESH
    # ==========================================

    def refresh(self):

        self.update_names()

        self.load_data()
