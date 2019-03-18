# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 18:04:47 2018

@author: krish
"""

import pandas as pd
from pandas.tseries.offsets import YearEnd

Land_Data_Fl = r'C:\Users\krish\DataScience\Project 1 - Climate Change\Data\Forest_Data\MajorLandUse.csv'
State_Code_Fl = r'C:\Users\krish\DataScience\Project 1 - Climate Change\Data\50_us_states_all_data.csv'
Land_Use_Data = pd.read_csv(Land_Data_Fl,usecols=['Region or State','Year','Forest-use land (all)','Land in urban areas'],na_values='N.A.')
State_Code_Data = pd.read_csv(State_Code_Fl)

Land_Use_Data = pd.merge(left=Land_Use_Data,right=State_Code_Data,left_on='Region or State',right_on='State Name',how='inner')

Land_Use_Data.drop(['Region or State','State Name'],axis=1, inplace=True)

Land_Use_Data.columns = ['Date','Forest_Land','Urban_Land','State']

Land_Use_Data = Land_Use_Data.set_index('Date')

Land_Use_Data.index = pd.to_datetime(Land_Use_Data.index,format='%Y') + YearEnd(1)
Land_Use_Data = Land_Use_Data.pivot(columns='State',values=['Forest_Land','Urban_Land'])
Land_Use_Data = Land_Use_Data.dropna(how='any')

Land_Use_Data = Land_Use_Data.resample('M').interpolate().round(0)
Land_Use_Data = Land_Use_Data.drop(Land_Use_Data.index[0])

Land_Use_Data = Land_Use_Data.stack().stack().reset_index()
Land_Use_Data.columns = ['Date','State','Land_Type','Area']
Land_Use_Data = Land_Use_Data.set_index(['Date','State','Land_Type']).unstack()
Land_Use_Data.columns = ['Forest_Area','Urban_Area']
Land_Use_Data.to_csv(r'C:\Users\krish\DataScience\Project 1 - Climate Change\All_Clean_Data\Land_Use_Data.csv')

# =============================================================================
# Resample_Land_Use = pd.DataFrame()
# 
# for state_code in State_Code_Data['State Code']:
#     State_Land_Use = Land_Use_Data.loc[Land_Use_Data.State == state_code,:]
#     
#     State_Land_Use = State_Land_Use.resample('M').interpolate()
#     Resample_Land_Use = Resample_Land_Use.append(State_Land_Use)
#     
#     
# 
# =============================================================================
