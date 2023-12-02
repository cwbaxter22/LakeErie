"""
TODO:
1) write a data cleaning function
2) add the other API key in the primary function, and write a function/loop to iterate through both
   apikeys + their associated devices.
4) Save the data to /data/processed/<device_name>_<parameter_name>.csv?
6) Add the units to the files.
7) data interfacer class to deal with the frontend/backend
"""

import os
import pandas as pd
#from dataloader import DataLoader


class DataTransformer():
    """
    This class can be used to aggregate and transform data from the user's computer. 
    This class is meant to be used in parallel with the DataLoader class.
    1) It will aggregate data from multiple csv files into one csv file
    2) It will transform the into a tidy format
    3) It will clean the data
    4) It will add units to the data (I think we should do this in the DataLoader class)

    """

    def __init__(self) -> None:
        """
        Arguments:
        --------
        variable (type): description
        
        Returns:
        --------
        
        Raises:
        -------
        """

        #undo the comment below and comment out the line below that to get the devices from the API
        #self.devices = list(DataLoader.get_devices().keys())
        self.devices = ["Beach2_Tower_iSIC"]
        self.raw_path = ""
        self.processed_path = ""
        self.project = ""

    def set_path(self, raw_path: str = "../../data/raw", processed_path: str = "../../data/processed") -> None:
        """
        This function sets the path for the raw and processed data.
        """
        self.raw_path = raw_path
        self.processed_path = processed_path

    def across_parameter_aggregate(self, device_name: str, project: str) -> None:

        """
        Here is the first working function for merging all of the data from a single device 
        into one csv file called "all_data.csv".
        TODO:

        """
        #initialize two empty dataframes to manipulate and write data to later
        df = pd.DataFrame()
        merged_df = pd.DataFrame()

        #loop through all the files in directory, read them in, and merge them into one dataframe
        #####################################################################
        # NOTE:this does not select for specific parameter files, so if there are additional
        # csv that haven't been hardcoded to ignore in this function, they will be merged into
        # the all_data.csv file.
        #####################################################################

        for filename in os.listdir(f"{self.raw_path}/{project}/{device_name}"):

            #iterate through all csv files
            if filename.endswith(".csv"):
                #these are the files that we don't want to merge into the all_data.csv file
                #########################################
                # Eventually will take this out because we will save them to the processed directory
                #########################################
                #if "all_data" not in filename and "identifier" not in filename and "tidy" 
                # not in filename:
                if all(keyword not in filename for keyword in ["all_data", "identifier", "tidy"]):
                    df = pd.read_csv(
                        os.path.join(
                            f"{self.raw_path}/{project}/{device_name}", filename
                            )
                            )

                    #merge the dataframes
                    if not merged_df.empty:
                        df["Units"] = df["Units"].astype(str)
                        merged_df = pd.merge(merged_df, df, on = ["times", "Units"], how="outer")
                    else:
                        merged_df = df

        # need to check to make sure the ../data/processed directory exists
        if not os.path.exists(f"{self.processed_path}"):
            os.makedirs(f"{self.processed_path}")
       
        #need to check to make sure the ../data/processed/<project> directory exists
        if not os.path.exists(f"{self.processed_path}/{project}"):
            os.makedirs(f"{self.processed_path}/{project}")

        #need to check to make sure the ../data/processed/<project>/<device_name> directory exists
        if not os.path.exists(os.path.join(f"{self.processed_path}/{project}/{device_name}")):  
            os.makedirs(os.path.join(f"{self.processed_path}/{project}/{device_name}"))

        if "AirTemp" in df.columns:
            df = df.rename(columns={"AirTemp": "Air_Temperature"})
        if "Temp" in df.columns:
            df = df.rename(columns={"Temp": "Water_Temperature"})
        if "ODO" in df.columns:
            df = df.rename(columns={"ODO": "Dissolved_Oxygen"})
        merged_df.to_csv(f"{self.processed_path}/{project}/{device_name}/all_data.csv", index=False)


    def device_aggregate(self, project: str) -> None:
        """
        Loops through all of the devices and calls across_parameter_aggregate on each device.
        """
        for device in self.devices:            
            self.across_parameter_aggregate(device, project)


    def tidy_data_transform(self, df: pd.DataFrame, device_name: str, project: str) -> None:
        """
        This function takes in a dataframe and returns a tidy dataframe.
        Formated columns: times, Units, parameter, value
        TODO: 
        2) Go over this cleaning iteration
        """
        #melts the dataframe into a tidy.format
        df = df.melt(id_vars=["times", "Units"], var_name="parameter", value_name="value")
        #cleaning functions:
        #changing the times to pandas datetime format
        df["times"] = pd.to_datetime(df["times"])
        #changing the value column to numeric
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        df = df.dropna()
        df = df.sort_values(by = "times")
        df.to_csv(f"{self.processed_path}/{project}/{device_name}/tidy_all_data.csv", index=False)


    def tidy_devices(self, project: str) -> None:
        """
        This function iterates through a list of devices 
        and creates tidy dataframes in the device directory.
        """
        #check to see if the ../data/processed directory exists -- for a test

        for device in self.devices:
            df = pd.DataFrame()
            #check to see if the all_data.csv file exists from the processed directory
            if not os.path.exists(os.path.join(f"{self.processed_path}/{project}/{device}", "all_data.csv")):
                #if it doesn't exist, then call the across_parameter_aggregate function
                #to create it.
                self.across_parameter_aggregate(device, project)

            #if it does, then read it in and tidy it
            else:
                df = pd.read_csv(os.path.join(f"{self.processed_path}/{project}/{device}", "all_data.csv"))
                self.tidy_data_transform(df, device, project)


    def downsample_hour(self, df: pd.DataFrame, device_name: str, project: str) -> None:
        """
        This function will downsample the data to 1 hour intervals.

        TODO:
        1) do we want standard error to the mean? or is std enough?
        """
        hourly_df = pd.DataFrame()

        ## is this doubled up in another function?
        df["times"] = pd.to_datetime(df["times"])
        
        #set the times column as the index
        df.set_index("times", inplace=True)

        #groupby the parameter and units, then resample the data to 1 hour intervals
        hourly_df = df.groupby(["parameter", "Units"]).resample("H").agg({"value": ["mean", "std"]})
        
        #reset the index
        hourly_df.reset_index(inplace=True)

        #combine multiindex columns into one column
        hourly_df.columns = [col[0] if col[1] == '' else f"{col[0]}_{col[1]}" for col in hourly_df.columns]
        
        #save the data to a csv file
        hourly_df.to_csv(f"{self.processed_path}/{project}/{device_name}/hourly_tidy_all_data.csv", index = False)


    def downsample_day(self, df: pd.DataFrame, device_name: str, project: str) -> None:
        """
        This function will downsample the data to 1 day intervals.
        TODO:
        1) do we want standard error to the mean? or is std enough?
        """
        daily_df = pd.DataFrame()
        #is this doubled up in another function?
        df["times"] = pd.to_datetime(df["times"])

        #set the times column as the index
        df.set_index("times", inplace=True)
        
        #groupby the parameter and units, then resample the data to 1 day intervals
        daily_df = df.groupby(["parameter", "Units"]).resample("D").agg({"value": ["mean", "std"]})

        #reset the index
        daily_df.reset_index(inplace=True)
        
        #combine multiindex columns into one column
        daily_df.columns = [col[0] if col[1] == '' else f"{col[0]}_{col[1]}" for col in daily_df.columns]

        #save the data to a csv file
        daily_df.to_csv(f"{self.processed_path}/{project}/{device_name}/daily_tidy_all_data.csv", index = False)

    def device_downsample_hour(self, project: str) -> None:
        """
        This function will call downsample_hour for all devices
        """
        
        # need to check to make sure the processed tidy_all_data.csv files exist if not, call tidy_data_transform

        for device in self.devices:
            df = pd.read_csv(f"{self.processed_path}/{project}/{device}/tidy_all_data.csv")
            self.downsample_hour(df, device, project)
    

    def device_downsample_day(self, project: str) -> None:
        """
        This function will call downsample_day for all devices
        """
        # need to check to make sure the processed tidy_all_data.csv files exist if not, call tidy_data_transform

        for device in self.devices:
            if device != "test_device":
                df = pd.read_csv(f"{self.processed_path}/{project}/{device}/tidy_all_data.csv")
                self.downsample_day(df, device, project)
                

    def across_projects(self) -> None:
        """
        Run the above functions for the old and new projects
        """
        project = "old"
        self.set_path()
        self.device_aggregate(project)
        self.tidy_devices(project)
        self.device_downsample_hour(project)
        self.device_downsample_day(project)

        project = "new"
        self.set_path()
        self.device_aggregate(project)
        self.tidy_devices(project)
        self.device_downsample_hour(project)
        self.device_downsample_day(project)


        return None

    def clean_data(self) -> None:
        """
        This function will clean the data.
        I think this function should be called as early as possible
        Remove NAN or replace with average?

        """

        return None

dataTransformer = DataTransformer()
dataTransformer.across_projects()
#dataTransformer.device_aggregate()
#dataTransformer.tidy_devices()
#dataTransformer.device_downsample_hour()
#dataTransformer.device_downsample_day()

