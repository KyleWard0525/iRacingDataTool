"""
GUI module for iRacing Telemetry Logger

Copyright © Kyle Ward 2023    
"""
import matplotlib.pyplot as plt
import customtkinter as ctk

# Set plt to use dark mode
plt.style.use("dark_background")

ctk.set_appearance_mode("dark") # Dark mode
ctk.set_default_color_theme("dark-blue") # Dark blue theme

COLORS = {
    "royal_purple": "#570091",
    "btn_hover": "#3c0063",
    "text_white": "#e3e3e3"
}

