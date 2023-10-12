
import math
import pandas as pd


data_file = 'data2024.csv'

dataframe = pd.read_csv(data_file,sep= ',')

dataframe['mandatory'] = dataframe['mandatory'].fillna('False')
dataframe['desired'] = dataframe['desired'].fillna('False')
dataframe['optional'] = dataframe['optional'].fillna('False')
dataframe['recommended'] = dataframe['recommended'].fillna('False')
dataframe['functional'] = dataframe['functional'].fillna('False')
dataframe['non_functional'] = dataframe['non_functional'].fillna('False')
dataframe['cost'] = dataframe['cost'].fillna('False')
dataframe['schedule'] = dataframe['schedule'].fillna('False')
dataframe['deliverables'] = dataframe['deliverables'].fillna('False')
dataframe['personnel/staffing'] = dataframe['personnel/staffing'].fillna('False')

dataframe.to_csv('data2024_cleaned.csv', index = False)