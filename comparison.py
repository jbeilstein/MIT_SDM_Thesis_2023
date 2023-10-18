import csv
import math
import pandas as pd
import spacy

# Parts of this code are from from https://spacy.io/
# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_lg")

data_file = 'ontology.csv'

ontology_dataframe = pd.read_csv(data_file,sep=',')

data_file = 'data2024_pathing.csv'

requirements_dataframe = pd.read_csv(data_file,sep=',')

req_ont_pairing = []
req_ont_pairing_column_names = ['req_id','ont_id','ont_name','similarity','ontology_association_truth']

req_ont_token_pairing = []
req_ont_token_pairing_column_names = ['req_id','ont_id','req_token','ont_token','ont_name','similarity']

unwanted_str = '`~1!2@3#4$5%6^7&8*9(0)-_=+[{]}]|\;:\'",<.>/?'

for req_i, req_row in requirements_dataframe.iterrows():
    current_req_matches = []    
    if req_i !=0 and req_row['id_num'] != '' and req_row['id_num'] != 'id_num' and math.isnan(req_row['id_num']) != True:
        # Enable this if you only want to look at functional requirements
        # if (req_row['functional'] == True):

        # Enable this if you only want to look at non_functional requirements
        # if (req_row['non_functional'] == True):
        
        # Enable this if you only want to look at all requirements
        # if (req_row['functional'] == True) or (req_row['non_functional'] == True):
    
        # Enable this if you only want to look at all entries in the document
        if (req_row['id_num'] >= 0):
            req_id = req_row['id_num']   
            req_text = req_row['text']
            req_text = req_text.replace("\n"," ")
                
            ##At this point the system has the requirements text for the current requirement row.  
            ##The following section will allow the inclusion of parent statements.  
            # if pd.isnull(req_row['child_of']) != True:
            #     req_text = req_text + ". " + requirements_dataframe.iloc[int(req_row['child_of'])]['text']

            ##The following section will allow the inclusion of child statements.  This can be used independently or in conjunction with the parent statment section above.
            ##This only looks at one generation lower
            # if pd.isnull(req_row['parent_of']) != True:
            #     child_list = req_row['parent_of'].split('/')
            #     n = len(child_list)
            #     for i in range(0,n):
            #         req_text = req_text + ". " + requirements_dataframe.iloc[int(i)]['text']
                
            req_doc = nlp(req_text)
                
            # for token in req_doc:
            #     print(token.text, token.lemma, token.pos, token.tag, token.dep_, token.is_alpha, token.is_stop)
            
            for ont_i, ont_row in ontology_dataframe.iterrows():
                if ont_row['component_id'] != '' and ont_row['component_id'] != 'id_num' and math.isnan(ont_row['component_id']) != True:
                    current_token_matches = []                    
                    ont_id = ont_row[0]
                    ont_name = ont_row['component_title']
                    ont_bool = req_row[ont_name]
                    ont_name = ont_name.replace('_',' ')
                    ont_name = ont_name.replace('/',' ')
                    #This next command allows semantic similarity with just the ontological names
                    # ont_text = ont_name 
                    #This next command allows semantic similarity with the ontological names and descriptions
                    # ont_text = ont_name + '. ' + ont_row[3]
                    #This next command allows semantic similarity with the ontological names and keywords
                    ont_text = ont_name + '. ' + ont_row[4] + '. ' + ont_row[5] + '. ' + ont_row[6]
                    #This next command allows semantic similarity with the ontological names, descriptions, and keywords
                    # ont_text = ont_name + '. ' + ont_row[3] + '. ' + ont_row[4] + '. ' + ont_row[5] + '. ' + ont_row[6]
                    
                    #This section will perform ontology and requirement text semantic similarity with the ont_text selected above
                    ont_doc = nlp(ont_text)
                    
                    for r_token in req_doc:
                        if str(r_token) not in unwanted_str:    
                            for o_token in ont_doc:
                                if str(o_token) not in unwanted_str:
                                    req_ont_token_score = [req_id,ont_id,r_token, o_token, ont_name, r_token.similarity(o_token)]
                                    current_token_matches.append(req_ont_token_score)
                                        
                    req_ont_token_matches = pd.DataFrame(current_token_matches, columns=req_ont_token_pairing_column_names)
                    best_token_pairs = req_ont_token_matches[req_ont_token_matches['similarity']>=0.9]
                    n = best_token_pairs.shape[0]
                    for i in range(0,n):
                        req_ont_token_pairing.append(best_token_pairs.iloc[i])                    
                                        
                    #This section allows a different set of ontology information to be semantically compared to the req_text
    
                    #This next command allows semantic similarity with just the ontological names
                    ont_text = ont_name 
                    #This next command allows semantic similarity with the ontological names and descriptions
                    # ont_text = ont_name + '. ' + ont_row[3]
                    #This next command allows semantic similarity with the ontological names and keywords
                    # ont_text = ont_name + '. ' + ont_row[4] + '. ' + ont_row[5] + '. ' + ont_row[6]
                    #This next command allows semantic similarity with the ontological names, descriptions, and keywords
                    # ont_text = ont_name + '. ' + ont_row[3] + '. ' + ont_row[4] + '. ' + ont_row[5] + '. ' + ont_row[6]
                    
                    #This section will perform ontology and requirement text semantic similarity
                    ont_doc = nlp(ont_text)
                    
                    pairing_score = [req_id, ont_id, ont_name, req_doc.similarity(ont_doc), ont_bool]
                    # print(pairing_score)
                    current_req_matches.append(pairing_score)

                    
            current_req_matches = pd.DataFrame(current_req_matches, columns=req_ont_pairing_column_names)
            best_pairs = current_req_matches.nlargest(4, 'similarity')
            n = best_pairs.shape[0]
            for i in range(0,n):
                req_ont_pairing.append(best_pairs.iloc[i])
            
req_ont_pairing = pd.DataFrame(req_ont_pairing, columns = req_ont_pairing_column_names)
req_ont_pairing.to_csv('req_ont_comparison.csv', index=False)

req_ont_token_pairing = pd.DataFrame(req_ont_token_pairing, columns = req_ont_token_pairing_column_names)
req_ont_token_pairing.to_csv('req_ont_token_comparison.csv', index=False)