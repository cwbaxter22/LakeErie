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


class TestCreateTrendline(unittest.TestCase):
    """Test cases for create_trendline function
    which uses pytimetk to create a trendline of 
    time series data"""

    def test_valid_data(self):
        """Test with valid data, expecting no errors"""
        data = pd.DataFrame({'times': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03']),
                             'value_mean': [10, 20, 30]})
        result = anomaly_mod.create_trendline(data)
        self.assertIsInstance(result)

    