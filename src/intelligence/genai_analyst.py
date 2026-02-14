import random

class GenAIAnalyst:
    def __init__(self):
        self.templates = {
            "Brute Force": {
                "explanation": "I detected multiple failed login attempts ({count} attempts) from IP {ip}, followed by a successful login or firewall block. This pattern strongly indicates a brute-force attack or credential stuffing attempt.",
                "remediation": [
                    "1. Immediately block IP {ip} at the firewall.",
                    "2. Reset the password for user '{user}' if compromised.",
                    "3. Enable MFA for all administrative accounts.",
                    "4. Review logs for any successful logins from this IP."
                ]
            },
            "Malware": {
                "explanation": "The EDR system detected a suspicious file '{file}' on host {host}. The signature matches known ransomware indicators.",
                "remediation": [
                    "1. Isolate host {host} from the network immediately.",
                    "2. Run a full scan using the installed AV/EDR agent.",
                    "3. Check for lateral movement to other hosts.",
                    "4. Restore encrypted files from secure backups if necessary."
                ]
            },
            "Data Exfiltration": {
                "explanation": "An unusual amount of data ({size}) was transferred to an external IP {ip} during off-hours. This deviates from the user's normal baseline.",
                "remediation": [
                    "1. Suspend the user account '{user}' pending investigation.",
                    "2. Analyze the destination IP {ip} against threat intel feeds.",
                    "3. Determine the sensitivity of the transferred data."
                ]
            }
        }

    def generate_analysis(self, alert_type: str, context: dict) -> dict:
        """
        Simulates an LLM generating an analysis.
        """
        # Default fallback
        explanation = "The system detected an anomaly that requires manual review."
        remediation = ["1. Investigate manually."]
        
        # Simple keyword matching to select template
        matched_key = None
        for key in self.templates:
            if key.lower() in alert_type.lower():
                matched_key = key
                break
        
        if matched_key:
            tmpl = self.templates[matched_key]
            explanation = tmpl["explanation"].format(**context)
            # Format remediation steps with context if needed (safe formatting)
            remediation = [step.format(**context) for step in tmpl["remediation"]]
        
        return {
            "summary": explanation,
            "steps": remediation,
            "confidence": "High" if matched_key else "Low"
        }
