import os
import pandas as pd

file = os.path.dirname(os.path.abspath(__file__))

df = pd.read_csv(r"..\data\iChart6_data\processed\Beach2_Buoy_all_data.csv")
#print(df.head())
