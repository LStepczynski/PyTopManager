from PyTopWindow import ClipboardWindow, WebsiteWindow, CommandWindow, ExecutableWindow, SettingsWindow
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

        # Contains saved webpages
        self.webpage_list_file = "webpages.txt"
        self.webpage_list = self.load_file(self.webpage_list_file)
        
        # Contains saved commands
        self.command_list_file = "commands.txt"
        self.command_list = self.load_file(self.command_list_file)

        # Contains saved programs
        self.executable_list_file = "executables.txt"
        self.executable_list = self.load_file(self.executable_list_file)

        self.clipboard_window_keybinds = ["CTRL", "SHIFT", "A"]
        self.webpage_window_keybinds = ["CTRL", "SHIFT", "S"]
        self.command_window_keybinds = ["CTRL", "SHIFT", "D"]
        self.executable_window_keybinds = ["CTRL", "SHIFT", "F"]

        self.lists = [self.webpage_list, self.command_list, self.executable_list]
        self.keybind_lists = [self.clipboard_window_keybinds,
                              self.webpage_window_keybinds,
                              self.command_window_keybinds,
                              self.executable_window_keybinds]

        self.screen_width = ctypes.windll.user32.GetSystemMetrics(0)
        self.screen_height = ctypes.windll.user32.GetSystemMetrics(1)

        # Keybinds for each window
        self.keybind_file = "keybinds.txt"
        try:
            with open(self.keybind_file, 'r') as f:
                lines = f.read().splitlines()  # Read lines and strip newline characters

                if len(lines) != 4:
                    raise Exception
                for line in lines:
                    if len(line.split()) != 3:
                        raise Exception
                    
                for index, keybind_list in enumerate(self.keybind_lists):
                    keybind_list = lines[index].split()

        except Exception:
            pass


    def settings(self):
        """Opens the settings window"""
        SettingsWindow(self,
                       (self.screen_width//2 - 400//2, self.screen_height//2 - 400//2),
                       (400, 450))
        
    
    def change_clipboard(self, clipboard_index):
        """Changes the clipboard to a different one"""
        self.clipboard_list[self.current_clipboard] = pyperclip.paste()
        self.current_clipboard = clipboard_index
        pyperclip.copy(self.clipboard_list[self.current_clipboard])

    def check_key(self):
        """Checks for keycombinations to open a window"""
        clipboard = self.clipboard_window_keybinds
        webpage = self.webpage_window_keybinds
        command = self.command_window_keybinds
        executable = self.executable_window_keybinds
        width = 300
        height = 400

        # Opens the clipboard window
        if keyboard.is_pressed(clipboard[0]) and keyboard.is_pressed(clipboard[1]) and keyboard.is_pressed(clipboard[2]):
            self.clipboard_list[self.current_clipboard] = pyperclip.paste()

            ClipboardWindow(self, 
                            (self.screen_width//2 - width//2, self.screen_height//2 - height//2), 
                            (width, height))
        
        # Opens the webpage window
        elif keyboard.is_pressed(webpage[0]) and keyboard.is_pressed(webpage[1]) and keyboard.is_pressed(webpage[2]):
            WebsiteWindow(self, 
                        (self.screen_width//2 - width//2, self.screen_height//2 - height//2), 
                        (width, height))
            
        # Opens the command window
        elif keyboard.is_pressed(command[0]) and keyboard.is_pressed(command[1]) and keyboard.is_pressed(command[2]):
            CommandWindow(self, 
                        (self.screen_width//2 - width//2, self.screen_height//2 - height//2), 
                        (width, height))
            
        # Opens the executable window
        elif keyboard.is_pressed(executable[0]) and keyboard.is_pressed(executable[1]) and keyboard.is_pressed(executable[2]):
            ExecutableWindow(self, 
                        (self.screen_width//2 - width//2, self.screen_height//2 - height//2), 
                        (width, height))


    def load_file(self, file_name):
        """Reads the contents of the file and returns a minimum of 10 elements"""
        text_list = []
        
        try:
            with open(file_name, 'r') as file:
                for line in file:
                    text_list.append(line.strip())
        except FileNotFoundError:
            return ["" for _ in range(10)]

        # Fill the list with empty strings up to a maximum of 10 elements
        while len(text_list) < 10:
            text_list.append("")

        return text_list


    def activate(self):
        """Checks for the key combinations while self.is_working"""
        while self.is_working:
            time.sleep(0.05)
            self.check_key()

