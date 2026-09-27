from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QStackedWidget,
    QFrame,
    QLabel
)

from PySide6.QtCore import QTimer

from GUI.Overview import Overview
from GUI.Trends import Trends
from GUI.OEE import OEE
from GUI.Settings import Settings
from GUI.Units import Units
from GUI.EMs import EMs
from GUI.History import History


class main_window(QMainWindow):

    def __init__(self, config, data_model):

        super().__init__()

        self.config = config
        self.data_model = data_model

        # ==========================================
        # DATA UPDATE TIMER
        # ==========================================

        self.data_timer = QTimer(self)

        self.data_timer.timeout.connect(
            self.update_data
        )

        self.data_timer.start(1000)

        self.setWindowTitle("SCADA")
        self.resize(1200, 700)

        # ==========================================
        # Central widget
        # ==========================================

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        central_widget.setLayout(main_layout)

        # ==========================================
        # Topbar
        # ==========================================

        topbar = self.create_topbar()
        main_layout.addWidget(topbar)

        # ==========================================
        # Content
        # ==========================================

        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)

        # ==========================================
        # Sidebar
        # ==========================================

        sidebar_frame = QFrame()
        sidebar_frame.setFixedWidth(180)

        sidebar = QVBoxLayout()
        sidebar_frame.setLayout(sidebar)

        sidebar.setContentsMargins(10, 10, 10, 10)
        sidebar.setSpacing(8)

        overview_button = QPushButton("Overview")
        units_button = QPushButton("Units")
        ems_button = QPushButton("EMs")
        trends_button = QPushButton("Trends")
        oee_button = QPushButton("OEE")
        history_button = QPushButton("History")
        settings_button = QPushButton("Settings")

        for button in [
            overview_button,
            units_button,
            ems_button,
            trends_button,
            oee_button,
            history_button,
            settings_button
        ]:
            button.setFixedHeight(40)

        sidebar.addWidget(overview_button)
        sidebar.addWidget(units_button)
        sidebar.addWidget(ems_button)
        sidebar.addWidget(trends_button)
        sidebar.addWidget(oee_button)
        sidebar.addWidget(history_button)
        sidebar.addWidget(settings_button)

        sidebar.addStretch()

        # ==========================================
        # Pages
        # ==========================================

        self.pages = QStackedWidget()

        self.overview_page = Overview()
        self.units_page = Units(self.config, self.data_model)
        self.ems_page = EMs(self.config, self.data_model)
        self.trends_page = Trends(self.config, self.data_model)
        self.oee_page = OEE(self.config, self.data_model)
        self.history_page = History(self.config)
        self.settings_page = Settings(self.config)

        self.pages.addWidget(self.overview_page)     # 0
        self.pages.addWidget(self.units_page)        # 1
        self.pages.addWidget(self.ems_page)          # 2
        self.pages.addWidget(self.trends_page)       # 3
        self.pages.addWidget(self.oee_page)          # 4
        self.pages.addWidget(self.history_page)      # 5
        self.pages.addWidget(self.settings_page)     # 6

        self.settings_page.settings_saved.connect(
            self.units_page.refresh
        )

        self.settings_page.settings_saved.connect(
            self.data_model.reload_config
        )

        self.settings_page.settings_saved.connect(
            self.ems_page.refresh
        )

        self.settings_page.settings_saved.connect(
            self.oee_page.refresh
        )

        self.settings_page.settings_saved.connect(
            self.trends_page.refresh
        )

        self.settings_page.settings_saved.connect(
            self.history_page.refresh
        )

        # ==========================================
        # Tilføj sidebar + pages
        # ==========================================

        content_layout.addWidget(sidebar_frame)
        content_layout.addWidget(self.pages)

        main_layout.addLayout(content_layout)

        # ==========================================
        # Navigation
        # ==========================================

        overview_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(0)
        )

        units_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(1)
        )

        ems_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(2)
        )

        trends_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(3)
        )

        oee_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(4)
        )

        history_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(5)
        )

        settings_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(6)
        )

    def create_topbar(self):

        topbar = QFrame()
        topbar.setFixedHeight(60)

        layout = QHBoxLayout()
        topbar.setLayout(layout)

        title = QLabel("SCADA SYSTEM")
        layout.addWidget(title)

        layout.addStretch()

        self.plc_status = QLabel("● PLC Disconnected")
        self.plc_status.setStyleSheet("color: #d9534f;")
        layout.addWidget(self.plc_status)

        time = QLabel("15:42:31")
        layout.addWidget(time)

        return topbar


    def set_plc_worker(self, worker, thread):
        self.plc_worker = worker
        self.plc_thread = thread

        worker.status_changed.connect(self.update_plc_status)
        self.settings_page.settings_saved.connect(worker.reload_config)

    def update_plc_status(self, connected, text):
        self.plc_status.setText("● " + text)
        if connected:
            self.plc_status.setStyleSheet("color: #45a85a;")
        else:
            self.plc_status.setStyleSheet("color: #d9534f;")

    def update_data(self):

        self.data_model.update()