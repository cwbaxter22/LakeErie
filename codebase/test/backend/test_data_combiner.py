"""
This file is used to test the data_combiner.py file and functions. 
It creates data files to be used for testing the data_combiner.py file.
The data files are created in the testdata directory.
They are deleted after the tests are run.

"""

import os
import sys
import unittest
import pathlib
import importlib

import numpy as np
import pandas as pd


#sys.path.append("../../src/backend")
#from data_combiner import DataCombiner
codebase_path = pathlib.Path(__file__).parents[2]
#https://stackoverflow.com/questions/65206129/importlib-not-utilising-recognising-path
spec = importlib.util.spec_from_file_location(
    name='data_combiner_mod',  # name is not related to the file, it's the module name!
    location= str(codebase_path) +
    "//src//backend//data_combiner.py"  # full path to the script
    )

data_combiner_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(data_combiner_mod)




class TestDataCombiner(unittest.TestCase):
    """
    This testing class tests the functions in the data_combiner.py file.
    Specifically, it sets up a testing directory with test csv files and
    tests the combine_daily and combine_hourly functions.
    """

    def setUp(self) -> None:
        """
        Set up the test cases, including creating a testing directory with test csv files.
        """
        #self.data_combiner = DataCombiner()
        self.data_combiner = data_combiner_mod.DataCombiner()
        self.devices = ["TREC_Tower"]
        self.projects = ["new", "old", "ichart"]
        #sys.path.append("/home/runner/work/LakeErie/LakeErie/codebase/test/backend/../testdata/raw/ichart") # Git Actions Running
        self.processed_path = "/home/runner/work/LakeErie/LakeErie/codebase/test/backend/../testdata/processed"

        #check to see if the data directory exists and create it if it does not
        if not os.path.exists(self.processed_path):
            os.mkdir(self.processed_path)
        if not os.path.exists(f"{self.processed_path}/combined"):
            os.mkdir(f"{self.processed_path}/combined")

        for project in self.projects:
            if not os.path.exists(f"{self.processed_path}/{project}"):
                os.mkdir(f"{self.processed_path}/{project}")

            # check to see if the processed directory exists
            for device in self.devices:
                if not os.path.exists(f"{self.processed_path}/{project}/{device}"):
                    os.mkdir(f"{self.processed_path}/{project}/{device}")

                if not os.path.exists(f"{self.processed_path}/combined/{device}"):
                    os.mkdir(f"{self.processed_path}/combined/{device}")

        self.data_combiner.set_path(self.processed_path)
        self.create_processed_test_csv("ichart", "2011")
        self.create_processed_test_csv("old", "2018")
        self.create_processed_test_csv("new", "2022")
        self.data_combiner.set_map({"TREC_Tower": ["TREC_Tower", "TREC_Tower", "TREC_Tower"]})

    def tearDown(self) -> None:
        """
        Tear down the test cases and remove the files. 
        """
        for project in self.projects:
            for device in self.devices:
                path = self.processed_path
                if os.path.exists(f"{path}/{project}/{device}/tidy_daily_all_data.csv"):
                    os.remove(f"{path}/{project}/{device}/tidy_daily_all_data.csv")
                if os.path.exists(f"{path}/{project}/{device}/tidy_hourly_all_data.csv"):
                    os.remove(f"{path}/{project}/{device}/tidy_hourly_all_data.csv")
                if os.path.exists(f"{path}/combined/{device}/daily_data.csv"):
                    os.remove(f"{path}/combined/{device}/daily_data.csv")
                if os.path.exists(f"{path}/combined/{device}/hourly_data.csv"):
                    os.remove(f"{path}/combined/{device}/hourly_data.csv")
                if os.path.exists(f"{path}/{project}/{device}"):
                    os.rmdir(f"{path}/{project}/{device}")
                if os.path.exists(f"{path}/combined/{device}"):
                    os.rmdir(f"{path}/combined/{device}")
            if os.path.exists(f"{path}/{project}"):
                os.rmdir(f"{path}/{project}")

    def create_processed_test_csv(self, project: str, year: str):
        """
        Create a test csv file to be used for testing the data_combiner.py file.

        Parameters
        ----------
        project : str
            The project you want to create the test csv file for.
        year : str
            The year you want in the test csv file.
        
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
            path = f"{self.processed_path}/{project}/{device}"
            expected_daily_data.to_csv(f"{path}/tidy_daily_all_data.csv", index=False)

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
            expected_hourly_data.to_csv(f"{path}/tidy_hourly_all_data.csv", index=False)

    def test_combine_daily(self):
        """
        This function tests the combine_daily function. It compares the 
        output function with the expected simulated data given below. 
        """
        # expected data given the transformations above.
        expected_data = {
            "times": ["2011-01-01",
                      "2011-01-01",
                      "2018-01-01",
                      "2018-01-01",
                      "2022-01-01",
                      "2022-01-01"],
            "parameter": ["Air_Temperature",
                          "ODO",
                          "Air_Temperature",
                          "ODO",
                          "Air_Temperature",
                          "ODO"],
            "Units": ["F", "mg/L", "F", "mg/L", "F", "mg/L"],
            "value_mean": [42.4, 9.9, 42.4, 9.9, 42.4, 9.9],
            "value_std": [0.43589,0.6245, 0.43589, 0.6245, 0.43589, 0.6245],
            "location": ["TREC_Tower",
                         "TREC_Tower",
                         "TREC_Tower",
                         "TREC_Tower",
                         "TREC_Tower",
                         "TREC_Tower"]
        }
        expected_data["times"] = pd.Series(expected_data["times"])
        expected_data = pd.DataFrame(expected_data)

        self.data_combiner.combine_daily()
        path = f"{self.processed_path}/combined/TREC_Tower"
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

    def test_combine_hourly(self):
        """
        Testing the function combine_hourly. It compares the output function
        with the expected simulated data given below.
        """
        # expected data given the transformations above.
        expected_data = {
            "times": ["2011-01-01 13:00:00",
                      "2011-01-01 13:00:00",
                      "2018-01-01 13:00:00",
                      "2018-01-01 13:00:00",
                      "2022-01-01 13:00:00",
                      "2022-01-01 13:00:00"],
            "parameter": ["Air_Temperature",
                          "ODO",
                          "Air_Temperature",
                          "ODO",
                          "Air_Temperature",
                          "ODO"],
            "Units": ["F", "mg/L", "F", "mg/L", "F", "mg/L"],
            "value_mean": [42.4, 9.9, 42.4, 9.9, 42.4, 9.9],
            "value_std": [0.43589,0.6245, 0.43589, 0.6245, 0.43589, 0.6245],
            "location": ["TREC_Tower",
                         "TREC_Tower",
                         "TREC_Tower",
                         "TREC_Tower",
                         "TREC_Tower",
                         "TREC_Tower"]
        }
        expected_data["times"] = pd.Series(expected_data["times"])
        expected_data = pd.DataFrame(expected_data)

        self.data_combiner.combine_hourly()
        path = f"{self.processed_path}/combined/TREC_Tower"
        self.assertTrue(os.path.exists(os.path.join(path, "hourly_data.csv")))
        df = pd.read_csv(os.path.join(path, "hourly_data.csv"))
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
