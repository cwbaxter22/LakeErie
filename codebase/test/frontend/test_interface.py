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


class TestGUIMethods(unittest.TestCase):
    '''Plotter testing: smoke (1)'''
    def test_smoke(self):
        """
        Testing that the plot function generates a figure using simple, arbitrary scatter plot
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
