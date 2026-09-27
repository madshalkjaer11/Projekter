from PLC.PLCReader import PLCReader


class PLCManager:

    def __init__(self, config):

        self.config = config

        self.reader = PLCReader(config)

    # ==========================================
    # CONNECTION
    # ==========================================

    def connect(self):

        return self.reader.connect()

    def disconnect(self):

        self.reader.disconnect()

    def is_connected(self):

        return self.reader.is_connected()

    # ==========================================
    # UNIT CONFIG
    # ==========================================

    def get_unit_config(self, unit_name):

        units = self.config.config.get("units", [])

        for unit in units:

            if unit["name"] == unit_name:
                return unit

        return None

    # ==========================================
    # EM CONFIG
    # ==========================================

    def get_em_config(self, em_name):

        ems = self.config.config.get("ems", [])

        for em in ems:

            if em["name"] == em_name:
                return em

        return None

    # ==========================================
    # UNIT DATA
    # ==========================================

    def get_unit_oee(self, unit_name):

        unit = self.get_unit_config(unit_name)

        if unit is None:
            return None

        return self.reader.read_real(
            unit["db"],
            unit["oee"]
        )

    def get_unit_availability(self, unit_name):

        unit = self.get_unit_config(unit_name)

        if unit is None:
            return None

        return self.reader.read_real(
            unit["db"],
            unit["availability"]
        )

    def get_unit_performance(self, unit_name):

        unit = self.get_unit_config(unit_name)

        if unit is None:
            return None

        return self.reader.read_real(
            unit["db"],
            unit["performance"]
        )

    def get_unit_quality(self, unit_name):

        unit = self.get_unit_config(unit_name)

        if unit is None:
            return None

        return self.reader.read_real(
            unit["db"],
            unit["quality"]
        )

    def get_unit_packml_state(self, unit_name):

        unit = self.get_unit_config(unit_name)

        if unit is None:
            return None

        return self.reader.read_int(
            unit["db"],
            unit["packml_state"]
        )

    # ==========================================
    # EM DATA
    # ==========================================

    def get_em_oee(self, em_name):

        em = self.get_em_config(em_name)

        if em is None:
            return None

        return self.reader.read_real(
            em["db"],
            em["oee"]
        )

    def get_em_availability(self, em_name):

        em = self.get_em_config(em_name)

        if em is None:
            return None

        return self.reader.read_real(
            em["db"],
            em["availability"]
        )

    def get_em_performance(self, em_name):

        em = self.get_em_config(em_name)

        if em is None:
            return None

        return self.reader.read_real(
            em["db"],
            em["performance"]
        )

    def get_em_quality(self, em_name):

        em = self.get_em_config(em_name)

        if em is None:
            return None

        return self.reader.read_real(
            em["db"],
            em["quality"]
        )

    def get_em_packml_state(self, em_name):

        em = self.get_em_config(em_name)

        if em is None:
            return None

        return self.reader.read_int(
            em["db"],
            em["packml_state"]
        )