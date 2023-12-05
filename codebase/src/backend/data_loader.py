"""
This file is used to define a DataLoader class that can be used to interface with the WQdata API
It can be used to get a list of available devices, parameters, and data for a given project.
"""
import http.client
import datetime
import json
import pandas as pd
import numpy as np
from collections import defaultdict

from typing import Dict
from config_combine import PARAMETERS


class DataLoader(): 
    """
    This class can be used to load data from the wqdatalive API.
    1) It can construct a url based on the parameters passed in
    2) Make a request to the API and handle errors
    3) Parse the reponse and return json (it will NOT clean or manipulate the data in any way - this will be done in the data cleaning class)
    """
    def __init__(self, apiKey: str, project: str) -> None:
        """
        Arguments: 
        ----------
        variable (type): description
        """
        self.devices = None
        self.device_parameters = defaultdict(list)
        self.apiKey = apiKey
        self.project = project

        # This is "state information" to keep track of processed data 
        self.processed_device_parameters = defaultdict(list)
        self.processed_devices = []
        self.current_start_time = None


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
        """
        Parse the json response from the API and check for errors
        """
        if "message" in data.keys():
            if data["message"] == "Request exceeds hourly limit":
                return False

            print(data["message"])

        return True

    def get_devices(self) -> Dict: 
        """
        Get the list of devices for our project

        Returns:
        ----------
        devices (dict): {device_name: device_id}
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
        Cache device parameters so we don't have to make this call again 

        Arguments:
        ----------
        deviceId (str): device id

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
        data (pd.DataFrame): dataframe with columns "times" and "values" OR None if failed

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



