import tkinter as tk
import webbrowser


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

        self.github = tk.Button(text="How To Use ?", command=self.howToUse, font=('', 15))
        self.github.pack()

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



class TopManagerPopUp:
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

