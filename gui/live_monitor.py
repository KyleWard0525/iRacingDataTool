"""
Live channel monitoring tab

Copyright © Kyle Ward 2023    
"""
import os 
import sys
import json
import tkinter as tk
import numpy as np
import customtkinter as ctk
from gui import COLORS
from logger import CHANNELS
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
from logger.iRTLData import iRTLDataProcessor

sys.path.append(os.getcwd())
from utils.data_bank import DataBank

class LiveMonitor(ctk.CTkFrame):
    
    def __init__(self, root, data_bank: DataBank, **kwargs):
        """
        Initialize the tab frame
        """
        # Initialize frame
        super().__init__(root, **kwargs)
        
        # Initialize class vars
        self.root = root
        self.data_bank = data_bank
        self.data = self.data_bank.data["live_telemetry"]
        self.data_processor = None
        self.figure = None
        self._plot = None
        
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
        
        # Build UI widgets
        self.build_widgets()
        
        
    def build_widgets(self):
        """
        Build UI widgets
        """
        
        # Create label for channel selection
        self.widgets["labels"]["channel_select"] = ctk.CTkLabel(self.root,
                                                                text="Select channel to monitor: ",
                                                                text_color=COLORS["text_white"],
                                                                font=("Arial", self.label_font_size)
                                                                )
        self.widgets["labels"]["channel_select"].grid(row=0, column=0, padx=10, pady=10)
        
        # Create combobox for channel selection
        self.widgets["inputs"]["string_vars"]["channel_select"] = tk.StringVar()
        self.widgets["inputs"]["channel_dropdown"] = ctk.CTkComboBox(self.root,
                                                                     values=self.data_bank.enabled_channels(),
                                                                     command=self.update_plot,
                                                                     font=("Arial", self.btn_font_size),
                                                                     state="readonly",
                                                                     variable=self.widgets["inputs"]["string_vars"]["channel_select"]
                                                                    )
        self.widgets["inputs"]["channel_dropdown"].grid(row=0, column=1, padx=10, pady=10)
        
    def update_channels(self):
        """
        Update channels in the channel select dropdown
        """
        self.widgets["inputs"]["channel_dropdown"].configure(values=self.data_bank.enabled_channels())
        
        
    def update_plot(self, val):
        """
        Update plot with new data
        """
        pass