import json
import os
from datetime import datetime

class Logger:
    def __init__(self):
        self.log_file = "logs.json"
        self.logs = self.load_logs()

    def load_logs(self):
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, "r", encoding="utf-8") as file:
                    return json.load(file)
            except Exception:
                return []
        return []

    def save_logs(self):
        try:
            with open(self.log_file, "w", encoding="utf-8") as file:
                json.dump(self.logs, file, ensure_ascii=False, indent=4)
        except Exception:
            pass

    def log(self, message):
        self.logs.append({
            "message": message,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        self.save_logs()