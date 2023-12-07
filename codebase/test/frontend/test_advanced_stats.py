""" testing for advanced statistics page in the streamlit app"""


##############

class TestCreateTrendline(unittest.TestCase):

    """Test cases for create_trendline function
            which uses pytimetk to create a trendline of 
            time series data"""

    def test_valid_data(self)
        "one shot test which brings in valid data, expecting no errors"

    def test_collumns_missing(self)
        "test to make sure both times and value_mean collumns are present, expecting raisevalueerror if either are not present 

    def test_valid_data_amount(self)
        "test to make sure each collumn has at least 3 non 0 or non NA values, expecting raisevalueerror if either are not present
        
    def test_time_datatype(self)
        "test to make sure times collumn is a datetime object, expecting raisevalueerror if not


############## 

class TestCreateAnomlyGraph(unittest.TestCase):

    """Test cases for create_anomaly_graph function, which brings in data, removes NA values, creates a 
        dataframe of values calculating from the anomomly calculation"""
    
    def test_valid_data(self)
        "one shot test which brings in valid data, expecting no errors"

    def nonzero_testvalues(self)
        "test to make sure iqr and clean_alpha are not specified to 0 values, expecting raisevalueerror if not"

    def test_numeric_in_data(self)
        "test to make sure data after NA's are removed does not have any non-numeric values, expecting raisevalueerror"
    
    def testAnomalydf_is_created (self)
        "test to make sure Anomaly df has a non0 value"

    def plotly_graph_is_created(self)
        "test to make sure plotly graph is created, expecting raisevalueerror if not"


###############

class TestAnomalydecomp(unittest.TestCase):

    """ Test cases for anomalydecomp function, which provides graphs of statistical decomposition of anomaly calculation, 
    including __________"""

    def test_valid_data(self)
        "one shot test which brings in valid data, expecting no errors"

    def nonzero_testvalues(self)
        "test to make sure iqr and clean_alpha are not specified to 0 values, expecting raisevalueerror if not"

    def test_numeric_in_data(self)
        "test to make sure data after NA's are removed does not have any non-numeric values, expecting raisevalueerror"

    def testAnomalydf_is_created (self)
        "test to make sure Anomaly df has a non0 value"

    def plotly_graph_is_created(self)
        "test to make sure plotly graph is created, expecting raisevalueerror if not"




##############

class Testcreate_leaflet_map(unittest.TestCase):

    """Test cases for create_leaflet_map function, which creates a map of the locations of the stations"""

    def test_valid_data(self)
        "one shot test which brings in valid data, expecting no errors"

    def test_selected_location(self)
        "test to make sure the selected location is in the stations list, expecting raisevalueerror if not"

    def test_map_is_created(self)
        "test to make sure map is created, expecting raisevalueerror if not"

    def test_seven_stations(self)
        "test to make sure there are 7 stations in the map, expecting raisevalueerror if not"

    
################



