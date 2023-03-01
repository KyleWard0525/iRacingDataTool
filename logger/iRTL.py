"""
iRacing Telemetry Logger

Copyright © Kyle Ward 2023
"""
import os
import sys
import json
import time
import irsdk    # iRacing SDK
import pandas as pd
from datetime import datetime
from threading import Thread

sys.path.append(os.getcwd())
from utils.data_utils import parse_irsdk_vars
from utils.data_bank import DataBank
from gui.live_monitor import LiveMonitor

class iRacingTelemetryLogger:
    
    def __init__(self, data_bank: DataBank, **kwargs):
        """
        Initialize the logger
        """
        self.ir_sdk = irsdk.IRSDK()
        self.data_dir = os.getcwd() + "\\data"
        self.sdk_vars = parse_irsdk_vars(self.data_dir + "\\irsdk_vars.txt")
        self.output_dir = self.data_dir + "\\outputs"
        self.recording = False
        self.polling_rate_hz = 60
        self.polling_rate = 1.0 / self.polling_rate_hz    # Polling rate in seconds; 
        self.data_precison = 3      # Number of decimal places to round data to
        self.data_err_code = 0  # Error code for failed data retrieval from sim
        self.data_bank = data_bank
        self.live_monitor = None
        
        # Create dictionary to store telemetry data
        self.data = {
            # channel_name: {"desc": str, "unit": str, "data": []}
            "time": {"desc": "Session time", "unit": "s", "data": []}
        }
        
        default_channels = ["Lap", "LapDist", "Alt", "Lat", "Lon"]
        
        # Check if list of channels to record is provided
        self.channels = []
        if "channels" in kwargs:
            _channels = kwargs["channels"]
            
            # Validate channels
            self.channels = [channel for channel in _channels if self.channel_exists(channel)]
            
            # Ensure 'Lap' is in the list of channels 
            for def_channel in default_channels:
                if not def_channel in self.channels:
                    self.channels.append(def_channel)
        else:
            # Create default list of channels to record
            self.channels = default_channels
            
        # Update channels in the databank
        for channel in self.channels:
            self.data_bank.data["channels"][channel] = 1
            
        # Loop through channels to add and extract channel data from sdk vars
        for channel in self.channels:
            # Read variable data from the sdk vars
            _var = self.sdk_vars[channel]
            
            # Check if channel is in the session data
            if not channel in self.data:
                self.data[channel] = {
                    "desc": _var["desc"],
                    "unit": _var["unit"],
                    "data": []
                }
    
    def channel_exists(self, channel: str) -> bool:
        """
        Check if a channel exists in the session data
        """
        for var in self.sdk_vars:
            if var["name"] == channel:
                return True
            
        return False
    
    def update_channels(self):
        """
        Update the list of channels to record
        """
        # Loop through channels to add and extract channel data from sdk vars
        for channel in self.channels:
            # Read variable data from the sdk vars
            _var = self.sdk_vars[channel]
            
            # Check if channel is in the session data
            if not channel in self.data:
                self.data[channel] = {
                    "desc": _var["desc"],
                    "unit": _var["unit"],
                    "data": []
                }
    
    def start(self, live_monitor: LiveMonitor):
        """
        Start the telemetry logger
        """
        if not self.live_monitor:
            self.live_monitor = live_monitor
        
        # Attempt to connect to iRacing
        sdk_ready = self.ir_sdk.startup()
        
        if not sdk_ready:
            print("\nERROR: Failed to connect to the iRacing SDK. Please ensure that the iRacing simulator is running\n")
            return False
        
        # Update channels in data dictionary
        self.update_channels()
        
        # Start the telemetry logger
        self.recording = True
        self.telemetry_thread = Thread(target=self.run) 
        self.telemetry_thread.start()
        return True
             
    def __filename(self):
        """
        Generate an output filename for the telemetry data
        """
        base_name = "iRTL"
        filetype = ".json"
        
        # Format the current date and time and append to the base name
        strftime = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
        return f"{base_name}_{strftime}{filetype}"
        
    def stop(self):
        """
        Stop the telemetry logger
        """
        self.recording = False
        filename = self.__filename()
        
        for channel_name, channel in self.data.items():
            self.data[channel_name]["data"] = [round(val, self.data_precison) for val in channel["data"]]
        
        # Save data to file
        with open(self.output_dir + "\\" + filename, "w") as f:
            json.dump(self.data, f)

        # Check if file saved successfully
        output_path = self.output_dir + "\\" + filename
        if os.path.exists(output_path):
            print(f"Telemetry data saved to {output_path}")
            return True
        else:
            return False
    
    def poll(self):
        """
        Poll the iRacing SDK for telemetry data. Only poll the selected channels in self.channels and self.data
        """
        # Loop through channels and poll data from the sim
        for channel_name, channel in self.data.items():
            if channel_name == "time":
                continue
            
            # Attempt to poll the channel data from the sim
            _data = self.ir_sdk[channel_name]
            if _data:
                channel["data"].append(_data)
            else:
                channel["data"].append(self.data_err_code)  # Failed to retrieve data from sim
                
        # Add session time to the data
        if len(self.data["time"]["data"]) > 1:
            self.data["time"]["data"].append(self.data["time"]["data"][-1] + self.polling_rate)
        else:
            self.data["time"]["data"].append(0.0)    # First data point is 0.0
            
        # Update the data bank with the latest data
        self.data_bank.data["live_telemetry"] = self.data
        self.live_monitor.plot()
    
    def run(self):
        """
        Run the telemetry logger
        """
        while self.recording:
            self.poll()