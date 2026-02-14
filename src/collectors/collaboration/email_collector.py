from ..base import BaseCollector
import random
from datetime import datetime

class CollaborationCollector(BaseCollector):
    def __init__(self, interval: int = 15):
        super().__init__("Email_Collab", interval)
        self.platforms = ["Office365", "Slack", "Zoom"]
        self.events = ["Phishing Email Detected", "External File Share", "Suspicious Login", "Mass Export"]

    def collect(self) -> list:
        if random.random() > 0.8:
            platform = random.choice(self.platforms)
            event = random.choice(self.events)
            
            log = {
                "timestamp": datetime.utcnow().isoformat(),
                "platform": platform,
                "event_type": event,
                "user": f"employee{random.randint(1, 100)}@company.com",
                "details": "Sent to external domain" if "File Share" in event else "Quarantined"
            }
            return [log]
        return []
