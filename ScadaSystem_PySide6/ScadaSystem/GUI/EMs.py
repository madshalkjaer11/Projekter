from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea
)

from PySide6.QtCore import Qt

from GUI.EMCard import EMCard


class EMs(QWidget):

    def __init__(
        self,
        config,
        data_model
    ):
        super().__init__()

        self.config = config
        self.data_model = data_model

        self.em_cards = {}

        self.setup_ui()

        # ==========================================
        # DATA MODEL SIGNAL
        # ==========================================

        self.data_model.data_updated.connect(
            self.update_data
        )

    # ==========================================
    # SETUP UI
    # ==========================================

    def setup_ui(self):

        scroll = QScrollArea()

        scroll.setWidgetResizable(
            True
        )

        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        # ======================================
        # CONTENT
        # ======================================

        self.content = QWidget()

        self.layout = QVBoxLayout()

        self.layout.setContentsMargins(
            10,
            10,
            10,
            10
        )

        self.layout.setSpacing(
            10
        )

        self.content.setLayout(
            self.layout
        )

        scroll.setWidget(
            self.content
        )

        # ======================================
        # MAIN LAYOUT
        # ======================================

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

        # ======================================
        # CREATE EM CARDS
        # ======================================

        self.refresh()

    # ==========================================
    # REFRESH
    # ==========================================

    def refresh(self):

        # --------------------------------------
        # REMOVE OLD CARDS
        # --------------------------------------

        while self.layout.count():

            item = self.layout.takeAt(0)

            widget = item.widget()

            if widget is not None:

                widget.deleteLater()

        self.em_cards = {}

        # --------------------------------------
        # GET EMS FROM CONFIG
        # --------------------------------------

        ems = self.config.config.get(
            "ems",
            []
        )

        # --------------------------------------
        # CREATE CARDS
        # --------------------------------------

        for em in ems:

            name = em["name"]

            data = self.data_model.get_em(
                name
            )

            if data is None:

                continue

            em_card = EMCard(
                name,
                data["OEE"],
                data["Availability"],
                data["Performance"],
                data["Quality"]
            )

            self.em_cards[name] = em_card

            self.layout.addWidget(
                em_card
            )

        # --------------------------------------
        # STRETCH
        # --------------------------------------

        self.layout.addStretch()

    # ==========================================
    # UPDATE DATA
    # ==========================================

    def update_data(self):

        for name, card in self.em_cards.items():

            data = self.data_model.get_em(
                name
            )

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