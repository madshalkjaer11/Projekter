import random
import time

from PySide6.QtCore import QObject, Signal, Slot

from LOGIC.packml import PACKML_STATES
from LOGIC.DataLogger import DataLogger


class DataModel(QObject):

    data_updated = Signal()

    def __init__(self, config, plc_manager=None):
        super().__init__()
        self.config = config
        self.plc = plc_manager
        self.simulation = False
        self.units = {}
        self.ems = {}
        self.last_update_time = time.monotonic()
        self.logger = DataLogger()
        self.log_interval = 2.0
        self.last_log_time = time.monotonic()
        self.create_data()

    def create_data(self):
        self.units = {}
        self.ems = {}
        for unit in self.config.config.get("units", []):
            name = unit["name"]
            self.units[name] = self._empty_data()
        for em in self.config.config.get("ems", []):
            name = em["name"]
            self.ems[name] = self._empty_data()

    def _empty_data(self):
        return {
            "OEE": 0,
            "Availability": 0,
            "Performance": 0,
            "Quality": 0,
            "PackML": 0,
            "PackMLTimes": self.create_packml_times(),
        }

    def create_packml_times(self):
        return {state_name: 0.0 for state_name in PACKML_STATES.values()}

    def update(self):
        """Only handles GUI-side timing/logging. PLC I/O happens in PLCWorker."""
        current_time = time.monotonic()
        delta_time = max(0, current_time - self.last_update_time)
        self.last_update_time = current_time

        if self.simulation:
            self.update_simulation(delta_time)

        self.update_logger(current_time)
        self.data_updated.emit()

    def update_simulation(self, delta_time):
        for collection in (self.units, self.ems):
            for name in collection:
                data = collection[name]
                for metric in ["OEE", "Availability", "Performance", "Quality"]:
                    old_value = data[metric]
                    new_value = random.uniform(70, 95) if old_value == 0 else old_value + random.uniform(-1, 1)
                    data[metric] = max(0, min(100, new_value))
                data["PackML"] = random.choice(list(PACKML_STATES.keys())[1:])
                self.update_packml_time(data, delta_time)

    def update_packml_time(self, data, delta_time):
        state_name = PACKML_STATES.get(data.get("PackML"))
        if state_name is not None:
            data["PackMLTimes"][state_name] += delta_time

    @Slot(dict)
    def apply_plc_data(self, snapshot):
        """Called through a queued Qt signal, therefore in the GUI thread."""
        current_time = time.monotonic()
        delta_time = max(0, current_time - self.last_update_time)
        self.last_update_time = current_time

        self._apply_collection(self.units, snapshot.get("units", {}), delta_time)
        self._apply_collection(self.ems, snapshot.get("ems", {}), delta_time)

        self.data_updated.emit()

    def _apply_collection(self, target, incoming, delta_time):
        for name, values in incoming.items():
            if name not in target:
                continue

            for metric in ["OEE", "Availability", "Performance", "Quality"]:
                value = values.get(metric)
                if value is not None:
                    target[name][metric] = value

            packml = values.get("PackML")
            if packml is not None:
                target[name]["PackML"] = packml
                self.update_packml_time(target[name], delta_time)

    @Slot()
    def reload_config(self):
        """Rebuild data structures immediately after Settings are saved."""
        self.create_data()
        self.last_update_time = time.monotonic()
        self.data_updated.emit()

    def update_logger(self, current_time):
        if current_time - self.last_log_time < self.log_interval:
            return

        for name, data in self.units.items():
            self.logger.log(
                unit=name, em="", oee=data["OEE"],
                availability=data["Availability"], performance=data["Performance"],
                quality=data["Quality"],
                packml=PACKML_STATES.get(data["PackML"], "UNKNOWN")
            )

        for name, data in self.ems.items():
            self.logger.log(
                unit="", em=name, oee=data["OEE"],
                availability=data["Availability"], performance=data["Performance"],
                quality=data["Quality"],
                packml=PACKML_STATES.get(data["PackML"], "UNKNOWN")
            )

        self.last_log_time = current_time

    def get_unit(self, name):
        return self.units.get(name)

    def get_em(self, name):
        return self.ems.get(name)

    def get_units(self):
        return self.units

    def get_ems(self):
        return self.ems
