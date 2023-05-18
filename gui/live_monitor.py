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
from threading import Thread

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
        
        # Create plot frame
        self.create_plot_frame()
        
    def create_plot_frame(self):
        """
        Create the UI frame for the plot
        """
        # Create frame
        self.widgets["frames"]["plot_frame"] = ctk.CTkFrame(self.root,
                                                            width=1250,
                                                            height=550,
                                                            )
        self.widgets["frames"]["plot_frame"].place(relx=0.5, rely=0.55, anchor="center")
        
    def update_channels(self):
        """
        Update channels in the channel select dropdown
        """
        self.widgets["inputs"]["channel_dropdown"].configure(values=self.data_bank.enabled_channels())
        
    def update_plot(self, val):
        """
        Update plot with new data
        """
        pass #self.plot()
            
    def plot(self):
        """
        Update plot with new data
        """
        # Get the name of the selected channel
        channel_name = self.widgets["inputs"]["string_vars"]["channel_select"].get()
        
        if channel_name != "":
            # Check if the figure has been created
            if not self.figure:
                self.figure = Figure(figsize=(15, 7), dpi=100)

            # Get the channel data from the data bank
            x_axis = self.data_bank.data["live_telemetry"]["time"]["data"]
            y_axis = self.data_bank.data["live_telemetry"][channel_name]["data"]      
            
            # Check if the x and y axis are the same length 
            if len(x_axis) > len(y_axis):
                for _ in range(len(x_axis) - len(y_axis)):
                    y_axis.append(0.0)
            
            if not self._plot:
                # Create plot
                self._plot = self.figure.add_subplot(111)
                self._plot.plot(x_axis, y_axis)
                self._plot.set_xlabel(f"time ({self.data_bank.data['live_telemetry']['time']['unit']})")                    # Set x-axis label
                self._plot.set_ylabel(f"{channel_name} ({self.data_bank.data['live_telemetry'][channel_name]['unit']})")    # Set y-axis label
                
                # Create canvas
                self.canvas = FigureCanvasTkAgg(self.figure, master=self.widgets["frames"]["plot_frame"])
                self.canvas.draw()
                self.canvas.get_tk_widget().pack()
            else:
                self._plot.clear()
                self._plot.plot(x_axis, y_axis)
                self._plot.set_ylabel(f"{channel_name} ({self.data_bank.data['live_telemetry'][channel_name]['unit']})")    # Set y-axis label
                self.canvas.draw()