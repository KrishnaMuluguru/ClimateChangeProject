# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a program to load the data into DataFrames
"""

from IPython import get_ipython;   
get_ipython().magic('reset -sf')

import pandas as pd
import os
import numpy as np

def leftpadZeros(x,n):
    x = str(x)
    if len(x) < n:
        x = (n-len(x))*'0' + x
    return x

def removeStarChar(x):
    x=str(x)
    if x[-1] == r'*':
        x[-1] = ''
    return x
        
#Load US stations list 
stations_list_file = r'C:\Users\krish\DataScience\Project 1 - Climate Change\Data\GSOD\GSOD_AllData\isd-history.csv'

stations_list = pd.read_csv(stations_list_file)

stations_list['Station_Num'] = stations_list.USAF +'-'+stations_list.WBAN.apply(leftpadZeros,n=5)
stations_list = stations_list.set_index('Station_Num')

stations_list.drop(['USAF','WBAN','BEGIN','END','LAT','LON','ICAO','ELEV(M)','STATION NAME'],axis=1,inplace=True)

us_stations_list = stations_list[(stations_list.CTRY=='US') & (pd.notnull(stations_list.STATE))]
del us_stations_list['CTRY']
us_stations_list.columns = ['State']


# Load climate data for all US Stations

us_climate_data = pd.DataFrame()

for year in range(1975,2019):
    print('loading ' + str(year) + ' data')    
    data_folder_loc = r'C:\Users\krish\DataScience\Project 1 - Climate Change\Data\GSOD\GSOD_AllData\gsod_' + str(year)

    us_climate_data_year = pd.DataFrame()

    for root, dirs, files in os.walk(data_folder_loc):
        for filename in files:
            for station_id in us_stations_list.index.values:
                if filename[0:12] == station_id:
                    stn_climate_data = pd.read_csv(root+'\\'+filename,compression='gzip',delim_whitespace=True,skiprows=1,header=None,na_values=['9999.9','999.9'],parse_dates=[2])
                    us_climate_data_year = us_climate_data_year.append(stn_climate_data)
                    
    us_climate_data_year.columns = ['Station', 'SubStn', 'Date', 'TempAVG', 'Remove1', 'DewPoint', 'Remove2', 'SeaLevelPressure', 'Remove3', 'StationPressure', 'Remove4', 'Visibility', 'Remove5', 'WindSpeed', 'Remove6', 'WindSpeedMax', 'WindGust', 'TempMAX', 'TempMIN', 'Precipitation', 'SnowDepth', 'FRSHTT']

    for i in range(1,7):
        del us_climate_data_year['Remove'+str(i)]
    
    us_climate_data_year.drop(['SeaLevelPressure','StationPressure','Visibility','WindSpeed','WindSpeedMax','WindGust','SnowDepth','Precipitation'],axis=1,inplace=True)
    
    us_climate_data_year['Station_Num'] = us_climate_data_year.Station.apply(leftpadZeros,n=6) +'-'+us_climate_data_year.SubStn.apply(leftpadZeros,n=5)
    us_climate_data_year.drop(['Station','SubStn'],axis=1,inplace=True)
    
    us_climate_data_year['FRSHTT'] = us_climate_data_year.FRSHTT.apply(leftpadZeros,n=6)
    us_climate_data_year['TempMAX'] = pd.to_numeric(us_climate_data_year.TempMAX.str.strip('*'))
    us_climate_data_year['TempMIN'] = pd.to_numeric(us_climate_data_year.TempMIN.str.strip('*'))
        

    us_climate_data_year[['Blank1','Fog','Rain','Snow','Hail','Thunder','Tornado','Blank2']] = us_climate_data_year['FRSHTT'].str.split('',expand=True)
    us_climate_data_year.drop(['Blank1','Blank2','Fog','FRSHTT'],axis=1,inplace=True)
    
    us_climate_data_year['Rain'] = pd.to_numeric(us_climate_data_year['Rain'])
    us_climate_data_year['Snow'] = pd.to_numeric(us_climate_data_year['Snow'])
    us_climate_data_year['Hail'] = pd.to_numeric(us_climate_data_year['Hail'])
    us_climate_data_year['Thunder'] = pd.to_numeric(us_climate_data_year['Thunder'])
    us_climate_data_year['Tornado'] = pd.to_numeric(us_climate_data_year['Tornado'])
    
    us_climate_data_year.dropna(how='any')
    
    dict_aggregation = {'TempAVG':np.mean,'TempMAX':np.mean,'TempMIN':np.mean,'Rain':np.sum,'Snow':np.sum,'Hail':np.sum,'Thunder':np.sum,'Tornado':np.sum}
    us_climate_data_year = us_climate_data_year.set_index('Date').groupby('Station_Num').resample(rule='M').agg(dict_aggregation)
    us_climate_data_year = us_climate_data_year.reset_index().set_index('Station_Num')
    
    us_climate_data_year = pd.merge(us_climate_data_year,us_stations_list,on='Station_Num',how='inner')
#    us_climate_data_year.to_csv(r'C:\Users\krish\DataScience\Project 1 - Climate Change\Data\GSOD\GSOD_Clean_Data\GSOD_Clean_'+str(year)+'.csv')
    
    us_climate_data_year = us_climate_data_year.reset_index().set_index('Date','State').drop(['Station_Num'],axis=1)
    
    
    us_climate_data_year = us_climate_data_year.groupby(['Date','State']).agg(dict_aggregation)
    
    us_climate_data_year[['TempMAX','TempAVG','TempMIN']] = us_climate_data_year[['TempMAX','TempAVG','TempMIN']].interpolate()
       
    us_climate_data = us_climate_data.append(us_climate_data_year)
    
    
us_climate_data.to_csv(r'C:\Users\krish\DataScience\Project 1 - Climate Change\All_Clean_Data\GSOD_All_Data_no_outliers.csv')
