from matplotlib.ticker import MultipleLocator

import csv
import math
import matplotlib.pyplot as plot
import pandas as pd

data_file = 'data2024_pathing.csv'

original_requirements_dataframe = pd.read_csv(data_file,sep=',')

temp = original_requirements_dataframe[original_requirements_dataframe['functional']==True]
req_id_list = list(temp['id_num'].unique())
req_column_names = ['req_id'] + req_id_list

data_file = 'req_dsm_pairing_token_comparison_functional.csv'

requirements_dataframe = pd.read_csv(data_file,sep=',')

req_req_dsm_pairing = []


for req1 in req_id_list:
    requirement_list = requirements_dataframe[requirements_dataframe['req1_id']==req1]
    entity_entry = str(req1)
    for req2 in req_id_list:
        temp_pairs = requirement_list[requirement_list['req2_id']==req2]
        count = (temp_pairs.similarity != 0).sum()
        if count != 0:
            entity_entry = entity_entry + ',1'
        else:
            entity_entry = entity_entry + ',0'
            
    req_req_dsm_pairing.append(entity_entry.split(','))        

req_relationships = pd.DataFrame(req_req_dsm_pairing, columns = req_column_names)
req_relationships.to_csv('req_relationships_one_way.csv', index=False)

i_pos=0
for i in req_relationships:
    if (i != 'req_id'):
        j_pos=0
        for j in req_id_list:
            value = req_relationships[req_relationships.columns[j_pos]][i_pos-1]
            if int(value) > 0:
                reflected_i = j_pos
                reflected_j = i_pos
                req_relationships.iloc[reflected_i][reflected_j] = 1
            j_pos = j_pos + 1
    i_pos = i_pos + 1
        
req_relationships_two_way = pd.DataFrame(req_relationships, columns = req_column_names)
req_relationships_two_way.to_csv('req_relationships_two_way.csv', index=False) 

num_classes = len(req_column_names)
dsm_matrix = req_relationships_two_way[req_relationships_two_way.columns[2:(num_classes+2)][0:(num_classes)]]

dsm = pd.DataFrame(dsm_matrix)
dsm = dsm.apply(pd.to_numeric)

plot.tight_layout()
figure, axes = plot.subplots(figsize=(10,10))

axes.matshow(dsm)
# axes.imshow(dsm)
# axes.set_xticklabels(columns[1:(num_classes+2)])
# axes.xaxis.set_major_locator(MultipleLocator(1))
plot.xticks(rotation=90,fontsize=8)
# axes.set_yticklabels(columns[1:(num_classes+2)])
# axes.yaxis.set_major_locator(MultipleLocator(1))
plot.yticks(fontsize=8)
plot.subplots_adjust(bottom=0.00)

ontology_dsm = plot.savefig('req_req_dsm.jpg', dpi=1000)

print(ontology_dsm)