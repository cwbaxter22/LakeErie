"""
This script runs after data_loader and before data_transformer. 
It combines the data all data sources (ichart, old, and new) into a single raw/combined folder. 
We can then run data_transformer on the combined data to get a single tidy csv file for the frontend
"""

import os

from config import COMBINE_MAP