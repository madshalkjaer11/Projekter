from threading import Thread
import time
import requests
import webview

from splash import Splash
from app import start_server, stop_server


# -------------------------
# Start Flask
# -------------------------

flask_thread = Thread(
    target=start_server,
    daemon=True
)

flask_thread.start()


# -------------------------
# Splash
# -------------------------

splash = Splash()
splash.show()


# -------------------------
# Vent til Flask svarer
# -------------------------

while True:

    try:

        requests.get(
            "http://127.0.0.1:5000",
            timeout=1
            )

        break

    except:

        time.sleep(0.2)


splash.close()


# -------------------------
# Luk program
# -------------------------

def closed():

    print("Closing PLC SCADA...")

    stop_server()

    print("Done.")


window = webview.create_window(

    "PLC SCADA",

    "http://127.0.0.1:5000",

    width=1400,

    height=900

)

window.events.closed += closed

webview.start()