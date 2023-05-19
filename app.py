"""
Tkinter app for iRacing Telemetry logger    

Copyright © Kyle Ward 2023
"""
import tkinter as tk
import customtkinter as ctk
from gui.main_screen import MainScreen
from utils.data_bank import DataBank

class iRTLApp(ctk.CTk):
    
    def __init__(self, **kwargs):
        """
        Initialize the app
        """
        super().__init__()
        self.geometry("1280x720")
        self.title("iRacing Telemetry Logger")
        
        # Create data storage object for passing data between screens
        self.data_bank = DataBank()
        
        # Create GUI screens
        self.screens = {}
        self.screens["main"] = MainScreen(root=self, data_bank=self.data_bank)
        self.screens["main"].place(relwidth=1, relheight=1)


# Run app
if __name__ == "__main__":
    app = iRTLApp()
    app.mainloop()