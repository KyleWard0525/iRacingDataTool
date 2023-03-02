"""
Data processor for iRacing telemetry data

Kyle Ward 2023    
"""
import os
import json
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
        with open(datafile_path, "r") as f:
            self.data = json.load(f)
            
        if self.data["Lap"]["data"][0] > 0:
            start_lap = self.data["Lap"]["data"][0]
            for i, point in enumerate(self.data["Lap"]["data"]):
                self.data["Lap"]["data"][i] = point - start_lap + 1
        
        # Get the number of laps and lap points
        self.n_laps = np.max(self.data["Lap"]["data"])
        self.lap_points = self.__get_lap_points()
    
    def __get_lap_points(self):
        """
        Get the start and end points for each lap
        """
        # Find lap endpoints
        min_lap = self.data["Lap"]["data"][0]
        max_lap = self.data["Lap"]["data"][-1]
        
        lap_pts = np.zeros(shape=(self.n_laps,2))
        for lap in range(self.n_laps):
            _pts = np.where(self.data["Lap"]["data"] == self.n_laps - lap)[0]
            lap_pts[lap] = [np.min(_pts), np.max(_pts)]
        lap_pts = np.flipud(lap_pts).astype(int)
        
        return lap_pts
    
    def get_lap_points(self, lap: int):
        """
        Get the start and endpoints for the given lap
        """
        return self.lap_points[lap-1]
    
    def get_channel_data_for_lap(self, channel: str, lap: int):
        """
        Get channel data for the specified lap

        Args:
            channel (str): channel name
            lap (int): lap number
        """
        if not channel in self.data.keys():
            return None
        
        lap_pts = self.get_lap_points(lap)
        return self.data[channel]["data"][lap_pts[0]:lap_pts[1]]
    
    def get_channel_data(self, channel: str):
        """
        Get channel data for the entire session
        """
        if not channel in self.data.keys():
            return None
        return self.data[channel]["data"]
    
    def get_lap_data(self, lap: int):
        """
        Get data for a specific lap
        """
        if lap > self.n_laps:
            raise Exception(f"iRTLDataProcessor.get_lap_data(): Lap {lap} does not exist!")
        
        # Get the lap points for the specified lap
        lap_pts = self.lap_points[lap-1]
        
        lap_data = {}
        for channel in self.data.keys():
            _data = np.array(self.data[channel]["data"][lap_pts[0]:lap_pts[1]])
            
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
    
    def plot_channel_across_stint(self, channel: str):
        """
        Plot the specified channel across the entire stint

        Args:
            channel (str): Channel name
        """
        # Check that the channel is in the list of selected channels to record
        if not channel in self.data.keys():
            raise Exception(f"iRTLDataProcessor.plot_channel_across_lap(): Channel '{channel}' not found in the data!")

        time_data = []
        channel_data = []
        unit = ""
        
        # Iterate through each lap
        for lap in range(self.n_laps):
            # Append the lap time to the time data
            lap_data = self.get_lap_data(lap+1)
            channel_data = np.concatenate((channel_data, lap_data[channel]["data"]))
            time_data = np.concatenate((time_data, lap_data["time"]["data"]))
            
            if unit == "":
                unit = lap_data[channel]["unit"]
                
        # Plot the data
        plt.title(f"{channel} (Laps 1-{self.n_laps})")
        plt.xlabel("Time (s)")
        plt.ylabel(f"{channel} ({unit})")
        plt.plot(time_data, channel_data, label=channel)
        plt.legend()
        plt.show()
        
        