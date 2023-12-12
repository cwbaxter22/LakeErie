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
import os
import importlib
import pathlib

import pandas as pd

codebase_path = pathlib.Path(__file__).parents[2]
#https://stackoverflow.com/questions/65206129/importlib-not-utilising-recognising-path
spec = importlib.util.spec_from_file_location(
    name='data_transformer_mod',  # name is not related to the file, it's the module name!
    location= str(codebase_path) +
    "//src//backend//data_transformer.py"  # full path to the script
    )

data_transformer_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(data_transformer_mod)

#from data_transformer import DataTransformer


# uncomment this section to run the data_transformer.py file for ichart data
# ichart
dataTransformer = data_transformer_mod.DataTransformer()
dataTransformer.set_path("../../data/raw/ichart/pivot")
dataTransformer.set_devices(["Beach2_Tower", "Beach2_Buoy", "Beach6_Buoy", "TREC_Tower"])
dataTransformer.device_aggregate("ichart")
dataTransformer.tidy_devices("ichart")
dataTransformer.device_downsample_hour("ichart")
dataTransformer.device_downsample_day("ichart")




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
        This function downsamples the data and puts it into tidy form. 
        A seperate class and function had to be created because the data files
        were too large to run data_transformer.py. This way, we downsample the 
        data first, and then put it into tidy format before running data_combiner. 

        Arguments:
        None. This function will run through the raw data in the new and old projects
        
        Returns:
        No returns, but writes 2 downsampled files to the processed directory for
        every project and device combination.
        
        Raises:
        -------
        
        """
        # iterates through the old and new project directories.
        for project in self.project:
            for device in os.listdir(f"../../data/raw/{project}"):
                for filename in os.listdir(f"../../data/raw/{project}/{device}"):
                    print("Downsampling: ", device, filename)
                    if filename.endswith(".csv"):
                        df = pd.read_csv(f"../../data/raw/{project}/{device}/{filename}")
                        # removing any extra headers that happened to get appended
                        # to the raw datafile (specifically any file for TREC_Tower)
                        df = df[df["times"] != "times"]
                        # There was an issue with the raw TREC_Tower data. It was duplicated
                        # and appended multiple times. This was due to a misshap when first
                        # running the data_loader.py script. Due to the large number of api
                        # calls we would have to make again to run the script, we decided to
                        # work with what we have.
                        df.drop_duplicates(subset=['times'], inplace=True)
                        df.dropna(subset=['times'], inplace=True)
                        df.reset_index(inplace=True)

                        df["times"] = pd.to_datetime(df["times"])
                        df.drop(columns=["index"], inplace=True)

                        # hard coded because of how data_loader is structured.
                        # Ideally in version 2 of this software, this would be a
                        # variable index that reads in the parameter we are looking for,
                        # instead of hardcoding.

                        parameter = df.columns[1]

                        # saving the parameter variable name for later and standardizing to "value"
                        df.rename(columns={parameter: 'value'}, inplace=True)
                        df.set_index("times", inplace=True)
                        df["value"] = df["value"].astype(float)

                        # downsampling by hour and by day
                        hourly_df = df.groupby(["Units"]).resample('H').agg(
                            {"value": ["mean", "std"]})
                        daily_df = df.groupby(["Units"]).resample('D').agg(
                            {"value": ["mean", "std"]})
                        hourly_df.reset_index(inplace=True)
                        daily_df.reset_index(inplace=True)
                        hourly_df.set_index("times", inplace=True)
                        daily_df.set_index("times", inplace=True)
                        hourly_df.reset_index(inplace=True)
                        daily_df.reset_index(inplace=True)

                        # concatonating double headers to one single header.

                        hourly_df.columns = [col[0] if col[1] == ''
                                             else f"{col[0]}_{col[1]}" for col in hourly_df.columns]
                        daily_df.columns = [col[0] if col[1] == ''
                                            else f"{col[0]}_{col[1]}" for col in daily_df.columns]
                        hourly_df["parameter"] = parameter
                        daily_df["parameter"] = parameter

                        #save the data to a csv file
                        path = f"../../data/processed/{project}/{device}"
                        hourly_df.to_csv(os.path.join(path, f"hourly_{filename}"), index = False)
                        daily_df.to_csv(os.path.join(path, f"daily_{filename}"), index = False)

                self.parser(f"../../data/processed/{project}/{device}")



    def parser(self, directory: str ) -> None:
        """
        This function is to combine all of the individual processed csvs 
        we created from the function "downsample" above. This function's
        output is one csv for all of the hourly data and one csv for all 
        of the daily data for a given project and device.
        """
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

#datawrangler = DataWrangler()
#datawrangler.downsample()
