# ==========================================
# PACKML STATES
# ==========================================

PACKML_STATES = {
    0: "UNKNOWN",

    1: "STOPPED",
    2: "STARTING",
    3: "IDLE",
    4: "SUSPENDED",
    5: "EXECUTE",
    6: "STOPPING",
    7: "ABORTING",
    8: "ABORTED",
    9: "HOLDING",
    10: "HELD",
    11: "UNHOLDING",
    12: "RESETTING",
    13: "COMPLETE",
    14: "CLEARING",
    15: "SUSPENDING",
    16: "UNSUSPENDING"
}


def get_state_name(state_number):

    return PACKML_STATES.get(
        state_number,
        "UNKNOWN"
    )