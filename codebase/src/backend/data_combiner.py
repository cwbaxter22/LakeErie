"""
This script runs after data_loader and data_transformer. 
It combines the data from all 3 sources (iChart, Old, New) from data/processed into a single combined dataset.
Ideally, this script only needs to be run once or any time we collect new data from the WQData API. 
"""
import os
import pandas as pd

from config_combine import COMBINE_MAP

def combine_data_sources() -> None:
    """
    This function combines the data from all 3 sources (iChart, Old, New) 
    from data/processed into a single combined dataset and saves to
    data/processed/combined.
    """
    # Iterate through the COMBINE_MAP, a map defining which files should be combined
    # between the different sources
    for name, all_device in COMBINE_MAP.items():
        combined_df = []
        for prod, prod_device in zip(["ichart", "old", "new"], all_device):
            # Skip if there is no device for this source
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
        # Combine the data from all 3 sources
        combined_df = pd.concat(combined_df, ignore_index=True).set_index("times")
        # Set the location variable as requested by the frontend
        combined_df["location"] = name
        # Save the combined data to a csv file
        combined_df.to_csv(f"../../data/processed/combined/{name}.csv")


if __name__ == "__main__":
    combine_data_sources()
