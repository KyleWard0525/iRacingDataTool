"""
Initialize logger module

Kyle Ward 2023    
"""
import os
import sys

sys.path.append(os.getcwd())
from utils.data_utils import parse_irsdk_vars

SDK_VARS = parse_irsdk_vars(os.getcwd() + "\\data\\irsdk_vars.txt")

# Data channels
CHANNELS = {
    # category: [channel, channel, ...]
    "environment": {
        "AirDensity": SDK_VARS["AirDensity"],
        "AirPressure": SDK_VARS["AirPressure"],
        "AirTemp": SDK_VARS["AirTemp"],
        "FogLevel": SDK_VARS["FogLevel"],
        "RelativeHumidity": SDK_VARS["RelativeHumidity"],
        "SessionTimeOfDay": SDK_VARS["SessionTimeOfDay"],
        "SessionTimeTotal": SDK_VARS["SessionTimeTotal"],
        "SolarAltitude": SDK_VARS["SolarAltitude"],
        "SolarAzimuth": SDK_VARS["SolarAzimuth"],
        "TrackTempCrew": SDK_VARS["TrackTempCrew"],
        "WindDir": SDK_VARS["WindDir"],
        "WindVel": SDK_VARS["WindVel"]
    },
    
    "powertrain": {
        "Clutch": SDK_VARS["Clutch"],
        "FuelLevel": SDK_VARS["FuelLevel"],
        "FuelLevelPct": SDK_VARS["FuelLevelPct"],
        "FuelPress": SDK_VARS["FuelPress"],
        "FuelUsePerHour": SDK_VARS["FuelUsePerHour"],
        "Gear": SDK_VARS["Gear"],
        "ManifoldPress": SDK_VARS["ManifoldPress"],
        "OilLevel": SDK_VARS["OilLevel"],
        "OilPress": SDK_VARS["OilPress"],
        "OilTemp": SDK_VARS["OilTemp"],
        "RPM": SDK_VARS["RPM"],
        "ShiftGrindRPM": SDK_VARS["ShiftGrindRPM"],
        "ShiftPowerPct": SDK_VARS["ShiftPowerPct"],
        "Throttle": SDK_VARS["Throttle"],
        "Voltage": SDK_VARS["Voltage"],
        "WaterLevel": SDK_VARS["WaterLevel"],
        "WaterTemp": SDK_VARS["WaterTemp"]
    },
    
    "brakes": {
        "Brake": SDK_VARS["Brake"],
        "BrakeABSactive": SDK_VARS["BrakeABSactive"],
        "LFbrakeLinePress": SDK_VARS["LFbrakeLinePress"],
        "LRbrakeLinePress": SDK_VARS["LRbrakeLinePress"],
        "RFbrakeLinePress": SDK_VARS["RFbrakeLinePress"],
        "RRbrakeLinePress": SDK_VARS["RRbrakeLinePress"],
    },
    
    "suspension": {
        "LFshockDefl": SDK_VARS["LFshockDefl"],
        "LFshockVel": SDK_VARS["LFshockVel"],
        "LRshockDefl": SDK_VARS["LRshockDefl"],
        "LRshockVel": SDK_VARS["LRshockVel"],
        "RFshockDefl": SDK_VARS["RFshockDefl"],
        "RFshockVel": SDK_VARS["RFshockVel"],
        "RRshockDefl": SDK_VARS["RRshockDefl"],
        "RRshockVel": SDK_VARS["RRshockVel"],
    },
    
    "steering": {
        "SteeringWheelAngle": SDK_VARS["SteeringWheelAngle"],
        "SteeringWheelPctTorque": SDK_VARS["SteeringWheelPctTorque"],
        "SteeringWheelTorque": SDK_VARS["SteeringWheelTorque"],
    },
    
    "tires": {
        "LFcoldPressure": SDK_VARS["LFcoldPressure"],
        "LFtempCL": SDK_VARS["LFtempCL"],
        "LFtempCM": SDK_VARS["LFtempCM"],
        "LFtempCR": SDK_VARS["LFtempCR"],
        "LFwearL": SDK_VARS["LFwearL"],
        "LFwearM": SDK_VARS["LFwearM"],
        "LFwearR": SDK_VARS["LFwearR"],
        "LRcoldPressure": SDK_VARS["LRcoldPressure"],
        "LRtempCL": SDK_VARS["LRtempCL"],
        "LRtempCM": SDK_VARS["LRtempCM"],
        "LRtempCR": SDK_VARS["LRtempCR"],
        "LRwearL": SDK_VARS["LRwearL"],
        "LRwearM": SDK_VARS["LRwearM"],
        "LRwearR": SDK_VARS["LRwearR"],
        "RFcoldPressure": SDK_VARS["RFcoldPressure"],
        "RFtempCL": SDK_VARS["RFtempCL"],
        "RFtempCM": SDK_VARS["RFtempCM"],
        "RFtempCR": SDK_VARS["RFtempCR"],
        "RFwearL": SDK_VARS["RFwearL"],
        "RFwearM": SDK_VARS["RFwearM"],
        "RFwearR": SDK_VARS["RFwearR"],
        "RRcoldPressure": SDK_VARS["RRcoldPressure"],
        "RRtempCL": SDK_VARS["RRtempCL"],
        "RRtempCM": SDK_VARS["RRtempCM"],
        "RRtempCR": SDK_VARS["RRtempCR"],
        "RRwearL": SDK_VARS["RRwearL"],
        "RRwearM": SDK_VARS["RRwearM"],
        "RRwearR": SDK_VARS["RRwearR"],
    },
    
    "vehicle": {
        "LatAccel": SDK_VARS["LatAccel"],
        "LongAccel": SDK_VARS["LongAccel"],
        "Pitch": SDK_VARS["Pitch"],
        "PitchRate": SDK_VARS["PitchRate"],
        "PlayerCarPosition": SDK_VARS["PlayerCarPosition"],
        "Roll": SDK_VARS["Roll"],
        "RollRate": SDK_VARS["RollRate"],   
        "Speed": SDK_VARS["Speed"],
        "VelocityX": SDK_VARS["VelocityX"],
        "VelocityY": SDK_VARS["VelocityY"],
        "VelocityZ": SDK_VARS["VelocityZ"],
        "VertAccel": SDK_VARS["VertAccel"],
        "Yaw": SDK_VARS["Yaw"],
        "YawNorth": SDK_VARS["YawNorth"],
        "YawRate": SDK_VARS["YawRate"],
    },
    
    "laps": {
        "Lap": SDK_VARS["Lap"],
        "LapBestLap": SDK_VARS["LapBestLap"],
        "LapBestLapTime": SDK_VARS["LapBestLapTime"],
        "LapCurrentLapTime": SDK_VARS["LapCurrentLapTime"],
        "LapDeltaToBestLap": SDK_VARS["LapDeltaToBestLap"],
        "LapDeltaToOptimalLap": SDK_VARS["LapDeltaToOptimalLap"],
        "LapDeltaToSessionBestLap": SDK_VARS["LapDeltaToSessionBestLap"],
        "LapDeltaToSessionLastlLap": SDK_VARS["LapDeltaToSessionLastlLap"],
        "LapDeltaToSessionOptimalLap": SDK_VARS["LapDeltaToSessionOptimalLap"],
        "LapDist": SDK_VARS["LapDist"],
        "LapDistPct": SDK_VARS["LapDistPct"],
        "LapLastLapTime": SDK_VARS["LapLastLapTime"],
        "RaceLaps": SDK_VARS["RaceLaps"],
    }
    
    # TODO: Add session category and hardware stats category
}