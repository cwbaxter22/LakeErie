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
    name='OldDataTransformer_mod',  # name is not related to the file, it's the module name!
    location= str(codebase_path) +
    "//src//backend//preprocess_ichart_data.py"  # full path to the script
    )

old_data_transformer_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old_data_transformer_mod)


class TestPreprocessIchartData(unittest.TestCase):
    """
    This testing class tests the functions in the run_data_transformer.py file.
    Specifically, it sets up a testing directory with test csv files and
    tests the combine_daily and combine_hourly functions.
    """

    def setUp(self) -> None:
        """
        Set up the test cases, including creating a testing directory with test csv files.
        """
        self.oldtransformer = old_data_transformer_mod.OldDataTransformer
        self.projects = ["ichart"]
        self.devices = ["TREC_Tower"]
        self.raw_path = "../testdata/raw/ichart"
        self.processed_path = "../testdata/processed"
        self.oldtransformer.set_path(self.raw_path, self.processed_path)

        if not os.path.exists("../testdata/raw"):
            os.mkdir("../testdata/raw")

        for project in self.projects:
            if not os.path.exists(f"../testdata/raw/{project}"):
                os.mkdir(f"../testdata/raw/{project}")

            # check to see if the processed directory exists
            if not os.path.exists(f"../testdata/raw/{project}/by_parameter"):
                os.mkdir(f"../testdata/raw/{project}/by_parameter")

            if not os.path.exists(f"../testdata/raw/{project}/pivot"):
                os.mkdir(f"../testdata/raw/{project}/pivot")
            
            for device in self.devices:
                if not os.path.exists(f"../testdata/raw/{project}/by_parameter/{device}"):
                    os.mkdir(f"../testdata/raw/{project}/by_parameter/{device}")
                if not os.path.exists(f"../testdata/raw/{project}/pivot/{device}"):
                    os.mkdir(f"../testdata/raw/{project}/pivot/{device}")

        # create a test csv file for tidy_all_data
        self.create_raw_test_csv()

    def tearDown(self) -> None:
        """
        Tear down the test cases and remove the files. 
        """
        # remove the test csv files
        os.remove(f"{self.raw_path}/by_parameter/TREC_Tower/AirTemp_F.csv")
        os.remove(f"{self.raw_path}/pivot/TREC_Tower/AirTemp_pivot.csv")



        # remove the test directories
        os.rmdir(f"{self.raw_path}/by_parameter/TREC_Tower")
        os.rmdir(f"{self.raw_path}/pivot/TREC_Tower")
        os.rmdir(f"{self.raw_path}/by_parameter")
        os.rmdir(f"{self.raw_path}/pivot")
        os.rmdir(f"{self.raw_path}")


    def create_raw_test_csv(self):
        """
        Create a test csv file to be used for testing the run_data_transformer.py file.
        
        """
        # create a test csv file for tidy_all_data
        test_df = {
            "times": ["5/6/2014 4:10", "5/6/2014 4:20"],
            "parameter": ["AirTemp_F", "AirTemp_F"],
            "value" : [44, 32],
        }
        test_df["times"] = pd.to_datetime(test_df["times"])
        test_df["times"] = pd.Series(test_df["times"])
        test_df = pd.DataFrame(test_df)

        test_df.to_csv(f"{self.raw_path}/by_parameter/TREC_Tower/AirTemp_F.csv", index=False)


    def test_format_pivot(self):
        
        """
        This function tests the downsample function. It compares the 
        output function with the expected simulated data given below. 
        """
        # expected data given the transformations above.
        expected_daily_data = {
            "times": ["2014-05-06 04:10:00", "2014-05-06 04:20:00"],
            "AirTemp": [44, 32],
            "Units" : ["F", "F"],
        }
        expected_daily_data["times"] = pd.Series(expected_daily_data["times"])
        expected_daily_data = pd.DataFrame(expected_daily_data)

        self.oldtransformer.format_pivot("TREC_Tower", "AirTemp_F")
        path = "../testdata/raw/ichart/pivot/TREC_Tower"
        self.assertTrue(os.path.exists(os.path.join(path, "AirTemp_pivot.csv")))
        df = pd.read_csv(os.path.join(path, "AirTemp_pivot.csv"))
        self.assertTrue(df["times"].equals(expected_daily_data["times"]),
                        "times are not equal")
        self.assertTrue(df["AirTemp"].equals(expected_daily_data["AirTemp"]),
                        "AirTemp are not equal")
        self.assertTrue(df["Units"].equals(expected_daily_data["Units"]),
                        "units are not equal")
        

if __name__ == '__main__':
    unittest.main()
