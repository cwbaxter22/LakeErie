"""
This script runs after data_loader and data_transformer. 
It combines the data from all 3 sources (iChart, Old, New) from data/processed 
into a single combined dataset. Ideally, this script only needs to be run once 
or any time we collect new data from the WQData API. 
"""

import os
import pandas as pd

from config_combine import COMBINE_MAP


class DataCombiner():
    """
    This class is used to combine the data from all 3 sources (iChart, Old, New)
    into a single combined dataset.
    """

    def __init__(self):
        """
        Initialize the DataCombiner class.
        """
        self.path = ""
        self.map = {}

    def set_path(self, path: str = "../../data/processed"):
        """
        Set the path to the data directory.

        Parameters
        path : str (the path to the data directory).
        """
        self.dir = path

    def set_map(self, map: dict = COMBINE_MAP):
        """
        Set the map to the data directory.

        Parameters
        map : dict (the map to the data directory).
        """
        self.map = map

    def combine_daily(self):
        """
        Combine the data from all 3 sources (iChart, Old, New) into a single combined dataset.
        It will combine all the daily data from the 3 sources into a single csv file.
        """

        # Run for daily data
        for name, all_device in self.map.items():
            combined_df = []
            for proj, prod_device in zip(["ichart", "old", "new"], all_device):
                # Skip in 
                if prod_device is None:
                    continue
                if proj == "ichart":
                    path = f"{self.dir}/{proj}/{prod_device}/tidy_daily_all_data.csv"
                else:
                    path = f"{self.dir}/{proj}/{prod_device}/tidy_daily_all_data.csv"
                if not os.path.exists(path):
                    raise FileNotFoundError(f"Path {path} does not exist.")

                combined_df.append(
                    pd.read_csv(path)
                )

            combined_df = pd.concat(combined_df, ignore_index=True).set_index("times")
            combined_df["location"] = name

            # Standardizing the variable names we are confident of.
            # Note: we do not know what the variable "Temperature" is, so we do not standardize it.
            # It could be water temperature, air temperature, battery temperature or something else.
            combined_df['parameter'] = combined_df['parameter'].replace('AirTemp',
                                                                        'Air_Temperature')
            combined_df['parameter'] = combined_df['parameter'].replace('Dissolved_Oxygen',
                                                                        'ODO')
            combined_df['parameter'] = combined_df['parameter'].replace('DO',
                                                                        'ODO')

            # removing gross outliers
            combined_df = combined_df[~((combined_df['parameter'] == 'Water_Temperature') &
                                        (combined_df['value_mean'] > 110))]
            combined_df = combined_df[~((combined_df['parameter'] == 'Water_Temperature') &
                                        (combined_df['value_mean'] <-50))]
            combined_df = combined_df[~((combined_df['parameter'] == 'Air_Temperature') &
                                        (combined_df['value_mean'] > 110))]
            combined_df = combined_df[~((combined_df['parameter'] == 'Air_Temperature') &
                                        (combined_df['value_mean'] <-50))]
            combined_df = combined_df[~((combined_df['parameter'] == 'Temperature') &
                                        (combined_df['value_mean'] <-50))]
            combined_df = combined_df[~((combined_df['parameter'] == 'ODO') &
                                        (combined_df['value_mean'] < 0.001))]
            combined_df = combined_df[~((combined_df['parameter'] == 'ODO') &
                                        (combined_df['value_mean'] > 30))]

            if not os.path.exists(f"{self.dir}/combined/{name}"):
                os.mkdir(f"{self.dir}/combined/{name}")
            combined_df.to_csv(f"{self.dir}/combined/{name}/daily_data.csv")


    def combine_hourly(self):
        """
        Combine the data from all 3 sources (iChart, Old, New) into a single combined dataset.
        It will combine all the hourly data from the 3 sources into a single csv file.
        """

        # Run for hourly data
        for name, all_device in self.map.items():
            combined_df = []
            for proj, prod_device in zip(["ichart", "old", "new"], all_device):
                # Skip in
                if prod_device is None:
                    continue
                if proj == "ichart":
                    path = f"{self.dir}/{proj}/{prod_device}/tidy_hourly_all_data.csv"
                    #path = f"../../data/processed/{proj}/{prod_device}/tidy_hourly_all_data.csv"
                else:
                    path = f"{self.dir}/{proj}/{prod_device}/tidy_hourly_all_data.csv"
                    #path = f"../../data/processed/{proj}/{prod_device}/tidy_hourly_all_data.csv"
                if not os.path.exists(path):
                    raise FileNotFoundError(f"Path {path} does not exist.")

                combined_df.append(
                    pd.read_csv(path)
                )
            combined_df = pd.concat(combined_df, ignore_index=True).set_index("times")
            combined_df["location"] = name

            # Standardizing the variable names we are confident of.
            # Note: we do not know what the variable "Temperature" is, so we do not standardize it.
            # It could be water temperature, air temperature, battery temperature or something else.
            combined_df['parameter'] = combined_df['parameter'].replace('AirTemp',
                                                                        'Air_Temperature')
            combined_df['parameter'] = combined_df['parameter'].replace('Dissolved_Oxygen',
                                                                        'ODO')
            combined_df['parameter'] = combined_df['parameter'].replace('DO',
                                                                        'ODO')

            # removing gross outliers
            combined_df = combined_df[~((combined_df['parameter'] == 'Water_Temperature') &
                                        (combined_df['value_mean'] > 110))]
            combined_df = combined_df[~((combined_df['parameter'] == 'Water_Temperature') &
                                        (combined_df['value_mean'] <-50))]
            combined_df = combined_df[~((combined_df['parameter'] == 'Air_Temperature') &
                                        (combined_df['value_mean'] > 110))]
            combined_df = combined_df[~((combined_df['parameter'] == 'Air_Temperature') &
                                        (combined_df['value_mean'] <-50))]
            combined_df = combined_df[~((combined_df['parameter'] == 'Temperature') &
                                        (combined_df['value_mean'] <-40))]
            combined_df = combined_df[~((combined_df['parameter'] == 'ODO') &
                                        (combined_df['value_mean'] < -10))]
            combined_df = combined_df[~((combined_df['parameter'] == 'ODO') &
                                        (combined_df['value_mean'] < 0.001))]
            combined_df = combined_df[~((combined_df['parameter'] == 'ODO') &
                                        (combined_df['value_mean'] > 30))]

            if not os.path.exists(f"{self.dir}/combined/{name}"):
                os.mkdir(f"{self.dir}/combined/{name}")
            combined_df.to_csv(f"{self.dir}/combined/{name}/hourly_data.csv")

dataCombiner = DataCombiner()
dataCombiner.set_path()
dataCombiner.combine_daily()
dataCombiner.combine_hourly()
