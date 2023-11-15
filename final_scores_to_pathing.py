import csv
import math
import numpy as np
import pandas as pd

def adjacent_node_recommender(requirement_file_name, initial_semantic_threshold, secondary_semantic_threshold):
        
    data_file = 'adjacent_nodes.csv'
    adjacency_dataframe = pd.read_csv(data_file,sep=',')

    requirements_dataframe = pd.read_csv(requirement_file_name,sep=',')

    data_file = 'req_to_ont_name_dsm.csv'
    name_dataframe = pd.read_csv(data_file,sep=',')

    data_file = 'req_to_ont_name_dsm_normalized.csv'
    name_dataframe_norm = pd.read_csv(data_file,sep=',')

    data_file = 'req_to_ont_description_dsm.csv'
    description_dataframe = pd.read_csv(data_file,sep=',')

    data_file = 'req_to_ont_description_dsm_normalized.csv'
    description_dataframe_norm = pd.read_csv(data_file,sep=',')

    data_file = 'req_to_ont_synonym_dsm.csv'
    synonyms_dataframe = pd.read_csv(data_file,sep=',')

    data_file = 'req_to_ont_synonyms_dsm_normalized.csv'
    synonyms_dataframe_norm = pd.read_csv(data_file,sep=',')

    req_list = []
    req_ont_pairing = []
    req_ont_pairing_column_names = ['req_id','ont_name_id_list','ont_name_score_list','ont_name_correct','ont_synonyms_id_list','ont_synonyms_score_list','ont_synonyms_correct']

    data_property_list = ['hasDatarate','hasHeight','hasLength','hasMass','hasWidth','limitAcceleration','limitAltitude','limitMass','limitVelocity','powerConsumed','powerSupplied']

    req_to_ont_dsm_columns = list(name_dataframe_norm.columns)
    width = len(req_to_ont_dsm_columns) + 1

    # This will remove all "block" type text entries and leave only single sentence requirement entries
    requirements_dataframe = requirements_dataframe[requirements_dataframe['entry_type'] != 'block']
    height = len(requirements_dataframe)
    columns = list(range(0,(len(req_to_ont_dsm_columns)-1)))
    columns = ['req_id'] + columns

    req_to_ont_ordered_name_pairing_norm = []
    req_to_ont_ordered_name_pairing_weights = []
    req_to_ont_ordered_name_pairing_norm_weights = []
    req_to_ont_ordered_name_pairing_boolean = []

    req_to_ont_ordered_description_pairing_norm = []
    req_to_ont_ordered_description_pairing_weights = []
    req_to_ont_ordered_description_pairing_norm_weights = []
    req_to_ont_ordered_description_pairing_boolean = []

    req_to_ont_ordered_synonyms_pairing_norm = []
    req_to_ont_ordered_synonyms_pairing_weights = []
    req_to_ont_ordered_synonyms_pairing_norm_weights = []
    req_to_ont_ordered_synonyms_pairing_boolean = []

    #This is the start of the Initial Pairing Tool.  The first step is go requirement by requirement and take each pair of semantic similarity scores and rank them in order by requirement.
    #At the end of this section Each requirement will have three sets of matrices in descending order of the highest to lowest STS scores.  There is a set of matrices for name similarity, 
    #description similarity, and synonym similarity.  
    current_req = 0
    for req_i, req_row in requirements_dataframe.iterrows():
        if (req_row['id_num'] != '') and (req_row['id_num'] != 'id_num') and (math.isnan(req_row['id_num']) != True):
            req_id = req_row['id_num']
            if len(req_list) == 0:
                req_list = str(req_id)
            else:
                req_list = req_list + "," + str(req_id)
            #The following command is based upon the Stack Overflow post https://stackoverflow.com/questions/52737799/sort-values-based-on-column-index written by 
            #User Jezrael on 10 Oct 2018.  Accessed 24 Oct 2023.
            name_row = name_dataframe_norm.iloc[current_req]
            name_row = name_row.sort_values(ascending=False)
            original_name_weight_row = name_dataframe.iloc[current_req]
            original_name_weight_row = original_name_weight_row.sort_values(ascending=False)
            
            description_row = description_dataframe_norm.iloc[current_req]
            description_row = description_row.sort_values(ascending=False)
            original_description_weight_row = description_dataframe.iloc[current_req]
            original_description_weight_row = original_description_weight_row.sort_values(ascending=False)
            
            synonyms_row = synonyms_dataframe_norm.iloc[current_req]
            synonyms_row = synonyms_row.sort_values(ascending=False)
            original_synonyms_weight_row = synonyms_dataframe.iloc[current_req]
            original_synonyms_weight_row = original_synonyms_weight_row.sort_values(ascending=False)
            
            name_length = len(name_row)
            if int(req_id) == '101':
                x=1
            name_list = str(req_id)
            name_weights_list = name_list
            name_weights_list_original = name_list
            name_boolean_list = name_list
            
            description_list = name_list
            description_weights_list = name_list
            description_weights_list_original = name_list
            description_boolean_list = name_list      
            
            synonyms_list = name_list
            synonyms_weights_list = name_list
            synyonyms_weights_list_original = name_list
            synonyms_boolean_list = name_list        
            

            for i in range(1,(name_length)):
            
                bool_found = False
                name_list = name_list + ',' + str(name_row.index[i])               
                name_weights_list = name_weights_list + ',' + str(name_row[i])
                name_weights_list_original = name_weights_list_original + ',' + str(original_name_weight_row[i])
                if name_row.index[i] in data_property_list:
                    # Parts of the following two lines of code are based upon the Stack Overflow entry https://stackoverflow.com/questions/27975069/how-to-filter-rows-containing-a-string-pattern-from-a-pandas-dataframe
                    # written by user Amit on 15 Jan 2015.  Accessed 24 Oct 2023
                    index_loc = req_to_ont_dsm_columns.index(name_row.index[i])
                    temp_dataframe = adjacency_dataframe[adjacency_dataframe['adjacent_columns'].str.contains(str(index_loc))]
                    for j, temp_row in temp_dataframe.iterrows():
                        if (req_row[req_to_ont_dsm_columns[j+1]] == True) and (bool_found == False):
                            name_boolean_list = name_boolean_list + ',1'
                            bool_found = True
                    if bool_found == False:
                        name_boolean_list = name_boolean_list + ',0'   
                elif req_row[name_row.index[i]] == True:
                    name_boolean_list = name_boolean_list + ',1'
                else:
                    name_boolean_list = name_boolean_list + ',0'
                    
                bool_found = False
                description_list = description_list + ',' + str(description_row.index[i])               
                description_weights_list = description_weights_list + ',' + str(description_row[i])
                description_weights_list_original = description_weights_list_original + ',' + str(original_description_weight_row[i])
                if description_row.index[i] in data_property_list:
                    # Parts of the following two lines of code are based upon the Stack Overflow entry https://stackoverflow.com/questions/27975069/how-to-filter-rows-containing-a-string-pattern-from-a-pandas-dataframe
                    # written by user Amit on 15 Jan 2015.  Accessed 24 Oct 2023
                    index_loc = req_to_ont_dsm_columns.index(description_row.index[i])
                    temp_dataframe = adjacency_dataframe[adjacency_dataframe['adjacent_columns'].str.contains(str(index_loc))]
                    for j, temp_row in temp_dataframe.iterrows():
                        if (req_row[req_to_ont_dsm_columns[j+1]] == True) and (bool_found == False):
                            description_boolean_list = description_boolean_list + ',1'
                            bool_found = True
                    if bool_found == False:
                        description_boolean_list = description_boolean_list + ',0'   
                elif req_row[description_row.index[i]] == True:
                    description_boolean_list = description_boolean_list + ',1'
                else:
                    description_boolean_list = description_boolean_list + ',0'

                if float(req_id) == 105:
                    x=1
                    
                synonyms_list = synonyms_list + ',' + str(synonyms_row.index[i])               
                synonyms_weights_list = synonyms_weights_list + ',' + str(synonyms_row[i])
                synyonyms_weights_list_original = synyonyms_weights_list_original + ',' + str(original_synonyms_weight_row[i])
                bool_found = False
                if synonyms_row.index[i] in data_property_list:
                    #Enable this comment if you do not want data properties included
                    #synonyms_boolean_list = synonyms_boolean_list + ',0'  
                    index_loc = req_to_ont_dsm_columns.index(synonyms_row.index[i])
                    temp_dataframe = adjacency_dataframe[adjacency_dataframe['adjacent_columns'].str.contains(str(index_loc))]
                    for j, temp_row in temp_dataframe.iterrows():
                        if (req_row[req_to_ont_dsm_columns[j+1]] == True) and (bool_found == False):
                            synonyms_boolean_list = synonyms_boolean_list + ',1'
                            bool_found = True
                    if bool_found == False:
                        synonyms_boolean_list = synonyms_boolean_list + ',0'   
                elif req_row[synonyms_row.index[i]] == True:
                    synonyms_boolean_list = synonyms_boolean_list + ',1'
                else:
                    synonyms_boolean_list = synonyms_boolean_list + ',0'    
                                
            req_to_ont_ordered_name_pairing_norm.append(name_list.split(','))
            req_to_ont_ordered_name_pairing_weights.append(name_weights_list_original.split(','))
            req_to_ont_ordered_name_pairing_norm_weights.append(name_weights_list.split(','))
            req_to_ont_ordered_name_pairing_boolean.append(name_boolean_list.split(','))
            
            req_to_ont_ordered_description_pairing_norm.append(description_list.split(','))
            req_to_ont_ordered_description_pairing_weights.append(description_weights_list_original.split(','))
            req_to_ont_ordered_description_pairing_norm_weights.append(description_weights_list.split(','))
            req_to_ont_ordered_description_pairing_boolean.append(description_boolean_list.split(','))
            
            req_to_ont_ordered_synonyms_pairing_norm.append(synonyms_list.split(','))
            req_to_ont_ordered_synonyms_pairing_weights.append(synyonyms_weights_list_original.split(','))
            req_to_ont_ordered_synonyms_pairing_norm_weights.append(synonyms_weights_list.split(','))
            req_to_ont_ordered_synonyms_pairing_boolean.append(synonyms_boolean_list.split(','))
            
        current_req = current_req + 1    

    #These matrices are ranked from highest to lowest STS for names
    req_to_ont_ordered_name_pairing_norm = pd.DataFrame(req_to_ont_ordered_name_pairing_norm, columns = columns)
    req_to_ont_ordered_name_pairing_norm.to_csv('req_to_ont_ordered_name_pairing_names.csv', index=False)

    req_to_ont_ordered_name_pairing_weights = pd.DataFrame(req_to_ont_ordered_name_pairing_weights, columns = columns)
    req_to_ont_ordered_name_pairing_weights.to_csv('req_to_ont_ordered_name_pairing_weights.csv', index=False)

    req_to_ont_ordered_name_pairing_norm_weights = pd.DataFrame(req_to_ont_ordered_name_pairing_norm_weights, columns = columns)
    req_to_ont_ordered_name_pairing_norm_weights.to_csv('req_to_ont_ordered_name_pairing_norm_weights.csv', index=False)

    req_to_ont_ordered_name_pairing_boolean = pd.DataFrame(req_to_ont_ordered_name_pairing_boolean, columns = columns)
    req_to_ont_ordered_name_pairing_boolean.to_csv('req_to_ont_ordered_name_pairing_boolean.csv', index=False)

    #These matrices are ranked from highest to lowest STS for descriptions
    req_to_ont_ordered_description_pairing_norm = pd.DataFrame(req_to_ont_ordered_description_pairing_norm, columns = columns)
    req_to_ont_ordered_description_pairing_norm.to_csv('req_to_ont_ordered_description_pairing_names.csv', index=False)

    req_to_ont_ordered_description_pairing_weights = pd.DataFrame(req_to_ont_ordered_description_pairing_weights, columns = columns)
    req_to_ont_ordered_description_pairing_weights.to_csv('req_to_ont_ordered_description_pairing_weights.csv', index=False)

    req_to_ont_ordered_description_pairing_norm_weights = pd.DataFrame(req_to_ont_ordered_description_pairing_norm_weights, columns = columns)
    req_to_ont_ordered_description_pairing_norm_weights.to_csv('req_to_ont_ordered_description_pairing_norm_weights.csv', index=False)

    req_to_ont_ordered_description_pairing_boolean = pd.DataFrame(req_to_ont_ordered_description_pairing_boolean, columns = columns)
    req_to_ont_ordered_description_pairing_boolean.to_csv('req_to_ont_ordered_description_pairing_boolean.csv', index=False)

    #These matrices are ranked from highest to lowest STS for synonyms
    req_to_ont_ordered_synonyms_pairing_norm = pd.DataFrame(req_to_ont_ordered_synonyms_pairing_norm, columns = columns)
    req_to_ont_ordered_synonyms_pairing_norm.to_csv('req_to_ont_ordered_synonyms_pairing_names.csv', index=False)

    req_to_ont_ordered_synonyms_pairing_weights = pd.DataFrame(req_to_ont_ordered_synonyms_pairing_weights, columns = columns)
    req_to_ont_ordered_synonyms_pairing_weights.to_csv('req_to_ont_ordered_synonyms_pairing_weights.csv', index=False)

    req_to_ont_ordered_synonyms_pairing_norm_weights = pd.DataFrame(req_to_ont_ordered_synonyms_pairing_norm_weights, columns = columns)
    req_to_ont_ordered_synonyms_pairing_norm_weights.to_csv('req_to_ont_ordered_synonyms_pairing_norm_weights.csv', index=False)

    req_to_ont_ordered_synonyms_pairing_boolean = pd.DataFrame(req_to_ont_ordered_synonyms_pairing_boolean, columns = columns)
    req_to_ont_ordered_synonyms_pairing_boolean.to_csv('req_to_ont_ordered_synonyms_pairing_boolean.csv', index=False)        
            
    #This is the second half of the Initial Assignment Tool
    #This section will assign requirements to ontologies based on what pairing exceed a semantic similarity threshold

    # This section allows the testing of a single threshold value
    # If you want to enable this go to the comments ST1 and ST3 below and comment out the respective lines below both entries, then uncomment the line below ST2
    semantic_threshold = initial_semantic_threshold

    current_pairings = []
    semantic_columns = ['req_id', 'ont_id', 'ontology_part', 'semantic_similarity_score', 'pairing_accuracy', 'similarity_source']
    req_to_ont_dsm_columns = list(name_dataframe_norm.columns)
    req_to_ont_dsm_columns = req_to_ont_dsm_columns[1:]


    current_req = 0
    for req_i, req_row in requirements_dataframe.iterrows():
        if (req_row['id_num'] != '') and (req_row['id_num'] != 'id_num') and (math.isnan(req_row['id_num']) != True):
            req_id = req_row['id_num']
            #The following command is based upon the Stack Overflow post https://stackoverflow.com/questions/52737799/sort-values-based-on-column-index written by 
            #User Jezrael on 10 Oct 2018.  Accessed 24 Oct 2023.
            name_ranks = req_to_ont_ordered_name_pairing_norm.iloc[current_req]
            name_ranks_weights = req_to_ont_ordered_name_pairing_weights.iloc[current_req] 
            name_ranks_weights_norm = req_to_ont_ordered_name_pairing_norm_weights.iloc[current_req]
            name_ranks_boolean = req_to_ont_ordered_name_pairing_boolean.iloc[current_req]

            description_ranks = req_to_ont_ordered_description_pairing_norm.iloc[current_req]
            description_ranks_weights = req_to_ont_ordered_description_pairing_weights.iloc[current_req]
            description_ranks_weights_norm =req_to_ont_ordered_description_pairing_norm_weights.iloc[current_req]
            description_ranks_boolean = req_to_ont_ordered_description_pairing_boolean.iloc[current_req]
            
            synonyms_ranks = req_to_ont_ordered_synonyms_pairing_norm.iloc[current_req]
            synonyms_ranks_weights = req_to_ont_ordered_synonyms_pairing_weights.iloc[current_req]
            synonyms_ranks_weights_norm = req_to_ont_ordered_synonyms_pairing_norm_weights.iloc[current_req]
            synonyms_ranks_boolean = req_to_ont_ordered_synonyms_pairing_boolean.iloc[current_req]
            
            current_pairing = []
            proceed = True
            name_proceed = True
            description_proceed = True
            synonyms_proceed = True
            for i in range(0,(len(name_ranks)-1)):
                if proceed == True:
                    if (float(name_ranks_weights[i]) > semantic_threshold) and (name_proceed == True):
                        #The next line is based upon code found on Stack Overflow located at https://stackoverflow.com/questions/176918/finding-the-index-of-an-item-in-a-list.
                        #It was written by user Alex Coventry on 7 Oct 2008, accessed 25 Oct 2023
                        ont_id = req_to_ont_dsm_columns.index(name_ranks[i])
                        current_pairing = [req_id, ont_id, name_ranks[i], float(name_ranks_weights[i]), name_ranks_boolean[i], 'name_similarity']
                        current_pairings.append(current_pairing)
                    else:
                        name_proceed = False
                        
                    if (float(description_ranks_weights[i]) > semantic_threshold) and (description_proceed == True):
                        #The next line is based upon code found on Stack Overflow located at https://stackoverflow.com/questions/176918/finding-the-index-of-an-item-in-a-list.
                        #It was written by user Alex Coventry on 7 Oct 2008, accessed 25 Oct 2023
                        ont_id = req_to_ont_dsm_columns.index(description_ranks[i])
                        current_pairing = [req_id, ont_id, description_ranks[i], float(description_ranks_weights[i]), description_ranks_boolean[i], 'description_similarity']
                        current_pairings.append(current_pairing)
                    else:
                        description_proceed = False
                        
                    if (float(synonyms_ranks_weights[i]) > semantic_threshold) and (synonyms_proceed == True):
                        #The next line is based upon code found on Stack Overflow located at https://stackoverflow.com/questions/176918/finding-the-index-of-an-item-in-a-list.
                        #It was written by user Alex Coventry on 7 Oct 2008, accessed 25 Oct 2023
                        ont_id = req_to_ont_dsm_columns.index(synonyms_ranks[i])
                        current_pairing = [req_id, ont_id, synonyms_ranks[i], float(synonyms_ranks_weights[i]), synonyms_ranks_boolean[i], 'synonyms_similarity']
                        current_pairings.append(current_pairing)
                    else:
                        synonyms_proceed = False                    
                        
                    if (name_proceed == False) and (description_proceed == False) and (synonyms_proceed == False):
                        proceed = False
            
        current_req = current_req + 1

    #This output .csv contains all of the recommended requirement to ontology pairings based upon the semantic_threshold set above        
    semantic_pairing_initial_dataframe = pd.DataFrame(current_pairings, columns = semantic_columns)
    semantic_pairing_initial_dataframe.to_csv('final_output_req_to_ont_semantic_pairing_initial.csv', index=False)

    #At this point there is an initial requirement to ontology matching.  
    #This next section is the Adjacency Validation Tool
    #It allows the nodes located in the Initial Assignment Tool above to act as anchors.  Then the neighboring nodes are checked against a new Semantic threshold of your choosing.
    #This value must be lower than the semantic_threshold above
    adjacent_threshold = secondary_semantic_threshold
    proceed = True
    semantic_index = semantic_columns.index('semantic_similarity_score')
    req_to_ont_adjacent_pairing = []
    req_to_ont_adjacent_pairing = []
    ont_identifiers = req_to_ont_dsm_columns
    req_ont_pairing_column_names = ['source_req_id','source_ont_id','source_ont_name','source_score','source_accuracy','adjacent_ont_id','adjacent_ont_name','adjacent_score','adjacent_accuracy']

    semantic_pairing_initial_dataframe = semantic_pairing_initial_dataframe.sort_values(by='semantic_similarity_score',ascending=False)

    for pair_i, pair_row in semantic_pairing_initial_dataframe.iterrows():
        source_req_id = pair_row['req_id']
        source_ont_id = pair_row['ont_id']
        source_ont_name = pair_row['ontology_part']
        source_score = pair_row['semantic_similarity_score']
        source_accuracy = pair_row['pairing_accuracy']
        source = pair_row['similarity_source']
        if source_score > semantic_threshold:
            adjacent_list = adjacency_dataframe.iloc[source_ont_id]
            adjacent_list = str(adjacent_list[1])
            adjacent_list = adjacent_list.split('\\')
            
            if len(adjacent_list) == 1:
                temp = str(adjacent_list[0])
                temp = temp.split('_')
                adjacent_ont_id = int(temp[0])
                adjacent_ont_name = temp[1]
                pairing_dataframe = semantic_pairing_initial_dataframe[semantic_pairing_initial_dataframe['req_id'] == source_req_id]
                paired_ont_list = pairing_dataframe['ont_id'].unique()
                
                if adjacent_ont_id not in paired_ont_list:
                    adjacent_ranked_name_row = (req_to_ont_ordered_name_pairing_norm[req_to_ont_ordered_name_pairing_norm['req_id'] == str(source_req_id)]).values     
                    adjacent_ranked_name_row = adjacent_ranked_name_row.tolist()
                    adjacent_ranked_name_row = adjacent_ranked_name_row[0]  
                    adjacent_ranked_name_pos = adjacent_ranked_name_row.index(adjacent_ont_name)              
                    adjacent_ranked_name_weight_row = (req_to_ont_ordered_name_pairing_weights[req_to_ont_ordered_name_pairing_weights['req_id'] == str(source_req_id)]).values
                    adjacent_ranked_name_weight_row = adjacent_ranked_name_weight_row.tolist()
                    adjacent_ranked_name_weight_row = adjacent_ranked_name_weight_row[0]  
                    adjacent_ranked_name_weight = float(adjacent_ranked_name_weight_row[adjacent_ranked_name_pos])
                    
                    adjacent_ranked_description_row = (req_to_ont_ordered_description_pairing_norm[req_to_ont_ordered_description_pairing_norm['req_id'] == str(source_req_id)]).values     
                    adjacent_ranked_description_row = adjacent_ranked_description_row.tolist()
                    adjacent_ranked_description_row = adjacent_ranked_description_row[0]  
                    adjacent_ranked_description_pos = adjacent_ranked_description_row.index(adjacent_ont_name)              
                    adjacent_ranked_description_weight_row = (req_to_ont_ordered_description_pairing_weights[req_to_ont_ordered_description_pairing_weights['req_id'] == str(source_req_id)]).values
                    adjacent_ranked_description_weight_row = adjacent_ranked_description_weight_row.tolist()
                    adjacent_ranked_description_weight_row = adjacent_ranked_description_weight_row[0]  
                    adjacent_ranked_description_weight = float(adjacent_ranked_description_weight_row[adjacent_ranked_description_pos])
                    
                    adjacent_ranked_synonyms_row = (req_to_ont_ordered_synonyms_pairing_norm[req_to_ont_ordered_synonyms_pairing_norm['req_id'] == str(source_req_id)]).values     
                    adjacent_ranked_synonyms_row = adjacent_ranked_synonyms_row.tolist()
                    adjacent_ranked_synonyms_row = adjacent_ranked_synonyms_row[0]  
                    adjacent_ranked_synonyms_pos = adjacent_ranked_synonyms_row.index(adjacent_ont_name)              
                    adjacent_ranked_synonyms_weight_row = (req_to_ont_ordered_synonyms_pairing_weights[req_to_ont_ordered_synonyms_pairing_weights['req_id'] == str(source_req_id)]).values
                    adjacent_ranked_synonyms_weight_row = adjacent_ranked_synonyms_weight_row.tolist()
                    adjacent_ranked_synonyms_weight_row = adjacent_ranked_synonyms_weight_row[0]  
                    adjacent_ranked_synonyms_weight = float(adjacent_ranked_synonyms_weight_row[adjacent_ranked_synonyms_pos])
                    
                    if (adjacent_ranked_name_weight > adjacent_threshold) or (adjacent_ranked_description_weight > adjacent_threshold) or (adjacent_ranked_synonyms_weight > adjacent_threshold):
                        adjacent_accuracy = requirements_dataframe[requirements_dataframe['id_num'] == source_req_id][adjacent_ont_name]
                        adjacent_accuracy = adjacent_accuracy.bool()
                        adjacent_score = max(adjacent_ranked_name_weight, adjacent_ranked_description_weight, adjacent_ranked_synonyms_weight)
                        req_to_ont_pair = [source_req_id, source_ont_id, source_ont_name, source_score, source_accuracy, adjacent_ont_id, adjacent_ont_name, adjacent_score, adjacent_accuracy]
                        req_to_ont_adjacent_pairing.append(req_to_ont_pair)
            else:
                for adjacent in adjacent_list:
                    temp = str(adjacent)
                    temp = temp.split('_')
                    adjacent_ont_id = int(temp[0])
                    adjacent_ont_name = temp[1]      
                    pairing_dataframe = semantic_pairing_initial_dataframe[semantic_pairing_initial_dataframe['req_id'] == source_req_id]
                    paired_ont_list = pairing_dataframe['ont_id'].unique()
                    
                    if adjacent_ont_id not in paired_ont_list:
                        adjacent_ranked_name_row = (req_to_ont_ordered_name_pairing_norm[req_to_ont_ordered_name_pairing_norm['req_id'] == str(source_req_id)]).values     
                        adjacent_ranked_name_row = adjacent_ranked_name_row.tolist()
                        adjacent_ranked_name_row = adjacent_ranked_name_row[0]  
                        adjacent_ranked_name_pos = adjacent_ranked_name_row.index(adjacent_ont_name)              
                        adjacent_ranked_name_weight_row = (req_to_ont_ordered_name_pairing_weights[req_to_ont_ordered_name_pairing_weights['req_id'] == str(source_req_id)]).values
                        adjacent_ranked_name_weight_row = adjacent_ranked_name_weight_row.tolist()
                        adjacent_ranked_name_weight_row = adjacent_ranked_name_weight_row[0]  
                        adjacent_ranked_name_weight = float(adjacent_ranked_name_weight_row[adjacent_ranked_name_pos])
                        
                        adjacent_ranked_description_row = (req_to_ont_ordered_description_pairing_norm[req_to_ont_ordered_description_pairing_norm['req_id'] == str(source_req_id)]).values     
                        adjacent_ranked_description_row = adjacent_ranked_description_row.tolist()
                        adjacent_ranked_description_row = adjacent_ranked_description_row[0]  
                        adjacent_ranked_description_pos = adjacent_ranked_description_row.index(adjacent_ont_name)              
                        adjacent_ranked_description_weight_row = (req_to_ont_ordered_description_pairing_weights[req_to_ont_ordered_description_pairing_weights['req_id'] == str(source_req_id)]).values
                        adjacent_ranked_description_weight_row = adjacent_ranked_description_weight_row.tolist()
                        adjacent_ranked_description_weight_row = adjacent_ranked_description_weight_row[0]  
                        adjacent_ranked_description_weight = float(adjacent_ranked_description_weight_row[adjacent_ranked_description_pos])
                        
                        adjacent_ranked_synonyms_row = (req_to_ont_ordered_synonyms_pairing_norm[req_to_ont_ordered_synonyms_pairing_norm['req_id'] == str(source_req_id)]).values     
                        adjacent_ranked_synonyms_row = adjacent_ranked_synonyms_row.tolist()
                        adjacent_ranked_synonyms_row = adjacent_ranked_synonyms_row[0]  
                        adjacent_ranked_synonyms_pos = adjacent_ranked_synonyms_row.index(adjacent_ont_name)              
                        adjacent_ranked_synonyms_weight_row = (req_to_ont_ordered_synonyms_pairing_weights[req_to_ont_ordered_synonyms_pairing_weights['req_id'] == str(source_req_id)]).values
                        adjacent_ranked_synonyms_weight_row = adjacent_ranked_synonyms_weight_row.tolist()
                        adjacent_ranked_synonyms_weight_row = adjacent_ranked_synonyms_weight_row[0]  
                        adjacent_ranked_synonyms_weight = float(adjacent_ranked_synonyms_weight_row[adjacent_ranked_synonyms_pos])
                            
                        if (adjacent_ranked_name_weight > adjacent_threshold) or (adjacent_ranked_description_weight > adjacent_threshold) or (adjacent_ranked_synonyms_weight > adjacent_threshold):
                            adjacent_accuracy = requirements_dataframe[requirements_dataframe['id_num'] == source_req_id][adjacent_ont_name]
                            adjacent_accuracy = adjacent_accuracy.bool()
                            adjacent_score = max(adjacent_ranked_name_weight, adjacent_ranked_description_weight, adjacent_ranked_synonyms_weight)
                            req_to_ont_pair = [source_req_id, source_ont_id, source_ont_name, source_score, source_accuracy, adjacent_ont_id, adjacent_ont_name, adjacent_score, adjacent_accuracy]
                            req_to_ont_adjacent_pairing.append(req_to_ont_pair)
                        
                        #Uncomment this if you want every adjacent node to be added      
                        # adjacent_accuracy = requirements_dataframe[requirements_dataframe['id_num'] == source_req_id][adjacent_ont_name]
                        # adjacent_accuracy = adjacent_accuracy.bool()
                        # req_to_ont_pair = [source_req_id, source_ont_id, source_ont_name, source_score, source_accuracy, adjacent_ont_id, adjacent_ont_name, adjacent_accuracy]
                        # req_to_ont_adjacent_pairing.append(req_to_ont_pair)

    req_to_ont_adjacent_pairing = pd.DataFrame(req_to_ont_adjacent_pairing, columns = req_ont_pairing_column_names)
    req_to_ont_adjacent_pairing.to_csv('final_output_req_to_ont_adjacent_pairing.csv', index=False)
    print('Adjacent node re-evaluation completed')

def weighted_pathing_tool():
    #This section is the Weighted Pathing Tool
    #This next section will cycle through all requirements and identify requirements with two or more identified ontology nodes and attempt to find the highest semantic pathway between those nodes.
    #For each requirement it will recommend up to six pathways.  It will 3 of those recommended will be the three pathways with the highest average semantic scores along the pathway including 
    # the start and end nodes.  The other 3 will be the three pathways with the highest average semantic scores along the pathway but excluding the start and end nodes.  The score contributed 
    # by each node is the highest semantic score among that node's three attributes (name, description, and synonym) and the current requirement.
    data_file = 'adjacent_nodes.csv'
    adjacency_dataframe = pd.read_csv(data_file,sep=',')
    
    data_file = 'final_output_req_to_ont_semantic_pairing_initial.csv'
    semantic_pairing_initial_dataframe = pd.read_csv(data_file,sep=',')   
    
    #These matrices are ranked from highest to lowest STS for names
    data_file = 'req_to_ont_ordered_name_pairing_names.csv'
    req_to_ont_ordered_name_pairing_norm = pd.read_csv(data_file,sep=',')  
    
    data_file = 'req_to_ont_ordered_name_pairing_weights.csv'
    req_to_ont_ordered_name_pairing_weights = pd.read_csv(data_file,sep=',')  
    
    #These matrices are ranked from highest to lowest STS for descriptions
    data_file = 'req_to_ont_ordered_description_pairing_names.csv'
    req_to_ont_ordered_description_pairing_norm = pd.read_csv(data_file,sep=',')  
    
    data_file = 'req_to_ont_ordered_description_pairing_weights.csv'
    req_to_ont_ordered_description_pairing_weights = pd.read_csv(data_file,sep=',')  
    
    data_file = 'final_output_req_to_ont_adjacent_pairing.csv'
    req_to_ont_adjacent_pairing = pd.read_csv(data_file,sep=',')  
    
    #These matrices are ranked from highest to lowest STS for synonyms
    data_file = 'req_to_ont_ordered_synonyms_pairing_names.csv'
    req_to_ont_ordered_synonyms_pairing_norm = pd.read_csv(data_file,sep=',')  
    
    data_file = 'req_to_ont_ordered_synonyms_pairing_weights.csv'
    req_to_ont_ordered_synonyms_pairing_weights = pd.read_csv(data_file,sep=',')  
 
    unique_requirements = semantic_pairing_initial_dataframe['req_id'].unique()

    best_paths = []
    best_paths_column_names = ['source_req', 'averaged_over', 'average_semantic_score', 'best_pathway_node_names', 'best_pathway_node_ids']

    complete_paths = []
    complete_paths_name = []        
    complete_paths_num_nodes = []
    complete_paths_semantic_score = []
    complete_paths_semantic_score_interior = []
    complete_paths_source_req = []

    for unique_req in unique_requirements:
        unique_dataframe = semantic_pairing_initial_dataframe[semantic_pairing_initial_dataframe['req_id'] == unique_req]
        unique_ontology = unique_dataframe['ont_id'].unique()
        adjacent_dataframe = req_to_ont_adjacent_pairing[req_to_ont_adjacent_pairing['source_req_id'] == unique_req]
        adjacent_ontologies = adjacent_dataframe['adjacent_ont_id'].unique()
        if len(adjacent_ontologies) != 0:
            for adjacent_ontology in adjacent_ontologies:
                if adjacent_ontology not in unique_ontology:
                    unique_ontology = np.append(unique_ontology,adjacent_ontology)

        
        node_combinations = []
        if len(unique_ontology) > 1:
            pathing = True
            added_nodes = ''
            start_index = 0
            stop_index = 0
            for unique_starting_node in unique_ontology:
                # start_node = unique_starting_node[0]
                start_node = unique_starting_node
                start_index = start_index + 1
                for unique_ending_node in unique_ontology:
                    # end_node = unique_ending_node[0]
                    end_node = unique_ending_node
                    stop_index = stop_index + 1
                    #Only perform one way comparisons against non-self values
                    if (unique_starting_node != unique_ending_node) and (stop_index > start_index):                       
                        node_combination = str(unique_req) + '\\' + str(start_node) + '\\' + str(end_node)
                        node_combination_reverse = str(unique_req) + '\\' + str(end_node) + '\\' + str(start_node)
                        if (node_combination not in node_combinations) and (node_combination_reverse not in node_combinations):
                            pathing = True
                            node_combinations.append(node_combination)
                        else:
                            pathing = False
        
                        if pathing == True:        
                            pathways_running = True
                            current_paths = [start_node]
                            current_paths_last_node = [start_node]
                            current_paths_continue = [True]
                            score_dataframe = unique_dataframe[unique_dataframe['ont_id'] == start_node]
                            if len(score_dataframe) == 0:
                                #if you're here then the score came from the adjacent dataframe
                                score_dataframe = adjacent_dataframe[adjacent_dataframe['adjacent_ont_id'] == start_node]
                                current_paths_name = score_dataframe['adjacent_ont_name'].unique()
                                current_paths_name = [current_paths_name[0]]
                                current_paths_num_nodes = [1]
                                current_paths_semantic_score = [score_dataframe.iloc[0][7]]
                            else:
                                #if you're here then the score came from the original dataframe
                                current_paths_name = score_dataframe['ontology_part'].unique()
                                current_paths_name = [current_paths_name[0]]
                                current_paths_num_nodes = [1]
                                current_paths_semantic_score = [score_dataframe.iloc[0][3]]
                            # current_paths_semantic_score = [score_dataframe['semantic_similarity_score'].max()]
                            current_paths_semantic_score_interior = [0]
                            next_paths = []
                            next_paths_name = []
                            next_paths_num_nodes = []
                            next_paths_last_node = []
                            next_paths_continue = []
                            next_paths_semantic_score = []
                            next_paths_semantic_score_interior = []
                            # print(node_combination)
                            
                            while pathways_running == True:
                                iteration = 0
                                if len(current_paths) == 1:
                                    i = 0
                                    if bool(current_paths_continue[i]) == True:
                                        adjacent_list = adjacency_dataframe.iloc[int(current_paths_last_node[i])]
                                        adjacent_list = str(adjacent_list[1])
                                        adjacent_list = adjacent_list.split('\\')
                                                    
                                        if len(adjacent_list) == 1:
                                            adjacent_str = str(adjacent_list[0])
                                            adjacent_str_split = adjacent_str.split('_')
                                            adjacent_value = adjacent_str_split[0]
                                            adjacent_ont_name = adjacent_str_split[1]
                                            if adjacent_value not in str(current_paths[i]):
                                                temp_paths = str(current_paths[i]) + '\\' + str(adjacent_value)
                                                temp_paths_name = str(current_paths_name[i]) + '\\' + str(adjacent_ont_name)
                                                temp_paths_num_nodes = int(current_paths_num_nodes[i]) + 1
                                                temp_paths_last_node = str(adjacent_value)
                                                if str(adjacent_value) == str(end_node):
                                                    temp_paths_continue = [False]
                                                else:
                                                    temp_paths_continue = [True]
                                                    
                                                adjacent_ranked_name_row = (req_to_ont_ordered_name_pairing_norm[req_to_ont_ordered_name_pairing_norm['req_id'] == int(unique_req)]).values     
                                                adjacent_ranked_name_row = adjacent_ranked_name_row.tolist()
                                                adjacent_ranked_name_row = adjacent_ranked_name_row[0]  
                                                adjacent_ranked_name_pos = adjacent_ranked_name_row.index(adjacent_ont_name)              
                                                adjacent_ranked_name_weight_row = (req_to_ont_ordered_name_pairing_weights[req_to_ont_ordered_name_pairing_weights['req_id'] == int(unique_req)]).values
                                                adjacent_ranked_name_weight_row = adjacent_ranked_name_weight_row.tolist()
                                                adjacent_ranked_name_weight_row = adjacent_ranked_name_weight_row[0]  
                                                adjacent_ranked_name_weight = float(adjacent_ranked_name_weight_row[adjacent_ranked_name_pos])
                                                
                                                adjacent_ranked_description_row = (req_to_ont_ordered_description_pairing_norm[req_to_ont_ordered_description_pairing_norm['req_id'] == int(unique_req)]).values     
                                                adjacent_ranked_description_row = adjacent_ranked_description_row.tolist()
                                                adjacent_ranked_description_row = adjacent_ranked_description_row[0]  
                                                adjacent_ranked_description_pos = adjacent_ranked_description_row.index(adjacent_ont_name)              
                                                adjacent_ranked_description_weight_row = (req_to_ont_ordered_description_pairing_weights[req_to_ont_ordered_description_pairing_weights['req_id'] == int(unique_req)]).values
                                                adjacent_ranked_description_weight_row = adjacent_ranked_description_weight_row.tolist()
                                                adjacent_ranked_description_weight_row = adjacent_ranked_description_weight_row[0]  
                                                adjacent_ranked_description_weight = float(adjacent_ranked_description_weight_row[adjacent_ranked_description_pos])
                                                
                                                adjacent_ranked_synonyms_row = (req_to_ont_ordered_synonyms_pairing_norm[req_to_ont_ordered_synonyms_pairing_norm['req_id'] == int(unique_req)]).values     
                                                adjacent_ranked_synonyms_row = adjacent_ranked_synonyms_row.tolist()
                                                adjacent_ranked_synonyms_row = adjacent_ranked_synonyms_row[0]  
                                                adjacent_ranked_synonyms_pos = adjacent_ranked_synonyms_row.index(adjacent_ont_name)              
                                                adjacent_ranked_synonyms_weight_row = (req_to_ont_ordered_synonyms_pairing_weights[req_to_ont_ordered_synonyms_pairing_weights['req_id'] == int(unique_req)]).values
                                                adjacent_ranked_synonyms_weight_row = adjacent_ranked_synonyms_weight_row.tolist()
                                                adjacent_ranked_synonyms_weight_row = adjacent_ranked_synonyms_weight_row[0]  
                                                adjacent_ranked_synonyms_weight = float(adjacent_ranked_synonyms_weight_row[adjacent_ranked_synonyms_pos])
                                                
                                                scores = [adjacent_ranked_name_weight, adjacent_ranked_description_weight, adjacent_ranked_synonyms_weight]                                       
                                                temp_paths_semantic_score = current_paths_semantic_score[i] + max(scores)
                                                if str(adjacent_value) != str(end_node):
                                                    temp_paths_semantic_score_interior = current_paths_semantic_score_interior[i] + max(scores)
                                                else:
                                                    temp_paths_semantic_score_interior = current_paths_semantic_score_interior[i]
                                                
                                                next_paths.append(temp_paths)
                                                next_paths_name.append(temp_paths_name)
                                                next_paths_num_nodes.append(temp_paths_num_nodes)
                                                next_paths_last_node.append(temp_paths_last_node)
                                                next_paths_continue.append(temp_paths_continue)
                                                next_paths_semantic_score.append(temp_paths_semantic_score)  
                                                next_paths_semantic_score_interior.append(temp_paths_semantic_score_interior)  
                                                
                                                iteration = iteration + 1
                                                
                                                if str(adjacent_value) == str(end_node):
                                                        complete_paths.append(temp_paths)  
                                                        complete_paths_name.append(temp_paths_name)  
                                                        complete_paths_num_nodes.append(temp_paths_num_nodes)  
                                                        complete_paths_semantic_score.append(temp_paths_semantic_score)
                                                        complete_paths_semantic_score_interior.append(temp_paths_semantic_score_interior)  
                                                        complete_paths_source_req.append(unique_req)  
                            
                                        else:
                                            for adjacent in adjacent_list:
                                                adjacent_str = str(adjacent)
                                                adjacent_str_split = adjacent_str.split('_')
                                                adjacent_value = adjacent_str_split[0]
                                                adjacent_ont_name = adjacent_str_split[1]
                                                if adjacent_value not in str(current_paths[i]):
                                                    temp_paths = str(current_paths[i]) + '\\' + str(adjacent_value)
                                                    temp_paths_name = str(current_paths_name[i]) + '\\' + str(adjacent_ont_name)
                                                    temp_paths_num_nodes = int(current_paths_num_nodes[i]) + 1
                                                    temp_paths_last_node = str(adjacent_value)
                                                    if str(adjacent_value) == str(end_node):
                                                        temp_paths_continue = [False]
                                                    else:
                                                        temp_paths_continue = [True]
                                                    
                                                    adjacent_ranked_name_row = (req_to_ont_ordered_name_pairing_norm[req_to_ont_ordered_name_pairing_norm['req_id'] == int(unique_req)]).values     
                                                    adjacent_ranked_name_row = adjacent_ranked_name_row.tolist()
                                                    adjacent_ranked_name_row = adjacent_ranked_name_row[0]  
                                                    adjacent_ranked_name_pos = adjacent_ranked_name_row.index(adjacent_ont_name)              
                                                    adjacent_ranked_name_weight_row = (req_to_ont_ordered_name_pairing_weights[req_to_ont_ordered_name_pairing_weights['req_id'] == int(unique_req)]).values
                                                    adjacent_ranked_name_weight_row = adjacent_ranked_name_weight_row.tolist()
                                                    adjacent_ranked_name_weight_row = adjacent_ranked_name_weight_row[0]  
                                                    adjacent_ranked_name_weight = float(adjacent_ranked_name_weight_row[adjacent_ranked_name_pos])
                                                    
                                                    adjacent_ranked_description_row = (req_to_ont_ordered_description_pairing_norm[req_to_ont_ordered_description_pairing_norm['req_id'] == int(unique_req)]).values     
                                                    adjacent_ranked_description_row = adjacent_ranked_description_row.tolist()
                                                    adjacent_ranked_description_row = adjacent_ranked_description_row[0]  
                                                    adjacent_ranked_description_pos = adjacent_ranked_description_row.index(adjacent_ont_name)              
                                                    adjacent_ranked_description_weight_row = (req_to_ont_ordered_description_pairing_weights[req_to_ont_ordered_description_pairing_weights['req_id'] == int(unique_req)]).values
                                                    adjacent_ranked_description_weight_row = adjacent_ranked_description_weight_row.tolist()
                                                    adjacent_ranked_description_weight_row = adjacent_ranked_description_weight_row[0]  
                                                    adjacent_ranked_description_weight = float(adjacent_ranked_description_weight_row[adjacent_ranked_description_pos])
                                                    
                                                    adjacent_ranked_synonyms_row = (req_to_ont_ordered_synonyms_pairing_norm[req_to_ont_ordered_synonyms_pairing_norm['req_id'] == int(unique_req)]).values     
                                                    adjacent_ranked_synonyms_row = adjacent_ranked_synonyms_row.tolist()
                                                    adjacent_ranked_synonyms_row = adjacent_ranked_synonyms_row[0]  
                                                    adjacent_ranked_synonyms_pos = adjacent_ranked_synonyms_row.index(adjacent_ont_name)              
                                                    adjacent_ranked_synonyms_weight_row = (req_to_ont_ordered_synonyms_pairing_weights[req_to_ont_ordered_synonyms_pairing_weights['req_id'] == int(unique_req)]).values
                                                    adjacent_ranked_synonyms_weight_row = adjacent_ranked_synonyms_weight_row.tolist()
                                                    adjacent_ranked_synonyms_weight_row = adjacent_ranked_synonyms_weight_row[0]  
                                                    adjacent_ranked_synonyms_weight = float(adjacent_ranked_synonyms_weight_row[adjacent_ranked_synonyms_pos])
                                                    
                                                    scores = [adjacent_ranked_name_weight, adjacent_ranked_description_weight, adjacent_ranked_synonyms_weight]                                       
                                                    temp_paths_semantic_score = current_paths_semantic_score[i] + max(scores)
                                                    if str(adjacent_value) != str(end_node):
                                                        temp_paths_semantic_score_interior = current_paths_semantic_score_interior[i] + max(scores)
                                                    else:
                                                        temp_paths_semantic_score_interior = current_paths_semantic_score_interior[i]
                                                                                                    
                                                    next_paths.append(temp_paths)
                                                    next_paths_name.append(temp_paths_name)
                                                    next_paths_num_nodes.append(temp_paths_num_nodes)
                                                    next_paths_last_node.append(temp_paths_last_node)
                                                    next_paths_continue.append(temp_paths_continue)
                                                    next_paths_semantic_score.append(temp_paths_semantic_score)  
                                                    next_paths_semantic_score_interior.append(temp_paths_semantic_score_interior)  
                                                    
                                                    iteration = iteration + 1
                                                    
                                                    if str(adjacent_value) == str(end_node):
                                                        complete_paths.append(temp_paths)  
                                                        complete_paths_name.append(temp_paths_name)  
                                                        complete_paths_num_nodes.append(temp_paths_num_nodes)  
                                                        complete_paths_semantic_score.append(temp_paths_semantic_score)
                                                        complete_paths_semantic_score_interior.append(temp_paths_semantic_score_interior)  
                                                        complete_paths_source_req.append(unique_req)  
                                                                
                                ##If you're here there are multiple paths
                                else:
                                    for i in range(0,len(current_paths)):
                                        if bool(current_paths_continue[i]) == True:
                                            adjacent_list = adjacency_dataframe.iloc[int(current_paths_last_node[i])]
                                            adjacent_list = str(adjacent_list[1])
                                            adjacent_list = adjacent_list.split('\\')
                                                        
                                            if len(adjacent_list) == 1:
                                                adjacent_str = str(adjacent)
                                                adjacent_str_split = adjacent_str.split('_')
                                                adjacent_value = adjacent_str_split[0]
                                                adjacent_ont_name = adjacent_str_split[1]
                                                if adjacent_value not in str(current_paths[i]):
                                                    temp_paths = str(current_paths[i]) + '\\' + str(adjacent_value)
                                                    temp_paths_name = str(current_paths_name[i]) + '\\' + str(adjacent_ont_name)
                                                    temp_paths_num_nodes = int(current_paths_num_nodes[i]) + 1
                                                    temp_paths_last_node = str(adjacent_value)
                                                    if str(adjacent_value) == str(end_node):
                                                        temp_paths_continue = [False]
                                                    else:
                                                        temp_paths_continue = [True]
                                                        
                                                    adjacent_ranked_name_row = (req_to_ont_ordered_name_pairing_norm[req_to_ont_ordered_name_pairing_norm['req_id'] == int(unique_req)]).values     
                                                    adjacent_ranked_name_row = adjacent_ranked_name_row.tolist()
                                                    adjacent_ranked_name_row = adjacent_ranked_name_row[0]  
                                                    adjacent_ranked_name_pos = adjacent_ranked_name_row.index(adjacent_ont_name)              
                                                    adjacent_ranked_name_weight_row = (req_to_ont_ordered_name_pairing_weights[req_to_ont_ordered_name_pairing_weights['req_id'] == int(unique_req)]).values
                                                    adjacent_ranked_name_weight_row = adjacent_ranked_name_weight_row.tolist()
                                                    adjacent_ranked_name_weight_row = adjacent_ranked_name_weight_row[0]  
                                                    adjacent_ranked_name_weight = float(adjacent_ranked_name_weight_row[adjacent_ranked_name_pos])
                                                    
                                                    adjacent_ranked_description_row = (req_to_ont_ordered_description_pairing_norm[req_to_ont_ordered_description_pairing_norm['req_id'] == int(unique_req)]).values     
                                                    adjacent_ranked_description_row = adjacent_ranked_description_row.tolist()
                                                    adjacent_ranked_description_row = adjacent_ranked_description_row[0]  
                                                    adjacent_ranked_description_pos = adjacent_ranked_description_row.index(adjacent_ont_name)              
                                                    adjacent_ranked_description_weight_row = (req_to_ont_ordered_description_pairing_weights[req_to_ont_ordered_description_pairing_weights['req_id'] == int(unique_req)]).values
                                                    adjacent_ranked_description_weight_row = adjacent_ranked_description_weight_row.tolist()
                                                    adjacent_ranked_description_weight_row = adjacent_ranked_description_weight_row[0]  
                                                    adjacent_ranked_description_weight = float(adjacent_ranked_description_weight_row[adjacent_ranked_description_pos])
                                                    
                                                    adjacent_ranked_synonyms_row = (req_to_ont_ordered_synonyms_pairing_norm[req_to_ont_ordered_synonyms_pairing_norm['req_id'] == int(unique_req)]).values     
                                                    adjacent_ranked_synonyms_row = adjacent_ranked_synonyms_row.tolist()
                                                    adjacent_ranked_synonyms_row = adjacent_ranked_synonyms_row[0]  
                                                    adjacent_ranked_synonyms_pos = adjacent_ranked_synonyms_row.index(adjacent_ont_name)              
                                                    adjacent_ranked_synonyms_weight_row = (req_to_ont_ordered_synonyms_pairing_weights[req_to_ont_ordered_synonyms_pairing_weights['req_id'] == int(unique_req)]).values
                                                    adjacent_ranked_synonyms_weight_row = adjacent_ranked_synonyms_weight_row.tolist()
                                                    adjacent_ranked_synonyms_weight_row = adjacent_ranked_synonyms_weight_row[0]  
                                                    adjacent_ranked_synonyms_weight = float(adjacent_ranked_synonyms_weight_row[adjacent_ranked_synonyms_pos])
                                                    
                                                    scores = [adjacent_ranked_name_weight, adjacent_ranked_description_weight, adjacent_ranked_synonyms_weight]                                       
                                                    temp_paths_semantic_score = current_paths_semantic_score[i] + max(scores)
                                                    if str(adjacent_value) != str(end_node):
                                                        temp_paths_semantic_score_interior = current_paths_semantic_score_interior[i] + max(scores)
                                                    else:
                                                        temp_paths_semantic_score_interior = current_paths_semantic_score_interior[i]
                                                
                                                    next_paths.append(temp_paths)
                                                    next_paths_name.append(temp_paths_name)
                                                    next_paths_num_nodes.append(temp_paths_num_nodes)
                                                    next_paths_last_node.append(temp_paths_last_node)
                                                    next_paths_continue.append(temp_paths_continue)
                                                    next_paths_semantic_score.append(temp_paths_semantic_score)  
                                                    next_paths_semantic_score_interior.append(temp_paths_semantic_score_interior)        
                                                                                
                                                    iteration = iteration + 1
                                                    
                                                    if str(adjacent_value) == str(end_node):
                                                        complete_paths.append(temp_paths)  
                                                        complete_paths_name.append(temp_paths_name)  
                                                        complete_paths_num_nodes.append(temp_paths_num_nodes)  
                                                        complete_paths_semantic_score.append(temp_paths_semantic_score)
                                                        complete_paths_semantic_score_interior.append(temp_paths_semantic_score_interior)  
                                                        complete_paths_source_req.append(unique_req)       
                                                                                            
                                            else:
                                                for adjacent in adjacent_list:
                                                    adjacent_str = str(adjacent)
                                                    adjacent_str_split = adjacent_str.split('_')
                                                    adjacent_value = adjacent_str_split[0]
                                                    adjacent_ont_name = adjacent_str_split[1]
                                                    if adjacent_value not in str(current_paths[i]):
                                                        temp_paths = str(current_paths[i]) + '\\' + str(adjacent_value)
                                                        temp_paths_name = str(current_paths_name[i]) + '\\' + str(adjacent_ont_name)
                                                        temp_paths_num_nodes = int(current_paths_num_nodes[i]) + 1
                                                        temp_paths_last_node = str(adjacent_value)
                                                        if str(adjacent_value) == str(end_node):
                                                            temp_paths_continue = [False]
                                                        else:
                                                            temp_paths_continue = [True]
                                                        
                                                        adjacent_ranked_name_row = (req_to_ont_ordered_name_pairing_norm[req_to_ont_ordered_name_pairing_norm['req_id'] == int(unique_req)]).values     
                                                        adjacent_ranked_name_row = adjacent_ranked_name_row.tolist()
                                                        adjacent_ranked_name_row = adjacent_ranked_name_row[0]  
                                                        adjacent_ranked_name_pos = adjacent_ranked_name_row.index(adjacent_ont_name)              
                                                        adjacent_ranked_name_weight_row = (req_to_ont_ordered_name_pairing_weights[req_to_ont_ordered_name_pairing_weights['req_id'] == int(unique_req)]).values
                                                        adjacent_ranked_name_weight_row = adjacent_ranked_name_weight_row.tolist()
                                                        adjacent_ranked_name_weight_row = adjacent_ranked_name_weight_row[0]  
                                                        adjacent_ranked_name_weight = float(adjacent_ranked_name_weight_row[adjacent_ranked_name_pos])
                                                        
                                                        adjacent_ranked_description_row = (req_to_ont_ordered_description_pairing_norm[req_to_ont_ordered_description_pairing_norm['req_id'] == int(unique_req)]).values     
                                                        adjacent_ranked_description_row = adjacent_ranked_description_row.tolist()
                                                        adjacent_ranked_description_row = adjacent_ranked_description_row[0]  
                                                        adjacent_ranked_description_pos = adjacent_ranked_description_row.index(adjacent_ont_name)              
                                                        adjacent_ranked_description_weight_row = (req_to_ont_ordered_description_pairing_weights[req_to_ont_ordered_description_pairing_weights['req_id'] == int(unique_req)]).values
                                                        adjacent_ranked_description_weight_row = adjacent_ranked_description_weight_row.tolist()
                                                        adjacent_ranked_description_weight_row = adjacent_ranked_description_weight_row[0]  
                                                        adjacent_ranked_description_weight = float(adjacent_ranked_description_weight_row[adjacent_ranked_description_pos])
                                                        
                                                        adjacent_ranked_synonyms_row = (req_to_ont_ordered_synonyms_pairing_norm[req_to_ont_ordered_synonyms_pairing_norm['req_id'] == int(unique_req)]).values     
                                                        adjacent_ranked_synonyms_row = adjacent_ranked_synonyms_row.tolist()
                                                        adjacent_ranked_synonyms_row = adjacent_ranked_synonyms_row[0]  
                                                        adjacent_ranked_synonyms_pos = adjacent_ranked_synonyms_row.index(adjacent_ont_name)              
                                                        adjacent_ranked_synonyms_weight_row = (req_to_ont_ordered_synonyms_pairing_weights[req_to_ont_ordered_synonyms_pairing_weights['req_id'] == int(unique_req)]).values
                                                        adjacent_ranked_synonyms_weight_row = adjacent_ranked_synonyms_weight_row.tolist()
                                                        adjacent_ranked_synonyms_weight_row = adjacent_ranked_synonyms_weight_row[0]  
                                                        adjacent_ranked_synonyms_weight = float(adjacent_ranked_synonyms_weight_row[adjacent_ranked_synonyms_pos])
                                                        
                                                        scores = [adjacent_ranked_name_weight, adjacent_ranked_description_weight, adjacent_ranked_synonyms_weight]                                       
                                                        temp_paths_semantic_score = current_paths_semantic_score[i] + max(scores)
                                                        if str(adjacent_value) != str(end_node):
                                                            temp_paths_semantic_score_interior = current_paths_semantic_score_interior[i] + max(scores)
                                                        else:
                                                            temp_paths_semantic_score_interior = current_paths_semantic_score_interior[i]

                                                        
                                                        next_paths.append(temp_paths)
                                                        next_paths_name.append(temp_paths_name)
                                                        next_paths_num_nodes.append(temp_paths_num_nodes)
                                                        next_paths_last_node.append(temp_paths_last_node)
                                                        next_paths_continue.append(temp_paths_continue)
                                                        next_paths_semantic_score.append(temp_paths_semantic_score)  
                                                        next_paths_semantic_score_interior.append(temp_paths_semantic_score_interior)  
                                                        
                                                        iteration = iteration + 1
                                                        
                                                        if str(adjacent_value) == str(end_node):
                                                            complete_paths.append(temp_paths)  
                                                            complete_paths_name.append(temp_paths_name)  
                                                            complete_paths_num_nodes.append(temp_paths_num_nodes)  
                                                            complete_paths_semantic_score.append(temp_paths_semantic_score)
                                                            complete_paths_semantic_score_interior.append(temp_paths_semantic_score_interior)
                                                            complete_paths_source_req.append(unique_req)  
                                                                        
                                current_paths = next_paths
                                current_paths_name = next_paths_name
                                current_paths_num_nodes = next_paths_num_nodes
                                current_paths_last_node = next_paths_last_node
                                current_paths_continue = next_paths_continue
                                current_paths_semantic_score = next_paths_semantic_score
                                current_paths_semantic_score_interior = next_paths_semantic_score_interior
                                next_paths = []
                                next_paths_name = []
                                next_paths_num_nodes = []
                                next_paths_last_node = []
                                next_paths_continue = []
                                next_paths_semantic_score = []      
                                next_paths_semantic_score_interior = []       
                                
                                if iteration == 0:
                                    pathways_running = False
                                                                    
                            semantic_average = []
                            highest_average = 0
                            highest_average_entry = 0
                            second_highest_average = 0
                            second_highest_average_entry = 0
                            third_highest_average = 0
                            third_highest_average_entry = 0

                            highest_average_interior = 0
                            highest_average_entry_interior = 0
                            second_highest_average_interior = 0
                            second_highest_average_entry_interior = 0
                            third_highest_average_interior = 0
                            third_highest_average_entry_interior = 0                        
                            
                            
                            for entry in range(0,(len(complete_paths_semantic_score)-1)):
                                current_semantic_score = float(complete_paths_semantic_score[entry])
                                current_semantic_score_interior = float(complete_paths_semantic_score_interior[entry])
                                current_num_nodes = float(complete_paths_num_nodes[entry])
                                average = current_semantic_score/current_num_nodes
                                if current_num_nodes > 2:
                                    average_interior = current_semantic_score_interior / (current_num_nodes - 2)
                                else:
                                    average_interior = 1
                                    
                                if average > highest_average:
                                    third_highest_average = second_highest_average
                                    third_highest_average_entry = second_highest_average_entry
                                    second_highest_average = highest_average
                                    second_highest_average_entry = highest_average_entry
                                    highest_average = average
                                    highest_average_entry = entry
                                elif average > second_highest_average:
                                    third_highest_average = second_highest_average
                                    third_highest_average_entry = second_highest_average_entry
                                    second_highest_average = average
                                    second_highest_average_entry = entry               
                                elif average > third_highest_average:
                                    third_highest_average = average
                                    third_highest_average_entry = entry          
                                    
                                if average_interior > highest_average_interior:
                                    third_highest_average_interior = second_highest_average_interior
                                    third_highest_average_entry_interior = second_highest_average_entry_interior
                                    second_highest_average_interior = highest_average_interior
                                    second_highest_average_entry_interior = highest_average_entry_interior
                                    highest_average_interior = average_interior
                                    highest_average_entry_interior = entry
                                elif average_interior > second_highest_average_interior:
                                    third_highest_average_interior = second_highest_average_interior
                                    third_highest_average_entry_interior = second_highest_average_entry_interior
                                    second_highest_average_interior = average_interior
                                    second_highest_average_entry_interior = entry               
                                elif average_interior > third_highest_average_interior:
                                    third_highest_average_interior = average_interior
                                    third_highest_average_entry_interior = entry       
                                    
                            if highest_average != 0:
                                best_req = str(complete_paths_source_req[highest_average_entry])
                                best_path_names = complete_paths_name[highest_average_entry]
                                best_path_ids = complete_paths[highest_average_entry]
                                best_path = [best_req, 'whole pathway', str(highest_average), best_path_names, best_path_ids]
                                best_paths.append(best_path)
                                
                            if second_highest_average != 0:
                                best_req = str(complete_paths_source_req[second_highest_average_entry])
                                best_path_names = complete_paths_name[second_highest_average_entry]
                                best_path_ids = complete_paths[second_highest_average_entry]
                                best_path = [best_req, 'whole pathway', str(second_highest_average), best_path_names, best_path_ids]
                                best_paths.append(best_path)
                                        
                            if third_highest_average != 0:
                                best_req = str(complete_paths_source_req[third_highest_average_entry])
                                best_path_names = complete_paths_name[third_highest_average_entry]
                                best_path_ids = complete_paths[third_highest_average_entry]
                                best_path = [best_req, 'whole pathway', str(third_highest_average), best_path_names, best_path_ids]
                                best_paths.append(best_path)
                                
                                
                            if highest_average_interior != 0:
                                best_req = str(complete_paths_source_req[highest_average_entry_interior])
                                best_path_names = complete_paths_name[highest_average_entry_interior]
                                best_path_ids = complete_paths[highest_average_entry_interior]
                                best_path = [best_req, 'interior nodes only', str(highest_average_interior), best_path_names, best_path_ids]
                                best_paths.append(best_path)
                                
                            if second_highest_average_interior != 0:
                                best_req = str(complete_paths_source_req[second_highest_average_entry_interior])
                                best_path_names = complete_paths_name[second_highest_average_entry_interior]
                                best_path_ids = complete_paths[second_highest_average_entry_interior]
                                best_path = [best_req, 'interior nodes only', str(second_highest_average_interior), best_path_names, best_path_ids]
                                best_paths.append(best_path)
                                        
                            if third_highest_average_interior != 0:
                                best_req = str(complete_paths_source_req[third_highest_average_entry_interior])
                                best_path_names = complete_paths_name[third_highest_average_entry_interior]
                                best_path_ids = complete_paths[third_highest_average_entry_interior]
                                best_path = [best_req, 'interior nodes only', str(third_highest_average_interior), best_path_names, best_path_ids]
                                best_paths.append(best_path)    
                                
                            next_paths = []
                            next_paths_name = []
                            next_paths_num_nodes = []
                            next_paths_last_node = []
                            next_paths_continue = []
                            next_paths_semantic_score = []   
                            next_paths_semantic_score_interior = []         
                            complete_paths = []  
                            complete_paths_name = []  
                            complete_paths_num_nodes = []   
                            complete_paths_semantic_score = [] 
                            complete_paths_semantic_score_interior = []
                            complete_paths_source_req = [] 
                             
                stop_index = 0
        else:
            pathing = False
        x=1            
    x=1            

    best_paths = pd.DataFrame(best_paths, columns = best_paths_column_names)
    best_paths.to_csv('final_output_best_paths.csv', index=False)
    print('Weighted pathing completed')