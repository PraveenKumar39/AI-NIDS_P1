import hashlib
import os
import glob
import logging

logger = logging.getLogger("IntegrityMonitor")

class IntegrityMonitor:
    def __init__(self, root_dir="src"):
        self.root_dir = root_dir
        self.baseline = {}
        
    def calculate_file_hash(self, filepath):
        """Calculates SHA-256 hash of a file."""
        sha256_hash = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                # Read and update hash string value in blocks of 4K
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            logger.error(f"Error hashing {filepath}: {e}")
            return None

    def build_baseline(self):
        """Scans directory and builds hash baseline."""
        logger.info(f"Building integrity baseline for {self.root_dir}...")
        files = glob.glob(os.path.join(self.root_dir, "**", "*.py"), recursive=True)
        # Also include app.py
        if os.path.exists("app.py"):
            files.append("app.py")
            
        for filepath in files:
            file_hash = self.calculate_file_hash(filepath)
            if file_hash:
                self.baseline[filepath] = file_hash
        logger.info(f"Baseline built with {len(self.baseline)} files.")

    def check_integrity(self):
        """Checks current files against baseline."""
        files = glob.glob(os.path.join(self.root_dir, "**", "*.py"), recursive=True)
        if os.path.exists("app.py"):
            files.append("app.py")
            
        compromised_files = []
        
        for filepath in files:
            current_hash = self.calculate_file_hash(filepath)
            
            if filepath not in self.baseline:
                # New file detected (could be malicious injection)
                compromised_files.append({"file": filepath, "status": "NEW_FILE"})
            elif self.baseline[filepath] != current_hash:
                # Modified file
                compromised_files.append({"file": filepath, "status": "MODIFIED"})
                
        # Check for deleted files
        for baseline_file in self.baseline:
            if baseline_file not in files:
                 compromised_files.append({"file": baseline_file, "status": "DELETED"})
                 
        return compromised_files
