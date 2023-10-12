
import math
import numpy as np
import pandas as pd


data_file = 'data2024_cleaned.csv'

dataframe = pd.read_csv(data_file,sep= ',')
pathing = pd.DataFrame(np.nan,index=['0'],columns=['pathing'])
location = 0

for i, row in dataframe.iterrows():
    current_path = ''
    if row[0] != 0 and row[0] != '' and row[0] != 'id_num' and math.isnan(row[0]) != True:
        current_parent = row['child_of']
        current_path = current_parent
        if current_parent != 0:
            while current_parent != 0:
                temp_row = dataframe[dataframe['id_num'] == current_parent]
                current_parent = int(temp_row['child_of'])
                current_path = str(current_path) + '/' + str(current_parent)            
        pathing.loc[location] = str(current_path)
        location = location + 1

for i, row in dataframe.iterrows():
    if row[0] != 0 and row[0] != '' and row[0] != 'id_num' and math.isnan(row[0]) != True:
        current_parent = row['child_of']
        current_children = dataframe.iloc[int(current_parent)]['parent_of']
        if pd.isnull(current_children):
            current_children = str(row[0])
        else:
            current_children = str(current_children) + '/' + str(row[0])   
        dataframe.loc[(dataframe.id_num==current_parent),'parent_of'] = current_children
       
    
dataframe['pathing'] = pathing

dataframe.to_csv('data2024_pathing.csv', index = False)