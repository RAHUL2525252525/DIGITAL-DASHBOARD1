def render_campaign_table(df):
    if df.empty:
        return "<p>No active transmissions found.</p>"
    
    # Header
    table_html = '''
    <table class="sovereign-table">
        <thead>
            <tr>
                <th>CAMPAIGN</th>
                <th>SPEND</th>
                <th>REVENUE</th>
                <th>CLICKS</th>
                <th>ROI</th>
            </tr>
        </thead>
        <tbody>
    '''
    
    # Rows
    for _, row in df.iterrows():
        roi = ((row['revenue'] - row['spend']) / row['spend'] * 100) if row['spend'] > 0 else 0
        table_html += f'''
            <tr>
                <td>{row['campaign_name']}</td>
                <td>${row['spend']:,}</td>
                <td>${row['revenue']:,}</td>
                <td>{row['clicks']:,}</td>
                <td style="color: {'#4ade80' if roi > 0 else '#ff6b6b'}">{roi:.1f}%</td>
            </tr>
        '''
    
    table_html += "</tbody></table>"
    return table_html