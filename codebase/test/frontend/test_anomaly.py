import unittest
import importlib
import pathlib
import pandas as pd
from datetime import datetime
from matplotlib import pyplot as plt

codebase_path = pathlib.Path(__file__).parents[2]
#https://stackoverflow.com/questions/65206129/importlib-not-utilising-recognising-path
spec = importlib.util.spec_from_file_location(
    name='anomaly_mod',  # name is not related to the file, it's the module name!
    location= str(codebase_path) +
    "//src//frontend//anomaly.py"  # full path to the script
)
anomaly_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(anomaly_mod)

##########
### Tests for Create Trendline Function
########################


class TestCreateTrendline(unittest.TestCase):
    """Test cases for create_trendline function
    which uses pytimetk to create a trendline of 
    time series data"""

#### Test to make sure it works with a valid dataset
    def test_valid_data(self):
        """Test with valid data, expecting no errors"""
        data = pd.DataFrame({'times': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03']),
                             'value_mean': [10, 20, 30]})
        result = anomaly_mod.create_trendline(data)
        self.assertIsNotNone(result)

### Test to make sure the data is a pandas dataframe, if not raise a Typeerror
    def test_non_dataframe_input(self):
        """Test to ensure TypeError is raised for non-DataFrame input"""
        non_dataframe_input = "This is not a DataFrame"
        with self.assertRaises(TypeError):
            anomaly_mod.create_trendline(non_dataframe_input)

# Test to raise an error if the 'Times" column is missing 
    def test_missing_times_column(self):
        """Test ValueError is raised when 'times' column is missing"""
        data = pd.DataFrame({'value_mean': [10, 20, 30]})
        with self.assertRaises(ValueError):
            anomaly_mod.create_trendline(data)

#Test to raise an error if the 'value_mean' column is missing
    def test_missing_value_mean_column(self):
        """Test ValueError is raised when 'value_mean' column is missing"""
        data = pd.DataFrame({'times': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03'])})
        with self.assertRaises(ValueError):
            anomaly_mod.create_trendline(data)

#Test to make sure the 'times' column is a datetime object, if not raise a Typeerror
    def test_non_datetime_times_column(self):
        """Test TypeError is raised when 'times' column is not a datetime object"""
        data = pd.DataFrame({'times': ['2023-01-01', '2023-01-02', '2023-01-03'],
                             'value_mean': [10, 20, 30]})
        with self.assertRaises(TypeError):
            anomaly_mod.create_trendline(data)

    


    