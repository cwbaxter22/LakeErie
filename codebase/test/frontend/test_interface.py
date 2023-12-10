"""Unittesting of GUI application functions

Module allows for the testing of the functions associated with the GUI application

This script requires that unittest and numpy be installed within the Python
environment you run the module in. The src module must be available to import.

This file can be run from the frontend/ directory using the command:
'py -m unittest discover'. 

Most tests are very basic as most work is performed by plotly (figure data cannot be indexed)
Therefore, many tests were made for the df_creation() function, since it is the 
'logic-heavy' portion of the code.
    
"""
import datetime
import importlib
import unittest
import pathlib
import numpy as np
import pandas as pd
import plotly.express as px

codebase_path = pathlib.Path(__file__).parents[2]
#https://stackoverflow.com/questions/65206129/importlib-not-utilising-recognising-path
spec = importlib.util.spec_from_file_location(
    name='plotting_mod',  # name is not related to the file, it's the module name!
    location= str(codebase_path) +
    "//src//frontend//df_manip_plotting.py"  # full path to the script
)
df_manip_plotting_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(df_manip_plotting_mod)

class TestDFCreation(unittest.TestCase):
    '''DF creation: smoke (1), oneshot (2)
    
    Path to df defined in initialization,
    If folder is moved, most tests will fail.'''
    def __init__(self, methodName: str = "runTest") -> None:
        """
        Initialization
        """
        super().__init__(methodName)
        codebase_folder_path = pathlib.Path(__file__).parents[2]
        self.path_to_df = str(codebase_folder_path) + "/data/processed/combined/"
    def test_smoke(self):
        """
        Passing the path to the combined data folder generates a dataframe.
        The default values should allow the function to always return a df, unless the
        user chooses to adjust the settings. 

        """
        try:
            df_manip_plotting_mod.df_creation(self.path_to_df)
        except RuntimeError:
            self.assertRaises(RuntimeError)
    def test_oneshot(self):
        """
        Check column names and function return types
        """
        def test_column_names(col_names: list) -> None:
            """
            Column names are correct

            Arguments:
            ----------
            col_names (list): list of potential column names for df

            Returns:
            ----------
            None: check performed in function 

            """
            (df_viz, _, _, _, _) = df_manip_plotting_mod.df_creation(self.path_to_df)
            col_names_curr = list(df_viz.columns)

            match_check = set(col_names_curr).issubset(col_names)
            self.assertTrue(match_check)
        def test_output_type() -> None:
            """
            Variables returned are correct type

            Arguments:
            ----------
            None

            Returns:
            ----------
            None: check performed in function 

            """
            (df_loc_time_selection,
                variable_to_plot,
                locations_to_graph,
                start_time, end_time) = df_manip_plotting_mod.df_creation(self.path_to_df)
            if not isinstance(df_loc_time_selection, (type(pd.DataFrame()))):
                self.assertRaises(TypeError)
            if not isinstance(variable_to_plot, (str)):
                self.assertRaises(TypeError)
            if not isinstance(locations_to_graph, (str, list)):
                self.assertRaises(TypeError)
            if not (any(isinstance(i, (type(datetime.date)))) for i in [start_time, end_time]):
                self.assertRaises(TypeError)

        # Column Name Tests
        # Column names should match what is in this list
        col_names_req = ["times", "parameter", "Units",
                         "value_mean", "value_std", "location"]
        test_column_names(col_names_req)
        # Column names should match this list as well, order does not matter
        col_names_req_alt = ["parameter", "Units", "value_mean",
                             "value_std", "location", "times"]
        test_column_names(col_names_req_alt)
        # Column names should not match this list because 'times' should not be capitalized
        incorrect_column_names = ["Times", "parameter", "Units",
                                "value_mean", "value_std", "location"]
        # Column names should not match this list because these are the names of the Seven Dwarves
        the_seven_dwarves = ["Dopey", "Doc", "Bashful",
                             "Sneezy", "Happy", "Grumpy",
                             "Sleepy"]
        with self.assertRaises(AssertionError):
            test_column_names(incorrect_column_names)
            test_column_names(the_seven_dwarves)
        # Output type tests
        # General check to ensure all output is of the correct type
        test_output_type()
    def test_edge(self):
        """
        Check folder address is correct
        """
        def test_folder_check(folder_location:str) -> None:
            """
            Location of folder is correct

            Arguments:
            ----------
            folder_location (str): Path to try to open dataframe

            Returns:
            ----------
            None: check performed in function 

            """
            self.assertTrue(self.path_to_df == folder_location)
            # Edge tests
            # Correct path should not create an error
        with self.assertRaises(AssertionError):
            # Incorrect path raise error
            test_folder_check("../A/Madeup/Folder")
            # Not a path at all, raise error
            test_folder_check(5)
class TestCreateAllTimeFig(unittest.TestCase):
    '''All time figure: smoke (1), edge test (1)'''
    def test_smoke(self):
        """
        Generate an arbitrary all-time figure.
        Note: Columns must contain parameter, value_mean, value_std, location, Units, and times.
        Indexing uses strings, so anything slightly different will return an error.

        """
        try:
            d = {'parameter': ['Air_Temp', 'Air_Temp', 'Air_Temp'],
                 'value_mean': [1.0, 1.1, 1.2],
                 'value_std': [0, 1, 2],
                 'location': ['trec', 'trec', 'trec'],
                 'Units' : ['F', 'F', 'F'],
                 'times' : pd.to_datetime(['2008-05-20', '2008-05-21', '2008-05-22'])}
            df = pd.DataFrame(data=d)
            df_manip_plotting_mod.create_all_time_fig(df,
                                               'Test Title',
                                               'value_mean',
                                               1,
                                               'trec',
                                               pd.to_datetime('2008-05-20'),
                                               pd.to_datetime('2008-05-22')
                                               )
        except RuntimeError:
            self.assertRaises(RuntimeError)
    def test_edge_test(self):
        """
        Time must be in pd datetime format

        """
        d = {'parameter': ['Air_Temp', 'Air_Temp', 'Air_Temp'],
                'value_mean': [1.0, 1.1, 1.2],
                'value_std': [0, 1, 2],
                'location': ['trec', 'trec', 'trec'],
                'Units' : ['F', 'F', 'F'],
                'times' : (['2008-05-20', '2008-05-21', '2008-05-22'])}
        df = pd.DataFrame(data=d)
        try:
            df_manip_plotting_mod.create_all_time_fig(df,
                                                'Test Title',
                                                'value_mean',
                                                1,
                                                'trec',
                                                pd.to_datetime('2008-05-20'),
                                                pd.to_datetime('2008-05-22')
                                                )
        except (Exception,):
            self.assertRaises(TypeError)
class TestAnnualComparisonFig(unittest.TestCase):
    '''Annual Comparison figure: smoke (1), edge (1)'''
    def test_smoke(self):
        """
        Generate an arbitrary annual comparison figure.
        Note: Columns must contain parameter, value_mean, value_std, location, and Units.
        Note2: No timestamps provided since the user will be given yearly options for all years.
        Indexing uses strings, so anything slightly different will return an error.

        """
        try:
            d = {'parameter': ['Air_Temp', 'Air_Temp', 'Air_Temp'],
                 'value_mean': [1.0, 1.1, 1.2],
                 'value_std': [0, 1, 2],
                 'location': ['trec', 'trec', 'trec'],
                 'Units' : ['F', 'F', 'F'],
                 'times' : pd.to_datetime(['2008-05-20', '2008-05-21', '2008-05-22'])}
            df = pd.DataFrame(data=d)
            df_manip_plotting_mod.create_annual_comparison_fig(df,
                                               'Test Title',
                                               'value_mean',
                                               1,
                                               'trec'
                                               )
        except RuntimeError:
            self.assertRaises(RuntimeError)
    def test_edge_test(self):
        """
        Dates must be in pd datetime format for function to run
        """
        try:
            d = {'parameter': ['Air_Temp', 'Air_Temp', 'Air_Temp'],
                 'value_mean': [1.0, 1.1, 1.2],
                 'value_std': [0, 1, 2],
                 'location': ['trec', 'trec', 'trec'],
                 'Units' : ['F', 'F', 'F'],
                 'times' : (['2008-05-20', '2008-05-21', '2008-05-22'])}
            df = pd.DataFrame(data=d)
            df_manip_plotting_mod.create_annual_comparison_fig(df,
                                               'Test Title',
                                               'value_mean',
                                               1,
                                               'trec'
                                               )
        except (Exception,):
            self.assertRaises(TypeError)
class TestPlotIt(unittest.TestCase):
    '''
    Plotter function: smoke (1), edge (1)

    This is a simple function that is just called to format plots.
    Nothing is returned and it requires only minimal testing.
    '''
    def test_smoke(self):
        """
        The plot function generates a figure using simple, arbitrary scatter plot
        Arbitrary data from https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html

        """
        try:
            fig = px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])
            d = {'col1': [1, 2], 'col2': [3, 4]}
            df = pd.DataFrame(data=d)
            df_manip_plotting_mod.plot_it(fig, df)
        except RuntimeError:
            self.assertRaises(RuntimeError)
    def test_edge(self):
        """
        Function should not work for things that are of the incorrect type
        """
        not_a_figure = np.ones((100, 100))
        d = {'col1': [1, 2], 'col2': [3, 4]}
        df = pd.DataFrame(data=d)
        with self.assertRaises(AttributeError):
            df_manip_plotting_mod.plot_it(not_a_figure, df)

if __name__ == '__main__':
    unittest.main()
