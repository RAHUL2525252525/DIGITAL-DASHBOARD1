def prepare_roi_chart_data(df):
    """Formats campaign data specifically for Chart.js labels and values."""
    if df.empty:
        return {"labels": [], "values": []}

    # Calculate ROI for each row
    df['roi'] = ((df['revenue'] - df['spend']) / df['spend'] * 100).fillna(0)
    
    return {
        "labels": df['campaign_name'].tolist(),
        "values": df['roi'].round(2).tolist()
    }