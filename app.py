from flask import Flask, render_template, jsonify, request
from logic import RuleEngine
import random
import time
from collections import deque

app = Flask(__name__)
engine = RuleEngine()

# Simulation State
current_data = {
    'oxygen_level': 80, # %
    'oxygen_consumption': 5, # units/hr
    'oxygen_refill': 5, # units/hr
    'bed_occupancy': 60, # %
    'icu_occupancy': 50, # %
    'patient_inflow': 10, # patients/hr
    'staff_available': 5, # count
    'pharmacy_stock': 200, # units
    'pharmacy_consumption': 10, # units/hr
    'pharmacy_restock': 10, # units/hr
    'total_ventilators': 20,
    'ventilators_in_use': 5,
    'blood_stock': 80, # units
    'blood_consumption': 2, # units/hr
    'blood_restock': 2 # units/hr
}

# In-Memory Storage
# Store last 50 data points for trends
metrics_history = deque(maxlen=50)
# Store last 50 alerts
alert_history = deque(maxlen=50)

def simulate_changes():
    """
    Simulate random fluctuations in hospital metrics with some momentum/trend logic.
    """
    global current_data
    
    # Helper to constrain values
    def constrain(val, min_val, max_val):
        return max(min_val, min(max_val, val))

    # Oxygen: Always drift
    drift = random.randint(-3, 3)
    if current_data['oxygen_level'] < 50: drift += 2
    if current_data['oxygen_level'] > 95: drift -= 2
    current_data['oxygen_level'] = constrain(current_data['oxygen_level'] + drift, 0, 100)
    
    # Consumption and Refill fluctuate constantly
    current_data['oxygen_consumption'] = constrain(current_data['oxygen_consumption'] + random.randint(-2, 2), 1, 25)
    current_data['oxygen_refill'] = constrain(current_data['oxygen_refill'] + random.randint(-2, 2), 1, 25)

    # Beds: Always changing
    current_data['bed_occupancy'] = constrain(current_data['bed_occupancy'] + random.randint(-2, 2), 0, 100)
    current_data['icu_occupancy'] = constrain(current_data['icu_occupancy'] + random.randint(-2, 2), 0, 100)

    # Staff & Inflow: Constant flux
    current_data['patient_inflow'] = constrain(current_data['patient_inflow'] + random.randint(-2, 2), 0, 50)
    current_data['staff_available'] = constrain(current_data['staff_available'] + random.randint(-1, 1), 5, 25)
    
    # Pharmacy: Constant drain/restock flux
    current_data['pharmacy_consumption'] = constrain(current_data['pharmacy_consumption'] + random.randint(-2, 2), 1, 25)
    current_data['pharmacy_restock'] = constrain(current_data['pharmacy_restock'] + random.randint(-2, 2), 1, 25) # Variable supply chain
    current_data['pharmacy_stock'] -= current_data['pharmacy_consumption']
    if current_data['pharmacy_stock'] < 50 and random.random() > 0.7:
        current_data['pharmacy_stock'] += 100 
    current_data['pharmacy_stock'] = max(0, current_data['pharmacy_stock'])

    # Ventilators: Constant flux
    # Total ventilators might fluctuate due to maintenance
    if random.random() > 0.9:
        current_data['total_ventilators'] = constrain(current_data['total_ventilators'] + random.randint(-1, 1), 15, 25)
    current_data['ventilators_in_use'] = constrain(current_data['ventilators_in_use'] + random.randint(-1, 1), 0, current_data['total_ventilators'])

    # Blood Bank: Constant flux
    current_data['blood_consumption'] = constrain(current_data['blood_consumption'] + random.randint(-1, 1), 1, 15)
    current_data['blood_restock'] = constrain(current_data['blood_restock'] + random.randint(-1, 1), 1, 15) # Variable donations
    current_data['blood_stock'] -= current_data['blood_consumption']
    if random.random() > 0.8: 
        current_data['blood_stock'] += 30
    current_data['blood_stock'] = max(0, current_data['blood_stock'])

def generate_initial_history():
    """
    Generate 50 data points of history so charts are full on startup.
    """
    print("Generating initial dummy data...")
    # Start from a "normal" state
    global current_data
    current_data = {
        'oxygen_level': 85,
        'oxygen_consumption': 5,
        'oxygen_refill': 5,
        'bed_occupancy': 60,
        'icu_occupancy': 40,
        'patient_inflow': 8,
        'staff_available': 12,
        'pharmacy_stock': 250,
        'pharmacy_consumption': 8,
        'pharmacy_restock': 0,
        'total_ventilators': 20,
        'ventilators_in_use': 4,
        'blood_stock': 85,
        'blood_consumption': 2,
        'blood_restock': 0
    }

    # Go back 50 steps in time
    now = time.time()
    for i in range(50):
        simulate_changes()
        # Fake timestamp for the past
        past_time = now - ((50 - i) * 2) # 2 seconds per step
        timestamp = time.strftime("%H:%M:%S", time.localtime(past_time))
        
        metrics_history.append({
            "timestamp": timestamp,
            "metrics": current_data.copy()
        })

# Initialize history on startup
generate_initial_history()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/trends')
def trends():
    return render_template('trends.html')

@app.route('/settings')
def settings():
    return render_template('settings.html', config=engine.config)

@app.route('/history')
def history():
    return render_template('history.html', alerts=list(alert_history))

@app.route('/department/<name>')
def department(name):
    return render_template('department.html', name=name)

@app.route('/api/metrics')
def get_metrics():
    # Only simulate if we haven't forced a scenario recently (optional, but for now just simulate)
    simulate_changes() 
    analysis = engine.evaluate_all(current_data)
    
    timestamp = time.strftime("%H:%M:%S")
    
    # Record History
    metrics_history.append({
        "timestamp": timestamp,
        "metrics": current_data.copy()
    })
    
    # Record Alerts
    for resource, result in analysis.items():
        if result['status'] != 'Normal':
            alert_history.appendleft({
                "timestamp": timestamp,
                "resource": resource.title(),
                "message": result['message'],
                "status": result['status']
            })

    # Calculate Overall Risk
    risk_score = engine.calculate_overall_risk(current_data)
    recommendations = engine.generate_recommendations(current_data, risk_score)

    response = {
        "metrics": current_data,
        "analysis": analysis,
        "risk_score": risk_score,
        "recommendations": recommendations,
        "timestamp": timestamp,
        "config": engine.config
    }
    return jsonify(response)

@app.route('/api/history/metrics')
def get_metrics_history():
    return jsonify(list(metrics_history))

@app.route('/api/settings', methods=['POST'])
def update_settings():
    new_config = request.json
    # Convert values to appropriate types (int/float)
    for k, v in new_config.items():
        if '.' in str(v):
            new_config[k] = float(v)
        else:
            new_config[k] = int(v)
            
    engine.update_config(new_config)
    return jsonify({"status": "success", "config": engine.config})

@app.route('/api/scenario/<name>', methods=['POST'])
def trigger_scenario(name):
    global current_data
    if name == 'oxygen_fail':
        current_data['oxygen_level'] = 25
        current_data['oxygen_consumption'] = 15
        current_data['oxygen_refill'] = 5
    elif name == 'icu_surge':
        current_data['bed_occupancy'] = 95
        current_data['icu_occupancy'] = 98
        current_data['patient_inflow'] = 20
    elif name == 'staff_shortage':
        current_data['staff_available'] = 2
        current_data['patient_inflow'] = 15
    elif name == 'normal':
        current_data['oxygen_level'] = 80
        current_data['oxygen_consumption'] = 5
        current_data['bed_occupancy'] = 60
        current_data['icu_occupancy'] = 50
        current_data['staff_available'] = 10
        current_data['patient_inflow'] = 5
        current_data['pharmacy_stock'] = 200
        current_data['ventilators_in_use'] = 5
        
    return jsonify({"status": "success", "message": f"Scenario {name} triggered"})

if __name__ == '__main__':
    app.run(debug=True)
