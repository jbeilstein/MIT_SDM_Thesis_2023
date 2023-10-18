import csv
import math
import pandas as pd
import matplotlib.pyplot as plot
import spacy

from csv import writer

# from spacy.pipeline import EntityRecognizer

# Parts of this code are from from https://spacy.io/
# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_lg")

# nlp = spacy.blank("en")
# config = {"task": {"@llm_tasks": "spacy.NER.v3", "labels": ["PERSON", "ORGANISATION", "LOCATION"]}}
# llm = nlp.add_pipe("llm", config=config)

ont_data_file = 'ontology.csv'

ontology_dataframe = pd.read_csv(ont_data_file,sep=',')

req_data_file = 'data2024_pathing.csv'

requirements_dataframe = pd.read_csv(req_data_file,sep=',')

write_data_file = 'entity_list_document.csv'

req_ont_pairing = []
column_names = ['req_id','ont_id','ont_name','similarity','ontology_association_truth']
running_text = ''

# for req_i, req_row in requirements_dataframe.iterrows():
#     current_req_matches = []    
#     if req_i !=0 and req_row['id_num'] != '' and req_row['id_num'] != 'id_num' and math.isnan(req_row['id_num']) != True:
#         req_id = req_row['id_num']   
#         req_text = req_row['text']
#         req_text = req_text.replace("\n"," ")
#         running_text = running_text + '. ' + req_text

                            
# req_doc = nlp(running_text)

# ent_list = []
# ent_text_merged = ''

# for ent in req_doc.ents:
#     if (ent.label_ != 'CARDINAL') and (ent.label_ != 'DATE') and (ent.label_ != 'TIME'):
#         ent_entry = [ent.text, ent.label_]
#         with open(write_data_file,'a',encoding = "utf-8",newline = '') as object:
#                     write_object = writer(object)
#                     write_object.writerow(ent_entry)
#                     object.close() 

for req_i, req_row in requirements_dataframe.iterrows():
    current_req_matches = []    
    if req_i !=0 and req_row['id_num'] != '' and req_row['id_num'] != 'id_num' and math.isnan(req_row['id_num']) != True:
        req_id = req_row['id_num']   
        req_text = req_row['text']
        req_text = req_text.replace("\n"," ")
        req_doc = nlp(req_text)

        ent_list = []
        ent_text_merged = ''

        for ent in req_doc.ents:
            if (ent.label_ != 'CARDINAL') and (ent.label_ != 'DATE') and (ent.label_ != 'TIME'):
                ent_entry = [ent.text, ent.label_,req_id]
                with open(write_data_file,'a',encoding = "utf-8",newline = '') as object:
                            write_object = writer(object)
                            write_object.writerow(ent_entry)
                            object.close()                           
    
ent_dataframe = pd.read_csv(write_data_file,sep=',')

# for i in ent_dataframe:
#     temp_dataframe_i = ent_dataframe[ent_dataframe[i]==True]
#     index_j = 1
#     for j in ent_dataframe:
#         if i != j:
#             temp_dateframe_j = temp_dataframe_i[temp_dataframe_i[j]==True]
#             if temp_dateframe_j.empty:
#                 count = 0
#             else:
#                 count = temp_dateframe_j.shape[0]
#             dsm.at[i,j] = int(count)
#         index_j = index_j + 1
#     index_i = index_i + 1
                        

# graph = plot.savefig('title_histogram.jpg')

# start_hist = ent_dataframe.hist(column = [1])
# graph = plot.savefig('type.jpg')


# x = ent_list
# llm_ner = nlp.add_pipe("llm_ner")
# This usually happens under the hood
# processed = llm_ner(req_doc)

# token_list = ''

# for token in req_doc:
#     print(token.text, token.lemma, token.pos_, token.tag, token.dep_, token.is_alpha, token.is_stop)
#     token_list = token_list + " " + token.text + "_" + token.pos_
    
# x = token_list