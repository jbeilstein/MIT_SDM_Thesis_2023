from matplotlib.ticker import MultipleLocator
from matplotlib import ticker

import csv
import math
import matplotlib.pyplot as plot
import pandas as pd

def requirement_to_ontology_score_visualizer(requirement_file_name):
    
    data_file = 'ontology_relationships_two_way.csv'
    ont_dataframe = pd.read_csv(data_file,sep=',')

    requirements_dataframe = pd.read_csv(requirement_file_name,sep=',')

    data_file = 'req_to_ont_comparison.csv'
    req_to_ont_semantics_dataframe = pd.read_csv(data_file,sep=',')

    req_ont_score_pairing = []
    req_ont_score_pairing_column_names = ['req_id','ont_id','ont_name','name_similarity','name_score','description_similarity','description_score','synonyms_similarity','synonyms_score','synonyms_max']
    # req_ont_score_pairing_column_names = ['req_id','ont_id','ont_name','name_similarity','name_score','description_similarity','description_score','units_similarity','units_score','units_max','synonyms_similarity','synonyms_score','synonyms_max']

    # This will remove all "block" type text entries
    requirements_dataframe = requirements_dataframe[requirements_dataframe['entry_type'] != 'block']

    #This section will iterate through every unique requirement ID and then every paired ontological entity.  It will break out the raw name, description, and synonym scores for visualization and later
    #analysis.
    for req in req_to_ont_semantics_dataframe['req_id'].unique():
        
        candidate_pairs = req_to_ont_semantics_dataframe[req_to_ont_semantics_dataframe['req_id'] == req]
        for ont in candidate_pairs['ont_id'].unique():
            name_list = []
            name_total = 0
            description_list = []
            description_total = 0
            # units = False
            # units_list = []
            # units_total = 0
            # units_max = 0
            snynonyms = False
            synonyms_list = []
            synonyms_total = 0
            synonyms_max = -1
            for temp_i, temp_pair in candidate_pairs[candidate_pairs['ont_id'] == ont].iterrows():
                if temp_i != 0:
                    #req_id	ont_id	ont_name	spacy similarity	semantic similarity	source
                    if temp_pair['source'] == 'ont_name':
                        name_list.append(float(temp_pair['semantic_similarity']))
                        name_total = name_total + float(temp_pair['semantic_similarity'])
                    elif temp_pair['source'] == 'ont_description':
                        description_list.append(float(temp_pair['semantic_similarity']))
                        description_total = description_total + float(temp_pair['semantic_similarity']    )
                    # elif temp_pair['source'] == 'ont_units':
                    #     units = True
                    #     units_list.append(float(temp_pair['semantic_similarity']))  
                    #     units_total = units_total + float(temp_pair['semantic_similarity'])
                    #     if (float(temp_pair['semantic_similarity']) > units_max):
                    #         units_max = float(temp_pair['semantic_similarity'])
                    elif temp_pair['source'] == 'ont_synonyms':
                        synonyms = True
                        synonyms_list.append(float(temp_pair['semantic_similarity']))   
                        synonyms_total = synonyms_total + float(temp_pair['semantic_similarity'])
                        if (float(temp_pair['semantic_similarity']) > synonyms_max):
                            synonyms_max = float(temp_pair['semantic_similarity']) 
            
            # score_entry = [temp_pair['req_id'], temp_pair['ont_id'], temp_pair['ont_name'], name_list, name_total, description_list, description_total, units_list, units_total, units_max, synonyms_list, synonyms_total, synonyms_max]
            score_entry = [temp_pair['req_id'], temp_pair['ont_id'], temp_pair['ont_name'], name_list, name_total, description_list, description_total, synonyms_list, synonyms_total, synonyms_max]
            req_ont_score_pairing.append(score_entry)
                            
    req_ont_token_pairing = pd.DataFrame(req_ont_score_pairing, columns = req_ont_score_pairing_column_names)
    req_ont_token_pairing.to_csv('req_to_ont_semantic_scored.csv', index=False)

    ontology_dataframe_columns = list(ont_dataframe.columns)
    num_cols = len(ontology_dataframe_columns)
    req_to_ont_dsm_columns = ['req_id'] + ontology_dataframe_columns[2:(num_cols-5)]
    req_to_ont_dsm = []
    req_to_ont_name_dsm = []
    req_to_ont_description_dsm = []
    # req_to_ont_units_dsm = []
    req_to_ont_synonyms_dsm = []
    req_list = ()

    for req_i, req_row in requirements_dataframe.iterrows():
        if req_row['id_num'] != '' and req_row['id_num'] != 'id_num' and math.isnan(req_row['id_num']) != True:
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
            # units_dsm_entry = str(req_id)
            synonyms_dsm_entry = str(req_id)
                            
            for i in range(0,(len(req_to_ont_dsm_columns)-1)):
                if i in ont_list:
                    names_count = 0
                    descriptions_count = 0
                    # units_count = 0
                    synonyms_count = 0
                    dsm_entry = dsm_entry + ',1'
                    temp_pairs = req_ont_pairs[req_ont_pairs['ont_id']==i]
                    names_count = (temp_pairs.name_score != 0).sum()
                    if names_count != 0:
                        names = float(temp_pairs.name_score)
                    else:
                        names = 0
                    name_dsm_entry = name_dsm_entry + ',' + str(names)
                        
                    descriptions_count = (temp_pairs.description_score != 0).sum()
                    if descriptions_count != 0:
                        descriptions = float(temp_pairs.description_score)                 
                    else:
                        descriptions = 0
                    description_dsm_entry = description_dsm_entry + ',' + str(descriptions)  
                        
                    # units_count = (temp_pairs.units_max != 0).sum()
                    # if units_count != 0:
                    #     units = float(temp_pairs.units_max)       
                    # else:
                    #     units = 0
                    # units_dsm_entry = units_dsm_entry + ',' + str(units) 
                                        
                    synonyms_count = (temp_pairs.synonyms_max != 0).sum()
                    if synonyms_count != 0:
                        synonyms = float(temp_pairs.synonyms_max)
                    else:
                        synonyms = 0
                    synonyms_dsm_entry = synonyms_dsm_entry + ',' + str(synonyms)     
                                    
                else:
                    dsm_entry = dsm_entry + ',0'
                    name_dsm_entry = name_dsm_entry + ',0'
                    description_dsm_entry = description_dsm_entry + ',0'
                    # units_dsm_entry = units_dsm_entry + ',0'
                    synonyms_dsm_entry = synonyms_dsm_entry + ',0'
                    
            dsm_entry_list = dsm_entry.split(',') 
            dsm_name_entry_list = name_dsm_entry.split(',')
            dsm_description_entry_list = description_dsm_entry.split(',')
            # dsm_units_entry_list = units_dsm_entry.split(',')
            dsm_synonyms_entry_list = synonyms_dsm_entry.split(',')
            req_to_ont_dsm.append(dsm_entry_list)
            req_to_ont_name_dsm.append(dsm_name_entry_list)
            req_to_ont_description_dsm.append(dsm_description_entry_list)
            # req_to_ont_units_dsm.append(dsm_units_entry_list)
            req_to_ont_synonyms_dsm.append(dsm_synonyms_entry_list)

    req_list = req_list.split(',')

    # ##This will save the csv and print the dsm linking requirements to any aspect of an ontology
    # req_to_ont_dsm_dataframe = pd.DataFrame(req_to_ont_dsm, columns = req_to_ont_dsm_columns)
    # req_to_ont_dsm_dataframe.to_csv('req_to_ont_dsm.csv', index=False) 
                
    # req_to_ont_dsm_dataframe = req_to_ont_dsm_dataframe.drop('req_id',axis=1)
    # req_to_ont_dsm_dataframe = req_to_ont_dsm_dataframe.apply(pd.to_numeric)

    # plot.tight_layout()
    # figure, axes = plot.subplots(figsize=(15,15))

    # axes.matshow(req_to_ont_dsm_dataframe)
    # # The follow axes labeling derived from https://stackoverflow.com/questions/49436895/arguments-for-loglocator 
    # # authored by user Y.Luo.  Authored 23 Mar 2018.  Accessed 23 Oct 2023.
    # axes.set_xticklabels(req_to_ont_dsm_columns[0:(len(req_to_ont_dsm_columns))])
    # axes.xaxis.set_major_locator(MultipleLocator(1))
    # plot.xticks(rotation=90,fontsize=6)
    # axes.set_yticklabels([" "] + req_list)
    # axes.yaxis.set_major_locator(MultipleLocator(1))
    # plot.yticks(fontsize=6)
    # plot.subplots_adjust(bottom=0.00)

    # ontology_dsm = plot.savefig('req_to_ontology_dsm.jpg', dpi=1000)

    # print(ontology_dsm)
    # plot.clf()

    ##This will print the dsm linking requirements to ontology names
    req_to_ont_dsm_name_dataframe = pd.DataFrame(req_to_ont_name_dsm, columns = req_to_ont_dsm_columns)
    req_to_ont_dsm_name_dataframe.to_csv('req_to_ont_name_dsm.csv', index=False) 

    req_to_ont_name_dsm_normalized = req_to_ont_dsm_name_dataframe            
    req_to_ont_dsm_name_dataframe = req_to_ont_dsm_name_dataframe.drop('req_id',axis=1)
    req_to_ont_dsm_name_dataframe = req_to_ont_dsm_name_dataframe.apply(pd.to_numeric)

    plot.tight_layout()
    figure, axes = plot.subplots(figsize=(15,15))

    # axes.xaxis.set_major_locator(ticker.FixedLocator(range(num_classes+1)))
    # axes.set_xticklabels(columns[2:(num_classes+3)])
    # plot.xticks(rotation=90,fontsize=8)
    # axes.yaxis.set_major_locator(ticker.FixedLocator(range(num_classes+1)))
    # axes.set_yticklabels(columns[2:(num_classes+3)])  

    num_nodes = len(req_to_ont_dsm_columns)
    num_reqs = len(req_list)
    
    axes.matshow(req_to_ont_dsm_name_dataframe, aspect='auto')
    # axes.imshow(dsm)
    axes.xaxis.set_major_locator(ticker.FixedLocator(range(num_nodes-1)))
    axes.set_xticklabels(req_to_ont_dsm_columns[1:(len(req_to_ont_dsm_columns))])
    plot.xticks(rotation=90,fontsize=6)
    axes.yaxis.set_major_locator(ticker.FixedLocator(range(num_reqs)))
    axes.set_yticklabels(req_list)
    plot.yticks(fontsize=12)
    plot.subplots_adjust(bottom=0.00)
 

    ontology_name_dsm = plot.savefig('req_to_ontology_name_dsm.jpg', dpi=1000)

    ontology_name_dsm
    plot.clf()

    ##This will print the dsm linking requirements to ontology descriptions
    req_to_ont_description_dsm_dataframe = pd.DataFrame(req_to_ont_description_dsm, columns = req_to_ont_dsm_columns)
    req_to_ont_description_dsm_dataframe.to_csv('req_to_ont_description_dsm.csv', index=False) 

    req_to_ont_description_dsm_normalized = req_to_ont_description_dsm_dataframe            
    req_to_ont_description_dsm_dataframe = req_to_ont_description_dsm_dataframe.drop('req_id',axis=1)
    req_to_ont_description_dsm_dataframe = req_to_ont_description_dsm_dataframe.apply(pd.to_numeric)

    plot.tight_layout()
    figure, axes = plot.subplots(figsize=(15,15))

    axes.matshow(req_to_ont_description_dsm_dataframe)
    axes.xaxis.set_major_locator(ticker.FixedLocator(range(num_nodes-1)))
    axes.set_xticklabels(req_to_ont_dsm_columns[1:(len(req_to_ont_dsm_columns))])
    plot.xticks(rotation=90,fontsize=6)
    axes.yaxis.set_major_locator(ticker.FixedLocator(range(num_reqs)))
    axes.set_yticklabels(req_list)  
    plot.yticks(fontsize=6)
    plot.subplots_adjust(bottom=0.00)

    ontology_description_dsm = plot.savefig('req_to_ontology_description_dsm.jpg', dpi=1000)

    ontology_description_dsm
    plot.clf()

    ##This will print the dsm linking requirements to ontology units
    # req_to_ont_units_dsm_dataframe = pd.DataFrame(req_to_ont_units_dsm, columns = req_to_ont_dsm_columns)
    # req_to_ont_units_dsm_dataframe.to_csv('req_to_ont_units_dsm.csv', index=False) 
                
    # req_to_ont_units_dsm_normalized = req_to_ont_units_dsm_dataframe
    # req_to_ont_units_dsm_dataframe = req_to_ont_units_dsm_dataframe.drop('req_id',axis=1)
    # req_to_ont_units_dsm_dataframe = req_to_ont_units_dsm_dataframe.apply(pd.to_numeric)

    # plot.tight_layout()
    # figure, axes = plot.subplots(figsize=(15,15))

    # axes.matshow(req_to_ont_units_dsm_dataframe)
    # axes.set_xticklabels(req_to_ont_dsm_columns[0:(len(req_to_ont_dsm_columns))])
    # axes.xaxis.set_major_locator(MultipleLocator(1))
    # plot.xticks(rotation=90,fontsize=6)
    # axes.set_yticklabels([" "] + req_list)
    # axes.yaxis.set_major_locator(MultipleLocator(1))
    # plot.yticks(fontsize=6)
    # plot.subplots_adjust(bottom=0.00)

    # ontology_units_dsm = plot.savefig('req_to_ontology_units_dsm.jpg', dpi=1000)

    # print(ontology_units_dsm)
    plot.clf()
                
    ##This will print the dsm linking requirements to ontology synonyms
    req_to_ont_synonyms_dsm_dataframe = pd.DataFrame(req_to_ont_synonyms_dsm, columns = req_to_ont_dsm_columns)
    req_to_ont_synonyms_dsm_dataframe.to_csv('req_to_ont_synonym_dsm.csv', index=False) 
                
    req_to_ont_synonyms_dsm_normalized = req_to_ont_synonyms_dsm_dataframe            
    req_to_ont_synonyms_dsm_dataframe = req_to_ont_synonyms_dsm_dataframe.drop('req_id',axis=1)
    req_to_ont_synonyms_dsm_dataframe = req_to_ont_synonyms_dsm_dataframe.apply(pd.to_numeric)

    plot.tight_layout()
    figure, axes = plot.subplots(figsize=(15,15))

    axes.matshow(req_to_ont_synonyms_dsm_dataframe)
    axes.xaxis.set_major_locator(ticker.FixedLocator(range(num_nodes-1)))
    axes.set_xticklabels(req_to_ont_dsm_columns[1:(len(req_to_ont_dsm_columns))])
    plot.xticks(rotation=90,fontsize=6)
    axes.yaxis.set_major_locator(ticker.FixedLocator(range(num_reqs)))
    axes.set_yticklabels(req_list)   
    plot.yticks(fontsize=6)
    plot.subplots_adjust(bottom=0.00)

    ontology_synonym_dsm = plot.savefig('req_to_ontology_synonym_dsm.jpg', dpi=1000)

    ontology_synonym_dsm
    plot.clf()

    #This section will perform a Min Max Rescaling normalization to aid in later analysis for the ontology's description semantic similarity vs. requirements
    # req_to_ont_description_dsm_normalized = req_to_ont_description_dsm_dataframe
    for req_i, req_row in req_to_ont_description_dsm_normalized.iterrows():
        sum = 0
        count = 0
        min = 1
        max = 0
        for col in req_to_ont_dsm_columns:
            if col != 'req_id':
                if float(req_row[col]) < min:
                    min = float(req_row[col])
                if float(req_row[col]) > max:
                    max = float(req_row[col])
                sum = sum + float(req_row[col])
                count = count + 1  
        for col in req_to_ont_dsm_columns:
            if col != 'req_id':
                # The following is based on a solution found on Stack Overflow at https://stackoverflow.com/questions/13842088/set-value-for-particular-cell-in-pandas-dataframe-using-index
                # Written by user Dina Taklit on 29 April, 2019.  Accessed 24 Oct 2023
                req_to_ont_description_dsm_normalized.at[req_i,col] = (float(req_row[col])-min)/(max-min)
        
    req_relationships = pd.DataFrame(req_to_ont_description_dsm_normalized, columns = req_to_ont_dsm_columns)
    req_relationships.to_csv('req_to_ont_description_dsm_normalized.csv', index=False)

    num_classes = len(req_list)
    dsm_matrix = req_relationships[req_relationships.columns[1:(num_classes+1)][0:(num_classes)]]

    dsm = pd.DataFrame(dsm_matrix)
    dsm = dsm.apply(pd.to_numeric)

    plot.tight_layout()
    figure, axes = plot.subplots(figsize=(10,10))

    axes.matshow(dsm)
    axes.xaxis.set_major_locator(ticker.FixedLocator(range(num_nodes-1)))
    axes.set_xticklabels(req_to_ont_dsm_columns[1:(len(req_to_ont_dsm_columns))])
    plot.xticks(rotation=90,fontsize=6)
    axes.yaxis.set_major_locator(ticker.FixedLocator(range(num_reqs)))
    axes.set_yticklabels(req_list)  
    plot.yticks(fontsize=6)
    plot.subplots_adjust(bottom=0.00)

    ontology_dsm = plot.savefig('req_to_ontology_description_dsm_normalized.jpg', dpi=1000)

    #This section will perform a Min Max Rescaling normalization to aid in later analysis for the ontology's name semantic similarity vs. requirements
    # req_to_ont_name_dsm_normalized = req_to_ont_dsm_name_dataframe
    for req_i, req_row in req_to_ont_name_dsm_normalized.iterrows():
        sum = 0
        count = 0
        min = 1
        max = 0
        for col in req_to_ont_dsm_columns:
            if col != 'req_id':
                if float(req_row[col]) < min:
                    min = float(req_row[col])
                if float(req_row[col]) > max:
                    max = float(req_row[col])
                sum = sum + float(req_row[col])
                count = count + 1  
        for col in req_to_ont_dsm_columns:
            if col != 'req_id':
                # The following is based on a solution found on Stack Overflow at https://stackoverflow.com/questions/13842088/set-value-for-particular-cell-in-pandas-dataframe-using-index
                # Written by user Dina Taklit on 29 April, 2019.  Accessed 24 Oct 2023
                req_to_ont_name_dsm_normalized.at[req_i,col] = (float(req_row[col])-min)/(max-min)
        
    req_relationships = pd.DataFrame(req_to_ont_name_dsm_normalized, columns = req_to_ont_dsm_columns)
    req_relationships.to_csv('req_to_ont_name_dsm_normalized.csv', index=False)

    num_classes = len(req_list)
    dsm_matrix = req_relationships[req_relationships.columns[1:(num_classes+1)][0:(num_classes)]]

    dsm = pd.DataFrame(dsm_matrix)
    dsm = dsm.apply(pd.to_numeric)

    plot.tight_layout()
    figure, axes = plot.subplots(figsize=(10,10))

    axes.matshow(dsm)
    axes.xaxis.set_major_locator(ticker.FixedLocator(range(num_nodes-1)))
    axes.set_xticklabels(req_to_ont_dsm_columns[1:(len(req_to_ont_dsm_columns))])
    plot.xticks(rotation=90,fontsize=6)
    axes.yaxis.set_major_locator(ticker.FixedLocator(range(num_reqs)))
    axes.set_yticklabels(req_list)  
    plot.yticks(fontsize=6)
    plot.subplots_adjust(bottom=0.00)

    ontology_dsm = plot.savefig('req_to_ontology_name_dsm_normalized.jpg', dpi=1000)

    #This section will perform a Min Max Rescaling normalization to aid in later analysis for the ontology's units semantic similarity vs. requirements
    # req_to_ont_units_dsm_normalized = req_to_ont_units_dsm_dataframe
    # for req_i, req_row in req_to_ont_units_dsm_normalized.iterrows():
    #     sum = 0
    #     count = 0
    #     min = 1
    #     max = 0
    #     for col in req_to_ont_dsm_columns:
    #         if col != 'req_id':
    #             if float(req_row[col]) < min:
    #                 min = float(req_row[col])
    #             if float(req_row[col]) > max:
    #                 max = float(req_row[col])
    #             sum = sum + float(req_row[col])
    #             count = count + 1  
    #     for col in req_to_ont_dsm_columns:
    #         if col != 'req_id':
    #             # The following is based on a solution found on Stack Overflow at https://stackoverflow.com/questions/13842088/set-value-for-particular-cell-in-pandas-dataframe-using-index
    #             # Written by user Dina Taklit on 29 April, 2019.  Accessed 24 Oct 2023
    #             req_to_ont_units_dsm_normalized.at[req_i,col] = (float(req_row[col])-min)/(max-min)
        
    # req_relationships = pd.DataFrame(req_to_ont_units_dsm_normalized, columns = req_to_ont_dsm_columns)
    # req_relationships.to_csv('req_to_ont_units_dsm_normalized.csv', index=False)

    # num_classes = len(req_list)
    # dsm_matrix = req_relationships[req_relationships.columns[1:(num_classes+1)][0:(num_classes)]]

    # dsm = pd.DataFrame(dsm_matrix)
    # dsm = dsm.apply(pd.to_numeric)

    # plot.tight_layout()
    # figure, axes = plot.subplots(figsize=(10,10))

    # axes.matshow(dsm)
    # axes.set_xticklabels(req_to_ont_dsm_columns[0:(len(req_to_ont_dsm_columns))])
    # axes.xaxis.set_major_locator(MultipleLocator(1))
    # plot.xticks(rotation=90,fontsize=6)
    # axes.set_yticklabels([" "] + req_list)
    # axes.yaxis.set_major_locator(MultipleLocator(1))
    # plot.yticks(fontsize=6)
    # plot.subplots_adjust(bottom=0.00)

    # ontology_dsm = plot.savefig('req_to_ontology_units_dsm_normalized.jpg', dpi=1000)

    #This section will perform a Min Max Rescaling normalization to aid in later analysis for the ontology's synonym semantic similarity vs. requirements
    # req_to_ont_synonyms_dsm_normalized = req_to_ont_synonyms_dsm_dataframe
    for req_i, req_row in req_to_ont_synonyms_dsm_normalized.iterrows():
        sum = 0
        count = 0
        min = 1
        max = 0
        for col in req_to_ont_dsm_columns:
            if col != 'req_id':
                if float(req_row[col]) < min:
                    min = float(req_row[col])
                if float(req_row[col]) > max:
                    max = float(req_row[col])
                sum = sum + float(req_row[col])
                count = count + 1  
        for col in req_to_ont_dsm_columns:
            if col != 'req_id':
                # The following is based on a solution found on Stack Overflow at https://stackoverflow.com/questions/13842088/set-value-for-particular-cell-in-pandas-dataframe-using-index
                # Written by user Dina Taklit on 29 April, 2019.  Accessed 24 Oct 2023
                req_to_ont_synonyms_dsm_normalized.at[req_i,col] = (float(req_row[col])-min)/(max-min)
        
    req_relationships = pd.DataFrame(req_to_ont_synonyms_dsm_normalized, columns = req_to_ont_dsm_columns)
    req_relationships.to_csv('req_to_ont_synonyms_dsm_normalized.csv', index=False)

    num_classes = len(req_list)
    dsm_matrix = req_relationships[req_relationships.columns[1:(num_classes+1)][0:(num_classes)]]

    dsm = pd.DataFrame(dsm_matrix)
    dsm = dsm.apply(pd.to_numeric)

    plot.tight_layout()
    figure, axes = plot.subplots(figsize=(10,10))

    axes.matshow(dsm)
    axes.xaxis.set_major_locator(ticker.FixedLocator(range(num_nodes-1)))
    axes.set_xticklabels(req_to_ont_dsm_columns[1:(len(req_to_ont_dsm_columns))])
    plot.xticks(rotation=90,fontsize=6)
    axes.yaxis.set_major_locator(ticker.FixedLocator(range(num_reqs)))
    axes.set_yticklabels(req_list) 
    plot.yticks(fontsize=6)
    plot.subplots_adjust(bottom=0.00)

    ontology_dsm = plot.savefig('req_to_ontology_synonyms_dsm_normalized.jpg', dpi=1000)
    print('Requirement to ontology visual comparisons completed')