from abc import ABC, abstractmethod
import threading
import time
import logging
from typing import Callable, Dict, Any

logger = logging.getLogger("LogCollector")

class BaseCollector(ABC):
    def __init__(self, name: str, interval: int = 5):
        self.name = name
        self.interval = interval
        self.running = False
        self.thread = None
        self.callback = None

    def start(self, callback: Callable[[Dict[str, Any]], None]):
        """Starts the collector in a background thread."""
        if self.running:
            return
        
        self.running = True
        self.callback = callback
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        logger.info(f"Collector '{self.name}' started.")

    def stop(self):
        """Stops the collector."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        logger.info(f"Collector '{self.name}' stopped.")

    def _run_loop(self):
        """Internal loop to fetch logs periodically."""
        while self.running:
            try:
                logs = self.collect()
                if logs:
                    for log in logs:
                        if self.callback:
                            self.callback(log)
            except Exception as e:
                logger.error(f"Error in collector '{self.name}': {e}")
            
            time.sleep(self.interval)

    @abstractmethod
    def collect(self) -> list:
        """Fetch new logs. Must be implemented by subclasses."""
        pass
