"""
Main driver for the iRacing Telemetry Logger    
"""
from scripts.iRTL import iRacingTelemetryLogger

def init_message():
    print("=========================================")
    print("iRacing Telemetry Logger")
    print("Kyle Ward 2023")
    print("\nPress 's' to start recording and 'q' to stop recording (quit)")
    print("=========================================\n")

def main():
    init_message()
    irtl = iRacingTelemetryLogger()
    
    while True:
        # Check if telemetry logger is recording
        if not irtl.recording:       
            op = input("Start recording ('s'): ")
            
            if op == "s":
                irtl.start()
        else:
            op = input("Stop recording ('q'): ")
            
            if op == "q":
                irtl.stop()
            


if __name__ == "__main__":
    main()