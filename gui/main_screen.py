"""
Main GUI screen for iRacing Telemetry Logger

Copyright © Kyle Ward 2023        
"""
import tkinter as tk
import customtkinter as ctk
from gui import COLORS

class MainScreen(ctk.CTkFrame):
    
    def __init__(self, root, **kwargs):
        """
        Initialize the main screen
        """
        super().__init__(root, **kwargs)
        
        # Create test button
        self.widgets = {
            "buttons": {}
        }
        
        self.font_size = 20
        
        self.widgets["buttons"]["test_button"] = ctk.CTkButton(self, text="Test", command=lambda: print("Test button pressed"), fg_color=COLORS["royal_purple"], font=("Arial", 20), cursor="hand2")
        self.widgets["buttons"]["test_button"].place(relx=0.5, rely=0.5, anchor="center")