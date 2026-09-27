from PySide6.QtCore import QObject, Signal, Slot
import time

from PLC.PLCManager import PLCManager


class PLCWorker(QObject):
    """
    Runs all blocking PLC communication outside the Qt GUI thread.

    The GUI never calls snap7 connect/db_read directly. The worker polls the
    PLC and sends a complete snapshot back through Qt signals.
    """

    data_ready = Signal(dict)
    status_changed = Signal(bool, str)
    error = Signal(str)
    finished = Signal()

    def __init__(self, config, poll_interval=1.0, reconnect_interval=5.0):
        super().__init__()
        self.config = config
        self.poll_interval = poll_interval
        self.reconnect_interval = reconnect_interval
        self.running = False
        self._force_disconnect = False
        self._last_error = ""
        self._last_status = None
        self._next_connect = 0.0
        self.plc = None

    @Slot()
    def run(self):
        """Main worker loop. This method runs in the PLC QThread."""
        self.running = True
        self.plc = PLCManager(self.config)
        self._next_connect = 0.0

        while self.running:
            now = time.monotonic()

            try:
                if self._force_disconnect:
                    self.plc.disconnect()
                    self._force_disconnect = False
                    self._set_status(False, "PLC Disconnected")
                    self._next_connect = now + self.reconnect_interval

                if not self.plc.is_connected():
                    if now >= self._next_connect:
                        if self.plc.connect():
                            self._set_status(True, "PLC Connected")
                        else:
                            self._set_status(False, "PLC Disconnected")
                            self._next_connect = time.monotonic() + self.reconnect_interval
                    self._sleep(self.poll_interval)
                    continue

                snapshot = self._read_all()

                if snapshot is None:
                    self._set_status(False, "PLC Disconnected")
                    self._next_connect = time.monotonic() + self.reconnect_interval
                else:
                    self._set_status(True, "PLC Connected")
                    self.data_ready.emit(snapshot)

            except Exception as exc:
                self._set_status(False, "PLC Disconnected")
                message = str(exc)
                if message != self._last_error:
                    self._last_error = message
                    self.error.emit(message)
                self._next_connect = time.monotonic() + self.reconnect_interval

            self._sleep(self.poll_interval)

        try:
            if self.plc is not None:
                self.plc.disconnect()
        except Exception:
            pass

        self.finished.emit()

    def _sleep(self, seconds):
        # Small sleeps keep shutdown responsive without touching the GUI thread.
        end = time.monotonic() + seconds
        while self.running and time.monotonic() < end:
            time.sleep(min(0.05, end - time.monotonic()))

    def _set_status(self, connected, text):
        if self._last_status == connected:
            return
        self._last_status = connected
        self.status_changed.emit(connected, text)

    def _read_all(self):
        """Read all configured Unit/EM values in the worker thread."""
        snapshot = {"units": {}, "ems": {}}

        for name in self.config.config.get("units", []):
            unit = name
            values = {
                "OEE": self.plc.get_unit_oee(unit["name"]),
                "Availability": self.plc.get_unit_availability(unit["name"]),
                "Performance": self.plc.get_unit_performance(unit["name"]),
                "Quality": self.plc.get_unit_quality(unit["name"]),
                "PackML": self.plc.get_unit_packml_state(unit["name"]),
            }
            snapshot["units"][unit["name"]] = values

            if any(value is None for value in values.values()):
                # The manager/reader marks the connection failed on a DB read
                # error. Stop this cycle and reconnect later.
                if not self.plc.is_connected():
                    return None

        for name in self.config.config.get("ems", []):
            em = name
            values = {
                "OEE": self.plc.get_em_oee(em["name"]),
                "Availability": self.plc.get_em_availability(em["name"]),
                "Performance": self.plc.get_em_performance(em["name"]),
                "Quality": self.plc.get_em_quality(em["name"]),
                "PackML": self.plc.get_em_packml_state(em["name"]),
            }
            snapshot["ems"][em["name"]] = values

            if any(value is None for value in values.values()):
                if not self.plc.is_connected():
                    return None

        return snapshot

    @Slot()
    def stop(self):
        self.running = False

    @Slot()
    def disconnect(self):
        self._force_disconnect = True

    @Slot()
    def reload_config(self):
        """Reconnect using newly saved PLC/IP/rack/slot and current DB map."""
        if self.plc is None:
            return
        try:
            self.plc.disconnect()
        except Exception:
            pass
        self.plc.reader.load_config()
        self._next_connect = 0.0
        self._last_status = None
