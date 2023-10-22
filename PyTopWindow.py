import tkinter as tk
import webbrowser
import threading
import os


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

        self.main_label = tk.Label(self.root, text="PyTopManager\nIs Currently Working", font=("", 25))
        self.main_label.pack(pady=15)

        self.info = tk.Label(self.root, text="Close This Window To Close the Program", font=('', 15))
        self.info.pack(pady=15)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack()

        self.github = tk.Button(self.button_frame, width=12, text="How To Use ?", command=self.howToUse, font=('', 15))
        self.github.grid(row=0, column=0, padx=10)

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



class ClipboardWindow:
    def __init__(self, pyTopManager, position, size):
        self.pyTopManager = pyTopManager
        self.position = position

        self.root = tk.Tk()
        self.root.title("Clipboards")
        self.root.geometry(f'{size[0]}x{size[1]}+{position[0]}+{position[1]}')
        self.root.attributes("-topmost", True)
        self.root.attributes("-toolwindow", True)

        self.root.bind("<KeyPress>", self.on_key_press)

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

    def on_key_press(self, event):
        key = event.keysym
        for index in range(10):
            if key != str(index):
                continue
            self.change_clipboard(index)
                

    def change_clipboard(self, index):
        self.pyTopManager.change_clipboard(index)
        self.root.destroy()



class WebsiteWindow:
    def __init__(self, pyTopManager, position, size):
        self.pyTopManager = pyTopManager
        self.position = position

        self.root = tk.Tk()
        self.root.title("Websites")
        self.root.geometry(f'{size[0]}x{size[1]}+{position[0]}+{position[1]}')
        self.root.attributes("-topmost", True)
        self.root.attributes("-toolwindow", True)

        self.root.bind("<KeyPress>", self.on_key_press)

        for index, element in enumerate(self.pyTopManager.webpage_list):
            if element == "":
                label = "Add Website"
            elif len(element) >= 20:
                label = element[:20] + "..."
            else: 
                label = element

            frame = tk.Frame(self.root)
            
            # Create a button with label text and a unique command based on the index 'i'
            tk.Button(
                frame, 
                text=label, 
                height=1,
                width=24,
                font=('', 15), 
                command=lambda label=label, i=index: self.open_webpage(label, i)
            ).grid(row=index, column=0) 
            
            # Create a delete button (assuming this is what it is for) with a unique command
            tk.Button(
                frame, 
                text="X", 
                height=1,
                font=('', 15), 
                command=lambda i=index: self.submit_webpage(i, "")
            ).grid(row=index, column=1) 
            
            frame.pack(fill='x')

    
        self.root.focus_force()
        self.root.mainloop()


    def open_webpage(self, label, index):
        if label == "Add Website" or "":
            self.add_webpage(index)
        else:
            webbrowser.open(self.pyTopManager.webpage_list[index])
            self.root.destroy()


    def add_webpage(self, index):
        self.topwindow = tk.Toplevel(self.root)
        self.topwindow.title("Add Webpage")
        self.topwindow.geometry("350x150")
        self.topwindow.attributes("-topmost", True)
        self.topwindow.attributes("-toolwindow", True)

        self.topwindow_label = tk.Label(self.topwindow, text="Enter an Url", font=('',20))
        self.topwindow_label.pack()
        self.topwindow_input = tk.Entry(self.topwindow, font=('',15))
        self.topwindow_input.pack(pady=20)
        self.topwindow_submit = tk.Button(self.topwindow, 
                                          text="Submit", 
                                          font=('', 15), 
                                          command=lambda: self.submit_webpage(index, self.topwindow_input.get()))
        self.topwindow_submit.pack()


    def submit_webpage(self, index, url):
        self.pyTopManager.webpage_list[index] = url
        with open(self.pyTopManager.webpage_list_file, 'w') as file:
            for line in self.pyTopManager.webpage_list:
                file.write(line + "\n")
        self.root.destroy()


    def on_key_press(self, event):
        key = event.keysym
        for index in range(10):
            if key != str(index):
                continue
            self.open_webpage(self.pyTopManager.webpage_list[index], index)



class CommandWindow:
    def __init__(self, pyTopManager, position, size):
            self.pyTopManager = pyTopManager
            self.position = position

            self.root = tk.Tk()
            self.root.title("Commands")
            self.root.geometry(f'{size[0]}x{size[1]}+{position[0]}+{position[1]}')
            self.root.attributes("-topmost", True)
            self.root.attributes("-toolwindow", True)

            self.root.bind("<KeyPress>", self.on_key_press)

            for index, element in enumerate(self.pyTopManager.command_list):
                if element == "":
                    label = "Add Command"
                elif len(element) >= 20:
                    label = element[:20] + "..."
                else: 
                    label = element

                frame = tk.Frame(self.root, bg='black')
                
                # Create a button with label text and a unique command based on the index 'i'
                tk.Button(
                    frame, 
                    text=label, 
                    height=1,
                    width=24,
                    font=('', 15), 
                    command=lambda label=label, i=index: self.run_command(label, i)
                ).grid(row=index, column=0) 
                
                # Create a delete button (assuming this is what it is for) with a unique command
                tk.Button(
                    frame, 
                    text="X", 
                    height=1,
                    font=('', 15), 
                    command=lambda i=index: self.submit_command(i, "")
                ).grid(row=index, column=1) 
                
                frame.pack(fill='x')

        
            self.root.focus_force()
            self.root.mainloop()


    def submit_command(self, index, command):
        self.pyTopManager.command_list[index] = command
        with open(self.pyTopManager.command_list_file, 'w') as file:
            for line in self.pyTopManager.command_list:
                file.write(line + "\n")
        self.root.destroy()


    def run_command(self, label, index):
        if label == "Add Command" or "":
            self.add_command(index)
        else:
            threading.Thread(target=os.system, args=(self.pyTopManager.command_list[index],)).start()
            self.root.destroy()


    def add_command(self, index):
        self.topwindow = tk.Toplevel(self.root)
        self.topwindow.title("Add Command")
        self.topwindow.geometry("350x150")
        self.topwindow.attributes("-topmost", True)
        self.topwindow.attributes("-toolwindow", True)

        self.topwindow_label = tk.Label(self.topwindow, text="Enter a command", font=('',20))
        self.topwindow_label.pack()
        self.topwindow_input = tk.Entry(self.topwindow, font=('',15))
        self.topwindow_input.pack(pady=20)
        self.topwindow_submit = tk.Button(self.topwindow, 
                                        text="Submit", 
                                        font=('', 15), 
                                        command=lambda: self.submit_command(index, self.topwindow_input.get()))
        self.topwindow_submit.pack()


    def on_key_press(self, event):
        key = event.keysym
        for index in range(10):
            if key != str(index):
                continue
            self.run_command(self.pyTopManager.command_list[index], index)
        


class SettingsWindow:
    def __init__(self, pyTopManger, position, size):
        self.pyTopManager = pyTopManger
        self.position = position
        self.size = size

        self.root = tk.Tk()
        self.root.geometry(f'{size[0]}x{size[1]}+{position[0]}+{position[1]}')
        self.root.title("Settings")
        self.root.attributes("-topmost", True)
        self.root.attributes("-toolwindow", True)

        self.main_label = tk.Label(self.root, text="Settings", font=('',25))
        self.main_label.pack()

        # Clipboard Window
        self.clipboard_frame = tk.Frame(self.root)
        self.clipboard_frame.pack(pady=15)

        self.clipboard_label = tk.Label(self.clipboard_frame, text="Current Key Bind for the Clipboard window:", font=('',13))
        self.clipboard_label.pack()

        self.clipboard_inside_frame = tk.Frame(self.clipboard_frame)
        self.clipboard_inside_frame.pack(pady=10)

        self.clipboard_keybind_label = tk.Label(self.clipboard_inside_frame, 
                                                text=" + ".join(self.pyTopManager.clipboard_window_keybinds),
                                                font=('', 12))
        self.clipboard_keybind_label.grid(row=0, column=0, padx=20)

        self.clipboard_keybind_change = tk.Button(self.clipboard_inside_frame, 
                                                  text="Change", 
                                                  command=lambda: self.change_keybinds(self.pyTopManager.clipboard_window_keybinds))
        self.clipboard_keybind_change.grid(row=0, column=1, padx=20)

        # Webpage Window
        self.webpage_frame = tk.Frame(self.root)
        self.webpage_frame.pack(pady=15)

        self.webpage_label = tk.Label(self.webpage_frame, text="Current Key Bind for the Webpage window:", font=('',13))
        self.webpage_label.pack()

        self.webpage_keybind_label = tk.Label(self.webpage_frame, 
                                                text=" + ".join(self.pyTopManager.webpage_window_keybinds),
                                                font=('', 12))
        self.webpage_keybind_label.pack()

        # Command Window
        self.command_frame = tk.Frame(self.root)
        self.command_frame.pack(pady=15)

        self.command_label = tk.Label(self.command_frame, text="Current Key Bind for the Command window:", font=('',13))
        self.command_label.pack()

        self.command_keybind_label = tk.Label(self.command_frame, 
                                                text=" + ".join(self.pyTopManager.command_window_keybinds),
                                                font=('', 12))
        self.command_keybind_label.pack()

        self.root.mainloop()
    
    def change_keybinds(self, keybind_list):
        self.topwindow = tk.Toplevel(self.root)
        self.topwindow.title("Change Keybinds")
        self.topwindow.geometry("300x130")
        self.topwindow.attributes("-topmost", True)
        self.topwindow.attributes("-toolwindow", True)

        self.topwindow_label = tk.Label(self.topwindow, text="Press the combination of\n keys you want to use", font=('', 18))
        self.topwindow_label.pack(pady=10)

        self.topwindow_keybind_label = tk.Label(self.topwindow, text="? + ? + ?", font=('', 20))
        self.topwindow_keybind_label.pack()