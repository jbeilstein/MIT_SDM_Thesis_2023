#This code will consolidate all of the requirement statements and their related elements

import math
import pandas as pd

data_file = 'structure.csv'

dataframe = pd.read_csv(data_file,sep = ',')


#This section will only leave sections which contain requirements or are referenced by requirement statements
requirement_dataframe = dataframe.loc[(dataframe['logical_shall'] == True) | (dataframe['logical_should'] == True) | (dataframe['associated_with'].str.len() > 0)]
#internal parent, sibling, child relationships go here


requirement_dataframe.to_csv('parsed_requirements.csv', index=False)

req_matches = []

