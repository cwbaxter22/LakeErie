"""
TODO: 
1. Create a class called DataTransformer
2. Load the DataLoader class and create instance
3. Call get_devices. Iterate through each device
4. Read all the .csv files in /data/raw/<device_name> and aggregate them into one dataframe
5. In the DataTransformer class create a method called downsample which converts the data to a lower time frequency (hourly or daily instead of minutely)
6. Do any other transformations to DataTransformer class that are important 
    (e.g. fill missing chunks with np.nans, add units, and convert to tidy format)
7. Save the data to /data/processed/<device_name>_<parameter_name>.csv
"""

# Import DataLoader class from dataloader.py
from dataloader import DataLoader 

