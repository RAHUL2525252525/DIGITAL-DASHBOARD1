import os
from dotenv import load_dotenv
import pandas as pd
from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials
from functools import wraps
import requests

# =========================
# LOAD ENV
# =========================
load_dotenv()

# =========================
# GROQ AI CONFIG
# =========================
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
print("GROQ KEY LOADED:", bool(GROQ_API_KEY))

# =========================
# PATHS
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
DATA_DIR = os.path.join(STATIC_DIR, 'data')

# =========================
# FLASK INIT
# =========================
app = Flask(__name__, static_folder=STATIC_DIR, template_folder=TEMPLATE_DIR)
app.secret_key = "aether_sovereign_secret_key"
CORS(app)

app.config.update(
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=False,
    SESSION_PERMANENT=True
)

# =========================
# GROQ CHAT API
# =========================
@app.route('/api/gemini-chat', methods=['POST'])
def groq_chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"reply": "Please enter a message"}), 400

        if not GROQ_API_KEY:
            return jsonify({"reply": "AI temporarily unavailable"}), 200

        url = "https://api.groq.com/openai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {
                    "role": "system",
                    "content": "You are Aether AI Assistant for a Digital Marketing & E-commerce Dashboard. Help users understand campaigns, products, orders, analytics, ROI in simple language."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        }

        response = requests.post(url, headers=headers, json=payload)

        print("GROQ STATUS:", response.status_code)
        print("GROQ RESPONSE:", response.text)

        result = response.json()

        reply = result["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})

    except Exception as e:
        print("Groq Error:", e)
        return jsonify({"reply": "AI temporarily unavailable"}), 200


# =========================
# FIREBASE INIT
# =========================
if not firebase_admin._apps:
    try:
        key_path = os.path.join(BASE_DIR, "serviceAccountKey.json")

        if os.path.exists(key_path):
            cred = credentials.Certificate(key_path)
            firebase_admin.initialize_app(cred)
        else:
            firebase_admin.initialize_app()
    except:
        firebase_admin.initialize_app()


# =========================
# LOGIN DECORATOR
# =========================
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('user_email'):
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return wrapper


# =========================
# AUTH ROUTES
# =========================
@app.route('/')
@app.route('/login')
def login_page():
    if session.get('user_email'):
        return redirect(url_for('dashboard_page'))
    return render_template('login.html')


@app.route('/login-handler', methods=['POST'])
def login_handler():
    data = request.get_json()

    email = data.get('email')
    id_token = data.get('idToken')

    user_name = data.get('name') or data.get('displayName') or email.split("@")[0]

    if not id_token:
        return jsonify({"status": "error", "message": "Missing token"}), 401

    try:
        session.clear()
        session['user_email'] = email
        session['user_name'] = user_name
        session['is_admin'] = (email == "srinivasrahul838@gmail.com")
        session.modified = True

        return jsonify({
            "status": "success",
            "redirect": "/dashboard"
        })

    except Exception as e:
        print("LOGIN ERROR:", str(e))
        return jsonify({"status": "error", "message": "Login failed"}), 401


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))


@app.route('/register')
def register_page():
    return render_template('register.html')


@app.route('/forgot-password')
def forgot_page():
    return render_template('forgot_password.html')


# =========================
# DASHBOARD
# =========================
@app.route('/dashboard')
@login_required
def dashboard_page():
    return render_template('dashboard.html')


@app.route('/check-session')
def check_session():
    return jsonify({
        "session": {
            "user_email": session.get("user_email"),
            "user_name": session.get("user_name")
        }
    })


# =========================
# DASHBOARD PAGES
# =========================
@app.route('/overview')
@login_required
def overview_page():
    return render_template('overview.html')


@app.route('/campaigns')
@login_required
def campaigns_page():
    return render_template('campaigns.html')


@app.route('/products')
@login_required
def products_page():
    return render_template('products.html')


@app.route('/orders')
@login_required
def orders_page():
    return render_template('orders.html')


# =========================
# DATA LOADER
# =========================
def load_campaign_data():
    try:
        campaigns_csv = os.path.join(DATA_DIR, 'campaigns.csv')
        clicks_csv = os.path.join(DATA_DIR, 'clicks.csv')
        conversions_csv = os.path.join(DATA_DIR, 'conversions.csv')

        if not all(os.path.exists(f) for f in [campaigns_csv, clicks_csv, conversions_csv]):
            return pd.DataFrame()

        df1 = pd.read_csv(campaigns_csv)
        df2 = pd.read_csv(clicks_csv)
        df3 = pd.read_csv(conversions_csv)

        df = df1.merge(df2, on='campaign_name', how='left')
        df = df.merge(df3, on='campaign_name', how='left')

        df[['spend', 'clicks', 'conversions']] = df[['spend', 'clicks', 'conversions']].fillna(0)
        df['revenue'] = df['conversions'] * 45

        return df

    except Exception as e:
        print(e)
        return pd.DataFrame()


@app.route('/api/campaign-stats')
def campaign_stats():
    df = load_campaign_data()

    if df.empty:
        return jsonify({"status": "no_data"})

    totals = {
        "total_campaigns": len(df),
        "total_clicks": int(df['clicks'].sum()),
        "total_conversions": int(df['conversions'].sum()),
        "total_spend": float(df['spend'].sum()),
        "total_revenue": float(df['revenue'].sum())
    }

    return jsonify({
        "status": "success",
        "totals": totals,
        "campaigns": df.to_dict(orient="records")
    })


# =========================
# RUN SERVER
# =========================
if __name__ == '__main__':
    app.run(debug=True, port=5000)