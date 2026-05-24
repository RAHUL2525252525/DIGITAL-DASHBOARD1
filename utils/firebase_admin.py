import os
import firebase_admin
from firebase_admin import credentials, auth

def init_firebase_admin(base_dir):
    """Initializes the Admin SDK safely."""
    if not firebase_admin._apps:
        key_path = os.path.join(base_dir, "serviceAccountKey.json")
        if os.path.exists(key_path):
            cred = credentials.Certificate(key_path)
            firebase_admin.initialize_app(cred)
        else:
            print(f"[ERROR]: {key_path} not found.")

def verify_token(id_token):
    """Verifies the Firebase ID Token from the frontend."""
    try:
        return auth.verify_id_token(id_token)
    except Exception:
        return None

def delete_firebase_user(uid):
    """Permanently deletes a user from Firebase Auth."""
    try:
        auth.delete_user(uid)
        return True
    except Exception:
        return False