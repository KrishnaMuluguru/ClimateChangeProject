# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 15:42:13 2019

@author: km4147
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from pandas.tseries.offsets import MonthEnd
import warnings

warnings.filterwarnings('ignore')

plt.style.use('fivethirtyeight')

CO2_Concentration = pd.read_csv('https://raw.githubusercontent.com/chaitu038/ClimateChangeProject1/master/Data-Folder/CO2_Concentration.csv',parse_dates = ['Date'],index_col=['Date','State'])

CO2_States_List = ['AK','CA','CO','FL','HI','OR','VI','WI','OK','UT','WA']

end_date_forecast = pd.to_datetime('2018-12-31')
start_date_backcast = pd.to_datetime('1975-01-31')

#params for best fit for each state: Find the code at the end
State_param = {'AK':{'param':(0,0,1),'season_param':(1,1,1,12)}
,'CA':{'param':(0,0,1),'season_param':(1,0,1,12)}
,'CO':{'param':(0,0,1),'season_param':(1,0,1,12)}
,'FL':{'param':(0,0,0),'season_param':(1,1,1,12)}
,'HI':{'param':(1,1,0),'season_param':(0,1,0,12)}
,'OK':{'param':(0,1,1),'season_param':(1,0,1,12)}
,'OR':{'param':(1,0,0),'season_param':(1,0,0,12)}
,'UT':{'param':(1,0,1),'season_param':(1,0,0,12)}
,'VI':{'param':(0,1,1),'season_param':(1,1,1,12)}
,'WA':{'param':(1,0,0),'season_param':(1,0,0,12)}
,'WI':{'param':(1,0,1),'season_param':(1,0,1,12)}}

CO2_Concentration_completed = pd.DataFrame()

def diff_months(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month + 1

for state in CO2_States_List:
    print('Processing: ',state)
    CO2_Concentration_State = CO2_Concentration[CO2_Concentration.index.get_level_values('State')==state].reset_index().set_index('Date')
    
    start_date_forecast = CO2_Concentration_State.index.max()+MonthEnd(1)
    end_date_backcast = CO2_Concentration_State.index.min()-MonthEnd(1)
    
    
    # Forecasting ------------------------------->
    CO2_Concentration_State_ForecastData = CO2_Concentration_State.sort_index(ascending=True)
    
    mod_forecast = sm.tsa.statespace.SARIMAX(CO2_Concentration_State_ForecastData.CO2_Concentration,
                                    order=State_param[state]['param'],
                                    seasonal_order=State_param[state]['season_param'],
                                    enforce_stationarity=False,
                                    enforce_invertibility=False)
    
    results_forecast = mod_forecast.fit()
    
    num_of_months_forecast = diff_months(end_date_forecast,start_date_forecast) 
    
    CO2_forecast = results_forecast.forecast(steps=num_of_months_forecast)
    
    if type(CO2_forecast.index) == 'pandas.core.indexes.datetimes.DatetimeIndex':
        pass
    else:
        CO2_forecast.index = pd.date_range(start=start_date_forecast,end=end_date_forecast,freq='M')
    
    
    ## Backcasting ----------------------------------------------->
    if start_date_backcast < end_date_backcast:
        CO2_Concentration_State_BackcastData = CO2_Concentration_State.sort_index(ascending=False)
    
        mod_backcast = sm.tsa.statespace.SARIMAX(CO2_Concentration_State_BackcastData.CO2_Concentration,
                                    order=State_param[state]['param'],
                                    seasonal_order=State_param[state]['season_param'],
                                    enforce_stationarity=False,
                                    enforce_invertibility=True)
    
        results_backcast = mod_backcast.fit()
    
        num_of_months_backcast = diff_months(end_date_backcast,start_date_backcast)
    
        CO2_backcast = results_backcast.forecast(steps=num_of_months_backcast)
    
        if type(CO2_backcast.index) == 'pandas.core.indexes.datetimes.DatetimeIndex':
            pass
        else:
            CO2_backcast.index = pd.date_range(start=start_date_backcast,end=end_date_backcast,freq='M')[::-1]
            CO2_backcast = CO2_backcast.sort_index(ascending=True)
        
        State_Backcast = CO2_backcast.to_frame('CO2_Concentration').assign(State=state)
        CO2_Concentration_State = State_Backcast.append(CO2_Concentration_State)
        
    CO2_Concentration_State.CO2_Concentration.plot()
    CO2_forecast.plot()
    plt.title(state)
    plt.show()
    
    State_Forecast = CO2_forecast.to_frame('CO2_Concentration').assign(State=state)
    
    CO2_Concentration_State = CO2_Concentration_State.append(State_Forecast)
    
    CO2_Concentration_completed = CO2_Concentration_completed.append(CO2_Concentration_State)
    
CO2_Concentration_completed.index.name = 'Date'
#CO2_Concentration_forecasted.to_csv(r'C:\Users\krish\DataScience\Project 1 - Climate Change\All_Clean_Data\CO2_Concentration_forecasted.csv')
CO2_Concentration_completed.to_csv(r'C:\Users\km4147\OneDrive - DHG LLP\Python Scripts\CO2_Concentration_forecasted.csv')





## Code to find the best fit param:
# =============================================================================
#     # Define the p, d and q parameters to take any value- 0 or 1
#     p = d = q = range(0, 2)
#     
#     # Generate all different combinations of p, q and q triplets
#     pdq = list(itertools.product(p, d, q))
#     
#     # Generate all different combinations of seasonal p, q and q triplets
#     seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
#     
#     warnings.filterwarnings('ignore') # specify to ignore warning messages
#     
#     i=1
#     for param in pdq:
#         for param_seasonal in seasonal_pdq:
#             try:
#                 mod = sm.tsa.statespace.SARIMAX(CO2_Concentration_State.CO2_Concentration,
#                                                 order=param,
#                                                 seasonal_order=param_seasonal,
#                                                 enforce_stationarity=False,
#                                                 enforce_invertibility=False)
#     
#                 results = mod.fit()
#     
#                 print('ARIMA{}x{}12 - AIC:{} - HQIC:{}'.format(param, param_seasonal, results.aic, results.hqic))
#                 
#                 start_date_forecast = CO2_Concentration_State.index.max()
#                 num_of_months = (end_date_forecast.year - start_date_forecast.year) * 12 + end_date_forecast.month - start_date_forecast.month
#                 
#                 CO2_forecast = results.forecast(steps=num_of_months)
#                 
#                 if type(CO2_forecast.index) == 'pandas.core.indexes.datetimes.DatetimeIndex':
#                     pass
#                 else:
#                     CO2_forecast.index = pd.date_range(start=start_date_forecast+MonthEnd(1),end=end_date_forecast,freq='M')
#                 
#                 CO2_forecast.plot()
#                 CO2_Concentration_State.CO2_Concentration.plot()
#                 plt.title(state)
#                 plt.show()
#     
#                 
#                 if i==1:
#                     least_aic = results.aic
#                     best_param = param
#                     best_param_seasonal = param_seasonal
#                 else:
#                     if results.aic < least_aic:
#                         least_aic = results.aic
#                         best_param = param
#                         best_param_seasonal = param_seasonal
#                     else:
#                         pass
#                 i=i+1
#             except:
#                 continue
#             
#     print('Best ARIMA{}x{}12 - AIC:{}'.format(best_param, best_param_seasonal, least_aic))
#     
# =============================================================================
