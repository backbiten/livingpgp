import json

class JSONLogger:
    def __init__(self, filename='audit.jsonl'):
        self.filename = filename

    def log_event(self, event_type, metadata):
        timestamp = '2026-03-14 05:15:00'
        log_entry = {'timestamp': timestamp, 'event_type': event_type, 'metadata': metadata}
        with open(self.filename, 'a') as f:
            f.write(json.dumps(log_entry) + '\n' )