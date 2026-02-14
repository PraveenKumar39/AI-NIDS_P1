import random

class ThreatIntel:
    def __init__(self):
        # Mock Feed
        self.malicious_ips = {
            "192.168.1.55": "Known Command & Control (C2)",
            "45.33.22.11": "Brute Force Botnet",
            "103.20.10.5": "Phishing Host"
        }
        self.malicious_domains = {
            "evil-bank-login.com": "Credential Theft",
            "update-windows-patch.exe.net": "Malware Dist"
        }

    def check_ip(self, ip: str) -> dict:
        """Checks if an IP is in the threat feed."""
        if ip in self.malicious_ips:
            return {
                "match": True,
                "type": "Malicious IP",
                "details": self.malicious_ips[ip],
                "severity": "High"
            }
        return {"match": False}

    def check_domain(self, domain: str) -> dict:
        """Checks if a domain is malicious."""
        if domain in self.malicious_domains:
            return {
                "match": True,
                "type": "Malicious Domain",
                "details": self.malicious_domains[domain],
                "severity": "Critical"
            }
        return {"match": False}
