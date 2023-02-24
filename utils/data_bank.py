"""
Data storage class for passing data between UI screens and modules
    
    
Copyright © Kyle Ward 2023
"""
from logger import CHANNELS

class DataBank:
    
    def __init__(self, **kwargs):
        """
        Initialize the data bank class
        """
        
        # Initialize internal data dictionary
        self.data = {
            "is_recording": False,
            "channels": {}
        }
        
        # Add channels to data dictionary
        for category in CHANNELS:
            for channel in CHANNELS[category]:
                self.data["channels"][channel] = 0  # 0 = don't log channel data, 1 = log channel data
                
    def enabled_channels(self):
        """
        Return a list of enabled channels
        """
        enabled_channels = []
        for channel in self.data["channels"]:
            if self.data["channels"][channel] == 1:
                enabled_channels.append(channel)
        return enabled_channels