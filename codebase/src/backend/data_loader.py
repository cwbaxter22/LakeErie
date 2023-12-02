"""
TODO: 
How do we know what start and end dates work for each device/param?
    - We could just write a script to iterate through each device and each parameter and try every date combo since 2016, 
      but that would take forever and seems annoying
Clean up doc strings, add type hints, and add error handling
Start processing data and thing about how we want final format to look
Add tests for each function
"""
import time
import os
import http.client
import datetime
import json
import pandas as pd
import numpy as np
from collections import defaultdict

from typing import Dict
from config import OLD_API_KEY, NEW_API_KEY, PARAMETERS

start_year = 2014
current_year = datetime.date.today().year # TODO: Change this to current year


class DataLoader(): 
    """
    This class can be used to load data from the wqdatalive API.
    1) It will construct a url based on the parameters passed in
    2) Make a request to the API and handle errors
    3) Parse the reponse and return json (it will NOT clean or manipulate the data in any way - this will be done in the data cleaning class)
    """
    def __init__(self, apiKey: str, project: str) -> None:
        """
        Arguments: 
        ----------
        variable (type): description

        Returns: 
        ----------

        Raises: 
        ----------
        """
        self.devices = None
        self.device_parameters = defaultdict(list)
        self.apiKey = apiKey

        self.processed_device_parameters = defaultdict(list)
        self.processed_devices = []
        self.current_start_time = None
        self.project = project


    def api_call(self, url: str) -> Dict:
        """
        Call WQData API
        """
        conn = http.client.HTTPSConnection("www.wqdatalive.com")
        conn.request("GET", url)
        res = conn.getresponse()
        data = res.read()
        data = data.decode("utf-8")
        data = json.loads(data)

        return data

    def find_errors(self, data: Dict) -> bool:
        if "message" in data.keys():
            if data["message"] == "Request exceeds hourly limit":
                return False

            print(data["message"])

        return True

    def get_devices(self) -> Dict: 
        """
        Get the list of devices for our project
        """
        if self.devices == None:
            devices = {}
            data = self.api_call(url=f"/api/v1/devices?apiKey={self.apiKey}")
            
            # Check for errors
            if not self.find_errors(data):
                return None

            # If no errors, parse data
            for d in data["devices"]: 
                # Replace space with underscores in device_name
                device_name = d["name"].replace(" ", "_")
                devices[device_name] = d["id"]

        self.devices = devices

        return self.devices


    def get_device_parameters(self, deviceId: str) -> Dict:
        """
        Get valid parameters for device 
        TODO: Should probably cache device params 

        Returns: 
        ----------
        parameters (dict): {parameter_name: parameter_id}
        """
        parameters = {}
        data = self.api_call(url=f"/api/v1/devices/{deviceId}/parameters?apiKey={self.apiKey}")
        # Check for errors
        if not self.find_errors(data):
            return None

        # If no errors, parse data
        for d in data["parameters"]: 
            parameter_name = d["name"].replace(" ", "_")
            if parameter_name in PARAMETERS:
                parameters[parameter_name] = (d["id"], d["unit"])

        # Save parameters for this device
        self.device_parameters[deviceId] = parameters
            
        return parameters


    def get_data(self,
        deviceId: str, 
        parameterId: str, 
        start_date: str, 
        end_date: str
    ) -> Dict:
        """
        Get data for a device and parameter between start and end dates
        Add 1 second to start_date so that times never overlap

        Arguments:
        ----------
        deviceId (str): device id
        parameterId (str): parameter id
        start_date (str): start date in format YYYY-MM-DD
        end_date (str): end date in format YYYY-MM-DD

        Returns:
        ----------

        """
        try:
            data = self.api_call(
                url=f"/api/v1/devices/{deviceId}/parameters/{parameterId}/data?apiKey={self.apiKey}&from={start_date}%2000:00:01&to={end_date}%2000:00:00"
            )
            # Check for errors
            if not self.find_errors(data):
                return None

            # If no errors, parse data
            times, values = [], []
            for d in data["data"]:
                times.append(d["timestamp"])
                values.append(d["value"])

            return pd.DataFrame({"times": times, "values": values}) 

        except Exception as e:
            print(e)
            return None


def get_times():
    """
    TODO: Change this to monthly
    Create list of strings for each 2 month segment between 2014 and 2023 starting in 2014-05-01
    """
    times = []
    for year in range(start_year, current_year + 1):
        for month in np.arange(1, 13):
            if month >= 10:
                times.append(f"{year}-{month}-01")
            else: 
                times.append(f"{year}-0{month}-01")

    return times


def aggregate_data(test: bool = False, old: bool = False, project: str = "new"):
    """
    This function will: 
    1. Create a DataLoader object
    2. Get devices for our project
    3. Get parameters for once device
    4. Iterate through each device, parameter, and time range and request data 
    5. Save data to CSV files
    """
    if old: 
        apiKey = OLD_API_KEY
    else: 
        apiKey = NEW_API_KEY

    # Create Dataloader
    dataLoader = DataLoader(apiKey=apiKey, project=project)
    Done = False

    while not Done:
        Done = ping_api(dataLoader, test=test)
        time.sleep(3600)


def ping_api(dataLoader, test: bool = False):
    """

    Arguments:
    ----------
    Returns:
    ----------
    """

    # Get Devices for our project
    if dataLoader.devices is None:
        devices = dataLoader.get_devices()
        if devices == None: 
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
            if parameters == None: 
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
                    import pdb; pdb.set_trace()
                    return False
                else: 
                    dataLoader.current_start_time = times[i+1]

                cur_data.rename(columns={"values": parameter_name}, inplace=True)

                # Add current data slice to aggregated dataframe
                data = pd.concat([data, cur_data], ignore_index=True)

                # Save data for parameter to CSV for current call
                data["Units"] = parameter_units
                save_path = os.path.join(device_directory, f"{parameter_name}.csv")
                data.to_csv(save_path, mode="a", index=False, header=(not os.path.exists(save_path)))

                # If testing mode, only get first 12 months
                if (i == 12) and test: break

            # Update processed_device_parameters because we have completed this parameter for this device
            dataLoader.processed_device_parameters[device_id].append(parameter_name)

        # Update processed_devices because we have successfully completed this device
        dataLoader.processed_devices.append(device_name)

        # If testing mode, only get first device
        if test: break

    return False

# Change this to false when we're ready to actually run 
TEST = True

# Collect Old Data
aggregate_data(test=TEST, old=True, project="old")

# Collect New Data
# aggregate_data(test=TEST, old=False, project="new")


