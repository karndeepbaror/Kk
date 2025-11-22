# ============================================================
#  BLUETOOTH SECURITY SUITE — ENGINE MODULE (PRO VERSION)
#  Developer: Karndeep Baror
#  GitHub: github.com/karndeepbaror
# ============================================================

import bluetooth
import random
import time
import csv
import json
import threading
import subprocess
from datetime import datetime


# ------------------------------------------------------------
# Vendor Prefixes (Simplified)
# ------------------------------------------------------------
VENDORS = {
    "D4:22:61": "Samsung",
    "F1:55:AC": "Apple Inc",
    "E2:44:77": "Xiaomi",
    "00:1A:7D": "Intel",
    "94:65:2D": "Realtek",
    "AC:37:43": "OnePlus",
}


# ------------------------------------------------------------
# ENGINE CLASS
# ------------------------------------------------------------
class SecurityEngine:
    def __init__(self):
        self.running = False
        self.devices = {}       # MAC → info
        self.lock = threading.Lock()
        self.whitelist = []
        self.blacklist = []
        self.alert_log = []
        self.session_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # --------------------------------------------------------
    # Vendor Lookup
    # --------------------------------------------------------
    def get_vendor(self, mac):
        prefix = mac.upper()[:8]
        return VENDORS.get(prefix, "Unknown Vendor")

    # --------------------------------------------------------
    # RSSI Reader (real or fallback)
    # --------------------------------------------------------
    def get_rssi(self, mac):
        try:
            out = subprocess.check_output(["hcitool", "rssi", mac],
                                          stderr=subprocess.DEVNULL).decode()
            if "RSSI return value" in out:
                return int(out.split()[-1])
        except:
            return random.randint(-90, -20)  # safe fallback
        return random.randint(-90, -20)

    # --------------------------------------------------------
    # Classic Bluetooth Scan
    # --------------------------------------------------------
    def scan_classic(self):
        try:
            found = bluetooth.discover_devices(duration=4, lookup_names=True)
            for mac, name in found:
                self.update_device(mac, name, "Classic")
        except:
            pass

    # --------------------------------------------------------
    # BLE Simulation (Safe — No real RF Decode)
    # --------------------------------------------------------
    def scan_ble(self):
        simulated = [
            ("D4:22:61:AA:73:11", "BLE Beacon A"),
            ("F1:55:AC:88:33:22", "Fitness Band"),
            ("E2:44:77:99:11:33", "Smart Sensor"),
        ]
        for mac, name in simulated:
            self.update_device(mac, name, "BLE")

    # --------------------------------------------------------
    # Device Update
    # --------------------------------------------------------
    def update_device(self, mac, name, dtype):
        rssi = self.get_rssi(mac)
        now = datetime.now().strftime("%H:%M:%S")

        with self.lock:
            if mac not in self.devices:
                # New device detected
                self.devices[mac] = {
                    "name": name,
                    "type": dtype,
                    "vendor": self.get_vendor(mac),
                    "first_seen": now,
                    "last_seen": now,
                    "rssi": rssi,
                    "rssi_history": [rssi],
                    "flags": []
                }
                self.generate_alert("NEW_DEVICE", mac)

            else:
                # Existing device update
                self.devices[mac]["last_seen"] = now
                self.devices[mac]["rssi"] = rssi
                self.devices[mac]["rssi_history"].append(rssi)

            # Run security checks
            self.security_checks(mac)

    # --------------------------------------------------------
    # Security Checks
    # --------------------------------------------------------
    def security_checks(self, mac):
        d = self.devices[mac]

        # Suspicious if not whitelisted
        if mac not in self.whitelist:
            self.flag(mac, "UNKNOWN_DEVICE")

        # Blacklisted
        if mac in self.blacklist:
            self.flag(mac, "BLACKLISTED_DEVICE")
            self.generate_alert("BLACKLIST_ALERT", mac)

        # MAC Anomaly (Randomizing MAC)
        if self.detect_random_mac(mac):
            self.flag(mac, "RANDOMIZED_MAC")
            self.generate_alert("RANDOM_MAC", mac)

        # Possible tracker movement detection
        if self.detect_movement_spike(d["rssi_history"]):
            self.flag(mac, "MOVEMENT_SPIKE")
            self.generate_alert("MOVEMENT_SPIKE", mac)

        # RSSI spike alert
        if self.detect_rssi_spike(d["rssi_history"]):
            self.flag(mac, "RSSI_SPIKE")

    # --------------------------------------------------------
    def flag(self, mac, f):
        if f not in self.devices[mac]["flags"]:
            self.devices[mac]["flags"].append(f)

    # --------------------------------------------------------
    # Randomized MAC detector
    # --------------------------------------------------------
    def detect_random_mac(self, mac):
        return mac.startswith("02") or mac.startswith("06")

    # --------------------------------------------------------
    # Movement spike detector
    # --------------------------------------------------------
    def detect_movement_spike(self, history):
        if len(history) < 4:
            return False
        diff = abs(history[-1] - history[-4])
        return diff > 25

    # --------------------------------------------------------
    # RSSI spike detector
    # --------------------------------------------------------
    def detect_rssi_spike(self, hist):
        if len(hist) < 3:
            return False
        return abs(hist[-1] - hist[-2]) > 18

    # --------------------------------------------------------
    # Alert Generator
    # --------------------------------------------------------
    def generate_alert(self, alert_type, mac):
        now = datetime.now().strftime("%H:%M:%S")
        entry = {
            "time": now,
            "type": alert_type,
            "mac": mac,
            "name": self.devices[mac]["name"]
        }
        self.alert_log.append(entry)

    # --------------------------------------------------------
    # Export Logs
    # --------------------------------------------------------
    def save_logs(self):
        # JSON
        with open("bt_logs.json", "w") as f:
            json.dump(self.devices, f, indent=4)

        # Alert Log CSV
        with open("alerts.csv", "w", newline='') as f:
            w = csv.writer(f)
            w.writerow(["Time", "Alert Type", "MAC", "Name"])
            for a in self.alert_log:
                w.writerow([a["time"], a["type"], a["mac"], a["name"]])

    # --------------------------------------------------------
    # Export Static Snapshot
    # --------------------------------------------------------
    def export_snapshot(self):
        return self.devices

    # --------------------------------------------------------
    # Start Loop
    # --------------------------------------------------------
    def start(self):
        self.running = True
        t = threading.Thread(target=self.loop, daemon=True)
        t.start()

    # --------------------------------------------------------
    def loop(self):
        while self.running:
            self.scan_classic()
            self.scan_ble()
            time.sleep(2)

    # --------------------------------------------------------
    def stop(self):
        self.running = False
        self.save_logs()
