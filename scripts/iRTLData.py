"""
Data processor for iRacing telemetry data

Kyle Ward 2023    
"""
import os
import numpy as np
import pandas as pd

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
            lap_data[channel] = {
                "desc": self.data[channel]["desc"],
                "unit": self.data[channel]["unit"],
                "data": self.data[channel]["data"][lap_pts[0]:lap_pts[1]]
            }
        
        return lap_data
    
    def get_lap_time(self, lap: int):
        """
        Get the lap time for a specific lap
        """
        if lap > self.n_laps:
            raise Exception(f"iRTLDataProcessor.get_lap_time(): Lap {lap} does not exist!")
        
        # Get the lap points for the specified lap
        lap_pts = self.lap_points[lap]
        return self.data["time"]["data"][lap_pts[1]] - self.data["time"]["data"][lap_pts[0]]