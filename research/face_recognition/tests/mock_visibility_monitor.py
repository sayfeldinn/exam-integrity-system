"""
A simple mock of your teammate's visibility monitor feature to test integration logic locally.
"""

class SystemStatus:
    NORMAL = "NORMAL"
    NO_FACE = "NO FACE"
    MULTIPLE_FACES = "MULTIPLE FACES"


def fake_on_status_change(status, message=None):
    print(f"[MOCK visibility_monitor] status={status} message={message}")