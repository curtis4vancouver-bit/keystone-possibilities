# scan_downloads.py
import os
import time
from pathlib import Path

downloads = Path(r"C:\Users\Curtis\Downloads")
now = time.time()
for f in downloads.glob("*"):
    if f.is_file() and now - f.stat().st_mtime < 600:
        print(f"File: {f.name}, Size: {f.stat().st_size}, Age: {int(now - f.stat().st_mtime)}s")
