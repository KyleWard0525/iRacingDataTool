"""
Test cases for plotting telemetry data    
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog as fd

telem_file = fd.askopenfilename(title="Select Telemetry File", filetypes=[("JSON", "*.json")], initialdir=os.getcwd() + "\\data\\outputs")
data = pd.read_json(telem_file)

print(f"{data.info() = }")


def plot_channel(data: pd.DataFrame, channel: str):
    
    # Find number of laps
    n_laps = np.max(data["Lap"]["data"])

    # Find lap endpoints
    lap_pts = np.zeros(shape=(n_laps,2))
    for lap in range(n_laps):
        _pts = np.where(data["Lap"]["data"] == n_laps - lap)[0]
        lap_pts[lap] = [np.min(_pts), np.max(_pts)]
    lap_pts = np.flipud(lap_pts).astype(int)
    
    start_pt = lap_pts[0][0]
    end_pt = lap_pts[-1][-1]
    
    print(f"{start_pt = } {end_pt = }")

    # Create x axis
    x = data["time"]["data"][start_pt:end_pt]
    
    # Create y axis
    y = data[channel]["data"][start_pt:end_pt]
    
    plt.xlabel("Time (s)")
    plt.ylabel(f"{channel} ({data[channel]['unit']})")
    plt.plot(x, y, label=channel)
    plt.legend()
    plt.show()

plot_channel(data, "Speed")
# lap1_pts = lap_pts[0]

# print(f"{lap1_pts = }")
# x = data["time"]["data"][lap1_pts[0]:lap1_pts[1]]

# print(f"{x = }")
# breakpoint()

# # Plot RPM vs. time for lap 1
# plt.title("RPM (Lap 1)")
# plt.plot(data["time"]["data"][lap1_pts[0]:lap1_pts[1]], data["RPM"]["data"][lap1_pts[0]:lap1_pts[1]], label="RPM")
# plt.xlabel("Time (s)")
# plt.ylabel("RPM")
# plt.show()