import tkinter as tk
import sys
import os
import time
try:
    from screeninfo import get_monitors
    screeninfo_available = True
except ImportError:
    print("Warning: screeninfo not installed.")
    screeninfo_available = False

class RedDotApp:
    def __init__(self):
        self.root = tk.Tk()
        print("Initializing Tkinter window")
        self.is_visible = True
        self.window_size = 4
        self.signal_file = os.path.expanduser("~/.red_dot_toggle")
        self.last_file_mtime = 0  # Track file modification time
        # Initialize signal file
        try:
            with open(self.signal_file, 'w') as f:
                f.write('')
            os.chmod(self.signal_file, 0o666)  # Ensure writable
            print(f"Initialized signal file: {self.signal_file}")
        except Exception as e:
            print(f"Error initializing signal file: {e}")
        self.initUI()

    def initUI(self):
        try:
            self.root.attributes('-alpha', 0.0)  # Transparent background
            self.root.attributes('-topmost', True)  # Always on top
            self.root.overrideredirect(True)  # No decorations
            self.root.config(cursor='none')
            print("Window properties set: transparent, topmost, cursor hidden")
        except Exception as e:
            print(f"Error setting window properties: {e}")
            sys.exit(1)

        # Get monitor details
        screen_x, screen_y, screen_width, screen_height = self.get_monitor_details()

        # Position window (1 pixel right and down from center)
        x_position = screen_x + (screen_width - self.window_size) // 2 + 1
        y_position = screen_y + (screen_height - self.window_size) // 2 + 1
        try:
            self.root.geometry(f"{self.window_size}x{self.window_size}+{x_position}+{y_position}")
            print(f"Window geometry set at: ({x_position}, {y_position})")
        except Exception as e:
            print(f"Error setting geometry: {e}")
            sys.exit(1)

        # Create canvas for red dot
        self.canvas = tk.Canvas(self.root, width=self.window_size, height=self.window_size, highlightthickness=0, borderwidth=0)
        self.canvas.pack()
        self.canvas.config(cursor='none')
        self.canvas.create_oval(0, 0, self.window_size, self.window_size, fill="red", outline="red")
        print("Red dot drawn")

        # Bind Ctrl+Q to exit
        try:
            self.root.bind('<Control-q>', lambda e: self.root.quit())
            print("Ctrl+Q bound for exit")
        except Exception as e:
            print(f"Error binding Ctrl+Q: {e}")

        # Start checking signal file
        self.check_signal()

    def get_monitor_details(self):
        if screeninfo_available:
            try:
                monitors = get_monitors()
                print("Detected monitors:")
                for i, m in enumerate(monitors):
                    print(f"Monitor {i}: {m.width}x{m.height}, Position: ({m.x}, {m.y}), Primary: {m.is_primary}")
                for m in monitors:
                    if m.is_primary:
                        print(f"Using primary monitor: {m.width}x{m.height}")
                        return m.x, m.y, m.width, m.height
                print("No primary monitor, using first monitor")
                return monitors[0].x, monitors[0].y, monitors[0].width, monitors[0].height
            except Exception as e:
                print(f"Error detecting monitors: {e}")
        print("Using default: 1920x1080")
        return 0, 0, 1920, 1080

    def toggle_visibility(self):
        try:
            print(f"Toggling visibility (current: {self.is_visible})")
            if self.is_visible:
                self.root.withdraw()
                print("Hiding red dot")
            else:
                self.root.deiconify()
                self.root.attributes('-topmost', True)  # Re-ensure topmost
                print("Showing red dot")
            self.is_visible = not self.is_visible
        except Exception as e:
            print(f"Error toggling visibility: {e}")

    def check_signal(self):
        try:
            file_exists = os.path.exists(self.signal_file)
            mtime = os.path.getmtime(self.signal_file) if file_exists else 0
            print(f"Checking signal file: exists={file_exists}, mtime={mtime}, last_mtime={self.last_file_mtime}, is_visible={self.is_visible}")
            if file_exists != self.is_visible or (file_exists and mtime > self.last_file_mtime):
                self.toggle_visibility()
                self.last_file_mtime = mtime if file_exists else time.time()
            self.root.after(200, self.check_signal)  # Increased to 200ms
        except Exception as e:
            print(f"Error checking signal: {e}")
            self.root.after(200, self.check_signal)

    def run(self):
        try:
            print("Starting Tkinter main loop")
            self.root.mainloop()
        except Exception as e:
            print(f"Error in main loop: {e}")
            sys.exit(1)

def main():
    app = RedDotApp()
    app.run()

if __name__ == '__main__':
    main()