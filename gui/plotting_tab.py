"""
UI page for the plotting tab

Copyright © Kyle Ward 2023    
"""
import os 
import sys
import json
import tkinter as tk
import customtkinter as ctk
from gui import COLORS
from logger import CHANNELS
from tkinter import messagebox
from tkinter import filedialog as fd

sys.path.append(os.getcwd())
from utils.data_bank import DataBank

class PlottingTab(ctk.CTkFrame):
    
    def __init__(self, root, data_bank: DataBank, **kwargs):
        """
        Initialize the plotting tab frame
        """
        # Initialize frame
        super().__init__(root, **kwargs)
        
        # Initialize class vars
        self.root = root
        self.data_bank = data_bank
        self.data = None
        
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
        
        # Font sizes
        self.btn_font_size = 15
        self.label_font_size = 20
        
        self.build_widgets()
        
    def build_widgets(self):
        """
        Build UI widgets
        """
        
        # File select button
        self.widgets["buttons"]["file_select"] = ctk.CTkButton(self.root, text="Select Telemetry File", command=self.select_file, font=("Arial", self.btn_font_size))
        self.widgets["buttons"]["file_select"].grid(row=0, column=0, padx=10, pady=10)
    
        # Channel select button
        
    
    def __validate_telemetry_data(self, data):
        # Check that the file contains at least one of the telemetry channels
        channel_found = False
        for category in CHANNELS:
            for channel in CHANNELS[category]:
                if channel in data:
                    channel_found = True
                    break
                
            # Check if channel was found
            if channel_found:
                break
            
        # Display an error message if no channels were found
        if not channel_found:
            messagebox.showerror("Telemetry File Error", "The selected file does not contain any telemetry data.")
            return False
        
        return True
    
    def select_file(self):
        """
        Select a telemetry file to plot
        """
        
        # Prompt user to select a telemetry file
        filename = fd.askopenfilename(title="Select Telemetry File", filetypes=[("JSON", "*.json")], initialdir=os.getcwd() + "\\data\\outputs")
        
        if not filename:
            return
        
        # Read the file
        with open(filename, "r") as file:
            data = json.load(file)
        
        # Validate the data
        if not self.__validate_telemetry_data(data):
            return
        
        # Extract just the telemetry data
        self.data = {}
        for category in CHANNELS:
            for channel in CHANNELS[category]:
                if channel in data:
                    self.data[channel] = data[channel]
        
        # Remove path from filename
        filename = filename.split("/")[-1]
        
        # Check if telemetry file label exists
        if not "telemetry_file" in self.widgets["labels"]:
            # Create telemetry file label
            self.widgets["labels"]["telemetry_file"] = ctk.CTkLabel(self.root, text=f"{filename}", text_color=COLORS["text_white"],font=("Arial", self.label_font_size))
            self.widgets["labels"]["telemetry_file"].grid(row=0, column=1, padx=10, pady=10)
            
            # TODO: Create other widgets
            
            # Channel select label
            self.widgets["labels"]["channel_select"] = ctk.CTkLabel(self.root, text="Channel: ", text_color=COLORS["text_white"],font=("Arial", self.label_font_size))
            self.widgets["labels"]["channel_select"].place(relx=0.45, rely=0.04, anchor="center")
            
            # Channel select dropdown
            channel_names = [channel_name for channel_name in self.data.keys()]
            self.widgets["inputs"]["string_vars"]["selected_channels"] = tk.StringVar(self.root)
            self.widgets["inputs"]["channel_dropdown"] = ctk.CTkComboBox (
                                                            self.root,
                                                            values=channel_names,
                                                            command=self.update_channel_selection,
                                                            font=("Arial", self.btn_font_size),
                                                            state="readonly",
                                                        )  
            self.widgets["inputs"]["channel_dropdown"].place(relx=0.55, rely=0.04, anchor="center")
            
            # Create plot frame
            self.create_plot_frame()
            
        else:
            self.widgets["labels"]["telemetry_file"].config(text=f"{filename}")
    
    def update_channel_selection(self, value):
        """
        Update the current channel selection, including plot and settings
        """
        print(f"\nIn PlottingTab.update_channel_selection(): channel = {value}")
        
    
    def create_plot_frame(self):
        """
        Create the plot frame
        """
        self.widgets["frames"]["plot_frame"] = ctk.CTkFrame(self.root,
                                                            width=1100,
                                                            height=550,
                                                            )
        self.widgets["frames"]["plot_frame"].place(relx=0.445, rely=0.545, anchor="center")
        

        
        
        