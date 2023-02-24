"""
Data storage class for passing data between UI screens and modules
    
    
Copyright © Kyle Ward 2023
"""


class DataBank:
    
    def __init__(self, **kwargs):
        """
        Initialize the data bank class
        """
        
        # Initialize internal data dictionary
        self.data = {
            "is_recording": False,
        }