from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QFrame
)

from PySide6.QtCore import Qt


class PackMLStateChart(QWidget):

    # States vi ønsker at vise på UnitCard
    DISPLAY_STATES = [
        "IDLE",
        "EXECUTE",
        "SUSPENDED",
        "HELD",
        "COMPLETE",
        "ABORTED",
        "STOPPED"
    ]

    def __init__(self):
        super().__init__()

        self.states = {}
        self.current_state = "UNKNOWN"

        self.state_widgets = {}

        self.setup_ui()

    # ==========================================
    # SETUP UI
    # ==========================================

    def setup_ui(self):

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
            10, 5, 10, 5
        )

        main_layout.setSpacing(6)

        self.setLayout(main_layout)

        # ======================================
        # TITLE
        # ======================================

        title = QLabel(
            "PACKML STATE TIME"
        )

        title.setStyleSheet("""
            font-size: 15px;
            font-weight: bold;
            color: #d5dee8;
        """)

        main_layout.addWidget(title)

        # ======================================
        # TOTAL TIME
        # ======================================

        self.total_label = QLabel(
            "Total time: 00:00:00"
        )

        self.total_label.setStyleSheet("""
            font-size: 11px;
            color: #8fa1b3;
        """)

        main_layout.addWidget(
            self.total_label
        )

        # ======================================
        # COLUMNS
        # ======================================

        columns = QHBoxLayout()

        columns.setSpacing(10)

        main_layout.addLayout(
            columns
        )

        self.left_column = QVBoxLayout()
        self.left_column.setSpacing(6)

        self.right_column = QVBoxLayout()
        self.right_column.setSpacing(6)

        columns.addLayout(
            self.left_column
        )

        columns.addLayout(
            self.right_column
        )

        # ======================================
        # CREATE STATES
        # ======================================

        for i, state in enumerate(
            self.DISPLAY_STATES
        ):

            if i < 4:

                self.add_state(
                    self.left_column,
                    state
                )

            else:

                self.add_state(
                    self.right_column,
                    state
                )

    # ==========================================
    # ADD STATE
    # ==========================================

    def add_state(
        self,
        layout,
        state
    ):

        frame = QFrame()

        frame.setFixedHeight(
            48
        )

        frame.setStyleSheet("""
            QFrame {
                background-color: #1d2b39;
                border: 1px solid #2d4052;
                border-radius: 6px;
            }
        """)

        frame_layout = QVBoxLayout()

        frame_layout.setContentsMargins(
            8, 5, 8, 5
        )

        frame_layout.setSpacing(3)

        frame.setLayout(
            frame_layout
        )

        # ======================================
        # TOP ROW
        # ======================================

        top_row = QHBoxLayout()

        top_row.setSpacing(5)

        # State name
        state_label = QLabel(
            f"● {state}"
        )

        state_label.setStyleSheet("""
            font-size: 10px;
            font-weight: bold;
            color: #b8c4d1;
            border: none;
        """)

        # Time
        time_label = QLabel(
            "00:00:00"
        )

        time_label.setAlignment(
            Qt.AlignRight |
            Qt.AlignVCenter
        )

        time_label.setStyleSheet("""
            font-size: 10px;
            color: #d5dee8;
            border: none;
        """)

        # Percentage
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
            font-size: 9px;
            color: #8fa1b3;
            border: none;
        """)

        top_row.addWidget(
            state_label
        )

        top_row.addStretch()

        top_row.addWidget(
            time_label
        )

        top_row.addWidget(
            percentage_label
        )

        frame_layout.addLayout(
            top_row
        )

        # ======================================
        # PROGRESS BAR
        # ======================================

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

        frame_layout.addWidget(
            progress
        )

        layout.addWidget(
            frame
        )

        # ======================================
        # SAVE REFERENCES
        # ======================================

        self.state_widgets[state] = {
            "frame": frame,
            "label": state_label,
            "time": time_label,
            "percentage": percentage_label,
            "progress": progress
        }

    # ==========================================
    # UPDATE DATA
    # ==========================================

    def update_data(
        self,
        packml_times,
        current_state
    ):

        self.states = packml_times

        self.current_state = (
            current_state
        )

        self.update_values()

    # ==========================================
    # UPDATE VALUES
    # ==========================================

    def update_values(self):

        total_time = 0

        # --------------------------------------
        # TOTAL
        # --------------------------------------

        for state in self.DISPLAY_STATES:

            total_time += self.states.get(
                state,
                0
            )

        self.total_label.setText(
            f"Total time: "
            f"{self.format_time(total_time)}"
        )

        # --------------------------------------
        # STATES
        # --------------------------------------

        for state in self.DISPLAY_STATES:

            seconds = self.states.get(
                state,
                0
            )

            if total_time > 0:

                percentage = (
                    seconds /
                    total_time *
                    100
                )

            else:

                percentage = 0

            widgets = self.state_widgets[
                state
            ]

            # ----------------------------------
            # TIME
            # ----------------------------------

            widgets["time"].setText(
                self.format_time(
                    seconds
                )
            )

            # ----------------------------------
            # PERCENTAGE
            # ----------------------------------

            widgets["percentage"].setText(
                f"{percentage:.1f}%"
            )

            # ----------------------------------
            # PROGRESS
            # ----------------------------------

            widgets["progress"].setValue(
                int(percentage)
            )

            # ----------------------------------
            # CURRENT STATE
            # ----------------------------------

            if state == self.current_state:

                widgets["frame"].setStyleSheet("""
                    QFrame {
                        background-color: #24394a;
                        border: 1px solid #4aaeff;
                        border-radius: 6px;
                    }
                """)

                widgets["label"].setStyleSheet("""
                    font-size: 10px;
                    font-weight: bold;
                    color: #4aaeff;
                    border: none;
                """)

                widgets["progress"].setStyleSheet("""
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

            else:

                widgets["frame"].setStyleSheet("""
                    QFrame {
                        background-color: #1d2b39;
                        border: 1px solid #2d4052;
                        border-radius: 6px;
                    }
                """)

                widgets["label"].setStyleSheet("""
                    font-size: 10px;
                    font-weight: bold;
                    color: #b8c4d1;
                    border: none;
                """)

                widgets["progress"].setStyleSheet("""
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

    # ==========================================
    # FORMAT TIME
    # ==========================================

    def format_time(
        self,
        seconds
    ):

        seconds = int(seconds)

        hours = (
            seconds // 3600
        )

        minutes = (
            (seconds % 3600) // 60
        )

        seconds = (
            seconds % 60
        )

        return (
            f"{hours:02d}:"
            f"{minutes:02d}:"
            f"{seconds:02d}"
        )