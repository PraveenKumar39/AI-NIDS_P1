from ..base import BaseCollector
import random
from datetime import datetime

class SecurityToolCollector(BaseCollector):
    def __init__(self, interval: int = 12):
        super().__init__("EDR_AV", interval)
        self.tools = ["CrowdStrike", "SentinelOne", "WindowsDefender"]
        self.threats = ["Ransomware.LockBit", "Trojan.Emotet", "Mimikatz_Credential_Dump", "Suspicious PowerShell"]

    def collect(self) -> list:
        if random.random() > 0.9: # Rare events
            tool = random.choice(self.tools)
            threat = random.choice(self.threats)
            
            log = {
                "timestamp": datetime.utcnow().isoformat(),
                "tool_name": tool,
                "threat_name": threat,
                "action_taken": "Quarantined" if random.random() > 0.2 else "Alert Only",
                "file_path": r"C:\Users\Admin\AppData\Local\Temp\malware.exe",
                "device_name": f"WORKSTATION-{random.randint(100, 999)}"
            }
            return [log]
        return []
