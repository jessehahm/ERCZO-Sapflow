
##############################################################

# readSapflow.py - Jesse Hahm

# Date: December 2015

#

# Purpose:  

# code to read in sapflow data from ICT data loggers. 
'''Reads files into dataframes
Strips maximum, minimum, and average daily values included in the output
Interprets the date-time column and sets it as data frame index
‘outer’ merges the four dataframes into one dataframe on the dataframe index (timestamp)
Subtracts an hour because dataloggers are on DLS time 
'''
##############################################################
## Import required libraries
import functools
import pandas as pd


def readCSV(allFiles, saveCSV):

	dfs = dict()
	
	for file_ in allFiles:
		dfs[file_] = pd.read_csv(str('Data\\' + file_ + '.csv'),sep=',', skiprows=[1])

	##Deal with one logger that has date time in separate columns... 
	dfs['RivNorth']['  date      time  '] = dfs['RivNorth'].iloc[:,0].map(str) + dfs['RivNorth'].iloc[:,1].map(str)
	dfs['RivNorth'].drop(dfs['RivNorth'].columns[[0,1]], axis=1, inplace=True)
	
	for df in dfs:
		dfs[df].rename(columns={'  date      time  ': 'datetime'}, inplace=True)
		#Drop logger-added statistic rows, 
		dfs[df] = dfs[df][~dfs[df].datetime.str.contains('maximum')]
		dfs[df] = dfs[df][~dfs[df].datetime.str.contains('minimum')]
		dfs[df] = dfs[df][~dfs[df].datetime.str.contains('average')]
		#convert date-time column to datetime data type, set index to datetime column
		dfs[df]['datetime'] =  pd.to_datetime(dfs[df]['datetime'], dayfirst=True)
		dfs[df].set_index(['datetime'], drop=True, inplace=True)
		#output has spurious extra column at end; drop it    
		dfs[df].drop(dfs[df].columns[-1], axis=1, inplace=True) 

	merge = functools.partial(pd.merge, left_index=True, right_index=True, how='outer')
	sapflow = functools.reduce(merge, dfs.values())
	sapflow.shape
	sapflow.index = sapflow.index - pd.Timedelta(1, 'h')
	## Force sensor data to numeric datatype
	sapflow = sapflow.apply(pd.to_numeric, args=('coerce',))
	
	## Trim whitespace from column headers
	sapflow.columns = sapflow.columns.map(str.strip)

	if saveCSV:
		sapflow.to_csv('Data\sapflow.csv')
		
	return sapflow