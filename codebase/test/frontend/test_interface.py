"""Unittesting of GUI application functions

Module allows for the testing of the functions associated with the GUI application

This script requires that unittest and numpy be installed within the Python
environment you run the module in. The src module must be available to import.

This file can be run from the frontend/ directory using the command:
'py -m unittest discover'. The module contains the following
tests:

    plot_it()
    * smoke_test - confirm the function is able to run.
    
"""
import importlib
import unittest
import pathlib
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
    '''DF creation: smoke (1)'''
    def test_smoke(self):
        """
        Passing the path to the combined data folder generates a dataframe.
        The default values should allow the function to always return a df, unless the
        user chooses to adjust the settings. 

        """
        try:
            codebase_folder_path = pathlib.Path(__file__).parents[2]
            path_to_df = str(codebase_folder_path) + "/data/processed/combined/"
            df_manip_plotting_mod.df_creation(path_to_df)
        except RuntimeError:
            self.assertRaises(RuntimeError)
    def test_oneshot_columnnames(self):
        """
        **Come back to this tomorrow.
        Confirm the dataframe columns are correct 

        """
        try:
            codebase_folder_path = pathlib.Path(__file__).parents[2]
            path_to_df = str(codebase_folder_path) + "/data/processed/combined/"
            df_manip_plotting_mod.df_creation(path_to_df)
        except RuntimeError:
            self.assertRaises(RuntimeError)
class TestCreateAllTimeFig(unittest.TestCase):
    '''All time figure testing: smoke (1)'''
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

class TestAnnualComparisonFig(unittest.TestCase):
    '''Annual Comparison figure testing: smoke (1)'''
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

class TestPlotIt(unittest.TestCase):
    '''Plotter testing: smoke (1)'''
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

if __name__ == '__main__':
    unittest.main()
