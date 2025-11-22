# ============================================================
#  BLUETOOTH SECURITY SUITE — UI MODULE (PRO VERSION)
#  Developer: Karndeep Baror
#  GitHub: github.com/karndeepbaror
# ============================================================

import os
import time
import threading
import random
import platform
from datetime import datetime
from engine import SecurityEngine


# ------------------------------------------------------------
# GLOBAL ENGINE
# ------------------------------------------------------------
engine = SecurityEngine()

display_mode = "hacker"      # options: clean / hacker / matrix
alert_sound_enabled = True


# ------------------------------------------------------------
# SOUND ALERT SYSTEM
# ------------------------------------------------------------
def play_alert_sound():
    if not alert_sound_enabled:
        return

    try:
        if platform.system() == "Windows":
            import winsound
            winsound.Beep(1200, 180)
            winsound.Beep(900, 180)
        else:
            os.system("printf '\\a'")
    except:
        pass


# ------------------------------------------------------------
# CLEAR SCREEN
# ------------------------------------------------------------
def clear():
    os.system("cls" if os.name == "nt" else "clear")


# ------------------------------------------------------------
# HEADER
# ------------------------------------------------------------
def header():
    print("\033[92mBluetooth Security Suite — PRO EDITION\033[0m")
    print("Developer: Karndeep Baror  |  GitHub: github.com/karndeepbaror")
    print("Session Start:", engine.session_start)
    print("-" * 60)


# ------------------------------------------------------------
# ANIMATED TOWER
# ------------------------------------------------------------
tower_frames = [
    [
        "       |",
        "       |",
        "    ---O---",
        "       |",
        "       |"
    ],
    [
        "       |",
        "    -- O --",
        "   --- O ---",
        "    -- O --",
        "       |"
    ],
    [
        "    -  |  -",
        "   --  O  --",
        " ----- O -----",
        "   --  O  --",
        "    -  |  -"
    ]
]


def draw_tower(step):
    frame = tower_frames[step % len(tower_frames)]
    print("\033[96m")
    for line in frame:
        print("   " + line)
    print("\033[0m")


# ------------------------------------------------------------
# MATRIX BACKGROUND GENERATOR
# ------------------------------------------------------------
def matrix_line(width=60):
    chars = "101010110110010100101010011010"
    return "".join(random.choice(chars) for _ in range(width))


# ------------------------------------------------------------
# DEVICE TABLE
# ------------------------------------------------------------
def show_devices():
    data = engine.export_snapshot()

    if not data:
        print("\nScanning for nearby Bluetooth devices...\n")
        return

    print("\n\033[93mNearby Devices:\033[0m\n")
    print("Name                 MAC                 RSSI   Type    Flags")
    print("-" * 60)

    for mac, d in data.items():
        rssi = d["rssi"]
        flags = ",".join(d["flags"]) if d["flags"] else "OK"

        # Colors
        if "BLACKLISTED" in flags:
            color = "\033[91m"  # red
        elif "UNKNOWN" in flags:
            color = "\033[93m"  # yellow
        else:
            color = "\033[92m"  # green

        print(f"{color}{d['name']:<20} {mac:<18} {rssi:<5}  {d['type']:<6}  {flags}\033[0m")


# ------------------------------------------------------------
# LIVE ALERT WINDOW
# ------------------------------------------------------------
def show_alerts():
    if not engine.alert_log:
        return

    latest = engine.alert_log[-1]
    atype = latest["type"]
    mac = latest["mac"]
    name = latest["name"]
    t = latest["time"]

    print("\n\033[91m[ALERT]\033[0m", f"{atype} | {name} ({mac}) at {t}")


# ------------------------------------------------------------
# MAIN UI LOOP
# ------------------------------------------------------------
def ui_loop():
    step = 0

    while True:
        clear()
        header()

        # MATRIX MODE BACKGROUND
        if display_mode == "matrix":
            for _ in range(3):
                print("\033[92m" + matrix_line() + "\033[0m")

        # Tower Animation
        draw_tower(step)

        # Device Viewer
        show_devices()

        # Alerts
        if engine.alert_log:
            show_alerts()
            play_alert_sound()

        step += 1
        time.sleep(0.5)


# ------------------------------------------------------------
# SETTINGS MENU (Optional)
# ------------------------------------------------------------
def settings_menu():
    global display_mode, alert_sound_enabled

    while True:
        clear()
        print("=== SETTINGS ===\n")
        print(f"1. Display Mode      : {display_mode}")
        print(f"2. Alert Sound       : {'ON' if alert_sound_enabled else 'OFF'}")
        print("3. Back")
        print("\nChoose option: ", end="")

        choice = input().strip()

        if choice == "1":
            display_mode = input("Enter mode (clean/hacker/matrix): ").strip()
        elif choice == "2":
            alert_sound_enabled = not alert_sound_enabled
        elif choice == "3":
            break


# ------------------------------------------------------------
# START UI + ENGINE
# ------------------------------------------------------------
def start_ui():
    engine.start()
    ui_loop()
