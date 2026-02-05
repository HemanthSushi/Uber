import streamlit as st
import pandas as pd
import analysis
import seaborn as sns
import matplotlib.pyplot as plt
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Uber Analysis Dashboard", layout="wide")
st.title("🚗 Uber NYC Data Analysis")

# --- DATA LOADING ---
# Ensure this matches your filename in Codespaces
DATA_FILE = 'uber-raw-data.csv'

if not os.path.exists(DATA_FILE):
    st.error(f"Error: {DATA_FILE} not found. Please ensure the file is in the main folder.")
    st.stop()

@st.cache_data
def load_data():
    return analysis.load_uber_data(DATA_FILE)

df = load_data()

# --- SIDEBAR ---
st.sidebar.header("Filter Map")
hour_to_filter = st.sidebar.slider('Select Hour of Day', 0, 23, 17)

# --- VISUAL 1: MAP ---
st.subheader(f"Pickup Locations at {hour_to_filter}:00")
map_filtered = df[df['hour'] == hour_to_filter]
st.map(map_filtered)

# --- VISUAL 2 & 3: GRAPHS ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Total Rides by Hour")
    hour_counts = df['hour'].value_counts().sort_index()
    st.bar_chart(hour_counts)

with col2:
    st.subheader("Demand Heatmap")
    heatmap_data = analysis.get_heatmap_data(df)
    
    fig, ax = plt.subplots()
    sns.heatmap(heatmap_data, cmap="YlGnBu", ax=ax)
    ax.set_yticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    plt.ylabel("Day of Week")
    plt.xlabel("Hour of Day")
    st.pyplot(fig)

# --- RAW DATA VIEW ---
if st.checkbox("Show Raw Data"):
    st.write(df.head(100))
