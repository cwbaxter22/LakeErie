# Lake Erie Project

This code creates a GUI which displays trends in limnological and environmental data from weather bouys and stations in and around Lake Erie. These stations are deployed by the Regional Science Consortium. The user interface will allow stakeholders to view trends in data.

### Users will be able to:

- Explore live data (V2.0)
- Compare climate variables over space and time
- View statistical trends

# Technology Review

Technology Review Presentation Available here:
https://docs.google.com/presentation/d/1Gqygo2uVCjlTfW1YYUflClmrQNrQyhChPKJihoyyjBY/edit?usp=sharing



# Data Draft
The data for this project is structured and discussed in the following way:
Project – Device – Parameter
Where,
- Project is the source of the data (separated by year/software) [“ichart”, “old”, “new”]
- Device is the datalogger (location) [ex: “TREC_Tower”, “Beach2_Buoy”]
- Parameter is the specific variable you are interested in [ex: “Air_Temperature”, “ODO”]
 
The data manipulation we performed was a crucial part of this project, and will hopefully be a huge help to the Regional Science Consortium. The data was split into 3 different areas, 2 of which the regional science consortium could not access, nor did they know where it was. The data across all three projects, spanning 15+ years, was very messy and inconsistent. There were multiple changes to the Device name (location, ex: “TREC_Tower” and “TREC_Tower_iSIC”), Parameter name for a given device (“DO” and “ODO”), Parameter name across devices, units for a given parameter. Merging all of the data sets and standardizing the format proved to be quite a challenge.
 
## Raw data
The raw data comes from the regional science consortium and their weather devices on lake erie. Specifically, the data we are using in this repository comes from three different sources/timeperiods:
iChart6 – an archived database managed by nexsens
WQDatalive project “Regional Science Consortium (Old)” – an archived database managed by nexsens
WQDatalive project “Regional Science Consortium” – a current database managed by nexsens
The raw data for a given parameter and device is variable, in the sense that it is not all collected the same way. Tower locations collect data every 10 minutes, some buoys collect data every 20 minutes, and lastly, other buoys collect data every 30 minutes.
 Towers are left running year round, so in theory, you have 365 days worth of data (collecting every 10 minutes). Buoys are only in the water in the spring-fall, but the time they go in and are taken out is variable (largely it was May to October). There are large gaps in the data when the devices were not working or had issues. There were even larger gaps in the data between projects.
Each data source presented its own challenges that will be explained below.
### Projects:
#### iChart6
This archived database turned out to be the easiest to get data from, but the most difficult to clean. The data was shared via a googledrive link, which was downloaded locally on to our machine. We then had to download, and receive login credentials for the archived software that is needed to run/open the raw datafiles from the googledrive. Once you set up and configured the old software, you could manually download the data by device for all parameters for a given year. After downloading all of the data to usable csvs, we had to clean the data to get it into a standardized format. We uploaded the raw csvs to this repository, as well as all of the steps in the cleaning process for transparency.
Data exists for this database from 2006-2011 for TREC_Tower and Beach2_Tower, 2008-2011 for Beach2_Buoy, and 2011 for Beach6_Buoy.
 
#### “Old”
This archived database was on the currently support WQData live website. It could be accessed via API. If you wanted to get the raw data, you would need to obtain access to this archived database, as well as an API key. 
Data exists from this database from 2014-2020 for Beach2_Tower and Near_Shore_Buoy, 2016-2020 for Beach2_Buoy and Walnut_Creek_Buoy, and 2019-2020 for Beach6_Buoy.
 
#### “New”
This database is live on WQData live’s website and is updated with new/current data. 
Data exists from this database from 2014-present for TREC_Tower, 2016-present for Bay_Buoy and 2021-present for the other locations.

### Note on Device: 
There was an unknown device from the “new” project. Specifically Near Shore Buoy had two device IDs. We chose one of them for this project.
### Note on Parameter: 
Parameter names were not kept constant throughout the life history of all projects. This led to much confusion about what some of the parameters were. Specifically, there exists “battery temperature”, “air temperature”, “water temperature”, and “temperature” for some devices. Since we could not determine what “temperature” was measuring, we did not try to group it with other devices. 
 We were not able to download all of the data - i.e. all parameters - for the “old” and “new” projects. This was due to the fact that we had limited API calls, and limited API functionality. Each API call was limited to 5000 data points, and when some of the loggers are collecting data every 10 minutes for 20 parameters, it adds up fast. We calculated that we could only use 1 API call for 1 month for 1 parameter. This means that it would take 120 calls (our maximum calls per hour) to get all the data (10 years) for 1 parameter on 1 device. We had 20 parameters for 7 devices. That is roughly 6 days of continual running to obtain the data. We could not justify this decision. Instead, we obtained the data for the most important parameters as specified by the Regional Science Consortium – Air temperature, Water temperature, and ODO. 

 
## Processed Data
To clean and process this data we used the following python scripts:
### Pre-process_ichart_data.py
This file adjusts the column names, removes unnecessary headers, replaces empty strings with NaN values, and saves the data to a new csv that matches the format necessary for the functions in data_transformer.py.
### Data_transformer.py
This file contains the functions needed in run_data_transformer.py. The functions aggregates all the data from one device (for a given project), transforms the data into tidy format, and downsampled the data into hourly and daily time periods. This downsampling is essential, due to the large files.
### Run_data_transformer.py
This file is a wrapper for actually processing and cleaning the data. Originally it was developed to run the data_tranformer.py file for each project, however it had to be altered because of the very large files for the tower devices from “old” and “new” project.
NOTE: there was an error when running data_loader.py, and the file for TREC_Tower contained multiple copies of the data and headers, leading the file to be 700Mb+ in size.
The script was altered to first downsample the data into hourly and daily time periods. Next duplicates were removed from the file to parse it down and clean.
Lastly, the dataframes are transformed into tidy format, standardizing all of the data in the same way.
 
 
 
## Recreating the processed data files:
If you are inclined to recreate the data files please follow these steps:
Fork or clone the repository with it’s associated raw data files
- Step 1: run preprocess_ichart_data.py to obtain ichart data in a workable form
- Step 2: run run_data_loader.py  to obtain the “old” and “new” project data in a workable form
- Step 3: run run_data_transformer.py to tidy, donwsample, and clean the data.
- Step 4: run data_combiner.py to combine the data across projects into all data by device.
 
## If you would like to download the raw data for the “old” and “new”
 
## Version 2 live data:
In version 2 we hope to expand the data collection to include live data. Given the timeframe of the project, we did not think it was feasible to add it in version 1, especially with the state the data was in. We hypothesize the easiest way to add live data would be to have a new script that is constantly running and sleeping in the background that collects the most recent data and appends it to the processed csv files we created. In this manner, the csv files are constantly growing with the newest data every 10 minutes. In this way, we don’t believe the scripts would hit the api call limit, and cleaning and processing the data will be easy and fast due to the small file sizes.
 
 









# Advanced Time series statistics and Anomaly detection

The *Advanced Statistics* page allows the user to further explore Bouy data by examining underlying trends and statistical anomalies in the selected dataset. This is done using the pytimetk library, which is a python library for time series analysis.

https://business-science.github.io/pytimetk

To begin, the user is prompted to select whether they want to view hourly or daily data, and are given a drop down menu of available locations to view data from. One one location may be selected at once. 

Data collection sites are displayed on a dynamic map, which allows the user to zoom in and out, pan around the map, and colors the selected site in **red**. Hovering over the icon in the map will display the name of the site.

![Alt text](image-1.png)

Users can then select the Start-date ,end-date, and variable they would like to view from the sidebar. Time series data is then visualized with a smooth line fit to the data in blue. 

![Alt text](image-2.png)

**NOTE:** Not all variables are available for all sites and all time periods. Significant data gaps exist in the data. If seleced time period or variable does not exist, no data will be displayed

If the user is interesting in observing the valued displayed, a *Show Selected Data* button is available below the time series plot:  

 This will display the data in a table below the plot. The user has the functionality to scroll through the data, filter each collumn in ascending or descending order, and download the data as a CSV file.

![Alt text](image-3.png)

### Anomaly Detection

The second major functionality of the Advanced Statistics dashboard is identifying data points which may be considered anomalies in the time series data. This functionality may allow the user to narrow in on data points or time periods which may have differed from the overall trend of the data and may indicate a significant event. 

Anomalies are identified by detecting underlying seaonal and trend components of the time series data. The user is prompted to enter a number of variables which will be used towards the statistical decomposition which determined data anomalies. These variables are: 

**Period**: The period value determines the window for the seasonal decomposition. The period value is the number of observations per seasonal cycle. For example, if the user is interested in observing seasonal trends in the data, the period value should be set to 365.25 (days in a year). If the user is interested in observing daily trends in the data, the period value should be set to 24 (hours in a day). The default is set to 7, which looks for weekly trends in the data. 

**IQR alpha:** The IQR alpha value is used to determine the threshold for identifying outliers in the data. It is default set to .05, which sets a 5% significance level for determining outliars. The user can adjust this value up or down to to increase or decrease the sensitivity of the anomaly detection.

After selecting the user-prefered variabled for **Period** and **IQR alpha**, the dashboard displays the time series data with added anomaly bands displayed in gray. Data points that fall outside of this range are colored red to clearly indicate that they are considered anomalies given the user-selected parameters. User can hover over these points to get further data. 

![Alt text](image-4.png)

Finally, the "Show Statistical Decomposition" button below the plot will display the statistical decomposition of the time series data. This will display the seasonal, trend, and residual components of the data.

![Alt text](image-5.png)





