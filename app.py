import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import folium
from streamlit_folium import st_folium
import random
import numpy as np

# Page configuration
st.set_page_config(
    page_title="BlueAlert Prototype",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for blue-cyan theme
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0f4c75 0%, #2a9d8f 100%);
        color: white;
    }
    
    .stApp > header {
        background-color: transparent;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 10px 0;
    }
    
    .alert-badge {
        background-color: #e74c3c;
        color: white;
        border-radius: 50%;
        width: 20px;
        height: 20px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        font-weight: bold;
        margin-left: 10px;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2a9d8f 0%, #0f4c75 100%);
    }
    
    .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
    }
    
    h1, h2, h3 {
        color: white !important;
    }
    
    .stDataFrame {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'sensor_data' not in st.session_state:
    st.session_state.sensor_data = {
        'TDS': 450,
        'Turbidity': 5.2,
        'Temperature': 28.5,
        'pH': 7.1
    }

if 'alert_count' not in st.session_state:
    st.session_state.alert_count = 3

# Mock data generation functions
@st.cache_data
def generate_mock_disease_data():
    """Generate mock disease case data"""
    diseases = ['Cholera', 'Typhoid', 'Diarrhea', 'Hepatitis A', 'Dysentery']
    cases_week = [15, 8, 32, 5, 12]
    cases_month = [45, 28, 89, 18, 35]
    cases_year = [450, 280, 890, 180, 350]
    
    return pd.DataFrame({
        'Disease': diseases,
        'Last Week': cases_week,
        'Last Month': cases_month,
        'Last Year': cases_year
    })

@st.cache_data
def generate_mock_location_data():
    """Generate mock location data for Northeast India"""
    locations = [
        {'name': 'Guwahati', 'lat': 26.1445, 'lon': 91.7362, 'district': 'Kamrup', 'cases': 45, 'risk': 'high'},
        {'name': 'Dibrugarh', 'lat': 27.4728, 'lon': 94.9120, 'district': 'Dibrugarh', 'cases': 12, 'risk': 'low'},
        {'name': 'Silchar', 'lat': 24.8333, 'lon': 92.7789, 'district': 'Cachar', 'cases': 28, 'risk': 'moderate'},
        {'name': 'Aizawl', 'lat': 23.7367, 'lon': 92.7173, 'district': 'Aizawl', 'cases': 35, 'risk': 'high'},
        {'name': 'Imphal', 'lat': 24.8170, 'lon': 93.9368, 'district': 'Imphal West', 'cases': 8, 'risk': 'low'},
        {'name': 'Kohima', 'lat': 25.6751, 'lon': 94.1086, 'district': 'Kohima', 'cases': 22, 'risk': 'moderate'},
        {'name': 'Shillong', 'lat': 25.5788, 'lon': 91.8933, 'district': 'East Khasi Hills', 'cases': 18, 'risk': 'moderate'},
        {'name': 'Itanagar', 'lat': 27.0844, 'lon': 93.6053, 'district': 'Papum Pare', 'cases': 6, 'risk': 'low'},
    ]
    return pd.DataFrame(locations)

@st.cache_data
def generate_trends_data():
    """Generate mock time series data for disease trends"""
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='W')
    diseases = ['Cholera', 'Typhoid', 'Diarrhea', 'Hepatitis A']
    
    data = []
    for disease in diseases:
        base_cases = random.randint(5, 20)
        seasonal_factor = np.sin(np.linspace(0, 2*np.pi, len(dates))) * random.randint(5, 15)
        noise = np.random.normal(0, 3, len(dates))
        cases = np.maximum(0, base_cases + seasonal_factor + noise).astype(int)
        
        for i, date in enumerate(dates):
            data.append({
                'Date': date,
                'Disease': disease,
                'Cases': cases[i],
                'Type': 'Actual'
            })
    
    # Add forecast data
    future_dates = pd.date_range(start='2025-01-01', end='2025-03-31', freq='W')
    for disease in diseases:
        base_forecast = random.randint(8, 25)
        for date in future_dates:
            data.append({
                'Date': date,
                'Disease': disease,
                'Cases': base_forecast + random.randint(-5, 5),
                'Type': 'Forecast'
            })
    
    return pd.DataFrame(data)

@st.cache_data
def generate_health_data():
    """Generate mock local health data"""
    age_groups = ['0-5', '6-18', '19-35', '36-60', '60+']
    genders = ['Male', 'Female']
    
    data = []
    for age in age_groups:
        for gender in genders:
            data.append({
                'Age Group': age,
                'Gender': gender,
                'Total Cases': random.randint(10, 100),
                'Recoveries': random.randint(8, 80),
                'At Risk': random.randint(2, 20),
                'Vaccination Rate (%)': random.randint(60, 95)
            })
    
    return pd.DataFrame(data)

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/200x100/2a9d8f/ffffff?text=BlueAlert", width=200)
    st.markdown("### 🌊 Control Panel")
    
    # Time period filter
    time_period = st.selectbox(
        "📅 Time Period",
        ["Last Week", "Last Month", "Last Year"],
        index=1
    )
    
    # Location filter
    location_data = generate_mock_location_data()
    districts = ['All'] + list(location_data['district'].unique())
    selected_district = st.selectbox(
        "📍 District Filter",
        districts
    )
    
    # Age group filter
    age_filter = st.selectbox(
        "👥 Age Group",
        ["All", "0-5", "6-18", "19-35", "36-60", "60+"]
    )
    
    # Gender filter
    gender_filter = st.selectbox(
        "⚥ Gender",
        ["All", "Male", "Female"]
    )
    
    st.markdown("---")
    
    # Refresh button
    if st.button("🔄 Refresh Data", type="primary"):
        # Simulate sensor data update
        st.session_state.sensor_data = {
            'TDS': random.randint(300, 800),
            'Turbidity': round(random.uniform(2, 15), 1),
            'Temperature': round(random.uniform(25, 35), 1),
            'pH': round(random.uniform(6.5, 8.5), 1)
        }
        st.rerun()

# Main content
# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🌊 BlueAlert Prototype")
    st.markdown("### Smart Health Surveillance Dashboard for Water-borne Disease Monitoring")

with col2:
    if st.session_state.alert_count > 0:
        st.markdown(f"""
        <div style="text-align: right; margin-top: 20px;">
            <span style="font-size: 18px;">🚨 Active Alerts</span>
            <span class="alert-badge">{st.session_state.alert_count}</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Interactive Map Section
st.markdown("## 🗺️ Disease Hotspot Map")

# Filter location data based on district selection
if selected_district != "All":
    filtered_locations = location_data[location_data['district'] == selected_district]
else:
    filtered_locations = location_data

# Create folium map
m = folium.Map(location=[25.5, 93.0], zoom_start=6)

# Add markers with different colors based on risk level
color_map = {'low': 'green', 'moderate': 'orange', 'high': 'red'}

for idx, row in filtered_locations.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=max(5, row['cases'] / 2),
        popup=folium.Popup(f"""
        <b>{row['name']}</b><br>
        District: {row['district']}<br>
        Cases: {row['cases']}<br>
        Risk Level: {row['risk'].title()}<br>
        Water Quality: {'Poor' if row['risk'] == 'high' else 'Good'}
        """, max_width=200),
        color=color_map[row['risk']],
        fillColor=color_map[row['risk']],
        fillOpacity=0.7
    ).add_to(m)

# Display map
map_data = st_folium(m, width=700, height=400)

# Disease Statistics Section
st.markdown("## 📊 Disease Statistics")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Cases by Disease")
    disease_data = generate_mock_disease_data()
    
    # Select data based on time period
    period_col = time_period
    chart_data = disease_data[['Disease', period_col]].copy()
    chart_data.columns = ['Disease', 'Cases']
    
    fig_bar = px.bar(
        chart_data,
        x='Disease',
        y='Cases',
        color='Cases',
        color_continuous_scale='Blues',
        title=f'Disease Cases - {time_period}'
    )
    fig_bar.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.markdown("### Disease Trends Over Time")
    trends_data = generate_trends_data()
    
    # Multi-select for diseases
    selected_diseases = st.multiselect(
        "Select diseases to display:",
        trends_data['Disease'].unique(),
        default=['Cholera', 'Diarrhea']
    )
    
    if selected_diseases:
        filtered_trends = trends_data[trends_data['Disease'].isin(selected_diseases)]
        
        fig_line = px.line(
            filtered_trends,
            x='Date',
            y='Cases',
            color='Disease',
            line_dash='Type',
            title='Disease Trends & Forecast'
        )
        fig_line.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig_line, use_container_width=True)

# Water Quality Section
st.markdown("## 💧 Real-time Water Quality Monitoring")

col1, col2, col3, col4 = st.columns(4)

with col1:
    tds_value = st.session_state.sensor_data['TDS']
    tds_status = "🔴 High" if tds_value > 500 else "🟡 Moderate" if tds_value > 300 else "🟢 Good"
    st.metric(
        label="TDS (ppm)",
        value=f"{tds_value}",
        delta=f"Status: {tds_status}",
        delta_color="inverse" if tds_value > 500 else "normal"
    )
    
    # TDS Progress bar
    progress = min(tds_value / 1000, 1.0)
    st.progress(progress)

with col2:
    turbidity = st.session_state.sensor_data['Turbidity']
    turb_status = "🔴 High" if turbidity > 10 else "🟡 Moderate" if turbidity > 5 else "🟢 Good"
    st.metric(
        label="Turbidity (NTU)",
        value=f"{turbidity}",
        delta=f"Status: {turb_status}"
    )

with col3:
    temp = st.session_state.sensor_data['Temperature']
    st.metric(
        label="Temperature (°C)",
        value=f"{temp}",
        delta="Normal Range" if 20 <= temp <= 30 else "Outside Range"
    )

with col4:
    ph = st.session_state.sensor_data['pH']
    ph_status = "🟢 Good" if 6.5 <= ph <= 8.5 else "🔴 Poor"
    st.metric(
        label="pH Level",
        value=f"{ph}",
        delta=f"Status: {ph_status}"
    )

# Add sensor integration comment
st.markdown("""
```python
# Real sensor integration placeholder
# Replace mock data with actual sensor API calls:
# response = requests.get('http://arduino-ip/api/sensors')
# sensor_data = response.json()
```
""")

# Local Health Data Section
st.markdown("## 👥 Local Health Demographics")

health_data = generate_health_data()

# Apply filters
filtered_health = health_data.copy()
if age_filter != "All":
    filtered_health = filtered_health[filtered_health['Age Group'] == age_filter]
if gender_filter != "All":
    filtered_health = filtered_health[filtered_health['Gender'] == gender_filter]

st.dataframe(filtered_health, use_container_width=True)

# Summary metrics
col1, col2, col3 = st.columns(3)
with col1:
    total_cases = filtered_health['Total Cases'].sum()
    st.metric("Total Cases", total_cases)
with col2:
    total_recoveries = filtered_health['Recoveries'].sum()
    recovery_rate = round((total_recoveries / total_cases) * 100, 1) if total_cases > 0 else 0
    st.metric("Recovery Rate", f"{recovery_rate}%")
with col3:
    at_risk = filtered_health['At Risk'].sum()
    st.metric("At Risk Population", at_risk)

# Safety Alerts Section
st.markdown("## 🚨 Active Safety Alerts")

alerts = [
    {
        "id": 1,
        "type": "High TDS Level",
        "message": "Water TDS levels exceed safe limits. Boil water before consumption!",
        "severity": "high",
        "location": "Guwahati District",
        "time": "2 hours ago"
    },
    {
        "id": 2,
        "type": "Disease Outbreak",
        "message": "Increased cholera cases detected in Aizawl region. Seek medical attention if symptoms present.",
        "severity": "high",
        "location": "Aizawl District",
        "time": "5 hours ago"
    },
    {
        "id": 3,
        "type": "Water Quality Warning",
        "message": "Turbidity levels elevated in Silchar area. Use water purification tablets.",
        "severity": "moderate",
        "location": "Cachar District",
        "time": "1 day ago"
    }
]

for alert in alerts:
    severity_color = "🔴" if alert["severity"] == "high" else "🟡"
    with st.expander(f"{severity_color} {alert['type']} - {alert['location']}"):
        st.write(f"**Message:** {alert['message']}")
        st.write(f"**Location:** {alert['location']}")
        st.write(f"**Time:** {alert['time']}")
        
        if alert["severity"] == "high":
            st.error("⚠️ Immediate action required!")
        else:
            st.warning("⚠️ Precautionary measures recommended")

# Educational Section
st.markdown("## 📚 Health Education & Awareness")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 💡 Water Safety Tips")
    safety_tips = [
        "Always boil water for at least 5 minutes before drinking",
        "Use water purification tablets when boiling is not possible",
        "Store treated water in clean, covered containers",
        "Wash hands frequently with soap and clean water",
        "Avoid ice unless made from safe water",
        "Eat hot, freshly cooked food",
        "Avoid raw vegetables and fruits unless you peel them yourself"
    ]
    
    for tip in safety_tips:
        st.markdown(f"• {tip}")

with col2:
    st.markdown("### 🧠 Quick Health Quiz")
    
    question = "What is the minimum time to boil water to make it safe for drinking?"
    options = ["1 minute", "3 minutes", "5 minutes", "10 minutes"]
    
    user_answer = st.radio(question, options)
    
    if st.button("Submit Answer"):
        if user_answer == "5 minutes":
            st.success("✅ Correct! Boiling water for at least 5 minutes kills most harmful bacteria and viruses.")
        else:
            st.error("❌ Incorrect. The correct answer is 5 minutes. Boiling for at least 5 minutes ensures water safety.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px;">
    <p>🌊 BlueAlert Smart Health Surveillance System | Prototype v1.0</p>
    <p>Developed for Smart India Hackathon | Monitoring Water-borne Diseases in Rural Areas</p>
</div>
""", unsafe_allow_html=True)