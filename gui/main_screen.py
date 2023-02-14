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
        self.root = root
        
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
        
        # Create tabs
        self.widgets["tabs"] = ctk.CTkTabview(self.root)
        self.widgets["tabs"].add("Home")
        self.widgets["tabs"].add("Channels")
        self.widgets["tabs"].place(relx=0.5, rely=0.55, relwidth=1, relheight=0.9, anchor="center")
        #self.widgets["tabs"].pack(padx=10, pady=70, fill="both", expand=True)
        

        self.widgets["tabs"].configure(border_width=0, fg_color="#000000")

        
        
        # Build buttons
        self.widgets["buttons"]["test_button"] = ctk.CTkButton(self.widgets["tabs"].tab("Home"), 
                                                               text="Test", 
                                                               command=lambda: print("Test button pressed"), 
                                                               fg_color=COLORS["royal_purple"],
                                                               hover_color=COLORS["btn_hover"],
                                                               font=("Arial", self.font_size),
                                                               cursor="hand2")
        self.widgets["buttons"]["test_button"].place(relx=0.5, rely=0.5, anchor="center")