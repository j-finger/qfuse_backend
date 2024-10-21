// static/js/charts.js

// Get the context of each canvas element
const ctxAccelX = document.getElementById('accel_x_chart').getContext('2d');
const ctxAccelY = document.getElementById('accel_y_chart').getContext('2d');
const ctxAccelZ = document.getElementById('accel_z_chart').getContext('2d');
const ctxGyroX = document.getElementById('gyro_x_chart').getContext('2d');
const ctxGyroY = document.getElementById('gyro_y_chart').getContext('2d');
const ctxGyroZ = document.getElementById('gyro_z_chart').getContext('2d');

// Declare chart variables
let accelXChart, accelYChart, accelZChart, gyroXChart, gyroYChart, gyroZChart;

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

/**
 * Fetches sensor data from the Flask API based on selected filters.
 */
function fetchData() {
    const device = document.getElementById('device').value;
    const subdevice = document.getElementById('subdevice').value;
    const url = new URL('/api/data', window.location.origin);
    if (device) url.searchParams.append('device', device);
    if (subdevice) url.searchParams.append('subdevice', subdevice);

    fetch(url)
        .then(response => response.json())
        .then(data => updateCharts(data))
        .catch(error => console.error('Error fetching data:', error));
}

/**
 * Updates all charts with the fetched data.
 * @param {Array} data - Array of sensor data objects.
 */
function updateCharts(data) {
    // Sort data by 'id' in ascending order
    data.sort((a, b) => a.id - b.id);

    const labels = data.map(d => d.id); // Using 'id' as the x-axis label

    // Extract unique subdevice_ids from the data
    const subdevices = [...new Set(data.map(d => d.subdevice_id))];
    const colors = generateColors(subdevices.length);

    // Prepare datasets for each chart
    const datasetsAccelX = [];
    const datasetsAccelY = [];
    const datasetsAccelZ = [];
    const datasetsGyroX = [];
    const datasetsGyroY = [];
    const datasetsGyroZ = [];

    subdevices.forEach((subdevice, index) => {
        const color = colors[index];
        // Filter data for the current subdevice
        const filteredData = data.filter(d => d.subdevice_id === subdevice);

        datasetsAccelX.push({
            label: `Subdevice ${subdevice}`,
            data: filteredData.map(d => ({ x: d.id, y: d.accel_x })),
            borderColor: color,
            fill: false
        });

        datasetsAccelY.push({
            label: `Subdevice ${subdevice}`,
            data: filteredData.map(d => ({ x: d.id, y: d.accel_y })),
            borderColor: color,
            fill: false
        });

        datasetsAccelZ.push({
            label: `Subdevice ${subdevice}`,
            data: filteredData.map(d => ({ x: d.id, y: d.accel_z })),
            borderColor: color,
            fill: false
        });

        datasetsGyroX.push({
            label: `Subdevice ${subdevice}`,
            data: filteredData.map(d => ({ x: d.id, y: d.gyro_x })),
            borderColor: color,
            fill: false
        });

        datasetsGyroY.push({
            label: `Subdevice ${subdevice}`,
            data: filteredData.map(d => ({ x: d.id, y: d.gyro_y })),
            borderColor: color,
            fill: false
        });

        datasetsGyroZ.push({
            label: `Subdevice ${subdevice}`,
            data: filteredData.map(d => ({ x: d.id, y: d.gyro_z })),
            borderColor: color,
            fill: false
        });
    });

    // Update each chart with new data
    accelXChart.data.labels = labels;
    accelXChart.data.datasets = datasetsAccelX;
    accelXChart.update();

    accelYChart.data.labels = labels;
    accelYChart.data.datasets = datasetsAccelY;
    accelYChart.update();

    accelZChart.data.labels = labels;
    accelZChart.data.datasets = datasetsAccelZ;
    accelZChart.update();

    gyroXChart.data.labels = labels;
    gyroXChart.data.datasets = datasetsGyroX;
    gyroXChart.update();

    gyroYChart.data.labels = labels;
    gyroYChart.data.datasets = datasetsGyroY;
    gyroYChart.update();

    gyroZChart.data.labels = labels;
    gyroZChart.data.datasets = datasetsGyroZ;
    gyroZChart.update();
}

/**
 * Generates distinct colors for each subdevice.
 * @param {number} num - Number of colors to generate.
 * @returns {Array} Array of color strings in HSL format.
 */
function generateColors(num) {
    const colors = [];
    const hueStep = Math.floor(360 / num);
    for (let i = 0; i < num; i++) {
        const hue = i * hueStep;
        colors.push(`hsl(${hue}, 70%, 50%)`);
    }
    return colors;
}

// Event listener for the "Filter" button
document.getElementById('filter-btn').addEventListener('click', fetchData);

// Initialize charts on page load
initializeCharts();

// Fetch initial data to populate charts
fetchData();

// Optional: Set up periodic data fetching (e.g., every 5 seconds)
// Uncomment the following line to enable automatic updates
// setInterval(fetchData, 5000); // Fetch every 5 seconds
