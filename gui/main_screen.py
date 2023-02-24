"""
Main GUI screen for iRacing Telemetry Logger

Copyright © Kyle Ward 2023        
"""
import tkinter as tk
import customtkinter as ctk
from PIL import Image
from gui import COLORS
from utils.data_bank import DataBank
from tktooltip import ToolTip
from logger import CHANNELS
from functools import partial
from logger.iRTL import iRacingTelemetryLogger
from tkinter import messagebox

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
        
        # Create telemetry logger object
        self.logger = iRacingTelemetryLogger()
        
        # UI widgets
        self.widgets = {
            "buttons": {},
            "labels": {},
            "images": {},
            "tabs": {},
            "tooltips": {},
            "inputs": {
                "string_vars": {}    
            },
            "frames": {}
        }
        
        self.channel_categories = [category for category in CHANNELS.keys()]
        
        # Font sizes
        self.btn_font_size = 20 
        self.title_font_size = 30
        self.input_label_font_size = 15
        
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
        self.widgets["images"]["record_status"] = ctk.CTkImage(light_image=Image.open("images/circle.png"), dark_image=Image.open("images/circle.png"), size=(35, 35))
        
        # Create 'Recording' status label
        self.widgets["labels"]["record_status"] = ctk.CTkLabel(self,
                                                               text="Not recording",
                                                               text_color=COLORS["text_white"],
                                                               font=("Arial", self.title_font_size-10)
                                                               )
        self.widgets["labels"]["record_status"].place(relx=0.125, rely=0.05, anchor="center")
        self.widgets["labels"]["record_status_image"] = ctk.CTkLabel(self, text="", image=self.widgets["images"]["record_status"])
        self.widgets["labels"]["record_status_image"].place(relx=0.0295, rely=0.05, anchor="center")
        
        
        # Create tabs
        self.create_tabs()
        
        # Create tooltips
        self.create_tooltips()
          
    def create_tabs(self):
        """
        Create tabs for each screen
        """
        # Create tab view and place it in the frame
        self.widgets["tabs"] = ctk.CTkTabview(self.root)
        self.widgets["tabs"].place(relx=0.5, rely=0.55, relwidth=1, relheight=0.9, anchor="center")
        
        # Create tabs
        self.create_home_tab()
        self.create_channels_tab()
    
    def create_home_tab(self):
        """
        Create the home tab
        """
        # Add a frame to the tab view for the home tab
        self.widgets["tabs"].add("Home")
        
        # Build buttons
        self.widgets["buttons"]["btn_toggle_record"] = ctk.CTkButton(self.widgets["tabs"].tab("Home"), 
                                                               text="Toggle Recording", 
                                                               command=self.toggle_recording, 
                                                               fg_color=COLORS["royal_purple"],
                                                               hover_color=COLORS["btn_hover"],
                                                               font=("Arial", self.btn_font_size),
                                                               cursor="hand2")
        self.widgets["buttons"]["btn_toggle_record"].place(relx=0.5, rely=0.5, anchor="center")
    
    def create_channels_tab(self):
        """
        Create the channel selection tab
        """
        # Add a frame to the tab view for the channel selection tab
        self.widgets["tabs"].add("Channels")
        
        # Add screen label
        self.widgets["labels"]["channels_label"] = ctk.CTkLabel(self.widgets["tabs"].tab("Channels"),
                                                                text="Channel Selection",
                                                                text_color=COLORS["text_white"], 
                                                                font=("Arial", self.title_font_size-2)
                                                                )
        self.widgets["labels"]["channels_label"].place(relx=0.5, rely=0.045, anchor="center")
        
        # Add label for category drop-down menu
        self.widgets["labels"]["category_label"] = ctk.CTkLabel(self.widgets["tabs"].tab("Channels"), 
                                                                text="Category:", 
                                                                text_color=COLORS["text_white"], 
                                                                font=("Arial", self.btn_font_size-1)
                                                                )
        self.widgets["labels"]["category_label"].place(relx=0.015, rely=0.05, anchor="w")
        
        # Add drop-down menu for selecting channel category
        self.widgets["inputs"]["category_dropdown"] = ctk.CTkComboBox(self.widgets["tabs"].tab("Channels"),
                                                                      values = self.channel_categories,
                                                                      command=self.update_channel_category,
                                                                      font=("Arial", self.btn_font_size-5),
                                                                      state="readonly",
                                                                      )
        self.widgets["inputs"]["category_dropdown"].place(relx=0.125, rely=0.05, anchor="w")
        
    def update_channel_category(self, value):
        """
        Update the channel tab when the category drop-down menu is changed
        """
        # Create channel selection page for the selected category
        self.update_channel_category_page(value)
        
    def update_channel_category_page(self, category: str):
        """
        Update the current channel selection page for the given category

        Args:
            category (str): ['environment', 'powertrain', 'brakes', 'suspension', 'steering', 'tires', 'vehicle', 'laps']
        """
        # Validate category
        if not category in self.channel_categories:
            raise ValueError(f"MainScreen.create_channel_category_page(): Invalid channel category '{category}'")
        
        # Check if frame for the category already exists
        if not f"channel_page_{category}" in self.widgets["frames"]:
            self.create_channel_category_page(category)
        
        # Hide the current channel selection page and show the new one
        if "channel_page" in self.widgets["frames"]:
            self.widgets["frames"]["channel_page"].place_forget()
        
        # Show the new channel selection page
        self.widgets["frames"]["channel_page"] = self.widgets["frames"][f"channel_page_{category}"]
        self.widgets["frames"]["channel_page"].place(relx=0.5, rely=0.55, anchor="center")
            
    def create_channel_category_page(self, category: str):
        """
        Create a selection page for the channels in a given category
        """ 
        # Validate category
        if not category in self.channel_categories:
            raise ValueError(f"MainScreen.create_channel_category_page(): Invalid channel category '{category}'")

        # Create a scrollable frame for the channel selection page
        if not f"channel_page_{category}" in self.widgets["frames"]:
            self.widgets["frames"][f"channel_page_{category}"] = ctk.CTkScrollableFrame(self.widgets["tabs"].tab("Channels"),
                                                                                width=1260, 
                                                                                height=525,
                                                                                corner_radius=0,
                                                                                orientation="vertical",
                                                                                )
            
        # Loop through channels in the category and create UI elements for each
        for i, channel in enumerate(CHANNELS[category]):
            # Create label for channel name
            self.widgets["labels"][channel] = ctk.CTkLabel(self.widgets["frames"][f"channel_page_{category}"],
                                                                text=f"{channel}: ",
                                                                text_color=COLORS["text_white"],
                                                                font=("Arial", self.input_label_font_size),
                                                                )
            self.widgets["labels"][channel].grid(row=i, column=0, padx=10, pady=10, sticky="w")    
            
            # Create label for channel description
            self.widgets["labels"][f"{channel}_desc"] = ctk.CTkLabel(self.widgets["frames"][f"channel_page_{category}"],
                                                                        text=f"{CHANNELS[category][channel]['desc']}", 
                                                                        text_color=COLORS["text_white"],
                                                                        font=("Arial", self.input_label_font_size)
                                                                    )
            self.widgets["labels"][f"{channel}_desc"].grid(row=i, column=1, padx=10, pady=10, sticky="w")    
            
            # Create label for channel unit
            self.widgets["labels"][f"{channel}_unit"] = ctk.CTkLabel(self.widgets["frames"][f"channel_page_{category}"],
                                                                        text=f"{CHANNELS[category][channel]['unit']}", 
                                                                        text_color=COLORS["text_white"],
                                                                        font=("Arial", self.input_label_font_size)
                                                                    )
            self.widgets["labels"][f"{channel}_unit"].grid(row=i, column=2, padx=10, pady=10, sticky="w")    
                    
            # Check if a string var exists for this channel
            if not channel in self.widgets["inputs"]["string_vars"]:
                self.widgets["inputs"]["string_vars"][channel] = ctk.StringVar()
            
            # Create toggle switch for channel
            callback = partial(self.toggle_channel, channel)
            self.widgets["inputs"][f"log_{channel}"] = ctk.CTkSwitch(self.widgets["frames"][f"channel_page_{category}"],
                                                                    text="",
                                                                    command=callback,
                                                                    variable=self.widgets["inputs"]["string_vars"][channel],
                                                                    onvalue="on",
                                                                    offvalue="off"
                                                                    )
            self.widgets["inputs"][f"log_{channel}"].grid(row=i, column=3, padx=10, pady=10, sticky="e")                                                                                 
        
    def toggle_channel(self, channel: str):
        """
        Toggle channel logging

        Args:
            channel (str): Channel name
        """
        # Check if channel is currently being logged
        if self.widgets["inputs"]["string_vars"][channel].get() == "on":
            # Enable logging channel
            self.data_bank.data["channels"][channel] = True
            
            # Update enabled channels in the logger
            self.logger.channels = self.data_bank.enabled_channels()
        else:
            # Disable logging channel
            self.data_bank.data["channels"][channel] = False
            
            # Update enabled channels in the logger
            self.logger.channels = self.data_bank.enabled_channels()
        
    def create_tooltips(self):
        """
        Create UI tooltips
        """    
        # Add tab tooltips
        pass
        
    def toggle_recording(self):
        """
        Toggle telemetry recording 
        """
        
        # Check if recording
        if self.data_bank.data["is_recording"]:
            # Stop recording
            self.data_bank.data["is_recording"] = False
            self.logger.stop()
            
            # Reconfigure record status label and image
            self.widgets["labels"]["record_status"].configure(text="Not recording")
            self.widgets["images"]["record_status"].configure(light_image=Image.open("images/circle.png"), dark_image=Image.open("images/circle.png"), size=(35, 35))
            self.widgets["labels"]["record_status_image"] = ctk.CTkLabel(self, text="", image=self.widgets["images"]["record_status"])
        else:
            # Start recording
            self.data_bank.data["is_recording"] = True
            
            # Attempt to start the telemetry logger
            if not self.logger.start():
                messagebox.showerror("Error", "ERROR: Failed to connect to the iRacing SDK. Please ensure that the iRacing simulator is running and try again.")
                return
            
            # Reconfigure record status label and image
            self.widgets["labels"]["record_status"].configure(text="Recording")
            self.widgets["images"]["record_status"].configure(light_image=Image.open("images/recording.png"), dark_image=Image.open("images/recording.png"), size=(40, 40))
            self.widgets["labels"]["record_status_image"] = ctk.CTkLabel(self, text="", image=self.widgets["images"]["record_status"])
        