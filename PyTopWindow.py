from tkinter import messagebox
import tkinter as tk
import webbrowser
import subprocess
import threading
import json
import os


class Window:
    def __init__(self, pyTopManager, position, size, on_press_func, argslist = None):
        
        self.pyTopManager = pyTopManager 
        self.position = position # Position on the screen the window will show up at

        self.argslist = argslist

        self.root = tk.Tk()
        self.root.geometry(f'{size[0]}x{size[1]}+{position[0]}+{position[1]}')
        self.root.attributes("-topmost", True)
        self.root.attributes("-toolwindow", True)

        self.root.bind("<KeyPress>", self.on_key_press)
        self.on_press_func = on_press_func


    def add_element(self, index, title, submit_func):
        """Window to ask the user for an url"""
        self.topwindow = tk.Toplevel(self.root)
        self.topwindow.title("Add Webpage")
        self.topwindow.geometry("360x260")
        self.topwindow.attributes("-topmost", True)
        self.topwindow.attributes("-toolwindow", True)

        # Main label of the add webpage window
        self.topwindow_label = tk.Label(self.topwindow, text=f"Enter a Label and\n {title}", font=('',20))
        self.topwindow_label.pack()

        # URL entry of the add webpage window
        self.topwindow_label_input = tk.Entry(self.topwindow, font=('',15))
        self.topwindow_label_input.pack(pady=20)

        self.topwindow_url_input = tk.Entry(self.topwindow, font=('',15))
        self.topwindow_url_input.pack(pady=20)

        self.topwindow_submit = tk.Button(self.topwindow, 
                                          text="Submit", 
                                          font=('', 15), 
                                          command=lambda: submit_func(index, self.topwindow_label_input.get(), self.topwindow_url_input.get()))
        self.topwindow_submit.pack()


    def on_key_press(self, event):
        """Listens for a number and activates the function linked to it"""
        key = event.keysym
        for index in range(10):
            if key != str(index):
                continue

            if not self.argslist:
                self.on_press_func(index)
            else:
                self.on_press_func(self.argslist[f"{index}"]["value"], index)


class ManagerWindow:
    """Manager Window that allows the user to close the program as well as read more about it"""
    def __init__(self, pyTopManager):
        """Takes in a PyTopManager class object and opens a tkinter window"""
        
        #The PyTopManager object
        self.pyTopManager = pyTopManager

        #Tkinter window
        self.root = tk.Tk()
        self.root.geometry("400x225")
        self.root.title("PyTopManager")

        # Main Label of the Main window
        self.main_label = tk.Label(self.root, text="PyTopManager\nIs Currently Working", font=("", 25))
        self.main_label.pack(pady=15)

        #Label of the Main window
        self.info = tk.Label(self.root, text="Close This Window To Close the Program", font=('', 15))
        self.info.pack(pady=15)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack()

        # Button redirecting to the github page
        self.github = tk.Button(self.button_frame, width=12, text="How To Use ?", command=self.howToUse, font=('', 15))
        self.github.grid(row=0, column=0, padx=10)

        # Button opening the settings window
        self.settings = tk.Button(self.button_frame, width=12, text="Settings", command=self.pyTopManager.settings, font=('', 15))
        self.settings.grid(row=0, column=1, padx=10)

        # Bind the close event to a function
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.root.mainloop()

    def howToUse(self):
        """Redirects the user to the project's github page"""
        webbrowser.open_new_tab("https://github.com/LStepczynski/PyTopManager")

    def on_close(self):
        """Closes the tkinter window and sets the PyTopManager object's property is_working to False"""
        self.pyTopManager.is_working = False
        self.root.destroy()



class ClipboardWindow(Window):
    """GUI interface for switching between clipboards"""
    def __init__(self, pyTopManager, position, size):
        super().__init__(pyTopManager, 
                         position, 
                         size, 
                         self.change_clipboard)
        
        self.root.title("Clipboard Window")

        # Creates the buttons to switch between clipboards
        for index, element in enumerate(self.pyTopManager.clipboard_list):
            label = f"Clipboard {index}: "
            if len(element) == 0:
                label += "EMPTY"
            elif len(element) <= 15:
                label += element
            else:
                label += element[:15] + "..."

            tk.Button(self.root, 
                      text=label, 
                      height=1,
                      bg= "lightgray" if self.pyTopManager.current_clipboard == index else "white",
                      font=('',15), 
                      command=lambda i=index: self.change_clipboard(i)).pack(fill='x')
    
        self.root.focus_force()
        self.root.mainloop()
                

    def change_clipboard(self, index):
        """Changes to a different clipboard"""
        self.pyTopManager.change_clipboard(index)
        self.root.destroy()



class WebsiteWindow(Window):
    """GUI interface for quick opening of websites"""
    def __init__(self, pyTopManager, position, size):
        
        super().__init__(pyTopManager, 
                         position, 
                         size, 
                         self.open_webpage,
                         pyTopManager.webpage_list)
        
        self.root.title("Webpage Window")

        # Creates the buttons that will open websites
        for index, element in enumerate([value["label"] for value in self.pyTopManager.webpage_list.values()]):

            # Shortens the text if it is too long
            if element == "":
                label = "Add Website"
            elif len(element) >= 20:
                label = element[:20] + "..."
            else: 
                label = element

            frame = tk.Frame(self.root)
            
            # Create a button that will either open a website or ask to set a website to the button
            tk.Button(
                frame, 
                text=label, 
                height=1,
                width=24,
                font=('', 15), 
                command=lambda label=label, i=index: self.open_webpage(label, i)
            ).grid(row=index, column=0) 
            
            # Create a delete button to delete a website from the button
            tk.Button(
                frame, 
                text="X", 
                height=1,
                font=('', 15), 
                command=lambda i=index: self.submit_webpage(i, "", "")
            ).grid(row=index, column=1) 
            
            frame.pack(fill='x')

    
        self.root.focus_force()
        self.root.mainloop()


    def open_webpage(self, label, index):
        """Opens a webpage or asks for an url"""

        # If button is not linked to any website asks for an URL
        if label == "Add Website" or "":
            self.add_element(index, "a URL", self.submit_webpage)
        
        # Opens a website and destroys the window
        else:
            webbrowser.open(self.pyTopManager.webpage_list[f"{index}"]["value"])
            self.root.destroy()


    def submit_webpage(self, index, label, url):
        """Reads the URL in the self.topwindow_input and edits the file where webpages are stored"""
        self.pyTopManager.webpage_list[f"{index}"] = {"value":url, "label":label}
        with open(self.pyTopManager.webpage_list_file, 'w') as file:
            json.dump(self.pyTopManager.webpage_list, file, indent=4)
        self.root.destroy()


class CommandWindow(Window):
    """GUI interface to quickly run commands"""
    def __init__(self, pyTopManager, position, size):
        super().__init__(pyTopManager, 
                         position, 
                         size, 
                         self.run_command,
                         pyTopManager.command_list)

        self.root.title("Command Window")

        # Creates the buttons to quickly run commands
        for index, element in enumerate([value["label"] for value in self.pyTopManager.command_list.values()]):
            
            # Shortens the text if too long
            if element == "":
                label = "Add Command"
            elif len(element) >= 20:
                label = element[:20] + "..."
            else: 
                label = element

            frame = tk.Frame(self.root)
            
            # Create a button with label running a command
            tk.Button(
                frame, 
                text=label, 
                height=1,
                width=24,
                font=('', 15), 
                command=lambda label=label, i=index: self.run_command(label, i)
            ).grid(row=index, column=0) 
            
            # Create a delete button to delete a command
            tk.Button(
                frame, 
                text="X", 
                height=1,
                font=('', 15), 
                command=lambda i=index: self.submit_command(i, "", "")
            ).grid(row=index, column=1) 
            
            frame.pack(fill='x')

    
        self.root.focus_force()
        self.root.mainloop()


    def submit_command(self, index, label, command):
        """Changes a command to a new one"""
        self.pyTopManager.command_list[f"{index}"] = {"value":command, "label":label}
        with open(self.pyTopManager.command_list_file, 'w') as file:
            json.dump(self.pyTopManager.command_list, file, indent=4)
        self.root.destroy()


    def run_command(self, label, index):
        """Runs a command or asks for one"""

        # If the button is not linked to any command asks for one
        if label == "Add Command" or "":
            self.add_element(index, "a Command", self.submit_command)

        # Runs the command linked to the button
        else:
            threading.Thread(target=os.system, args=(self.pyTopManager.command_list[f"{index}"]["value"],)).start()
            self.root.destroy()


class ExecutableWindow(Window):
    """GUI interface to quickly open files"""
    def __init__(self, pyTopManager, position, size):
        super().__init__(pyTopManager, 
                         position, 
                         size, 
                         self.run_program,
                         pyTopManager.webpage_list)

        self.root.title("Executable Window")

        # Creates the buttons to quickly run commands
        for index, element in enumerate([value["label"] for value in self.pyTopManager.executable_list.values()]):
            
            # Shortens the text if too long
            if element == "":
                label = "Add path to .exe"
            elif len(element) >= 20:
                label = element[:20] + "..."
            else: 
                label = element

            frame = tk.Frame(self.root)
            
            # Create a button with label running a command
            tk.Button(
                frame, 
                text=label, 
                height=1,
                width=24,
                font=('', 15), 
                command=lambda label=label, i=index: self.run_program(label, i)
            ).grid(row=index, column=0) 
            
            # Create a delete button to delete a command
            tk.Button(
                frame, 
                text="X", 
                height=1,
                font=('', 15), 
                command=lambda i=index: self.submit_program(i, "", "")
            ).grid(row=index, column=1) 
            
            frame.pack(fill='x')

    
        self.root.focus_force()
        self.root.mainloop()


    def submit_program(self, index, label, command):
        """Changes a command to a new one"""
        self.pyTopManager.executable_list[f"{index}"] = {"value":command, "label":label}
        with open(self.pyTopManager.executable_list_file, 'w') as file:
            json.dump(self.pyTopManager.executable_list, file, indent=4)
        self.root.destroy()


    def run_program(self, label, index):
        """Runs a command or asks for one"""

        # If the button is not linked to any command asks for one
        if label == "Add path to .exe" or "":
            self.add_element(index, "an Executable", self.submit_program)

        # Runs the command linked to the button
        else:
            self.root.destroy()
            try:
                subprocess.Popen(self.pyTopManager.executable_list[f"{index}"]["value"])
            except Exception as e:
                messagebox.showerror("Execution problem", f"There has been a problem runing the executable file \n {e}")



class SettingsWindow:
    """GUI interface for the settings of the PyTopManager"""

    class ChangeKeybinds:
        """GUI interface to change keybinds of the PyTopManager application"""
        def __init__(self, parent, keybind_list, label, pyTopManager):
            self.parent = parent # The SettingsWindow object
            self.keybind_list = keybind_list 
            self.label_to_edit = label
            self.pyTopManager = pyTopManager

            self.root = tk.Toplevel(self.parent)
            self.root.title("Change Keybinds")
            self.root.geometry("300x130")
            self.root.attributes("-topmost", True)
            self.root.attributes("-toolwindow", True)
            self.keybind_index = 0

            # new keybinds for a selected window
            self.keybind_text = ["?" for _ in range(3)]

            # Main label of the ChangeKeybinds window
            self.main_label = tk.Label(self.root, text="Press the combination of\n keys you want to use", font=('', 18))
            self.main_label.pack(pady=10)

            # Label that shows the selected keybinds by the user of the ChangeKeybinds window
            self.keybind_label = tk.Label(self.root, text=f"{self.keybind_text[0]} + {self.keybind_text[1]} + {self.keybind_text[2]}", font=('', 20))
            self.keybind_label.pack()

            self.root.bind("<KeyPress>", self.on_key_press)


        def update_file(self):
            """Updates the file storing the keybinds"""
            with open(self.pyTopManager.keybind_file, 'w') as f:
                json.dump({key : value for key, value in zip(range(10), self.pyTopManager.keybind_lists)}, f, indent=4)


        def on_key_press(self, event):
            """Listens for 3 keys and sets them to the activation keybind of the selected window"""
            key = event.keysym
            
            # Converts the names of the key so the keyboard module can undestand them
            match key:
                case "Control_L":
                    key = 'CTRL'
                case "Control_R":
                    key = 'CTRL'
                case "Shift_L":
                    key = 'SHIFT'
                case "Shift_R":
                    key = 'SHIFT'
                case "Alt_L":
                    key = 'ALT'
                case "Alt_R":
                    key = 'ALT'

            # Sets the key as the new keybind
            self.keybind_list[self.keybind_index] = key.upper()

            # Updates the Label that shows the selected keybinds by the user of the ChangeKeybinds window
            for index in range(3):
                self.keybind_text[index] = key
                self.keybind_label.config(text=f"{self.keybind_text[0]} + {self.keybind_text[1]} + {self.keybind_text[2]}")

            # If the user already inputed 3 keys closes the window and updates the keybind label of the selected window
            if self.keybind_index == 2:
                self.keybind_index = 0
                self.label_to_edit.config(text=" + ".join(self.keybind_list))
                self.update_file()
                self.root.destroy()
                return

            self.keybind_index += 1

    def __init__(self, pyTopManger, position, size):
        self.pyTopManager = pyTopManger
        self.position = position # Position on the screen the window will show up at
        self.size = size

        self.root = tk.Tk()
        self.root.geometry(f'{size[0]}x{size[1]}+{position[0]}+{position[1]}')
        self.root.title("Settings")
        self.root.attributes("-topmost", True)
        self.root.attributes("-toolwindow", True)

        # Main label of the Settings window
        self.main_label = tk.Label(self.root, text="Settings", font=('',25))
        self.main_label.pack()

        # Clipboard Window
        self.clipboard_frame = tk.Frame(self.root)
        self.clipboard_frame.pack(pady=15)

        self.clipboard_label = tk.Label(self.clipboard_frame, text="Current Key Bind for the Clipboard window:", font=('',13))
        self.clipboard_label.pack()

        self.clipboard_inside_frame = tk.Frame(self.clipboard_frame)
        self.clipboard_inside_frame.pack(pady=10)

        # Label showing the current keybind for the clipboard window
        self.clipboard_keybind_label = tk.Label(self.clipboard_inside_frame, 
                                                text=" + ".join(self.pyTopManager.clipboard_window_keybinds),
                                                font=('', 12))
        self.clipboard_keybind_label.grid(row=0, column=0, padx=20)

        # Button launching the ChangeKeybinds window for the clipboard window
        self.clipboard_keybind_change = tk.Button(self.clipboard_inside_frame, 
                                                  text="Change", 
                                                  command=lambda: self.ChangeKeybinds(self.root, 
                                                                                      self.pyTopManager.clipboard_window_keybinds, 
                                                                                      self.clipboard_keybind_label,
                                                                                      self.pyTopManager))
        self.clipboard_keybind_change.grid(row=0, column=1, padx=20)

        # Webpage Window
        self.webpage_frame = tk.Frame(self.root)
        self.webpage_frame.pack(pady=15)

        self.webpage_label = tk.Label(self.webpage_frame, text="Current Key Bind for the Webpage window:", font=('',13))
        self.webpage_label.pack()

        self.webpage_inside_frame = tk.Frame(self.webpage_frame)
        self.webpage_inside_frame.pack(pady=10)

        # Label showing the current keybind for the webpage window
        self.webpage_keybind_label = tk.Label(self.webpage_inside_frame, 
                                                text=" + ".join(self.pyTopManager.webpage_window_keybinds),
                                                font=('', 12))
        self.webpage_keybind_label.grid(row=0, column=0, padx=20)

        # Button launching the ChangeKeybinds window for the webpage window
        self.webpage_keybind_change = tk.Button(self.webpage_inside_frame, 
                                                  text="Change", 
                                                  command=lambda: self.ChangeKeybinds(self.root, 
                                                                                      self.pyTopManager.webpage_window_keybinds, 
                                                                                      self.webpage_keybind_label,
                                                                                      self.pyTopManager))
        self.webpage_keybind_change.grid(row=0, column=1, padx=20)

        # Command Window
        self.command_frame = tk.Frame(self.root)
        self.command_frame.pack(pady=15)

        self.command_label = tk.Label(self.command_frame, text="Current Key Bind for the Command window:", font=('',13))
        self.command_label.pack()

        self.command_inside_frame = tk.Frame(self.command_frame)
        self.command_inside_frame.pack(pady=10)

        # Label showing the current keybind for the command window
        self.command_keybind_label = tk.Label(self.command_inside_frame, 
                                                text=" + ".join(self.pyTopManager.command_window_keybinds),
                                                font=('', 12))
        self.command_keybind_label.grid(row=0, column=0, padx=20)

        # Button launching the ChangeKeybinds window for the command window
        self.command_keybind_change = tk.Button(self.command_inside_frame, 
                                                  text="Change", 
                                                  command=lambda: self.ChangeKeybinds(self.root, 
                                                                                      self.pyTopManager.command_window_keybinds, 
                                                                                      self.command_keybind_label,
                                                                                      self.pyTopManager))
        self.command_keybind_change.grid(row=0, column=1, padx=20)

        # Executable Window
        self.executable_frame = tk.Frame(self.root)
        self.executable_frame.pack(pady=15)

        self.executable_label = tk.Label(self.executable_frame, text="Current Key Bind for the Executable window:", font=('',13))
        self.executable_label.pack()

        self.executable_inside_frame = tk.Frame(self.executable_frame)
        self.executable_inside_frame.pack(pady=10)

        # Label showing the current keybind for the executable window
        self.executable_keybind_label = tk.Label(self.executable_inside_frame, 
                                                text=" + ".join(self.pyTopManager.executable_window_keybinds),
                                                font=('', 12))
        self.executable_keybind_label.grid(row=0, column=0, padx=20)

        # Button launching the ChangeKeybinds window for the executable window
        self.executable_keybind_change = tk.Button(self.executable_inside_frame, 
                                                  text="Change", 
                                                  command=lambda: self.ChangeKeybinds(self.root, 
                                                                                      self.pyTopManager.executable_window_keybinds, 
                                                                                      self.executable_keybind_label,
                                                                                      self.pyTopManager))
        self.executable_keybind_change.grid(row=0, column=1, padx=20)

        self.root.mainloop()