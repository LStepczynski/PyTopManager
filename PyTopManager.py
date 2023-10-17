from ManagerWindow import ClipboardWindow, WebsiteWindow
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

        self.webpage_list_file = "webpages.txt"
        self.webpage_list = self.load_webpages(self.webpage_list_file)
        print(self.webpage_list)
        
    
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

            WebsiteWindow(self, 
                            (screen_width//2 - width//2, screen_height//2 - height//2), 
                            (width, height))
        
    def load_webpages(self, file_name):
        url_list = []
        
        try:
            with open(file_name, 'r') as file:
                for line in file:
                    url_list.append(line.strip())
        except FileNotFoundError:
            return ["" for _ in range(10)]

        # Fill the list with empty strings up to a maximum of 10 elements
        while len(url_list) < 10:
            url_list.append("")

        return url_list


    def activate(self):
        """Do something while is_working"""
        while self.is_working:
            time.sleep(0.05)
            self.check_key()

