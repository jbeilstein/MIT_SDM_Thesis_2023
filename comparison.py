import csv
import math
import pandas as pd
import spacy

# Parts of this code are from from https://spacy.io/
# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")

data_file = 'ontology.csv'

ontology_dataframe = pd.read_csv(data_file,sep=',')

data_file = 'data2024_pathing.csv'

requirements_dataframe = pd.read_csv(data_file,sep=',')

req_ont_pairing = []
column_names = ['req_id','ont_id','ont_name','similarity','ontology_association_truth']

for req_i, req_row in requirements_dataframe.iterrows():
    current_req_matches = []    
    if req_i !=0 and req_row['id_num'] != '' and req_row['id_num'] != 'id_num' and math.isnan(req_row['id_num']) != True:
        if (req_row['functional'] == True):
            req_id = req_row['id_num']   
            req_text = req_row['text']
            req_text = req_text.replace("\n"," ")
            req_doc = nlp(req_text)
                
            # for token in req_doc:
            #     print(token.text, token.lemma, token.pos, token.tag, token.dep_, token.is_alpha, token.is_stop)
            
            for ont_i, ont_row in ontology_dataframe.iterrows():
                if ont_row['component_id'] != '' and ont_row['component_id'] != 'id_num' and math.isnan(ont_row['component_id']) != True:
                    ont_id = ont_row[0]
                    ont_name = ont_row['component_title']
                    ont_bool = req_row[ont_name]
                    ont_name = ont_name.replace('_',' ')
                    ont_name = ont_name.replace('/',' ')
                    ont_text = ont_name + ' ' + ont_row[3] + ' ' + ont_row[4] + ' ' + ont_row[5] + ' ' + ont_row[6]
                    ont_doc = nlp(ont_text)
                    
                    # for token in ont_doc:
                    #     print(token.text, token.lemma, token.pos, token.tag, token.dep_, token.is_alpha, token.is_stop)
                        
                    pairing_score = [req_id, ont_id, ont_name, req_doc.similarity(ont_doc), ont_bool]
                    current_req_matches.append(pairing_score)
                    
            current_req_matches = pd.DataFrame(current_req_matches, columns=column_names)
            best_pairs = current_req_matches.nlargest(4, 'similarity')
            n = best_pairs.shape[0]
            for i in range(0,n):
                req_ont_pairing.append(best_pairs.iloc[i])
            
req_ont_pairing = pd.DataFrame(req_ont_pairing, columns=column_names)
req_ont_pairing.to_csv('req_ont_comparison.csv', index=False)