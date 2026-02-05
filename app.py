import streamlit as st
import pandas as pd
import analysis
import seaborn as sns
import matplotlib.pyplot as plt
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Uber NYC Dashboard", layout="wide")
st.title("🚗 Uber NYC Pickup Analysis")

# --- FILE PATH CONFIGURATION ---
# Updated to look inside the 'data' folder
DATA_FILE = 'data/uber-raw-data.csv'

# Safety check to prevent app crashes
if not os.path.exists(DATA_FILE):
    st.error(f"File not found at: {DATA_FILE}")
    st.info("Please make sure the 'data' folder exists and contains 'uber-raw-data.csv'.")
    st.stop()

@st.cache_data
def load_data():
    return analysis.load_uber_data(DATA_FILE)

# Load the dataset
df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Map Filters")
hour_to_filter = st.sidebar.slider('Select Hour of Day', 0, 23, 17)

# --- VISUALS ---
# 1. Pickup Map
st.subheader(f"Pickup Hotspots at {hour_to_filter}:00")
map_filtered = df[df['hour'] == hour_to_filter]
st.map(map_filtered)

# 2. Charts Row
col1, col2 = st.columns(2)

with col1:
    st.subheader("Total Rides by Hour")
    hour_counts = df['hour'].value_counts().sort_index()
    st.bar_chart(hour_counts)

with col2:
    st.subheader("Weekly Demand Heatmap")
    heatmap_data = analysis.get_heatmap_data(df)
    
    # Plotting the heatmap
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(heatmap_data, cmap="YlGnBu", ax=ax)
    ax.set_yticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    plt.ylabel("Day of Week")
    plt.xlabel("Hour of Day")
    st.pyplot(fig)

# 3. Data Inspection
if st.checkbox("Show Sample Raw Data"):
    st.write(df.head(50))
