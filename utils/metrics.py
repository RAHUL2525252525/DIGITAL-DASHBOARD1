def get_dashboard_totals(df):
    """Calculates the high-level totals for the gold stat cards."""
    if df.empty:
        return {"reach": 0, "clicks": 0, "conversions": 0, "roi": 0}

    total_reach = int(df['reach'].sum())
    total_clicks = int(df['clicks'].sum())
    total_convs = int(df['conversions'].sum())
    
    # Calculate global ROI
    total_spend = df['spend'].sum()
    total_rev = df['revenue'].sum()
    avg_roi = ((total_rev - total_spend) / total_spend * 100) if total_spend > 0 else 0
    
    return {
        "reach": f"{total_reach:,}",
        "clicks": f"{total_clicks:,}",
        "conversions": f"{total_convs:,}",
        "roi": f"{avg_roi:.1f}%"
    }