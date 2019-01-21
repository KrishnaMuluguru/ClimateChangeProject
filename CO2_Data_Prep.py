# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 21:38:08 2018

@author: krish
"""

import os
import pandas as pd
from pandas.tseries.offsets import MonthEnd

# Prepare CO2 Concentration Data

def get_line_number(phrase, file_name):
    with open(file_name) as f:
        for i, line in enumerate(f, 1):
            if phrase in line:
                return i

CO2_Concentration_Dir = r'C:\Users\krish\DataScience\Project 1 - Climate Change\Data\CO2_Data\Concentration_Monthly'

CO2_Conc_Data = pd.DataFrame()
for root,dirs,files in os.walk(CO2_Concentration_Dir):
    for CO2_file in files:
        skip_num_lines = get_line_number('data_fields',root+'\\'+CO2_file)
        CO2_Conc_Data_State = pd.read_csv(root+'\\'+CO2_file,header=None,delim_whitespace=True,skiprows=skip_num_lines)
        CO2_Conc_Data_State.columns = ['State','Year','Month','CO2_Concentration']
        CO2_Conc_Data_State['State'] = CO2_file[4:6]
        CO2_Conc_Data_State['Date'] = pd.to_datetime(CO2_Conc_Data_State['Year'].astype(str)+CO2_Conc_Data_State['Month'].astype(str), format='%Y%m') + MonthEnd(1)
        CO2_Conc_Data_State = CO2_Conc_Data_State.set_index(['State','Date']).drop(['Year','Month'],axis=1)
        CO2_Conc_Data = CO2_Conc_Data.append(CO2_Conc_Data_State)

CO2_Conc_Data.to_csv(r'C:\Users\krish\DataScience\Project 1 - Climate Change\All_Clean_Data\CO2_Concentration.csv')

