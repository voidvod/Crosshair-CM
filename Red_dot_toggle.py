import os
import sys
signal_file = os.path.expanduser("~/.red_dot_toggle")
print(f"Attempting to access signal file: {signal_file}")
try:
    if os.path.exists(signal_file):
        os.remove(signal_file)
        print("Signaled to hide red dot")
    else:
        with open(signal_file, 'w') as f:
            f.write('')
        os.chmod(signal_file, 0o666)  # Ensure writable
        print("Signaled to show red dot")
except Exception as e:
    print(f"Error modifying signal file: {e}")
    sys.exit(1)