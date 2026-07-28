from flask import Flask, render_template, jsonify, request, send_file
from plc_reader import PLCReader
from datetime import datetime

import threading
import time
import csv
import random
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

with open(CONFIG_PATH, "r") as file:
    CONFIG = json.load(file)

if "units" not in CONFIG:
    legacy_unit = CONFIG.pop("unit", None)
    CONFIG["units"] = []

    if legacy_unit:
        CONFIG["units"].append({
            "name": "Unit01",
            "state_db": legacy_unit["db_number"],
            "state_byte": legacy_unit["start_byte"]
        })


app = Flask(__name__)

system_start_time = time.time()

SIMULATION_MODE = True

plc_connected = False

# --------------------------------------------------
# PLC
# --------------------------------------------------

plc = PLCReader(
    ip=CONFIG["plc"]["ip"],
    rack=CONFIG["plc"]["rack"],
    slot=CONFIG["plc"]["slot"]
)

if not SIMULATION_MODE:
    plc.connect()


# --------------------------------------------------
# PACKML STATES
# --------------------------------------------------

PACKML_STATES = {

    0: "Idle",
    1: "Starting",
    2: "Execute",
    3: "Holding",
    4: "Held",
    5: "Un-holding",
    6: "Suspending",
    7: "Suspended",
    8: "Un-suspending",
    9: "Stopping",
    10: "Stopped",
    11: "Resetting"
}


# --------------------------------------------------
# STATUSER
# --------------------------------------------------

STATUS_TEXT = {

    0: "Standby",
    1: "Gennemskyl 1",
    2: "Gennemskyl 2",
    3: "Gennemskyl 3",
    4: "Regulering",

    5: "Station stopped",
    6: "Standby",
    7: "Ready",
    8: "Running",
    9: "Checking height",
    10: "Going to storage",
    11: "Discarding",
    12: "Stopped",

    13: "Standby",
    14: "Resetting",
    15: "Ready",
    16: "Checking color",
    17: "Grabbing block",
    18: "Placing block",
    19: "Delivering block",
    20: "Starting order",

    21: "Standby",
    22: "Receiving from storage",
    23: "Transfer",
    24: "Checking color",
    25: "Order to chute 1",
    26: "Order to chute 2",
    27: "Handling wrong delivery",
    28: "Station stopped"
}


# --------------------------------------------------
# GLOBALE DATA
# --------------------------------------------------

latest_data = []

latest_unit_data = []

# Historik gemmes i backend
state_history = [
    {}
    for _ in CONFIG["stations"]
]

unit_history = [
    {}
    for _ in CONFIG["units"]
]


def calculate_oee(history):

    total_time = sum(history.values())

    if total_time <= 0:
        return {
            "availability": 0,
            "performance": 100,
            "quality": 100,
            "oee": 0
        }

    availability = (
        history.get("Execute", 0)
        / total_time
        * 100
    )

    return {
        "availability": round(availability, 1),
        "performance": 100,
        "quality": 100,
        "oee": round(availability, 1)
    }


# --------------------------------------------------
# CSV SETUP
# --------------------------------------------------

csv_file = "packml_log.csv"

try:

    with open(csv_file, "x", newline="") as file:

        writer = csv.writer(file)

        headers = ["Timestamp"]

        for station in CONFIG["stations"]:
            headers.append(station["name"])

        for unit in CONFIG["units"]:
            headers.append(unit["name"])

        writer.writerow(headers)

except FileExistsError:
    pass


# --------------------------------------------------
# PLC LOOP
# --------------------------------------------------

def plc_loop():

    global latest_data
    global latest_unit_data
    global state_history
    global unit_history
    global plc_connected

    last_csv_write = 0
    last_update = time.time()


    while True:

        now = time.time()
        delta_time = round(now - last_update, 2)
        last_update = now


        try:

            # --------------------------------------------------
            # SIMULATION
            # --------------------------------------------------

            if SIMULATION_MODE:

                plc_connected = True

                unit_states = [
                    random.randint(0, 11)
                    for _ in CONFIG["units"]
                ]

                states = [
                    random.randint(0, 11)
                    for _ in CONFIG["stations"]
                ]


                statuses = [
                    random.randint(0, 28)
                    for _ in CONFIG["stations"]
                ]


            # --------------------------------------------------
            # RIGTIG PLC
            # --------------------------------------------------

            else:

                plc_connected = plc.get_connected()

                # UNITS
                unit_states = []

                for unit in CONFIG["units"]:

                    unit_state = plc.read_packml_state(
                        db_number=unit["state_db"],
                        start_byte=unit["state_byte"]
                    )

                    unit_states.append(unit_state)


                # EM STATES
                states = []

                for station in CONFIG["stations"]:

                    state = plc.read_packml_state(
                        db_number=station["state_db"],
                        start_byte=station["state_byte"]
                    )

                    states.append(state)


                # STATUS
                statuses = []

                for station in CONFIG["stations"]:

                    status = plc.read_packml_state(
                        db_number=station["status_db"],
                        start_byte=station["status_byte"]
                    )

                    statuses.append(status)


            # --------------------------------------------------
            # UNIT HISTORIK
            # --------------------------------------------------

            latest_unit_data = []

            for i, unit_state in enumerate(unit_states):

                unit_state_name = PACKML_STATES.get(
                    unit_state,
                    "Unknown"
                )


                if unit_state_name not in unit_history[i]:

                    unit_history[i][unit_state_name] = 0


                unit_history[i][unit_state_name] += delta_time


                latest_unit_data.append({

                    "name": CONFIG["units"][i]["name"],

                    "state": unit_state,

                    "state_name": unit_state_name,

                    "history": unit_history[i],

                    "oee": calculate_oee(unit_history[i])
                })


            # --------------------------------------------------
            # EM DATA
            # --------------------------------------------------

            latest_data = []

            for i, state in enumerate(states):

                state_name = PACKML_STATES.get(
                    state,
                    "Unknown"
                )


                if state_name not in state_history[i]:

                    state_history[i][state_name] = 0


                state_history[i][state_name] += delta_time


                latest_data.append({

                    "plc": f"EM0{i+1}",

                    "state": state,

                    "state_name": state_name,

                    "status": statuses[i],

                    "status_text": STATUS_TEXT.get(
                        statuses[i],
                        "Ukendt status"
                    ),

                    "history": state_history[i],

                    "oee": calculate_oee(state_history[i])
                })


            # --------------------------------------------------
            # CSV LOGGING (hver 2 sek)
            # --------------------------------------------------

            current_time = time.time()


            if current_time - last_csv_write >= 2:

                timestamp = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )


                with open(csv_file, "a", newline="") as file:

                    writer = csv.writer(file)

                    writer.writerow(
                        [timestamp] +
                        states +
                        unit_states)


                print(f"Logged: {timestamp}")


                last_csv_write = current_time


        except Exception as e:

            plc_connected = False

            print("PLC fejl:", e)


        time.sleep(1)


# --------------------------------------------------
# START THREAD
# --------------------------------------------------

thread = threading.Thread(target=plc_loop)

thread.daemon = True

thread.start()


# --------------------------------------------------
# ROUTES
# --------------------------------------------------

@app.route("/unit")
def unit_page():

    return render_template(
        "unit.html",
        config=CONFIG
    )


@app.route("/api/packml")
def packml_data():

    return jsonify(latest_data)


@app.route("/api/unit")
def unit_data():

    return jsonify(latest_unit_data)

@app.route("/api/runtime")
def runtime_data():

    runtime_seconds = int(
        time.time() - system_start_time
    )

    return jsonify({

        "runtime": runtime_seconds
    })

@app.route("/api/plc_status")
def plc_status():

    return jsonify({

        "connected": plc_connected
    })

@app.route("/api/state_colors")
def state_colors():

    return jsonify(
        CONFIG["state_colors"]
    )

@app.route("/download/packml-log")
def download_packml_log():

    return send_file(
        os.path.abspath(csv_file),
        as_attachment=True,
        download_name="packml_log.csv"
    )

@app.route("/settings")
def settings():

    return render_template(
        "Settings.html",
        config=CONFIG
    )

@app.route("/")
def index():
    return render_template(
        "index.html",
        config=CONFIG
    )

@app.route("/api/settings", methods=["POST"])
def save_settings():

    global CONFIG
    global plc

    CONFIG = request.json

    global state_history
    global unit_history

    state_history = [
        {}
        for _ in CONFIG["stations"]
    ]

    unit_history = [
        {}
        for _ in CONFIG["units"]
    ]

    with open(CONFIG_PATH, "w") as file:
        json.dump(CONFIG, file, indent=4)

    if not SIMULATION_MODE:    
        plc.disconnect()

    plc = PLCReader(
        ip=CONFIG["plc"]["ip"],
        rack=CONFIG["plc"]["rack"],
        slot=CONFIG["plc"]["slot"]
    )

    print("Nye indstillinger gemt")
    print(f"IP: {plc.ip}, Rack: {plc.rack}, Slot: {plc.slot}")

    if not SIMULATION_MODE:
        try:
            plc.connect()

            if plc.get_connected():
                print(f"PLC forbundet til ip: {plc.ip}, rack: {plc.rack}, slot: {plc.slot}")
        except Exception as e:
            print("Fejl ved forbindelse til PLC med nye indstillinger:", e)


    return {"success": True}

# --------------------------------------------------
# START SERVER
# --------------------------------------------------

if __name__ == "__main__":

    app.run(debug=False)
