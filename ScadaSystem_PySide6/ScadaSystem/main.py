import sys

from PySide6.QtCore import QThread
from PySide6.QtWidgets import QApplication

from GUI.main_window import main_window
from CONFIG.ConfigManager import ConfigManager
from LOGIC.DataModel import DataModel
from PLC.PLCWorker import PLCWorker


app = QApplication(sys.argv)

config = ConfigManager()
data_model = DataModel(config)

# PLC communication is deliberately kept out of the GUI thread.
plc_thread = QThread()
plc_worker = PLCWorker(config, poll_interval=1.0, reconnect_interval=5.0)
plc_worker.moveToThread(plc_thread)

plc_thread.started.connect(plc_worker.run)
plc_worker.data_ready.connect(data_model.apply_plc_data)

window = main_window(config, data_model)
window.set_plc_worker(plc_worker, plc_thread)
window.show()

plc_thread.start()

exit_code = app.exec()

plc_worker.stop()
plc_thread.quit()
plc_thread.wait(3000)

sys.exit(exit_code)
