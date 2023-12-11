"""
This file is used to test the data_combiner.py file.

"""

import os
import sys
import unittest

import numpy as np
import pandas as pd

sys.path.append("../../src/backend")
from data_transformer import DataTransformer
from data_combiner import DataCombiner


class TestDataCombiner(unittest.TestCase):
    """
    
    """

    def setUp(self) -> None:
        """
        Set up the test cases.
        """
        self.data_transformer = DataTransformer()
        self.data_combiner = DataCombiner()
        self.devices = ["TREC_Tower", "Beach2_Buoy"]
        self.projects = ["new", "old", "ichart"]
        

        #check to see if the data directory exists and create it if it does not
        if not os.path.exists("../testdata/processed"):
            os.mkdir("../testdata/processed")
        if not os.path.exists("../testdata/processed/combined"):
            os.mkdir("../testdata/processed/combined")
        
        for project in self.projects:
            if not os.path.exists(f"../testdata/processed/{project}"):
                os.mkdir(f"../testdata/processed/{project}")

            # check to see if the processed directory exists
            for device in self.devices:
                if not os.path.exists(f"../testdata/processed/{project}/{device}"):
                    os.mkdir(f"../testdata/processed/{project}/{device}")
           
                if not os.path.exists(f"../testdata/processed/combined/{device}"):
                    os.mkdir(f"../testdata/processed/combined/{device}")
        
        self.data_combiner.set_path("../testdata/processed")
        self.create_processed_test_csv("ichart", "2011")
        self.create_processed_test_csv("old", "2018")
        self.create_processed_test_csv("new", "2022")
        self.data_combiner.set_map({"TREC_Tower": ["TREC_Tower", "TREC_Tower", "TREC_Tower"], "Beach2_Buoy": ["Beach2_Buoy", "Beach2_Buoy", "Beach2_Buoy"]})
        

            
    def create_processed_test_csv(self, project: str, year: str):
        """
        Create a test csv file to be used for testing the data_combiner.py file.

        Parameters
        ----------
        path : str
            The path of the csv file to be created.
        """
        # create a test csv file for tidy_all_data
        for device in self.devices:
            expected_daily_data = {
                "times": [f"1/1/{year}", f"1/1/{year}"],
                "Units": ["F", "mg/L"],
                "value_mean": [42.4, 9.9],
                "value_std": [0.43589, 0.6245],
                "parameter": ["Air_Temperature", "ODO"]
            }
            expected_daily_data["times"] = pd.to_datetime(expected_daily_data["times"])
            expected_daily_data["times"] = pd.Series(expected_daily_data["times"])
            expected_daily_data = pd.DataFrame(expected_daily_data)
            expected_daily_data.to_csv(f"../testdata/processed/{project}/{device}/tidy_daily_all_data.csv", index=False)


            expected_hourly_data = {
                "times": [f"1/1/{year} 13:00", f"1/1/{year} 13:00"],
                "Units": ["F", "mg/L"],
                "value_mean": [42.4, 9.9],
                "value_std": [0.43589, 0.6245],
                "parameter": ["Air_Temperature", "ODO"]
            }
            expected_hourly_data["times"] = pd.to_datetime(expected_hourly_data["times"])
            expected_hourly_data["times"] = pd.Series(expected_hourly_data["times"])
            expected_hourly_data = pd.DataFrame(expected_hourly_data)
            expected_hourly_data.to_csv(f"../testdata/processed/{project}/{device}/tidy_hourly_all_data.csv", index=False)


        
        

    def test_combine_daily(self):
        """
        
        """

        expected_columns = ["times", "Units", "value_mean", "value_std", "parameter", "location"]
        expected_data = {
            "times": ["2011-01-01", "2011-01-01", "2018-01-01", "2018-01-01", "2022-01-01", "2022-01-01"],
            "parameter": ["Air_Temperature","ODO", "Air_Temperature", "ODO", "Air_Temperature", "ODO"],
            "Units": ["F", "mg/L", "F", "mg/L", "F", "mg/L"],
            "value_mean": [42.4, 9.9, 42.4, 9.9, 42.4, 9.9],
            "value_std": [0.43589,0.6245, 0.43589, 0.6245, 0.43589, 0.6245],
            "location": ["TREC_Tower", "TREC_Tower", "TREC_Tower", "TREC_Tower", "TREC_Tower", "TREC_Tower"]
        }
        expected_data["times"] = pd.Series(expected_data["times"])
        expected_data = pd.DataFrame(expected_data)
        
        self.data_combiner.combine_daily()
        path = "../testdata/processed/combined/TREC_Tower"
        self.assertTrue(os.path.exists(os.path.join(path, "daily_data.csv")))
        df = pd.read_csv(os.path.join(path, "daily_data.csv"))
        self.assertTrue(df["times"].equals(expected_data["times"]),
                        "times are not equal")
        self.assertTrue(df["parameter"].equals(expected_data["parameter"]),
                        "parameters are not equal")
        self.assertTrue(df["Units"].equals(expected_data["Units"]),
                        "units are not equal")
        self.assertTrue(df["value_mean"].equals(expected_data["value_mean"]),
                        "value_means are not equal")
        sd_check = np.isclose(df["value_std"],expected_data["value_std"])
        for truth in sd_check:
            self.assertTrue(truth, "value_stds are not equal")
        self.assertTrue(df["location"].equals(expected_data["location"]),
                        "locations are not equal")


if __name__ == '__main__':
    unittest.main()
