import snap7
from snap7.util import get_int


class PLCReader:
    def __init__(self, ip, rack=0, slot=1):
        self.ip = ip
        self.rack = rack
        self.slot = slot

        self.client = snap7.client.Client()

    def connect(self):
        self.client.connect(self.ip, self.rack, self.slot)

    def disconnect(self):
        self.client.disconnect()

    def read_packml_state(self,db_number, start_byte=0):
        """
        Læser PackML state fra PLC DB.
        State forventes som INT.
        """

        data = self.client.db_read(db_number, start_byte, 2)
        state = get_int(data, 0)

        return state
    
    def get_connected(self):
        return self.client.get_connected()