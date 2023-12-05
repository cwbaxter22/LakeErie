import unittest
import sys
import os
import pandas as pd
import numpy as np

sys.path.append("../../src/backend")
from iChart6_data_transformer import OldDataTransformer






class TestDataTransformer(unittest.TestCase):
    
    #test to make sure that the function can call DataLoader.get_devices()
    #def test_get_devices(self):
        #self.assertEqual(dataTransformer.get_devices(), <list of devices - actual>, msg)
        #self.assertEqual(dataTransformer.get_devices(), None)

    def setUp(self) -> None:
        self.devices = ["TREC_Tower", "Beach2_Buoy"]
        self.project = ["new", "old", "iChart"]
        self.dataTransformer = DataTransformer()
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

        self.dataTransformer.set_path("../testdata/raw", "../testdata/processed")

    def tearDown(self) -> None:
        self.wipe_test_data()
        pass

    #remove all csv files in the directory
    def wipe_test_data(self):
        
        directories = [
            "../testdata/raw/new/TREC_Tower",
            "../testdata/raw/new/Beach2_Buoy",
            "../testdata/raw/old/TREC_Tower",
            "../testdata/raw/old/Beach2_Buoy",
            "../testdata/raw/iChart/TREC_Tower",
            "../testdata/raw/iChart/Beach2_Buoy",
            "../testdata/processed/new/TREC_Tower",
            "../testdata/processed/new/Beach2_Buoy",
            "../testdata/processed/old/TREC_Tower",
            "../testdata/processed/old/Beach2_Buoy",
            "../testdata/processed/iChart/TREC_Tower",
            "../testdata/processed/iChart/Beach2_Buoy"
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
        """
        data = {
            "times": [
                "1/1/2018 13:10",
                "1/1/2018 13:20",
                "1/1/2018 13:30",
                "1/1/2018 13:10",
                "1/1/2018 13:20",
                "1/1/2018 13:30"
                ],
            "ODO": [10.1, 9.2, 10.4, np.nan, np.nan, np.nan],
            "Units": ["mg/L", "mg/L", "mg/L", "F", "F", "F"],
            "Air_Temperature": [np.nan, np.nan, np.nan, 42.1, 42.9, 42.2],
        }
        
        data["times"] = pd.Series(data["times"])
        df = pd.DataFrame(data)
        df.to_csv(f"{test_csv_path}/all_data.csv", index=False)

    def create_tidy_all_data_csv(self, test_csv_path: str) -> None:
        data = {
            "times": ["1/1/2018 13:10", "1/1/2018 13:10", "1/1/2018 13:20", "1/1/2018 13:20", "1/1/2018 13:30", "1/1/2018 13:30"],
            "Units": ["mg/L", "F", "mg/L", "F", "mg/L", "F"],
            "parameter": ["ODO", "Air_Temperature", "ODO", "Air_Temperature", "ODO", "Air_Temperature"],
            "value": [10.1, 42.1, 9.2, 42.9, 10.4, 42.2]
        }
        data["times"] = pd.to_datetime(data["times"])
        data["times"] = pd.Series(data["times"])
        data = pd.DataFrame(data)
        data.to_csv(f"{test_csv_path}/tidy_all_data.csv", index=False)


    #smoke test
    def test_across_parameter_aggregate(self):
        expected_columns = ['times', 'ODO', 'Units', 'Air_Temperature']
        expected_data = {
            "times": ["1/1/2018 13:10", "1/1/2018 13:20", "1/1/2018 13:30", "1/1/2018 13:10", "1/1/2018 13:20", "1/1/2018 13:30"],
            "ODO": [10.1, 9.2, 10.4, np.nan, np.nan, np.nan],
            "Units": ["mg/L", "mg/L", "mg/L", "F", "F", "F"],
            "Air_Temperature": [np.nan, np.nan, np.nan, 42.1, 42.9, 42.2],
        }
        expected_data["times"] = pd.Series(expected_data["times"])
        expected_data = pd.DataFrame(expected_data)

        for project in self.project:
            for device in self.devices:
                self.dataTransformer.across_parameter_aggregate(device, project)
                self.assertTrue(os.path.exists(f"../testdata/processed/{project}/{device}/all_data.csv"))
                df = pd.read_csv(f"../testdata/processed/{project}/{device}/all_data.csv")
                self.assertListEqual(list(df.columns), expected_columns)
                self.assertTrue(df.equals(expected_data), "dataframes are not equal")


    def test_tidy_data_transform(self):
        expected_data = {
            "times": ["1/1/2018 13:10", "1/1/2018 13:10", "1/1/2018 13:20", "1/1/2018 13:20", "1/1/2018 13:30", "1/1/2018 13:30"],
            "Units": ["mg/L", "F", "mg/L", "F", "mg/L", "F"],
            "parameter": ["ODO", "Air_Temperature", "ODO", "Air_Temperature", "ODO", "Air_Temperature"],
            "value": [10.1, 42.1, 9.2, 42.9, 10.4, 42.2]
        }
        expected_data["times"] = pd.to_datetime(expected_data["times"])
        expected_data["times"] = pd.Series(expected_data["times"])
        expected_data = pd.DataFrame(expected_data)


        for project in self.project:
            for device in self.devices:
                self.create_all_data_csv(f"../testdata/processed/{project}/{device}")
                self.dataTransformer.tidy_data_transform(pd.read_csv(f"../testdata/processed/{project}/{device}/all_data.csv"), device, project)
                self.assertTrue(os.path.exists(f"../testdata/processed/{project}/{device}/tidy_all_data.csv"))
                df = pd.read_csv(f"../testdata/processed/{project}/{device}/tidy_all_data.csv")
                df["times"] = pd.to_datetime(df["times"])
                self.assertTrue(df.equals(expected_data), "dataframes are not equal")


    def test_downsample_hour(self):

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
                self.create_tidy_all_data_csv(f"../testdata/processed/{project}/{device}")
                self.dataTransformer.downsample_hour(pd.read_csv(f"../testdata/processed/{project}/{device}/tidy_all_data.csv"), device, project)
                self.assertTrue(os.path.exists(f"../testdata/processed/{project}/{device}/hourly_tidy_all_data.csv"))
                df = pd.read_csv(f"../testdata/processed/{project}/{device}/hourly_tidy_all_data.csv")
                df["times"] = pd.to_datetime(df["times"])
                self.assertTrue(df["times"].equals(expected_data["times"]), "times are not equal")
                self.assertTrue(df["parameter"].equals(expected_data["parameter"]), "parameters are not equal")
                self.assertTrue(df["Units"].equals(expected_data["Units"]), "units are not equal")
                self.assertTrue(df["value_mean"].equals(expected_data["value_mean"]), "value_means are not equal")
                std_Check = np.isclose(df["value_std"],expected_data["value_std"])
                for truth in std_Check:
                    self.assertTrue(truth, "value_stds are not equal")


    def test_downsample_day(self):

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
                self.create_tidy_all_data_csv(f"../testdata/processed/{project}/{device}")
                self.dataTransformer.downsample_day(pd.read_csv(f"../testdata/processed/{project}/{device}/tidy_all_data.csv"), device, project)
                self.assertTrue(os.path.exists(f"../testdata/processed/{project}/{device}/daily_tidy_all_data.csv"))
                df = pd.read_csv(f"../testdata/processed/{project}/{device}/daily_tidy_all_data.csv")
                df["times"] = pd.to_datetime(df["times"])
                self.assertTrue(df["times"].equals(expected_data["times"]), "times are not equal")
                self.assertTrue(df["parameter"].equals(expected_data["parameter"]), "parameters are not equal")
                self.assertTrue(df["Units"].equals(expected_data["Units"]), "units are not equal")
                self.assertTrue(df["value_mean"].equals(expected_data["value_mean"]), "value_means are not equal")
                std_Check = np.isclose(df["value_std"],expected_data["value_std"])
                for truth in std_Check:
                    self.assertTrue(truth, "value_stds are not equal")



if __name__ == '__main__':
    unittest.main()