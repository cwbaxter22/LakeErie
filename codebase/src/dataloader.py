"""
TODO: 
How do we know what start and end dates work for each device/param?
    - We could just write a script to iterate through each device and each parameter and try every date combo since 2016, 
      but that would take forever and seems annoying
Clean up doc strings, add type hints, and add error handling
Start processing data and thing about how we want final format to look
Add tests for each function
"""

import os
import http.client
import datetime
import json
import pandas as pd

from typing import Dict
from config import apiKey

start_year = 2014
current_year = datetime.date.today().year # TODO: Change this to current year


class DataLoader(): 
    """
    This class can be used to load data from the wqdatalive API.
    1) It will construct a url based on the parameters passed in
    2) Make a request to the API and handle errors
    3) Parse the reponse and return json (it will NOT clean or manipulate the data in any way - this will be done in the data cleaning class)
    """
    def __init__(self) -> None:
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


    def get_devices(self) -> Dict: 
        """
        Get the list of devices for our project
        """
        if self.devices == None:
            devices = {}
            data = self.api_call(url=f"/api/v1/devices?apiKey={apiKey}")
            for d in data["devices"]: 
                devices[d["name"]] = d["id"]
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
        df = self.api_call(url=f"/api/v1/devices/{deviceId}/parameters?apiKey={apiKey}")

        for d in df["parameters"]: 
            parameters[d["name"]] = (d["id"], d["unit"])
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
        """
        data = self.api_call(
            url=f"/api/v1/devices/{deviceId}/parameters/{parameterId}/data?apiKey={apiKey}&from={start_date}%2000:00:01&to={end_date}%2000:00:00"
        
        )
        times, values = [], []
        for d in data["data"]:
            times.append(d["timestamp"])
            values.append(d["value"])

        return pd.DataFrame({"times": times, "values": values}) 


def get_times():
    """
    Create list of strings for each 3 month segment between 2014 and 2023 starting in 2014-05-01
    """
    times = []
    for year in range(start_year, current_year + 1):
        for month in [1, 3, 5, 7, 9, 11]:
            if month == 11:
                times.append(f"{year}-{month}-01")
            else: 
                times.append(f"{year}-0{month}-01")

    return times


def aggregate_data(test=False):
    """
    This function will: 
    1. Create a DataLoader object
    2. Get devices for our project
    3. Get parameters for once device
    4. Iterate through each device, parameter, and time range and request data 
    5. Save data to CSV files
    """
    # Create Dataloader
    dataLoader = DataLoader()

    # Get Devices for our project
    devices = dataLoader.get_devices()

    times = get_times()
    num_times = len(times)


    # Iterate through each device
    for device_name, device_id in devices.items():
        print("Starting Device:", device_name)
        # Replace space with underscores in device_name
        device_name = device_name.replace(" ", "_")

        # If doesn't already exist, create folder for device
        device_directory = f"../data/raw/{device_name}"
        if not os.path.exists(device_directory):
            os.mkdir(device_directory)

        # Get parameters for one device
        parameters = dataLoader.get_device_parameters(deviceId=device_id)

        # Iterate through each parameter
        for parameter_name, (parameter_id, parameter_units) in parameters.items():
            print("- parameter:", parameter_name)
            # Replace space with underscores in parameter_name
            parameter_name = parameter_name.replace(" ", "_")

            # Create Pandas Dataframe to concat data to
            data = pd.DataFrame(columns=["times", parameter_name])

            # Iterate through each 2-month time range
            for i in range(num_times):
                # Skip last time because we don't have data for it
                if i == num_times - 1:
                    continue

                # Request data from that device
                cur_data = dataLoader.get_data(
                    deviceId=device_id,
                    parameterId=parameter_id,
                    start_date=times[i], 
                    end_date=times[i+1]
                )
                cur_data.rename(columns={"values": parameter_name}, inplace=True)

                # Add current data slice to aggregated dataframe
                data = pd.concat([cur_data, data], ignore_index=True)

                if (i == 10) and test: break
            
            # Save data for parameter to CSV
            data["Units"] = parameter_units
            data.to_csv(os.path.join(device_directory,f"{parameter_name}.csv"), index=False)

        if test: break

# Change this to false when we're ready to actually run 
TEST = True
aggregate_data(test=TEST)


