import unittest

import pandas as pd
from datetime import datetime

from anomaly.py import create_trendline  
from anomaly.py import create_anomaly_graph
from anomaly.py import create_anomaly_decomp_graph

### Test CreateTrendLine, which plots value vs time and fits a non-linear trendline from pytimetk

class TestCreateTrendline(unittest.TestCase):
    """
    Test cases for the create_trendline function.
    """

    def test_valid_data(self):
        """
        Test create_trendline with valid data.
        """
        data = pd.DataFrame({
            'times': [datetime(2023, 1, 1), datetime(2023, 1, 2)],
            'value_mean': [1, 2]
        })
        # This test should not raise any exceptions
        create_trendline(data)

    def test_missing_columns(self):
        """
        Test create_trendline with missing columns.
        """
        data = pd.DataFrame({'invalid_column': [1, 2]})
        # Expecting a ValueError to be raised since required columns are missing
        with self.assertRaises(ValueError):
            create_trendline(data)

    def test_invalid_datetime_column(self):
        """
        Test create_trendline with an invalid datetime column.
        """
        data = pd.DataFrame({
            'times': ['2023-01-01', '2023-01-02'],
            'value_mean': [1, 2]
        })
        # Expecting a ValueError to be raised since 'times' column is not a datetime object
        with self.assertRaises(ValueError):
            create_trendline(data)

    def test_empty_columns(self):
        """
        Test create_trendline with empty columns.
        """
        data = pd.DataFrame({'times': [], 'value_mean': []})
        # Expecting a ValueError to be raised since either 'times' or 'value_mean' column is empty
        with self.assertRaises(ValueError):
            create_trendline(data)

    def test_non_numeric_values(self):
        """
        Test create_trendline with non-numeric values.
        """
        data = pd.DataFrame({
            'times': [datetime(2023, 1, 1), datetime(2023, 1, 2)],
            'value_mean': [1, 'invalid']
        })
        # Expecting a ValueError to be raised since 'value_mean' column contains non-numeric values
        with self.assertRaises(ValueError):
            create_trendline(data)

    def test_single_row(self):
        """
        Test create_trendline with a DataFrame containing a single row.
        """
        data = pd.DataFrame({'times': [datetime(2023, 1, 1)], 'value_mean': [1]})
        # This test should not raise any exceptions
        create_trendline(data)

    def test_invalid_data_types(self):
        """
        Test create_trendline with valid columns but incorrect data types.
        """
        data = pd.DataFrame({
            'times': [datetime(2023, 1, 1), datetime(2023, 1, 2)],
            'value_mean': [1, 'invalid']
        })
        # Expecting a ValueError to be raised since 'value_mean' column contains non-numeric values
        with self.assertRaises(ValueError):
            create_trendline(data)

# Tests CreateAnomalyGraph, which runs statistical tests on time series data and plots time series 
    # with anomaly bars and points highlighted which are considered anomalies 

class TestCreateAnomalyGraph(unittest.TestCase):
    """
    Test cases for the create_anomaly_graph function.
    """

    def test_valid_data(self):
        """
        Test create_anomaly_graph with valid data.
        """
        data = pd.DataFrame({
            'times': [datetime(2023, 1, 1), datetime(2023, 1, 2)],
            'value_mean': [1, 2]
        })
        # This test should not raise any exceptions
        create_anomaly_graph(data)

    def test_missing_columns(self):
        """
        Test create_anomaly_graph with missing columns.
        """
        data = pd.DataFrame({'invalid_column': [1, 2]})
        # Expecting a ValueError to be raised since required columns are missing
        with self.assertRaises(ValueError):
            create_anomaly_graph(data)

    def test_invalid_datetime_column(self):
        """
        Test create_anomaly_graph with an invalid datetime column.
        """
        data = pd.DataFrame({
            'times': ['2023-01-01', '2023-01-02'],
            'value_mean': [1, 2]
        })
        # Expecting a ValueError to be raised since 'times' column is not a datetime object
        with self.assertRaises(ValueError):
            create_anomaly_graph(data)

    def test_empty_columns(self):
        """
        Test create_anomaly_graph with empty columns.
        """
        data = pd.DataFrame({'times': [], 'value_mean': []})
        # Expecting a ValueError to be raised since either 'times' or 'value_mean' column is empty
        with self.assertRaises(ValueError):
            create_anomaly_graph(data)

    def test_non_numeric_values(self):
        """
        Test create_anomaly_graph with non-numeric values.
        """
        data = pd.DataFrame({
            'times': [datetime(2023, 1, 1), datetime(2023, 1, 2)],
            'value_mean': [1, 'invalid']
        })
        # Expecting a ValueError to be raised since 'value_mean' column contains non-numeric values
        with self.assertRaises(ValueError):
            create_anomaly_graph(data)

    def test_edge_case_single_row(self):
        """
        Test create_anomaly_graph with a DataFrame containing a single row.
        """
        data = pd.DataFrame({'times': [datetime(2023, 1, 1)], 'value_mean': [1]})
        # This test should not raise any exceptions
        create_anomaly_graph(data)


##### Test AnomalyDecomp, which gives a look at the statistics underlying the anomaly detection

class TestAnomalyDecomp(unittest.TestCase):
    """
    Test cases for the anomaly_decomp function.
    """

    def test_valid_data(self):
        """
        Test anomaly_decomp with valid data.
        """
        data = pd.DataFrame({
            'times': [datetime(2023, 1, 1), datetime(2023, 1, 2)],
            'value_mean': [1, 2]
        })
        # This test should not raise any exceptions
        anomaly_decomp(data)

    def test_invalid_data_type(self):
        """
        Test anomaly_decomp with invalid data type.
        """
        data = "invalid_data_type"
        # Expecting a ValueError to be raised since 'data' argument must be a pandas DataFrame
        with self.assertRaises(ValueError):
            anomaly_decomp(data)

    def test_invalid_times_type(self):
        """
        Test anomaly_decomp with invalid 'times' argument type.
        """
        data = pd.DataFrame({'times': [datetime(2023, 1, 1)], 'value_mean': [1]})
        # Expecting a ValueError to be raised since 'times' argument must be a string
        with self.assertRaises(ValueError):
            anomaly_decomp(data, times=123)

    def test_invalid_value_mean_type(self):
        """
        Test anomaly_decomp with invalid 'value_mean' argument type.
        """
        data = pd.DataFrame({'times': [datetime(2023, 1, 1)], 'value_mean': [1]})
        # Expecting a ValueError to be raised since 'value_mean' argument must be a string
        with self.assertRaises(ValueError):
            anomaly_decomp(data, value_mean=123)

    def test_non_integer_period(self):
        """
        Test anomaly_decomp with non-integer 'period'.
        """
        data = pd.DataFrame({'times': [datetime(2023, 1, 1)], 'value_mean': [1]})
        # Expecting a ValueError to be raised since 'period' argument must be an integer
        with self.assertRaises(ValueError):
            anomaly_decomp(data, period=1.5)

    def test_non_float_iqr_alpha(self):
        """
        Test anomaly_decomp with non-float 'iqr_alpha'.
        """
        data = pd.DataFrame({'times': [datetime(2023, 1, 1)], 'value_mean': [1]})
        # Expecting a ValueError to be raised since 'iqr_alpha' argument must be a float
        with self.assertRaises(ValueError):
            anomaly_decomp(data, iqr_alpha='0.05')

    def test_non_float_clean_alpha(self):
        """
        Test anomaly_decomp with non-float 'clean_alpha'.
        """
        data = pd.DataFrame({'times': [datetime(2023, 1, 1)], 'value_mean': [1]})
        # Expecting a ValueError to be raised since 'clean_alpha' argument must be a float
        with self.assertRaises(ValueError):
            anomaly_decomp(data, clean_alpha='0.75')