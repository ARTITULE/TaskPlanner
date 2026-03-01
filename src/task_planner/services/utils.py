import subprocess
from PyQt5.QtGui import QPalette

def get_system_theme():
    try:
        result = subprocess.run(
            ['defaults', 'read', '-g', 'AppleInterfaceStyle'],
            capture_output=True, text=True
        )
        return "dark" if "Dark" in result.stdout else "light"
    except Exception:
        return "light"
