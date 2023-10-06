import math
import matplotlib.pyplot as plot
import networkx as nx
import numpy as np
import pandas as pd

data_file = 'parsed_requirements_2.csv'

dataframe = pd.read_csv(data_file,sep=',')
#tree = dataframe.loc[(dataframe['id_num'] == 119) | (dataframe['logical_shall'] == True) | (dataframe['logical_should'] == True) | (dataframe['child_of'] != 0)]
tree = dataframe.loc[(dataframe['logical_shall'] == True) | (dataframe['logical_should'] == True) | dataframe['associated_with'].str.len() > 0 ]

network = nx.from_pandas_edgelist(tree, 
                                  source='child_of', 
                                  target='id_num')
labels = {}
color = []
list_associated = tree['associated_with'].unique()
list_child_of = tree['child_of'].unique()

for node in network:
    # if isinstance(node,list) == True:
    if node in list_associated:
        color.append('red')
    elif node in list_child_of:
        color.append('green')
    else:
        color.append('blue')
        
nx.draw_kamada_kawai(network,
                     node_color=color,
                     node_size=50)
graph = plot.savefig('requirements_network.jpg')

print(graph)
plot.clf()

### This visualizes ontologies
data_file = 'ontology.csv'

ontology_tree = pd.read_csv(data_file,sep=',')


ontology_network = nx.from_pandas_edgelist(ontology_tree, 
                                            source='component_id', 
                                            target='parent_id')

nx.draw_kamada_kawai(ontology_network,
                        node_size=50)
ontology_graph = plot.savefig('ontology_network.jpg')

print(ontology_graph)

