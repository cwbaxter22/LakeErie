"""
The purpose of this file is to run the data_transformer.py file for all devices and projects.
We found that in practice, the files we generated from the "new" and "old" projects (the
data that we downloaded using data_loader.py) were too large to run on our local machines. 
Therefore, we decided to run a downsample function first on the data to try and pair it down.
As it turned out, 2 of the data sets were too large to run on the local machine. Stay tuned 
for the solution we find.

This file will run the data_transformer program for ichart data since all of those files were 
small enough to run on our local machines. 
It will then pairdown the data from the new and old projects and get them into tidy format to 
aggregate with the ichart data. 

Due to the large file size, we will only run this program once in order to generate the processed
data. 
"""

from data_transformer import DataTransformer
import pandas as pd
import os 


# # uncomment this section to run the data_transformer.py file for ichart data
# # ichart
# dataTransformer = DataTransformer()
# dataTransformer.set_path("../../data/raw/ichart/pivot")
# dataTransformer.set_devices(["Beach2_Tower", "Beach2_Buoy", "Beach6_Buoy", "TREC_Tower"])
# dataTransformer.device_aggregate("ichart")
# dataTransformer.tidy_devices("ichart")
# dataTransformer.device_downsample_hour("ichart")
# dataTransformer.device_downsample_day("ichart")




class DataWrangler:
    """
    This class can be used to aggregate and transform data from the user's computer.
    Specifically, it is meant to be used to downsample the data from the new and old projects, 
    as those project files were too large for the data_transformer file. They would crash the 
    computer. 

    The class downsamples the raw data to hourly and daily formats,
    making it much easier to work with. It then tidies the data and saves it to a csv file in
    the processed data directory. 

    
    """
    def __init__(self) -> None:
        # the project names (also built into the file directory system)
        self.project = [ "new", "old"]

    
    def downsample(self) -> None:
        """
        This function

        Arguments:

        variable (type): description
        
        Returns:
        No returns, but writes 2 csv files to the processed directory.
        
        Raises:
        -------
        
        """
        for project in self.project:
            for device in os.listdir(f"../../data/raw/{project}"):
                if device == "TREC_Tower_iSIC":
                    continue
                if device == "Beach2_Tower_iSIC":
                    continue
                for filename in os.listdir(f"../../data/raw/{project}/{device}"):
                    print(device, filename)
                    if filename.endswith(".csv"):
                        df = pd.read_csv(f"../../data/raw/{project}/{device}/{filename}")
                        df["times"] = pd.to_datetime(df["times"])
                        parameter = df.columns[1]
                        df.rename(columns={parameter: 'value'}, inplace=True)
                        df.set_index("times", inplace=True)
                        hourly_df = df.groupby(["Units"]).resample('H').agg({"value": ["mean", "std"]})
                        daily_df = df.groupby(["Units"]).resample('D').agg({"value": ["mean", "std"]})
                        hourly_df.reset_index(inplace=True)
                        daily_df.reset_index(inplace=True)
                        hourly_df.set_index("times", inplace=True)
                        daily_df.set_index("times", inplace=True)
                        hourly_df.reset_index(inplace=True)
                        daily_df.reset_index(inplace=True)
                        hourly_df.columns = [col[0] if col[1] == '' else f"{col[0]}_{col[1]}" for col in hourly_df.columns]
                        daily_df.columns = [col[0] if col[1] == '' else f"{col[0]}_{col[1]}" for col in daily_df.columns]
                        hourly_df["parameter"] = parameter
                        daily_df["parameter"] = parameter
        
                        #save the data to a csv file
                        hourly_df.to_csv(f"../../data/processed/{project}/{device}/hourly_{filename}", index = False)
                        daily_df.to_csv(f"../../data/processed/{project}/{device}/daily_{filename}", index = False)

                self.parser(f"../../data/processed/{project}/{device}")
                    


    def parser(self, directory: str ) -> None:
        df_merged = pd.DataFrame()
        for filename in os.listdir(directory):
            if filename.endswith(".csv"):
                if filename.startswith("hourly"):
                    df = pd.read_csv(f"{directory}/{filename}")
                    df_merged = pd.concat([df_merged, df], ignore_index=True)
        df_merged.to_csv(f"{directory}/tidy_hourly_all_data.csv", index = False)

        df_merged = pd.DataFrame()
        for filename in os.listdir(directory):
            if filename.endswith(".csv"):
                if filename.startswith("daily"):
                    print("location2:", filename)
                    df = pd.read_csv(f"{directory}/{filename}")
                    df_merged = pd.concat([df_merged, df], ignore_index=True)
        df_merged.to_csv(f"{directory}/tidy_daily_all_data.csv", index = False)
        print("tidied the data for ", directory)



datawrangler = DataWrangler()
datawrangler.downsample()