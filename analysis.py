import pandas as pd
import numpy as np

def load_and_clean_data(file_path):
    """
    Loads the CSV data and performs necessary cleaning and feature engineering.
    """
    # Load data
    data = pd.read_csv(file_path)
    
    # Rename columns to be compatible with Streamlit's map (requires 'lat', 'lon')
    # Adjust 'Lat'/'Lon' based on your specific CSV headers
    data.rename(columns={'Lat': 'lat', 'Lon': 'lon', 'Base': 'base'}, inplace=True)
    
    # Convert Date/Time string to datetime objects
    data['Date/Time'] = pd.to_datetime(data['Date/Time'])
    
    # Feature Engineering: Extract useful components
    data['dom'] = data['Date/Time'].dt.day          # Day of Month
    data['weekday'] = data['Date/Time'].dt.weekday  # Day of Week (0=Monday)
    data['hour'] = data['Date/Time'].dt.hour        # Hour of Day
    
    return data

def get_peak_hours(data):
    """
    Returns a histogram of rides per hour.
    """
    return np.histogram(data['Date/Time'].dt.hour, bins=24, range=(0,24))[0]