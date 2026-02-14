import random
from datetime import datetime

class UEBAEngine:
    def __init__(self):
        self.user_baselines = {
            "alice": {"typical_hours": (9, 17), "typical_location": "US"},
            "bob": {"typical_hours": (8, 16), "typical_location": "UK"}
        }

    def analyze_behavior(self, user: str, event_type: str, metadata: dict = {}) -> dict:
        """Analyzes a user action for anomalies."""
        anomalies = []
        
        # 1. Provide Mock Analysis for specific scenarios
        if event_type == "Logon Success":
            # Simulate "Impossible Travel" randomly
            if random.random() > 0.8:
                anomalies.append("Impossible Travel Detected (US -> China in 1 hour)")
            
            # Simulate "Abnormal Hours"
            current_hour = datetime.utcnow().hour
            if user in self.user_baselines:
                start, end = self.user_baselines[user]["typical_hours"]
                if not (start <= current_hour <= end) and random.random() > 0.5:
                     anomalies.append(f"Login outside typical hours ({start}:00-{end}:00)")

        if anomalies:
            return {
                "is_anomalous": True,
                "risk_score": 85,
                "anomalies": anomalies
            }
        
        return {"is_anomalous": False, "risk_score": 10}
