import csv
import math
import numpy as np
import pandas as pd

#This section will compile all the results with respect to the requirement identifier desired.
def requirement_result_compiler(requirement_file_name, requirement_of_interest, semantic_threshold, secondary_semantic_threshold):
    
    print(' ')
    print('********************************************************************************************************************************')
    print(' ')
    print('Running Score Compiler')
    print('The following are the results comparing to Requirement #' + str(requirement_of_interest))
    
    data_file = 'final_output_best_paths.csv'
    best_paths_dataframe = pd.read_csv(data_file,sep=',')

    data_file = 'final_output_req_to_ont_adjacent_pairing.csv'
    adjacent_node_dataframe = pd.read_csv(data_file,sep=',')
    
    data_file = 'adjacent_nodes.csv'
    adjacency_dataframe = pd.read_csv(data_file,sep=',')

    data_file = 'final_output_req_to_req_pairing_comparison.csv'
    req_to_req_pairing_dataframe = pd.read_csv(data_file,sep=',')
    
    data_file = 'req_to_ont_comparison.csv'
    req_to_ont_comparison_dataframe = pd.read_csv(data_file,sep=',')

    # This will filter all the results dataframes on the desired requirement and consolidate the requirement.  There are two for loops since the similarity scores
    # were calculated using nested for loops.  Requirement 1 was compared to Requirement 2 and on, Requirement 2 was compared to Req 3 and on.  The first loop 
    # checks for if the desired requirement was the first requirement.  The second loop checks if the second requirement was our requirement of interest.
    best_reqs = []
    
    #This will keep track of high similarity ontology nodes for later
    high_similarity_nodes =[]
    
    #This checks the requirement similarity scores for when the current requirement was the requirement of interest
    temp_pairing_dataframe = req_to_req_pairing_dataframe[req_to_req_pairing_dataframe['req1_id'] == int(requirement_of_interest)]
    temp_pairing_dataframe.sort_values(by=['similarity'], ascending=False)
    unique_paired_requirements = temp_pairing_dataframe['req2_id'].unique()


    #Cycle through requirements compared against the desired requirement
    for unique_req in unique_paired_requirements:
        unique_dataframe = temp_pairing_dataframe[temp_pairing_dataframe['req2_id'] == unique_req]
        req_score = float(unique_dataframe['similarity'])
        current_entry = [unique_req, req_score]
        best_reqs.append(current_entry)
        
    #This checks the requirement similarity scores for when another requirement was the requirement of interest
    temp_pairing_dataframe = req_to_req_pairing_dataframe[req_to_req_pairing_dataframe['req2_id'] == int(requirement_of_interest)]  
    temp_pairing_dataframe.sort_values(by=['similarity'], ascending=False)  
    unique_paired_requirements = temp_pairing_dataframe['req1_id'].unique()
    
    #Cycle through requirements compared against the desired requirement
    for unique_req in unique_paired_requirements:
        unique_dataframe = temp_pairing_dataframe[temp_pairing_dataframe['req1_id'] == unique_req]
        req_score = float(unique_dataframe['similarity'])
        current_entry = [unique_req, req_score]
        best_reqs.append(current_entry)    
        
    best_req_dataframe = pd.DataFrame(best_reqs, columns = ['req_id', 'similarity'])
    best_req_dataframe = best_req_dataframe.sort_values(by=['similarity'], ascending=False)
    unique_paired_requirements = best_req_dataframe['req_id'].unique()
    count = 0
    bonus_count = 0
    
    print(' ')
    print('********************************************************************************************************************************')
    print(' ')
    print('Requirement to Requirement Comparison Results:')
    for unique_req in unique_paired_requirements:
        temp_req_row = best_req_dataframe[best_req_dataframe['req_id'] == unique_req]

        req_score = temp_req_row['similarity'].values[0]
        if req_score > semantic_threshold:
            print('Requirement number ' + str(requirement_of_interest) + ' exceeds the semantic similarity threshold with Requirement ' + str(unique_req) + ', with a Semantic Textual Similarity Score of ' + str(f"{req_score:.7}"))
            count = count + 1    
    
    #This section will advise the users on the five highest scores that don't exceed the threshold
    current_iteration = 0
    
    print(' ')
    print('The following do not exceed the semantic similarity threshold, but are the highest semantic scoring requirement statements:')
    for unique_req in unique_paired_requirements:
        if (current_iteration >= count) and (bonus_count < 5):
            temp_req_row = best_req_dataframe[best_req_dataframe['req_id'] == unique_req]
            req_score = temp_req_row['similarity'].values[0]
            print('Requirement number ' + str(requirement_of_interest) + ' has the next highest semantic similarity score with Requirement ' + str(unique_req) + ', with a Semantic Textual Similarity Score of ' + str(f"{req_score:.7}"))
            bonus_count = bonus_count + 1
        current_iteration = current_iteration + 1
    
    best_reqs = []
    
    #This section will find the best Requirement to Ontology pairings
    temp_pairing_dataframe = req_to_ont_comparison_dataframe[req_to_ont_comparison_dataframe['req_id'] == int(requirement_of_interest)]
    temp_pairing_dataframe = temp_pairing_dataframe.sort_values(by=['semantic_similarity'], ascending=False)
    unique_paired_onts = temp_pairing_dataframe['ont_id'].unique()
    
    print(' ')
    print('********************************************************************************************************************************')
    print(' ')
    print('Requirement to Ontology Comparison Results:')
    count = 0
    bonus_count = 0
    current_iteration = 0
    associated_nodes = []
    
    for unique_ont in unique_paired_onts:
        temp_req_row = temp_pairing_dataframe[temp_pairing_dataframe['ont_id'] == unique_ont]
        
        ont_score = temp_req_row['semantic_similarity'].values[0]
        ont_name = temp_req_row['ont_name'].values[0]
        if ont_score > semantic_threshold:
            print('Requirement number ' + str(requirement_of_interest) + ' exceeds the semantic similarity threshold with the ' + str(ont_name) + ' (Node #' + str(unique_ont) + '), with a Semantic Textual Similarity Score of ' + str(f"{ont_score:.7}"))
            high_similarity_nodes.append([unique_ont])
            associated_nodes.append(unique_ont)
            count = count + 1
    
    #This section will find all the added adjacent nodes that exceeded the second threshold
    temp_pairing_dataframe = adjacent_node_dataframe[adjacent_node_dataframe['source_req_id'] == int(requirement_of_interest)]
    temp_pairing_dataframe = temp_pairing_dataframe.sort_values(by=['adjacent_score'], ascending=False)
    unique_paired_onts = temp_pairing_dataframe['adjacent_ont_id'].unique()
    
    count = 0
    bonus_count = 0
    current_iteration = 0
    for unique_ont in unique_paired_onts:
        temp_req_row = temp_pairing_dataframe[temp_pairing_dataframe['adjacent_ont_id'] == unique_ont]
        
        ont_score = temp_req_row['adjacent_score'].values[0]
        ont_name = temp_req_row['adjacent_ont_name'].values[0]
        if (ont_score > secondary_semantic_threshold) and (unique_ont not in associated_nodes):
            print('After re-evaluation due to an adjacent node, Requirement number ' + str(requirement_of_interest) + ' exceeds the re-evaluation semantic similarity threshold with the ' + str(ont_name) + ' (Node #' + str(unique_ont) + '), with a Semantic Textual Similarity Score of ' + str(f"{ont_score:.7}"))
            high_similarity_nodes.append([unique_ont])
            count = count + 1
    
    temp_pairing_dataframe = req_to_ont_comparison_dataframe[req_to_ont_comparison_dataframe['req_id'] == int(requirement_of_interest)]
    temp_pairing_dataframe = temp_pairing_dataframe.sort_values(by=['semantic_similarity'], ascending=False)
    unique_paired_onts = temp_pairing_dataframe['ont_id'].unique()
                
    print(' ')
    print('The following do not exceed the semantic similarity threshold, but are the highest semantic scoring ontology nodes:')        
    for unique_ont in unique_paired_onts:
        if (current_iteration >= count) and (bonus_count < 5):
            temp_req_row = temp_pairing_dataframe[temp_pairing_dataframe['ont_id'] == unique_ont]
            ont_score = temp_req_row['semantic_similarity'].values[0]
            ont_name = temp_req_row['ont_name'].values[0]
            print('Requirement number ' + str(requirement_of_interest) + ' has the next highest semantic similarity score with the ' + str(ont_name) + ' (Node #' + str(unique_ont) + '), with a Semantic Textual Similarity Score of ' + str(f"{ont_score:.7}"))
            high_similarity_nodes.append([unique_ont])
            bonus_count = bonus_count + 1
        current_iteration = current_iteration + 1
        
        
    #This next section will identify the highest scoring requirements associated with high semantic similarity ontology nodes.
    ont_count = 0
    print(' ')
    print('********************************************************************************************************************************')
    print(' ')
    print('Associated Ontologies having high semantic similarity with other requirement analysis:')
    for unique_ont in high_similarity_nodes:
        if ont_count < 3:
            temp_pairing_dataframe = req_to_ont_comparison_dataframe.sort_values(by=['semantic_similarity'], ascending=False)
            ont_id = int(unique_ont[0])
            temp_pairing_dataframe = temp_pairing_dataframe[temp_pairing_dataframe['ont_id'] == ont_id]
            unique_paired_reqs = temp_pairing_dataframe['req_id'].unique()
            req_count = 0
            for unique_req in unique_paired_reqs:
                if (int(unique_req) != int(requirement_of_interest)) and (req_count < 5):
                    temp_req_row = temp_pairing_dataframe[temp_pairing_dataframe['req_id'] == unique_req]
                    req_score = temp_req_row['semantic_similarity'].values[0]
                    ont_name = temp_req_row['ont_name'].values[0]
                    print('Requirement number ' + str(requirement_of_interest) + ' has high semantic similarity score with the ' + str(ont_name) + ' (Node #' + str(ont_id) + '), which has high Semantic Textual Similarity with Requirement '+str(unique_req) +  ' with a STS Score of ' + str(f"{req_score:.7}"))
                    req_count = req_count + 1
            print(' ')
            ont_count = ont_count + 1
            
    print('********************************************************************************************************************************')
    print(' ')
    print('The following are the requirements with highest semantic similarity scores to adjacent nodes:')
    #This next section will identify the highest scoring requirements associated with nodes adjacent to high semantic similarity ontology nodes.
    ont_count = 0
    adjacent_node_list = []
    adjacent_node_name_list = []
    source_node_list = []
    
    for unique_ont in high_similarity_nodes:
        if ont_count < 3:
            ont_id = int(unique_ont[0])
            #This section will find all nodes adjacent to the current high similarity node.  Only unique ones will be printed
            adjacent_list = adjacency_dataframe.iloc[ont_id]
            source_node = str(adjacent_list[0])
            source_list = source_node.split('\\') 
            source_str = str(source_list[0])
            source_str_split = source_str.split('_')
            source_ont_name = source_str_split[1]
            
            adjacent_list = str(adjacent_list[1])
            adjacent_list = adjacent_list.split('\\') 
            
            if len(adjacent_list) == 1:
                adjacent_str = str(adjacent_list[0])
                adjacent_str_split = adjacent_str.split('_')
                adjacent_value = adjacent_str_split[0]
                adjacent_ont_name = adjacent_str_split[1]
                if adjacent_value not in str(adjacent_node_list):
                    adjacent_node_list.append(adjacent_value)
                    adjacent_node_name_list.append(adjacent_ont_name)
                    source_node_list.append(source_ont_name)
                    
            else:
                for adjacent in adjacent_list:
                    adjacent_str = str(adjacent)
                    adjacent_str_split = adjacent_str.split('_')
                    adjacent_value = adjacent_str_split[0]
                    adjacent_ont_name = adjacent_str_split[1]
                    if adjacent_value not in str(adjacent_node_list):
                        adjacent_node_list.append(adjacent_value)
                        adjacent_node_name_list.append(adjacent_ont_name)
                        source_node_list.append(source_ont_name)
                        
    for adjacent_value in adjacent_node_list:
        adjacent_pos = adjacent_node_list.index(adjacent_value)  
        source = source_node_list[adjacent_pos]
        adjacent_node = adjacent_node_name_list[adjacent_pos]
        if int(adjacent_value) not in associated_nodes:
            print(' ')
            print('The following are because the ' + str(adjacent_node) + ' is adjacent to the ' + str(source) + ' which had relatively high semantic similarity to Requirement ' + str(requirement_of_interest))
            temp_pairing_dataframe = req_to_ont_comparison_dataframe.sort_values(by=['semantic_similarity'], ascending=False)
            temp_pairing_dataframe = temp_pairing_dataframe[temp_pairing_dataframe['req_id'] != int(requirement_of_interest)]
            temp_pairing_dataframe = temp_pairing_dataframe[temp_pairing_dataframe['ont_id'] == int(adjacent_value)]
            temp_pairing_dataframe = temp_pairing_dataframe.sort_values(by=['semantic_similarity'], ascending=False)             
            unique_paired_reqs = temp_pairing_dataframe['req_id'].unique()
            # unique_paired_reqs = temp_pairing_dataframe.sort_values(['semantic_similarity'], ascending=False).groupby(['semantic_similarity'],sort=False)['req_id'].unique()
            # unique_paired_reqs = temp_pairing_dataframe.sort_values(['semantic_similarity'], ascending=False).groupby(['req_id'],sort=False)['req_id'].unique()
            req_count = 0
                
            for unique_req in unique_paired_reqs:
                if req_count < 5:
                    temp_req_row = temp_pairing_dataframe[temp_pairing_dataframe['req_id'] == unique_req]
                    temp_req_row = temp_req_row.sort_values(by=['semantic_similarity'], ascending=False)
                    req_score = temp_req_row['semantic_similarity'].values[0]
                    print('The adjacent node ' + str(adjacent_node) + ' and Requirement ' + str(unique_req) + ' have a relatively high semantic similarity score of ' + str(f"{req_score:.7}"))
                    req_count = req_count + 1
                    

    temp_pairing_dataframe = best_paths_dataframe[best_paths_dataframe['source_req'] == int(requirement_of_interest)]
    count = 0
    if len(temp_pairing_dataframe) > 0:
        print(' ')
        print('********************************************************************************************************************************')
        print(' ')
        print('Requirement ' + str(requirement_of_interest) + ' has been associated with two or more ontology nodes.  Below are the highest semantic pathways between those nodes:')
        print(' ')            
        for row_i, row in temp_pairing_dataframe.iterrows():
                            
            path_score = row['average_semantic_score']
            path_node_names = row['best_pathway_node_names']
            path_node_names = path_node_names.replace('\\',' to ')
            path_node_ids = row['best_pathway_node_ids']
            path_node_ids = path_node_ids.replace('\\',' to ')
            average_over = row['averaged_over']
            
            print('The pathway [' + str(path_node_names) + '] has an average semantic similarity score of ' + str(f"{path_score:.7}") + ' averaged over the ' + str(average_over) + '.')
            count = count + 1
            if count == 3:
                count = 0
                print(' ')
                
    else:
        
        print(' ')
        print('********************************************************************************************************************************')
        print(' ')
        print('Requirement ' + str(requirement_of_interest) + ' was not associated with more than two nodes.  No pathing was attempted as there was not a source and destination pair.')
        print(' ')
        
    print(' ')
    print('********************************************************************************************************************************')
    print(' ')
    print('Score compiler complete')
    print(' ')
    