import streamlit as st
from streamlit import session_state as ss



# Page configuration
st.set_page_config(
    page_title="BlueAlert - Smart Health Surveillance",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Global CSS for modern matte blue-cyan theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #0f4c75 0%, #2a9d8f 100%);
        color: white;
        min-height: 100vh;
    }
    
    .stApp > header {
        background-color: transparent;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border-radius: 12px;
        padding: 24px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 16px 0;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    
    .card:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        border-color: rgba(255, 255, 255, 0.3);
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        margin: 10px 0;
        transition: all 0.2s ease;
        text-align: center;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 24px rgba(0, 0, 0, 0.15);
    }
    
    .alert-badge {
        background-color: #e74c3c;
        color: white;
        border-radius: 50%;
        width: 24px;
        height: 24px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        font-weight: bold;
        margin-left: 10px;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(231, 76, 60, 0.7); }
        70% { box-shadow: 0 0 0 8px rgba(231, 76, 60, 0); }
        100% { box-shadow: 0 0 0 0 rgba(231, 76, 60, 0); }
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2a9d8f 0%, #0f4c75 100%);
    }
    
    .nav-item {
        padding: 12px 16px;
        margin: 4px 0;
        border-radius: 8px;
        transition: all 0.2s ease;
        cursor: pointer;
        border: 1px solid transparent;
    }
    
    .nav-item:hover {
        background: rgba(255, 255, 255, 0.1);
        border-color: rgba(255, 255, 255, 0.2);
    }
    
    h1, h2, h3, h4 {
        color: white !important;
        font-weight: 600;
    }
    
    .stSelectbox > div > div,
    .stDateInput > div > div,
    .stMultiSelect > div > div {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
    }
    
    .stDataFrame {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        overflow: hidden;
    }
    
    .folium-map {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #2a9d8f, #0f4c75);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    .status-good { color: #27ae60; font-weight: 600; }
    .status-moderate { color: #f39c12; font-weight: 600; }
    .status-high { color: #e74c3c; font-weight: 600; }
    
    @media (max-width: 768px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        .card {
            margin: 8px 0;
            padding: 16px;
        }
        
        .folium-map {
            width: 100%;
            height: 50vh;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for persistent data
if 'sensor_data' not in ss:
    ss.sensor_data = {
        'TDS': 450,
        'Turbidity': 5.2,
        'Temperature': 28.5,
        'pH': 7.1
    }

if 'alert_count' not in ss:
    ss.alert_count = 3

if 'time_period' not in ss:
    ss.time_period = "Last Month"

if 'selected_district' not in ss:
    ss.selected_district = "All"

if 'age_filter' not in ss:
    ss.age_filter = "All"

if 'gender_filter' not in ss:
    ss.gender_filter = "All"

# Define pages
home_page = st.Page("pages/home.py", title="Home", icon="🏠")
map_page = st.Page("pages/map.py", title="Disease Map", icon="📍")
charts_page = st.Page("pages/charts.py", title="Analytics", icon="📊")
water_quality_page = st.Page("pages/water_quality.py", title="Water Quality", icon="💧")
alerts_page = st.Page("pages/alerts.py", title="Alerts", icon="🚨")
education_page = st.Page("pages/education.py", title="Education", icon="📚")

# Navigation
pg = st.navigation({
    "Dashboard": [home_page, map_page, charts_page],
    "Monitoring": [water_quality_page, alerts_page],
    "Resources": [education_page]
})

# Sidebar with branding and filters
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h2 style="color: white; margin: 0;">🌊 BlueAlert</h2>
        <p style="color: rgba(255, 255, 255, 0.8); margin: 5px 0 0 0;">Smart Health Surveillance</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Global filters in sidebar
    st.markdown("### 🎛️ Global Filters")
    
    # Time period filter
    ss.time_period = st.selectbox(
        "📅 Time Period",
        ["Last Week", "Last Month", "Last Year"],
        index=["Last Week", "Last Month", "Last Year"].index(ss.time_period)
    )
    
    # Location filter (will be used by map and charts)
    districts = ['All', 'Kamrup', 'Dibrugarh', 'Cachar', 'Aizawl', 'Imphal West', 'Kohima', 'East Khasi Hills', 'Papum Pare']
    ss.selected_district = st.selectbox(
        "📍 District Filter",
        districts,
        index=districts.index(ss.selected_district) if ss.selected_district in districts else 0
    )
    
    # Demographics filters
    ss.age_filter = st.selectbox(
        "👥 Age Group",
        ["All", "0-5", "6-18", "19-35", "36-60", "60+"],
        index=["All", "0-5", "6-18", "19-35", "36-60", "60+"].index(ss.age_filter)
    )
    
    ss.gender_filter = st.selectbox(
        "⚥ Gender",
        ["All", "Male", "Female"],
        index=["All", "Male", "Female"].index(ss.gender_filter)
    )
    
    st.markdown("---")
    
    # Status indicators
    st.markdown("### 📊 System Status")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Active Alerts", ss.alert_count, delta="2 new")
    with col2:
        st.metric("Sensors Online", "8/8", delta="All OK")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 10px;">
        <small style="color: rgba(255, 255, 255, 0.6);">
            BlueAlert v1.0<br>
            Smart India Hackathon 2024
        </small>
    </div>
    """, unsafe_allow_html=True)

# Run the selected page
pg.run()