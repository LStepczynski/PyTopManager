from ManagerWindow import TopManagerPopUp
import pyperclip
import keyboard
import ctypes
import time

class PyTopManager:
    """Class that will manage different functions of the desktop"""
    def __init__(self, is_working):
        self.is_working = is_working
        self.clipboard_list = ['' for _ in range(10)] # Contents of the clipboards
        self.current_clipboard = 0                    # Current Clipboard index
    
    def change_clipboard(self, clipboard_index):
        self.clipboard_list[self.current_clipboard] = pyperclip.paste()
        self.current_clipboard = clipboard_index
        pyperclip.copy(self.clipboard_list[self.current_clipboard])

    def check_key(self):
        if keyboard.is_pressed('SHIFT') and keyboard.is_pressed('a') and keyboard.is_pressed("CTRL"):
            self.clipboard_list[self.current_clipboard] = pyperclip.paste()
            screen_width = ctypes.windll.user32.GetSystemMetrics(0)
            screen_height = ctypes.windll.user32.GetSystemMetrics(1)

            width = 300
            height = 400

            TopManagerPopUp(self, 
                            (screen_width//2 - width//2, screen_height//2 - height//2), 
                            (width, height))

    def activate(self):
        """Do something while is_working"""
        while self.is_working:
            time.sleep(0.05)
            self.check_key()

