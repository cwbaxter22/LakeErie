# Components

## Cleaned Database Filler
**Operation**   
1. Call API with request for data within time frame (to avoid computational expense, API calls will be administered at a set frequency, hence the time frame).
2. Remove data points that fall outside of the lowerbound to upperbound variable range.
3. Return the cleaned collection of data as a database. 
4. If percent of removed data points is 100%, send an email signaling buoy may require maintentance.
5. Percentage of points removed and timestamp is recorded in an audit log to provide for easier maintenance.

**Inputs**   
* Extraneous data upperbound [float]
* Extraneous data lowerbound [float]
* Start time of data collection [datetime]
* End time of data collection [datetime]
* Uncleaned database [database]  

**Outputs**  
* Cleaned databse [database]
* Percent of removed extraneous datapoints [int]
* Timestamp of operation completion [int]

**Component Interfacing**  
* Component will pass data to cleaned database location, auditlog.txt will be updated with timestamp and data removal percentage
* Cleaned database will be accessed by *Historical Data Plotter*


## Historical Data Plotter  
**Operation**  
1. Generates plot of chosen variable data from chosen start time to end time at a specified frequency of data collection
(i.e. days, weeks, etc)  
2. Allows user to download a .jpg of plot

**Inputs**  
* Cleaned database [database]
* Start time of data collection [datetime]
* End time of data collection [datetime]
* Climate Variable [string]
* Frequency of collection [string]
	* Daily, weekly, monthly  

**Outputs**  
* Interactive (hover over for datapoint) plot of variable over time with trendline [GUI plot]
* Image of variable plot (downloadable) [jpeg]

**Component Interfacing**  
Retrieves data in database generated from *Cleaned Database Filler*
