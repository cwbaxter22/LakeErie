from data_transformer import DataTransformer
import pandas as pd
import os 

# # ichart
# dataTransformer = DataTransformer()
# dataTransformer.set_path("../../data/raw/ichart/pivot")
# dataTransformer.set_devices(["Beach2_Tower", "Beach2_Buoy", "Beach6_Buoy", "TREC_Tower"])
# dataTransformer.device_aggregate("ichart")
# dataTransformer.tidy_devices("ichart")
# dataTransformer.device_downsample_hour("ichart")
# dataTransformer.device_downsample_day("ichart")

# old
#dataTransformer = DataTransformer()
#dataTransformer.set_path()
#dataTransformer.set_devices(["3100-iSIC", "Beach2_SDL", "Beach2_Tower_iSIC","Walnut_Creek_iSIC"])
#dataTransformer.across_parameter_aggregate("3100-iSIC", "old")
#dataTransformer.device_aggregate("old")
#dataTransformer.tidy_devices("old")
#dataTransformer.device_downsample_hour("old")
#dataTransformer.device_downsample_day("old")

# new
# dataTransformer = DataTransformer()
# dataTransformer.set_path("../../data/raw/ichart/pivot")
# dataTransformer.set_devices(["Beach2_Tower", "Beach2_Buoy", "Beach6_Buoy", "TREC_Tower"])
# dataTransformer.device_aggregate("ichart")
# dataTransformer.tidy_devices("ichart")
# dataTransformer.device_downsample_hour("ichart")
# dataTransformer.device_downsample_day("ichart")


hourly_df = pd.read_csv(r"../../data/raw/old/3100-iSIC/Air_Temperature.csv")

# ## is this doubled up in another function?
# hourly_df["times"] = pd.to_datetime(hourly_df["times"])
# parameter = hourly_df.columns[1]
# hourly_df.rename(columns={parameter: 'value'}, inplace=True)
# #hourly_df["parameter"] = parameter

# print(hourly_df.head())


        
# #set the times column as the index
# hourly_df.set_index("times", inplace=True)

# #groupby the parameter and units, then resample the data to 1 hour intervals
# print(1)
# #hourly_df = hourly_df.groupby(["parameter", "Units"]).resample("H").agg({"value": ["mean", "std"]})
# #hourly_df = hourly_df.groupby(["Units"]).resample("H").agg({"value": ["mean", "std"]})
# result = hourly_df.resample('H').agg({"value": ["mean", "std"]})
# print(result.head())
# #reset the index
# hourly_df.reset_index(inplace=True)

# #combine multiindex columns into one column
# hourly_df.columns = [col[0] if col[1] == '' else f"{col[0]}_{col[1]}" for col in hourly_df.columns]

# hourly_df["parameter"] = parameter
# print(hourly_df.head())
        
# #save the data to a csv file
# hourly_df.to_csv("../../data/processed/old/3100-iSIC/Air_Temperature_hourly.csv", index = False)