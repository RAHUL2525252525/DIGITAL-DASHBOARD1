import pandas as pd
import os

DATA_DIR = 'data'

def load_campaign_data():
    """Loads and cleans the main campaign summary data."""
    try:
        path = os.path.join(DATA_DIR, 'campaigns.csv')
        df = pd.read_csv(path)
        # Ensure numeric columns are actually numbers
        numeric_cols = ['spend', 'revenue', 'clicks', 'conversions', 'reach']
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        return df
    except Exception as e:
        print(f"Error loading campaigns: {e}")
        return pd.DataFrame()

def load_detailed_clicks():
    """Loads daily click data for engagement graphs."""
    path = os.path.join(DATA_DIR, 'clicks.csv')
    return pd.read_csv(path) if os.path.exists(path) else pd.DataFrame()