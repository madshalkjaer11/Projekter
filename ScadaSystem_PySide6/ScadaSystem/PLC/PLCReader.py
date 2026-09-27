import snap7
from snap7.util import get_bool, get_int, get_real


class PLCReader:

    def __init__(self, config):

        self.config = config

        self.client = snap7.client.Client()

        self.connected = False

        self.ip = ""
        self.rack = 0
        self.slot = 1

        self.load_config()

    # ==========================================
    # LOAD PLC CONFIG
    # ==========================================

    def load_config(self):

        self.ip = self.config.get(
            "plc",
            "ip"
        )

        self.rack = self.config.get(
            "plc",
            "rack"
        )

        self.slot = self.config.get(
            "plc",
            "slot"
        )

    # ==========================================
    # CONNECT
    # ==========================================

    def connect(self):

        try:

            # Hent eventuelle nye PLC-indstillinger
            self.load_config()

            if self.client.get_connected():

                self.connected = True
                return True

            self.client.connect(
                self.ip,
                self.rack,
                self.slot
            )

            self.connected = self.client.get_connected()

            return self.connected

        except Exception as e:

            self.connected = False

            print(
                f"PLC connection error: {e}"
            )

            return False

    # ==========================================
    # DISCONNECT
    # ==========================================

    def disconnect(self):

        try:

            if self.client.get_connected():

                self.client.disconnect()

            self.connected = False

        except Exception as e:

            print(
                f"PLC disconnect error: {e}"
            )

    # ==========================================
    # CONNECTION STATUS
    # ==========================================

    def is_connected(self):

        try:

            self.connected = (
                self.client.get_connected()
            )

        except Exception:

            self.connected = False

        return self.connected

    # ==========================================
    # READ DB
    # ==========================================

    def read_db(
        self,
        db_number,
        start,
        size
    ):

        if not self.is_connected():

            if not self.connect():

                return None

        try:

            data = self.client.db_read(
                db_number,
                start,
                size
            )

            return data

        except Exception as e:

            print(
                f"PLC DB read error: {e}"
            )

            self.connected = False

            return None

    # ==========================================
    # READ REAL
    # ==========================================

    def read_real(
        self,
        db_number,
        byte_offset
    ):

        data = self.read_db(
            db_number,
            byte_offset,
            4
        )

        if data is None:

            return None

        try:

            return get_real(
                data,
                0
            )

        except Exception as e:

            print(
                f"REAL read error: {e}"
            )

            return None

    # ==========================================
    # READ INT
    # ==========================================

    def read_int(
        self,
        db_number,
        byte_offset
    ):

        data = self.read_db(
            db_number,
            byte_offset,
            2
        )

        if data is None:

            return None

        try:

            return get_int(
                data,
                0
            )

        except Exception as e:

            print(
                f"INT read error: {e}"
            )

            return None

    # ==========================================
    # READ BOOL
    # ==========================================

    def read_bool(
        self,
        db_number,
        byte_offset,
        bit_offset
    ):

        data = self.read_db(
            db_number,
            byte_offset,
            1
        )

        if data is None:

            return None

        try:

            return get_bool(
                data,
                0,
                bit_offset
            )

        except Exception as e:

            print(
                f"BOOL read error: {e}"
            )

            return None