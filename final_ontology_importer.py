from matplotlib.ticker import MultipleLocator
from matplotlib.colors import ListedColormap
from matplotlib import ticker
from owlready2 import *

import numpy as np
import pandas as pd
import matplotlib.pyplot as plot


#The purpose of this module is to import an ontology .OWL model and convert it into a DSM matrix which shows connections and relationships between classes within the model.
def ontology_importer(ontology_file_name):

    # onto_path.append("C:/Users/path/to/folder")

    ontology = get_ontology(ontology_file_name).load()
    # ontology = get_ontology("path/to/folder/urn_webprotege_ontology_4ff9270f-7edf-46c7-8aa6-6220043778bb.owl").load()

    ontology.load(only_local=True)

    classes = list(ontology.classes())
    object_props = list(ontology.object_properties())
    data_props = list(ontology.data_properties())

    # print(classes)
    # print(object_props)
    # print(data_props)

    entity_count = len(classes)
    entity_list = ''
    entity_reference = []
    current_entity = 1

    #This section will create a list with comma separated names for each class in the ontology.  This will be used to create a dataframe at a later time
    for entity in classes:
        if len(entity_list) == 0:
            entity_list = str(entity.name)
        else:
            entity_list = entity_list + ',' + str(entity.name)
        entity_reference.append(entity.name)
        current_entity = current_entity + 1

    #This section will create a list with comma separated names for each data property in the ontology.  This will be used to create a dataframe at a later time    
    # for entity in data_props:
    #     if len(entity_list) == 0:
    #         entity_list = str(entity.name)
    #     else:
    #         entity_list = entity_list + ',' + str(entity.name)
    #     entity_reference.append(entity.name)
    #     current_entity = current_entity + 1

    entity_list = 'reference_num,class,' + entity_list + ',name,description,units,synonyms,sources'    
    columns = entity_list.split(',')    
    current_entity = 0
    relationship_list = []

    #This section will create the directional connectivity matrix and populate class descriptions, units, and synonyms
    for entity in classes:
        entity_entry = str(current_entity) + '\\' + entity.name
        attached = entity.is_a
        connected_str = ''
        for connected in attached:
            if hasattr(connected,'name') == True:
                if str(connected) != 'owl.Thing':    
                    connected_name = connected.value.name
                    # connection_pos = entity_reference.index(connection_name)
                    if len(connected_str) == 0:
                        connected_str = str(connected_name)
                    else:
                        connected_str = connected_str + '\\' + str(connected_name)
            elif hasattr(connected,'property') == True:
                if hasattr(connected.value,'name') == True:
                    connected_name = connected.value.name
                    # connection_pos = entity_reference.index(connection_name)
                    if len(connected_str) == 0:
                        connected_str = str(connected_name)
                    else:
                        connected_str = connected_str + '\\' + str(connected_name)
                else:
                    connected_property = connected.property
                    connected_name = connected_property.name
                    if len(connected_str) == 0:
                        connected_str = str(connected_name)
                    else:
                        connected_str = connected_str + '\\' + str(connected_name)
        for reference in entity_reference:
            if reference in connected_str:
                entity_entry = entity_entry + '\\1'
            else:
                entity_entry = entity_entry + '\\0'
        
                
        comments = entity.comment[0]
        comments_parsed = comments.split('\\\\')
        
        entity_name = comments_parsed[0]
        entity_description = comments_parsed[1]
        entity_units = comments_parsed[2]
        entity_synonyms = comments_parsed[3]
        entity_sources = comments_parsed[4]
        
        entity_entry = entity_entry + '\\' + entity_name + '\\' + entity_description + '\\' + entity_units + '\\' + entity_synonyms + '\\' + entity_sources
        relationship_list.append(entity_entry.split('\\'))    
        current_entity = current_entity + 1

    #Data properties have been removed because they do not provide uniquely identifying information
    # for entity in data_props:
    #     entity_entry = str(current_entity) + '\\' + entity.name
    #     # attached = entity.is_a
    #     # connected_str = ''
    #     # if len(connected_str) == 0:
    #     #     connected_str = str(connected_name)
    #     # else:
    #     #     connected_str = connected_str + '\\' + str(connected_name)
    #     # Data properties do not relate to other data properties and 
    #     for reference in entity_reference:
    #             entity_entry = entity_entry + '\\0'
        
    #     comments = entity.comment[0]
    #     comments_parsed = comments.split('\\\\')
        
    #     entity_name = comments_parsed[0]
    #     entity_description = comments_parsed[1]
    #     entity_units = comments_parsed[2]
    #     entity_synonyms = comments_parsed[3]
    #     entity_sources = comments_parsed[4]
        
    #     entity_entry = entity_entry + '\\' + entity_name + '\\' + entity_description + '\\' + entity_units + '\\' + entity_synonyms + '\\' + entity_sources
    #     relationship_list.append(entity_entry.split('\\'))    
    #     current_entity = current_entity + 1
                
    test = data_props[0]
    python_name = test._python_name
    name = test.label[0]

    ontology_relationships = pd.DataFrame(relationship_list, columns = columns)
    ontology_relationships.to_csv('ontology_relationships_one_way.csv', index=False)

    #Copy the one way relationships into a new dataframe
    ontology_relationships_two_way = ontology_relationships

    #Mirror the one way relationships into two way relationships.  This creates a symmetric system about the diagonal
    for i in ontology_relationships_two_way:
        if (i != 'reference_num') and (i != 'class') and (i != 'name') and (i != 'description') and (i != 'units') and (i != 'synonyms') and (i != 'sources'):
            entity_i_pos = entity_reference.index(i)
            for j in entity_reference:
                entity_j_pos = entity_reference.index(j) + 2
                entity_value = ontology_relationships_two_way[ontology_relationships_two_way.columns[entity_j_pos]][entity_i_pos]
                if int(entity_value) > 0:
                    reflected_i_pos = entity_reference.index(j)
                    reflected_j_pos = entity_reference.index(i) + 2
                    # ontology_relationships_two_way.iloc[reflected_i_pos][reflected_j_pos] = int(ontology_relationships_two_way.iloc[reflected_i_pos][reflected_j_pos]) + 1
                    ontology_relationships_two_way.iloc[reflected_i_pos][reflected_j_pos] = 1
    
    #Save the relationship diagram        
    ontology_relationships_two_way = pd.DataFrame(ontology_relationships_two_way, columns = columns)
    ontology_relationships_two_way.to_csv('ontology_relationships_two_way.csv', index=False) 

    #Plot the two way relationships
    num_classes = len(entity_reference)
    dsm_matrix = ontology_relationships_two_way[ontology_relationships_two_way.columns[2:(num_classes+2)][0:(num_classes)]]

    dsm_plot = np.array(dsm_matrix)
    dsm = pd.DataFrame(dsm_matrix)
    dsm = dsm.apply(pd.to_numeric)

    plot.tight_layout()
    figure, axes = plot.subplots(figsize=(10,10))

    color_map = ListedColormap(['w', 'w', 'w'])
    axes.matshow(dsm, cmap=color_map)
    plot.tick_params(axis='x', which='both', bottom=False, top=True, labelbottom=False)
    axes.xaxis.set_major_locator(ticker.FixedLocator(range(num_classes+1)))
    axes.set_xticklabels(columns[2:(num_classes+3)])
    plot.xticks(rotation=90,fontsize=8)
    axes.yaxis.set_major_locator(ticker.FixedLocator(range(num_classes+1)))
    axes.set_yticklabels(columns[2:(num_classes+3)])  
    #The next two lines of code are based on the Stack Overflow post by user Charelf at https://stackoverflow.com/questions/38973868/adjusting-gridlines-and-ticks-in-matplotlib-imshow
    #Written 5 May 2021, Accessed 4 November 2023.
    plot.hlines(y=np.arange(0, len(dsm))+0.5, xmin=np.full(len(dsm), 0)-0.5, xmax=np.full(len(dsm), len(dsm))-0.5, color="k", linewidth=0.5)
    plot.vlines(x=np.arange(0, len(dsm))+0.5, ymin=np.full(len(dsm), 0)-0.5, ymax=np.full(len(dsm), len(dsm))-0.5, color="k", linewidth=0.5)
    for i in range(len(dsm)):
        for j in range(len(dsm)):
            if int(dsm_plot[i,j]) == 1:
                text = axes.text(j,i,'x', ha='center', va='center', color='k')
    plot.yticks(fontsize=8)
    
    plot.subplots_adjust(bottom=0.00)

    #Save the file
    ontology_dsm = plot.savefig('ontology_dsm.jpg', dpi=1000)

    ontology_dsm
    
    print('Ontology imported')