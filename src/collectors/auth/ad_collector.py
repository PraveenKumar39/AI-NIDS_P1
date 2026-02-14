from ..base import BaseCollector
import random
from datetime import datetime

class AuthCollector(BaseCollector):
    def __init__(self, interval: int = 5):
        super().__init__("Auth_Logs", interval)
        self.users = ["alice", "bob", "charlie", "admin", "service_account"]
        self.events = ["Logon Success", "Logon Failed", "Account Locked", "Password Changed"]
        
    def collect(self) -> list:
        # Simulate AD/SSO logs
        if random.random() > 0.7: # 30% chance of generating event
            user = random.choice(self.users)
            event = random.choice(self.events)
            
            log = {
                "timestamp": datetime.utcnow().isoformat(),
                "user": user,
                "event": event,
                "source_ip": f"192.168.1.{random.randint(10, 200)}",
                "service": "Active Directory"
            }
            return [log]
        return []
