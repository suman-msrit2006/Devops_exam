// Chart Configuration
Chart.defaults.color = '#94a3b8';
Chart.defaults.borderColor = 'rgba(255, 255, 255, 0.1)';
Chart.defaults.font.family = "'Inter', sans-serif";

let charts = {};

function initCharts() {
    // Oxygen Chart
    const ctxOxygen = document.getElementById('chartOxygen').getContext('2d');
    charts.oxygen = new Chart(ctxOxygen, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Oxygen Level (%)',
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                data: [],
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { beginAtZero: true, max: 100 }
            },
            plugins: {
                legend: { position: 'top' }
            }
        }
    });

    // Occupancy Chart
    const ctxOccupancy = document.getElementById('chartOccupancy').getContext('2d');
    charts.occupancy = new Chart(ctxOccupancy, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Bed Occupancy (%)',
                    borderColor: '#10b981',
                    data: [],
                    tension: 0.4
                },
                {
                    label: 'ICU Occupancy (%)',
                    borderColor: '#ef4444',
                    data: [],
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { beginAtZero: true, max: 100 }
            }
        }
    });

    // Staff Chart
    const ctxStaff = document.getElementById('chartStaff').getContext('2d');
    charts.staff = new Chart(ctxStaff, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Staff Available',
                    backgroundColor: '#8b5cf6',
                    data: []
                },
                {
                    label: 'Patient Inflow',
                    backgroundColor: '#f59e0b',
                    data: []
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { beginAtZero: true }
            }
        }
    });

    // Stock Chart
    const ctxStock = document.getElementById('chartStock').getContext('2d');
    charts.stock = new Chart(ctxStock, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Pharmacy Stock',
                    borderColor: '#ec4899',
                    data: [],
                    tension: 0.4
                },
                {
                    label: 'Blood Stock',
                    borderColor: '#ef4444',
                    borderDash: [5, 5],
                    data: [],
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

function updateCharts() {
    fetch('/api/history/metrics')
        .then(response => response.json())
        .then(data => {
            // Process data (assuming data is sorted by time)
            const labels = data.map(d => d.timestamp);
            
            // Update Oxygen
            charts.oxygen.data.labels = labels;
            charts.oxygen.data.datasets[0].data = data.map(d => d.metrics.oxygen_level);
            charts.oxygen.update();

            // Update Occupancy
            charts.occupancy.data.labels = labels;
            charts.occupancy.data.datasets[0].data = data.map(d => d.metrics.bed_occupancy);
            charts.occupancy.data.datasets[1].data = data.map(d => d.metrics.icu_occupancy);
            charts.occupancy.update();

            // Update Staff
            charts.staff.data.labels = labels;
            charts.staff.data.datasets[0].data = data.map(d => d.metrics.staff_available);
            charts.staff.data.datasets[1].data = data.map(d => d.metrics.patient_inflow);
            charts.staff.update();

            // Update Stock
            charts.stock.data.labels = labels;
            charts.stock.data.datasets[0].data = data.map(d => d.metrics.pharmacy_stock);
            charts.stock.data.datasets[1].data = data.map(d => d.metrics.blood_stock);
            charts.stock.update();
        })
        .catch(err => console.error("Error updating charts:", err));
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initCharts();
    updateCharts();
    setInterval(updateCharts, 5000); // Poll every 5 seconds
});
