from ..base import BaseCollector
import random
from datetime import datetime

class WebLogCollector(BaseCollector):
    def __init__(self, interval: int = 4):
        super().__init__("Web_Access_Logs", interval)
        self.endpoints = ["/login", "/api/v1/data", "/admin", "/index.html", "/contact"]
        self.methods = ["GET", "POST", "PUT"]
        self.status_codes = [200, 200, 200, 401, 403, 404, 500]

    def collect(self) -> list:
        logs = []
        # Generate a batch of requests
        for _ in range(random.randint(1, 5)):
            log = {
                "timestamp": datetime.utcnow().isoformat(),
                "remote_addr": f"10.0.0.{random.randint(1, 255)}",
                "method": random.choice(self.methods),
                "url": random.choice(self.endpoints),
                "status": random.choice(self.status_codes),
                "user_agent": "Mozilla/5.0 (compatible; Bot/1.0)"
            }
            logs.append(log)
        return logs
