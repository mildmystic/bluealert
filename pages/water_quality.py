import streamlit as st
from streamlit import session_state as ss
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import time

st.title("💧 Water Quality Monitoring")
st.markdown("### Real-time sensor data and water quality analysis")

# Refresh sensor data function
def refresh_sensor_data():
    """Simulate sensor data refresh with realistic variations"""
    # Simulate API call placeholder
    # In real implementation: response = requests.get('/api/sensors')
    
    ss.sensor_data = {
        'TDS': random.randint(200, 800),
        'Turbidity': round(random.uniform(1.5, 12.0), 1),
        'Temperature': round(random.uniform(22.0, 35.0), 1),
        'pH': round(random.uniform(6.0, 9.0), 1),
        'Dissolved_Oxygen': round(random.uniform(4.0, 10.0), 1),
        'Conductivity': random.randint(150, 600),
        'Chlorine': round(random.uniform(0.1, 2.0), 2),
        'Fluoride': round(random.uniform(0.5, 2.5), 2)
    }
    ss.last_update = datetime.now()

# Initialize last update time
if 'last_update' not in ss:
    ss.last_update = datetime.now()

# Real-time controls
st.markdown('<div class="card">', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🔄 Refresh Data", type="primary", use_container_width=True):
        with st.spinner("Fetching latest sensor readings..."):
            time.sleep(1)  # Simulate API delay
            refresh_sensor_data()
        st.success("Data updated successfully!")
        st.rerun()

with col2:
    auto_refresh = st.checkbox("🔁 Auto Refresh", help="Refresh every 30 seconds")

with col3:
    st.markdown(f"**📡 Last Update:**")
    st.markdown(f"{ss.last_update.strftime('%H:%M:%S')}")

with col4:
    status_icon = "🟢" if all(
        400 <= ss.sensor_data.get('TDS', 0) <= 600,
        ss.sensor_data.get('Turbidity', 0) <= 5,
        6.5 <= ss.sensor_data.get('pH', 0) <= 8.5
    ) else "🔴"
    st.markdown(f"**⚡ System Status:** {status_icon} {'Online' if status_icon == '🟢' else 'Alert'}")

st.markdown('</div>', unsafe_allow_html=True)

# Auto-refresh implementation
if auto_refresh:
    # This would typically use st.rerun() with a timer in a real app
    st.info("Auto-refresh enabled. Data will update every 30 seconds.")

# Current sensor readings
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 🌡️ Current Sensor Readings")

def get_status_info(param, value):
    """Get status color and text for each parameter"""
    thresholds = {
        'TDS': {'good': (0, 300), 'moderate': (300, 600), 'poor': (600, float('inf'))},
        'Turbidity': {'good': (0, 1), 'moderate': (1, 5), 'poor': (5, float('inf'))},
        'pH': {'good': (6.5, 8.5), 'moderate': (6.0, 9.0), 'poor': (0, float('inf'))},
        'Temperature': {'good': (20, 30), 'moderate': (15, 35), 'poor': (0, float('inf'))},
        'Dissolved_Oxygen': {'good': (6, float('inf')), 'moderate': (4, 6), 'poor': (0, 4)},
        'Conductivity': {'good': (0, 400), 'moderate': (400, 800), 'poor': (800, float('inf'))},
        'Chlorine': {'good': (0.2, 1.0), 'moderate': (0.1, 2.0), 'poor': (0, float('inf'))},
        'Fluoride': {'good': (0.7, 1.2), 'moderate': (0.5, 1.5), 'poor': (0, float('inf'))}
    }
    
    if param not in thresholds:
        return 'good', '#27ae60'
    
    thresh = thresholds[param]
    
    # Special handling for pH (good range is between two values)
    if param == 'pH':
        if thresh['good'][0] <= value <= thresh['good'][1]:
            return 'good', '#27ae60'
        elif thresh['moderate'][0] <= value <= thresh['moderate'][1]:
            return 'moderate', '#f39c12'
        else:
            return 'poor', '#e74c3c'
    
    # Special handling for Dissolved Oxygen (higher is better)
    elif param == 'Dissolved_Oxygen':
        if value >= thresh['good'][0]:
            return 'good', '#27ae60'
        elif value >= thresh['moderate'][0]:
            return 'moderate', '#f39c12'
        else:
            return 'poor', '#e74c3c'
    
    # Standard handling (lower is better)
    else:
        if thresh['good'][0] <= value <= thresh['good'][1]:
            return 'good', '#27ae60'
        elif thresh['moderate'][0] <= value <= thresh['moderate'][1]:
            return 'moderate', '#f39c12'
        else:
            return 'poor', '#e74c3c'

# Create sensor metrics in a grid
sensor_metrics = [
    ('TDS', ss.sensor_data['TDS'], 'ppm', 'Total Dissolved Solids'),
    ('Turbidity', ss.sensor_data['Turbidity'], 'NTU', 'Water Clarity'),
    ('Temperature', ss.sensor_data['Temperature'], '°C', 'DS18B20 Sensor'),
    ('pH', ss.sensor_data['pH'], '', 'pH Level'),
    ('Dissolved_Oxygen', ss.sensor_data.get('Dissolved_Oxygen', 6.5), 'mg/L', 'Oxygen Content'),
    ('Conductivity', ss.sensor_data.get('Conductivity', 350), 'µS/cm', 'Electrical Conductivity'),
    ('Chlorine', ss.sensor_data.get('Chlorine', 0.5), 'mg/L', 'Chlorine Level'),
    ('Fluoride', ss.sensor_data.get('Fluoride', 1.0), 'mg/L', 'Fluoride Content')
]

# Display in 4x2 grid
for i in range(0, len(sensor_metrics), 4):
    cols = st.columns(4)
    for j, (param, value, unit, description) in enumerate(sensor_metrics[i:i+4]):
        if j < len(cols):
            status, color = get_status_info(param, value)
            
            with cols[j]:
                st.markdown(f"""
                <div class="metric-card" style="border-left: 4px solid {color};">
                    <h4 style="margin: 0; color: {color};">{param.replace('_', ' ')}</h4>
                    <h2 style="margin: 5px 0; color: white;">{value} <small style="opacity: 0.7;">{unit}</small></h2>
                    <p style="margin: 5px 0 0 0; opacity: 0.8; font-size: 12px;">{description}</p>
                    <p style="margin: 5px 0 0 0; color: {color}; font-weight: 600; font-size: 14px;">{status.title()}</p>
                </div>
                """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Progress bars for key parameters
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 📊 Parameter Status Indicators")

col1, col2 = st.columns(2)

with col1:
    # TDS Progress
    tds_progress = min(ss.sensor_data['TDS'] / 1000, 1.0)
    st.markdown("**TDS Level**")
    st.progress(tds_progress)
    st.caption(f"{ss.sensor_data['TDS']} ppm / 1000 ppm (safe limit)")
    
    # pH Progress (need to normalize pH scale)
    ph_value = ss.sensor_data['pH']
    ph_progress = abs(ph_value - 7.0) / 3.0  # Distance from neutral (7.0)
    st.markdown("**pH Level**")
    st.progress(1 - ph_progress if 6.5 <= ph_value <= 8.5 else ph_progress)
    st.caption(f"pH {ph_value} (optimal: 6.5-8.5)")

with col2:
    # Turbidity Progress
    turb_progress = min(ss.sensor_data['Turbidity'] / 10, 1.0)
    st.markdown("**Turbidity Level**")
    st.progress(turb_progress)
    st.caption(f"{ss.sensor_data['Turbidity']} NTU / 10 NTU (alert level)")
    
    # Temperature Progress
    temp_value = ss.sensor_data['Temperature']
    temp_progress = min(max(temp_value - 20, 0) / 20, 1.0)  # 20-40°C range
    st.markdown("**Temperature**")
    st.progress(temp_progress)
    st.caption(f"{temp_value}°C (normal: 20-30°C)")

st.markdown('</div>', unsafe_allow_html=True)

# Historical trends
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 📈 24-Hour Trends")

# Generate mock historical data
@st.cache_data
def generate_historical_data():
    hours = pd.date_range(start=datetime.now() - timedelta(hours=24), end=datetime.now(), freq='H')
    
    data = []
    for hour in hours:
        # Simulate realistic variations
        base_tds = 450 + random.randint(-50, 100)
        base_turb = 3.5 + random.uniform(-1, 3)
        base_temp = 26 + random.uniform(-3, 6)
        base_ph = 7.2 + random.uniform(-0.5, 0.8)
        
        data.append({
            'Time': hour,
            'TDS': base_tds,
            'Turbidity': round(base_turb, 1),
            'Temperature': round(base_temp, 1),
            'pH': round(base_ph, 1)
        })
    
    return pd.DataFrame(data)

historical_data = generate_historical_data()

# Parameter selection for trend display
col1, col2 = st.columns([3, 1])

with col2:
    selected_params = st.multiselect(
        "Select Parameters:",
        options=['TDS', 'Turbidity', 'Temperature', 'pH'],
        default=['TDS', 'pH'],
        key="trend_params"
    )

with col1:
    if selected_params:
        # Create subplot for selected parameters
        fig = go.Figure()
        
        colors = {'TDS': '#3498db', 'Turbidity': '#e67e22', 'Temperature': '#e74c3c', 'pH': '#27ae60'}
        
        for param in selected_params:
            fig.add_trace(go.Scatter(
                x=historical_data['Time'],
                y=historical_data[param],
                mode='lines+markers',
                name=param,
                line=dict(color=colors.get(param, '#ffffff'), width=2),
                marker=dict(size=4)
            ))
        
        fig.update_layout(
            title='Water Quality Trends - Last 24 Hours',
            xaxis_title='Time',
            yaxis_title='Values',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            height=400,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Select parameters to display trends")

st.markdown('</div>', unsafe_allow_html=True)

# Water quality alerts and recommendations
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### ⚠️ Quality Alerts & Recommendations")

def generate_alerts():
    alerts = []
    
    # Check each parameter and generate alerts
    if ss.sensor_data['TDS'] > 500:
        alerts.append({
            'type': 'High TDS Level',
            'message': f"TDS level is {ss.sensor_data['TDS']} ppm, exceeding recommended limit of 500 ppm",
            'recommendation': "Use water filtration or reverse osmosis system",
            'severity': 'high'
        })
    
    if ss.sensor_data['Turbidity'] > 5:
        alerts.append({
            'type': 'High Turbidity',
            'message': f"Water clarity is poor ({ss.sensor_data['Turbidity']} NTU)",
            'recommendation': "Boil water for 10 minutes before consumption",
            'severity': 'high'
        })
    
    if not (6.5 <= ss.sensor_data['pH'] <= 8.5):
        alerts.append({
            'type': 'pH Imbalance',
            'message': f"pH level is {ss.sensor_data['pH']}, outside safe range (6.5-8.5)",
            'recommendation': "Test water source and consider pH correction",
            'severity': 'moderate'
        })
    
    if ss.sensor_data['Temperature'] > 30:
        alerts.append({
            'type': 'High Temperature',
            'message': f"Water temperature is {ss.sensor_data['Temperature']}°C",
            'recommendation': "Allow water to cool before consumption",
            'severity': 'low'
        })
    
    return alerts

alerts = generate_alerts()

if alerts:
    for alert in alerts:
        severity_colors = {'high': '#e74c3c', 'moderate': '#f39c12', 'low': '#3498db'}
        severity_icons = {'high': '🚨', 'moderate': '⚠️', 'low': 'ℹ️'}
        
        st.markdown(f"""
        <div style="
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid {severity_colors[alert['severity']]};
            border-radius: 8px;
            padding: 16px;
            margin: 12px 0;
        ">
            <h4 style="color: {severity_colors[alert['severity']]}; margin: 0 0 8px 0;">
                {severity_icons[alert['severity']]} {alert['type']}
            </h4>
            <p style="margin: 0 0 8px 0; opacity: 0.9;">{alert['message']}</p>
            <p style="margin: 0; font-weight: 500; color: {severity_colors[alert['severity']]};">
                💡 {alert['recommendation']}
            </p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.success("✅ All water quality parameters are within acceptable limits!")

st.markdown('</div>', unsafe_allow_html=True)

# Sensor network status
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 📡 Sensor Network Status")

# Mock sensor network data
sensor_locations = [
    {'id': 'S001', 'location': 'Main Reservoir', 'status': 'online', 'battery': 89, 'signal': 95},
    {'id': 'S002', 'location': 'Treatment Plant A', 'status': 'online', 'battery': 67, 'signal': 78},
    {'id': 'S003', 'location': 'Distribution Point 1', 'status': 'online', 'battery': 92, 'signal': 88},
    {'id': 'S004', 'location': 'Distribution Point 2', 'status': 'maintenance', 'battery': 45, 'signal': 0},
    {'id': 'S005', 'location': 'Rural Well A', 'status': 'online', 'battery': 78, 'signal': 65},
    {'id': 'S006', 'location': 'Rural Well B', 'status': 'online', 'battery': 83, 'signal': 72},
    {'id': 'S007', 'location': 'Community Tank', 'status': 'online', 'battery': 91, 'signal': 94},
    {'id': 'S008', 'location': 'Backup Source', 'status': 'standby', 'battery': 95, 'signal': 82}
]

sensor_df = pd.DataFrame(sensor_locations)

# Display sensor status in columns
cols = st.columns(4)
for i, sensor in enumerate(sensor_locations):
    col_idx = i % 4
    
    status_colors = {
        'online': '#27ae60',
        'maintenance': '#f39c12',
        'standby': '#3498db',
        'offline': '#e74c3c'
    }
    
    status_icons = {
        'online': '🟢',
        'maintenance': '🟡',
        'standby': '🔵',
        'offline': '🔴'
    }
    
    with cols[col_idx]:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid {status_colors[sensor['status']]};">
            <h4 style="margin: 0; font-size: 14px;">{status_icons[sensor['status']]} {sensor['id']}</h4>
            <p style="margin: 2px 0; font-size: 12px; opacity: 0.8;">{sensor['location']}</p>
            <p style="margin: 2px 0; color: {status_colors[sensor['status']]}; font-size: 12px; font-weight: 600;">
                {sensor['status'].title()}
            </p>
            <p style="margin: 2px 0; font-size: 11px;">
                🔋 {sensor['battery']}% | 📶 {sensor['signal']}%
            </p>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# API Integration placeholder
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 🔧 Sensor Integration")

st.markdown("""
```python
# Real sensor integration example
import requests
import json

# Arduino/ESP32 API endpoint
SENSOR_API_URL = "http://192.168.1.100/api/sensors"

def fetch_sensor_data():
    try:
        response = requests.get(SENSOR_API_URL, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                'TDS': data.get('tds', 0),
                'Turbidity': data.get('turbidity', 0),
                'Temperature': data.get('temperature', 0),
                'pH': data.get('ph', 0),
                'timestamp': data.get('timestamp')
            }
    except requests.RequestException as e:
        print(f"Error fetching sensor data: {e}")
        return None

# Usage in production:
# sensor_data = fetch_sensor_data()
# if sensor_data:
#     st.session_state.sensor_data = sensor_data
```
""")

st.info("💡 In production, replace mock data with real sensor API calls to Arduino/ESP32 devices")

st.markdown('</div>', unsafe_allow_html=True)

# Export and sharing
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 📤 Export & Share")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Generate Report", use_container_width=True):
        # Prepare water quality report data
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'sensors': ss.sensor_data,
            'alerts': len(alerts),
            'status': 'good' if not alerts else 'alert'
        }
        st.success("Water quality report generated!")

with col2:
    # Export current readings
    export_df = pd.DataFrame([ss.sensor_data])
    export_df['timestamp'] = datetime.now()
    
    st.download_button(
        label="📥 Download Data",
        data=export_df.to_csv(index=False),
        file_name=f"water_quality_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        use_container_width=True
    )

with col3:
    if st.button("📱 Share Alert", use_container_width=True):
        if alerts:
            st.info("Alert notifications sent to registered users")
        else:
            st.success("All parameters normal - no alerts to share")

st.markdown('</div>', unsafe_allow_html=True)