"""
The WQData API only allows 140 API calls per hour, 5,000 data points per API call, and 90 days of data per API call. 
The aim of this script is to use the DataLoader class to scrape data from the WQData API and save it to CSV files 
efficiently and within the constraints of the WQData API. 

WQData also transitioned to new dataloggers in 2016, so another challenge is there are TWO different data sources, 
each with their own API key. 

To do this we run aggregate_data() twice: 
1. Execute Aggregate Data with API key set to old
2. Execute Aggregate Data with API key set to new

Ideally this script only needs to be run once to get all of the data.

Refer to the aggregate_data() docstring for an explanation of how this function works. 
"""
import time
import os

import datetime
import pandas as pd
import numpy as np

from config import OLD_API_KEY, NEW_API_KEY
from data_loader import DataLoader

# CREATE GLOBAL TIME CONSTANTS
START_YEAR = 2014
CURRENT_YEAR = datetime.date.today().year

def get_times() -> list:
    """
    Create list of strings for each 1 month segment between START_YEAR and CURRENT_YEAR starting in 2014-05-01

    Returns: 
    ----------
    times [list]: list of strings for each 1 month segment (e.g. ['2014-05-01', '2014-06-01', ...])
    """
    times = []
    for year in range(START_YEAR, CURRENT_YEAR + 1):
        for month in np.arange(1, 13):
            if month >= 10:
                times.append(f"{year}-{month}-01")
            else:
                times.append(f"{year}-0{month}-01")

    return times


def aggregate_data(test: bool = False, old: bool = False, project: str = "new") -> None:
    """
    This function will: 
    1. Create a DataLoader object with the correct API key and project
    2. Call ping_api() until all data has been collected for that project
        - if we run out of API calls for that hour before download all the data, 
        we will sleep for 1 hour and then resume
    """
    if old:
        apiKey = OLD_API_KEY
    else:
        apiKey = NEW_API_KEY

    # Create Dataloader
    dataLoader = DataLoader(apiKey=apiKey, project=project)
    done = False

    while not done:
        print("Starting new call")
        done = ping_api(dataLoader, test=test)
        print("Sleeping for 1 hour")
        time.sleep(3600)


def ping_api(dataLoader, test: bool = False) -> bool:
    """
    This function will:
    1. Get all devices for the project
    2. Iterate through each device
    3. Iterate through each parameter for that device
    4. Iterate through each 1-month time range
    5. Request data from that device
    6. Save data for parameter to CSV for current call
    7. Return True if we have successfully downloaded all data, False if we haven't finished downloading all data

    If we run out of API keys, dataLoader keeps track of its existing state.
    Using this the dataloader state information, ping_api will resume where it left off when we call ping_api() again

    Arguments:
    ----------
    dataLoader (DataLoader): DataLoader object
    test (bool): default False

    Returns:
    ----------
    status (bool): True if successfully downloaded all data, False if we haven't finished downloading all data
    """

    # Get Devices for our project
    if dataLoader.devices is None:
        devices = dataLoader.get_devices()
        if devices is None:
            return False
    else: 
        devices = dataLoader.devices

    times = get_times()
    num_times = len(times)

    # Iterate through each device
    for device_name, device_id in devices.items():

        # Skip devices that we have already processed
        if device_name in dataLoader.processed_devices:
            continue

        print("Starting Device:", device_name)

        # If doesn't already exist, create folder for device
        device_directory = f"../../data/raw/{dataLoader.project}/{device_name}"
        if not os.path.exists(device_directory):
            os.mkdir(device_directory)

        # Get parameters for one device
        if len(dataLoader.device_parameters[device_id]) == 0:
            # If we haven't already gotten parameters for this device, get them
            parameters = dataLoader.get_device_parameters(deviceId=device_id)
            if parameters is None:
                return False
        else: 
            # Otherwise, grab the parameters for this device
            parameters = dataLoader.device_parameters[device_id]

        # Iterate through each parameter
        for parameter_name, (parameter_id, parameter_units) in parameters.items():
            print("- parameter:", parameter_name)
            if parameter_name in dataLoader.processed_device_parameters[device_id]:
                continue

            # Create Empty Pandas Dataframe to concat data to
            data = pd.DataFrame(columns=["times", parameter_name])

            # Iterate through each 1-month time range
            for i in range(num_times):
                # Skip last time because we don't have data for it
                if i == num_times - 1:
                    continue

                if dataLoader.current_start_time is not None:
                    if times[i] != dataLoader.current_start_time:
                        continue

                # Request data from that device
                cur_data = dataLoader.get_data(
                    deviceId=device_id,
                    parameterId=parameter_id,
                    start_date=times[i],
                    end_date=times[i+1]
                )

                if cur_data is None:
                    dataLoader.current_start_time = times[i]
                    return False
                else:
                    dataLoader.current_start_time = times[i+1]

                cur_data.rename(columns={"values": parameter_name}, inplace=True)

                # Add current data slice to aggregated dataframe
                data = pd.concat([data, cur_data], ignore_index=True)

                # Save data for parameter to CSV for current call
                data["Units"] = parameter_units
                save_path = os.path.join(device_directory, f"{parameter_name}.csv")
                data.to_csv(
                    save_path,
                    mode="a",
                    index=False,
                    header=(not os.path.exists(save_path))
                )

                # If testing mode, only get first 12 months
                if (i == 12) and test:
                    break

            # Reset current_start_time to 0 for next parameter
            dataLoader.current_start_time = times[0]

            # Update processed_device_parameters because we have completed this parameter for this device
            dataLoader.processed_device_parameters[device_id].append(parameter_name)

        # Update processed_devices because we have successfully completed this device
        dataLoader.processed_devices.append(device_name)

        # If testing mode, only get first device
        if test:
            break

    return True

if __name__ == "__main__":
    pass
    """
    Uncomment this block of code to run the aggregate data using the DataLoader
    """
    # Set this to True to run in test mode
    # TEST = False

    # Collect Old Data
    # aggregate_data(test=TEST, old=True, project="old")

    # Collect New Data
    # aggregate_data(test=TEST, old=False, project="new")
