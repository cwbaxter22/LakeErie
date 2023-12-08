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
        #self.assertIsInstance(result, plt.Figure)

    def test_columns_missing(self):
        """Test to make sure both 'times' and 'value_mean' columns are present,
        expecting ValueError if either is not present"""
        data = pd.DataFrame({'value_mean': [10, 20, 30]})
        with self.assertRaises(ValueError):
            anomaly_mod.create_trendline(data)

    def test_valid_data_amount(self):
        """Test to make sure each column has at least 3 non-0 or non-NA values,
        expecting ValueError if either is not present"""
        data = pd.DataFrame({'times': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03']),
                             'value_mean': [10, 'NA', 30]})
        with self.assertRaises(ValueError):
            anomaly_mod.create_trendline(data)

    def test_time_datatype(self):
        """Test to make sure 'times' column is a datetime object,
        expecting ValueError if not"""
        data = pd.DataFrame({'times': ['2023-01-01', '2023-01-02', '2023-01-03'],
                             'value_mean': [10, 20, 30]})
        with self.assertRaises(ValueError):
            anomaly_mod.create_trendline(data)

class TestCreateAnomalyGraphFunction(unittest.TestCase):
    """Test cases for create_anomaly_graph function, which brings in data, removes NA values, creates a 
    dataframe of values calculating from the anomaly calculation"""

    def test_valid_data(self):
        """One shot test which brings in valid data, expecting no errors"""
        data = pd.DataFrame({'times': pd.date_range('2023-01-01', period=10),
                             'value_mean': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]})
        result = anomaly_mod.create_anomaly_graph(data)
        # Check if result is as expected (depends on the plotting engine used)

    def test_nonzero_testvalues(self):
        """Test to make sure 'iqr_alpha' and 'clean_alpha' are not specified as 0 values,
        expecting ValueError if not"""
        data = pd.DataFrame({'times': pd.date_range('2023-01-01', period=5),
                             'value_mean': [10, 20, 30, 40, 50]})
        with self.assertRaises(ValueError):
            anomaly_mod.create_anomaly_graph(data, iqr_alpha=0, clean_alpha=0)

    def test_numeric_in_data(self):
        """Test to make sure data after NA's are removed does not have any non-numeric values,
        expecting ValueError if not"""
        data = pd.DataFrame({'times': pd.date_range('2023-01-01', periods=5),
                             'value_mean': [10, 20, None, 40, 'string']})
        with self.assertRaises(ValueError):
            anomaly_mod.create_anomaly_graph(data)

    def test_anomaly_df_is_created(self):
        """Test to make sure Anomaly df has a non-zero value"""
        data = pd.DataFrame({'times': pd.date_range('2023-01-01', periods=5),
                             'value_mean': [10, 20, 30, 40, 50]})
        result = anomaly_mod.create_anomaly_graph(data)
        # Check if the anomaly DataFrame is created and has non-zero values

    def test_plotly_graph_is_created(self):
        """Test to make sure plotly graph is created,
        expecting ValueError if not"""
        data = pd.DataFrame({'times': pd.date_range('2023-01-01', periods=5),
                             'value_mean': [10, 20, 30, 40, 50]})
        with self.assertRaises(ValueError):
            anomaly_mod.create_anomaly_graph(data, engine='invalid_engine')

class TestAnomalyDecompFunction(unittest.TestCase):
    """Test cases for anomaly_decomp function, which provides graphs of statistical decomposition
    of anomaly calculation, including __________"""

    def test_valid_data(self):
        """One shot test which brings in valid data, expecting no errors"""
        data = pd.DataFrame({'times': pd.date_range('2023-01-01', period=10),
                             'value_mean': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]})
        result = anomaly_mod.anomaly_decomp(data)
        # Check if result is as expected (depends on the plotting engine used)

    def test_nonzero_testvalues(self):
        """Test to make sure 'iqr_alpha' and 'clean_alpha' are not specified as 0 values,
        expecting ValueError if not"""
        data = pd.DataFrame({'times': pd.date_range('2023-01-01', period=5),
                             'value_mean': [10, 20, 30, 40, 50]})
        with self.assertRaises(ValueError):
            anomaly_mod.anomaly_decomp(data, iqr_alpha=0, clean_alpha=0)

    def test_numeric_in_data(self):
        """Test to make sure data after NA's are removed does not have any non-numeric values,
        expecting ValueError if not"""
        data = pd.DataFrame({'times': pd.date_range('2023-01-01', period=5),
                             'value_mean': [10, 20, None, 40, 'string']})
        with self.assertRaises(ValueError):
            anomaly_mod.anomaly_decomp(data)

    def test_anomaly_df_is_created(self):
        """Test to make sure Anomaly df has a non-zero value"""
        data = pd.DataFrame({'times': pd.date_range('2023-01-01', period=5),
                             'value_mean': [10, 20, 30, 40, 50]})
        result = anomaly_mod.anomaly_decomp(data)
        # Check if the anomaly DataFrame is created and has non-zero values

