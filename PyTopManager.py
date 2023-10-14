
class PyTopManager:
    """Class that will manage different functions of the desktop"""
    def __init__(self, is_working):
        self.is_working = is_working
    
    def activate(self):
        """Do something while is_working"""
        while self.is_working:
            pass