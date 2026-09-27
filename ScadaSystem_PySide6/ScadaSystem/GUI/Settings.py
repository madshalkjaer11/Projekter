from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QFrame,
    QLineEdit,
    QSpinBox,
    QPushButton,
    QMessageBox,
    QComboBox
)

from PySide6.QtCore import Qt, Signal

class NoWheelSpinBox(QSpinBox):

    def wheelEvent(self, event):
        event.ignore()


class NoWheelComboBox(QComboBox):

    def wheelEvent(self, event):
        event.ignore()


class Settings(QWidget):

    settings_saved = Signal()

    def __init__(self, config):
        super().__init__()

        self.config = config

        self.setup_ui()

    # =====================================================
    # SETUP UI
    # =====================================================

    def setup_ui(self):

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
            15, 15, 15, 15
        )

        main_layout.setSpacing(15)

        self.setLayout(main_layout)

        # =================================================
        # GLOBAL STYLE
        # =================================================

        self.setStyleSheet("""
            QWidget {
                color: #222222;
                font-size: 13px;
            }

            QLabel {
                color: #555555;
            }

            QLineEdit,
            QSpinBox,
            QComboBox {
                background-color: #ffffff;
                color: #222222;
                border: 1px solid #bfc5ca;
                border-radius: 3px;
                padding: 4px 7px;
                min-height: 24px;
            }

            QLineEdit:focus,
            QSpinBox:focus,
            QComboBox:focus {
                border: 1px solid #4aaeff;
            }

            QComboBox {
                background-color: #ffffff;
                color: #222222;
                border: 1px solid #bfc5ca;
                border-radius: 3px;
                padding-left: 8px;
                padding-right: 5px;
                min-height: 24px;
            }

            QComboBox:hover {
                border: 1px solid #9da6ad;
            }

            QComboBox:focus {
                border: 1px solid #4aaeff;
            }

            QComboBox::drop-down {
                width: 28px;
                background-color: #e9e9e9;
                border-left: 1px solid #c5c5c5;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }

            QPushButton {
                background-color: #e9e9e9;
                color: #222222;
                border: 1px solid #bfc5ca;
                border-radius: 3px;
                padding: 6px 12px;
            }

            QPushButton:hover {
                background-color: #dedede;
            }

            QPushButton:pressed {
                background-color: #d2d2d2;
            }
        """)

        # =================================================
        # TITLE
        # =================================================

        title = QLabel("SETTINGS")

        title.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: bold;
                color: #222222;
            }
        """)

        main_layout.addWidget(title)

        # =================================================
        # PLC SETTINGS
        # =================================================

        plc_frame = self.create_card()

        plc_layout = QHBoxLayout()

        plc_layout.setContentsMargins(
            15, 10, 15, 10
        )

        plc_layout.setSpacing(10)

        plc_frame.setLayout(plc_layout)

        # PLC title

        plc_title = QLabel(
            "PLC SETTINGS"
        )

        plc_title.setStyleSheet("""
            QLabel {
                font-size: 15px;
                font-weight: bold;
                color: #222222;
            }
        """)

        plc_layout.addWidget(
            plc_title
        )

        # IP label

        ip_label = QLabel(
            "IP Address"
        )

        ip_label.setFixedWidth(
            75
        )

        plc_layout.addWidget(
            ip_label
        )

        # IP input

        self.ip_input = QLineEdit()

        self.ip_input.setFixedWidth(
            160
        )

        self.ip_input.setText(
            self.config.get(
                "plc",
                "ip"
            )
        )

        plc_layout.addWidget(
            self.ip_input
        )

        # Rack

        rack_label = QLabel(
            "Rack"
        )

        plc_layout.addWidget(
            rack_label
        )

        self.rack_input = NoWheelSpinBox()

        self.rack_input.setRange(
            0, 10
        )

        self.rack_input.setFixedWidth(
            70
        )

        self.rack_input.setValue(
            self.config.get(
                "plc",
                "rack"
            )
        )

        plc_layout.addWidget(
            self.rack_input
        )

        # Slot

        slot_label = QLabel(
            "Slot"
        )

        plc_layout.addWidget(
            slot_label
        )

        self.slot_input = NoWheelSpinBox()

        self.slot_input.setRange(
            0, 10
        )

        self.slot_input.setFixedWidth(
            70
        )

        self.slot_input.setValue(
            self.config.get(
                "plc",
                "slot"
            )
        )

        plc_layout.addWidget(
            self.slot_input
        )

        plc_layout.addStretch()

        main_layout.addWidget(
            plc_frame
        )

        # =================================================
        # UNIT / EM CONTAINER
        # =================================================

        machine_layout = QHBoxLayout()

        machine_layout.setSpacing(
            15
        )

        main_layout.addLayout(
            machine_layout
        )

        # =================================================
        # UNIT SETTINGS
        # =================================================

        unit_frame = self.create_card()

        unit_frame.setMinimumHeight(
            380
        )

        unit_layout = QVBoxLayout()

        unit_layout.setContentsMargins(
            15, 14, 15, 15
        )

        unit_layout.setSpacing(
            10
        )

        unit_frame.setLayout(
            unit_layout
        )

        machine_layout.addWidget(
            unit_frame
        )

        # Unit title

        unit_title = QLabel(
            "UNIT SETTINGS"
        )

        unit_title.setStyleSheet("""
            QLabel {
                font-size: 15px;
                font-weight: bold;
                color: #222222;
            }
        """)

        unit_layout.addWidget(
            unit_title
        )

        # Unit settings grid

        unit_grid = QGridLayout()

        unit_grid.setHorizontalSpacing(
            10
        )

        unit_grid.setVerticalSpacing(
            8
        )

        unit_layout.addLayout(
            unit_grid
        )

        # Number of units

        unit_grid.addWidget(
            self.create_label(
                "Number of Units"
            ),
            0,
            0
        )

        self.unit_count = NoWheelSpinBox()

        self.unit_count.setRange(
            1, 50
        )

        self.unit_count.setFixedWidth(
            100
        )

        self.unit_count.setValue(
            len(
                self.config.config["units"]
            )
        )

        unit_grid.addWidget(
            self.unit_count,
            0,
            1
        )

        # Configure Unit

        unit_grid.addWidget(
            self.create_label(
                "Configure Unit"
            ),
            1,
            0
        )

        self.unit_selector = NoWheelComboBox()

        self.unit_selector.setFixedWidth(
            180
        )

        unit_grid.addWidget(
            self.unit_selector,
            1,
            1
        )

        # Unit fields

        self.unit_fields = {}

        self.create_machine_fields(
            unit_grid,
            self.unit_fields,
            2
        )

        # =================================================
        # EM SETTINGS
        # =================================================

        em_frame = self.create_card()

        em_frame.setMinimumHeight(
            380
        )

        em_layout = QVBoxLayout()

        em_layout.setContentsMargins(
            15, 14, 15, 15
        )

        em_layout.setSpacing(
            10
        )

        em_frame.setLayout(
            em_layout
        )

        machine_layout.addWidget(
            em_frame
        )

        # EM title

        em_title = QLabel(
            "EM SETTINGS"
        )

        em_title.setStyleSheet("""
            QLabel {
                font-size: 15px;
                font-weight: bold;
                color: #222222;
            }
        """)

        em_layout.addWidget(
            em_title
        )

        # EM settings grid

        em_grid = QGridLayout()

        em_grid.setHorizontalSpacing(
            10
        )

        em_grid.setVerticalSpacing(
            8
        )

        em_layout.addLayout(
            em_grid
        )

        # Number of EMs

        em_grid.addWidget(
            self.create_label(
                "Number of EMs"
            ),
            0,
            0
        )

        self.em_count = NoWheelSpinBox()

        self.em_count.setRange(
            1, 100
        )

        self.em_count.setFixedWidth(
            100
        )

        self.em_count.setValue(
            len(
                self.config.config["ems"]
            )
        )

        em_grid.addWidget(
            self.em_count,
            0,
            1
        )

        # Configure EM

        em_grid.addWidget(
            self.create_label(
                "Configure EM"
            ),
            1,
            0
        )

        self.em_selector = NoWheelComboBox()

        self.em_selector.setFixedWidth(
            180
        )

        em_grid.addWidget(
            self.em_selector,
            1,
            1
        )

        # EM fields

        self.em_fields = {}

        self.create_machine_fields(
            em_grid,
            self.em_fields,
            2
        )

        # =================================================
        # SIGNALS
        # =================================================

        self.unit_selector.currentIndexChanged.connect(
            self.load_selected_unit
        )

        self.em_selector.currentIndexChanged.connect(
            self.load_selected_em
        )

        self.unit_count.valueChanged.connect(
            self.update_unit_selector
        )

        self.em_count.valueChanged.connect(
            self.update_em_selector
        )

        # =================================================
        # INITIALIZE
        # =================================================

        self.update_unit_selector()
        self.update_em_selector()

        # =================================================
        # SAVE
        # =================================================

        save_button = QPushButton(
            "SAVE SETTINGS"
        )

        save_button.setFixedHeight(
            40
        )

        save_button.setStyleSheet("""
            QPushButton {
                background-color: #4aaeff;
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 13px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #369cf0;
            }

            QPushButton:pressed {
                background-color: #258bdc;
            }
        """)

        save_button.clicked.connect(
            self.save_settings
        )

        main_layout.addWidget(
            save_button
        )

    # =====================================================
    # CREATE CARD
    # =====================================================

    def create_card(self):

        frame = QFrame()

        frame.setStyleSheet("""
            QFrame {
                background-color: #f4f4f4;
                border: 1px solid #bfc5ca;
                border-radius: 2px;
            }
        """)

        return frame

    # =====================================================
    # CREATE LABEL
    # =====================================================

    def create_label(
        self,
        text
    ):

        label = QLabel(text)

        label.setFixedWidth(
            115
        )

        label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: #555555;
                background: transparent;
                border: none;
            }
        """)

        return label

    # =====================================================
    # CREATE MACHINE FIELDS
    # =====================================================

    def create_machine_fields(
        self,
        grid,
        fields,
        start_row
    ):

        definitions = [
            ("name", "Name", "text"),
            ("db", "DB", "number"),
            ("packml_state", "PackML State", "number"),
            ("oee", "OEE", "number"),
            ("availability", "Availability", "number"),
            ("performance", "Performance", "number"),
            ("quality", "Quality", "number")
        ]

        for row, (
            key,
            label_text,
            field_type
        ) in enumerate(
            definitions,
            start=start_row
        ):

            label = self.create_label(
                label_text
            )

            grid.addWidget(
                label,
                row,
                0
            )

            if field_type == "text":

                widget = QLineEdit()

                widget.setFixedWidth(
                    180
                )

            else:

                widget = NoWheelSpinBox()

                widget.setRange(
                    0,
                    10000
                )

                widget.setFixedWidth(
                    100
                )

            grid.addWidget(
                widget,
                row,
                1
            )

            fields[key] = widget

        # Sørger for at indholdet
        # bliver øverst i kortet.

        grid.setRowStretch(
            start_row + len(definitions),
            1
        )

    # =====================================================
    # DEFAULT UNIT
    # =====================================================

    def create_default_unit(
        self,
        index
    ):

        return {
            "name": f"UNIT {index + 1}",
            "db": 20 + index,
            "packml_state": 4,
            "oee": 6,
            "availability": 10,
            "performance": 14,
            "quality": 18
        }

    # =====================================================
    # DEFAULT EM
    # =====================================================

    def create_default_em(
        self,
        index
    ):

        return {
            "name": f"EM {index + 1:02d}",
            "db": 30 + index,
            "packml_state": 4,
            "oee": 6,
            "availability": 10,
            "performance": 14,
            "quality": 18
        }

    # =====================================================
    # ENSURE UNIT COUNT
    # =====================================================

    def ensure_unit_count(
        self,
        count
    ):

        while len(
            self.config.config["units"]
        ) < count:

            index = len(
                self.config.config["units"]
            )

            self.config.config[
                "units"
            ].append(
                self.create_default_unit(
                    index
                )
            )

    # =====================================================
    # ENSURE EM COUNT
    # =====================================================

    def ensure_em_count(
        self,
        count
    ):

        while len(
            self.config.config["ems"]
        ) < count:

            index = len(
                self.config.config["ems"]
            )

            self.config.config[
                "ems"
            ].append(
                self.create_default_em(
                    index
                )
            )

    # =====================================================
    # UPDATE UNIT SELECTOR
    # =====================================================

    def update_unit_selector(self):

        count = self.unit_count.value()

        self.ensure_unit_count(
            count
        )

        current_index = (
            self.unit_selector.currentIndex()
        )

        self.unit_selector.blockSignals(
            True
        )

        self.unit_selector.clear()

        for index in range(count):

            name = self.config.config[
                "units"
            ][index]["name"]

            self.unit_selector.addItem(
                name
            )

        if count > 0:

            if current_index < 0:
                current_index = 0

            if current_index >= count:
                current_index = count - 1

            self.unit_selector.setCurrentIndex(
                current_index
            )

        self.unit_selector.blockSignals(
            False
        )

        self.load_selected_unit()

    # =====================================================
    # UPDATE EM SELECTOR
    # =====================================================

    def update_em_selector(self):

        count = self.em_count.value()

        self.ensure_em_count(
            count
        )

        current_index = (
            self.em_selector.currentIndex()
        )

        self.em_selector.blockSignals(
            True
        )

        self.em_selector.clear()

        for index in range(count):

            name = self.config.config[
                "ems"
            ][index]["name"]

            self.em_selector.addItem(
                name
            )

        if count > 0:

            if current_index < 0:
                current_index = 0

            if current_index >= count:
                current_index = count - 1

            self.em_selector.setCurrentIndex(
                current_index
            )

        self.em_selector.blockSignals(
            False
        )

        self.load_selected_em()

    # =====================================================
    # LOAD SELECTED UNIT
    # =====================================================

    def load_selected_unit(self):

        index = (
            self.unit_selector.currentIndex()
        )

        if index < 0:
            return

        unit = self.config.config[
            "units"
        ][index]

        self.unit_fields[
            "name"
        ].setText(
            unit["name"]
        )

        self.unit_fields[
            "db"
        ].setValue(
            unit["db"]
        )

        self.unit_fields[
            "packml_state"
        ].setValue(
            unit["packml_state"]
        )

        self.unit_fields[
            "oee"
        ].setValue(
            unit["oee"]
        )

        self.unit_fields[
            "availability"
        ].setValue(
            unit.get(
                "availability",
                0
            )
        )

        self.unit_fields[
            "performance"
        ].setValue(
            unit.get(
                "performance",
                0
            )
        )

        self.unit_fields[
            "quality"
        ].setValue(
            unit.get(
                "quality",
                0
            )
        )

    # =====================================================
    # LOAD SELECTED EM
    # =====================================================

    def load_selected_em(self):

        index = (
            self.em_selector.currentIndex()
        )

        if index < 0:
            return

        em = self.config.config[
            "ems"
        ][index]

        self.em_fields[
            "name"
        ].setText(
            em["name"]
        )

        self.em_fields[
            "db"
        ].setValue(
            em["db"]
        )

        self.em_fields[
            "packml_state"
        ].setValue(
            em["packml_state"]
        )

        self.em_fields[
            "oee"
        ].setValue(
            em["oee"]
        )

        self.em_fields[
            "availability"
        ].setValue(
            em.get(
                "availability",
                0
            )
        )

        self.em_fields[
            "performance"
        ].setValue(
            em.get(
                "performance",
                0
            )
        )

        self.em_fields[
            "quality"
        ].setValue(
            em.get(
                "quality",
                0
            )
        )

    # =====================================================
    # SAVE SETTINGS
    # =====================================================

    def save_settings(self):

        # -------------------------------------------------
        # PLC
        # -------------------------------------------------

        self.config.set(
            "plc",
            "ip",
            self.ip_input.text()
        )

        self.config.set(
            "plc",
            "rack",
            self.rack_input.value()
        )

        self.config.set(
            "plc",
            "slot",
            self.slot_input.value()
        )

        # -------------------------------------------------
        # CURRENT UNIT
        # -------------------------------------------------

        unit_index = (
            self.unit_selector.currentIndex()
        )

        if unit_index >= 0:

            self.config.config[
                "units"
            ][unit_index] = {
                "name": self.unit_fields[
                    "name"
                ].text(),

                "db": self.unit_fields[
                    "db"
                ].value(),

                "packml_state": self.unit_fields[
                    "packml_state"
                ].value(),

                "oee": self.unit_fields[
                    "oee"
                ].value(),

                "availability": self.unit_fields[
                    "availability"
                ].value(),

                "performance": self.unit_fields[
                    "performance"
                ].value(),

                "quality": self.unit_fields[
                    "quality"
                ].value()
            }

        # -------------------------------------------------
        # CURRENT EM
        # -------------------------------------------------

        em_index = (
            self.em_selector.currentIndex()
        )

        if em_index >= 0:

            self.config.config[
                "ems"
            ][em_index] = {
                "name": self.em_fields[
                    "name"
                ].text(),

                "db": self.em_fields[
                    "db"
                ].value(),

                "packml_state": self.em_fields[
                    "packml_state"
                ].value(),

                "oee": self.em_fields[
                    "oee"
                ].value(),

                "availability": self.em_fields[
                    "availability"
                ].value(),

                "performance": self.em_fields[
                    "performance"
                ].value(),

                "quality": self.em_fields[
                    "quality"
                ].value()
            }

        # -------------------------------------------------
        # NUMBER OF UNITS
        # -------------------------------------------------

        unit_count = (
            self.unit_count.value()
        )

        self.config.config[
            "units"
        ] = self.config.config[
            "units"
        ][:unit_count]

        # -------------------------------------------------
        # NUMBER OF EMS
        # -------------------------------------------------

        em_count = (
            self.em_count.value()
        )

        self.config.config[
            "ems"
        ] = self.config.config[
            "ems"
        ][:em_count]

        # -------------------------------------------------
        # SAVE
        # -------------------------------------------------

        self.config.save()
        self.settings_saved.emit()

        self.update_unit_selector()
        self.update_em_selector()

        QMessageBox.information(
            self,
            "Settings",
            "Settings saved successfully."
        )