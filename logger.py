from datetime import datetime

class Logger:
    def __init__(self, log_file='backup.log'):
        self.log_file = log_file

    def log(self, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.log_file, 'a') as f:
            f.write(f"[{timestamp}] {message}\n")