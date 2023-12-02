NEW_API_KEY = "13d18ee6d1d44c5785e2abe453aa44b8"
OLD_API_KEY = "e0cc2da1e8494b57b4ebd6ee0fa45173"

PARAMETERS = [
    "Air_Temperature",
    "ODO",
    "DO",
    "Dissolved_Oxygen",
    "Water_Temeperature",
    "Temperature",
]

COMBINE_MAP = [
    # iCHART, OLD, NEW,
    ["TREC_Tower", "TREC_Tower_iSIC"] # iChart, NEW (AirTemp, Air_Temperature)
    ["Beach2_Tower", "Beach2_Tower_iSIC", "X2-C-VZ4G-01284"], # (Air_Temperature, AirTemp, Air_Temperature)
    ["Beach2_Buoy","Beach2_SDL","X2-CB-C-VZ4G-20213"], # (Temperature, Temp, Temperature) -> Water and (ODO, ODO, ODO)
    ["Beach6_Buoy","X2-SDL-C-VZ4G-31668","X2-CB-C-VZ4G-20229"], # (Temperature, Temp, Temperature) -> Water and (ODO, ODO, ODO)
    ["3100-iSIC", "X2-CB-C-AT4G-20205"] # Old, New (Air_Temperature, Air_Temperature) and (DO, ODO) and (Temperature, Temperature)
    ["Walnut_Creek_iSIC" ,"X2-CB-C-AT4G-20200"] # Old, New (Air_Temperature, Air_Temperature) 
    ["Surface_Data"] # New (Water Temperature and Dissolved_Oxygen)
]