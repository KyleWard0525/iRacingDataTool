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
            "buttons": {},
            "labels": {},
            "tabs": {}
        }
        
        # Default font size
        self.font_size = 20 
        
        # Build widgets
        self.build_widgets()
        
    def build_widgets(self):
        """
        Build GUI widgets and add them to the frame
        """
        # Create title label
        self.widgets["labels"]["title"] = ctk.CTkLabel(self, text="iRacing Telemetry Logger", text_color=COLORS["text_white"], font=("Arial", self.font_size+15))
        self.widgets["labels"]["title"].place(relx=0.5, rely=0.05, anchor="center")
        
        # Build buttons
        self.widgets["buttons"]["test_button"] = ctk.CTkButton(self, 
                                                               text="Test", 
                                                               command=lambda: print("Test button pressed"), 
                                                               fg_color=COLORS["royal_purple"],
                                                               hover_color=COLORS["btn_hover"],
                                                               font=("Arial", self.font_size),
                                                               cursor="hand2")
        self.widgets["buttons"]["test_button"].place(relx=0.5, rely=0.5, anchor="center")