import streamlit as st
from streamlit import session_state as ss
import pandas as pd
from datetime import datetime, timedelta
import random

st.title("🚨 Health & Safety Alerts")
st.markdown("### Real-time notifications and emergency warnings")

# Mock alert data
@st.cache_data
def generate_alerts_data():
    alerts = [
        {
            "id": 1,
            "type": "Water Quality",
            "title": "High TDS Levels Detected",
            "message": "TDS levels in Guwahati district exceed 600 ppm. Immediate water treatment recommended.",
            "severity": "high",
            "location": "Guwahati, Kamrup",
            "time": datetime.now() - timedelta(hours=2),
            "status": "active",
            "affected_population": 25000,
            "source": "Sensor Network"
        },
        {
            "id": 2,
            "type": "Disease Outbreak",
            "title": "Cholera Cases Rising",
            "message": "15 new cholera cases reported in Aizawl region. Enhanced surveillance activated.",
            "severity": "critical",
            "location": "Aizawl, Mizoram",
            "time": datetime.now() - timedelta(hours=5),
            "status": "active",
            "affected_population": 8000,
            "source": "Health Department"
        },
        {
            "id": 3,
            "type": "Water Contamination",
            "title": "Turbidity Alert",
            "message": "High turbidity detected in Silchar water supply. Boiling water recommended.",
            "severity": "moderate",
            "location": "Silchar, Cachar",
            "time": datetime.now() - timedelta(days=1),
            "status": "monitoring",
            "affected_population": 12000,
            "source": "Sensor Network"
        },
        {
            "id": 4,
            "type": "System Alert",
            "title": "Sensor Maintenance Required",
            "message": "Sensor S004 at Distribution Point 2 requires maintenance check.",
            "severity": "low",
            "location": "Dibrugarh District",
            "time": datetime.now() - timedelta(days=2),
            "status": "scheduled",
            "affected_population": 0,
            "source": "System Monitoring"
        },
        {
            "id": 5,
            "type": "Environmental",
            "title": "Monsoon Water Quality Warning",
            "message": "Heavy rainfall may affect water quality. Increased monitoring activated.",
            "severity": "moderate",
            "location": "Regional",
            "time": datetime.now() - timedelta(days=3),
            "status": "resolved",
            "affected_population": 50000,
            "source": "Weather Service"
        }
    ]
    return alerts

alerts_data = generate_alerts_data()

# Alert summary cards
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 📊 Alert Summary")

col1, col2, col3, col4 = st.columns(4)

active_alerts = [a for a in alerts_data if a['status'] == 'active']
critical_alerts = [a for a in alerts_data if a['severity'] == 'critical']
total_affected = sum(a['affected_population'] for a in active_alerts)

with col1:
    st.markdown(f"""
    <div class="metric-card" style="border-left: 4px solid #e74c3c;">
        <h3 style="color: #e74c3c; margin: 0;">{len(active_alerts)}</h3>
        <p style="margin: 5px 0 0 0; opacity: 0.8;">Active Alerts</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card" style="border-left: 4px solid #c0392b;">
        <h3 style="color: #c0392b; margin: 0;">{len(critical_alerts)}</h3>
        <p style="margin: 5px 0 0 0; opacity: 0.8;">Critical Alerts</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card" style="border-left: 4px solid #f39c12;">
        <h3 style="color: #f39c12; margin: 0;">{total_affected:,}</h3>
        <p style="margin: 5px 0 0 0; opacity: 0.8;">People Affected</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    response_time = "< 2 hrs"
    st.markdown(f"""
    <div class="metric-card" style="border-left: 4px solid #27ae60;">
        <h3 style="color: #27ae60; margin: 0;">{response_time}</h3>
        <p style="margin: 5px 0 0 0; opacity: 0.8;">Avg Response Time</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Filters and controls
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 🎛️ Alert Filters")

col1, col2, col3, col4 = st.columns(4)

with col1:
    severity_filter = st.multiselect(
        "Severity Level",
        options=['critical', 'high', 'moderate', 'low'],
        default=['critical', 'high', 'moderate', 'low']
    )

with col2:
    type_filter = st.multiselect(
        "Alert Type",
        options=['Water Quality', 'Disease Outbreak', 'Water Contamination', 'System Alert', 'Environmental'],
        default=['Water Quality', 'Disease Outbreak', 'Water Contamination']
    )

with col3:
    status_filter = st.multiselect(
        "Status",
        options=['active', 'monitoring', 'scheduled', 'resolved'],
        default=['active', 'monitoring']
    )

with col4:
    time_filter = st.selectbox(
        "Time Range",
        options=['All Time', 'Last 24 Hours', 'Last Week', 'Last Month']
    )

st.markdown('</div>', unsafe_allow_html=True)

# Filter alerts based on selection
filtered_alerts = alerts_data.copy()

if severity_filter:
    filtered_alerts = [a for a in filtered_alerts if a['severity'] in severity_filter]
if type_filter:
    filtered_alerts = [a for a in filtered_alerts if a['type'] in type_filter]
if status_filter:
    filtered_alerts = [a for a in filtered_alerts if a['status'] in status_filter]

# Time filtering
if time_filter != 'All Time':
    cutoff_times = {
        'Last 24 Hours': datetime.now() - timedelta(days=1),
        'Last Week': datetime.now() - timedelta(weeks=1),
        'Last Month': datetime.now() - timedelta(days=30)
    }
    cutoff = cutoff_times[time_filter]
    filtered_alerts = [a for a in filtered_alerts if a['time'] >= cutoff]

# Active alerts list
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown(f"### 🔔 Current Alerts ({len(filtered_alerts)} found)")

if not filtered_alerts:
    st.info("No alerts match the current filters.")
else:
    # Sort by severity and time
    severity_order = {'critical': 0, 'high': 1, 'moderate': 2, 'low': 3}
    filtered_alerts.sort(key=lambda x: (severity_order[x['severity']], -x['time'].timestamp()))
    
    for alert in filtered_alerts:
        severity_colors = {
            'critical': '#c0392b',
            'high': '#e74c3c',
            'moderate': '#f39c12',
            'low': '#3498db'
        }
        
        severity_icons = {
            'critical': '🆘',
            'high': '🚨',
            'moderate': '⚠️',
            'low': 'ℹ️'
        }
        
        status_colors = {
            'active': '#e74c3c',
            'monitoring': '#f39c12',
            'scheduled': '#3498db',
            'resolved': '#27ae60'
        }
        
        time_ago = datetime.now() - alert['time']
        if time_ago.days > 0:
            time_str = f"{time_ago.days} day{'s' if time_ago.days > 1 else ''} ago"
        elif time_ago.seconds > 3600:
            hours = time_ago.seconds // 3600
            time_str = f"{hours} hour{'s' if hours > 1 else ''} ago"
        else:
            minutes = time_ago.seconds // 60
            time_str = f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        
        with st.expander(f"{severity_icons[alert['severity']]} {alert['title']} - {alert['location']}", 
                        expanded=alert['severity'] in ['critical', 'high']):
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                **{alert['message']}**
                
                📍 **Location:** {alert['location']}  
                🕐 **Time:** {time_str}  
                📊 **Source:** {alert['source']}  
                👥 **Affected Population:** {alert['affected_population']:,} people  
                """)
                
                # Action buttons based on alert type
                if alert['type'] == 'Water Quality':
                    if st.button(f"View Water Quality Data", key=f"water_{alert['id']}"):
                        st.switch_page("pages/water_quality.py")
                elif alert['type'] == 'Disease Outbreak':
                    if st.button(f"View Disease Map", key=f"map_{alert['id']}"):
                        st.switch_page("pages/map.py")
            
            with col2:
                st.markdown(f"""
                <div style="text-align: center;">
                    <div style="
                        background: {severity_colors[alert['severity']]};
                        color: white;
                        padding: 8px 16px;
                        border-radius: 20px;
                        font-weight: bold;
                        font-size: 12px;
                        margin: 8px 0;
                    ">
                        {alert['severity'].upper()}
                    </div>
                    <div style="
                        background: {status_colors[alert['status']]};
                        color: white;
                        padding: 6px 12px;
                        border-radius: 16px;
                        font-size: 11px;
                        margin: 4px 0;
                    ">
                        {alert['status'].upper()}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if alert['status'] == 'active':
                    if st.button("Mark Resolved", key=f"resolve_{alert['id']}", type="primary"):
                        st.success(f"Alert {alert['id']} marked as resolved!")

st.markdown('</div>', unsafe_allow_html=True)

# Emergency contacts and procedures
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 📞 Emergency Response")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Emergency Contacts")
    contacts = [
        {"role": "Health Emergency", "number": "102", "available": "24/7"},
        {"role": "Water Quality Lab", "number": "+91-361-2345678", "available": "9 AM - 6 PM"},
        {"role": "District Collector", "number": "+91-361-2456789", "available": "24/7"},
        {"role": "Public Health Officer", "number": "+91-361-2567890", "available": "8 AM - 8 PM"},
        {"role": "Emergency Response Team", "number": "+91-361-2678901", "available": "24/7"}
    ]
    
    for contact in contacts:
        st.markdown(f"""
        <div style="
            background: rgba(255, 255, 255, 0.05);
            padding: 12px;
            border-radius: 8px;
            margin: 8px 0;
            border-left: 4px solid #27ae60;
        ">
            <strong>{contact['role']}</strong><br>
            📞 {contact['number']}<br>
            <small style="opacity: 0.8;">Available: {contact['available']}</small>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("#### Immediate Actions")
    
    action_steps = [
        {"condition": "Water Contamination", "steps": [
            "Stop using contaminated water immediately",
            "Switch to bottled/treated water",
            "Notify local health authorities",
            "Follow boiling guidelines"
        ]},
        {"condition": "Disease Outbreak", "steps": [
            "Seek immediate medical attention",
            "Isolate affected individuals",
            "Report to surveillance system",
            "Follow hygiene protocols"
        ]},
        {"condition": "Sensor Failure", "steps": [
            "Switch to backup monitoring",
            "Increase manual testing",
            "Schedule maintenance",
            "Update stakeholders"
        ]}
    ]
    
    for action in action_steps:
        with st.expander(f"📋 {action['condition']}"):
            for i, step in enumerate(action['steps'], 1):
                st.markdown(f"{i}. {step}")

st.markdown('</div>', unsafe_allow_html=True)

# Alert statistics and analytics
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 📈 Alert Analytics")

# Generate mock alert statistics
alert_stats = pd.DataFrame({
    'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug'],
    'Total Alerts': [12, 8, 15, 22, 18, 35, 28, 19],
    'Critical': [2, 1, 3, 5, 4, 8, 6, 4],
    'Resolved': [10, 7, 13, 20, 16, 32, 25, 17]
})

col1, col2 = st.columns(2)

with col1:
    # Alert trends
    import plotly.express as px
    
    fig_trends = px.line(
        alert_stats,
        x='Month',
        y=['Total Alerts', 'Critical', 'Resolved'],
        title='Alert Trends Over Time'
    )
    
    fig_trends.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        height=300
    )
    
    st.plotly_chart(fig_trends, use_container_width=True)

with col2:
    # Alert types distribution
    alert_types = pd.DataFrame({
        'Type': ['Water Quality', 'Disease Outbreak', 'System Alert', 'Environmental'],
        'Count': [45, 28, 15, 12]
    })
    
    fig_types = px.pie(
        alert_types,
        values='Count',
        names='Type',
        title='Alert Types Distribution'
    )
    
    fig_types.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        height=300
    )
    
    st.plotly_chart(fig_types, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Notification settings
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 🔔 Notification Settings")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### Alert Preferences")
    
    email_alerts = st.checkbox("📧 Email Notifications", value=True)
    sms_alerts = st.checkbox("📱 SMS Alerts", value=True)
    app_notifications = st.checkbox("📲 App Notifications", value=True)
    dashboard_alerts = st.checkbox("🖥️ Dashboard Alerts", value=True)

with col2:
    st.markdown("#### Severity Levels")
    
    critical_notify = st.checkbox("🆘 Critical", value=True)
    high_notify = st.checkbox("🚨 High", value=True)
    moderate_notify = st.checkbox("⚠️ Moderate", value=False)
    low_notify = st.checkbox("ℹ️ Low", value=False)

with col3:
    st.markdown("#### Quiet Hours")
    
    quiet_hours = st.checkbox("🌙 Enable Quiet Hours", value=False)
    if quiet_hours:
        quiet_start = st.time_input("Start Time", value=datetime.strptime("22:00", "%H:%M").time())
        quiet_end = st.time_input("End Time", value=datetime.strptime("07:00", "%H:%M").time())
        st.caption("Non-critical alerts will be suppressed during these hours")

if st.button("💾 Save Notification Settings", type="primary"):
    st.success("Notification preferences updated successfully!")

st.markdown('</div>', unsafe_allow_html=True)

# Recent alert activity feed
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 📰 Recent Activity Feed")

activity_feed = [
    {"time": "2 minutes ago", "action": "New critical alert generated", "details": "Cholera outbreak in Aizawl"},
    {"time": "15 minutes ago", "action": "Alert resolved", "details": "Water quality restored in Jorhat"},
    {"time": "1 hour ago", "action": "Sensor maintenance scheduled", "details": "S004 - Distribution Point 2"},
    {"time": "2 hours ago", "action": "High TDS alert triggered", "details": "Guwahati district"},
    {"time": "3 hours ago", "action": "System health check completed", "details": "All sensors operational"},
    {"time": "5 hours ago", "action": "Weekly report generated", "details": "Water quality summary"},
    {"time": "6 hours ago", "action": "Alert escalated", "details": "No response to turbidity warning"},
    {"time": "8 hours ago", "action": "New user registered", "details": "Health officer from Imphal"}
]

for activity in activity_feed:
    st.markdown(f"""
    <div style="
        background: rgba(255, 255, 255, 0.03);
        padding: 12px 16px;
        border-radius: 6px;
        margin: 6px 0;
        border-left: 3px solid #3498db;
    ">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <strong>{activity['action']}</strong>
            <small style="opacity: 0.6;">{activity['time']}</small>
        </div>
        <p style="margin: 4px 0 0 0; opacity: 0.8; font-size: 14px;">{activity['details']}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)