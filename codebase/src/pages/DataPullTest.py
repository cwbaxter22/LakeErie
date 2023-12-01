import os
import pandas as pd

dirname = os.path.dirname(__file__)

beach6hourly = os.path.join(dirname, "data/iChart6_data/processed/Beach6_Buoy/daily_tidy_all_data.csv")
df = pd.read_csv(beach6hourly)
print(df.head())
