import sqlite3
from datetime import datetime, timedelta
import config

def init_db():
    conn = sqlite3.connect('aprs.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bulletins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            poster TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT NOT NULL,
            recipient TEXT NOT NULL,
            text TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def format_timestamp(timestamp):
    dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    return dt.strftime("%b%d %H:%M").upper()

def add_bulletin(callsign, text):
    conn = sqlite3.connect('aprs.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bulletins (text, poster) VALUES (?, ?)", (text, callsign))
    conn.commit()
    conn.close()


def get_bulletins():
    conn = sqlite3.connect('aprs.db')
    cursor = conn.cursor()
    cursor.execute("SELECT text, poster, timestamp FROM bulletins ORDER BY timestamp DESC")
    results = cursor.fetchall()
    conn.close()
    return [(text, poster, format_timestamp(ts)) for text, poster, ts in results]


def add_message(sender, recipient, text):
    conn = sqlite3.connect('aprs.db')
    cursor = conn.cursor()
    normalized_recipient = normalize_callsign(recipient)
    cursor.execute("INSERT INTO messages (sender, recipient, text) VALUES (?, ?, ?)", (sender, normalized_recipient, text))
    conn.commit()
    conn.close()

def get_messages_for_user(callsign):
    conn = sqlite3.connect('aprs.db')
    cursor = conn.cursor()
    normalized_callsign = normalize_callsign(callsign)
    cursor.execute("""
        SELECT sender, text, timestamp 
        FROM messages 
        WHERE UPPER(recipient) = ? 
        ORDER BY timestamp DESC
    """, (normalized_callsign,))
    results = cursor.fetchall()
    conn.close()
    return [(normalize_callsign(sender), text, format_timestamp(ts)) for sender, text, ts in results]

def normalize_callsign(callsign):
    return callsign.split('-')[0].upper()

def delete_expired_bulletins():
    """Delete bulletins older than the configured expiration time."""
    expiration_threshold = datetime.now() - timedelta(days=config.BULLETIN_EXPIRATION_DAYS)
    conn = sqlite3.connect('aprs.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bulletins WHERE timestamp < ?", (expiration_threshold,))
    conn.commit()
    conn.close()