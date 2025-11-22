# ============================================================
#  BLUETOOTH ENGINE - System Security
# ============================================================

import sys
import os
import time

# Force working directory to the project root
ROOT = os.path.dirname(os.path.abspath(__file__))
ENGINE_DIR = os.path.join(ROOT, "BluetoothEngine")

# Add BluetoothEngine folder to Python PATH
sys.path.insert(0, ENGINE_DIR)

# Try importing engine module
try:
    from engine import BluetoothEngine
except Exception as e:
    print("\n[ERROR] Unable to load engine module!")
    print("Reason:", e)
    print("Make sure your folder structure is correct.\n")
    sys.exit(1)

def main():
    print("\n====================================================")
    print("   BLUETOOTH ENGINE - LAUNCHER")
    print("====================================================\n")

    print("[✓] Engine folder loaded:", ENGINE_DIR)
    time.sleep(0.8)

    try:
        engine = BluetoothEngine()
        engine.start()
    except Exception as e:
        print("\n[FATAL ERROR] Bluetooth Engine crashed!")
        print("Reason:", e)
        sys.exit(1)

    print("\n[✓] System running...")
    print("[i] Press CTRL+C to exit.\n")

    # Keep process alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n[✓] Shutdown complete.")
        sys.exit(0)


if __name__ == "__main__":
    main()
