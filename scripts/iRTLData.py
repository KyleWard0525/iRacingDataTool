"""
Data processor for iRacing telemetry data

Kyle Ward 2023    
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class iRTLDataProcessor:
    """
    Data processor for iRacing telemetry data
    """
    def __init__(self, datafile_path: str):
        """
        Initialize the data processor
        """
        # Check if datafile exists
        if not os.path.exists(datafile_path):
            raise Exception(f"iRTLDataProcessor.__init__(): Datafile '{datafile_path}' not found!")

        # Read datafile
        self.data = pd.read_json(datafile_path)
        
        # Get the number of laps and lap points
        self.n_laps = np.max(self.data["Lap"]["data"])
        self.lap_points = self.__get_lap_points()
    
    def __get_lap_points(self):
        """
        Get the start and end points for each lap
        """
        # Find lap endpoints
        lap_pts = np.zeros(shape=(self.n_laps,2))
        for lap in range(self.n_laps):
            _pts = np.where(self.data["Lap"]["data"] == self.n_laps - lap)[0]
            lap_pts[lap] = [np.min(_pts), np.max(_pts)]
        lap_pts = np.flipud(lap_pts).astype(int)
        
        return lap_pts
    
    def get_lap_data(self, lap: int):
        """
        Get data for a specific lap
        """
        if lap > self.n_laps:
            raise Exception(f"iRTLDataProcessor.get_lap_data(): Lap {lap} does not exist!")
        
        # Get the lap points for the specified lap
        lap_pts = self.lap_points[lap]
        
        lap_data = {}
        for channel in self.data.keys():
            _data = np.array(self.data[channel]["data"][lap_pts[0]:lap_pts[1]])
            
            # Check for errors in the data
            err_idxs = np.where(_data == -99999)[0]
            
            # Loop through the error indices and replace the error values with the previous value
            for err_idx in err_idxs:
                _data[err_idx] = _data[err_idx-1]
            
            # Check if channel unit is a percentage
            if self.data[channel]["unit"] == "%":
                _data *= 100
            
            lap_data[channel] = {
                "desc": self.data[channel]["desc"],
                "unit": self.data[channel]["unit"],
                "data": _data
            }
        
        return lap_data
    
    def get_lap_time(self, lap: int):
        """
        Get the lap time for a specific lap
        """
        if lap > self.n_laps:
            raise Exception(f"iRTLDataProcessor.get_lap_time(): Lap {lap} does not exist!")
        
        # Get the lap points for the specified lap
        lap_pts = self.lap_points[lap-1]
        return self.data["time"]["data"][lap_pts[1]] - self.data["time"]["data"][lap_pts[0]]
    
    def plot_channel_across_lap(self, channel: str, lap: int):
        """
        Plot the specified channel across the specified lap

        Args:
            lap (int): Lap number
            channel (str): Channel name
        """
        # Check that the channel is in the list of selected channels to record
        if not channel in self.data.keys():
            raise Exception(f"iRTLDataProcessor.plot_channel_across_lap(): Channel '{channel}' not found in the data!")
        if lap > self.n_laps:
            raise Exception(f"iRTLDataProcessor.get_lap_time(): Lap {lap} does not exist!")
        
        # Get lap data and extract the channel data
        lap_data = self.get_lap_data(lap)
        x = lap_data["time"]["data"]
        plt.title(f"{channel} (Lap {lap})")
        plt.xlabel("Time (s)")
        plt.ylabel(f"{channel} ({lap_data[channel]['unit']})")
        plt.plot(x, lap_data[channel]["data"], label=channel)
        plt.legend()
        plt.show()