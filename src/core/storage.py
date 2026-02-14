import sqlite3
import json
import logging
from datetime import datetime

logger = logging.getLogger("LogStorage")

class LogStorage:
    def __init__(self, db_path: str = "logs.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize the SQLite database schema."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS security_events (
                id TEXT PRIMARY KEY,
                timestamp TEXT,
                source_type TEXT,
                severity TEXT,
                event_name TEXT,
                raw_data TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def save_log(self, normalized_log: dict):
        """Saves a normalized log entry."""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute('''
                INSERT INTO security_events (id, timestamp, source_type, severity, event_name, raw_data)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                normalized_log["id"],
                normalized_log["timestamp"],
                normalized_log["source_type"],
                normalized_log["severity"],
                normalized_log["event_name"],
                json.dumps(normalized_log["original_data"])
            ))
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Failed to save log: {e}")

    def get_recent_logs(self, limit: int = 100):
        """Retrieves the most recent logs."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT * FROM security_events ORDER BY timestamp DESC LIMIT ?', (limit,))
        rows = c.fetchall()
        conn.close()
        
        logs = []
        for row in rows:
            logs.append({
                "id": row[0],
                "timestamp": row[1],
                "source_type": row[2],
                "severity": row[3],
                "event_name": row[4],
                "raw_data": json.loads(row[5])
            })
        return logs
