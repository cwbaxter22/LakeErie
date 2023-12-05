import unittest
import sys
import os
import pandas as pd
import numpy as np

sys.path.append("../../src/backend")
from data_transformer import DataTransformer






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



    # # test to make sure that the file path of <raw>/<project> exists and contains a directory for each device
    # def test_raw_project_path(self):
    #     raw_project_path = '<raw>/<project>'  # Replace with your actual path

    #     # Check if the <raw>/<project> path exists
    #     self.assertTrue(os.path.exists(raw_project_path), f"Path '{raw_project_path}' does not exist.")

    #     # List all subdirectories in <raw>/<project>
    #     device_directories = [d for d in os.listdir(raw_project_path) if os.path.isdir(os.path.join(raw_project_path, d))]

    #     # Replace 'device1', 'device2', etc. with the actual device names you expect
    #     expected_devices = ['device1', 'device2', 'device3']

    #     # Check if directories for each device exist
    #     for device in expected_devices:
    #        for device in expected_devices:
    #         device_path = os.path.join(raw_project_path, device)
    #         self.assertIn(device, device_directories, f"Directory for device '{device}' does not exist.")

    #         # Check if the device directory contains CSV files
    #         csv_files = [f for f in os.listdir(device_path) if f.lower().endswith('.csv')]
    #         self.assertTrue(csv_files, f"No CSV files found in directory '{device_path}' for device '{device}'.")


        
    
    # # test to make sure that function: across_parameter_aggregate can read in a csv
    # def test_across_parameter_aggregate_reads_csv(self):
    #     # Replace with the actual path to your test CSV file
    #     test_csv_path = 'path/to/test.csv'

    #     # Call the function and check if it reads the CSV successfully
    #     result_df = across_parameter_aggregate(test_csv_path)

    #     # Assertions
    #     self.assertIsNotNone(result_df, f"Failed to read CSV from '{test_csv_path}'.")
    #     self.assertIsInstance(result_df, pd.DataFrame, "Result is not a DataFrame.")
    #     self.assertFalse(result_df.empty, "DataFrame is empty.")


    # # test to make sure that across_parameter_aggregate only merges files that follow the format: <parameter_name>.csv
    #    #for every file in the directory

    #       #if the filename exists more than 1 time
    #         #throw error saying only 1 file per parameter name is allowed
    # def check_duplicate_files(directory):
    #     file_count = {}
    #     duplicate_files = []

    #     # Iterate over all files in the directory
    #     for filename in os.listdir(directory):
    #         filepath = os.path.join(directory, filename)

    #         # Check if it is a file
    #         if os.path.isfile(filepath):
    #             # Extract parameter name from the file name
    #             parameter_name = filename.split('.')[0]

    #             # Count occurrences of each parameter name
    #             file_count[parameter_name] = file_count.get(parameter_name, 0) + 1

    #             # If a parameter name is repeated, add it to the list of duplicates
    #             if file_count[parameter_name] > 1 and parameter_name not in duplicate_files:
    #                 duplicate_files.append(parameter_name)

    #     return duplicate_files
    
    # def test_check_duplicate_files(self):
    #     # Replace with the actual path to your test directory
    #     test_directory = 'path/to/test_directory'

    #     # Call the function to check for duplicate files
    #     duplicates = check_duplicate_files(test_directory)

    #     # Assertions
    #     self.assertFalse(duplicates, f"Duplicate files found: {duplicates}")


    # # test to make sure that across_parameter_aggregate can merge two csv files
    # expected_columns = ['common_column', 'value1', 'value2']
    #     self.assertIsNotNone(merged_df, "Failed to merge CSV files.")
    #     self.assertIsInstance(merged_df, pd.DataFrame, "Result is not a DataFrame.")
    #     self.assertListEqual(list(merged_df.columns), expected_columns, "Unexpected columns in merged DataFrame.")
    #     self.assertEqual(len(merged_df), 2, "Unexpected number of rows in merged DataFrame.")


    # # test to make sure that the directory <processed> exists
    # def test_processed_directory_exists(self):
    #     processed_directory = '<processed>'
    #     self.assertTrue(os.path.exists(processed_directory), f"Path '{processed_directory}' does not exist.")

    # # test to make sure that the directory <processed>/<project> exists
    # def test_processed_project_directory_exists(self):
    #     processed_project_directory = '<processed>/<project>'
    #     self.assertTrue(os.path.exists(processed_project_directory), f"Path '{processed_project_directory}' does not exist.")

    # # test to make sure that the directory <processed>/<project>/<device_name> exists
    # def test_processed_device_directory_exists(self):
    #     processed_device_directory = '<processed>/<project>/<device_name>'
    #     self.assertTrue(os.path.exists(processed_device_directory), f"Path '{processed_device_directory}' does not exist.")

    # # test to make sure that across_parameter_aggregate can write a csv file
    # def test_across_parameter_aggregate_writes_csv(self):
    #     # Replace with the actual path to your test CSV file
    #     test_csv_path = 'path/to/test.csv'

    #     # Call the function and check if it writes the CSV successfully
    #     result_df = across_parameter_aggregate(test_csv_path)

    #     # Replace with the actual path to your test output CSV file
    #     test_output_csv_path = 'path/to/test_output.csv'

    #     # Write the DataFrame to a CSV file
    #     result_df.to_csv(test_output_csv_path, index=False)

    #     # Check if the CSV file was written successfully
    #     self.assertTrue(os.path.exists(test_output_csv_path), f"Failed to write CSV to '{test_output_csv_path}'.")

    # # test to make sure that that csv file is named all_data.csv
    # def test_across_parameter_aggregate_writes_csv_with_correct_name(self):
    #     # Replace with the actual path to your test CSV file
    #     test_csv_path = 'path/to/test.csv'

    #     # Call the function and check if it writes the CSV successfully
    #     result_df = across_parameter_aggregate(test_csv_path)

    #     # Replace with the actual path to your test output CSV file
    #     test_output_csv_path = 'path/to/test_output.csv'

    #     # Write the DataFrame to a CSV file
    #     result_df.to_csv(test_output_csv_path, index=False)

    #     # Check if the CSV file was written successfully
    #     self.assertTrue(os.path.exists(test_output_csv_path), f"Failed to write CSV to '{test_output_csv_path}'.")

    #     # Check if the CSV file has the correct name
    #     self.assertEqual(os.path.basename(test_output_csv_path), 'all_data.csv', "CSV file has incorrect name.")

    # # test to make sure that the csv file is written to the correct directory
    # def test_across_parameter_aggregate_writes_csv_to_correct_directory(self):
    #     # Replace with the actual path to your test CSV file
    #     test_csv_path = 'path/to/test.csv'

    #     # Call the function and check if it writes the CSV successfully
    #     result_df = across_parameter_aggregate(test_csv_path)

    #     # Replace with the actual path to your test output CSV file
    #     test_output_csv_path = 'path/to/test_output.csv'

    #     # Write the DataFrame to a CSV file
    #     result_df.to_csv(test_output_csv_path, index=False)

    #     # Check if the CSV file was written successfully
    #     self.assertTrue(os.path.exists(test_output_csv_path), f"Failed to write CSV to '{test_output_csv_path}'.")

    #     # Check if the CSV file was written to the correct directory
    #     self.assertEqual(os.path.dirname(test_output_csv_path), '<processed>/<project>/<device_name>', "CSV file was not written to the correct directory.")
    # # test to make sure that the csv file data follows the format times, parameter, value, units
    # def test_across_parameter_aggregate_writes_csv_with_correct_columns(self):
    #     # Replace with the actual path to your test CSV file
    #     test_csv_path = 'path/to/test.csv'

    #     # Call the function and check if it writes the CSV successfully
    #     result_df = across_parameter_aggregate(test_csv_path)

    #     # Replace with the actual path to your test output CSV file
    #     test_output_csv_path = 'path/to/test_output.csv'

    #     # Write the DataFrame to a CSV file
    #     result_df.to_csv(test_output_csv_path, index=False)

    #     # Check if the CSV file was written successfully
    #     self.assertTrue(os.path.exists(test_output_csv_path), f"Failed to write CSV to '{test_output_csv_path}'.")

    #     # Check if the CSV file has the correct columns
    #     expected_columns = ['times', 'parameter', 'value', 'units']
    #     self.assertListEqual(list(result_df.columns), expected_columns, "CSV file has incorrect columns.")



    # # test to make sure that device_aggregate runs for every device
    # def test_device_aggregate_runs_for_every_device(self):
    #     # Replace with the actual path to your test directory
    #     test_directory = 'path/to/test_directory'
            
    #         # Call the function to check for duplicate files
    #         duplicates = check_duplicate_files(test_directory)
    
    #         # Assertions
    #         self.assertFalse(duplicates, f"Duplicate files found: {duplicates}")



    # # test to make sure that tidy_data_transform can read in a csv
    # def test_tidy_data_transform_reads_csv(self):
    #     # Replace with the actual path to your test CSV file
    #     test_csv_path = 'path/to/test.csv'

    #     # Call the function and check if it reads the CSV successfully
    #     result_df = tidy_data_transform(test_csv_path)

    #     # Assertions
    #     self.assertIsNotNone(result_df, f"Failed to read CSV from '{test_csv_path}'.")
    #     self.assertIsInstance(result_df, pd.DataFrame, "Result is not a DataFrame.")
    #     self.assertFalse(result_df.empty, "DataFrame is empty.")
    # # test to make sure that tidy_data_transform can write a csv
    # def test_tidy_data_transform_writes_csv(self):
    #     # Replace with the actual path to your test CSV file
    #     test_csv_path = 'path/to/test.csv'

    #     # Call the function and check if it writes the CSV successfully
    #     result_df = tidy_data_transform(test_csv_path)

    #     # Replace with the actual path to your test output CSV file
    #     test_output_csv_path = 'path/to/test_output.csv'

    #     # Write the DataFrame to a CSV file
    #     result_df.to_csv(test_output_csv_path, index=False)

    #     # Check if the CSV file was written successfully
    #     self.assertTrue(os.path.exists(test_output_csv_path), f"Failed to write CSV to '{test_output_csv_path}'.")

    # # test to make sure that tidy_data_transform can write a csv to the correct directory
    # # test to make sure that tidy_data_transform can write a csv with the correct name
    # # test to make sure that tidy_data_transform can write a csv with the correct columns
    # # test to make sure that tidy_data_transform can write a csv with the correct data
    # # test to make sure that tidy_data_transform can write a csv with the correct data types
    # # test to make sure that tidy_data_transform can write a csv with the correct units
    # # test to make sure that tidy_data_transform can write a csv with the correct parameter name
    # # test to make sure that tidy_data_transform can write a csv with the correct times
    # # test to make sure that tidy_data_transform can write a csv with the correct values
    # # test to make sure that tidy_data_transform can write a csv with the correct device name
    # # test to make sure that tidy_data_transform can write a csv with the correct project name
    # # test to make sure that tidy_data_transform can write a csv with the correct device id

    # # test to make sure that tidy_devices runs for every device
    # # test to make sure that tidy_devices can read in a csv
    # # test to make sure that tidy_devices can call tidy_data_transform

    # # test to make sure that downsample_hour can aggregate data by hour
    # # test to make sure that downsample_hour can write a csv
    # # test to make sure that downsample_hour can write a csv to the correct directory
    # # test to make sure that downsample_hour can write a csv with the correct name
    # # test to make sure that downsample_hour can write a csv with the correct columns
    # # test to make sure that downsample_hour can write a csv with the correct data
    # # test to make sure that downsample_hour can write a csv with the correct data types

    # # test to make sure that downsample_day can aggregate data by day
    # # test to make sure that downsample_day can write a csv
    # # test to make sure that downsample_day can write a csv to the correct directory
    # # test to make sure that downsample_day can write a csv with the correct name
    # # test to make sure that downsample_day can write a csv with the correct columns
    # # test to make sure that downsample_day can write a csv with the correct data
    # # test to make sure that downsample_day can write a csv with the correct data types

    # # test to make sure that device_downsample_hour runs for every device
    # # test to make sure that device_downsample_hour can read in a csv
    # # test to make sure that device_downsample_hour can call downsample_hour

    # # test to make sure that device_downsample_day runs for every device
    # # test to make sure that device_downsample_day can read in a csv
    # # test to make sure that device_downsample_day can call downsample_day








    # def test_(self): 
    #     pass