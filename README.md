# Hospital Resource Failure Predictor

A real-time dashboard for monitoring and predicting hospital resource shortages. This application simulates a hospital environment, tracking critical metrics like oxygen levels, bed occupancy, staff availability, and medical stocks to provide early warnings and actionable recommendations.

## 🚀 Features.........

*   **Real-time Dashboard**: Live monitoring of Oxygen, Beds/ICU, Staff, Pharmacy, Blood Bank, and Ventilators.
*   **Predictive Analysis**: Logic engine that calculates risk scores and identifies critical trends (e.g., Consumption > Refill).
*   **Interactive Scenarios**: Trigger simulated emergencies (Oxygen Crisis, ICU Surge, Staff Shortage) to test system resilience.
*   **Historical Trends**: Visual charts using Chart.js to analyze resource fluctuations over time.
*   **Configurable Thresholds**: Adjust critical limits and safety ratios via the Settings page.
*   **Smart Recommendations**: Automated suggestions based on current risk levels (e.g., "Divert ambulances", "Order resupply").

## 🛠️ Tech Stack

*   **Backend**: Python, Flask
*   **Frontend**: HTML5, CSS3 (Premium Dark Mode), JavaScript
*   **Visualization**: Chart.js
*   **Icons**: FontAwesome
*   **Fonts**: Inter, JetBrains Mono

## 📦 Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/AKSHAY73499/VOISE-HACKATHON.git
    cd VOISE-HACKATHON
    ```

2.  **Install Dependencies**
    Ensure you have Python installed. Install Flask:
    ```bash
    pip install flask
    ```

3.  **Run the Application**
    ```bash
    python app.py
    ```

4.  **Access the Dashboard**
    Open your browser and navigate to:
    `http://127.0.0.1:5000`

5.  **DashBoard**
   <img width="889" height="794" alt="image" src="https://github.com/user-attachments/assets/b0d33350-2fd9-45b7-9a58-effb8befc23c" />


## 📂 Project Structure

```
ER/
├── app.py              # Main Flask application and simulation logic
├── logic.py            # Rule engine for risk analysis and recommendations
├── static/
│   ├── css/
│   │   └── styles.css  # Premium dark-mode styling
│   └── js/
│       ├── dashboard.js # Real-time dashboard updates
│       └── trends.js    # Chart.js configuration for trends page
├── templates/
│   ├── index.html      # Main dashboard
│   ├── trends.html     # Historical data visualization
│   ├── settings.html   # Configuration interface
│   ├── history.html    # Alert history log
│   └── department.html # Department-specific views
└── README.md           # Project documentation
```

## 🎮 Usage

*   **Dashboard**: Monitor the "Overall Risk Level" gauge. Green is safe, Red is critical.
*   **Simulation Controls**: Use the buttons at the top to force specific scenarios (e.g., "Trigger Oxygen Crisis") and observe how the system reacts.
*   **Trends**: Check the Trends page to see how resources have been fluctuating over the last few minutes.
*   **Settings**: Go to Settings to tweak the sensitivity of the alerts (e.g., increase the "Critical Bed Occupancy" threshold).

## 📄 Application Pages

The application consists of the following key interfaces:

### 1. **Dashboard (`index.html`)**
The command center of the application.
-   **Overview**: Displays real-time cards for all 6 major resources (Oxygen, Beds, Staff, Pharmacy, Blood, Ventilators).
-   **Risk Gauge**: A visual speedometer showing the overall hospital risk score (0-100%).
-   **Smart Recommendations**: Dynamic list of actionable advice based on current alerts.
-   **Simulation Controls**: Buttons to trigger specific emergency scenarios for testing.

### 2. **Trends Analysis (`trends.html`)**
Visualizes historical data to identify patterns.
-   **Charts**: Four interactive charts showing data over time:
    -   Oxygen Levels
    -   Occupancy Rates (Beds vs ICU)
    -   Staff Availability vs Patient Inflow
    -   Medical Stock Levels (Pharmacy & Blood)
-   **Auto-Update**: Charts refresh automatically as new data comes in.

### 3. **Alert History (`history.html`)**
A log of all critical events.
-   **Audit Trail**: Lists past alerts with timestamps, resource names, and severity levels.
-   **Status Tracking**: Helps in post-incident analysis by showing when resources went critical.

### 4. **System Settings (`settings.html`)**
Configuration panel for hospital administrators.
-   **Threshold Adjustment**: Sliders and inputs to define what constitutes a "Critical" or "Warning" state.
-   **Resource Ratios**: Configure safety ratios like `Staff per Patient` or `Oxygen per Patient`.
-   **Dynamic Updates**: Changes apply immediately to the logic engine without restarting the server.

### 5. **Department Details (`department.html`)**
Focused view for individual departments.
-   **Drill-down**: Provides a dedicated view for a specific resource (e.g., `/department/oxygen`).
-   **Specific Metrics**: Shows detailed metrics relevant only to that department.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
