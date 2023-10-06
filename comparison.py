import csv
import math
import pandas as pd
import spacy

# Parts of this code are from from https://spacy.io/
# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")

data_file = 'ontology.csv'

ontology_dataframe = pd.read_csv(data_file,sep=',')

data_file = 'parsed_requirements.csv'

requirements_dataframe = pd.read_csv(data_file,sep=',')

req_ont_pairing = []
column_names = ['req_id','ont_id','similarity']

for req_i, req_row in requirements_dataframe.iterrows():
    current_req_matches = []
    if req_row[0] != '' and req_row[0] != 'id_num' and math.isnan(req_row[0]) != True:
        req_id = req_row[0]   
        req_text = req_row[15]
        req_doc = nlp(req_text)
            
        # for token in req_doc:
        #     print(token.text, token.lemma, token.pos, token.tag, token.dep_, token.is_alpha, token.is_stop)
        
    for ont_i, ont_row in ontology_dataframe.iterrows():
        if ont_row[0] != '' and ont_row[0] != 'id_num' and math.isnan(ont_row[0]) != True:
            ont_id = ont_row[0]   
            ont_text = ont_row[1].replace('_',' ') + ' ' + ont_row[3] + ' ' + ont_row[4] + ' ' + ont_row[5] + ' ' + ont_row[6]
            ont_doc = nlp(ont_text)
            
            # for token in ont_doc:
            #     print(token.text, token.lemma, token.pos, token.tag, token.dep_, token.is_alpha, token.is_stop)
                
            pairing_score = [req_id,ont_id,req_doc.similarity(ont_doc)]
            current_req_matches.append(pairing_score)
            
    current_req_matches = pd.DataFrame(current_req_matches, columns=column_names)
    best_pair = current_req_matches.loc[(current_req_matches['similarity'].idxmax())]
    req_ont_pairing.append(best_pair)
            
req_ont_pairing = pd.DataFrame(req_ont_pairing, columns=column_names)
req_ont_pairing.to_csv('req_ont_comparison.csv', index=False)