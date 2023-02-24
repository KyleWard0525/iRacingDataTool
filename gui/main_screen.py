"""
Main GUI screen for iRacing Telemetry Logger

Copyright © Kyle Ward 2023        
"""
import tkinter as tk
import customtkinter as ctk
from PIL import Image
from gui import COLORS
from utils.data_bank import DataBank

class MainScreen(ctk.CTkFrame):
    
    def __init__(self, root, data_bank: DataBank, **kwargs):
        """
        Initialize the main screen
        """
        # Initialize frame
        super().__init__(root, **kwargs)
        self.root = root
        
        # Set data bank object
        self.data_bank = data_bank
        
        # Create test button
        self.widgets = {
            "buttons": {},
            "labels": {},
            "images": {},
            "tabs": {}
        }
        
        # Font sizes
        self.btn_font_size = 20 
        self.title_font_size = 35
        
        # Build widgets
        self.build_widgets()
        
    def build_widgets(self):
        """
        Build GUI widgets and add them to the frame
        """
        # Create title label
        self.widgets["labels"]["title"] = ctk.CTkLabel(self, text="iRacing Telemetry Logger", text_color=COLORS["text_white"], font=("Arial", self.title_font_size))
        self.widgets["labels"]["title"].place(relx=0.5, rely=0.05, anchor="center")
        
        
        # Create 'Recording' status image
        self.widgets["images"]["record_status"] = ctk.CTkImage(light_image=Image.open("images/circle.png"), dark_image=Image.open("images/circle.png"), size=(40, 40))
        
        # Create 'Recording' status label
        self.widgets["labels"]["record_status"] = ctk.CTkLabel(self,
                                                               text="Not recording",
                                                               text_color=COLORS["text_white"],
                                                               font=("Arial", self.title_font_size-5)
                                                               )
        self.widgets["labels"]["record_status"].place(relx=0.125, rely=0.05, anchor="center")
        self.widgets["labels"]["record_status_image"] = ctk.CTkLabel(self, text="", image=self.widgets["images"]["record_status"])
        self.widgets["labels"]["record_status_image"].place(relx=0.0295, rely=0.05, anchor="center")
        
        
        # Create tabs
        self.widgets["tabs"] = ctk.CTkTabview(self.root)
        self.widgets["tabs"].add("Home")
        self.widgets["tabs"].add("Channels")
        self.widgets["tabs"].place(relx=0.5, rely=0.55, relwidth=1, relheight=0.9, anchor="center")
        
        # Configure tabs
        self.widgets["tabs"].configure(border_width=0, fg_color="#000000")
        
        # Build buttons
        self.widgets["buttons"]["test_button"] = ctk.CTkButton(self.widgets["tabs"].tab("Home"), 
                                                               text="Test", 
                                                               command=self.toggle_recording, 
                                                               fg_color=COLORS["royal_purple"],
                                                               hover_color=COLORS["btn_hover"],
                                                               font=("Arial", self.btn_font_size),
                                                               cursor="hand2")
        self.widgets["buttons"]["test_button"].place(relx=0.5, rely=0.5, anchor="center")
        
        
    def toggle_recording(self):
        """
        Toggle telemetry recording 
        """
        
        # Check if recording
        if self.data_bank.data["is_recording"]:
            # Stop recording
            self.data_bank.data["is_recording"] = False
            
            # Reconfigure record status label and image
            self.widgets["labels"]["record_status"].configure(text="Not recording")
            self.widgets["images"]["record_status"].configure(light_image=Image.open("images/circle.png"), dark_image=Image.open("images/circle.png"), size=(40, 40))
            self.widgets["labels"]["record_status_image"] = ctk.CTkLabel(self, text="", image=self.widgets["images"]["record_status"])
        else:
            # Start recording
            self.data_bank.data["is_recording"] = True
            
            # Reconfigure record status label and image
            self.widgets["labels"]["record_status"].configure(text="Recording")
            self.widgets["images"]["record_status"].configure(light_image=Image.open("images/recording.png"), dark_image=Image.open("images/recording.png"), size=(40, 40))
            self.widgets["labels"]["record_status_image"] = ctk.CTkLabel(self, text="", image=self.widgets["images"]["record_status"])
        