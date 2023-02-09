"""
iRacing Telemetry Logger

Copyright © Kyle Ward 2023
"""
import os
import json
import irsdk    # iRacing SDK
from data_utils import parse_irsdk_vars

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
        
        # Create dictionary to store telemetry data
        self.data = {
            "session": {
                # channel_name: {"desc": str, "unit": str, "data": []}
            }
        }
        
        # Create list of channels to record
        self.channels = ["RPM", "Speed", "LatAccel", "LongAccel", "VertAccel", "Throttle", "Pitch", "Yaw", "Roll"]
        
        # Loop through channels to add and extract channel data from sdk vars
        for channel in self.channels:
            # Read variable data from the sdk vars
            _var = self.sdk_vars[channel]
            
            # Check if channel is in the session data
            if not channel in self.data["session"]:
                self.data["session"][channel] = {
                    "desc": _var["desc"],
                    "unit": _var["unit"],
                    "data": []
                }
        