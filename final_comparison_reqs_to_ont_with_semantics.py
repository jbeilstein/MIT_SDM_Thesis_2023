from spacy.lang.en import stop_words

import csv
import math
import pandas as pd
import spacy

##Parts of the following code are derived from https://www.sbert.net/docs/pretrained_models.html and was accessed on 20 Oct 2023
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-MiniLM-L6-v2')

# Parts of this code are from from https://spacy.io/
# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_lg")

data_file = 'ontology_relationships_two_way.csv'

ontology_dataframe = pd.read_csv(data_file,sep=',')

data_file = 'data2024_final.csv'

requirements_dataframe = pd.read_csv(data_file,sep=',')

req_ont_pairing = []
req_ont_pairing_column_names = ['req_id','ont_id','ont_name','spacy similarity','semantic similarity','source']
# req_ont_pairing_column_names = ['req_id','ont_id','ont_name','similarity','ontology_association_truth']

req_ont_token_pairing = []
req_ont_token_pairing_column_names = ['req_id','ont_id','req_token','ont_token','ont_name','similarity','source']

common_articles = ['the','The','are','is','Is','and','or','of','be','to','To','in','In','that','a','A','an','An','as','for','For','from','From',
                   'it','It','its','have','via','their','there','a','A','with','With','without','Without','on','On','each','Each','all','All',
                   'if','If','by','By','shall','Shall','will','Will','not','Not','at','At','this','This','when','When','than','Than','per',
                   'etc.','more','they','They','them','Them','same','Same','any','Any','only','Only','must','Must','may','May','do','Do','\'s',
                   'can','could','above','below','between','into']
unwanted_str = '`~1!2@3#4$5%6^7&8*9(0)-_=+[{]}]|\;:\'",<.>/?aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ'

current_req_matches = []  
for req_i, req_row in requirements_dataframe.iterrows():   
    if req_row['id_num'] != '' and req_row['id_num'] != 'id_num' and math.isnan(req_row['id_num']) != True:
        # Enable this if you only want to look at functional requirements

        # Enable this if you only want to look at non_functional requirements
        # if (req_row['non_functional'] == True):
        
        # Enable this if you only want to look at all requirements
        # if (req_row['functional'] == True) or (req_row['non_functional'] == True):
    
        # Enable this if you only want to look at all entries in the document
        # if (req_row['id_num'] >= 0):
        req_id = req_row['id_num']   
        req_text = req_row['text']
        req_text = req_text.replace("\n","")
            
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
            # if ont_row['component_id'] != '' and ont_row['component_id'] != 'id_num' and math.isnan(ont_row['component_id']) != True:
            current_token_matches = []                    
            ont_id = ont_row['reference_num']
            ont_name = ont_row['name']
            
            # ont_bool = req_row[ont_name]
            ont_name = ont_name.replace('_',' ')
            ont_name = ont_name.replace('/',' ')
            
            #This next command allows semantic similarity with the ontological names and descriptions
            ont_description = ont_row['description']
            
            #This next command allows semantic similarity with the ontological names and units
            ont_units = ont_row['units']           
            
            #This next command allows semantic similarity with the ontological names and synonyms
            ont_synonyms = ont_row['synonyms']            
            
            #This next command allows semantic similarity with the ontological names and keywords
            if (ont_row['units'] != ' ') and (ont_row['units'] != '') and isinstance(ont_units,str) == True:
                ont_units = ont_row['units'].replace(',',' ')
                ont_units_enable = True
            else:
                ont_units = ""
                ont_units_enable = False
                
            #This next command allows semantic similarity with the ontological names, descriptions, and keywords
            if (ont_synonyms != ' ') and (ont_synonyms != '') and isinstance(ont_synonyms,str) == True:
                ont_synonyms = ont_row['synonyms'].replace(',',' ')
                ont_synonyms_enable = True
            else:
                ont_units = ""
                ont_synonyms_enable = False

                           
            #This section will perform ontology and requirement text semantic similarity with the ontology name
            req1_embedding = model.encode(req_text)
            
            ont_doc = nlp(ont_name)
            for r_token in req_doc:
                if (str(r_token) not in unwanted_str) and (str(r_token) not in common_articles) and (str(r_token) != '\n') and (r_token.dep_ != 'nummod') and (r_token.dep_ != 'punct') and (r_token.dep_ != 'appos') and (str(r_token) not in stop_words.STOP_WORDS):    
                    for o_token in ont_doc:
                        if (str(o_token) not in unwanted_str) and (str(o_token) not in common_articles) and (str(o_token) != '\n') and (o_token.dep_ != 'nummod') and (o_token.dep_ != 'punct') and (o_token.dep_ != 'appos') and (str(o_token) not in stop_words.STOP_WORDS):
                            req_dsm_token_score = [req_id,ont_id,str(r_token), str(o_token), ont_name, r_token.similarity(o_token),'ontology name']
                            if (req_dsm_token_score[4] != 0) and (req_dsm_token_score not in current_token_matches):
                                current_token_matches.append(req_dsm_token_score)    
                            
            #This section will perform ontology and requirement text semantic similarity with the ontology description
            ont_doc = nlp(ont_description)
            for r_token in req_doc:
                if (str(r_token) not in unwanted_str) and (str(r_token) not in common_articles) and (str(r_token) != '\n') and (r_token.dep_ != 'nummod') and (r_token.dep_ != 'punct') and (r_token.dep_ != 'appos') and (str(r_token) not in stop_words.STOP_WORDS):    
                    for o_token in ont_doc:
                        if (str(o_token) not in unwanted_str) and (str(o_token) not in common_articles) and (str(o_token) != '\n') and (o_token.dep_ != 'nummod') and (o_token.dep_ != 'punct') and (o_token.dep_ != 'appos') and (str(o_token) not in stop_words.STOP_WORDS):
                            req_dsm_token_score = [req_id,ont_id,str(r_token), str(o_token), ont_name, r_token.similarity(o_token),'ontology description']
                            if (req_dsm_token_score[4] != 0) and (req_dsm_token_score not in current_token_matches):
                                current_token_matches.append(req_dsm_token_score)    

            #This section will perform ontology and requirement text semantic similarity with the ontology name
            if ont_units_enable == True:
                ont_doc = nlp(ont_units)                
                for r_token in req_doc:
                    if (str(r_token) not in unwanted_str) and (str(r_token) not in common_articles) and (str(r_token) != '\n') and (r_token.dep_ != 'nummod') and (r_token.dep_ != 'punct') and (r_token.dep_ != 'appos') and (str(r_token) not in stop_words.STOP_WORDS):    
                        for o_token in ont_doc:
                            if (str(o_token) not in unwanted_str) and (str(o_token) not in common_articles) and (str(o_token) != '\n') and (o_token.dep_ != 'nummod') and (o_token.dep_ != 'punct') and (o_token.dep_ != 'appos')and (str(o_token) not in stop_words.STOP_WORDS):
                                req_dsm_token_score = [req_id,ont_id,str(r_token), str(o_token), ont_name, r_token.similarity(o_token),'ontology units']
                                if (req_dsm_token_score[4] != 0) and (req_dsm_token_score not in current_token_matches):
                                    current_token_matches.append(req_dsm_token_score)    
                            
            #This section will perform ontology and requirement text semantic similarity with the ontology name
            if ont_synonyms_enable == True:
                ont_doc = nlp(ont_synonyms)
                for r_token in req_doc:
                    if (str(r_token) not in unwanted_str) and (str(r_token) not in common_articles) and (str(r_token) != '\n') and (r_token.dep_ != 'nummod') and (r_token.dep_ != 'punct') and (r_token.dep_ != 'appos') and (str(r_token) not in stop_words.STOP_WORDS):    
                        for o_token in ont_doc:
                            if (str(o_token) not in unwanted_str) and (str(o_token) not in common_articles) and (str(o_token) != '\n') and (o_token.dep_ != 'nummod') and (o_token.dep_ != 'punct') and (o_token.dep_ != 'appos') and (str(o_token) not in stop_words.STOP_WORDS):
                                req_dsm_token_score = [req_id,ont_id,str(r_token), str(o_token), ont_name, r_token.similarity(o_token),'ontology synonyms']
                                if (req_dsm_token_score[4] != 0) and (req_dsm_token_score not in current_token_matches):
                                    current_token_matches.append(req_dsm_token_score)    
                                                                
            req_ont_token_matches = pd.DataFrame(current_token_matches, columns=req_ont_token_pairing_column_names)
            best_token_pairs = req_ont_token_matches[req_ont_token_matches['similarity']>=0.1]
            n = best_token_pairs.shape[0]
            for i in range(0,n):
                req_ont_token_pairing.append(best_token_pairs.iloc[i])                    
                                
            #This section allows a different set of ontology information to be semantically compared to the req_text

            #This next command allows semantic similarity with just the ontological names
            ont_text = ont_name 
            ont_doc = nlp(ont_text)
            ont_embedding = model.encode(ont_name)
            semantic_similarity_name = util.cos_sim(req1_embedding, ont_embedding)
            pairing_score = [req_id, ont_id, ont_name, req_doc.similarity(ont_doc),semantic_similarity_name,'ont_name']
            current_req_matches.append(pairing_score)
            
            #This next command allows semantic similarity with the ontological names and descriptions
            ont_text = ont_description 
            ont_doc = nlp(ont_text)
            ont_embedding = model.encode(ont_description)
            semantic_similarity_description = util.cos_sim(req1_embedding, ont_embedding)
            pairing_score = [req_id, ont_id, 'ont_description', req_doc.similarity(ont_doc),semantic_similarity_description,'ont_description']
            current_req_matches.append(pairing_score)
            
            #This next command allows semantic similarity with the ontological names and keywords
            if ont_units_enable == True:
                ont_text = ont_units
                ont_doc = nlp(ont_text)
                ont_embedding = model.encode(ont_units)
                semantic_similarity_units = util.cos_sim(req1_embedding, ont_embedding)
                pairing_score = [req_id, ont_id, ont_text, req_doc.similarity(ont_doc),semantic_similarity_units,'ont_units']
                current_req_matches.append(pairing_score)
                
            #This next command allows semantic similarity with the ontological names, descriptions, and keywords
            if ont_synonyms_enable == True:
                ont_text = ont_synonyms
                ont_doc = nlp(ont_text)
                ont_embedding = model.encode(ont_synonyms)
                semantic_similarity_synonyms = util.cos_sim(req1_embedding, ont_embedding)
                pairing_score = [req_id, ont_id, ont_text, req_doc.similarity(ont_doc),semantic_similarity_synonyms,'ont_synonyms']
                current_req_matches.append(pairing_score)
            
            #This section will perform ontology and requirement text semantic similarity
            # ont_doc = nlp(ont_text)
            # pairing_score = [req_id, ont_id, ont_name, req_doc.similarity(ont_doc)]
            # current_req_matches.append(pairing_score)                    
            
req_ont_pairing = pd.DataFrame(current_req_matches, columns = req_ont_pairing_column_names)
req_ont_pairing.to_csv('req_to_ont_comparison.csv', index=False)

req_ont_token_pairing = pd.DataFrame(req_ont_token_pairing, columns = req_ont_token_pairing_column_names)
req_ont_token_pairing.to_csv('req_to_ont_token_comparison.csv', index=False)