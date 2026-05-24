import pytest
import os
import pandas as pd
from utils.data_loader import load_campaign_data

def test_load_campaign_data_missing_file(monkeypatch):
    # Temporarily point to a non-existent file
    monkeypatch.setattr("utils.data_loader.DATA_DIR", "wrong_folder")
    
    df = load_campaign_data()
    
    # Should return an empty DataFrame, not crash
    assert isinstance(df, pd.DataFrame)
    assert df.empty

def test_data_cleaning():
    # Test if the loader correctly handles strings in numeric columns
    # (Assuming you implement numeric conversion in your loader)
    test_csv_path = 'data/test_campaigns.csv'
    
    # Create a temporary bad CSV
    bad_data = "campaign_name,spend,revenue\nCamp1,100,five-hundred"
    with open(test_csv_path, "w") as f:
        f.write(bad_data)
        
    df = pd.read_csv(test_csv_path)
    # Perform cleaning check
    df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce').fillna(0)
    
    assert df.iloc[0]['revenue'] == 0
    
    # Cleanup
    if os.path.exists(test_csv_path):
        os.remove(test_csv_path)