// ~/qfuse_backend/sensor_dashboard/static/js/charts.js

// Get the context of each canvas element
const ctxAccelX = document.getElementById('accel_x_chart').getContext('2d');
const ctxAccelY = document.getElementById('accel_y_chart').getContext('2d');
const ctxAccelZ = document.getElementById('accel_z_chart').getContext('2d');
const ctxGyroX = document.getElementById('gyro_x_chart').getContext('2d');
const ctxGyroY = document.getElementById('gyro_y_chart').getContext('2d');
const ctxGyroZ = document.getElementById('gyro_z_chart').getContext('2d');

// Declare chart variables
let accelXChart, accelYChart, accelZChart, gyroXChart, gyroYChart, gyroZChart;

// Store colors for subdevices to maintain consistency
const subdeviceColors = {};

/**
 * Generates a unique color for each subdevice using the golden angle approximation.
 * This ensures a good distribution of colors.
 * @param {string} subdevice - The subdevice identifier.
 * @returns {string} - The HSL color string.
 */
function generateColorForSubdevice(subdevice) {
    if (subdeviceColors[subdevice]) {
        return subdeviceColors[subdevice];
    } else {
        const hue = (Object.keys(subdeviceColors).length * 137.508) % 360; // Golden angle approximation
        const color = `hsl(${hue}, 70%, 50%)`;
        subdeviceColors[subdevice] = color;
        return color;
    }
}

/**
 * Initializes all six Chart.js line charts.
 */
function initializeCharts() {
    const commonOptions = {
        responsive: true,
        scales: {
            x: {
                type: 'linear',
                title: {
                    display: true,
                    text: 'Sample ID'
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Value'
                }
            }
        },
        plugins: {
            legend: {
                display: true,
                position: 'top',
            },
            title: {
                display: false,
                text: ''
            }
        }
    };

    accelXChart = new Chart(ctxAccelX, {
        type: 'line',
        data: { datasets: [] },
        options: { ...commonOptions }
    });

    accelYChart = new Chart(ctxAccelY, {
        type: 'line',
        data: { datasets: [] },
        options: { ...commonOptions }
    });

    accelZChart = new Chart(ctxAccelZ, {
        type: 'line',
        data: { datasets: [] },
        options: { ...commonOptions }
    });

    gyroXChart = new Chart(ctxGyroX, {
        type: 'line',
        data: { datasets: [] },
        options: { ...commonOptions }
    });

    gyroYChart = new Chart(ctxGyroY, {
        type: 'line',
        data: { datasets: [] },
        options: { ...commonOptions }
    });

    gyroZChart = new Chart(ctxGyroZ, {
        type: 'line',
        data: { datasets: [] },
        options: { ...commonOptions }
    });
}

let lastDataId = 0; // Keep track of the last data point's 'id'

/**
 * Fetches sensor data from the Flask API based on selected filters.
 * If 'lastDataId' is set, fetches only new data since the last 'id'.
 */
function fetchData() {
    const device = document.getElementById('device').value;
    const subdevice = document.getElementById('subdevice').value;
    const url = new URL('/api/data', window.location.origin);
    if (device) url.searchParams.append('device', device);
    if (subdevice) url.searchParams.append('subdevice', subdevice);
    if (lastDataId) url.searchParams.append('since_id', lastDataId);

    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.length > 0) {
                lastDataId = data[data.length - 1].id;
                updateChartsIncremental(data);
            }
        })
        .catch(error => console.error('Error fetching data:', error));
}

/**
 * Updates all charts with the fetched incremental data.
 * @param {Array} data - Array of sensor data objects.
 */
function updateChartsIncremental(data) {
    // Assuming data is sorted by 'id' in ascending order

    const subdevices = [...new Set(data.map(d => d.subdevice_id))];

    subdevices.forEach(subdevice => {
        const filteredData = data.filter(d => d.subdevice_id === subdevice);

        // Prepare datasets for each chart
        const datasetsInfo = [
            { chart: accelXChart, key: 'accel_x' },
            { chart: accelYChart, key: 'accel_y' },
            { chart: accelZChart, key: 'accel_z' },
            { chart: gyroXChart, key: 'gyro_x' },
            { chart: gyroYChart, key: 'gyro_y' },
            { chart: gyroZChart, key: 'gyro_z' },
        ];

        datasetsInfo.forEach(({ chart, key }) => {
            let dataset = chart.data.datasets.find(ds => ds.label === `Subdevice ${subdevice}`);

            if (!dataset) {
                // Create a new dataset if it doesn't exist
                const color = generateColorForSubdevice(subdevice);
                dataset = {
                    label: `Subdevice ${subdevice}`,
                    data: [],
                    borderColor: color,
                    fill: false
                };
                chart.data.datasets.push(dataset);
            }

            // Append new data points
            filteredData.forEach(d => {
                dataset.data.push({ x: d.id, y: d[key] });
            });

            // Optionally limit the number of data points to prevent memory issues
            const MAX_POINTS = 5000;
            if (dataset.data.length > MAX_POINTS) {
                dataset.data = dataset.data.slice(-MAX_POINTS);
            }

            chart.update();
        });
    });
}

/**
 * Resets all charts and clears the subdevice colors.
 */
function resetCharts() {
    const charts = [accelXChart, accelYChart, accelZChart, gyroXChart, gyroYChart, gyroZChart];
    charts.forEach(chart => {
        chart.data.datasets = [];
        chart.update();
    });
    // Clear subdevice colors
    for (let key in subdeviceColors) {
        delete subdeviceColors[key];
    }
    lastDataId = 0; // Reset the lastDataId
}

// Event listener for the "Filter" button
document.getElementById('filter-btn').addEventListener('click', () => {
    // Reset charts and lastDataId
    resetCharts();
    fetchData();
});

// Initialize charts on page load
initializeCharts();

// Fetch initial data to populate charts
fetchData();

// Set up periodic data fetching (e.g., every 5 seconds)
setInterval(fetchData, 5000); // Fetch every 5 seconds
