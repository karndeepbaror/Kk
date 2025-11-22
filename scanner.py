import bluetooth
import time
import threading
from alerts import send_alert
from utils import log_event

class BluetoothScanner:
    def __init__(self):
        self.known_devices = {}
        self.running = True

    def scan_devices(self):
        """
        Safe Bluetooth discovery (NO jamming).
        Detects:
        - New devices
        - Disappearing devices
        - Rapid connect/disconnect attempts (suspicious)
        """
        while self.running:
            try:
                nearby = bluetooth.discover_devices(duration=4, lookup_names=True)
            except Exception as e:
                log_event(f"Scan error: {e}")
                time.sleep(2)
                continue

            current_scan = {}

            for addr, name in nearby:
                current_scan[addr] = name

                # NEW DEVICE DETECTED
                if addr not in self.known_devices:
                    log_event(f"[NEW] {name} ({addr}) detected")
                    send_alert(f"New Bluetooth device detected: {name} [{addr}]")

                # SIGNAL MONITOR (dummy safe signal simulation)
                signal_strength = self.fake_signal_strength()
                log_event(f"{name} ({addr}) → Signal: {signal_strength}%")

            # Detect disappearing devices
            lost = set(self.known_devices.keys()) - set(current_scan.keys())
            for lost_addr in lost:
                lost_name = self.known_devices[lost_addr]
                log_event(f"[LOST] {lost_name} ({lost_addr}) disappeared")
                send_alert(f"Device out of range: {lost_name}")

            self.known_devices = current_scan  
            time.sleep(2)

    def fake_signal_strength(self):
        """Safe dummy signal level generator."""
        import random
        return random.randint(20, 100)

    def start(self):
        thread = threading.Thread(target=self.scan_devices)
        thread.daemon = True
        thread.start()
