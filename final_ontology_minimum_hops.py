import csv
import math
import numpy as np
import pandas as pd

data_file = 'ontology_relationships_two_way.csv'

ontology_dataframe = pd.read_csv(data_file,sep=',')
ontology_dataframe = ontology_dataframe.drop('reference_num',axis=1)
ontology_dataframe = ontology_dataframe.drop('class',axis=1)
ontology_dataframe = ontology_dataframe.drop('name',axis=1)
ontology_dataframe = ontology_dataframe.drop('description',axis=1)
ontology_dataframe = ontology_dataframe.drop('units',axis=1)
ontology_dataframe = ontology_dataframe.drop('synonyms',axis=1)
ontology_dataframe = ontology_dataframe.drop('sources',axis=1)

height = ontology_dataframe.shape[0]
width = ontology_dataframe.shape[0]

columns = list(range(0,width))
blank = np.zeros(shape=(height,width))
ontology_pathing_two_way = pd.DataFrame(blank, columns = columns)
ontology_pathing_two_way = ontology_pathing_two_way.replace(int(0),np.nan)

nans_remaining = height * width
#This will step through and find the single-hop shortest paths
for ont1_i, ont1_row in ontology_dataframe.iterrows():
    # if ont_row['component_id'] != '' and ont_row['component_id'] != 'id_num' and math.isnan(ont_row['component_id']) != True:
    for ont2_i, ont2_row in ontology_dataframe.iterrows():
            # if ont_row['component_id'] != '' and ont_row['component_id'] != 'id_num' and math.isnan(ont_row['component_id']) != True:
        if ont1_i != ont2_i:
            if (math.isnan(ontology_pathing_two_way.iloc[ont1_i][ont2_i]) == True) and (int(ontology_dataframe.iloc[ont1_i][ont2_i]) == 1):        
                ontology_pathing_two_way.iloc[ont1_i][ont2_i] = ont2_i
                nans_remaining = nans_remaining - 1
                
while nans_remaining > len(columns):    
    for ont1_i, ont1_row in ontology_dataframe.iterrows():
        # if ont_row['component_id'] != '' and ont_row['component_id'] != 'id_num' and math.isnan(ont_row['component_id']) != True:
        for ont2_i, ont2_row in ontology_dataframe.iterrows():
                # if ont_row['component_id'] != '' and ont_row['component_id'] != 'id_num' and math.isnan(ont_row['component_id']) != True:
            if ont1_i != ont2_i:
                if (math.isnan(ontology_pathing_two_way.iloc[ont1_i][ont2_i]) == True): 
                    
                    temp_dataframe = ontology_pathing_two_way[ontology_pathing_two_way[ont2_i].notnull()]   
                    if temp_dataframe.empty != True:
                        ontology_pathing_two_way.iloc[ont1_i][ont2_i] = ont2_i
                        nans_remaining = nans_remaining - 1
    
ontology_pathing_two_way = pd.DataFrame(ontology_pathing_two_way, columns = columns)
ontology_pathing_two_way.to_csv('ontology_shortest_paths_two_way.csv', index=False) 


