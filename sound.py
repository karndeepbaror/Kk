# ============================================================
#  BLUETOOTH SECURITY SUITE — SOUND ALERTS
# ============================================================

import platform
import os

def beep():
    """Play safe terminal beep for alerts"""
    try:
        if platform.system() == "Windows":
            import winsound
            winsound.Beep(1200, 200)
            winsound.Beep(1000, 200)
        else:
            # Linux / Mac terminal bell
            print("\a", end="")
    except:
        pass

def custom_alert(pattern=None):
    """
    Optional: custom beep pattern
    pattern = list of (freq, duration_ms)
    """
    try:
        if pattern is None:
            beep()
        else:
            if platform.system() == "Windows":
                import winsound
                for f, d in pattern:
                    winsound.Beep(f, d)
            else:
                beep()
    except:
        pass
