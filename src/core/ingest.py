from datetime import datetime
import json
import uuid

class LogNormalizer:
    @staticmethod
    def normalize(log_data: dict, source_type: str) -> dict:
        """
        Converts raw logs into a unified JSON schema (OCSF-inspired).
        """
        normalized = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "source_type": source_type,
            "original_data": log_data,
            "severity": "Unknown",
            "event_name": "Unknown",
            "user": None,
            "src_ip": None,
            "dst_ip": None
        }

        # Source-specific mappings
        if source_type == "windows_event":
            normalized["event_name"] = log_data.get("EventID", "Unknown")
            normalized["severity"] = log_data.get("Level", "Info")
        
        elif source_type == "firewall":
            normalized["src_ip"] = log_data.get("src_ip")
            normalized["dst_ip"] = log_data.get("dst_ip")
            normalized["event_name"] = log_data.get("action", "Traffic")

        return normalized
