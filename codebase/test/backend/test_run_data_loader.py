"""
This is the testing script for the run_data_loader.py file. The run_data_loader files uses the
DataLoader class to call the WQData API and save the data to the raw data directory from multiple
project sources (old and new). Note that run_data_loader has significant logic to handle the constraints
of the WQData API (e.g. hourly limit, data limit, etc.). 
"""
from unittest.mock import patch, MagicMock
import unittest
import pathlib
import importlib
import sys

codebase_path = pathlib.Path(__file__).parents[2]
#https://stackoverflow.com/questions/65206129/importlib-not-utilising-recognising-path
# Run data loader
spec = importlib.util.spec_from_file_location(
    name='run_data_loader_mod',  # name is not related to the file, it's the module name!
    location= str(codebase_path) +
    "//src//backend//run_data_loader.py"  # full path to the script
)

run_data_loader_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run_data_loader_mod)

# Config
spec2 = importlib.util.spec_from_file_location(
    name='config_combine_mod',  # name is not related to the file, it's the module name!
    location= str(codebase_path) +
    "//src//backend//config_combine.py"  # full path to the script
)

config_combine_mod = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(config_combine_mod)

sys.path.append("../../src/backend")
from run_data_loader_mod import (
    START_YEAR,
    CURRENT_YEAR,
    get_times,
    aggregate_data,
    ping_api,
)
from config_combine_mod import OLD_API_KEY, NEW_API_KEY


class TestRunnerDataLoader(unittest.TestCase):
    """
    Test functions in run_data_loader.py
    """

    def test_get_times(self):
        """
        This tests that get_times returns a list of strings 
        for each 1 month segment between START_YEAR and CURRENT_YEAR
        starting in 2014-05-01
        """
        times = get_times()
        self.assertEqual(times[0], f"{START_YEAR}-01-01")
        self.assertEqual(times[-1], f"{CURRENT_YEAR}-12-01")
        self.assertEqual(len(times), (CURRENT_YEAR - START_YEAR + 1) * 12)


    @patch("run_data_loader.time")
    @patch("run_data_loader.ping_api")
    @patch("run_data_loader.DataLoader")
    def test_aggregate_data(self, mock_data_loader, mock_ping_api, mock_time):
        """
        test 
        """
        mock_data_loader(apiKey="1234", project="old")
        mock_ping_api.return_value = True
        mock_time.sleep.return_value = None

        aggregate_data(old=True, project="old")

        self.assertEqual(mock_ping_api.call_count, 1)
        self.assertEqual(mock_time.sleep.call_count, 1)


    @patch("run_data_loader.os.path.exists", return_value=True)
    def test_ping_api(self, os_path_exists):
        """
        Test the ping_api function in run_data_loader.py
        """
        # Create mock data_loader object
        mock_data_loader = MagicMock()

        # Test first case: get_devices fails
        mock_data_loader.get_devices.return_value = None
        mock_data_loader.devices = None
        cur_status = ping_api(mock_data_loader)
        self.assertFalse(cur_status)

        # Test second case: get_devices succeeds, but all devices are processed
        mock_data_loader.devices = {"mock_name": "mock_id"}
        mock_data_loader.processed_devices = ["mock_name"]
        cur_status = ping_api(mock_data_loader)
        self.assertTrue(cur_status)

        # Test third case: parameters are not found for device from API
        mock_data_loader.devices = {"mock_name": "mock_id"}
        mock_data_loader.processed_devices = [] # No device has been processed yet
        mock_data_loader.device_parameters = {"mock_id": []}
        mock_data_loader.get_device_parameters.return_value = None
        cur_status = ping_api(mock_data_loader)
        self.assertFalse(cur_status)

        # Test fourth case: parameters are found for device from API
        mock_data_loader.get_device_parameters.return_value = {"mock_param": ("mock_id", "mock_unit")}
        mock_data_loader.processed_devices_parameters = {"mock_id": ["mock_param"]}
        cur_status = ping_api(mock_data_loader)
        self.assertTrue(cur_status)


# Execute Test Runner
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRunnerDataLoader)
    _ = unittest.TextTestRunner().run(suite)