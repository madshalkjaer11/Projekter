const stateColors = JSON.parse(
    document.getElementById('stateColorsData').textContent
);

// --------------------------------------------------
// PLC STATUS
// --------------------------------------------------

async function updatePLCStatus() {

    try {

        const response =
            await fetch('/api/plc_status');


        const data =
            await response.json();


        const lamp =
            document.getElementById('plcLamp');


        const text =
            document.getElementById('plcText');


        if (data.connected) {

            lamp.classList.remove('red');

            lamp.classList.add('green');

            text.innerText = "PLC Connected";

        } else {

            lamp.classList.remove('green');

            lamp.classList.add('red');

            text.innerText = "PLC Disconnected";
        }

    } catch(err) {

        console.error(
            "PLC Status fejl:",
            err
        );
    }
}

document.getElementById("emConfigForm").addEventListener(
    "submit",
    async function(e) {

        e.preventDefault();

        const stations = [];
        const units = [];

        document
            .querySelectorAll("#stationsContainer .station-card")
            .forEach((card, index) => { 

                stations.push({

                    name: `EM${String(index + 1).padStart(2, '0')}`,

                    state_db: parseInt(
                        document.querySelector(
                            `[name="state_db_${index}"]`
                        ).value
                    ),

                    state_byte: parseInt(
                        document.querySelector(
                            `[name="state_byte_${index}"]`
                        ).value
                    ),

                    status_db: parseInt(
                        document.querySelector(
                            `[name="status_db_${index}"]`
                        ).value
                    ),

                    status_byte: parseInt(
                        document.querySelector(
                            `[name="status_byte_${index}"]`
                        ).value
                    )
                });
            });

        document
            .querySelectorAll("#unitsContainer .station-card")
            .forEach((card, index) => {

                units.push({

                    name: `Unit${String(index + 1).padStart(2, '0')}`,

                    state_db: parseInt(
                        document.querySelector(
                            `[name="unit_state_db_${index}"]`
                        ).value
                    ),

                    state_byte: parseInt(
                        document.querySelector(
                            `[name="unit_state_byte_${index}"]`
                        ).value
                    )
                });
            });

        const config = {

            plc: {
                ip: document.querySelector('[name="ip"]').value,
                rack: parseInt(document.querySelector('[name="rack"]').value),
                slot: parseInt(document.querySelector('[name="slot"]').value)
            },

            units: units,

            stations: stations,

            state_colors: stateColors
        };

        console.log(config);

        await fetch("/api/settings", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(config)
        });

        alert("Indstillinger gemt!");

        location.reload();
    }
);

const emCountInput =
    document.querySelector('[name="em_count"]');

const unitCountInput =
    document.querySelector('[name="unit_count"]');

const stateSelect =
    document.getElementById("stateSelect");

const colorPicker =
    document.getElementById("stateColorPicker");

if (stateSelect && colorPicker) {

    colorPicker.value =
        stateColors[stateSelect.value];

    stateSelect.addEventListener(
        "change",
        () => {

            colorPicker.value =
                stateColors[stateSelect.value];
        }
    );

    colorPicker.addEventListener(
        "input",
        () => {

            stateColors[stateSelect.value] =
                colorPicker.value;
        }
    );
}

emCountInput.addEventListener("change", function() {

    const count = parseInt(this.value);

    const container =
        document.getElementById("stationsContainer");

    const current =
        container.querySelectorAll(
            "#stationsContainer .station-card"
        ).length;

    // Tilføj nye stationer
    for(let i = current; i < count; i++) {

container.insertAdjacentHTML(
    "beforeend",
    `
    <div class="station-card">

        <label class="station-name">EM${String(i + 1).padStart(2, '0')}</label>

        

            <span class="EM-label">State DB</span>
            <input type="number"
                   name="state_db_${i}"
                   value="0"
                   class="input-felt">

            <label class="EM-label">State Byte</label>
            <input type="number"
                   name="state_byte_${i}"
                   value="0"
                   class="input-felt">



            <label class="EM-label">Status DB</label>
            <input type="number"
                   name="status_db_${i}"
                   value="0"
                   class="input-felt">

            <label class="EM-label">Status Byte</label>
            <input type="number"
                   name="status_byte_${i}"
                   value="0"
                   class="input-felt">



    </div>
    `
);
    }

    // Fjern overskydende stationer
    while(
        container.querySelectorAll(".station-card").length >
        count
    ) {
        container.lastElementChild.remove();
    }
});

unitCountInput.addEventListener("change", function() {

    const count = Math.max(0, parseInt(this.value) || 0);

    const container =
        document.getElementById("unitsContainer");

    const current =
        container.querySelectorAll(".station-card").length;

    for (let i = current; i < count; i++) {

        container.insertAdjacentHTML(
            "beforeend",
            `
            <div class="station-card">

                <label class="station-name">
                    Unit${String(i + 1).padStart(2, '0')}
                </label>

                <label class="EM-label">State DB</label>
                <input type="number"
                       name="unit_state_db_${i}"
                       value="0"
                       class="input-felt">

                <label class="EM-label">State Byte</label>
                <input type="number"
                       name="unit_state_byte_${i}"
                       value="0"
                       class="input-felt">

            </div>
            `
        );
    }

    while (
        container.querySelectorAll(".station-card").length >
        count
    ) {
        container.lastElementChild.remove();
    }
});

updatePLCStatus();

setInterval(() => {
    updatePLCStatus();
}, 1000);
