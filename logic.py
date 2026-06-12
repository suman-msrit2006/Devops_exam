class RuleEngine:
    def __init__(self):
        # Thresholds (Configurable)
        self.config = {
            'OXYGEN_CRITICAL_LEVEL': 30,
            'OXYGEN_PER_PATIENT': 0.5,
            'BED_OCCUPANCY_CRITICAL': 85,
            'ICU_OCCUPANCY_CRITICAL': 90,
            'STAFF_SAFE_RATIO': 4,
            'PHARMACY_MIN_STOCK': 50,
            'MEDS_PER_PATIENT': 0.1,
            'VENTILATOR_CRITICAL_PERCENT': 90,
            'BLOOD_CRITICAL_LEVEL': 20
        }

    def update_config(self, new_config):
        self.config.update(new_config)

    def check_oxygen(self, level, consumption_rate, refill_rate, patient_count=0):
        """
        Oxygen Rule:
        IF oxygen_level < threshold → "High risk"
        IF available_oxygen < (patient_count * per_patient_need) → "Insufficient"
        """
        # Calculate required oxygen based on patients (simplified)
        required_oxygen = patient_count * self.config['OXYGEN_PER_PATIENT']
        
        status = "Normal"
        message = "Oxygen levels stable."
        color = "green"

        if level < self.config['OXYGEN_CRITICAL_LEVEL']:
            status = "Critical"
            message = "High risk: oxygen shortage soon"
            color = "red"
        elif level < required_oxygen:
            status = "Critical"
            message = f"Insufficient oxygen for {patient_count} patients!"
            color = "red"
        elif consumption_rate > refill_rate:
            status = "Warning"
            message = "Critical trend detected: Consumption > Refill"
            color = "yellow"
        
        return {"status": status, "message": message, "color": color}

    def check_beds(self, bed_occupancy, icu_occupancy):
        status = "Normal"
        message = "Bed availability normal."
        color = "green"

        if icu_occupancy > self.config['ICU_OCCUPANCY_CRITICAL']:
            status = "Critical"
            message = "ICU near collapse"
            color = "red"
        elif bed_occupancy > self.config['BED_OCCUPANCY_CRITICAL']:
            status = "Warning"
            message = "Beds will run out soon"
            color = "yellow"
            
        return {"status": status, "message": message, "color": color}

    def check_staff(self, patient_inflow, staff_available):
        status = "Normal"
        message = "Staffing levels adequate."
        color = "green"

        if patient_inflow > (staff_available * self.config['STAFF_SAFE_RATIO']):
            status = "Warning"
            message = "Staff shortage predicted due to high inflow"
            color = "yellow"
            
        return {"status": status, "message": message, "color": color}

    def check_pharmacy(self, stock_level, consumption_rate, restock_rate, patient_count=0):
        status = "Normal"
        message = "Stock levels healthy."
        color = "green"

        required_stock_24h = patient_count * self.config['MEDS_PER_PATIENT'] * 24

        if stock_level < self.config['PHARMACY_MIN_STOCK']:
            status = "Critical"
            message = "Low stock: reorder now"
            color = "red"
        elif stock_level < required_stock_24h:
            status = "Critical"
            message = f"Stock insufficient for {patient_count} patients (24h buffer)"
            color = "red"
        elif stock_level > 0 and consumption_rate > restock_rate:
            status = "Warning"
            message = "Stock-out predicted soon (Consumption > Restock)"
            color = "yellow"
            
        return {"status": status, "message": message, "color": color}

    def check_blood_bank(self, stock, consumption):
        status = "Normal"
        message = "Blood stock adequate."
        color = "green"

        if stock < self.config['BLOOD_CRITICAL_LEVEL']:
            status = "Critical"
            message = "CRITICAL: Blood stock dangerously low!"
            color = "red"
        elif stock < 40:
            status = "Warning"
            message = "Blood stock running low."
            color = "yellow"
            
        return {"status": status, "message": message, "color": color}

    def check_ventilators(self, total, in_use):
        status = "Normal"
        message = "Ventilator availability normal."
        color = "green"
        
        if total == 0:
            usage_percent = 100
        else:
            usage_percent = (in_use / total) * 100
        
        if usage_percent > self.config['VENTILATOR_CRITICAL_PERCENT']:
            status = "Critical"
            message = "Ventilators near capacity!"
            color = "red"
        elif usage_percent > 75:
            status = "Warning"
            message = "High ventilator usage."
            color = "yellow"
            
        return {"status": status, "message": message, "color": color}

    def calculate_overall_risk(self, data):
        # Simple heuristic: max of individual risks
        risks = []
        
        # Oxygen Risk
        if data['oxygen_level'] < self.config['OXYGEN_CRITICAL_LEVEL']: risks.append(90)
        elif data['oxygen_level'] < 50: risks.append(50)
        else: risks.append(10)
        
        # Bed Risk
        if data['icu_occupancy'] > self.config['ICU_OCCUPANCY_CRITICAL']: risks.append(95)
        elif data['bed_occupancy'] > self.config['BED_OCCUPANCY_CRITICAL']: risks.append(70)
        else: risks.append(20)
        
        # Staff Risk
        if data['patient_inflow'] > (data['staff_available'] * self.config['STAFF_SAFE_RATIO']): risks.append(60)
        else: risks.append(10)
        
        return max(risks) if risks else 0

    def generate_recommendations(self, data, risk_score):
        recs = []
        
        if data['oxygen_level'] < 50:
            recs.append({
                "priority": "High",
                "message": "Oxygen levels critical",
                "action": "Initiate emergency refill"
            })
            
        if data['icu_occupancy'] > 90:
            recs.append({
                "priority": "High",
                "message": "ICU Full",
                "action": "Divert ambulances"
            })
            
        if data['pharmacy_stock'] < 50:
             recs.append({
                "priority": "Medium",
                "message": "Pharmacy stock low",
                "action": "Order resupply"
            })
            
        if not recs:
            recs.append({
                "priority": "Low",
                "message": "System operating normally",
                "action": "Monitor trends"
            })
            
        return recs

    def evaluate_all(self, data):
        # Derive patient count from bed occupancy for simulation purposes
        # Assuming 100 beds total
        total_beds = 100
        patient_count = int((data['bed_occupancy'] / 100) * total_beds)

        results = {}
        results['oxygen'] = self.check_oxygen(data['oxygen_level'], data['oxygen_consumption'], data['oxygen_refill'], patient_count)
        results['beds'] = self.check_beds(data['bed_occupancy'], data['icu_occupancy'])
        results['staff'] = self.check_staff(data['patient_inflow'], data['staff_available'])
        results['pharmacy'] = self.check_pharmacy(data['pharmacy_stock'], data['pharmacy_consumption'], data['pharmacy_restock'], patient_count)
        results['ventilators'] = self.check_ventilators(data['total_ventilators'], data['ventilators_in_use'])
        results['blood'] = self.check_blood_bank(data['blood_stock'], data['blood_consumption'])
        return results
