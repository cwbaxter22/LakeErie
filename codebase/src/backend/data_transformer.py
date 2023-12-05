
import os
import pandas as pd

#from data_loader import DataLoader


class DataTransformer():
    """
    This class can be used to aggregate and transform data from the user's computer. 
    This class is meant to be used in parallel with the DataLoader class.
    1) Specify the desrired path to the raw and processed data via set_path
    2) Run across_projects to aggregate and transform data from the old and new projects
        a) This function will call the following functions:
            i) device_aggregate
            ii) tidy_devices
            iii) device_downsample_hour
            iv) device_downsample_day

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
        self.devices = []
        self.raw_path = ""
        self.processed_path = ""
        self.project = ""

    def set_path(self,
                 raw_path: str = "../../data/raw",
                 processed_path: str = "../../data/processed"
                 ) -> None:
        """
        This function sets the path for the raw and processed data.
        The defaults are set to the expected path for the data on the user's computer, 
        given the user correctly downloaded/cloned the repository.
        """
        self.raw_path = raw_path
        self.processed_path = processed_path

    # need to add the default to get.devices from zac's code
    def set_devices(self, devices: list) -> None:
        self.devices = devices

    def across_parameter_aggregate(self, device_name: str, project: str) -> None:

        """
        Merges the data from multiple csv files into one csv file.

        Arguments:
        device_name (str): the name of the device that you want to aggregate data for.
        project (str): the name of the project that you want to aggregate data for.

        variable (type): description
        
        Returns:
        No returns, but writes a csv file to the processed directory.
        
        Raises:
        -------

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
            print(1)

            #iterate through all csv files
            if filename.endswith(".csv"):
                #these are the files that we don't want to merge into the all_data.csv file
                #if "all_data" not in filename and "identifier" not in filename and "tidy" 
                # not in filename:
                print(2)
                if all(keyword not in filename for keyword in ["all_data", "identifier", "tidy"]):
                    df = pd.read_csv(
                        os.path.join(
                            f"{self.raw_path}/{project}/{device_name}", filename
                            )
                            )
                    print(3)
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

        #standardize the column names across all data sets
        if "AirTemp" in df.columns:
            df = df.rename(columns={"AirTemp": "Air_Temperature"})
        if "Temp" in df.columns:
            df = df.rename(columns={"Temp": "Water_Temperature"})
        if "ODO" in df.columns:
            df = df.rename(columns={"ODO": "Dissolved_Oxygen"})

        #write the merged dataframe to a csv file
        merged_df.to_csv(f"{self.processed_path}/{project}/{device_name}/all_data.csv", index=False)

    def device_aggregate(self, project: str) -> None:
        """
        Loops through all of the devices and calls across_parameter_aggregate on each device.
        """
        for device in self.devices:            
            self.across_parameter_aggregate(device, project)

    def tidy_data_transform(self, df: pd.DataFrame, device_name: str, project: str) -> None:
        """
        Takes the all_data.csv file and transforms it into a tidy format.
        To be run after the device_aggregate function.

        Arguments:
        df (pd.DataFrame): the dataframe (all_data.csv) that you want to transform into a tidy format.
        device_name (str): the name of the device that you want to aggregate data for.

        project (str): the name of the project that you want to aggregate data for.

        variable (type): description
        
        Returns:
        No returns, but writes a csv file to the processed directory.
        
        Raises:
        -------

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

        Arguments:
        df (pd.DataFrame): the dataframe (tidy_all_data.csv) that you want to aggregate data for.
        device_name (str): the name of the device that you want to aggregate data for.
        project (str): the name of the project that you want to aggregate data for.

        
        Returns:
        No returns, but writes a csv file to the processed directory.
        
        Raises:
        -------
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

    # def across_projects(self, project: string) -> None:
    #     """
    #     Run all data cleaning functions for a given project
    #     """
    #     self.set_path()
    #     self.device_aggregate(project)
    #     self.tidy_devices(project)
    #     self.device_downsample_hour(project)
    #     self.device_downsample_day(project)
        
# dataTransformer = DataTransformer()
# dataTransformer.set_path("../../data/raw/ichart/pivot")
# dataTransformer.set_devices(["Beach2_Tower", "Beach2_Buoy", "Beach6_Buoy", "TREC_Tower"])
# dataTransformer.device_aggregate("ichart")
# dataTransformer.across_projects(project = "old")
#dataTransformer.device_aggregate(project = "old")
#dataTransformer.tidy_devices(project = "old")
#dataTransformer.device_downsample_hour(project = "old")
#dataTransformer.device_downsample_day(project = "old")

