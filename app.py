import streamlit as st
import pandas as pd
import analysis # Import your local analysis module

# --- PAGE CONFIGURATION ---
st.set_page_config(layout="wide", page_title="Uber Data Dashboard")

st.title("🚖 NYC Uber Rides Analysis")
st.markdown("This dashboard visualizes Uber pickups in New York City to identify high-traffic areas and peak times.")

# --- DATA LOADING ---
@st.cache_data # Caches the data so it doesn't reload on every interaction
def get_data():
    # Make sure this path matches your actual file location
    path = "data/uber-raw-data.csv" 
    return analysis.load_and_clean_data(path)

try:
    df = get_data()
except FileNotFoundError:
    st.error("Error: 'uber-raw-data.csv' not found. Please place it in the 'data' folder.")
    st.stop()

# --- SIDEBAR CONTROLS ---
st.sidebar.header("Filter Options")

# Show Raw Data Toggle
if st.sidebar.checkbox('Show Raw Data'):
    st.subheader('Raw Data')
    st.write(df.head(50))

# Hour Slider
hour_selected = st.sidebar.slider("Select Hour of Day", 0, 23, 17) # Default to 5 PM (17:00)

# --- VISUALIZATION SECTION ---

# Row 1: Map and Histogram
col1, col2 = st.columns([2, 1]) # Makes the map column twice as wide as the chart

with col1:
    st.subheader(f"Map of Pickups at {hour_selected}:00")
    # Filter data by the selected hour
    filtered_data = df[df['Date/Time'].dt.hour == hour_selected]
    # Simple Streamlit Map
    st.map(filtered_data)

with col2:
    st.subheader("Total Rides by Hour")
    # Get histogram data using the helper function
    hist_values = analysis.get_peak_hours(df)
    st.bar_chart(hist_values)

# --- ADVANCED METRICS ---
st.markdown("---")
st.subheader("Quick Stats")
col3, col4, col5 = st.columns(3)

with col3:
    st.metric("Total Rides Loaded", f"{len(df):,}")
with col4:
    busiest_hour = df['hour'].mode()[0]
    st.metric("Busiest Hour of Day", f"{busiest_hour}:00")
with col5:
    peak_day = df['dom'].mode()[0]
    st.metric("Busiest Day of Month", f"Day {peak_day}")