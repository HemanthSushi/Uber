import pandas as pd

def load_uber_data(file_path):
    """Loads and cleans the Uber dataset."""
    df = pd.read_csv(file_path)
    
    # Convert string timestamps to Python datetime objects
    df['Date/Time'] = pd.to_datetime(df['Date/Time'])
    
    # Rename columns for Streamlit map compatibility (requires lowercase)
    df.rename(columns={'Lat': 'lat', 'Lon': 'lon'}, inplace=True)
    
    # Extract time features for analysis
    df['hour'] = df['Date/Time'].dt.hour
    df['weekday'] = df['Date/Time'].dt.weekday
    
    return df

def get_heatmap_data(df):
    """Creates a pivot table of rides by weekday and hour."""
    # Group by weekday and hour, then count occurrences
    table = df.groupby(['weekday', 'hour']).size().unstack()
    return table
