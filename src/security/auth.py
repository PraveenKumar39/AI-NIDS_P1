import time
from collections import defaultdict

class AuthGuard:
    def __init__(self, max_attempts=5, lockout_time=900):
        self.max_attempts = max_attempts
        self.lockout_time = lockout_time # 15 minutes
        self.attempts = defaultdict(list)
        self.lockouts = {}

    def is_locked_out(self, ip_address):
        """Checks if an IP is currently locked out."""
        if ip_address in self.lockouts:
            lockout_expiry = self.lockouts[ip_address]
            if time.time() < lockout_expiry:
                return True, lockout_expiry - time.time()
            else:
                # Lockout expired
                del self.lockouts[ip_address]
                if ip_address in self.attempts:
                    del self.attempts[ip_address]
        return False, 0

    def record_attempt(self, ip_address, success):
        """Records a login attempt."""
        if success:
            # Clear attempts on success
            if ip_address in self.attempts:
                del self.attempts[ip_address]
            return

        # Record failure
        current_time = time.time()
        self.attempts[ip_address].append(current_time)
        
        # Cleanup old attempts (older than lockout window)
        # We only care about attempts within a short window, say 1 hour, 
        # but for simplicity, let's just check count.
        
        if len(self.attempts[ip_address]) >= self.max_attempts:
            self.lockouts[ip_address] = current_time + self.lockout_time
            return True # Triggered Lockout
            
        return False
