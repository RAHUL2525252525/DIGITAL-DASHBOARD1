def render_engagement_section():
    return '''
    <div class="engagement-container">
        <div class="chart-wrapper">
            <h3>KINETIC ENGAGEMENT (CLICKS)</h3>
            <canvas id="clicksChart"></canvas>
        </div>
        <div class="chart-wrapper">
            <h3>CONVERSION FLOW</h3>
            <canvas id="conversionChart"></canvas>
        </div>
    </div>
    '''