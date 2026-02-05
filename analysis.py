import pandas as pd

def load_uber_data(file_path):
    """Loads and cleans the Uber dataset from the specified path."""
    df = pd.read_csv(file_path)
    
    # Convert timestamps to datetime objects
    df['Date/Time'] = pd.to_datetime(df['Date/Time'])
    
    # Rename columns for Streamlit map compatibility (lat/lon must be lowercase)
    df.rename(columns={'Lat': 'lat', 'Lon': 'lon'}, inplace=True)
    
    # Extract time features
    df['hour'] = df['Date/Time'].dt.hour
    df['weekday'] = df['Date/Time'].dt.weekday
    
    return df

def get_heatmap_data(df):
    """Creates a pivot table of ride counts by weekday and hour."""
    # Group by weekday (0-6) and hour (0-23)
    table = df.groupby(['weekday', 'hour']).size().unstack()
    return table
