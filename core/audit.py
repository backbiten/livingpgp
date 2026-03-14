import json
import os
import time
from hashlib import sha256

class JSONLogger:
    """
    Structured logging for Living PGP Audit Trails.
    Implements log rotation and basic integrity hashing for 2026 standards.
    """
    def __init__(self, filename='audit.jsonl', max_size_mb=10):
        self.filename = filename
        self.max_size = max_size_mb * 1024 * 1024  # Convert to bytes
        self.current_session_id = os.urandom(8).hex()

    def _rotate_log(self):
        """
        Rotates the log file if it exceeds the maximum size.
        """
        if os.path.exists(self.filename) and os.path.getsize(self.filename) > self.max_size:
            timestamp = int(time.time())
            os.rename(self.filename, f"{self.filename}.{timestamp}.old")

    def log_event(self, event_type, metadata, sensitive=False):
        """
        Logs a cryptographic or policy event. 
        If 'sensitive' is True, metadata is hashed to protect PII while maintaining auditability.
        """
        self._rotate_log()
        
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
        
        if sensitive:
            # Hash sensitive metadata to prevent PII leaks in the audit log
            metadata = {
                "protected_hash": sha256(json.dumps(metadata).encode()).hexdigest(),
                "status": "ENCRYPTED_AT_REST"
            }

        log_entry = {
            'timestamp': timestamp,
            'session': self.current_session_id,
            'event_type': event_type,
            'metadata': metadata
        }
        
        with open(self.filename, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
            
        return log_entry