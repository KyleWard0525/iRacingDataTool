"""
GUI module for iRacing Telemetry Logger

Copyright © Kyle Ward 2023    
"""
import datetime as dt
import matplotlib.pyplot as plt
import customtkinter as ctk

# Set plt to use dark mode
plt.style.use("dark_background")

ctk.set_appearance_mode("dark") # Dark mode
ctk.set_default_color_theme("dark-blue") # Dark blue theme

COLORS = {
    "royal_purple": "#570091",
    "btn_hover": "#032687",
    "text_white": "#e3e3e3",
    "text_red": "#d10d1d",
    "text_blue": "#132fba"
}

# App metadata
APP_NAME = "iRacing Telemetry Logger"
MAJOR_VERSION = 0
MINOR_VERSION = 0
PATCH_VERSION = 1
BUILD_VERSION = 0
BUILD_TYPE = "b" # a = alpha build, b = beta build, d = development/debug, pre = pre-release build, r = release build
VERSION = f"v{MAJOR_VERSION}.{MINOR_VERSION}.{PATCH_VERSION}.{BUILD_VERSION}{BUILD_TYPE}"



APP_METADATA = {
    "name": APP_NAME,   
    "version": VERSION,
    "author": "Kyle Ward",
    "copyright": f"Copyright © Kyle Ward {dt.date.today().year}",
}
