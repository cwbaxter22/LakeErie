"""
This is the testing script for the data_loader.py file which contains the DataLoader class.
"""
from unittest.mock import patch
import unittest
import sys

sys.path.append("../../src/backend")
from data_loader import DataLoader


class TestDataLoader(unittest.TestCase):
    """
    Test Class for DataLoader and each of the following functions:
    1) api_call
    2) find_errors
    3) get_devices
    4) get_device_parameters
    5) get_data
    """

    @patch('data_loader.http.client.HTTPSConnection')
    @patch('data_loader.http.client.HTTPResponse')
    def test_api_call(self, mock_res, mock_conn):
        """
        This function tests that the api_call function in the DataLoader class 
        correctly calls the WQData API and returns the correct data.
        """
        mock_conn("www.wqdatalive.com").request.return_value = None
        mock_conn("www.wqdatalive.com").getresponse.return_value = mock_res
        mock_res.read.return_value = '{"devices": [{"id": "1234", "name": "test"}]}'.encode("utf-8")

        test_url = "/api/v1/devices?apiKey=1234"
        data = DataLoader(apiKey="1234", project="test").api_call(url=test_url)

        # Check that API is called with correct arguments
        mock_conn("www.wqdatalive.com").request.assert_called_with("GET", test_url)
        # Check that API response is parsed correctly
        self.assertEqual(data, {"devices": [{"id": "1234", "name": "test"}]})

    def test_find_errors(self):
        """
        This function tests that the find_errors function in the DataLoader class
        correctly parses the API response and checks for errors.
        """
        bad_data = {"message": "Request exceeds hourly limit"}
        # Check that function returns False if API quota has been reached
        self.assertFalse(DataLoader(apiKey="1234", project="test").find_errors(data=bad_data))
        # Check that function returns True if API response is valid
        good_data = {"devices": [{"id": "1234", "name": "test"}]}
        self.assertTrue(DataLoader(apiKey="1234", project="test").find_errors(data=good_data))

    @patch('data_loader.DataLoader.api_call', return_value={"devices": [{"id": "1234", "name": "test_device"}]})
    def test_get_devices(self, mock_api_call):
        """
        This function tests that the get_devices function in the DataLoader class
        correctly parses the API response and returns the correct devices.
        """
        data_loader = DataLoader(apiKey="1234", project="test")

        devices = data_loader.get_devices()
        # Verify that WQData API is only called once
        mock_api_call.assert_called_once()
        # Verify that data_loader correctly parses devices from API
        self.assertEqual(devices, {"test_device": "1234"})
        # Verify that devices as stored in data_loader
        self.assertEqual(data_loader.devices, {"test_device": "1234"})

    @patch('data_loader.DataLoader.api_call', return_value={"parameters": [{"id": "1234", "name": "Air Temperature", "unit": "test units"}]})
    @patch('data_loader.DataLoader.find_errors', return_value=True)
    def test_get_device_parameters(self, mock_find_errors, mock_api_call):
        """
        This function tests that the get_device_parameters function in the DataLoader class
        correctly parses the API response and returns the correct parameters for the device.
        """

        data_loader = DataLoader(apiKey="1234", project="test")
        parameters = data_loader.get_device_parameters(deviceId="1234")
        
        # Verify that WQData API is only called once
        mock_api_call.assert_called_once()
        # Verify that find_errors is only called once
        mock_find_errors.assert_called_once()
        # Verify that data_loader correctly parses parameters from API
        self.assertEqual(parameters, {"Air_Temperature": ("1234", "test units")})
        # Verify that parameters are stored in data_loader
        self.assertEqual(
            data_loader.device_parameters["1234"],
            {"Air_Temperature": ("1234", "test units")}
        )

    #@patch('data_loader.DataLoader.api_call', return_value={"data": [{"value": "1234", "timestamp": "2021-01-01T00:00:00.000Z"}]})
    #@patch('data_loader.DataLoader.find_errors', return_value=True)
    #def test_get_data(self, mock_find_errors, mock_api_call):
    #    """
    #    This functions thats the get_data function in the DataLoader class calls the WQData API
    #    with the correct arguments and returns the correct data.
        #"""
        #data_loader = DataLoader(apiKey="1234", project="test")
        #data = data_loader.get_data(
        #    deviceId="1234",
        #    parameterId="1234",
        #    start_date="2021-01-01",
        #    end_date="2021-01-02"
        #)

        # Verify that WQData API is only called once
        mock_api_call.assert_called_once()
        # Verify that find_errors is only called once
        mock_find_errors.assert_called_once()
        # Verify that data_loader correctly parses data from API and returns pandas dataFrame
        #self.assertEqual(data["values"], "1234")


# Execute Test Runner
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDataLoader)
    _ = unittest.TextTestRunner().run(suite)