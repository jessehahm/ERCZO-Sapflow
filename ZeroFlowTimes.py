# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 13:48:37 2016
#ZeroFlowTimes.py
@author: JesseH
"""
#%% imports
import pandas as pd
import databaseQuery
import matplotlib.pyplot as plt
import numpy as np

#%% Variable declaration
startDateTime = pd.to_datetime('2015-07-01 05:00:00')
stopDateTime = pd.to_datetime('2016-02-11 05:00:00')

dateStart = str(startDateTime.year) + '-' + str(startDateTime.month) + '-' + str(startDateTime.day)
dateStop =  str(stopDateTime.year) + '-' + str(stopDateTime.month) + '-' + str(stopDateTime.day)

#%% Database query
#here we make use of external .py file with odmquery function (thanks Collin!) to get data from the database
#2957	Relative Humidity WSSR
#46	Relative Humidity - WSAM
relHumid = databaseQuery.odmquery(dateStart, 
                                  dateStop, 
                                  '2957', True)

#%% Resample to match sapflow frequency (half hourly)
halfHourly = relHumid.copy()
halfHourly = halfHourly['DataValue'].resample('30min', how='first')

#%% Identify sunrise; select times three hours before sunrise
sunrise = np.sin((halfHourly.index.month-9)*3.14159/6)+6

predawn = halfHourly[(halfHourly.index.hour < sunrise) & 
                    (halfHourly.index.hour >= (sunrise-3))]
                    
#%% Subselect by relative humidity between 92 and 95%
zeroFlowTimes = predawn[(predawn > 92) &
                        (predawn < 95)]
                        
#%% Output to csv
zeroFlowTimes.to_csv('SagehornZeroFlowTimes.csv')