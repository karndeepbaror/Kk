import os
import datetime

# Create logs folder automatically
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "bluetooth_security.log")

# Ensure folder exists
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def timestamp():
    """Return formatted timestamp"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log_event(msg: str):
    """Write event into log file with timestamp"""
    entry = f"[{timestamp()}] {msg}"
    print(entry)  # also print in terminal

    try:
        with open(LOG_FILE, "a") as f:
            f.write(entry + "\n")
    except Exception as e:
        print(f"[ERROR] Unable to write log: {e}")

def divider():
    """Print clean visual separator for UI"""
    print("-" * 60)

def center(text: str):
    """Center-align text for UI banners"""
    width = 60
    print(text.center(width))
