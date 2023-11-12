"""
TODO: 
How do we know what start and end dates work for each device/param?
    - We could just write a script to iterate through each device and each parameter and try every date combo since 2016, 
      but that would take forever and seems annoying
Clean up doc strings, add type hints, and add error handling
Start processing data and thing about how we want final format to look
"""

import http.client
import json
import pandas as pd

from typing import Dict
from config import apiKey


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

    def api_call(self, url) -> Dict:
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

    def get_device_parameters(self, deviceId) -> Dict:
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
            parameters[d["name"]] = d["id"]
        return parameters

    def get_data(self,
        deviceId: str, 
        parameterId: str, 
        start_date: str, 
        end_date: str
    ) -> Dict:
        """
        Get data for a device and parameter between start and end dates
        Arguments:
        ----------
        deviceId (str): device id
        parameterId (str): parameter id
        start_date (str): start date in format YYYY-MM-DD
        end_date (str): end date in format YYYY-MM-DD
        """
        data = self.api_call(
            url=f"/api/v1/devices/{deviceId}/parameters/{parameterId}/data?apiKey={apiKey}&from={start_date}%2010:00:00&to={end_date}%2010:00:00"
        )
        times, values = [], []
        for d in data["data"]:
            times.append(d["timestamp"])
            values.append(d["value"])

        return pd.DataFrame({"times": times, "values": values}) 



# Create Dataloader
dataLoader = DataLoader()
# Get Devices for our project
devices = dataLoader.get_devices()
# Get parameters for one device
parameters = dataLoader.get_device_parameters(deviceId=devices["TREC Tower iSIC"])
# Request data from that device
data = dataLoader.get_data(
    deviceId=devices["TREC Tower iSIC"], 
    parameterId=parameters["Air Temperature"], 
    start_date="2019-06-01", 
    end_date="2019-06-10"
)
print(data)
