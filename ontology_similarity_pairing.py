from matplotlib.ticker import MultipleLocator

import csv
import math
import matplotlib.pyplot as plot
import pandas as pd
import spacy

nlp = spacy.load("en_core_web_lg")

data_file = 'ontology_relationships_two_way.csv'

ont_dataframe = pd.read_csv(data_file,sep=',')

data_file = 'data2024_pathing.csv'

requirements_dataframe = pd.read_csv(data_file,sep=',')

data_file = 'req_to_ont_token_comparison.csv'

req_to_ont_dataframe = pd.read_csv(data_file,sep=',')

req_ont_score_pairing = []
req_ont_score_pairing_column_names = ['req_id','ont_id','ont_name','name_similarity','name_score','description_similarity','description_score','units_similarity','units_score','synonyms_similarity','synonyms_score']

#This section will iterate through every unique requirement ID and then every paired ontological entity
for req in req_to_ont_dataframe['req_id'].unique():
    candidate_pairs = req_to_ont_dataframe[req_to_ont_dataframe['req_id'] == req]

    for ont in candidate_pairs['ont_id'].unique():
        name_list = []
        name_total = 0
        description_list = []
        description_total = 0
        units_list = []
        units_total = 0
        synonyms_list = []
        synonyms_total = 0
        for temp_i, temp_pair in candidate_pairs[candidate_pairs['ont_id'] == ont].iterrows():
            if temp_i != 0:
                if temp_pair['source'] == 'ontology name':
                    name_list.append(float(temp_pair['similarity']))
                    name_total = name_total + temp_pair['similarity']
                elif temp_pair['source'] == 'ontology description':
                    description_list.append(float(temp_pair['similarity']))
                    description_total = description_total + temp_pair['similarity']    
                elif temp_pair['source'] == 'ontology units':
                    units_list.append(float(temp_pair['similarity']))  
                    units_total = units_total + temp_pair['similarity']   
                elif temp_pair['source'] == 'ontology synonyms':
                    synonyms_list.append(float(temp_pair['similarity']))   
                    synonyms_total = synonyms_total + temp_pair['similarity']  
        score_entry = [temp_pair['req_id'], temp_pair['ont_id'], temp_pair['ont_name'], name_list, name_total, description_list, description_total, units_list, units_total, synonyms_list, synonyms_total]
        req_ont_score_pairing.append(score_entry)
                        
req_ont_token_pairing = pd.DataFrame(req_ont_score_pairing, columns = req_ont_score_pairing_column_names)
req_ont_token_pairing.to_csv('req_to_ont_scores.csv', index=False)

ontology_dataframe_columns = list(ont_dataframe.columns)
num_cols = len(ontology_dataframe_columns)
req_to_ont_dsm_columns = ['req_id'] + ontology_dataframe_columns[2:(num_cols-5)]
req_to_ont_dsm = []
req_to_ont_name_dsm = []
req_to_ont_description_dsm = []
req_to_ont_units_dsm = []
req_to_ont_synonyms_dsm = []
req_list = ()

for req_i, req_row in requirements_dataframe.iterrows():
    if req_i !=0 and req_row['id_num'] != '' and req_row['id_num'] != 'id_num' and math.isnan(req_row['id_num']) != True:
        # Enable this if you only want to look at functional requirements
        if (req_row['functional'] == True):
            req_id = req_row['id_num']
            if len(req_list) == 0:
                req_list = str(req_id)
            else:
                req_list = req_list + "," + str(req_id)
            
            #This section gets a list of all unique ontology id's paired with the current requirement ID.   
            req_ont_pairs = req_ont_token_pairing[req_ont_token_pairing['req_id'] == req_id]
            ont_list = list(req_ont_pairs['ont_id'].unique())
            
            #This section clears strings which will be used to track which aspect of a description contributed to the pairing
            #This tracks association between a requirement id and an ontology id
            dsm_entry = str(req_id) 
            name_dsm_entry = str(req_id)
            description_dsm_entry = str(req_id)
            units_dsm_entry = str(req_id)
            synonyms_dsm_entry = str(req_id)
               
            for i in range(0,(len(req_to_ont_dsm_columns)-1)):
                if i in ont_list:
                    names = 0
                    descriptions = 0
                    units = 0
                    synonyms = 0
                    dsm_entry = dsm_entry + ',1'
                    temp_pairs = req_ont_pairs[req_ont_pairs['ont_id']==i]
                    names = (temp_pairs.name_score != 0).sum()
                    descriptions = (temp_pairs.description_score != 0).sum()
                    units = (temp_pairs.units_score != 0).sum()
                    synonyms = (temp_pairs.synonyms_score != 0).sum()
                    if names != 0:
                        name_dsm_entry = name_dsm_entry + ',1'
                    else:
                        name_dsm_entry = name_dsm_entry + ',0'
                    if descriptions != 0:
                        description_dsm_entry = description_dsm_entry + ',1'
                    else:
                        description_dsm_entry = description_dsm_entry + ',0'
                    if units != 0:
                        units_dsm_entry = units_dsm_entry + ',1'
                    else:
                        units_dsm_entry = units_dsm_entry + ',0'
                    if synonyms != 0:
                        synonyms_dsm_entry = synonyms_dsm_entry + ',1'
                    else:
                        synonyms_dsm_entry = synonyms_dsm_entry + ',0'
                        
                else:
                    dsm_entry = dsm_entry + ',0'
                    name_dsm_entry = name_dsm_entry + ',0'
                    description_dsm_entry = description_dsm_entry + ',0'
                    units_dsm_entry = units_dsm_entry + ',0'
                    synonyms_dsm_entry = synonyms_dsm_entry + ',0'
                    
            dsm_entry_list = dsm_entry.split(',') 
            dsm_name_entry_list = name_dsm_entry.split(',')
            dsm_description_entry_list = description_dsm_entry.split(',')
            dsm_units_entry_list = units_dsm_entry.split(',')
            dsm_synonyms_entry_list = synonyms_dsm_entry.split(',')
            req_to_ont_dsm.append(dsm_entry_list)
            req_to_ont_name_dsm.append(dsm_name_entry_list)
            req_to_ont_description_dsm.append(dsm_description_entry_list)
            req_to_ont_units_dsm.append(dsm_units_entry_list)
            req_to_ont_synonyms_dsm.append(dsm_synonyms_entry_list)

req_list = req_list.split(',')

##This will save the csv and print the dsm linking requirements to any aspect of an ontology
req_to_ont_dsm_dataframe = pd.DataFrame(req_to_ont_dsm, columns = req_to_ont_dsm_columns)
req_to_ont_dsm_dataframe.to_csv('req_to_ont_dsm.csv', index=False) 
            
req_to_ont_dsm_dataframe = req_to_ont_dsm_dataframe.drop('req_id',axis=1)
req_to_ont_dsm_dataframe = req_to_ont_dsm_dataframe.apply(pd.to_numeric)

plot.tight_layout()
figure, axes = plot.subplots(figsize=(15,15))

axes.matshow(req_to_ont_dsm_dataframe)
# axes.imshow(dsm)
axes.set_xticklabels(req_to_ont_dsm_columns[0:(len(req_to_ont_dsm_columns))])
axes.xaxis.set_major_locator(MultipleLocator(1))
plot.xticks(rotation=90,fontsize=6)
axes.set_yticklabels(req_list)
axes.yaxis.set_major_locator(MultipleLocator(1))
plot.yticks(fontsize=6)
plot.subplots_adjust(bottom=0.00)

ontology_dsm = plot.savefig('req_to_ontology_dsm.jpg', dpi=1000)

print(ontology_dsm)
plot.clf()

##This will print the dsm linking requirements to ontology names
req_to_ont_dsm_dataframe = pd.DataFrame(req_to_ont_name_dsm, columns = req_to_ont_dsm_columns)
req_to_ont_dsm_dataframe.to_csv('req_to_ont_name_dsm.csv', index=False) 
            
req_to_ont_dsm_dataframe = req_to_ont_dsm_dataframe.drop('req_id',axis=1)
req_to_ont_dsm_dataframe = req_to_ont_dsm_dataframe.apply(pd.to_numeric)

plot.tight_layout()
figure, axes = plot.subplots(figsize=(15,15))

axes.matshow(req_to_ont_dsm_dataframe)
# axes.imshow(dsm)
axes.set_xticklabels(req_to_ont_dsm_columns[0:(len(req_to_ont_dsm_columns))])
axes.xaxis.set_major_locator(MultipleLocator(1))
plot.xticks(rotation=90,fontsize=6)
axes.set_yticklabels(req_list)
axes.yaxis.set_major_locator(MultipleLocator(1))
plot.yticks(fontsize=6)
plot.subplots_adjust(bottom=0.00)

ontology_name_dsm = plot.savefig('req_to_ontology_name_dsm.jpg', dpi=1000)

print(ontology_name_dsm)
plot.clf()

##This will print the dsm linking requirements to ontology descriptions
req_to_ont_dsm_dataframe = pd.DataFrame(req_to_ont_description_dsm, columns = req_to_ont_dsm_columns)
req_to_ont_dsm_dataframe.to_csv('req_to_ont_description_dsm.csv', index=False) 
            
req_to_ont_dsm_dataframe = req_to_ont_dsm_dataframe.drop('req_id',axis=1)
req_to_ont_dsm_dataframe = req_to_ont_dsm_dataframe.apply(pd.to_numeric)

plot.tight_layout()
figure, axes = plot.subplots(figsize=(15,15))

axes.matshow(req_to_ont_dsm_dataframe)
# axes.imshow(dsm)
axes.set_xticklabels(req_to_ont_dsm_columns[0:(len(req_to_ont_dsm_columns))])
axes.xaxis.set_major_locator(MultipleLocator(1))
plot.xticks(rotation=90,fontsize=6)
axes.set_yticklabels(req_list)
axes.yaxis.set_major_locator(MultipleLocator(1))
plot.yticks(fontsize=6)
plot.subplots_adjust(bottom=0.00)

ontology_description_dsm = plot.savefig('req_to_ontology_description_dsm.jpg', dpi=1000)

print(ontology_description_dsm)
plot.clf()

##This will print the dsm linking requirements to ontology units
req_to_ont_dsm_dataframe = pd.DataFrame(req_to_ont_units_dsm, columns = req_to_ont_dsm_columns)
req_to_ont_dsm_dataframe.to_csv('req_to_ont_units_dsm.csv', index=False) 
            
req_to_ont_dsm_dataframe = req_to_ont_dsm_dataframe.drop('req_id',axis=1)
req_to_ont_dsm_dataframe = req_to_ont_dsm_dataframe.apply(pd.to_numeric)

plot.tight_layout()
figure, axes = plot.subplots(figsize=(15,15))

axes.matshow(req_to_ont_dsm_dataframe)
# axes.imshow(dsm)
axes.set_xticklabels(req_to_ont_dsm_columns[0:(len(req_to_ont_dsm_columns))])
axes.xaxis.set_major_locator(MultipleLocator(1))
plot.xticks(rotation=90,fontsize=6)
axes.set_yticklabels(req_list)
axes.yaxis.set_major_locator(MultipleLocator(1))
plot.yticks(fontsize=6)
plot.subplots_adjust(bottom=0.00)

ontology_units_dsm = plot.savefig('req_to_ontology_units_dsm.jpg', dpi=1000)

print(ontology_units_dsm)
plot.clf()
            
##This will print the dsm linking requirements to ontology synonyms
req_to_ont_dsm_dataframe = pd.DataFrame(req_to_ont_synonyms_dsm, columns = req_to_ont_dsm_columns)
req_to_ont_dsm_dataframe.to_csv('req_to_ont_synonym_dsm.csv', index=False) 
            
req_to_ont_dsm_dataframe = req_to_ont_dsm_dataframe.drop('req_id',axis=1)
req_to_ont_dsm_dataframe = req_to_ont_dsm_dataframe.apply(pd.to_numeric)

plot.tight_layout()
figure, axes = plot.subplots(figsize=(15,15))

axes.matshow(req_to_ont_dsm_dataframe)
# axes.imshow(dsm)
axes.set_xticklabels(req_to_ont_dsm_columns[0:(len(req_to_ont_dsm_columns))])
axes.xaxis.set_major_locator(MultipleLocator(1))
plot.xticks(rotation=90,fontsize=6)
axes.set_yticklabels(req_list)
axes.yaxis.set_major_locator(MultipleLocator(1))
plot.yticks(fontsize=6)
plot.subplots_adjust(bottom=0.00)

ontology_synonym_dsm = plot.savefig('req_to_ontology_synonym_dsm.jpg', dpi=1000)

print(ontology_synonym_dsm)
plot.clf()