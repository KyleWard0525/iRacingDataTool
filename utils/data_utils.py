"""
Data utilities for iRTL   

Copyright © Kyle Ward 2023
"""
import os
import sys

def parse_irsdk_vars(var_file: str) -> dict:
    """
    Parse the iRacing SDK variables from a text file into a dictionary

    A single var item will include:
        - Name
        - Description
        - Unit

    Args:
        var_file (str): Path to the text file containing the iRacing SDK variables
    """
    sdk_vars = {}
    raw_data = []
    
    # Check if the file exists
    if not os.path.isfile(var_file):
        print(f"\nERROR: File '{var_file}' does not exist\n")
        sys.exit(1)
    
    # Read the var file
    with open(var_file, "r") as f:
        raw_data = [line.strip() for line in f.readlines()]
        
    # Parse raw data
    for line in raw_data:
        _var = {
            "desc": "",
            "unit": ""
        }
        
        # Split by ',' and extract the unit
        name_desc, _var['unit'] = line.split(",")
        _var['unit'] = _var['unit'].strip()
        
        # Split by ' ' and extract the name and description
        nd = [val for val in name_desc.split(" ", 8) if val != ""]
        varname = nd[0]
        _var['desc'] = nd[1].strip()
        
        # Add the var to the list
        sdk_vars[varname] = _var
        
    return sdk_vars