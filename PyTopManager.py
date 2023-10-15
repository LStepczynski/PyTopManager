import pyperclip
import keyboard
import time

class PyTopManager:
    """Class that will manage different functions of the desktop"""
    def __init__(self, is_working):
        self.is_working = is_working
        self.clipboar_list = ['' for _ in range(10)] # Contents of the clipboards
        self.current_clipboard = 1                   # Current Clipboard index
    
    def change_clipboard(self, clipboard_index):
        self.clipboar_list[self.current_clipboard] = pyperclip.paste()
        self.current_clipboard = clipboard_index
        pyperclip.copy(self.clipboar_list[self.current_clipboard])

    def check_key(self):
        if keyboard.is_pressed('SHIFT') and keyboard.is_pressed('a'):
            for index in range(10):
                if keyboard.is_pressed(f"{index}"):
                    self.change_clipboard(index)

    def activate(self):
        """Do something while is_working"""
        while self.is_working:
            time.sleep(0.05)
            self.check_key()

