import tkinter as tk
from tkinter import filedialog, messagebox
from backup import BackupManager
from config import ConfigManager
from logger import Logger

class BackupApp:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.logger = Logger()
        self.root = tk.Tk()
        self.root.title("Backup Tool")

        self.source_var = tk.StringVar(value=self.config_manager.config.get("source", ""))
        self.destination_var = tk.StringVar(value=self.config_manager.config.get("destination", ""))
        self.version_var = tk.StringVar(value=self.config_manager.config.get("version", "v1"))
        self.zip_var = tk.BooleanVar(value=self.config_manager.config.get("zip", False))

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Source Folder").grid(row=0, column=0)
        tk.Entry(self.root, textvariable=self.source_var, width=40).grid(row=0, column=1)
        tk.Button(self.root, text="Browse", command=self.browse_source).grid(row=0, column=2)

        tk.Label(self.root, text="Destination Folder").grid(row=1, column=0)
        tk.Entry(self.root, textvariable=self.destination_var, width=40).grid(row=1, column=1)
        tk.Button(self.root, text="Browse", command=self.browse_destination).grid(row=1, column=2)

        tk.Label(self.root, text="Version").grid(row=2, column=0)
        tk.Entry(self.root, textvariable=self.version_var).grid(row=2, column=1)

        tk.Checkbutton(self.root, text="ZIP Backup", variable=self.zip_var).grid(row=3, column=1)

        tk.Button(self.root, text="Start Backup", command=self.start_backup).grid(row=4, column=1)

    def browse_source(self):
        path = filedialog.askdirectory()
        if path:
            self.source_var.set(path)

    def browse_destination(self):
        path = filedialog.askdirectory()
        if path:
            self.destination_var.set(path)

    def start_backup(self):
        source = self.source_var.get()
        destination = self.destination_var.get()
        version = self.version_var.get()
        zip_option = self.zip_var.get()

        try:
            backup_manager = BackupManager(source, destination, version, zip_option)
            backup_path = backup_manager.perform_backup()
            self.logger.log(f"Backup completed: {backup_path}")
            messagebox.showinfo("Success", f"Backup created: {backup_path}")
            self.config_manager.save_config({
                "source": source,
                "destination": destination,
                "version": version,
                "zip": zip_option
            })
        except Exception as e:
            self.logger.log(f"Error: {str(e)}")
            messagebox.showerror("Error", str(e))

    def run(self):
        self.root.mainloop()
