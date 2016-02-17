##############################################################
# databaseQuery.py
# Author: Collin Bode; modified by Jesse Hahm
# Date: May 10, 2014 (original); January 2015
##############################################################import pandas as pd
import matplotlib.pyplot as plt
import platform
import pandas.io.sql as ps
import MySQLdb
import datetime as dt
import os#grab user/pw from gitignored filef = open('pw.pwd')lines = f.readlines()username = lines[0]username = username.rstrip('\n')password = lines[1]

def odmquery(datestart,dateend,dsid,nobad):
    # NOTE: this excludes bad data. To include bad data, remove Qualifier sql
     
    # database connection
    hostname = "gall.berkeley.edu"   # "wanda.berkeley.edu"
       
    conn = MySQLdb.connect(host=hostname, db="odm", user=username, passwd=password)
    
    # Construct SQL query
    sql = 'SELECT DV.LocalDateTime, DV.DataValue FROM datavalues2 DV, qualifiers Q WHERE DV.LocalDateTime >= "'+datestart+'" AND DV.LocalDateTime <= "'+dateend+'" AND (DV.DatastreamID = "'+dsid+'" AND DV.QualifierID = Q.QualifierID) '
    if(nobad == True):
        sql += 'AND (Q.QualifierCode not like "X%") '
    sql += 'ORDER BY DV.LocalDateTime'

    # Pull data from odm sensor database into Pandas Dataframe
    df = ps.read_sql(sql,con=conn)
    conn.close()
    
    # Set Datetime as index

    df.set_index(['LocalDateTime'],inplace=True)
   # Save to file in case working offline
    #df.to_csv(path+'precip_wy'+str(year)+'.csv')
    
    return df
    