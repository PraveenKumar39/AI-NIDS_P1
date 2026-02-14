from datetime import datetime, timedelta

class CorrelationEngine:
    def __init__(self):
        self.rules = [
            {"name": "Brute Force & Firewall Block", "severity": "High", "time_window": 300},
            {"name": "Compromised Host Exfiltration", "severity": "Critical", "time_window": 600}
        ]

    def correlate(self, events: list) -> list:
        """
        Analyzes a stream of mixed events for patterns.
        Input: List of normalized event dicts.
        Output: List of correlated 'Alert' dicts.
        """
        alerts = []
        
        # Index events by IP for correlation
        events_by_ip = {}
        for e in events:
            # Extract IP based on source type logic (simplified)
            ip = e.get('source_ip') or e.get('src_ip') or e.get('remote_addr')
            if ip:
                if ip not in events_by_ip:
                    events_by_ip[ip] = []
                events_by_ip[ip].append(e)

        # Rule 1: Brute Force & Firewall Block
        # Logic: If an IP has > 3 Failed Logins AND > 1 Firewall Deny
        for ip, ip_events in events_by_ip.items():
            failed_logins = [e for e in ip_events if e.get('event') == 'Logon Failed' or e.get('status') == 401]
            firewall_denies = [e for e in ip_events if e.get('action') == 'DENY']
            
            if len(failed_logins) >= 3 and len(firewall_denies) >= 1:
                alerts.append({
                    "name": "Brute Force & Firewall Drop",
                    "severity": "High",
                    "source_ip": ip,
                    "details": f"IP {ip} had {len(failed_logins)} failed logins and was blocked by firewall.",
                    "timestamp": datetime.utcnow().isoformat()
                })

        return alerts
