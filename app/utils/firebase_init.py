import firebase_admin
from firebase_admin import credentials, db
from app.config import settings
import os
import json

def initialize_firebase():
    if not firebase_admin._apps:
        # Check if raw JSON string is provided via environment variable (Production)
        if settings.FIREBASE_SERVICE_ACCOUNT_JSON:
            try:
                service_account_info = json.loads(settings.FIREBASE_SERVICE_ACCOUNT_JSON)
                cred = credentials.Certificate(service_account_info)
                firebase_admin.initialize_app(cred, {
                    'databaseURL': settings.FIREBASE_DATABASE_URL
                })
                print("✅ Firebase Admin SDK initialized from environment variable.")
                return db
            except Exception as e:
                print(f"❌ Error initializing Firebase from JSON string: {e}")

        # Fallback to service account file (Development)
        if not os.path.exists(settings.FIREBASE_SERVICE_ACCOUNT):
            print(f"⚠️ Firebase service account file or JSON string not found.")
            return None
        
        try:
            cred = credentials.Certificate(settings.FIREBASE_SERVICE_ACCOUNT)
            firebase_admin.initialize_app(cred, {
                'databaseURL': settings.FIREBASE_DATABASE_URL
            })
            print("✅ Firebase Admin SDK initialized from service account file.")
        except Exception as e:
            print(f"❌ Error initializing Firebase from file: {e}")
            return None
            
    return db

db_ref = initialize_firebase()
