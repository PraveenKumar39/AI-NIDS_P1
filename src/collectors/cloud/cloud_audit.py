from ..base import BaseCollector
import random
from datetime import datetime

class CloudCollector(BaseCollector):
    def __init__(self, interval: int = 8):
        super().__init__("Cloud_Audit", interval)
        self.providers = ["AWS", "Azure", "GCP"]
        self.actions = ["ConsoleLogin", "CreateBucket", "DeleteVM", "UpdateSecurityGroup", "GetSecret"]
        self.regions = ["us-east-1", "eu-west-1", "ap-south-1"]

    def collect(self) -> list:
        if random.random() > 0.6:
            provider = random.choice(self.providers)
            action = random.choice(self.actions)
            
            log = {
                "timestamp": datetime.utcnow().isoformat(),
                "provider": provider,
                "event_name": action,
                "region": random.choice(self.regions),
                "source_ip": f"203.0.113.{random.randint(1, 255)}",
                "user_identity": "root_account" if action == "ConsoleLogin" else "devops-user"
            }
            return [log]
        return []
