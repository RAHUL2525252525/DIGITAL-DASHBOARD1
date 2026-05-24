import pytest
from utils.metrics import calculate_roi, calculate_ctr, get_dashboard_totals
import pandas as pd

def test_calculate_roi():
    # Test normal profit
    assert calculate_roi(200, 100) == 100.0
    # Test break even
    assert calculate_roi(100, 100) == 0.0
    # Test loss
    assert calculate_roi(50, 100) == -50.0
    # Test zero spend (should not crash)
    assert calculate_roi(100, 0) == 0

def test_calculate_ctr():
    # 10 clicks out of 100 impressions = 10%
    assert calculate_ctr(10, 100) == 10.0
    # Zero impressions
    assert calculate_ctr(10, 0) == 0

def test_get_dashboard_totals():
    # Create a mock dataframe
    data = {
        'reach': [100, 200],
        'clicks': [10, 20],
        'conversions': [1, 2],
        'spend': [50, 50],
        'revenue': [150, 150]
    }
    df = pd.DataFrame(data)
    
    totals = get_dashboard_totals(df)
    
    assert totals['reach'] == "300"
    assert totals['clicks'] == "30"
    assert totals['roi'] == "200.0%" # ((300-100)/100) * 100