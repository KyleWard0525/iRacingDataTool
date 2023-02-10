"""
Test cases for iRTLData

Kyle Ward 2023    
"""
import os
import sys
import matplotlib.pyplot as plt

plt.style.use("dark_background")

sys.path.append(os.getcwd())
from scripts.iRTLData import iRTLDataProcessor

data_proc = iRTLDataProcessor(f"{os.getcwd()}\\data\\outputs\\iRTL_02-09-2023_21-10-28.json")
lap2_data = data_proc.get_lap_data(2)

print(f"{lap2_data.keys() = }")
print(f"{len(lap2_data['time']['data']) = }")
print(f"Lap 1 time: {data_proc.get_lap_time(3)}s")

# Plot lap 2 throttle position
x = lap2_data["time"]["data"]
plt.title("Throttle Position (Lap 2)")
plt.xlabel("Time (s)")
plt.ylabel("Throttle Position (%)")
plt.plot(x, lap2_data["Throttle"]["data"], label="Throttle %")
plt.show()