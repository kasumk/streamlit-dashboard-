import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# Generate random data for the example
np.random.seed(42)

# Generate time series data
timestamps = pd.date_range(datetime(2023, 1, 1), datetime(2023, 1, 31), freq='H')

# Generate random latitude and longitude data
latitude = np.random.uniform(37.0, 38.0, len(timestamps))
longitude = np.random.uniform(-122.0, -121.0, len(timestamps))

# Generate random speed data
speed = np.random.uniform(0, 100, len(timestamps))

# Generate random maintenance, speed, and accident alerts
maintenance_alert = np.random.choice([0, 1], len(timestamps), p=[0.9, 0.1])
speed_alert = np.random.choice([0, 1], len(timestamps), p=[0.8, 0.2])
accident_alert = np.random.choice([0, 1], len(timestamps), p=[0.95, 0.05])

# Create the DataFrame
data = pd.DataFrame({
    'timestamp': timestamps,
    'latitude': latitude,
    'longitude': longitude,
    'speed': speed,
    'maintenance_alert': maintenance_alert,
    'speed_alert': speed_alert,
    'accident_alert': accident_alert
})

# Calculate total distance traveled
data['distance'] = data['speed'] * 1  # Assuming 1 hour time interval

# Create a Streamlit app
st.set_page_config(page_title="Vehicle Dashboard", page_icon="🚗")

# Sidebar for filters
st.sidebar.header("Filters")
start_date = st.sidebar.date_input("Start Date", min(data['timestamp']))
end_date = st.sidebar.date_input("End Date", max(data['timestamp'])) + timedelta(days=1)

# Convert the 'timestamp' column to date objects for comparison
data['date'] = data['timestamp'].dt.date

# Filter data based on selected dates
filtered_data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]

# Title
st.title("Vehicle Dashboard")

# Location History Map
st.header("Location History Map")
st.map(filtered_data)

# Speed History Line Chart
st.header("Speed History Chart")
fig_speed_history = px.line(filtered_data, x='timestamp', y='speed', title='Speed History')
st.plotly_chart(fig_speed_history)

# Speed Level Info
st.header("Speed Level")
avg_speed = filtered_data['speed'].mean()
st.info(f"Average Speed: {avg_speed:.2f} km/h")

# Maintenance Alert Warning
st.header("Maintenance Alert")
maintenance_alert_count = filtered_data['maintenance_alert'].sum()
st.warning(f"Number of Maintenance Alerts: {maintenance_alert_count}")

# Speed Alert Error
st.header("Speed Alert")
speed_alert_count = filtered_data['speed_alert'].sum()
st.error(f"Number of Speed Alerts: {speed_alert_count}")

# Accident Alert Success
st.header("Accident Alert")
accident_alert_count = filtered_data['accident_alert'].sum()
st.success(f"Number of Accident Alerts: {accident_alert_count}")

# Total Distance Traveled Info
st.header("Total Distance Traveled")
total_distance = filtered_data['distance'].sum()
st.info(f"Total Distance Traveled: {total_distance:.2f} km")

# Bar Chart for Maintenance, Speed, and Accident Alerts
st.header("Alerts Overview Chart")
alert_counts = filtered_data[['maintenance_alert', 'speed_alert', 'accident_alert']].sum()
fig_alerts_bar = px.bar(x=alert_counts.index, y=alert_counts.values, labels={'x': 'Alert Type', 'y': 'Number of Alerts'},
                        title='Alerts Overview')
st.plotly_chart(fig_alerts_bar)

# Pie Chart for Maintenance, Speed, and Accident Alerts
st.header("Alerts Distribution Chart")
fig_alerts_pie = px.pie(values=alert_counts.values, names=alert_counts.index, title='Alerts Distribution')
st.plotly_chart(fig_alerts_pie)
