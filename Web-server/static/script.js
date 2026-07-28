// --------------------------------------------------
// RUNTIME
// --------------------------------------------------

async function updateRuntime() {

    try {

        const response =
            await fetch('/api/runtime');


        const data =
            await response.json();


        const elapsed =
            data.runtime;


        const hours =
            String(Math.floor(elapsed / 3600))
            .padStart(2, '0');


        const minutes =
            String(Math.floor((elapsed % 3600) / 60))
            .padStart(2, '0');


        const seconds =
            String(elapsed % 60)
            .padStart(2, '0');


        document.getElementById('runtime')
            .innerText =
            `${hours}:${minutes}:${seconds}`;

    } catch(err) {

        console.error(
            "Runtime fejl:",
            err
        );
    }
}


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


// --------------------------------------------------
// CHARTS
// --------------------------------------------------

const charts = [];


// --------------------------------------------------
// PACKML FARVER
// --------------------------------------------------

const stateColors = JSON.parse(
    document.getElementById('stateColorsData').textContent
);


// --------------------------------------------------
// OPRET DIAGRAM
// --------------------------------------------------

function createChart(canvasId) {

    const ctx =
        document.getElementById(canvasId)
            .getContext('2d');


    return new Chart(ctx, {

        type: 'doughnut',

        data: {

            labels: ['Starter'],

            datasets: [{

                data: [1],

                backgroundColor: ['#444444'],

                borderWidth: 0
            }]
        },


        options: {

            responsive: true,

            plugins: {

                legend: {

                    position: 'bottom',

                    labels: {

                        color: 'white'
                    }
                },


                tooltip: {

                    callbacks: {

                        label: function(context) {

                            const value =
                                context.raw;


                            const data =
                                context.dataset.data;


                            const total =
                                data.reduce(
                                    (a, b) => a + b,
                                    0
                                );


                            const percent =
                                ((value / total) * 100)
                                .toFixed(1);


                            return `${context.label}: ${percent}% (${value}s)`;
                        }
                    }
                }
            }
        }
    });
}


// --------------------------------------------------
// OPRET 4 DIAGRAMMER
// --------------------------------------------------

document
    .querySelectorAll('canvas[id^="chart"]')
    .forEach(canvas => {

        charts.push(
            createChart(canvas.id)
        );
    });


// --------------------------------------------------
// HENT PLC DATA
// --------------------------------------------------

async function updateData() {

    try {

        const response =
            await fetch('/api/packml');


        const data =
            await response.json();


        data.forEach((plc, index) => {

            const stateName =
                plc.state_name;


            const history =
                plc.history;


            // Labels + værdier
            const labels =
                Object.keys(history);


            const values =
                Object.values(history);


            // Farver
            const colors =
                labels.map(label => {

                    return stateColors[label]
                        || '#95a5a6';
                });


            if (!charts[index]) {
                return;
            }

            // Update chart
            charts[index].data.labels =
                labels;


            charts[index]
                .data
                .datasets[0]
                .data =
                values;


            charts[index]
                .data
                .datasets[0]
                .backgroundColor =
                colors;


            charts[index].update();


            // --------------------------------------------------
            // STATE BOX
            // --------------------------------------------------

            document.getElementById(
                `state${index + 1}`
            ).innerHTML = `

                <span class="label">
                    PackML state
                </span>

                <div class="info-value">
                    ${stateName}
                </div>
            `;


            // --------------------------------------------------
            // STATUS BOX
            // --------------------------------------------------

            document.getElementById(
                `status${index + 1}`
            ).innerHTML = `

                <span class="label">
                    Status
                </span>

                <div class="info-value">
                    ${plc.status_text}
                </div>
            `;


            // --------------------------------------------------
            // OEE BOX
            // --------------------------------------------------

            document.getElementById(
                `oee${index + 1}`
            ).innerHTML = `

                <span class="label">
                    OEE
                </span>

                <div class="info-value">
                    ${plc.oee.oee.toFixed(1)}%
                </div>
            `;
        });

    } catch(err) {

        console.error(
            "PLC data fejl:",
            err
        );
    }
}


// --------------------------------------------------
// FØRSTE LOAD
// --------------------------------------------------

updateRuntime();

updatePLCStatus();

updateData();


// --------------------------------------------------
// INTERVALS
// --------------------------------------------------

setInterval(() => {

    updateRuntime();

}, 1000);


setInterval(() => {

    updatePLCStatus();

}, 1000);


setInterval(() => {

    updateData();

}, 1000);
