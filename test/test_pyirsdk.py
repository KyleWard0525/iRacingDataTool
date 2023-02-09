"""
Test cases for learning how to use pyirsdk    
"""
import os
import irsdk

def main():
    ir_sdk = irsdk.IRSDK()
    sdk_ready = ir_sdk.startup()
    
    if sdk_ready:
        print(f"\nConnected to iRacing SDK")
        
        # Attempt to read oil temperature
        if ir_sdk["OilTemp"]:
            print(f"\nCurrent oil temperature: {ir_sdk['OilTemp']} C")
        if ir_sdk["TrackTemp"]:
            print(f"\nCurrent track temperature: {ir_sdk['TrackTemp']} C")
    else:
        print(f"\nERROR: Failed to connect to iRacing SDK. Please make sure iRacing is running.")
        exit(1)
    



if __name__ == "__main__":
    main()