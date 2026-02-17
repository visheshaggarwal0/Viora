import json
import os
from datetime import datetime

class Memory:
    def __init__(self, storage_file: str = "data/memory.json"):
        self.storage_file = storage_file
        self.data = self._load_memory()

    def _load_memory(self):
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        return {"notes": [], "logs": []}

    def save_memory(self):
        with open(self.storage_file, 'w') as f:
            json.dump(self.data, f, indent=4)

    def add_note(self, content: str):
        timestamp = datetime.now().isoformat()
        self.data["notes"].append({"timestamp": timestamp, "content": content})
        self.save_memory()

    def get_notes(self):
        return self.data["notes"]

    def log_interaction(self, user_input: str, agent_response: str):
        timestamp = datetime.now().isoformat()
        self.data["logs"].append({
            "timestamp": timestamp,
            "user": user_input,
            "agent": agent_response
        })
        self.save_memory()
