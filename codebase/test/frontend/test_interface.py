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
import unittest
import plotly.express as px
import sys

# Add path to pages
#codebase_path = pathlib.Path(__file__).parents[2]
#sys.path.append("../../src/pages")
# Get creative importing streamlit pages, since they begin with a number
sys.path.append("../../src/pages")
TemporalData = __import__('2_Temporal_Data')


class TestGUIMethods(unittest.TestCase):
    '''Plotter testing: smoke (1)'''
    def test_smoke(self):
        """
        Testing that the plot function generates a figure using simple, arbitrary scatter plot

        """
        try:
            fig = px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])
            TemporalData.plot_it(fig)
        except RuntimeError:
            self.assertRaises(RuntimeError)

if __name__ == '__main__':
    unittest.main()
