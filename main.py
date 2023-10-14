from ManagerWindow import ManagerWindow
from PyTopManager import PyTopManager
import threading


def managerWindow(pyTopManager):
    ManagerWindow(pyTopManager)

if __name__ == "__main__":
    # Creates a PyTopManager object 
    manager = PyTopManager(True)

    # Creates and activates managerWindow thread 
    t1 = threading.Thread(target=managerWindow, args=(manager,))
    t1.start()

    # Activates the PyTopManager object
    manager.activate()
