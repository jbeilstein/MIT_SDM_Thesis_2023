import math
import matplotlib.pyplot as plot
import networkx as nx
import numpy as np
import pandas as pd

# data_file = 'parsed_requirements_2.csv'
data_file = 'data2024_cleaned.csv'

dataframe = pd.read_csv(data_file,sep=',')
#tree = dataframe.loc[(dataframe['id_num'] == 119) | (dataframe['logical_shall'] == True) | (dataframe['logical_should'] == True) | (dataframe['child_of'] != 0)]
# tree = dataframe.loc[(dataframe['logical_shall'] == True) | (dataframe['logical_should'] == True) | dataframe['associated_with'].str.len() > 0 ]

## This visualizes all relationships within the document
# tree = dataframe

## This visualizes all relationships with the exception of page numbers
tree = dataframe.loc[(dataframe['label_type'] != 'page_level')]


network = nx.from_pandas_edgelist(tree, 
                                  source = 'child_of', 
                                  target = 'id_num')
node_label = []
node_color = []
# list_associated = tree['associated_with'].unique()
list_child_of = tree['child_of'].unique()

for node in network:
    # if isinstance(node,list) == True:
    node_label.append(node)
    if math.isnan(node) == False:
        if node != 0:
        # if node not in [0,1,2]:
            temp = dataframe.loc[(dataframe['id_num'] == int(node))]
            
            ##The following statements can be used to highlight network nodes associated with various categories of requirements
            # if dataframe.iloc[int(node)]['mandatory'] == True:
            #     node_color.append('black')
            # elif dataframe.iloc[int(node)]['desired'] == True:
            #     node_color.append('black')
            # elif dataframe.iloc[int(node)]['optional'] == True:
            #     node_color.append('black')
            # elif dataframe.iloc[int(node)]['recommended'] == True:
            #     node_color.append('black')
            # else:
            #     node_color.append('black')
            
            ##Use this section if you want to identify functional requirements
            # if dataframe.iloc[int(node)]['functional'] == True:
            #     node_color.append('red')
            # elif dataframe.iloc[int(node)]['non_functional'] == True:
            #     node_color.append('orange')
            # else:
            #     node_color.append('black')
                
            ##Use this section if you want to identify non-functional requirements    
            if dataframe.iloc[int(node)]['non_functional'] == True:
                node_color.append('red')
            else:
                node_color.append('black')
            
            ##The following statements can be used to highlight network nodes associated with various parts of the CANSAT ontology
            # if dataframe.iloc[int(node)]['aero_mechanism/aero_brake'] == True:
            #     node_color.append('red')
            # else:
            #     node_color.append('black')
            
            # if dataframe.iloc[int(node)]['audio_beacon'] == True:
            #     node_color.append('red')
            # else:
            #     node_color.append('black')
            
            # if dataframe.iloc[int(node)]['camera'] == True:
            #     node_color.append('red')
            # else:
            #     node_color.append('black')
            
            # if dataframe.iloc[int(node)]['cansat/payload/probe'] == True:
            #     node_color.append('red')
            # else:
            #     node_color.append('black')   
                        
            # if dataframe.iloc[int(node)]['data/kinematics/telemetry'] == True:
            #     node_color.append('red')
            # else:
            #     node_color.append('black')
                
            # if dataframe.iloc[int(node)]['egg/compartment'] == True:
            #     node_color.append('red')
            # else:
            #     node_color.append('black')
                
            # if dataframe.iloc[int(node)]['electrical'] == True:
            #     node_color.append('red')
            # else:
            #     node_color.append('black')
                
            # if dataframe.iloc[int(node)]['ground_station'] == True:
            #     node_color.append('red')
            # else:
            #     node_color.append('black')
                
            # if dataframe.iloc[int(node)]['heat_shield'] == True:
            #     node_color.append('red')
            # else:
            #     node_color.append('black')
                
            # if dataframe.iloc[int(node)]['materials/mechanical'] == True:
            #     node_color.append('red')
            # else:
            #     node_color.append('black')
                
            # if dataframe.iloc[int(node)]['nose_cone'] == True:
            #     node_color.append('red')
            # else:
            #     node_color.append('black')
                
            # if dataframe.iloc[int(node)]['parachute'] == True:
            #     node_color.append('red')
            # else:
            #     node_color.append('black')
                
            # if dataframe.iloc[int(node)]['radio'] == True:
            #     node_color.append('red')
            # else:
            #     node_color.append('black')
                
            # if dataframe.iloc[int(node)]['rocket'] == True:
            #     node_color.append('red')
            # else:
            #     node_color.append('black')
                
            # if dataframe.iloc[int(node)]['sensors'] == True:
            #     node_color.append('red')
            # else:
            #     node_color.append('black')
                
            # if dataframe.iloc[int(node)]['software'] == True:
            #     node_color.append('red')
            # else:
            #     node_color.append('black')
            
        ##This is required to catch any nodes which are not classified
        else:
            node_color.append('black')
            
    # if node in list_associated:
    #     node_color.append('red')
    # elif node in list_child_of:
    #     node_color.append('green')
    # else:
    #     node_color.append('blue')
    
    ##This is required to catch any nodes which are not classified
    else:
        node_color.append('black')

plot.figure(figsize=(20,20))
     
nx.draw_kamada_kawai(network,
                     with_labels = True,
                    # pos,
                     node_color = node_color,
                     node_size = 25)

# positioning = nx.spring_layout(network, k=10, iterations=30)
# nx.draw_spring(network,
#                      with_labels = True,
#                     # pos = positioning,
#                      node_color = node_color,
#                      node_size = 1)

graph = plot.savefig('requirements_network.jpg', dpi=1000)
graph = plot.savefig('requirements_network.pdf', dpi=1000)

print(graph)
plot.clf()

### This visualizes ontologies
data_file = 'ontology.csv'

ontology_tree = pd.read_csv(data_file,sep=',')


ontology_network = nx.from_pandas_edgelist(ontology_tree, 
                                            source = 'component_id', 
                                            target = 'parent_id')

node_label = []
node_color = []

for node in ontology_network:
    # if isinstance(node,list) == True:
    node_label.append(node)
        
nx.draw_kamada_kawai(ontology_network,
                     with_labels = True,
                     node_size = 1)
ontology_graph = plot.savefig('ontology_network.jpg', dpi=1000)

print(ontology_graph)

