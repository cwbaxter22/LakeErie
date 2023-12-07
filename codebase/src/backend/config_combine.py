PARAMETERS = [
    "Air_Temperature",
    "ODO",
    "DO",
    "Dissolved_Oxygen",
    "Water_Temeperature",
    "Temperature",
]


# iCHART, OLD, NEW,
COMBINE_MAP = {
   "Trec_Tower": ["TREC_Tower", None, "TREC_Tower_iSIC"], # iChart, NEW (AirTemp, Air_Temperature)
   "Beach2_Tower": ["Beach2_Tower", "Beach2_Tower_iSIC", "X2-C-VZ4G-01284"], # (Air_Temperature, AirTemp, Air_Temperature)
   "Beach2_Buoy": ["Beach2_Buoy","Beach2_SDL","X2-CB-C-VZ4G-20213"], # (Temperature, Temp, Temperature) -> Water and (ODO, ODO, ODO)
   "Beach6_Buoy": ["Beach6_Buoy", None,"X2-CB-C-VZ4G-20229"], # (Temperature, Temp, Temperature) -> Water and (ODO, ODO, ODO)
   "Location": [None, "3100-iSIC", "X2-CB-C-AT4G-20205"], # Old, New (Air_Temperature, Air_Temperature) and (DO, ODO) and (Temperature, Temperature)
   "Walnut_Creek": [None, "Walnut_Creek_iSIC" ,"X2-CB-C-AT4G-20200"], # Old, New (Air_Temperature, Air_Temperature)
   "Surface_Data": [None, None, "Surface_Data"], # New (Water Temperature and Dissolved_Oxygen)
}