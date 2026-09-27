from CONFIG.ConfigManager import ConfigManager
from PLC.PLCManager import PLCManager


# ==========================================
# LOAD CONFIG
# ==========================================

config = ConfigManager()

print("==========================================")
print("PLC TEST")
print("==========================================")


# ==========================================
# CREATE PLC MANAGER
# ==========================================

plc = PLCManager(config)

print("\nPLCManager created")


# ==========================================
# PLC CONFIG
# ==========================================

print("\n--- PLC CONFIG ---")

print("IP:", config.get("plc", "ip"))
print("Rack:", config.get("plc", "rack"))
print("Slot:", config.get("plc", "slot"))


# ==========================================
# UNIT CONFIG
# ==========================================

print("\n--- UNIT CONFIG ---")

unit1 = plc.get_unit_config("UNIT 1")
unit2 = plc.get_unit_config("UNIT 2")

print("UNIT 1:")
print(unit1)

print("\nUNIT 2:")
print(unit2)


# ==========================================
# EM CONFIG
# ==========================================

print("\n--- EM CONFIG ---")

em1 = plc.get_em_config("EM 01")
em2 = plc.get_em_config("EM 02")

print("EM 01:")
print(em1)

print("\nEM 02:")
print(em2)


# ==========================================
# TEST INVALID NAME
# ==========================================

print("\n--- INVALID NAME TEST ---")

print(
    "UNIT 99:",
    plc.get_unit_config("UNIT 99")
)

print(
    "EM 99:",
    plc.get_em_config("EM 99")
)


# ==========================================
# PLC CONNECTION
# ==========================================

print("\n--- PLC CONNECTION ---")

print(
    "Connected:",
    plc.is_connected()
)


print("\n==========================================")
print("TEST FINISHED")
print("==========================================")