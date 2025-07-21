# backup.py
import os
import shutil
import zipfile
from datetime import datetime

class BackupManager:
    def __init__(self, source, destination, version="v1", zip_backup=False):
        self.source = source
        self.destination = destination
        self.version = version
        self.zip_backup = zip_backup
        self.timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    def generate_backup_name(self):
        folder_name = os.path.basename(self.source.rstrip("/\\"))
        backup_name = f"{folder_name}_backup_{self.timestamp}_{self.version}"
        return os.path.join(self.destination, backup_name)

    def perform_backup(self):
        if not os.path.exists(self.source):
            raise FileNotFoundError("Source directory does not exist.")
        if not os.path.exists(self.destination):
            os.makedirs(self.destination)

        backup_path = self.generate_backup_name()

        if self.zip_backup:
            backup_path += ".zip"
            self._zip_directory(self.source, backup_path)
        else:
            shutil.copytree(self.source, backup_path)

        return backup_path

    def _zip_directory(self, src_dir, zip_file_path):
        with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(src_dir):
                for file in files:
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, src_dir)
                    zipf.write(full_path, arcname)