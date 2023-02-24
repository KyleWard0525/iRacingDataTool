"""
Test cases for plotting telemetry data    
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

telem_file = os.getcwd() + "\\data\\outputs\\iRTL_02-09-2023_21-10-28.json"
data = pd.read_json(telem_file)

# Find number of laps
n_laps = np.max(data["Lap"]["data"])

# Find lap endpoints
lap_pts = np.zeros(shape=(n_laps,2))
for lap in range(n_laps):
    _pts = np.where(data["Lap"]["data"] == n_laps - lap)[0]
    lap_pts[lap] = [np.min(_pts), np.max(_pts)]
lap_pts = np.flipud(lap_pts).astype(int)

print(f"\n{data.keys() = }")
print(f"{n_laps = }")
print(f"{lap_pts = }")

lap1_pts = lap_pts[0]

print(f"{lap1_pts = }")
x = data["time"]["data"][lap1_pts[0]:lap1_pts[1]]

print(f"{x = }")
breakpoint()

# Plot RPM vs. time for lap 1
plt.title("RPM (Lap 1)")
plt.plot(data["time"]["data"][lap1_pts[0]:lap1_pts[1]], data["RPM"]["data"][lap1_pts[0]:lap1_pts[1]], label="RPM")
plt.xlabel("Time (s)")
plt.ylabel("RPM")
plt.show()