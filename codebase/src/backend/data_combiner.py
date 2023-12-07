"""
This script runs after data_loader and data_transformer. 
It combines the data from all 3 sources (iChart, Old, New) from data/processed into a single combined dataset.
Ideally, this script only needs to be run once or any time we collect new data from the WQData API. 
"""
import os
import pandas as pd

from config_combine import COMBINE_MAP

# Run for daily data
for name, all_device in COMBINE_MAP.items():
    combined_df = []
    for prod, prod_device in zip(["ichart", "old", "new"], all_device):
        # Skip in 
        if prod_device is None:
            continue
        if prod == "ichart":
            path = f"../../data/processed/{prod}/{prod_device}/tidy_daily_all_data.csv"
        else:
            path = f"../../data/processed/{prod}/{prod_device}/tidy_daily_all_data.csv"
        if not os.path.exists(path):
            raise FileNotFoundError(f"Path {path} does not exist.")

        combined_df.append(
            pd.read_csv(path)
        )
    combined_df = pd.concat(combined_df, ignore_index=True).set_index("times")
    combined_df["location"] = name
    if not os.path.exists(f"../../data/processed/combined/{name}"):
        os.mkdir(f"../../data/processed/combined/{name}")
    combined_df.to_csv(f"../../data/processed/combined/{name}/daily.csv")

# Run for hourly data
for name, all_device in COMBINE_MAP.items():
    combined_df = []
    for prod, prod_device in zip(["ichart", "old", "new"], all_device):
        # Skip in 
        if prod_device is None:
            continue
        if prod == "ichart":
            path = f"../../data/processed/{prod}/{prod_device}/tidy_hourly_all_data.csv"
        else:
            path = f"../../data/processed/{prod}/{prod_device}/tidy_hourly_all_data.csv"
        if not os.path.exists(path):
            raise FileNotFoundError(f"Path {path} does not exist.")

        combined_df.append(
            pd.read_csv(path)
        )
    combined_df = pd.concat(combined_df, ignore_index=True).set_index("times")
    combined_df["location"] = name
    if not os.path.exists(f"../../data/processed/combined/{name}"):
        os.mkdir(f"../../data/processed/combined/{name}")
    combined_df.to_csv(f"../../data/processed/combined/{name}/hourly.csv")