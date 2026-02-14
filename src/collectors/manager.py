import logging
from typing import Dict, List
from .base import BaseCollector

logger = logging.getLogger("CollectorManager")

class CollectorManager:
    def __init__(self):
        self.collectors: Dict[str, BaseCollector] = {}
        self.storage_callback = None

    def register_collector(self, collector: BaseCollector):
        """Registers a new collector."""
        self.collectors[collector.name] = collector
        logger.info(f"Registered collector: {collector.name}")

    def start_all(self, storage_callback):
        """Starts all registered collectors."""
        self.storage_callback = storage_callback
        for name, collector in self.collectors.items():
            collector.start(self._handle_log)
    
    def stop_all(self):
        """Stops all registered collectors."""
        for name, collector in self.collectors.items():
            collector.stop()

    def _handle_log(self, log: dict):
        """Central hub for processing logs from all collectors."""
        # 1. Normalize (future)
        # 2. Enrich (future)
        # 3. Store
        if self.storage_callback:
            self.storage_callback(log)
