import sqlite3
from datetime import datetime
from threading import Lock

DATABASE = "email_logs.db"
db_lock = Lock()

def log_email_activity(recipient, status, message=None, error=None):
    try:
        recipient = recipient if recipient else "N/A"
        with db_lock:
            conn = sqlite3.connect(DATABASE, check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO email_logs (timestamp, recipient, status, message, error)
                VALUES (?, ?, ?, ?, ?)
            """, (datetime.now().isoformat(), recipient, status, message, error))
            conn.commit()
            conn.close()
    except sqlite3.OperationalError as e:
        if "database is locked" in str(e):
            print("Database is locked. Could not log email activity.")
        else:
            print(f"Failed to log email activity: {e}")
    except Exception as e:
        print(f"Failed to log email activity: {e}")
