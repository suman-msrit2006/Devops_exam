function updateDashboard() {
    fetch('/api/metrics')
        .then(response => response.json())
        .then(data => {
            const metrics = data.metrics;
            const analysis = data.analysis;
            const config = data.config;
            const riskScore = data.risk_score;
            const recommendations = data.recommendations;
            
            document.getElementById('timestamp').textContent = data.timestamp;

            // Update Risk Gauge
            if (riskScore !== undefined) {
                updateRiskGauge(riskScore);
            }

            // Update Recommendations
            if (recommendations) {
                updateRecommendations(recommendations);
            }

            // Update Thresholds Display
            if (config) {
                document.getElementById('thr-oxygen').textContent = config.OXYGEN_CRITICAL_LEVEL;
                document.getElementById('thr-bed').textContent = config.BED_OCCUPANCY_CRITICAL;
                document.getElementById('thr-icu').textContent = config.ICU_OCCUPANCY_CRITICAL;
                document.getElementById('thr-staff').textContent = config.STAFF_SAFE_RATIO;
                document.getElementById('thr-pharm').textContent = config.PHARMACY_MIN_STOCK;
                document.getElementById('thr-vent').textContent = config.VENTILATOR_CRITICAL_PERCENT;
                document.getElementById('thr-blood').textContent = config.BLOOD_CRITICAL_LEVEL;
            }

            // Update Oxygen
            updateCard('oxygen', metrics.oxygen_level, metrics.oxygen_consumption, metrics.oxygen_refill, analysis.oxygen);
            
            // Update Beds
            updateCard('beds', metrics.bed_occupancy, metrics.icu_occupancy, null, analysis.beds);
            document.getElementById('val-bed-occ').textContent = metrics.bed_occupancy;
            document.getElementById('val-icu-occ').textContent = metrics.icu_occupancy;

            // Update Staff
            updateCard('staff', metrics.staff_available, metrics.patient_inflow, null, analysis.staff);
            document.getElementById('val-staff-avail').textContent = metrics.staff_available;
            document.getElementById('val-pat-inflow').textContent = metrics.patient_inflow;

            // Update Pharmacy
            updateCard('pharmacy', metrics.pharmacy_stock, metrics.pharmacy_consumption, metrics.pharmacy_restock, analysis.pharmacy);
            document.getElementById('val-pharm-stock').textContent = metrics.pharmacy_stock;
            document.getElementById('val-pharm-cons').textContent = metrics.pharmacy_consumption;
            document.getElementById('val-pharm-restock').textContent = metrics.pharmacy_restock;

            // Update Blood Bank
            updateCard('blood', metrics.blood_stock, metrics.blood_consumption, metrics.blood_restock, analysis.blood);
            document.getElementById('val-blood-stock').textContent = metrics.blood_stock;
            document.getElementById('val-blood-cons').textContent = metrics.blood_consumption;
            document.getElementById('val-blood-restock').textContent = metrics.blood_restock;

            // Update Ventilators
            updateCard('ventilators', metrics.ventilators_in_use, metrics.total_ventilators, null, analysis.ventilators);
            document.getElementById('val-vent-use').textContent = metrics.ventilators_in_use;
            document.getElementById('val-vent-total').textContent = metrics.total_ventilators;
            document.getElementById('val-vent-percent').textContent = Math.round((metrics.ventilators_in_use / metrics.total_ventilators) * 100);
        })
        .catch(error => console.error('Error fetching metrics:', error));
}

function updateCard(type, val1, val2, val3, analysis) {
    // Specific value updates are handled in the main loop for clarity where IDs differ
    // This function handles the common status/alert logic
    
    if (type === 'oxygen') {
        document.getElementById('val-oxygen-level').textContent = val1;
        document.getElementById('val-oxygen-cons').textContent = val2;
        document.getElementById('val-oxygen-refill').textContent = val3;
    }

    const statusEl = document.getElementById(`status-${type}`);
    const alertEl = document.getElementById(`alert-${type}`);
    
    // Reset classes
    statusEl.className = 'status-indicator';
    alertEl.className = 'alert-box';
    
    // Apply new state
    statusEl.classList.add(`status-${analysis.color}`);
    
    alertEl.textContent = analysis.message;
    if (analysis.status === 'Critical') {
        alertEl.classList.add('alert-critical');
    } else if (analysis.status === 'Warning') {
        alertEl.classList.add('alert-warning');
    }
}

function updateRiskGauge(score) {
    const gauge = document.getElementById('risk-gauge');
    const scoreEl = document.getElementById('risk-score');
    const labelEl = document.getElementById('risk-label');

    scoreEl.textContent = `${score}%`;

    // Determine Color and Label
    let color = 'var(--success-color)';
    let label = 'LOW RISK';
    
    if (score > 60) {
        color = 'var(--danger-color)';
        label = 'HIGH RISK';
        labelEl.style.color = 'var(--danger-color)';
    } else if (score > 30) {
        color = 'var(--warning-color)';
        label = 'MEDIUM RISK';
        labelEl.style.color = 'var(--warning-color)';
    } else {
        labelEl.style.color = 'var(--success-color)';
    }

    labelEl.textContent = label;
    
    // Update Conic Gradient
    gauge.style.background = `conic-gradient(${color} ${score * 3.6}deg, rgba(255,255,255,0.1) 0deg)`;
}

function updateRecommendations(recs) {
    const list = document.getElementById('recommendations-list');
    list.innerHTML = ''; // Clear current list

    recs.forEach(rec => {
        const item = document.createElement('div');
        let priorityClass = 'rec-low';
        if (rec.priority === 'High') priorityClass = 'rec-high';
        if (rec.priority === 'Medium') priorityClass = 'rec-medium';

        item.className = `rec-item ${priorityClass}`;
        
        item.innerHTML = `
            <div class="rec-content">
                <strong>${rec.message}</strong>
                <span>Priority: ${rec.priority}</span>
            </div>
            <div class="rec-action">
                ${rec.action}
            </div>
        `;
        list.appendChild(item);
    });
}

function triggerScenario(name) {
    fetch(`/api/scenario/${name}`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            updateDashboard(); // Immediate update
        })
        .catch(error => console.error('Error triggering scenario:', error));
}

// Poll every 2 seconds
setInterval(updateDashboard, 2000);
updateDashboard(); // Initial call
