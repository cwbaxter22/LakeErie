"""
Docstring
"""

import os
import sys
import unittest

import numpy as np
import pandas as pd

sys.path.append("../../src/backend")
from data_transformer import DataTransformer


class TestDataTransformer(unittest.TestCase):
    """
    Test Class for DataTransformer and each of the following functions:
    1) across_parameter_aggregate
    2) tidy_data_transform
    3) downsample_hour
    4) downsample_day

    """

    def setUp(self) -> None:
        """
        This function creates a test directory with the following structure:
        testdata
        ├── processed
        │   ├── new
        │   │   ├── Beach2_Buoy
        │   │   │   ├── Air_Temperature.csv
        │   │   │   └── ODO.csv
        │   │   └── TREC_Tower
        │   │       ├── Air_Temperature.csv
        │   │       └── ODO.csv
        │   ├── old
        │   │   ├── Beach2_Buoy
        │   │   │   ├── Air_Temperature.csv
        │   │   │   └── ODO.csv
        │   │   └── TREC_Tower
        │   │       ├── Air_Temperature.csv
        │   │       └── ODO.csv
        │   └── ichart
        │       ├── Beach2_Buoy
        │       │   ├── Air_Temperature.csv
        │       │   └── ODO.csv
        │       └── TREC_Tower
        │           ├── Air_Temperature.csv
        │           └── ODO.csv
        └── raw
            ├── new
            │   ├── Beach2_Buoy
            │   │   ├── Air_Temperature.csv
            │   │   └── ODO.csv
            │   └── TREC_Tower
            │       ├── Air_Temperature.csv
            │       └── ODO.csv
            ├── old
            │   ├── Beach2_Buoy
            │   │   ├── Air_Temperature.csv
            │   │   └── ODO.csv
            │   └── TREC_Tower
            │       ├── Air_Temperature.csv
            │       └── ODO.csv
            └── ichart
                ├── Beach2_Buoy
                │   ├── Air_Temperature.csv
                │   └── ODO.csv
                └── TREC_Tower
                    ├── Air_Temperature.csv
                    └── ODO.csv
        
        We do this to create all of the files that we would have in the real directory.

        """
        self.devices = ["TREC_Tower", "Beach2_Buoy"]
        self.project = ["new", "old", "ichart"]
        self.data_transformer = DataTransformer()
        for project in self.project:
            if not os.path.exists(f"../testdata/raw/{project}"):
                os.makedirs(f"../testdata/raw/{project}")
            if not os.path.exists(f"../testdata/processed/{project}"):
                os.makedirs(f"../testdata/processed/{project}")

            for device in self.devices:
                if not os.path.exists(f"../testdata/raw/{project}/{device}"):
                    os.makedirs(f"../testdata/raw/{project}/{device}")
                self.create_raw_test_csv(f"../testdata/raw/{project}/{device}")
                if not os.path.exists(f"../testdata/processed/{project}/{device}"):
                    os.makedirs(f"../testdata/processed/{project}/{device}")

        self.data_transformer.set_path("../testdata/raw", "../testdata/processed")

    def tearDown(self) -> None:
        """
        This function calls wipe_test_data which will delete the test directory created in setUp
        
        """
        self.wipe_test_data()

    #remove all csv files in the directory
    def wipe_test_data(self):
        """
        This function deletes all of the csv files in the test directory
        """

        directories = [
            "../testdata/raw/new/TREC_Tower",
            "../testdata/raw/new/Beach2_Buoy",
            "../testdata/raw/old/TREC_Tower",
            "../testdata/raw/old/Beach2_Buoy",
            "../testdata/raw/ichart/TREC_Tower",
            "../testdata/raw/ichart/Beach2_Buoy",
            "../testdata/processed/new/TREC_Tower",
            "../testdata/processed/new/Beach2_Buoy",
            "../testdata/processed/old/TREC_Tower",
            "../testdata/processed/old/Beach2_Buoy",
            "../testdata/processed/ichart/TREC_Tower",
            "../testdata/processed/ichart/Beach2_Buoy"
            ]
        for directory in directories:
            for filename in os.listdir(directory):
                if filename.endswith(".csv"):
                    file_path = os.path.join(directory, filename)
                    os.remove(file_path)



    def create_raw_test_csv(self, test_csv_path: str) -> None:
        """
        Creates a test CSV file with the following columns:
        times, parameter1, parameter2, parameter3

        We can then use this to test the across_parameter_aggregate function.
        """

        data = {
            "times": ["1/1/2018 13:10", "1/1/2018 13:20", "1/1/2018 13:30"],
            "Air_Temperature": [42.1, 42.9, 42.2],
            "Units": ["F", "F", "F"],
        }
        df = pd.DataFrame(data)
        df.to_csv(f"{test_csv_path}/Air_Temperature.csv", index=False)

        data = {
            "times": ["1/1/2018 13:10", "1/1/2018 13:20", "1/1/2018 13:30"],
            "ODO": [10.1, 9.2, 10.4],
            "Units": ["mg/L", "mg/L", "mg/L"],
        }
        df = pd.DataFrame(data)
        df.to_csv(f"{test_csv_path}/ODO.csv", index=False)


    def create_all_data_csv(self, test_csv_path: str) -> None:
        """
        Creates a test CSV file with the following columns:
        times, ODO, Units, Air_Temperature

        This dataframe is the result of the across_parameter_aggregate function.
        We use this to test the tidy_data_transform function.

        """
        data = {
            "times": ["1/1/2018 13:10",
                      "1/1/2018 13:20",
                      "1/1/2018 13:30",
                      "1/1/2018 13:10",
                      "1/1/2018 13:20",
                      "1/1/2018 13:30"],
            "ODO": [10.1, 9.2, 10.4, np.nan, np.nan, np.nan],
            "Units": ["mg/L", "mg/L", "mg/L", "F", "F", "F"],
            "Air_Temperature": [np.nan, np.nan, np.nan, 42.1, 42.9, 42.2],
        }

        data["times"] = pd.Series(data["times"])
        df = pd.DataFrame(data)
        df.to_csv(f"{test_csv_path}/all_data.csv", index=False)

    def create_tidy_all_data_csv(self, test_csv_path: str) -> None:
        """
        Creates a test CSV file with the following columns:
        times, Units, parameter, value

        This dataframe is the output of the tidy_data_transform function.

        We use this to test the downsample_hour and downsample_day functions.
        
        """
        data = {
            "times": ["1/1/2018 13:10",
                      "1/1/2018 13:10",
                      "1/1/2018 13:20",
                      "1/1/2018 13:20",
                      "1/1/2018 13:30",
                      "1/1/2018 13:30"],
            "Units": ["mg/L", "F", "mg/L", "F", "mg/L", "F"],
            "parameter": ["ODO",
                          "Air_Temperature",
                          "ODO",
                          "Air_Temperature",
                          "ODO",
                          "Air_Temperature"],
            "value": [10.1, 42.1, 9.2, 42.9, 10.4, 42.2]
        }
        data["times"] = pd.to_datetime(data["times"])
        data["times"] = pd.Series(data["times"])
        data = pd.DataFrame(data)
        data.to_csv(f"{test_csv_path}/tidy_all_data.csv", index=False)


    def test_across_parameter_aggregate(self):
        """
        This function tests that the across_parameter_aggregate function in the DataTransformer
        class correctly merges the csv files in the raw directory and writes the result to the 
        processed directory.

        """


        expected_columns = ['times', 'ODO', 'Units', 'Air_Temperature']
        expected_data = {
            "times": ["1/1/2018 13:10",
                      "1/1/2018 13:20",
                      "1/1/2018 13:30",
                      "1/1/2018 13:10",
                      "1/1/2018 13:20",
                      "1/1/2018 13:30"],
            "ODO": [10.1, 9.2, 10.4, np.nan, np.nan, np.nan],
            "Units": ["mg/L", "mg/L", "mg/L", "F", "F", "F"],
            "Air_Temperature": [np.nan, np.nan, np.nan, 42.1, 42.9, 42.2],
        }
        expected_data["times"] = pd.Series(expected_data["times"])
        expected_data = pd.DataFrame(expected_data)

        for project in self.project:
            for device in self.devices:
                path = f"../testdata/processed/{project}/{device}"
                self.data_transformer.across_parameter_aggregate(device, project)
                self.assertTrue(os.path.exists(os.path.join(path, "all_data.csv")))
                df = pd.read_csv(os.path.join(path, "all_data.csv"))
                self.assertListEqual(list(df.columns), expected_columns)
                self.assertTrue(df.equals(expected_data), "dataframes are not equal")


    def test_tidy_data_transform(self):
        """
        This function tests that the tidy_data_transform function in the DataTransformer class
        correctly transforms the data from the across_parameter_aggregate function and writes 
        the result to the processed directory.
        """

        expected_data = {
            "times": ["1/1/2018 13:10",
                      "1/1/2018 13:10",
                      "1/1/2018 13:20",
                      "1/1/2018 13:20",
                      "1/1/2018 13:30",
                      "1/1/2018 13:30"],
            "Units": ["mg/L", "F", "mg/L", "F", "mg/L", "F"],
            "parameter": ["ODO",
                          "Air_Temperature",
                          "ODO",
                          "Air_Temperature",
                          "ODO",
                          "Air_Temperature"],
            "value": [10.1, 42.1, 9.2, 42.9, 10.4, 42.2]
        }
        expected_data["times"] = pd.to_datetime(expected_data["times"])
        expected_data["times"] = pd.Series(expected_data["times"])
        expected_data = pd.DataFrame(expected_data)


        for project in self.project:
            for device in self.devices:
                path = f"../testdata/processed/{project}/{device}"
                self.create_all_data_csv(path)
                self.data_transformer.tidy_data_transform(
                    pd.read_csv(os.path.join(path, "all_data.csv")),
                    device,
                    project)
                self.assertTrue(os.path.exists(
                    (os.path.join(path, "all_data.csv"))))
                df = pd.read_csv(os.path.join(path, "tidy_all_data.csv"))
                df["times"] = pd.to_datetime(df["times"])
                self.assertTrue(df.equals(expected_data), "dataframes are not equal")


    def test_downsample_hour(self):
        """
        This function tests that the downsample_hour function in the DataTransformer class
        correctly downsamples the data from the tidy_data_transform function and writes the 
        result to the processed directory.
        """

        expected_data = {
            "parameter": ["Air_Temperature", "ODO"],
            "Units": ["F", "mg/L"],
            "times": ["1/1/2018 13:00", "1/1/2018 13:00"],
            "value_mean": [42.4, 9.9],
            "value_std": [0.43589, 0.6245]
        }
        expected_data["times"] = pd.to_datetime(expected_data["times"])
        expected_data["times"] = pd.Series(expected_data["times"])
        expected_data = pd.DataFrame(expected_data)

        for project in self.project:
            for device in self.devices:
                path = f"../testdata/processed/{project}/{device}"
                self.create_tidy_all_data_csv(path)
                self.data_transformer.downsample_hour(
                    pd.read_csv(
                        os.path.join(path, "tidy_all_data.csv")),
                    device,
                    project)
                self.assertTrue(os.path.exists(
                    os.path.join(path, "hourly_tidy_all_data.csv")))
                df = pd.read_csv(os.path.join(path, "hourly_tidy_all_data.csv"))
                df["times"] = pd.to_datetime(df["times"])
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


    def test_downsample_day(self):
        """
        This function tests that the downsample_day function in the DataTransformer class
        correctly downsamples the data from the tidy_data_transform function and writes the 
        result to the processed directory.
        """

        expected_data = {
            "parameter": ["Air_Temperature", "ODO"],
            "Units": ["F", "mg/L"],
            "times": ["1/1/2018", "1/1/2018"],
            "value_mean": [42.4, 9.9],
            "value_std": [0.43589, 0.6245]
        }
        expected_data["times"] = pd.to_datetime(expected_data["times"])
        expected_data["times"] = pd.Series(expected_data["times"])
        expected_data = pd.DataFrame(expected_data)

        for project in self.project:
            for device in self.devices:
                path = f"../testdata/processed/{project}/{device}"
                self.create_tidy_all_data_csv(path)
                self.data_transformer.downsample_day(pd.read_csv(os.path.join(path,
                                                                             "tidy_all_data.csv")),
                                                                device,
                                                                project)
                self.assertTrue(os.path.exists(os.path.join(path, "daily_tidy_all_data.csv")))
                df = pd.read_csv(os.path.join(path, "daily_tidy_all_data.csv"))
                df["times"] = pd.to_datetime(df["times"])

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



if __name__ == '__main__':
    unittest.main()
