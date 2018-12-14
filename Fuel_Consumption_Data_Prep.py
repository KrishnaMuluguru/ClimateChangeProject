# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 22:10:33 2018

@author: krish
"""

import pandas as pd
from pandas.tseries.offsets import YearEnd


def InterpolatedValue(dt,st):
    dif = (Temp_Cons_Data.loc[pd.to_datetime(str(dt.year)+'-12-31'),st]-Temp_Cons_Data.loc[pd.to_datetime(str(dt.year-1)+'-12-31'),st])/12
    val = (Temp_Cons_Data.loc[pd.to_datetime(str(dt.year)+'-12-31'),st]/12) + (dif*mult_factors[dt.month])
    return val
    
Data_File = r'C:\Users\krish\DataScience\Project 1 - Climate Change\CO2_Data\Consumption_Monthly\Annual_Fuel_Consumption_1960-2017.csv'

Data_Parameters = ['PATCP','CLTCP']  # Identifier for Total Petroleum products consumption 

Fuel_Consumption_Data = pd.read_csv(Data_File)

Fuel_Consumption_Data = Fuel_Consumption_Data.loc[Fuel_Consumption_Data['MSN'].isin(Data_Parameters),:]
Fuel_Consumption_Data.drop(['Data_Status'],axis=1,inplace=True)

Fuel_Consumption_Data.set_index(['State','MSN'], inplace=True)
Fuel_Consumption_Data = Fuel_Consumption_Data.transpose()

Fuel_Consumption_Data.index = pd.to_datetime(Fuel_Consumption_Data.index,format='%Y') + YearEnd(1)
Temp_Cons_Data = Fuel_Consumption_Data

Fuel_Consumption_Data = Fuel_Consumption_Data.resample('M').mean()
Fuel_Consumption_Data = Fuel_Consumption_Data.drop(Fuel_Consumption_Data.index[0])


mult_factors = {}
for mnth,fctr in  enumerate(range(-55,65,10)):
    mult_factors[mnth+1] = fctr/100

for i in Fuel_Consumption_Data.index:
    for c in Fuel_Consumption_Data.columns:
        Fuel_Consumption_Data.loc[i,c] = InterpolatedValue(i,c)

Fuel_Consumption_Data = Fuel_Consumption_Data.stack().stack().reset_index()
Fuel_Consumption_Data.columns = ['Date','MSN','State','Consumption']
Fuel_Consumption_Data = Fuel_Consumption_Data.set_index(['Date','State','MSN'])
Fuel_Consumption_Data = Fuel_Consumption_Data.unstack()
Fuel_Consumption_Data.columns = ['Coal_Consumption','Petrol_Consumption']

Fuel_Consumption_Data.to_csv(r'C:\Users\krish\DataScience\Project 1 - Climate Change\All_Clean_Data\Fuel_Consumption.csv')