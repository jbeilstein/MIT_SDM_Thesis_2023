import csv
import math
import pandas as pd
import spacy
##The following code is from https://www.sbert.net/docs/pretrained_models.html and was accessed on 20 Oct 2023

from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-MiniLM-L6-v2')

query_embedding = model.encode('this sentence discusses the cansat')
# query_embedding = model.encode('the cansat attached to rocket')
# query_embedding = model.encode('the cansat maximum altitude is measured in meters')
# passage_embedding = model.encode(['the rocket airframe shall not be used as part of the cansat operation'])
# passage_embedding = model.encode(['The Cansat shall function as a nose cone during the rocket ascent portion of the flight'])
passage_embedding = model.encode(['At 100 meters, the Cansat shall have a descent rate of less than 5 m/s.'])

print("Similarity:", util.dot_score(query_embedding, passage_embedding))
print("Similarity:", util.cos_sim(query_embedding, passage_embedding))

# nlp = spacy.load("en_core_web_lg")

data_file = 'ontology_relationships_two_way.csv'

ontology_dataframe = pd.read_csv(data_file,sep=',')

data_file = 'req_dsm_pairing_token_comparison.csv'

req_req_dataframe = pd.read_csv(data_file,sep=',')



# r_doc = nlp("distance")
# o_doc = nlp("length")

# print(r_doc.similarity(o_doc))
# x=1