import csv
import math
import pandas as pd
import spacy
import time

start = time.time()
# Parts of this code are from from https://spacy.io/
# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_lg")

data_file = 'data2024_pathing.csv'

requirements_dataframe = pd.read_csv(data_file,sep=',')

req_dsm_pairing = []
req_dsm_pairing_column_names = ['req1_id','req2_id','req_text','req2_text','similarity']

req_dsm_token_pairing = []
req_dsm_token_pairing_column_names = ['req1_id','req2_id','req1_token','req2_token','similarity']

common_articles = ['the','The','are','is','Is','and','or','of','be','to','To','in','In','that','a','A','an','An','as','for','For','from','From',
                   'it','It','its','have','via','their','there','a','A','with','With','without','Without','on','On','each','Each','all','All',
                   'if','If','by','By','shall','Shall','will','Will','not','Not','at','At','this','This','when','When','than','Than','per',
                   'etc.','more','they','They','them','Them','same','Same','any','Any','only','Only','must','Must','may','May','do','Do']
unwanted_str = '`~1!2@3#4$5%6^7&8*9(0)-_=+[{]}]|\;:\'",<.>/?aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ'

for req_i, req_row in requirements_dataframe.iterrows():
    current_req_matches = []    
    if req_i !=0 and req_row['id_num'] != '' and req_row['id_num'] != 'id_num' and math.isnan(req_row['id_num']) != True:
        # Enable this if you only want to look at functional requirements
        # if (req_row['functional'] == True):

        # Enable this if you only want to look at non_functional requirements
        # if (req_row['non_functional'] == True):
        
        # Enable this if you only want to look at all requirements
        # if (req_row['functional'] == True) or (req_row['non_functional'] == True):
    
        # Enable this if you want to look at all entries in the document
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
            
            for req2_i, req2_row in requirements_dataframe.iterrows():
                if req2_row['id_num'] != '' and req2_row['id_num'] != req_row['id_num'] and math.isnan(req2_row['id_num']) != True:                    
                    # Enable this if you only want to look at functional requirements
                    # if (req_row['functional'] == True) and (req2_i > req_i):

                    # Enable this if you only want to look at non_functional requirements
                    # if (req_row['non_functional'] == True) and (req2_i > req_i):
                    
                    # Enable this if you only want to look at all requirements
                    # if ((req2_row['functional'] == True) or (req2_row['non_functional'] == True)) and (req2_i > req_i):
                
                    # Enable this if you want to look at all entries in the document
                    if (req_row['id_num'] >= 0) and (req2_i > req_i):
                        
                        current_token_matches = []                    
                        req2_id = req2_row['id_num']
                        req2_text = req2_row['text']
                        req2_text = req2_text.replace('/',' ')
                        req2_doc = nlp(req2_text)
                        
                        for r_token in req_doc:
                            if (str(r_token) not in unwanted_str) and (str(r_token) not in common_articles) and (str(r_token) != '\n') and (r_token.dep_ != 'nummod') and (r_token.dep_ != 'punct') and (r_token.dep_ != 'appos'):    
                                for r2_token in req2_doc:
                                    if (str(r2_token) not in unwanted_str) and (str(r2_token) not in common_articles) and (str(r2_token) != '\n') and (r2_token.dep_ != 'nummod') and (r2_token.dep_ != 'punct') and (r_token.dep_ != 'appos'):
                                        req_dsm_token_score = [req_id,req2_id,r_token, r2_token, r_token.similarity(r2_token)]
                                        if req_dsm_token_score[4] != 0:
                                            current_token_matches.append(req_dsm_token_score)
                                            
                        req_dsm_token_matches = pd.DataFrame(current_token_matches, columns=req_dsm_token_pairing_column_names)
                        best_token_pairs = req_dsm_token_matches[req_dsm_token_matches['similarity']>=0.9]
                        n = best_token_pairs.shape[0]
                        for i in range(0,n):
                            req_dsm_token_pairing.append(best_token_pairs.iloc[i])                    
                                            
                        #This section allows a different set of ontology information to be semantically compared to the req_text
        
                        #This section will perform ontology and requirement text semantic similarity
                        # req2_doc = nlp(req2_text)
                        
                        # pairing_score = [req_id, req2_id, req_text, req2_text, req_doc.similarity(req2_doc)]
                        # print(pairing_score)
                        # current_req_matches.append(pairing_score)
                    
            current_req_matches = pd.DataFrame(current_req_matches, columns=req_dsm_pairing_column_names)
            # best_pairs = current_req_matches.nlargest(4, 'similarity')
            # n = best_pairs.shape[0]
            # for i in range(0,n):
            #     req_dsm_pairing.append(best_pairs.iloc[i])
            print(req_id)
            print(time.time()-start)
            
# req_dsm_pairing = pd.DataFrame(req_dsm_pairing, columns = req_dsm_pairing_column_names)
# req_dsm_pairing.to_csv('req_dsm_pairing_comparison.csv', index=False)

req_dsm_token_pairing = pd.DataFrame(req_dsm_token_pairing, columns = req_dsm_token_pairing_column_names)
req_dsm_token_pairing.to_csv('req_dsm_pairing_token_comparison.csv', index=False)

