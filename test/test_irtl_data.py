"""
Test cases for iRTLData

Kyle Ward 2023    
"""
import os
import sys
import matplotlib.pyplot as plt

plt.style.use("dark_background")

sys.path.append(os.getcwd())
from logger.iRTLData import iRTLDataProcessor

data_proc = iRTLDataProcessor(f"{os.getcwd()}\\data\\outputs\\iRTL_02-09-2023_21-10-28.json")

# Plot lap 2 throttle position
data_proc.plot_channel_across_stint("VertAccel")