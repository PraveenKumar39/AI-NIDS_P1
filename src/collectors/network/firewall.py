from ..base import BaseCollector
import os

class FirewallCollector(BaseCollector):
    def __init__(self, log_path: str = "firewall.log", interval: int = 5):
        super().__init__("Firewall", interval)
        self.log_path = log_path
        self.last_position = 0

    def collect(self) -> list:
        logs = []
        if not os.path.exists(self.log_path):
            return logs

        with open(self.log_path, "r") as f:
            f.seek(self.last_position)
            lines = f.readlines()
            self.last_position = f.tell()

        for line in lines:
            parts = line.strip().split(" ")
            if len(parts) >= 5: # Basic check
                logs.append({
                    "raw": line.strip(),
                    "action": parts[0], # ALLOW/DENY
                    "src_ip": parts[1],
                    "dst_ip": parts[2],
                    "port": parts[3],
                    "time": parts[4] if len(parts) > 4 else "unknown"
                })
        return logs
