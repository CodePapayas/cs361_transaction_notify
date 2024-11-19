import sqlite3
from datetime import datetime

DATABASE = "email_logs.db"


def log_email_activity(recipient, status, message=None, error=None):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO email_logs (timestamp, recipient, status, message, error)
            VALUES (?, ?, ?, ?, ?)
        """, (datetime.now().isoformat(), recipient, status, message, error))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Failed to log email activity: {e}")
