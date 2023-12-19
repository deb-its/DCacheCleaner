import os
import shutil
import tkinter as tk
from tkinter import ttk
from threading import Thread
import psutil

def is_discord_running():
    for process in psutil.process_iter(['pid', 'name']):
        if "Discord.exe" in process.info['name']:
            return True
    return False

def delete_discord_cache(logs_directory, progress_var, status_label):
    try:
        if is_discord_running():
            status_label.config(text="Please close discord before clearing cache.")
            return

        # Specify the paths to Discord cache directories
        cache_paths = [
            os.path.join(os.getenv("APPDATA"), "discord", "Cache"),
            os.path.join(os.getenv("APPDATA"), "discord", "Code Cache"),
            os.path.join(os.getenv("APPDATA"), "discord", "GPUCache")
        ]

        total_directories = len(cache_paths)
        deleted_at_least_one_directory = False

        for index, cache_path in enumerate(cache_paths):
            try:
                # Check if the directory exists before attempting to delete
                if os.path.exists(cache_path):
                    # Extract the last part of the path (e.g., "Cache", "Code Cache", "GPUCache")
                    cache_name = os.path.basename(cache_path)
                    shutil.rmtree(cache_path)
                    progress_value = (index + 1) / total_directories * 100
                    progress_var.set(progress_value)
                    status_label.config(text=f"Deleted {cache_name}")
                    deleted_at_least_one_directory = True
                else:
                    status_label.config(text=f"There are no more Cache.")
            except Exception as e:
                status_label.config(text=f"Error deleting {cache_path}: {e}")

        # Display the success message only if at least one directory was deleted
        if deleted_at_least_one_directory:
            status_label.config(text="Discord Cache Cleaned!")

    except Exception as e:
        status_label.config(text=f"Error: {e}")

root = tk.Tk()
root.title("Discord Cache Cleaner")

delete_button = tk.Button(root, text="Clear Cache", command=lambda: Thread(target=delete_discord_cache, args=(os.path.expandvars(r"%appdata%\discord\logs"), progress_var, status_label)).start())
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, length=290, mode="determinate")
status_label = tk.Label(root, text="")

delete_button.pack(pady=10)
progress_bar.pack(pady=10)
status_label.pack()

root.mainloop()
