from CONFIG.ConfigManager import ConfigManager
from PLC.PLCManager import PLCManager
from LOGIC.DataModel import DataModel


# ==========================================
# CONFIG
# ==========================================

config = ConfigManager()


# ==========================================
# PLC MANAGER
# ==========================================

plc = PLCManager(config)


# ==========================================
# DATA MODEL
# ==========================================

data_model = DataModel(
    config,
    plc
)


# ==========================================
# SIMULATION
# ==========================================

print("==========================================")
print("DATA MODEL TEST")
print("==========================================")

print("\nSimulation:", data_model.simulation)


# ==========================================
# UPDATE
# ==========================================

data_model.update()


# ==========================================
# UNITS
# ==========================================

print("\n--- UNITS ---")

for name, data in data_model.get_units().items():

    print(name)
    print(data)


# ==========================================
# EMS
# ==========================================

print("\n--- EMS ---")

for name, data in data_model.get_ems().items():

    print(name)
    print(data)


# ==========================================
# SINGLE VALUE
# ==========================================

print("\n--- SINGLE VALUE ---")

unit1 = data_model.get_unit("UNIT 1")

print(
    "UNIT 1 OEE:",
    unit1["OEE"]
)


print("\n==========================================")
print("TEST FINISHED")
print("==========================================")