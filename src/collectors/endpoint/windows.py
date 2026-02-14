from ..base import BaseCollector
import logging
import platform

# Only import pywin32 if on Windows
if platform.system() == "Windows":
    import win32evtlog

logger = logging.getLogger("WindowsCollector")

class WindowsEventCollector(BaseCollector):
    def __init__(self, interval: int = 10, log_type: str = "Security"):
        super().__init__(f"Windows_{log_type}", interval)
        self.log_type = log_type
        self.server = "localhost" # Local machine

    def collect(self) -> list:
        logs = []
        if platform.system() != "Windows":
            return []

        try:
            hand = win32evtlog.OpenEventLog(self.server, self.log_type)
            flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
            total = win32evtlog.GetNumberOfEventLogRecords(hand)
            
            # Read last 10 events for demo purposes
            events = win32evtlog.ReadEventLog(hand, flags, 0)
            
            for event in events:
                logs.append({
                    "EventID": event.EventID,
                    "TimeGenerated": event.TimeGenerated.Format(),
                    "SourceName": event.SourceName,
                    "EventCategory": event.EventCategory,
                    "EventType": event.EventType,
                    "StringInserts": event.StringInserts
                })
                
            win32evtlog.CloseEventLog(hand)
            
        except Exception as e:
            if "privilege is not held" in str(e):
                print(f"[WARN] Windows Event Log requires Admin privileges. Skipping.")
            else:
                logger.error(f"Failed to read Windows Event Log: {e}")
            
        return logs
