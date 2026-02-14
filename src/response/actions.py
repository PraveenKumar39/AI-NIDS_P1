import logging
import time

logger = logging.getLogger("SOAR_Actions")

class ResponseManager:
    def __init__(self):
        self.history = []

    def execute_action(self, action_name: str, target: str, created_by: str = "System") -> dict:
        """
        Executes a simulated response action.
        """
        logger.info(f"Executing {action_name} on {target} by {created_by}")
        
        status = "Success"
        message = ""
        
        if action_name == "Block_IP":
            # Simulation: Add IP to firewall blocklist
            message = f"IP {target} has been added to the Perimeter Firewall blocklist."
            
        elif action_name == "Disable_User":
            # Simulation: Disable Active Directory account
            message = f"User account {target} has been disabled in Active Directory."
            
        elif action_name == "Isolate_Host":
            # Simulation: EDR isolation
            message = f"Host {target} network access has been restricted to management VLAN only."
            
        else:
            status = "Failed"
            message = f"Unknown action: {action_name}"

        record = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "action": action_name,
            "target": target,
            "status": status,
            "message": message,
            "executor": created_by
        }
        
        self.history.insert(0, record) # Add recent first
        return record

    def get_history(self):
        return self.history
