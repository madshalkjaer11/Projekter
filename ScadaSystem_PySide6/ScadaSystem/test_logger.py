from LOGIC.DataLogger import DataLogger


logger = DataLogger()


logger.log(
    unit="UNIT 1",
    oee=84.2,
    availability=92.1,
    performance=89.3,
    quality=96.8,
    packml="Execute"
)


logger.log(
    unit="UNIT 2",
    oee=91.4,
    availability=95.2,
    performance=93.1,
    quality=97.8,
    packml="Execute"
)


logger.log(
    em="EM 01",
    oee=82.3,
    availability=90.1,
    performance=87.4,
    quality=94.2,
    packml="Idle"
)


print("Data logged successfully.")