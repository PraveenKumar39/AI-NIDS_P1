class ContextManager:
    def __init__(self):
        self.hr_data = {
            "alice": {"role": "Engineer", "dept": "R&D", "manager": "Dave"},
            "bob": {"role": "Sales", "dept": "Revenue", "manager": "Sarah"},
            "admin": {"role": "SysAdmin", "dept": "IT", "manager": "CTO"}
        }
        self.asset_data = {
            "192.168.1.55": {"type": "Workstation", "owner": "alice", "criticality": "Low"},
            "10.0.0.1": {"type": "Database Server", "owner": "IT", "criticality": "High"}
        }

    def get_user_context(self, username: str) -> dict:
        return self.hr_data.get(username, {"role": "Unknown", "dept": "Unknown"})

    def get_asset_context(self, ip: str) -> dict:
        return self.asset_data.get(ip, {"type": "Unknown", "criticality": "Unknown"})
