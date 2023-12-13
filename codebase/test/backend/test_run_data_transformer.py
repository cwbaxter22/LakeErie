"""
This testing class tests the functions in the run_data_transformer.py file.
Specifically, it sets up a testing directory with test csv files and
tests the downsample function. 
"""


import os
import unittest
import pathlib
import importlib

import numpy as np
import pandas as pd


codebase_path = pathlib.Path(__file__).parents[2]
#https://stackoverflow.com/questions/65206129/importlib-not-utilising-recognising-path
spec = importlib.util.spec_from_file_location(
    name='data_wrangler_mod',  # name is not related to the file, it's the module name!
    location= str(codebase_path) +
    "//src//backend//run_data_transformer.py"  # full path to the script
    )

data_wrangler_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(data_wrangler_mod)



class TestRunDataTransformer(unittest.TestCase):
    """
    This testing class tests the functions in the run_data_transformer.py file.
    Specifically, it sets up a testing directory with test csv files and
    tests the combine_daily and combine_hourly functions.
    """

    def setUp(self) -> None:
        """
        Set up the test cases, including creating a testing directory with test csv files.
        """
        self.data_wrangler = data_wrangler_mod.DataWrangler()
        self.projects = ["old"]
        self.devices = ["TREC_Tower"]
        self.data_wrangler.set_project(self.projects)
        self.raw_path = "../testdata/raw"
        self.processed_path = "../testdata/processed"
        self.data_wrangler.set_path(self.raw_path, self.processed_path)

        if not os.path.exists("../testdata/raw"):
            os.mkdir("../testdata/raw")

        for project in self.projects:
            if not os.path.exists(f"../testdata/raw/{project}"):
                os.mkdir(f"../testdata/raw/{project}")

            # check to see if the processed directory exists
            for device in self.devices:
                if not os.path.exists(f"../testdata/raw/{project}/{device}"):
                    os.mkdir(f"../testdata/raw/{project}/{device}")


        #check to see if the data directory exists and create it if it does not
        if not os.path.exists("../testdata/processed"):
            os.mkdir("../testdata/processed")

        for project in self.projects:
            if not os.path.exists(f"../testdata/processed/{project}"):
                os.mkdir(f"../testdata/processed/{project}")

            # check to see if the processed directory exists
            for device in self.devices:
                if not os.path.exists(f"../testdata/processed/{project}/{device}"):
                    os.mkdir(f"../testdata/processed/{project}/{device}")

        # create a test csv file for tidy_all_data
        self.create_raw_test_csv()

    def tearDown(self) -> None:
        """
        Tear down the test cases and remove the files. 
        """
        # remove the test csv files
        os.remove(f"{self.raw_path}/old/TREC_Tower/Air_Temperature.csv")
        os.remove(f"{self.processed_path}/old/TREC_Tower/tidy_daily_all_data.csv")
        os.remove(f"{self.processed_path}/old/TREC_Tower/tidy_hourly_all_data.csv")
        os.remove(f"{self.processed_path}/old/TREC_Tower/hourly_Air_Temperature.csv")
        os.remove(f"{self.processed_path}/old/TREC_Tower/daily_Air_Temperature.csv")


        # remove the test directories
        os.rmdir(f"{self.raw_path}/old/TREC_Tower")
        os.rmdir(f"{self.raw_path}/old")
        os.rmdir(f"{self.processed_path}/old/TREC_Tower")
        os.rmdir(f"{self.processed_path}/old")

    def create_raw_test_csv(self):
        """
        Create a test csv file to be used for testing the run_data_transformer.py file.
        
        """
        # create a test csv file for tidy_all_data
        test_df = {
            "times": ["5/6/2014 4:10", "5/6/2014 3:40", "5/6/2014 4:00", "5/6/2014 3:50"],
            "Air_Temperature": [42.4, 43.4, 43.4, 42.4],
            "Units" : ["F", "F", "F", "F"],
        }
        test_df["times"] = pd.to_datetime(test_df["times"])
        test_df["times"] = pd.Series(test_df["times"])
        test_df = pd.DataFrame(test_df)

        test_df.to_csv(f"{self.raw_path}/old/TREC_Tower/Air_Temperature.csv", index=False)

    def test_downsample(self):
        """
        This function tests the downsample function. It compares the 
        output function with the expected simulated data given below. 
        """
        # expected data given the transformations above.
        expected_daily_data = {
            "times": ["2014-05-06"],
            "Units": ["F"],
            "value_mean": [42.9],
            "value_std": [0.57735],
            "parameter": ["Air_Temperature"],
        }
        expected_daily_data["times"] = pd.Series(expected_daily_data["times"])
        expected_daily_data = pd.DataFrame(expected_daily_data)

        self.data_wrangler.downsample()
        path = "../testdata/processed/old/TREC_Tower"
        self.assertTrue(os.path.exists(os.path.join(path, "tidy_daily_all_data.csv")))
        df = pd.read_csv(os.path.join(path, "tidy_daily_all_data.csv"))
        self.assertTrue(df["times"].equals(expected_daily_data["times"]),
                        "times are not equal")
        self.assertTrue(df["parameter"].equals(expected_daily_data["parameter"]),
                        "parameters are not equal")
        self.assertTrue(df["Units"].equals(expected_daily_data["Units"]),
                        "units are not equal")
        self.assertTrue(df["value_mean"].equals(expected_daily_data["value_mean"]),
                        "value_means are not equal")
        sd_check = np.isclose(df["value_std"],expected_daily_data["value_std"])
        for truth in sd_check:
            self.assertTrue(truth, "value_stds are not equal")

        expected_hourly_data = {
            "times": ["2014-05-06 03:00:00", "2014-05-06 04:00:00"],
            "Units": ["F", "F"],
            "value_mean": [42.9, 42.9],
            "value_std": [0.707107, 0.707107],
            "parameter": ["Air_Temperature", "Air_Temperature"],
        }
        expected_hourly_data["times"] = pd.Series(expected_hourly_data["times"])
        expected_hourly_data = pd.DataFrame(expected_hourly_data)

        self.data_wrangler.downsample()
        path = "../testdata/processed/old/TREC_Tower"
        self.assertTrue(os.path.exists(os.path.join(path, "tidy_hourly_all_data.csv")))
        df = pd.read_csv(os.path.join(path, "tidy_hourly_all_data.csv"))
        self.assertTrue(df["times"].equals(expected_hourly_data["times"]),
                        "times are not equal")
        self.assertTrue(df["parameter"].equals(expected_hourly_data["parameter"]),
                        "parameters are not equal")
        self.assertTrue(df["Units"].equals(expected_hourly_data["Units"]),
                        "units are not equal")
        self.assertTrue(df["value_mean"].equals(expected_hourly_data["value_mean"]),
                        "value_means are not equal")
        sd_check = np.isclose(df["value_std"],expected_hourly_data["value_std"])
        for truth in sd_check:
            self.assertTrue(truth, "value_stds are not equal")



if __name__ == '__main__':
    unittest.main()
