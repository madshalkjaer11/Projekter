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
// PACKML FARVER
// --------------------------------------------------

const stateColors = {
    ...JSON.parse(
        document.getElementById('stateColorsData').textContent
    )
};


// --------------------------------------------------
// CHARTS
// --------------------------------------------------

const unitCharts = [];

function createUnitChart(canvas) {

    return new Chart(canvas.getContext('2d'), {

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

document
    .querySelectorAll('canvas[id^="unitChart"]')
    .forEach(canvas => {

        unitCharts.push(
            createUnitChart(canvas)
        );
    });


// --------------------------------------------------
// UNIT DATA
// --------------------------------------------------

async function updateUnit() {

    try {

        const response =
            await fetch('/api/unit');


        const data =
            await response.json();


        data.forEach((unit, index) => {

            const chart = unitCharts[index];

            if (!chart) {
                return;
            }

            const labels =
                Object.keys(unit.history);


            const values =
                Object.values(unit.history);


            const colors =
                labels.map(label =>
                    stateColors[label] || '#888'
                );


            chart.data.labels =
                labels;


            chart.data.datasets[0].data =
                values;


            chart.data.datasets[0].backgroundColor =
                colors;


            chart.update();


            document.getElementById(
                `unitState${index + 1}`
            ).innerText =
                unit.state_name;


            document.getElementById(
                `unitOee${index + 1}`
            ).innerHTML = `
                ${unit.oee.oee.toFixed(1)}%
            `;
        });


    } catch(err) {

        console.error(
            "Unit fejl:",
            err
        );
    }
}


// --------------------------------------------------
// FØRSTE LOAD
// --------------------------------------------------

updateRuntime();

updatePLCStatus();

updateUnit();


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

    updateUnit();

}, 1000);
