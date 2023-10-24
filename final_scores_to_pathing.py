import csv
import math
import numpy as np
import pandas as pd

adjacent_nodes = pd.DataFrame(adjacency_list_all, columns = ['adjacent_columns'])
adjacent_nodes.to_csv('adjacent_nodes.csv', index=False) 

data_file = 'ontology_relationships_two_way.csv'

ontology_dataframe = pd.read_csv(data_file,sep=',')

data_file = 'data2024_final.csv'

requirements_dataframe = pd.read_csv(data_file,sep=',')

req_ont_pairing = []
req_ont_pairing_column_names = ['req_id','ont_id','ont_name','spacy similarity','semantic similarity','source']