"""
iRacing Telemetry Logger

Copyright © Kyle Ward 2023
"""
import os
import sys
import json
import time
import irsdk    # iRacing SDK
from datetime import datetime
from threading import Thread

sys.path.append(os.getcwd())
from scripts.data_utils import parse_irsdk_vars

class iRacingTelemetryLogger:
    
    def __init__(self):
        """
        Initialize the logger
        """
        self.ir_sdk = irsdk.IRSDK()
        self.data_dir = os.getcwd() + "\\data"
        self.sdk_vars = parse_irsdk_vars(self.data_dir + "\\irsdk_vars.txt")
        self.output_dir = self.data_dir + "\\outputs"
        self.recording = False
        self.polling_rate = 0.01    # Polling rate in seconds; 0.01 = 100Hz
        
        # Create dictionary to store telemetry data
        self.data = {
            # channel_name: {"desc": str, "unit": str, "data": []}
        }
        
        # Create list of channels to record
        self.channels = ["RPM", "Speed", "LatAccel", "LongAccel", "VertAccel", "Throttle", "Pitch", "Yaw", "Roll"]
        
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
        
    def start(self):
        """
        Start the telemetry logger
        """
        # Attempt to connect to iRacing
        sdk_ready = self.ir_sdk.startup()
        
        if not sdk_ready:
            print("\nERROR: Failed to connect to the iRacing SDK. Please ensure that the iRacing simulator is running\n")
            return False
         
        self.recording = True
        self.telemetry_thread = Thread(target=self.run) 
        self.telemetry_thread.start()
        
        
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
        # Save data to file
        with open(self.output_dir + "\\" + filename, "w") as f:
            json.dump(self.data, f)

        # Check if file saved successfully
        output_path = self.output_dir + "\\" + filename
        if os.path.exists(output_path):
            print(f"\nTelemetry data saved to {output_path}\n")
            return True
        else:
            return False
    
    def poll(self):
        """
        Poll the iRacing SDK for telemetry data. Only poll the selected channels in self.channels and self.data
        """
        # Loop through channels and poll data from the sim
        for channel_name, channel in self.data.items():
            # Attempt to poll the channel data from the sim
            _data = self.ir_sdk[channel_name]
            if _data:
                channel["data"].append(_data)
            else:
                channel["data"].append(-99999)  # Failed to retrieve data from sim, set to -99999
                
    def run(self):
        """
        Run the telemetry logger
        """
        print("\nRecording telemetry data...\n")
        
        while self.recording:
            self.poll()
            time.sleep(self.polling_rate)