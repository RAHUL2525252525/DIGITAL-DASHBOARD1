from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    """Protects routes from unauthenticated users."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_email'):
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Protects routes from non-admin users."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_email'):
            return redirect(url_for('login_page'))
        if not session.get('is_admin'):
            flash("Administrator privileges required.")
            return redirect(url_for('dashboard_page'))
        return f(*args, **kwargs)
    return decorated_function