from matplotlib.ticker import MultipleLocator
from owlready2 import *

import pandas as pd
import matplotlib.pyplot as plot

onto_path.append("C:/Users/Beerstein/Documents/MIT/Thesis")
# onto_path.append("C:/Users/path/to/folder")

ontology = get_ontology("C:/Users/Beerstein/Documents/MIT/Thesis/urn_webprotege_ontology_4ff9270f-7edf-46c7-8aa6-6220043778bb.owl").load()
# ontology = get_ontology("path/to/folder/urn_webprotege_ontology_4ff9270f-7edf-46c7-8aa6-6220043778bb.owl").load()

ontology.load(only_local=True)

classes = list(ontology.classes())
object_props = list(ontology.object_properties())
data_props = list(ontology.data_properties())

print(classes)
print(object_props)
print(data_props)

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
for entity in data_props:
    if len(entity_list) == 0:
        entity_list = str(entity.name)
    else:
        entity_list = entity_list + ',' + str(entity.name)
    entity_reference.append(entity.name)
    current_entity = current_entity + 1

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

for entity in data_props:
    entity_entry = str(current_entity) + '\\' + entity.name
    # attached = entity.is_a
    # connected_str = ''
    # if len(connected_str) == 0:
    #     connected_str = str(connected_name)
    # else:
    #     connected_str = connected_str + '\\' + str(connected_name)
    # Data properties do not relate to other data properties and 
    for reference in entity_reference:
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
            
test = data_props[0]
python_name = test._python_name
name = test.label[0]
# comments = test.comment[0]
# split_comment = comments.split('\\')

ontology_relationships = pd.DataFrame(relationship_list, columns = columns)
ontology_relationships.to_csv('ontology_relationships_one_way.csv', index=False)

# ontology_relationships_matrix = ontology_relationships[ontology_relationships.columns[1:31]][0:30]
ontology_relationships_two_way = ontology_relationships

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
        
ontology_relationships_two_way = pd.DataFrame(ontology_relationships_two_way, columns = columns)
ontology_relationships_two_way.to_csv('ontology_relationships_two_way.csv', index=False) 

num_classes = len(entity_reference)
dsm_matrix = ontology_relationships_two_way[ontology_relationships_two_way.columns[2:(num_classes+2)][0:(num_classes)]]

dsm = pd.DataFrame(dsm_matrix)
dsm = dsm.apply(pd.to_numeric)

plot.tight_layout()
figure, axes = plot.subplots(figsize=(10,10))

axes.matshow(dsm)
# axes.imshow(dsm)
axes.set_xticklabels(columns[1:(num_classes+2)])
axes.xaxis.set_major_locator(MultipleLocator(1))
plot.xticks(rotation=90,fontsize=8)
axes.set_yticklabels(columns[1:(num_classes+2)])
axes.yaxis.set_major_locator(MultipleLocator(1))
plot.yticks(fontsize=8)
plot.subplots_adjust(bottom=0.00)

ontology_dsm = plot.savefig('ontology_dsm.jpg', dpi=1000)

print(ontology_dsm)