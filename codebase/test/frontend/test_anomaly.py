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



###### 
### Tests for Anomaly Calculation Function
##########


class TestCreateAnomalyGraph(unittest.TestCase):
    """Test cases for create_anomaly_graph function, which runs time series statistics
    on selected database and creates a graph with anomaly bands and a clear notation of anomalies in red"""

    # Test to make sure it works with a valid dataset
    def test_valid_data(self):
        """Test with valid data, expecting no errors"""
        data = pd.DataFrame({
            'times': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05', '2023-01-06', '2023-01-07', '2023-01-08']),
            'value_mean': [10, 20, 30, 40, 35, 25, 15, 22]
        })
        result = anomaly_mod.create_anomaly_graph(data)
        self.assertIsNotNone(result)

    # Test to make sure data is longer than the selected period value
    def test_short_data_raises_value_error(self):
        """Test ValueError is raised when the DataFrame is shorter than the specified period"""
        short_data = pd.DataFrame({
            'times': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03']),
            'value_mean': [10, 20, 30]
        })

        with self.assertRaises(ValueError) as context:
            anomaly_mod.create_anomaly_graph(short_data, period=5)

        expected_error_message = "Data must be longer than the selected Period value."
        self.assertEqual(str(context.exception), expected_error_message)

    #Test to make sure that the data is a pandas dataframe
    def test_non_dataframe_raises_type_error(self):
        """Test TypeError is raised when data is not a pandas DataFrame"""
        non_dataframe = "This is not a DataFrame"

        with self.assertRaises(TypeError):
            anomaly_mod.create_anomaly_graph(non_dataframe)

    # Test to make sure a TypeError is raised when times is not a datetime object
    def test_non_datetime_column(self):
        """Test TypeError is raised when 'times' column is not a datetime object"""
        data = pd.DataFrame({
            'times': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05', '2023-01-06', '2023-01-07', '2023-01-08'],
            'value_mean': [1, 2, 3, 4, 5, 6, 7, 8]
        })
        with self.assertRaises(TypeError):
            anomaly_mod.create_anomaly_graph(data)

    #Test to make sure anom_plot is actually created 
    def test_anom_plot_created(self):
        # Test to ensure anom_plot is created
        data = pd.DataFrame({
            'times': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05', '2023-01-06', '2023-01-07', '2023-01-08']),
            'value_mean': [10, 20, 30, 40, 35, 25, 15, 22]
        })
        anom_plot = anomaly_mod.create_anomaly_graph(data)

        # Check if anom_plot is not None
        self.assertIsNotNone(anom_plot)

    #Test to make sure clean_alpha is a non-zero numeric value
    def test_invalid_clean_alpha_raises_value_error(self):
        """Test ValueError is raised when clean_alpha is non-numeric or zero"""
        data = pd.DataFrame({
            'times': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05', '2023-01-06', '2023-01-07', '2023-01-08']),
            'value_mean': [10, 20, 30, 40, 35, 25, 15, 22]
        })

        with self.assertRaises(ValueError) as context:
            anomaly_mod.create_anomaly_graph(data, clean_alpha=0)

        expected_error_message = "clean_alpha must be a non-zero numeric value."
        self.assertEqual(str(context.exception), expected_error_message)

    # Test to make sure period is a non-zero numeric value
    def test_invalid_period_raises_value_error(self):
        """Test ValueError is raised when period is non-numeric or zero"""
        data = pd.DataFrame({
            'times': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05', '2023-01-06', '2023-01-07', '2023-01-08']),
            'value_mean': [10, 20, 30, 40, 35, 25, 15, 22]
        })

        with self.assertRaises(ValueError) as context:
            anomaly_mod.create_anomaly_graph(data, period=0)

        expected_error_message = "Period must be a non-zero numeric value."
        self.assertEqual(str(context.exception), expected_error_message)

    # Test to make sure clean_alpha is a non-zero numeric value
    def test_invalid_clean_alpha_raises_value_error(self):
        """Test ValueError is raised when clean_alpha is non-numeric or zero"""
        data = pd.DataFrame({
            'times': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05', '2023-01-06', '2023-01-07', '2023-01-08']),
            'value_mean': [10, 20, 30, 40, 35, 25, 15, 22]
        })

        with self.assertRaises(ValueError) as context:
            anomaly_mod.create_anomaly_graph(data, clean_alpha=0)

        expected_error_message = "clean_alpha must be a non-zero numeric value."
        self.assertEqual(str(context.exception), expected_error_message)


###### 
### Tests for Anomaly decomposition Function
##########
    

class TestAnomalyDecomp(unittest.TestCase):
    """Test cases for anomaly_decomp function"""

    # Test with valid data, expecting no errors
    def test_valid_data(self):
        data = pd.DataFrame({
            'times': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05', '2023-01-06', '2023-01-07', '2023-01-08']),
            'value_mean': [10, 20, 30, 40, 35, 25, 15, 22]
        })
        result = anomaly_mod.anomaly_decomp(data)
        self.assertIsNotNone(result)

    # Test TypeError is raised when data is not a pandas DataFrame
    def test_non_dataframe_raises_type_error(self):
        non_dataframe = "This is not a DataFrame"

        with self.assertRaises(TypeError):
            anomaly_mod.anomaly_decomp(non_dataframe)

    # Test TypeError is raised when 'times' column is not a datetime object
    def test_non_datetime_column(self):
        data = pd.DataFrame({
            'times': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05', '2023-01-06', '2023-01-07', '2023-01-08'],
            'value_mean': [1, 2, 3, 4, 5, 6, 7, 8]
        })
        with self.assertRaises(TypeError) as context:
            anomaly_mod.anomaly_decomp(data)

        expected_error_message = "The 'times' column must be of datetime type."
        self.assertEqual(str(context.exception), expected_error_message)

    # Test to ensure decomp is created
    def test_decomp_created(self):
        data = pd.DataFrame({
            'times': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05', '2023-01-06', '2023-01-07', '2023-01-08']),
            'value_mean': [10, 20, 30, 40, 35, 25, 15, 22]
        })
        decomp = anomaly_mod.anomaly_decomp(data)

        # Check if decomp is not None
        self.assertIsNotNone(decomp)

    # Test ValueError is raised when clean_alpha is non-numeric or zero
    def test_invalid_clean_alpha_raises_value_error(self):
        data = pd.DataFrame({
            'times': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05', '2023-01-06', '2023-01-07', '2023-01-08']),
            'value_mean': [10, 20, 30, 40, 35, 25, 15, 22]
        })

        with self.assertRaises(ValueError) as context:
            anomaly_mod.anomaly_decomp(data, clean_alpha=0)

        expected_error_message = "clean_alpha must be a non-zero numeric value."
        self.assertEqual(str(context.exception), expected_error_message)

    # Test ValueError is raised when period is non-numeric or zero
    def test_invalid_period_raises_value_error(self):
        data = pd.DataFrame({
            'times': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05', '2023-01-06', '2023-01-07', '2023-01-08']),
            'value_mean': [10, 20, 30, 40, 35, 25, 15, 22]
        })

        with self.assertRaises(ValueError) as context:
            anomaly_mod.anomaly_decomp(data, period=0)

        expected_error_message = "Period must be a non-zero numeric value."
        self.assertEqual(str(context.exception), expected_error_message)

    # Test ValueError is raised when clean_alpha is non-numeric or zero
    def test_invalid_clean_alpha_raises_value_error(self):
        data = pd.DataFrame({
            'times': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05', '2023-01-06', '2023-01-07', '2023-01-08']),
            'value_mean': [10, 20, 30, 40, 35, 25, 15, 22]
        })

        with self.assertRaises(ValueError) as context:
            anomaly_mod.anomaly_decomp(data, clean_alpha=0)

        expected_error_message = "clean_alpha must be a non-zero numeric value."
        self.assertEqual(str(context.exception), expected_error_message)