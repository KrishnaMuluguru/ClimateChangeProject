import pandas as pd

CO2_Concentration = pd.read_csv('https://raw.githubusercontent.com/chaitu038/ClimateChangeProject1/master/Data-Folder/CO2_Concentration_forecasted.csv',parse_dates = ['Date'])
States_List = pd.read_excel('https://raw.githubusercontent.com/chaitu038/ClimateChangeProject1/master/Data-Folder/State_Regions.xlsx')

Complete_CO2_Data = pd.DataFrame()

for state in States_List.State:
    Complete_CO2_Data = Complete_CO2_Data.append(pd.DataFrame({'Date':pd.date_range(start=pd.to_datetime('1975-01-31'),end=pd.to_datetime('2018-12-31'),freq='M'),'State':state}),ignore_index=True)


Complete_CO2_Data = pd.merge(left=Complete_CO2_Data,right=CO2_Concentration,how='left',on=['Date','State'])

CO2_Mean = Complete_CO2_Data.groupby(by=['Date']).mean().reset_index()

Complete_CO2_Data = pd.merge(left=Complete_CO2_Data,right=CO2_Mean,how='left',on=['Date'])

Complete_CO2_Data['CO2_Concentration'] = Complete_CO2_Data.apply(lambda row: row['CO2_Concentration_y'] if pd.isna(row['CO2_Concentration_x']) else row['CO2_Concentration_x'],axis=1)
Complete_CO2_Data = Complete_CO2_Data.drop(['CO2_Concentration_x','CO2_Concentration_y'],axis=1)
Complete_CO2_Data = Complete_CO2_Data.set_index(['Date','State'])

Complete_CO2_Data.to_csv(r'C:\Users\krish\OneDrive\Documents\Python Scripts\ClimateChangeAnalysis\Clean_Data\CO2_Concentration_Completed.csv')

