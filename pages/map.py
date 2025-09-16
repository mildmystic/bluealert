import streamlit as st
from streamlit import session_state as ss
import pandas as pd
import folium
from streamlit_folium import st_folium
import random

st.title("📍 Disease Hotspot Map")
st.markdown("### Interactive mapping of water-borne disease cases across Northeast India")

@st.cache_data
def generate_location_data():
    """Generate mock location data for Northeast India"""
    locations = [
        {'name': 'Guwahati', 'lat': 26.1445, 'lon': 91.7362, 'district': 'Kamrup', 'cases': 45, 'risk': 'high', 'population': 957352},
        {'name': 'Dibrugarh', 'lat': 27.4728, 'lon': 94.9120, 'district': 'Dibrugarh', 'cases': 12, 'risk': 'low', 'population': 154296},
        {'name': 'Silchar', 'lat': 24.8333, 'lon': 92.7789, 'district': 'Cachar', 'cases': 28, 'risk': 'moderate', 'population': 172830},
        {'name': 'Aizawl', 'lat': 23.7367, 'lon': 92.7173, 'district': 'Aizawl', 'cases': 35, 'risk': 'high', 'population': 293416},
        {'name': 'Imphal', 'lat': 24.8170, 'lon': 93.9368, 'district': 'Imphal West', 'cases': 8, 'risk': 'low', 'population': 264986},
        {'name': 'Kohima', 'lat': 25.6751, 'lon': 94.1086, 'district': 'Kohima', 'cases': 22, 'risk': 'moderate', 'population': 99039},
        {'name': 'Shillong', 'lat': 25.5788, 'lon': 91.8933, 'district': 'East Khasi Hills', 'cases': 18, 'risk': 'moderate', 'population': 143229},
        {'name': 'Itanagar', 'lat': 27.0844, 'lon': 93.6053, 'district': 'Papum Pare', 'cases': 6, 'risk': 'low', 'population': 44829},
        {'name': 'Jorhat', 'lat': 26.7509, 'lon': 94.2037, 'district': 'Jorhat', 'cases': 15, 'risk': 'moderate', 'population': 153889},
        {'name': 'Tezpur', 'lat': 26.6340, 'lon': 92.7933, 'district': 'Sonitpur', 'cases': 9, 'risk': 'low', 'population': 58851}
    ]
    return pd.DataFrame(locations)

# Load and filter location data
location_data = generate_location_data()

# Apply district filter from sidebar
if ss.selected_district != "All":
    filtered_locations = location_data[location_data['district'] == ss.selected_district]
    if filtered_locations.empty:
        st.info(f"No data available for {ss.selected_district} district.")
        filtered_locations = location_data
else:
    filtered_locations = location_data

# Map controls
st.markdown('<div class="card">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    show_risk_levels = st.multiselect(
        "Risk Levels to Display",
        options=['low', 'moderate', 'high'],
        default=['low', 'moderate', 'high'],
        key="risk_filter"
    )

with col2:
    map_style = st.selectbox(
        "Map Style",
        ["OpenStreetMap", "Satellite", "Terrain"],
        key="map_style"
    )

with col3:
    show_population = st.checkbox("Show Population Data", value=False)

st.markdown('</div>', unsafe_allow_html=True)

# Filter by selected risk levels
if show_risk_levels:
    filtered_locations = filtered_locations[filtered_locations['risk'].isin(show_risk_levels)]

# Create the map
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 🗺️ Interactive Disease Map")

# Determine map tile based on style selection
tile_mapping = {
    "OpenStreetMap": "OpenStreetMap",
    "Satellite": "Esri.WorldImagery",
    "Terrain": "Stamen Terrain"
}

m = folium.Map(
    location=[25.5, 93.0], 
    zoom_start=6,
    tiles=tile_mapping[map_style]
)

# Color mapping for risk levels
color_map = {'low': 'green', 'moderate': 'orange', 'high': 'red'}
risk_icons = {'low': '✅', 'moderate': '⚠️', 'high': '🚨'}

# Add markers
for idx, row in filtered_locations.iterrows():
    # Calculate incidence rate per 100k
    incidence_rate = round((row['cases'] / row['population']) * 100000, 1)
    
    popup_content = f"""
    <div style="min-width: 200px;">
        <h4 style="color: {color_map[row['risk']]}; margin: 0 0 10px 0;">
            {risk_icons[row['risk']]} {row['name']}
        </h4>
        <p><strong>District:</strong> {row['district']}</p>
        <p><strong>Total Cases:</strong> {row['cases']}</p>
        <p><strong>Risk Level:</strong> {row['risk'].title()}</p>
        <p><strong>Incidence Rate:</strong> {incidence_rate}/100k</p>
        {f"<p><strong>Population:</strong> {row['population']:,}</p>" if show_population else ""}
        <p><strong>Water Quality:</strong> {'Poor' if row['risk'] == 'high' else 'Moderate' if row['risk'] == 'moderate' else 'Good'}</p>
    </div>
    """
    
    # Create circle marker with size based on cases
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=max(8, min(row['cases'] / 2, 30)),  # Scale radius with cases
        popup=folium.Popup(popup_content, max_width=300),
        tooltip=f"{row['name']}: {row['cases']} cases ({row['risk']} risk)",
        color=color_map[row['risk']],
        fillColor=color_map[row['risk']],
        fillOpacity=0.7,
        weight=2
    ).add_to(m)

# Add a legend
legend_html = '''
<div style="position: fixed; 
            top: 10px; right: 10px; width: 150px; height: 120px; 
            background-color: white; border:2px solid grey; z-index:9999; 
            font-size:14px; padding: 10px;">
<p style="margin: 0;"><strong>Risk Levels</strong></p>
<p style="margin: 5px 0;"><i class="fa fa-circle" style="color:red"></i> High Risk</p>
<p style="margin: 5px 0;"><i class="fa fa-circle" style="color:orange"></i> Moderate</p>
<p style="margin: 5px 0;"><i class="fa fa-circle" style="color:green"></i> Low Risk</p>
</div>
'''

m.get_root().html.add_child(folium.Element(legend_html))

# Display the map
map_data = st_folium(m, width=None, height=500, returned_objects=["last_object_clicked"])

st.markdown('</div>', unsafe_allow_html=True)

# Statistics panel
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 📊 Regional Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_cases = filtered_locations['cases'].sum()
    st.metric("Total Cases", total_cases)

with col2:
    high_risk_areas = len(filtered_locations[filtered_locations['risk'] == 'high'])
    st.metric("High Risk Areas", high_risk_areas)

with col3:
    avg_cases = round(filtered_locations['cases'].mean(), 1)
    st.metric("Avg Cases per Area", avg_cases)

with col4:
    total_population = filtered_locations['population'].sum()
    overall_rate = round((total_cases / total_population) * 100000, 1)
    st.metric("Incidence Rate", f"{overall_rate}/100k")

st.markdown('</div>', unsafe_allow_html=True)

# Detailed location data
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 📋 Location Details")

# Add search functionality
search_term = st.text_input("🔍 Search locations:", placeholder="Enter city or district name")

display_data = filtered_locations.copy()
if search_term:
    display_data = display_data[
        display_data['name'].str.contains(search_term, case=False, na=False) |
        display_data['district'].str.contains(search_term, case=False, na=False)
    ]

# Calculate additional metrics
display_data['Incidence Rate'] = round((display_data['cases'] / display_data['population']) * 100000, 1)
display_data['Risk Score'] = display_data['risk'].map({'low': 1, 'moderate': 2, 'high': 3})

# Sort by cases (descending)
display_data = display_data.sort_values('cases', ascending=False)

# Format the display
formatted_data = display_data[['name', 'district', 'cases', 'risk', 'Incidence Rate', 'population']].copy()
formatted_data.columns = ['Location', 'District', 'Cases', 'Risk Level', 'Rate per 100k', 'Population']
formatted_data['Risk Level'] = formatted_data['Risk Level'].str.title()
formatted_data['Population'] = formatted_data['Population'].apply(lambda x: f"{x:,}")

st.dataframe(
    formatted_data,
    use_container_width=True,
    hide_index=True
)

if display_data.empty and search_term:
    st.info(f"No locations found matching '{search_term}'")

st.markdown('</div>', unsafe_allow_html=True)

# Map interaction feedback
if map_data['last_object_clicked']:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🎯 Selected Location Details")
    
    clicked_lat = map_data['last_object_clicked']['lat']
    clicked_lng = map_data['last_object_clicked']['lng']
    
    # Find the closest location
    distances = []
    for idx, row in filtered_locations.iterrows():
        dist = ((row['lat'] - clicked_lat) ** 2 + (row['lon'] - clicked_lng) ** 2) ** 0.5
        distances.append((dist, idx, row))
    
    if distances:
        _, _, closest_location = min(distances)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            **📍 {closest_location['name']}**
            - **District:** {closest_location['district']}
            - **Total Cases:** {closest_location['cases']}
            - **Risk Level:** {closest_location['risk'].title()}
            - **Population:** {closest_location['population']:,}
            """)
        
        with col2:
            incidence = round((closest_location['cases'] / closest_location['population']) * 100000, 1)
            risk_color = color_map[closest_location['risk']]
            
            st.markdown(f"""
            **📊 Statistics**
            - **Incidence Rate:** {incidence} per 100k
            - **Risk Status:** <span style="color: {risk_color};">●</span> {closest_location['risk'].title()}
            - **Water Quality:** {'Poor' if closest_location['risk'] == 'high' else 'Good'}
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Export options
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 💾 Export Data")

col1, col2 = st.columns(2)

with col1:
    if st.button("📊 Generate Report", use_container_width=True):
        st.success("Report generated! Check your downloads folder.")

with col2:
    csv_data = display_data.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv_data,
        file_name=f"disease_map_data_{ss.selected_district}_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )

st.markdown('</div>', unsafe_allow_html=True)