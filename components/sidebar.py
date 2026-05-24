
def render_sidebar(active_page="overview"):
    # Path mapping: (Label, URL Path, Key)
    links = [
        ("COMMAND OVERVIEW", "/", "overview"),
        ("CAMPAIGN ANALYTICS", "/analytics", "analytics"),
        ("ROI REPORTS", "/roi", "roi"),
        ("SYSTEM SETTINGS", "/settings", "settings")
    ]
    
    links_html = ""
    for label, href, key in links:
        active_class = "active" if key == active_page else ""
        # The onclick triggers a browser redirect to the Flask route
        links_html += f'<li class="{active_class}" onclick="window.location.href=\'{href}\'">{label}</li>'
    # ... rest of your code

    return f'''
    <nav>
        <div class="logo-section">
            <img src="/assets/logo.png" alt="Aether Logo">
            <h1>AETHER SOVEREIGN</h1>
        </div>
        <ul class="nav-links">
            {links_html}
        </ul>
        <button class="logout-btn" id="logoutBtn">TERMINATE SESSION</button>
    </nav>
    '''