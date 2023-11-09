import csv
import math
import numpy as np
import pandas as pd

#The ontology mapper will convert the DSM into a set of adjacency vectors which will be used by later modules of the algorithm

def ontology_mapper():
    data_file = 'ontology_relationships_two_way.csv'
    ontology_dataframe = pd.read_csv(data_file,sep=',')
    ontology_dataframe = ontology_dataframe.drop('reference_num',axis=1)
    ontology_dataframe = ontology_dataframe.drop('class',axis=1)
    ontology_dataframe = ontology_dataframe.drop('name',axis=1)
    ontology_dataframe = ontology_dataframe.drop('description',axis=1)
    ontology_dataframe = ontology_dataframe.drop('units',axis=1)
    ontology_dataframe = ontology_dataframe.drop('synonyms',axis=1)
    ontology_dataframe = ontology_dataframe.drop('sources',axis=1)
    column_names = ontology_dataframe.columns

    height = ontology_dataframe.shape[0]
    width = ontology_dataframe.shape[0]

    columns = list(range(0,width))
    blank = np.zeros(shape=(height,width))
    ontology_pathing_two_way = pd.DataFrame(blank, columns = columns)
    ontology_pathing_two_way = ontology_pathing_two_way.replace(int(0),np.nan)

    #Cycle through every node in the ontology and find all adjacent nodes
    
    adjacency_list_all = []
    for ont1_i, ont1_row in ontology_dataframe.iterrows():
        ont_name = column_names[ont1_i]
        source_list = str(ont1_i)  + '_' + ont_name
        adjacency_list_row = ''
        for column in columns:
            if ontology_dataframe.iloc[ont1_i][column] == 1:
                if len(adjacency_list_row) != 0:
                    adjacency_list_row = adjacency_list_row + '\\' + str(column) + '_' + column_names[column]
                else:
                    adjacency_list_row = str(column) + '_' + column_names[column]
            if ont1_i == 40:
                x=1        
        adjacency_list_all.append([source_list, adjacency_list_row])
                        
    adjacent_nodes = pd.DataFrame(adjacency_list_all, columns = ['ontology_column','adjacent_columns'])
    adjacent_nodes.to_csv('adjacent_nodes.csv', index=False)
    print('Ontology mapped') 


