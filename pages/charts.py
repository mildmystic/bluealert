import streamlit as st
from streamlit import session_state as ss
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import numpy as np

st.title("📊 Analytics Dashboard")
st.markdown("### Comprehensive data analysis and trend visualization")

@st.cache_data
def generate_disease_data():
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
def generate_demographic_data():
    """Generate demographic breakdown data"""
    age_groups = ['0-5', '6-18', '19-35', '36-60', '60+']
    diseases = ['Cholera', 'Typhoid', 'Diarrhea', 'Hepatitis A']
    
    data = []
    for disease in diseases:
        for age in age_groups:
            cases = random.randint(5, 50)
            data.append({
                'Disease': disease,
                'Age Group': age,
                'Cases': cases,
                'Male': random.randint(int(cases*0.4), int(cases*0.6)),
                'Female': cases - random.randint(int(cases*0.4), int(cases*0.6))
            })
    
    return pd.DataFrame(data)

# Disease Statistics Overview
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 📈 Disease Case Analysis")

disease_data = generate_disease_data()

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Cases by Disease Type")
    
    # Select data based on time period from sidebar
    period_col = ss.time_period
    chart_data = disease_data[['Disease', period_col]].copy()
    chart_data.columns = ['Disease', 'Cases']
    
    fig_bar = px.bar(
        chart_data,
        x='Disease',
        y='Cases',
        color='Cases',
        color_continuous_scale='Blues',
        title=f'Disease Cases - {ss.time_period}',
        text='Cases'
    )
    fig_bar.update_traces(textposition='outside')
    fig_bar.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        height=400
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.markdown("#### Disease Distribution")
    
    fig_pie = px.pie(
        chart_data,
        values='Cases',
        names='Disease',
        title=f'Disease Distribution - {ss.time_period}',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_pie.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        height=400
    )
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Trend Analysis
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 📉 Trend Analysis & Forecasting")

col1, col2 = st.columns([3, 1])

with col2:
    st.markdown("#### Controls")
    
    trends_data = generate_trends_data()
    selected_diseases = st.multiselect(
        "Select Diseases:",
        options=trends_data['Disease'].unique(),
        default=['Cholera', 'Diarrhea'],
        key="trend_diseases"
    )
    
    show_forecast = st.checkbox("Show AI Forecast", value=True)
    
    chart_type = st.selectbox(
        "Chart Type:",
        ["Line Chart", "Area Chart", "Scatter Plot"]
    )

with col1:
    if selected_diseases:
        filtered_trends = trends_data[trends_data['Disease'].isin(selected_diseases)]
        
        if not show_forecast:
            filtered_trends = filtered_trends[filtered_trends['Type'] == 'Actual']
        
        if chart_type == "Line Chart":
            fig_trend = px.line(
                filtered_trends,
                x='Date',
                y='Cases',
                color='Disease',
                line_dash='Type',
                title='Disease Trends Over Time'
            )
        elif chart_type == "Area Chart":
            fig_trend = px.area(
                filtered_trends,
                x='Date',
                y='Cases',
                color='Disease',
                title='Disease Trends Over Time'
            )
        else:  # Scatter Plot
            fig_trend = px.scatter(
                filtered_trends,
                x='Date',
                y='Cases',
                color='Disease',
                symbol='Type',
                title='Disease Cases Distribution'
            )
        
        fig_trend.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            height=400
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("Please select at least one disease to display trends.")

st.markdown('</div>', unsafe_allow_html=True)

# Demographic Analysis
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 👥 Demographic Analysis")

demographic_data = generate_demographic_data()

# Apply filters from sidebar
if ss.age_filter != "All":
    demographic_data = demographic_data[demographic_data['Age Group'] == ss.age_filter]

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Cases by Age Group")
    
    age_summary = demographic_data.groupby('Age Group')['Cases'].sum().reset_index()
    
    fig_age = px.bar(
        age_summary,
        x='Age Group',
        y='Cases',
        color='Cases',
        color_continuous_scale='Reds',
        title='Cases by Age Group'
    )
    fig_age.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        height=350
    )
    st.plotly_chart(fig_age, use_container_width=True)

with col2:
    st.markdown("#### Gender Distribution")
    
    # Create gender breakdown data
    gender_data = []
    for _, row in demographic_data.iterrows():
        gender_data.extend([
            {'Disease': row['Disease'], 'Age Group': row['Age Group'], 'Gender': 'Male', 'Cases': row['Male']},
            {'Disease': row['Disease'], 'Age Group': row['Age Group'], 'Gender': 'Female', 'Cases': row['Female']}
        ])
    
    gender_df = pd.DataFrame(gender_data)
    gender_summary = gender_df.groupby('Gender')['Cases'].sum().reset_index()
    
    fig_gender = px.pie(
        gender_summary,
        values='Cases',
        names='Gender',
        title='Gender Distribution',
        color_discrete_map={'Male': '#3498db', 'Female': '#e74c3c'}
    )
    fig_gender.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        height=350
    )
    st.plotly_chart(fig_gender, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Heatmap Analysis
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 🗂️ Disease-Age Group Heatmap")

# Create pivot table for heatmap
heatmap_data = demographic_data.pivot_table(
    values='Cases',
    index='Disease',
    columns='Age Group',
    aggfunc='sum',
    fill_value=0
)

fig_heatmap = px.imshow(
    heatmap_data,
    aspect='auto',
    color_continuous_scale='YlOrRd',
    title='Disease Cases by Age Group'
)

fig_heatmap.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='white',
    height=400
)

st.plotly_chart(fig_heatmap, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Correlation Analysis
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 🔗 Correlation Analysis")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Disease Correlation Matrix")
    
    # Create correlation data
    correlation_data = disease_data[['Cholera', 'Typhoid', 'Diarrhea', 'Hepatitis A', 'Dysentery']].T
    correlation_data.columns = ['Cases']
    correlation_data['Temperature'] = [28.5, 29.2, 27.8, 30.1, 28.9]
    correlation_data['Humidity'] = [85, 82, 88, 79, 86]
    correlation_data['Rainfall'] = [245, 198, 267, 189, 223]
    
    corr_matrix = correlation_data.corr()
    
    fig_corr = px.imshow(
        corr_matrix,
        color_continuous_scale='RdBu_r',
        aspect='auto',
        title='Environmental Factors Correlation'
    )
    
    fig_corr.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        height=300
    )
    
    st.plotly_chart(fig_corr, use_container_width=True)

with col2:
    st.markdown("#### Key Insights")
    
    insights = [
        "🌡️ **Temperature**: Moderate positive correlation with case counts",
        "💧 **Humidity**: Strong correlation with water-borne diseases",
        "🌧️ **Rainfall**: Seasonal peaks align with monsoon periods",
        "👥 **Age Groups**: Children (0-5) and elderly (60+) most vulnerable",
        "📊 **Peak Season**: Cases increase during June-September",
        "🏥 **Recovery Rate**: Improved from 78% to 85% this year"
    ]
    
    for insight in insights:
        st.markdown(f"- {insight}")
    
    st.markdown("---")
    st.markdown("#### Recommendations")
    recommendations = [
        "Increase water quality monitoring during monsoon",
        "Focus preventive measures on vulnerable age groups",
        "Deploy mobile health units to high-correlation areas"
    ]
    
    for rec in recommendations:
        st.markdown(f"✅ {rec}")

st.markdown('</div>', unsafe_allow_html=True)

# Data Export
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 📤 Export Analytics")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Generate Full Report", use_container_width=True):
        st.success("Comprehensive analytics report generated!")

with col2:
    # Prepare export data
    export_data = pd.merge(disease_data, demographic_data.groupby('Disease')['Cases'].sum(), 
                          left_on='Disease', right_index=True, suffixes=('_period', '_demographic'))
    
    st.download_button(
        label="📥 Download Data",
        data=export_data.to_csv(index=False),
        file_name=f"analytics_data_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )

with col3:
    if st.button("📧 Email Report", use_container_width=True):
        st.info("Report will be sent to registered health officials.")

st.markdown('</div>', unsafe_allow_html=True)