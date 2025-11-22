# ============================================================
#  BLUETOOTH SECURITY SUITE — MONITOR MODULE
# ============================================================

import time
from utils import log_event
from alerts import send_alert

class DeviceMonitor:
    def __init__(self, engine):
        self.engine = engine
        self.running = True

    def monitor_loop(self):
        """
        Live device behavior monitor:
        - Rapid signal change
        - Unknown devices appearing repeatedly
        - Blacklisted device attempts
        """
        while self.running:
            devices = self.engine.export_snapshot()
            for mac, d in devices.items():
                # Signal spike
                history = d.get("rssi_history", [])
                if len(history) >= 3:
                    diff = abs(history[-1] - history[-2])
                    if diff > 25:
                        log_event(f"Signal spike detected: {d['name']} ({mac})")
                        send_alert(f"Signal spike: {d['name']}")

                # Unknown device repeated
                if mac not in self.engine.whitelist:
                    send_alert(f"Unknown device present repeatedly: {d['name']}")

                # Blacklist
                if mac in self.engine.blacklist:
                    send_alert(f"Blacklisted device detected: {d['name']}")

            time.sleep(3)

    def start(self):
        import threading
        t = threading.Thread(target=self.monitor_loop, daemon=True)
        t.start()
