import streamlit as st
from streamlit import session_state as ss
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

st.title("🌊 BlueAlert Dashboard")
st.markdown("### Real-time Health Surveillance Overview")

# Quick stats cards
st.markdown('<div class="card">', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h3 style="color: #27ae60; margin: 0;">142</h3>
        <p style="margin: 5px 0 0 0; opacity: 0.8;">Total Cases</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h3 style="color: #f39c12; margin: 0;">12</h3>
        <p style="margin: 5px 0 0 0; opacity: 0.8;">High Risk Areas</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h3 style="color: #3498db; margin: 0;">8</h3>
        <p style="margin: 5px 0 0 0; opacity: 0.8;">Active Sensors</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <h3 style="color: #e74c3c; margin: 0;">{}</h3>
        <p style="margin: 5px 0 0 0; opacity: 0.8;">Active Alerts</p>
    </div>
    """.format(ss.alert_count), unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Recent activity and trends
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📈 Disease Trends (Last 30 Days)")
    
    # Generate mock trend data
    dates = pd.date_range(start='2024-08-01', end='2024-08-31', freq='D')
    diseases = ['Cholera', 'Typhoid', 'Diarrhea', 'Hepatitis A']
    
    trend_data = []
    for disease in diseases:
        base_cases = random.randint(1, 8)
        for i, date in enumerate(dates):
            cases = max(0, base_cases + random.randint(-3, 5))
            trend_data.append({
                'Date': date,
                'Disease': disease,
                'Cases': cases
            })
    
    trend_df = pd.DataFrame(trend_data)
    
    fig = px.line(
        trend_df,
        x='Date',
        y='Cases',
        color='Disease',
        title='Daily Case Reports'
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        showlegend=True,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🚨 Recent Alerts")
    
    recent_alerts = [
        {"time": "2 hours ago", "type": "High TDS", "location": "Guwahati", "severity": "high"},
        {"time": "5 hours ago", "type": "Cholera Outbreak", "location": "Aizawl", "severity": "high"},
        {"time": "1 day ago", "type": "Water Quality", "location": "Silchar", "severity": "moderate"},
        {"time": "2 days ago", "type": "Turbidity Alert", "location": "Dibrugarh", "severity": "moderate"},
    ]
    
    for alert in recent_alerts:
        severity_color = "#e74c3c" if alert["severity"] == "high" else "#f39c12"
        st.markdown(f"""
        <div style="
            background: rgba(255, 255, 255, 0.05);
            padding: 12px;
            border-radius: 8px;
            margin: 8px 0;
            border-left: 4px solid {severity_color};
        ">
            <strong style="color: {severity_color};">{alert['type']}</strong><br>
            <small style="opacity: 0.8;">{alert['location']} • {alert['time']}</small>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("View All Alerts", key="view_alerts"):
        st.switch_page("pages/alerts.py")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Water quality summary
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 💧 Current Water Quality Status")

col1, col2, col3, col4 = st.columns(4)

def get_status_class(value, thresholds, reverse=False):
    if reverse:
        if value < thresholds[0]: return "status-high"
        elif value < thresholds[1]: return "status-moderate"
        else: return "status-good"
    else:
        if value > thresholds[1]: return "status-high"
        elif value > thresholds[0]: return "status-moderate"
        else: return "status-good"

def get_status_text(value, thresholds, reverse=False):
    if reverse:
        if value < thresholds[0]: return "Poor"
        elif value < thresholds[1]: return "Fair"
        else: return "Good"
    else:
        if value > thresholds[1]: return "High"
        elif value > thresholds[0]: return "Moderate"
        else: return "Good"

with col1:
    tds_value = ss.sensor_data['TDS']
    tds_class = get_status_class(tds_value, [300, 500])
    tds_status = get_status_text(tds_value, [300, 500])
    
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="margin: 0;">TDS Level</h4>
        <h2 style="margin: 5px 0; color: white;">{tds_value} <small>ppm</small></h2>
        <p class="{tds_class}" style="margin: 0;">{tds_status}</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    turbidity = ss.sensor_data['Turbidity']
    turb_class = get_status_class(turbidity, [3, 8])
    turb_status = get_status_text(turbidity, [3, 8])
    
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="margin: 0;">Turbidity</h4>
        <h2 style="margin: 5px 0; color: white;">{turbidity} <small>NTU</small></h2>
        <p class="{turb_class}" style="margin: 0;">{turb_status}</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    temp = ss.sensor_data['Temperature']
    temp_class = get_status_class(temp, [25, 32])
    temp_status = "Normal" if 20 <= temp <= 30 else "High"
    
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="margin: 0;">Temperature</h4>
        <h2 style="margin: 5px 0; color: white;">{temp} <small>°C</small></h2>
        <p class="{temp_class}" style="margin: 0;">{temp_status}</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    ph = ss.sensor_data['pH']
    ph_class = "status-good" if 6.5 <= ph <= 8.5 else "status-high"
    ph_status = "Good" if 6.5 <= ph <= 8.5 else "Poor"
    
    st.markdown(f"""
    <div class="metric-card">
        <h4 style="margin: 0;">pH Level</h4>
        <h2 style="margin: 5px 0; color: white;">{ph}</h2>
        <p class="{ph_class}" style="margin: 0;">{ph_status}</p>
    </div>
    """, unsafe_allow_html=True)

if st.button("View Detailed Water Quality", key="view_water_quality"):
    st.switch_page("pages/water_quality.py")

st.markdown('</div>', unsafe_allow_html=True)

# Regional overview
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 🗺️ Regional Disease Distribution")

# Mock regional data
regional_data = pd.DataFrame({
    'District': ['Kamrup', 'Dibrugarh', 'Cachar', 'Aizawl', 'Imphal West', 'Kohima'],
    'Cases': [45, 12, 28, 35, 8, 22],
    'Risk Level': ['High', 'Low', 'Moderate', 'High', 'Low', 'Moderate']
})

fig = px.bar(
    regional_data,
    x='District',
    y='Cases',
    color='Risk Level',
    color_discrete_map={'High': '#e74c3c', 'Moderate': '#f39c12', 'Low': '#27ae60'},
    title='Cases by District'
)

fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='white',
    height=300
)

st.plotly_chart(fig, use_container_width=True)

if st.button("View Interactive Map", key="view_map"):
    st.switch_page("pages/map.py")

st.markdown('</div>', unsafe_allow_html=True)

# Quick actions
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### ⚡ Quick Actions")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🗺️ View Disease Map", use_container_width=True):
        st.switch_page("pages/map.py")

with col2:
    if st.button("📊 Analyze Trends", use_container_width=True):
        st.switch_page("pages/charts.py")

with col3:
    if st.button("💧 Check Water Quality", use_container_width=True):
        st.switch_page("pages/water_quality.py")

with col4:
    if st.button("📚 Health Education", use_container_width=True):
        st.switch_page("pages/education.py")

st.markdown('</div>', unsafe_allow_html=True)