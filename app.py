"""
Tkinter app for iRacing Telemetry logger    
"""
import tkinter as tk
import customtkinter as ctk
from gui.main_screen import MainScreen

class iRTLApp(ctk.CTk):
    
    def __init__(self, **kwargs):
        """
        Initialize the app
        """
        super().__init__()
        self.geometry("1280x720")
        self.title("iRacing Telemetry Logger")
        
        self.screens = {}
        self.screens["main"] = MainScreen(root=self)
        self.screens["main"].place(relwidth=1, relheight=1)


# Run app
if __name__ == "__main__":
    app = iRTLApp()
    app.mainloop()