from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea
)

from PySide6.QtCore import Qt

from GUI.UnitCard import UnitCard


class Units(QWidget):

    def __init__(self, config, data_model):
        super().__init__()

        self.config = config
        self.data_model = data_model

        self.unit_cards = {}

        self.setup_ui()

        # Lyt efter nye data fra DataModel
        self.data_model.data_updated.connect(
            self.update_data
        )

    def setup_ui(self):

        # ==========================================
        # SCROLL AREA
        # ==========================================

        scroll = QScrollArea()

        scroll.setWidgetResizable(True)

        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        # ==========================================
        # CONTENT
        # ==========================================

        self.content = QWidget()

        self.layout = QVBoxLayout()

        self.layout.setContentsMargins(
            10,
            10,
            10,
            10
        )

        self.layout.setSpacing(10)

        self.content.setLayout(self.layout)

        # ==========================================
        # SCROLL CONTENT
        # ==========================================

        scroll.setWidget(self.content)

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

        main_layout.addWidget(scroll)

        self.setLayout(main_layout)

        # ==========================================
        # CREATE UNITS
        # ==========================================

        self.refresh()

    # ==============================================
    # REFRESH UNITS
    # ==============================================

    def refresh(self):

        # Fjern eksisterende UnitCards
        while self.layout.count():

            item = self.layout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

        self.unit_cards = {}

        # Hent Units fra config
        units = self.config.config.get(
            "units",
            []
        )

        # Opret en UnitCard for hver Unit
        for unit in units:

            name = unit["name"]

            data = self.data_model.get_unit(name)

            if data is None:
                continue

            unit_card = UnitCard(
                name,
                data["OEE"],
                data["Availability"],
                data["Performance"],
                data["Quality"]
            )

            self.unit_cards[name] = unit_card

            self.layout.addWidget(unit_card)

        # Sørg for at cards ligger øverst
        self.layout.addStretch()

    # ==============================================
    # UPDATE DATA
    # ==============================================

    def update_data(self):

        for name, card in self.unit_cards.items():

            data = self.data_model.get_unit(name)

            if data is None:
                continue

            card.update_data(
                data["OEE"],
                data["Availability"],
                data["Performance"],
                data["Quality"],
                data["PackML"],
                data["PackMLTimes"]
            )